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

This assistant answers questions using the `campus_life` documents about courses, dining, housing, and campus rules. It searches for relevant passages and uses them to write a short answer with source filenames. A relevance cutoff blocks clearly off-topic questions before they reach the model. Questions that require counting every location can still fail because retrieval may return only some of the needed documents.

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

The good: cheapest housing tier by about $900 a year, and the singles are real singles.

The bad: known damp problem on the ground floor; two rooms were taken offline in 2024.

For each one, ask: could someone answer a question using only this,
without reading what came before or after?

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

**1. Chunking:** I used AI implement my chunking rules and provide me with a preview of the code before using it. I got back the code reviewed it and made sure that it was implementing the set rules.

**2. Retrieval:** I used AI to test retrieval and help choose a cutoff. and to review my quesitions to make them more forcused and it replaced the questions with focused ones.I left one of the question to show the gaps in and the limitation of the retrieval

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
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 4/5 | 4/5 | 4/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks identify their topic and contain understandable thoughts without cut-off sentences | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Housing-count answer reports the seven buildings represented in the corpus | 1 of 1 | 0/1 | 0/1 | 0/1 | MISSED |

**Criteria 4 and 5 clarification (after the baseline run):** These measurable targets clarify the original descriptions in `criteria.md`; they were not defined before testing. Evidence: `results/run_2026-09-29_1703_before.md`.

**Criterion 4 method:** Manually inspected the first retrieved chunk for each of the five questions in each run: `admin_add_drop_deadline.txt`, `course_cs_210_exams.txt`, `course_math_220_workload.txt`, `dining_the_ridgeway_cafe_followup.txt`, and `housing_aldridge_hall.txt`. All five identify their topic and contain understandable thoughts without sentences cut off by chunking. These same chunks appear in all three runs, so the counts repeat. This assesses chunk readability, not whether the chunk answers the question; the housing description is readable but does not establish a campus-wide count.

**Criterion 5 method:** Checked the answer to "How many houses are on campus?" in each run. All three say there is not enough information rather than giving seven, so each scores 0/1. The refusal avoids inventing a total, but the counting target is still missed.

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.6. Refused 5 of 5.

Retrieval is deterministic and the gate is a comparison against a
fixed number, so these do not vary between runs — one pass over the
list is the whole measurement.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.923 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.891 | refused |

### When can I drop a course, and when does a W appear on my transcript? — run 1

- Best distance: 0.1994 (passed the gate)
- Criterion 1 (retrieval contains answer): pass
- Criterion 2 (answer names a source): pass

**Retrieved chunks:**

`admin_add_drop_deadline.txt` — distance 0.1994
```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

`admin_withdrawal_deadline.txt` — distance 0.4426
```
On the withdrawal deadline

Withdrawal is a different thing from dropping and has a different date. Dropping ends at week six. Withdrawal runs to week ten, requires an adviser signature, and puts a W on the transcript that doesn't affect GPA. The two dates appear on different pages of the registrar's site and this catches people every year.
```

`admin_transcript_requests.txt` — distance 0.5263
```
On the transcript requests

Official transcripts cost $8 and take three business days electronically, or ten by post. Unofficial ones are free and instant from the student portal, and are accepted by most employers and by every graduate programme at the application stage.
```

`admin_pass_fail_option.txt` — distance 0.5351
```
On the pass/fail option

Any course outside your major can be taken pass/fail, and — the part nobody mentions — you can declare it as late as week eight, after you've seen your midterm. A pass needs a C- or better. Two per year, maximum eight across a degree.
```

`admin_grade_appeals.txt` — distance 0.5930
```
On the grade appeals

A grade appeal starts with the instructor and has to be raised within fifteen days of the grade posting. Only after that does it go to the department. Skipping the instructor step gets the appeal returned, which wastes most of the fifteen days.
```

**Answer:**

```
You can drop a course through the end of week six. A drop after week two shows as a W on your transcript. 

Source: `admin_add_drop_deadline.txt`
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | Four of five questions had answer-bearing chunks in every run, meeting the 4/5 target; the housing-count question lacked the complete evidence. |
| 2 | Every answer names a source | MISSED | Only four of five answers named a source file in each run, below the 5/5 target; the housing responses omitted filenames. |
| 3 | Gate stops out-of-corpus questions | MET | The gate refused all five off-topic questions, exceeding the 4/5 target; this single deterministic check is repeated across the three columns. |
| 4 | Sampled chunks identify their topic and are understandable without cut-off sentences | MET under revised criterion | The first retrieved chunk for each of the five questions passed manual inspection in all three runs, meeting the revised 4/5 target. |
| 5 | Housing answer reports seven buildings represented in the corpus | MISSED under revised criterion | The housing answer supplied no total in any run, scoring 0/1 each time against the revised 1/1 target. |

