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

"""ASCII transliteration for injected free text.

Takes an arbitrary Unicode string and returns pure 7-bit ASCII, so text
staged into the injection directory never carries non-Latin script into the
assembled prompt. Common technical and typographic symbols are mapped to
readable ASCII equivalents; anything else is decomposed and stripped.

The filter works per character on ``ord(ch) < 128``, which means a literal
ASCII question mark in the input is preserved. This differs from
``paths.ascii_sanitize``, which turns every '?' into a space.
"""

import unicodedata


# Deterministic transliteration of common technical and math symbols. Applied
# to injected free text before it reaches the prompt, so ordinary symbols a
# model summary may emit (delta, ohm, micron, ...) survive as readable ASCII
# rather than tripping the English-only check, which is there to catch real
# non-English script such as CJK or Cyrillic.
_ASCII_MAP = {
    u"Δ": "delta", u"δ": "delta",          # Delta / delta
    u"Ω": "ohm", u"Ω": "ohm",              # Omega / ohm sign
    u"µ": "u", u"μ": "u",                   # micro sign / Greek mu
    u"°": "deg",                                 # degree
    u"±": "+/-",                                 # plus-minus
    u"×": "x", u"÷": "/",                   # multiply / divide
    u"≤": "<=", u"≥": ">=", u"≠": "!=",# le / ge / ne
    u"≈": "~=", u"∞": "inf",                # approx / infinity
    u"→": "->", u"←": "<-",                 # arrows
    u"↔": "<->", u"⇒": "=>",                # arrows
    u"·": "*", u"•": "*",                   # middle dot / bullet
    u"′": "'", u"″": "\"",                  # prime / double prime
    u"–": "-", u"—": "--", u"−": "-",  # en/em dash / minus
    u"‘": "'", u"’": "'",                   # curly single quotes
    u"“": "\"", u"”": "\"",                 # curly double quotes
    u"…": "...",                                 # ellipsis
    u" ": " ", u" ": " ", u" ": " ",   # nbsp / thin spaces
    u"½": "1/2", u"¼": "1/4", u"¾": "3/4",
    u"Σ": "sum", u"σ": "sigma",
    u"§": "S",                                   # section sign
    u"α": "alpha", u"β": "beta", u"γ": "gamma",
    u"λ": "lambda", u"π": "pi", u"θ": "theta",
    u"™": "(TM)", u"®": "(R)", u"©": "(C)",
    u"€": "EUR", u"£": "GBP",
}


def ascii_sanitize(text):
    """Transliterate technical and math symbols to ASCII and strip whatever
    remains non-ASCII, substituting '?' where nothing readable is left.

    A pure, deterministic function with no I/O. The per-character strip
    guarantees no non-Latin script survives into the prompt, while _ASCII_MAP
    keeps the meaning of the common technical glyphs.
    """
    if not text:
        return text
    out = []
    for ch in text:
        if ord(ch) < 128:
            out.append(ch)
            continue
        repl = _ASCII_MAP.get(ch)
        if repl is not None:
            out.append(repl)
            continue
        # Last resort: NFKD-decompose and keep the ASCII remainder, which turns
        # an accented Latin letter into the bare letter; if nothing is left,
        # emit '?'.
        decomp = unicodedata.normalize("NFKD", ch)
        kept = "".join(c for c in decomp if ord(c) < 128)
        out.append(kept if kept else "?")
    return "".join(out)
