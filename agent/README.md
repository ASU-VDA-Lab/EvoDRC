# EvoDRC agent

A drop-in replacement for the `agent/` folder of the
[DAC26 DRC Benchmark](https://github.com/ASU-VDA-Lab/DAC26_DRC_Benchmark).

The benchmark's own agent gets one shot at repairing a layout. This one works in
rounds: it splits the design into pieces, repairs each piece, checks the result,
writes down what it learned, and goes again with better notes.

It only handles **block-level repair**. Cell, polygon and detection cases fall
through to the benchmark's original agent, untouched.

---

## 1. Set up

You need Docker, a benchmark checkout, and to be logged in to Claude on this
machine (`~/.claude/.credentials.json`).

**Build the image** — two steps. The stock image is missing two Python packages.

```bash
cd /path/to/DAC26_DRC_Benchmark
docker build -f Dockerfile.repair -t drc-benchmark-repair:latest .
docker build -t drc-benchmark-repair:latest - < /path/to/EvoDRC/Dockerfile.evodrc
```

Both use the same tag on purpose, so the benchmark picks up the second one with
no extra flags. Check it worked:

```bash
docker run --rm drc-benchmark-repair:latest python3 -c "import networkx, dataclasses; print('ok')"
```

**Install the agent** — copy it in. A symlink will not work.

```bash
cd /path/to/DAC26_DRC_Benchmark
mv agent agent_official_backup
cp -a /path/to/EvoDRC/agent ./agent
```

---

## 2. Run

```bash
cd /path/to/DAC26_DRC_Benchmark
RECORD_TOKENS=1 bash src/evaluate_claude.sh --task repair --case Block5
```

Three things matter here:

* **`RECORD_TOKENS=1` is required.** Without it the run stops immediately with a
  clear error. It cannot be set from inside the image.
* **Run from the benchmark root.** That is where the container's folder mounts
  are resolved from.
* **Use `--task` and `--case`.** Positional arguments are silently ignored, and
  the run quietly sweeps every case instead of the one you meant.

**Each case runs twice.** `--case` filters the case list but *not* the model
list, and the benchmark ships two models — `claude-sonnet-4-6` at medium effort
and `claude-opus-4-6` at high. So the command above is two full runs, and their
results land side by side under different model folders. Budget accordingly.

The benchmark's case list ships two block designs, `Block5` and `Block7`. Asking
for anything else exits immediately with `matched zero entries in CASES`.

---

## 3. Choose a variant

Everything is configured in `agent/evodrc.conf`, a plain `KEY=VALUE` file. It has
to be a file: the benchmark only forwards four environment variables into the
container, and none of them is ours.

The main switch is `ABLATION`:

| `ABLATION` | What it does |
|---|---|
| *(empty)* | The full method. Starts with prior experience and keeps learning. |
| `1` | Starts with the rules but no prior experience. |
| `2` | Starts with experience but stops learning after the first round. |
| `3` | Repairs the design as a whole instead of splitting it up. |

Other useful keys:

| Key | Default | What it does |
|---|---|---|
| `MAX_ITERS` | 3 (5 for `ABLATION=3`) | How many rounds to run |
| `MAX_CONCURRENT_CALLS` | `5` | Most AI calls running at once; `0` = no limit |
| `CALL_COOLDOWN_SECONDS` | `2` | Pause after a call finishes before the next one starts |
| `LEAF_CONCURRENCY` | `5` | Pieces repaired in parallel |
| `KNOW_CONCURRENCY` | `2` | Layers whose notes are updated in parallel |
| `KNOW_ATTEMPTS` | `2` | Retries when a note rewrite breaks the rules |
| `CU_DRC` | `1` | Arbitrate when two pieces edit the same shared thing |
| `CU_DELTA_LE0` | `1` | Also accept repairs that break even, not just improvements |
| `VIA_COMPETITION` | `1` | Arbitrate when two pieces edit the same via cell |

`evodrc.conf` also carries `EVODRC_PROMPT_MODE`, which selects the request
format. Leave it at `exp3`.

Environment variables win over the file, and the file wins over the built-in
defaults. A missing file is fine — the defaults are the full method. A negative
number is treated as a typo and falls back to the default, so you cannot
accidentally switch a safety limit off.

`MAX_CONCURRENT_CALLS` and `CALL_COOLDOWN_SECONDS` cover **every** AI call the
agent makes. They matter because one round can issue a lot of them: each piece
costs one call, and each layer whose notes get updated costs up to six more.

---

## 4. Where the results go

Two places, both under the benchmark folder.

**The repaired layout**, which the benchmark scores:

```
result/<model>-<effort>/block/repair/Block5/Block5_repaired.py
```

**The full record of the run:**

```
temp/data/<variant>/Block5/<model>/
```

`<variant>` is `evodrc`, `ablation1`, `ablation2` or `ablation3`, matching the
`ABLATION` setting. Because the model name is part of the path, the two models
each get their own tree and never overwrite each other. The agent prints the
exact path when it starts. Look for a line beginning `EVODRC_ITER persist_root=`
in the run log.

Inside:

```
db/                  everything learned, one folder per chip layer
skill/               the current notes for each layer, plus rejected drafts
crop_history/        a snapshot of each piece's inputs, per round
iter1/, iter2/ ...   one folder per round
  input/             the layout and violations this round started from
  leaf/<piece>/      the request sent, the repair proposed, the context given
  gated/             whether each repair was accepted, and why
  repaired/          the resulting layout and its remaining violations
  block_result.json  violations before and after
```

> **Re-running a case replaces its previous results.** The folder name has no
> timestamp in it. Copy it aside first if you want to keep it.

This matches the published `data/` tree in the repository root, with these
differences:

* A self-run does not produce `usage/` or the per-round `score/`.
* It adds exactly **one** extra entry: `_inject/` at the top of the results
  folder. That is deliberate. The requests name the knowledge files by their
  full path, and that path must not change between rounds, so the folder they
  are served from has to sit somewhere stable.
* Everything else the run needs internally — working copies, per-call
  records, staging folders, logs — is written **inside the container**, in a
  place that is not shared with your computer, and is discarded when the
  container is removed. None of it reaches your results folder.

### A note about the shared `temp/` folder

The requests name two scratch folders by full path at the top of the
benchmark's `temp/` folder, so EvoDRC creates `conn/` and `drc/` there at the
start of a run and removes them again at the end. Three consequences:

* **Run one case at a time.** Two EvoDRC runs sharing one benchmark folder
  share those two scratch folders, and the first to finish takes them away.
* Any other stray files the AI writes at that level are **left alone on
  purpose** — EvoDRC never chooses those names, so it cannot tell its own
  from another run's. Delete them by hand if you like.
* If a run is killed rather than allowed to finish, `conn/` and `drc/` are
  left behind at that folder and no later run will clear them — delete the
  two folders by hand before the next run.

---

## 5. How a round works

1. **Split** the design into pieces small enough to reason about. Neighbouring
   pieces in the same row are merged into one unit, so a "piece" is often a group.
2. **Repair** every piece — one AI call each, running in parallel up to the limit.
3. **Check** each proposed repair against the connectivity that must be preserved.
   This is a plain calculation, not an AI judgement. Broken repairs are dropped.
4. **Arbitrate** when several pieces want to change the same shared thing: each
   candidate is measured for real, and the best one wins.
5. **Assemble** the accepted repairs and run a full design rule check.
6. **Learn.** For each layer that was touched, two independent rewrites of its
   notes are drafted — one building on the existing notes, one written fresh from
   the evidence alone — and a separate judging step picks at most one. Rejected
   drafts are kept.
7. **Repeat** with the repaired layout. Stops early if the design is clean or
   nothing is repairable.

The notes reach the AI **by file path, never pasted into the request**, so the
knowledge base can grow without bloating the prompt.

---

## 6. When something goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| Stops at once, complains about `RECORD_TOKENS` | launched without it | add `RECORD_TOKENS=1` |
| Runs cases you did not ask for | positional arguments are ignored | use `--task` and `--case` |
| `ModuleNotFoundError: networkx` | second image build was skipped | see step 1 |
| Complains `check_connectivity` is missing | not launched through `evaluate_claude.sh` | use the documented command |
| `RuntimeError` about `ABLATION` | typo in `evodrc.conf` | see the table in section 3 |
| A previous run's results are gone | expected — re-running replaces them | copy the folder aside first |
| Stops with `refusing to annotate a FROZEN benchmark input` | a script pointed the splitter at the benchmark's own `testcase/` files | copy the layout to a writable folder first and work on the copy |

Some things are non-fatal by design. If one piece fails to merge correctly, that
piece is skipped and the round continues. If the arbitration step fails, assembly
falls back to first-come-first-served for that round. Both are logged.

---

## 7. What is in this folder

| Path | Role |
|---|---|
| `agent.py` | entry point the benchmark calls |
| `prompt_format.py` | builds the request from the case description |
| `skill.md` | the fixed background instructions |
| `prompts/` | per-task templates |
| `evodrc.conf` | **the settings file** (section 3) |
| `knowledge/cla/` | starting notes for the full method |
| `knowledge/cold_start/` | starting notes for `ABLATION=1` — rules only |
| `knowledge/deck_map.json` | which design rule belongs to which layer |
| `src/` | the repair pipeline |
| `src/iter/` | the round loop: splitting, scheduling, checking, learning |

Nothing is written into this folder while running — it is mounted read-only.