Evidence: `results/run_2026-09-29_1703_before.md`. Criteria 4 and 5 use the post-baseline clarifications recorded beneath the original wording in `criteria.md`.

arguement of the opposite side verdict from claude

**1. You said MET (4/5). Argue MISSED:**
Your own README admits the disqualifying flaw: *"The focused questions were tested during this review and their expected phrases were added afterward, so this is not a held-out evaluation."* You wrote the `expects` strings — "week six," "lecture material," "6 to 8 hours" — **after** seeing what the corpus already said, then built a fuzzy matcher to look for exactly those phrases. That's not measuring retrieval quality, it's measuring whether you can find text you already know exists. A criterion is only evidence if it could plausibly have failed by surprise; this one was constructed backward from the answer key. 4/5 under those conditions isn't a MET, it's a foregone conclusion.

**2. You said MISSED (4/5, needed 5/5). Argue MET:**
Look at what the "failure" actually is: in all three runs, the housing-count answer is a refusal — *"I don't have enough information to determine how many houses are on campus."* `generate.py`'s own grounding instruction explicitly demands this behavior: *"If the documents don't cover the question, say you don't have enough information. Do not guess."* A refusal is not "an answer without a source" — it's the system correctly declining to fabricate one. If you exclude the one case where citing a source would mean citing a source for a fact it doesn't have, every real, substantive answer the system produced named a source in **all 3 runs, 4 for 4**. Counting a deliberate, correct refusal as a strike against "names a source" punishes exactly the behavior your grounding instruction was designed to reward.

**3. You said MET (5/5, needed 4/5). Argue MISSED:**
Check the actual distances: 0.825, 0.923, 0.886, 0.844, 0.891 — every out-of-scope question landed nowhere near the 0.6 cutoff. These questions ("capital of Mongolia," "oil change," "1994 World Cup") aren't adjacent to your corpus at all; they're maximally, obviously off-topic. A gate that refuses these tells you almost nothing about whether it can catch the failure mode that actually matters: a plausible-sounding, *almost*-covered question. Notice your housing-count question — a question your corpus genuinely can't answer — scored 0.404, comfortably on the "pass" side of the gate. That's the real stress case, and it's not in your OUT_OF_SCOPE set at all. 5/5 on an easy test tells you the gate works when nothing is close; it tells you nothing about whether it works when something merely resembles being close, which is the only place a relevance gate is actually hard.

**4. You said "MET under revised criterion." Argue MISSED:**
You already know this corpus has a broken chunk: `course_math_220.txt` contains *"I lived here my sophomore year"* — a sentence that describes living in a building, sitting inside a math course document. It's not cut off, it's actively wrong for its context, which is arguably worse than the truncation the criterion was written to catch. Your revision scoped the sample down to *"the first retrieved chunk for each test question"* — and by coincidence, that broken sentence lives in `course_math_220.txt`, which retrieves at distance 0.5091, dead last of 5 results for the MATH 220 question, never first. The revision rules say a revision is legitimate only when the original criterion **couldn't be measured** — not when re-scoping it conveniently steps around a defect you already know is sitting in the corpus. This reads exactly like the thing the professor's own instructions warn against: *"Lowering a target because you missed it... costs you the point."* You didn't lower a number, but you narrowed the sample in a way that guarantees the one known bad chunk never gets checked.

**5. You said "MISSED under revised criterion." Argue MET:**
Zero out of five housing documents retrieved even mention a total count — and at `TOP_K = 5`, the system is structurally incapable of ever retrieving all 7 housing chunks (`Calder Annexe` and `Morrow House` never even entered the result set in any of the three runs). This isn't a system failing to notice an answer that was in front of it — the number "7" appears **nowhere in the corpus** as a stated fact; it exists only because you counted files yourself. A criterion that can only be satisfied by the model inferring a fact from evidence that was never given to it isn't testing your retrieval pipeline — it's testing whether the model will guess when it shouldn't. Given that it refused instead of guessing, three times, consistently, that's arguably the system behaving exactly as designed — which makes this a flaw in the criterion's construction, not a MISSED result for the pipeline.

