#BSD 3-Clause License
#
#Copyright (c) 2026, ASU-VDA-Lab
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#################################################################################

"""Process-wide gate that every model call in the agent passes through.

Repair work and knowledge work run in separate thread pools that know nothing
about each other, so neither pool's size bounds the total number of calls in
flight. ``CallGate`` supplies that bound, plus a pause after each call:

  (a) MAX_CONCURRENT_CALLS   the maximum number of calls in flight at once,
                             across every call class, process-wide;
  (b) CALL_COOLDOWN_SECONDS  after a call completes, the slot it freed stays
                             closed for this many seconds before the next
                             queued call may start on it.

Work stays pipelined rather than batched: as soon as a credit matures the next
queued caller takes it, so the per-pool concurrency settings still act as
sub-caps below the global one. Internally the gate holds ``cap`` credits;
``release()`` appends ``clock() + cooldown_s`` to a maturity list instead of
returning a credit directly, and ``acquire()`` harvests matured entries before
spending. A single ``threading.Condition`` guards both structures, and waiting
on it releases the lock, so a cooling slot lets a caller with an already-free
credit through.

Repair calls are gated at the subprocess boundary: leaf_runner runs as a child
process, so schedule._run_one holds the slot for the child's whole lifetime.
Each child makes exactly one model call, so the bound is conservative -- the
slot is also held during the child's parsing tail. Knowledge calls run in this
process and are gated around the call itself.
"""

import contextlib
import os
import sys
import threading
import time


DEFAULT_MAX_CONCURRENT = 5
DEFAULT_COOLDOWN_S = 2.0

_GATE = [None]                 # the process-wide singleton, in a cell
_GATE_LOCK = threading.Lock()  # guards lazy construction and reset

_VERBOSE = os.environ.get("EVODRC_THROTTLE_LOG", "") == "1"


def _log(msg):
    if _VERBOSE:
        sys.stderr.write("[throttle] %s\n" % msg)


class CallGate(object):
    """Global in-flight cap combined with a post-completion cooldown.

    ``max_concurrent <= 0`` builds an unlimited gate, where acquire and
    release only keep counters and neither blocks nor applies a cooldown.
    """

    def __init__(self, max_concurrent, cooldown_s, clock=time.monotonic):
        self.cap = int(max_concurrent)
        self.unlimited = self.cap <= 0
        self.cooldown_s = max(0.0, float(cooldown_s))
        self._clock = clock
        self._cond = threading.Condition()
        self._free = 0 if self.unlimited else self.cap
        self._maturity = []        # clock() times at which spent credits return
        self._live = 0             # calls currently in flight
        self._peak = 0             # high-water mark of _live

    # -- introspection ----------------------------------------------------
    def in_flight(self):
        with self._cond:
            return self._live

    def peak(self):
        with self._cond:
            return self._peak

    def free(self):
        """Credits spendable right now, including matured cooldowns.
        An unlimited gate reports -1, having no finite budget."""
        if self.unlimited:
            return -1
        with self._cond:
            self._harvest(self._clock())
            return self._free

    def pending_cooldowns(self):
        """Credits still cooling down. Matured credits are harvested first, so
        one that no acquire has picked up yet counts as free rather than
        pending; otherwise an idle gate would report an inflated backlog."""
        if self.unlimited:
            return 0
        with self._cond:
            self._harvest(self._clock())
            return len(self._maturity)

    # -- internals (caller must hold self._cond) --------------------------
    def _harvest(self, now):
        """Move every matured credit back into the free pool."""
        if not self._maturity:
            return
        keep = []
        for m in self._maturity:
            if m <= now:
                self._free += 1
            else:
                keep.append(m)
        self._maturity = keep

    # -- the gate ---------------------------------------------------------
    def acquire(self, label=""):
        """Block until a credit is spendable, then spend it.

        Returns the seconds waited, measured by this gate's clock. Safe to
        call from any number of threads."""
        if self.unlimited:
            with self._cond:
                self._live += 1
                if self._live > self._peak:
                    self._peak = self._live
            return 0.0
        t_enter = self._clock()
        with self._cond:
            while True:
                now = self._clock()
                self._harvest(now)
                if self._free > 0:
                    self._free -= 1
                    self._live += 1
                    if self._live > self._peak:
                        self._peak = self._live
                    waited = now - t_enter
                    _log("acquire [%s]: free=%d live=%d cooling=%d "
                         "waited=%.2fs" % (label, self._free, self._live,
                                           len(self._maturity), waited))
                    return waited
                # Nothing spendable: sleep until the earliest cooldown
                # matures, or wait for a release() notification if none is
                # pending. Condition.wait releases the lock, so another thread
                # can take a free credit while this one waits.
                step = (max(0.0, min(self._maturity) - now)
                        if self._maturity else None)
                _log("WAIT %s [%s] cap=%d cooling=%d"
                     % ("%.2fs" % step if step is not None else "for-release",
                        label, self.cap, len(self._maturity)))
                self._cond.wait(timeout=step)

    def release(self, label=""):
        """Record that a call finished, successfully or not. Its credit
        becomes spendable ``cooldown_s`` from now, and waiters are notified so
        an untimed wait wakes and can re-arm itself with a timeout."""
        with self._cond:
            self._live = max(0, self._live - 1)
            if self.unlimited:
                return
            if self.cooldown_s <= 0:
                self._free += 1
            else:
                self._maturity.append(self._clock() + self.cooldown_s)
            _log("release [%s]: free=%d live=%d cooling=%d"
                 % (label, self._free, self._live, len(self._maturity)))
            self._cond.notify_all()


