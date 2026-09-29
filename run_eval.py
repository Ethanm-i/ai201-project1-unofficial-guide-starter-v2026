#!/usr/bin/env python3
"""
Run your test questions repeatedly and write the results down.

    python run_eval.py                 three runs, the default
    python run_eval.py --runs 5        more runs
    python run_eval.py --label after   name this run, e.g. before/after a fix

This does the mechanical half of unit 2 for you: it asks each of your questions
the same way three separate times, with caching turned off so you get three
real answers, and writes everything into results/ as a table with one row per
question.

It also puts every question in `OUT_OF_SCOPE` through retrieval and the gate
and records what happened, so criterion 3 — the one about out-of-corpus
questions — has evidence in the same file as the other four. That part costs
nothing: a question the gate refuses never reaches the model.

That table is the raw material for your run log, not the run log itself. The
submission template wants one row per *criterion* — aggregating your questions
up into your criteria is your work, not the script's.

⚠️ What it does NOT do is decide whether an answer's wording is exactly right.

Criterion 1 (retrieved chunk contains the answer) is scored automatically via
`scorer.py::retrieval_hit(expects, results) -> bool`, if you've built it —
until then that column is blank. Criterion 2 (every answer names a source) is
checked automatically in this file (`_names_a_source`), since it's a
structural check rather than a judgment call. Criteria 4 and 5 are yours to
score by hand from the "Real output" section, since criteria.md doesn't define
a machine-checkable target for them.
"""

import argparse
import datetime as dt
import sys
from pathlib import Path

import config
import questions as qs

# Targets from criteria.md. Keep these in sync by hand if you revise a target
# there — criteria.md is free-form prose, so there's nothing to parse it from.
CRITERION_1_TARGET = 4  # of 5: retrieved chunks contain the answer
CRITERION_2_TARGET = 5  # of 5: every answer names a source
CRITERION_3_TARGET = 4  # of 5: gate stops out-of-corpus questions


def load_retrieval_hit():
    """Use scorer.py's retrieval_hit if the student has built it."""
    try:
        import scorer  # noqa: PLC0415
    except ImportError:
        return None
    fn = getattr(scorer, "retrieval_hit", None)
    return fn if callable(fn) else None


def _names_a_source(answer: str, results) -> bool:
    """Does the answer literally name at least one retrieved source file?

    Checked against the full filename and its stem without the extension,
    since an answer might drop the ".txt" or wrap the name in backticks.
    """
    lowered = answer.lower()
    for r in results:
        stem = r.source.rsplit(".", 1)[0]
        if r.source.lower() in lowered or stem.lower() in lowered:
            return True
    return False


def run_once(question: str, top_k, threshold, corpus, variant):
    """One question, one run. Returns the answer and what retrieval gave us."""
    from store import search
    import gate
    from generate import answer_from_chunks

    results = search(question, top_k=top_k, corpus=corpus, variant=variant)
    decision = gate.check(results, threshold=threshold)

    if not decision.passed:
        return gate.REFUSAL, results, decision

    # cache=False on purpose. Three runs have to be three real answers.
    answer = answer_from_chunks(question, results, cache=False)
    return answer, results, decision


