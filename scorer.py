from rapidfuzz import fuzz

# 0-100. How close a fuzzy match has to be to count. partial_ratio finds the
# best-aligned substring, so small wording differences (punctuation, "to" vs
# "-", plurals) still score high without a plain "in" check being fooled.
MATCH_THRESHOLD = 85


def judge(question, expects, answer, results) -> bool:
    """Does the final generated answer contain what we expected?

    This is what run_eval.py calls automatically for every run — it fills
    in the pass/fail columns in your run log.
    """
    return fuzz.partial_ratio(expects.lower().strip(), answer.lower()) >= MATCH_THRESHOLD


def retrieval_hit(expects, results) -> bool:
    """Criterion 1 evidence: did any RETRIEVED CHUNK contain the answer,
    before generation ever ran?

    `results` is the list store.py::search() returns — each item has a
    `.text`. Not called automatically by run_eval.py; call it yourself
    when filling in criterion 1's numbers for the README.
    """
    target = expects.lower().strip()
    return any(
        fuzz.partial_ratio(target, r.text.lower()) >= MATCH_THRESHOLD
        for r in results
    )