# ===========================================================================
# Process-wide singleton
# ===========================================================================
def _env_num(name, default, cast):
    """Read a non-negative number from the environment.

    A negative value is invalid and falls back to ``default``; it must never
    become "unlimited" or "no cooldown", which is how ``cap < 0`` would behave
    in :class:`CallGate`. An explicit 0 keeps its meaning. This mirrors the
    equivalent checks in ``conf``, and both are needed because ``get_gate()``
    reads ``os.environ`` directly and therefore also covers the leaf
    subprocess, where ``conf.resolve()`` never runs."""
    raw = (os.environ.get(name) or "").strip()
    if not raw:
        return default
    try:
        val = cast(raw)
    except (TypeError, ValueError):
        return default
    if val < 0:
        _log("%s=%r is negative -- using default %r" % (name, raw, default))
        return default
    return val


def get_gate():
    """Return the process-wide gate, building it on first use.

    It reads ``os.environ`` rather than a config object: ``conf.resolve()``
    has already written the resolved MAX_CONCURRENT_CALLS and
    CALL_COOLDOWN_SECONDS back into the environment, and going through the
    environment keeps this module usable from the leaf subprocess, where no
    RunConfig exists."""
    gate = _GATE[0]
    if gate is not None:
        return gate
    with _GATE_LOCK:
        if _GATE[0] is None:
            cap = _env_num("MAX_CONCURRENT_CALLS", DEFAULT_MAX_CONCURRENT, int)
            cool = _env_num("CALL_COOLDOWN_SECONDS", DEFAULT_COOLDOWN_S, float)
            _GATE[0] = CallGate(cap, cool)
            _log("gate built: cap=%d cooldown=%.2fs" % (cap, cool))
        return _GATE[0]


def reset_for_test(max_concurrent=None, cooldown_s=None, clock=None):
    """Rebuild the process-wide gate with explicit settings.

    With no arguments the singleton is simply cleared, so the next
    ``get_gate()`` re-reads the environment."""
    with _GATE_LOCK:
        if max_concurrent is None and cooldown_s is None and clock is None:
            _GATE[0] = None
            return None
        cap = (max_concurrent if max_concurrent is not None
               else _env_num("MAX_CONCURRENT_CALLS", DEFAULT_MAX_CONCURRENT,
                             int))
        cool = (cooldown_s if cooldown_s is not None
                else _env_num("CALL_COOLDOWN_SECONDS", DEFAULT_COOLDOWN_S,
                              float))
        _GATE[0] = CallGate(cap, cool, clock or time.monotonic)
        return _GATE[0]


@contextlib.contextmanager
def call_slot(label=""):
    """Context manager that every model call runs inside.

    The ``try/finally`` returns the credit even when the call raises, so a
    failing backend cannot leak a slot and stall the run."""
    gate = get_gate()
    gate.acquire(label)
    try:
        yield gate
    finally:
        gate.release(label)