def main():
    parser = argparse.ArgumentParser(description="Run the test questions and log the results.")
    parser.add_argument("--runs", type=int, default=3, help="runs per question (default 3)")
    parser.add_argument("--label", default="", help="a name for this run, e.g. 'before'")
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--variant", default="default")
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--threshold", type=float, default=None)
    args = parser.parse_args()

    corpus = args.corpus or config.CORPUS
    top_k = args.top_k or config.TOP_K
    threshold = config.THRESHOLD if args.threshold is None else args.threshold

    items = qs.answered()
    if not items:
        print(
            "questions.py has no questions in it yet.\n"
            "Milestone 2 asks you to write five. Fill them in and run this again.",
            file=sys.stderr,
        )
        sys.exit(1)

    retrieval_hit = load_retrieval_hit()
    if retrieval_hit is None:
        print("No scorer.retrieval_hit found — criterion 1 will be blank.")
        print("Build scorer.py::retrieval_hit(expects, results) to score it automatically.\n")

    if args.runs < 3:
        print(f"⚠️  {args.runs} run(s). The submission asks for three.\n")

    transcript = []
    rows = []

    for item in items:
        question = item["question"]
        expects = item.get("expects", "")
        print(f"\n{question}")

        crit1_runs = []
        crit2_runs = []
        for run in range(1, args.runs + 1):
            answer, results, decision = run_once(
                question, top_k, threshold, corpus, args.variant
            )

            crit1 = retrieval_hit(expects, results) if retrieval_hit else None
            crit2 = _names_a_source(answer, results)
            crit1_runs.append(crit1)
            crit2_runs.append(crit2)

            def _mark(v):
                return {True: "pass", False: "fail", None: "—"}[v]

            print(
                f"  run {run}: criterion 1 (retrieval) {_mark(crit1)}, "
                f"criterion 2 (names source) {_mark(crit2)}  "
                f"(best distance {decision.best_distance:.3f})"
            )

            transcript.append(
                {
                    "question": question,
                    "run": run,
                    "answer": answer,
                    "chunks": [
                        {"source": r.source, "distance": r.distance, "text": r.text}
                        for r in results
                    ],
                    "best_distance": decision.best_distance,
                    "gate_passed": decision.passed,
                    "crit1": crit1,
                    "crit2": crit2,
                }
            )

        rows.append(
            {
                "question": question,
                "expects": expects,
                "crit1_runs": crit1_runs,
                "crit2_runs": crit2_runs,
            }
        )

    gate_rows = check_out_of_scope(top_k, threshold, corpus, args.variant)

    write_report(
        rows, transcript, gate_rows, args, corpus, top_k, threshold,
        scored=retrieval_hit is not None,
    )


def check_out_of_scope(top_k, threshold, corpus, variant):
    """Put every OUT_OF_SCOPE question through retrieval and the gate.

    Criterion 3 in criteria.md is about questions the corpus doesn't cover, and
    it needs evidence in the run log like the other four. This costs nothing:
    a question the gate refuses never reaches the model, so there is no API
    call and no reason to run it three times — retrieval is deterministic and
    the gate is a comparison against a fixed number.
    """
    from store import search
    import gate

    questions = getattr(qs, "OUT_OF_SCOPE", [])
    if not questions:
        return []

    print("\nOut-of-scope questions (the gate should refuse these):")
    rows = []
    for question in questions:
        results = search(question, top_k=top_k, corpus=corpus, variant=variant)
        decision = gate.check(results, threshold=threshold)
        refused = not decision.passed
        print(f"  {'refused' if refused else 'LET THROUGH'}  "
              f"(best distance {decision.best_distance:.3f})  {question}")
        rows.append(
            {
                "question": question,
                "refused": refused,
                "best_distance": decision.best_distance,
            }
        )

    kept = sum(r["refused"] for r in rows)
    print(f"  -> gate refused {kept} of {len(rows)}")
    return rows


def _mark(v) -> str:
    return {True: "pass", False: "fail", None: " "}[v]