## Diagnoses

Evidence: `results/run_2026-09-29_1703_before.md`.

**Criterion 2 — Generation:** The housing question passed the gate, but the model returned a refusal without a source filename in all three runs. The prompt requests citations, but the pipeline does not enforce them on generated refusals.

**Criterion 5 — Retrieval:** The housing-count question retrieved descriptions of only five buildings. Calder Annexe and Morrow House were absent, and none of the retrieved chunks stated the total. With incomplete evidence, the model declined to give a count.

**Pattern:** Both misses occurred on the housing-count question. Incomplete retrieval prevented the count, and the resulting refusal omitted citations. The refusal avoided guessing, but still missed the recorded targets.

**Possible reaseon that are cause question five to fail**

it looks like the program can only retrive 5 results ann there are 7 housing buildings hence 2 building are left out.  And the chunking systm made it more worse since not almost all the house documents are split into two chunks. In addition, in all the documents there is no document that says that there are 7 housing buildings. and this makes it hard for the system to give the correct number.

## The Improvement

**What I changed:** Increased `TOP_K` in `config.py` from 5 to 10. This experiment changed only the number of retrieved chunks; the questions, chunking strategy, relevance cutoff of 0.6, grounding prompt, and scoring rules stayed the same.

**Why I picked it:** The housing-count question retrieved only five building descriptions in the baseline, so increasing top-k tested whether more complete retrieval would let the model supply the count.

### Run Log — After

Before evidence: [17:03 baseline report](results/run_2026-09-29_1703_before.md).
After evidence: [22:56 after report](results/run_2026-09-29_2256_after.md), produced by `run_eval.py::main`, with three runs per question and caching off.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 4/5 | 4/5 | 4/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks identify their topic and contain understandable thoughts without cut-off sentences | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Housing-count answer reports the seven buildings represented in the corpus | 1 of 1 | 0/1 | 0/1 | 0/1 | MISSED |

**Manual scoring check:** The saved report automatically scores criterion 1 as 5/5. That is a false positive: `scorer.py::retrieval_hit` matches the expected string `7` in `transit_walking.txt`, where it refers to minutes, not a housing total. The table above records the manually verified 4/5; the original report is preserved. All seven documented buildings now appear across the housing results, but no single retrieved chunk contains the total, and the descriptions do not establish an exhaustive campus-wide list.

For criterion 4, the first retrieved chunk for each question was the same as in the baseline, so the same five-chunk readability check still scores 5/5. All three housing answers refused to provide a count and named no source file, leaving criteria 2 and 5 missed. All five off-topic questions were refused, so criterion 3 repeats the single gate-check result across all three columns.

**Before and after comparison:** Each cell lists runs 1, 2, and 3.

| Criterion | Before: top-k 5 | After: top-k 10, manually checked |
|---|---|---|
| 1. Retrieval | 4/5, 4/5, 4/5 | 4/5, 4/5, 4/5 |
| 2. Source filenames | 4/5, 4/5, 4/5 | 4/5, 4/5, 4/5 |
| 3. Off-topic refusals | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 |
| 4. Sampled chunk readability | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 |
| 5. Housing count | 0/1, 0/1, 0/1 | 0/1, 0/1, 0/1 |

**Actual after-run evidence:** Housing question, run 3, from `results/run_2026-09-29_2256_after.md`. Retrieval: `store.py::search`; answer: `generate.py::answer_from_chunks`.

Excerpt from retrieved `transit_walking.txt` (distance 0.6040), showing the misleading numeric match:

```text
Rough numbers, measured rather than guessed. Aldridge Hall to the science quad: 4 minutes. Fenwick Court to central campus: 18 minutes. Morrow House to Kestrel Commons: 7 minutes. Library to Ridgeway Café: 3 minutes.
```

Full generated answer:

```text
I do not have enough information to determine the total number of houses on campus, as the provided documents only describe specific residential buildings and do not list all of them.
```

**Did it help?** Raising top-k retrieved descriptions of all seven documented housing buildings, but it did not improve any manually checked criterion: the housing answer still refused the count and omitted citations in all three runs. The extra results also included study-room booking and walking times, adding irrelevant context. The apparent automatic retrieval gain came from a scoring false positive, not a supported housing total.

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
