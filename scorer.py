import re

from rapidfuzz import fuzz

# 0-100. How close a fuzzy match has to be to count. partial_ratio finds the
# best-aligned substring, so small wording differences (punctuation, "to" vs
# "-", plurals) still score high without a plain "in" check being fooled.
MATCH_THRESHOLD = 85

# Below this many characters, fuzzy partial_ratio is unreliable — a single
# character (e.g. expects="7") scores ~100 against almost any text, since
# "best-aligned substring" is trivial to satisfy at length 1.
MIN_FUZZY_LENGTH = 4


def _matches(expects: str, text: str) -> bool:
    """Does `text` contain `expects`, allowing for small wording differences?

    Short expected strings (below MIN_FUZZY_LENGTH) skip fuzzy matching AND
    skip plain substring matching — a bare "7" would otherwise "match"
    the 7 hidden inside "1968" or "$1.75". They get a word-boundary match
    instead, so "7" matches "7 dining halls" but not "Built 1968".
    """
    expects = expects.lower().strip()
    text = text.lower()
    if len(expects) < MIN_FUZZY_LENGTH:
        return re.search(rf"\b{re.escape(expects)}\b", text) is not None
    return fuzz.partial_ratio(expects, text) >= MATCH_THRESHOLD


def judge(question, expects, answer, results) -> bool:
    """Does the final generated answer contain what we expected?

    This is what run_eval.py calls automatically for every run — it fills
    in the pass/fail columns in your run log.
    """
    return _matches(expects, answer)


def retrieval_hit(expects, results) -> bool:
    """Criterion 1 evidence: did any RETRIEVED CHUNK contain the answer,
    before generation ever ran?

    `results` is the list store.py::search() returns — each item has a
    `.text`. Called by run_eval.py to score criterion 1 automatically.
    """
    return any(_matches(expects, r.text) for r in results)