def write_report(rows, transcript, gate_rows, args, corpus, top_k, threshold, scored):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = len(rows[0]["crit2_runs"]) if rows else 0
    total_q = len(rows)
    total_oos = len(gate_rows)
    run_headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    run_divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        f"- Produced by: `run_eval.py::main`",
        f"- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`",
        f"- Scoring: `scorer.py::retrieval_hit` (criterion 1), "
        f"`run_eval.py::_names_a_source` (criterion 2)",
        f"- Corpus: `{corpus}` (index variant `{args.variant}`)",
        f"- top-k: {top_k} · relevance cutoff: {threshold}",
        f"- Runs per question: {n}, caching off",
        f"- When: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    # --- Summary: one row per criterion, matching the README's table -------
    def verdict_for(counts, target):
        return "MET" if counts and all(c >= target for c in counts) else "MISSED"

    lines += [
        "## Summary — one row per criterion",
        "",
        f"| Criterion | Target | {run_headers} | Verdict |",
        f"|---|---|{run_divider}|---|",
    ]

    if scored:
        crit1_counts = [
            sum(1 for r in rows if r["crit1_runs"][i]) for i in range(n)
        ]
        cells = " | ".join(f"{c}/{total_q}" for c in crit1_counts)
        v = verdict_for(crit1_counts, CRITERION_1_TARGET)
        lines.append(
            f"| 1. Retrieved chunk contains the answer | {CRITERION_1_TARGET} of {total_q} "
            f"| {cells} | {v} |"
        )
    else:
        blanks = " | ".join([" "] * n)
        lines.append(
            f"| 1. Retrieved chunk contains the answer | {CRITERION_1_TARGET} of {total_q} "
            f"| {blanks} | — (build scorer.retrieval_hit) |"
        )

    crit2_counts = [sum(1 for r in rows if r["crit2_runs"][i]) for i in range(n)]
    cells2 = " | ".join(f"{c}/{total_q}" for c in crit2_counts)
    v2 = verdict_for(crit2_counts, CRITERION_2_TARGET)
    lines.append(
        f"| 2. Every answer names a source | {CRITERION_2_TARGET} of {total_q} "
        f"| {cells2} | {v2} |"
    )

    if gate_rows:
        refused = sum(r["refused"] for r in gate_rows)
        oos_cells = " | ".join([f"{refused}/{total_oos}"] * n)
        v3 = "MET" if refused >= CRITERION_3_TARGET else "MISSED"
        lines.append(
            f"| 3. Gate stops out-of-corpus questions | {CRITERION_3_TARGET} of {total_oos} "
            f"| {oos_cells} | {v3} |"
        )

    lines += [
        "",
        "> Criteria 4 and 5 are yours — criteria.md doesn't define a countable",
        "> check for them, so this script can't score them. Judge those by hand",
        "> from the real output below.",
        "",
        "---",
        "",
        "## Criterion 1 detail — one row per question",
        "",
        "Produced by `scorer.py::retrieval_hit`. `pass` means the match in",
        "scorer.py found `expects` inside at least one retrieved chunk's text.",
        "",
    ]

    if scored:
        lines += [f"| Question | {run_headers} |", f"|---|{run_divider}|"]
        for row in rows:
            cells = " | ".join(_mark(v) for v in row["crit1_runs"])
            q = row["question"].replace("|", "\\|")
            lines.append(f"| {q} | {cells} |")
    else:
        lines.append("> scorer.py has no `retrieval_hit` function yet, so this is blank.")

    lines += [
        "",
        "---",
        "",
        "## Criterion 2 detail — one row per question",
        "",
        "Produced by `run_eval.py::_names_a_source`. `pass` means the answer",
        "text literally contains one of the retrieved chunks' filenames.",
        "",
        f"| Question | {run_headers} |",
        f"|---|{run_divider}|",
    ]
    for row in rows:
        cells = " | ".join(_mark(v) for v in row["crit2_runs"])
        q = row["question"].replace("|", "\\|")
        lines.append(f"| {q} | {cells} |")

    if gate_rows:
        lines += [
            "",
            "---",
            "",
            "## Criterion 3 — the relevance gate on out-of-corpus questions",
            "",
            f"Produced by `run_eval.py::check_out_of_scope`, cutoff {threshold}. "
            f"Refused {refused} of {total_oos}.",
            "",
            "Retrieval is deterministic and the gate is a comparison against a",
            "fixed number, so these do not vary between runs — one pass over the",
            "list is the whole measurement.",
            "",
            "| Out-of-scope question | Best distance | Gate |",
            "|---|---|---|",
        ]
        for row in gate_rows:
            question = row["question"].replace("|", "\\|")
            gate_cell = "refused" if row["refused"] else "**let through**"
            lines.append(f"| {question} | {row['best_distance']:.3f} | {gate_cell} |")

    lines += [
        "",
        "---",
        "",
        "## Real output",
        "",
        "This is what the system actually produced, including the full text of",
        "every retrieved chunk. Paste the relevant parts into your README",
        "underneath the tables above — the rubric asks for real output as text,",
        "not a description of it.",
        "",
    ]

    for entry in transcript:
        lines += [
            f"### {entry['question']} — run {entry['run']}",
            "",
            f"- Best distance: {entry['best_distance']:.4f} "
            f"({'passed' if entry['gate_passed'] else 'refused by'} the gate)",
            f"- Criterion 1 (retrieval contains answer): {_mark(entry['crit1'])}",
            f"- Criterion 2 (answer names a source): {_mark(entry['crit2'])}",
            "",
            "**Retrieved chunks:**",
            "",
        ]
        for chunk in entry["chunks"]:
            lines += [
                f"`{chunk['source']}` — distance {chunk['distance']:.4f}",
                "```",
                chunk["text"],
                "```",
                "",
            ]
        lines += [
            "**Answer:**",
            "",
            "```",
            entry["answer"],
            "```",
            "",
        ]

    path.write_text("\n".join(lines), encoding="utf-8")

    import generate as gen

    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print(gen.usage())
    print("\nCommit this file. It's the evidence the run actually happened.")


if __name__ == "__main__":
    main()
