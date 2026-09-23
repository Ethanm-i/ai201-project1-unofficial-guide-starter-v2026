# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Corpus:** `campus_life` (the current project configuration).

**Chunk size:** A target of 400 characters per chunk, including the document title. Keep posts that fit within this target whole. For longer posts, group complete paragraphs up to the target and repeat the title in each chunk. Treat 400 as a soft limit: keep a paragraph intact when splitting it would lose a complete thought.

**Overlap:** Zero characters of body-text overlap. Repeat the document title in each chunk so the course, building, or service being discussed remains clear. If a paragraph depends on the preceding paragraph to make sense, keep them together even if this exceeds the target.

**Baseline observation:** Inspection of the cleaned corpus files found 88 documents, with lengths ranging from 178 to 549 characters and an average of about 317. With the starter's 800-character windows and 120-character overlap, each document fits in one chunk, producing 88 chunks. These numbers were checked from the files; indexing has not been rerun for this proposal.

**Reason:** Short course posts such as `course_hist_118_exams.txt` contain closely related assessment details and should stay together. Longer housing posts such as `housing_old_brewhouse.txt` mix room descriptions, advantages, heating problems, laundry, and noise across paragraphs. A 400-character target gives those longer posts an opportunity to split at existing paragraph boundaries without cutting sentences. Repeating the title prevents a paragraph about heating or laundry from losing the name of the building. Body overlap starts at zero because these posts are already short and unnecessary repetition could crowd retrieval results with duplicate text.

**Status:** This is the proposed strategy before implementation. Next, implement it in `chunker.py::split_documents`, inspect five actual chunks, and revise the target or grouping rule if the chunks need more context. The starter chunker is still in use.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

======================================================================
Chunk 1  |  source: thread_bike_commute.txt#0  |  produced by: chunker.py::fallback_split
======================================================================
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.

--- reply 3 (22 votes) ---
Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

--- reply 4 (5 votes) ---
If you do get one, the campus does free registration and it's the only reason I got mine back after it was taken.

For each one, ask: could someone answer a question using only this,
without reading what came before or after?

**Chunk 1** — source: `` — produced by: ``

```
======================================================================
Chunk 1  |  source: admin_add_drop_deadline.txt#0  |  produced by: chunker.py::split_documents
======================================================================
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `` — produced by: ``

```
======================================================================
Chunk 2  |  source: course_cs_210.txt#0  |  produced by: chunker.py::split_documents
======================================================================
CS 210 Data Structures

I'm a junior and I've done this twice now. Format is lecture with weekly labs; slides go up after class, not before. Assessment: two midterms and a final, all drawn from lecture material rather than the textbook. Midterms are curved, the final is not.

Expect 8 to 10 hours a week outside class.
```

**Chunk 3** — source: `` — produced by: ``

```
======================================================================
Chunk 3  |  source: course_math_220_workload.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Workload for MATH 220 Linear Algebra

People keep asking so: 6 to 8 hours a week, almost all of it on problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `` — produced by: ``

```
======================================================================
Chunk 4  |  source: dining_the_ridgeway_cafe_followup.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Re: The Ridgeway Café

Adding to what people have said about The Ridgeway Café. The wait figure of 10 to 15 minutes at 12:30 matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: seating is tight; about 40 seats for a building of 900. Nobody tells you this at orientation.
```

**Chunk 5** — source: `` — produced by: ``

```
======================================================================
Chunk 5  |  source: housing_morrow_house.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Morrow House — what it's actually like

Just finished a year in this building. Built 1954, partially renovated 2008. Rooms are singles and doubles, hall bathrooms.

```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
What material do CS 210 exams cover?

**Answer:**

```
CS 210 exams are drawn from lecture material rather than the textbook, and they reuse lab problems.


Source: `course_cs_210_exams.txt` (and `course_cs_210.txt`)

Sources retrieved: course_cs_210.txt, course_cs_210_exams.txt, course_cs_340_exams.txt, course_engl_205_exams.txt
```

**My relevance cutoff:** `0.6` (draft for review).

**Retrieval settings:** `TOP_K = 5`, with the current `campus_life` index of 100 chunks from 88 documents. Lower distances indicate closer matches. The gate accepts a question only when its best distance is strictly below `0.6`.

The five in-scope questions below had best distances from 0.1994 to 0.4043. The five questions in `OUT_OF_SCOPE` ranged from 0.8246 to 0.9231. Keeping the starter cutoff of 0.6 puts it between these groups: all five in-scope questions pass, and all five off-topic questions are rejected in this sample. These are measured retrieval results, not a guarantee for unseen questions or a score for generated-answer accuracy.

| Question | In corpus? | Best distance |
|---|---|---|
| When can I drop a course, and when does a W appear on my transcript? | Yes | 0.1994 |
| What material do CS 210 exams cover, and which exams are curved? | Yes | 0.3335 |
| How much weekly work does MATH 220 require? | Yes | 0.3943 |
| When should I visit Ridgeway Cafe to avoid the lunchtime wait? | Yes | 0.2344 |
| How many houses are on campus? | Yes | 0.4043 |
| What is the capital of Mongolia? | No | 0.8246 |
| How do I change the oil in a diesel engine? | No | 0.9231 |
| Who won the 1994 World Cup? | No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8442 |
| How do I write a for loop in Rust? | No | 0.8907 |

**Retrieval review:** The first result for each of the four focused questions contained information that answered it. The fifth question, "How many houses are on campus?", returned five housing descriptions, but those results do not establish the total of seven housing buildings represented in the corpus. Passing the gate is not the same as retrieving a complete answer. For the first three questions, the top sources were `admin_add_drop_deadline.txt`, `course_cs_210_exams.txt`, and `course_math_220_workload.txt`. Lower-ranked results sometimes concerned other courses or administrative topics. Keep top-k at 5 for now: for MATH 220, the fifth result provides additional relevant course context. The model still needs to distinguish the named course or location from unrelated results.

**Limitations and question revision:** The original file contained four completed questions. Several asked for campus-wide counts or summaries. In the initial check, "How many dinning halls are on campus?" retrieved housing documents with a best distance of 0.4969, which passes the cutoff despite not answering the question. The housing-count question also retrieved only part of the evidence needed for a campus-wide total. The current set keeps four focused questions and restores the original housing-count question as the fifth test. Its expected corpus count is seven buildings: Aldridge Hall, Calder Annexe, Fenwick Court, Innisfree Hall, Morrow House, Old Brewhouse, and Tamsin Court. This question preserves an observed retrieval weakness. The focused questions were tested during this review and their expected phrases were added afterward, so this is not a held-out evaluation. A distance gate measures similarity, not whether the retrieved text fully answers a question.

A lower cutoff could reject useful answers; a higher cutoff could admit more unrelated material. The existing grounding instruction requires source-only answers, refusal when the documents do not cover the question, and source filenames. It remains necessary for near misses that pass the gate. The diesel-engine question was also tested through `app.py ask`: it returned "I don't have enough information about that." with zero model calls.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
