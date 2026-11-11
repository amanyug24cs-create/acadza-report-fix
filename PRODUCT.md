# `PRODUCT.md` — Product Thinking: Student Trust, Safety Boundaries & Next-Gen Loops

## 1. Who Loses the Most When a Question Is Broken — and How Our Design Reflects That

**The serious 17-year-old JEE/NEET aspirant taking a timed mock test at 11 PM loses the most.**
When a question has a wrong answer key (`R001`–`R005`), a malformed MCQ key array (`R020`: `["A, B, D"]`), or a wrong question type (`R021`: SCQ stored as MCQ with `["", "B"]`), the damage is not just a lost $+4 / -1$ mark:
1. **Cognitive & Time Spiral**: A sincere student who derives $V = \sqrt{40^2 + (60-30)^2} = 50\text{ V}$ (`R003`) or $\tau = 3/\ln 8 = 1.44\text{ min}$ (`R021`) wastes 6–8 minutes doubting their own fundamentals, re-solving twice (`R029`), and losing confidence right before the real exam.
2. **Compounding Cohort Harm**: Every hour a broken question stays live in an 8-lakh question bank, dozens more students hit the exact same landmine.
3. **Faculty Burnout**: Because ~35–40% of student reports are false alarms (`no_error`, `not_actionable`, `display_issue`), faculty get fatigued wading through noise and take days to reach the true critical defects.

**How our design reflects this:**
* **Instant Auto-Healing for Deterministic High-Stakes Bugs**: Confirmed key errors (`R001`–`R005`, `R020`), type mismatches (`R021`), and solution-verified missing stem values (`R006`, `R007/R008`) are auto-applied immediately once independent solve + solution agreement + scope guards pass—cutting time-to-fix from days to seconds.
* **Urgency-First Faculty Triage Queue**: Our console groups duplicate reports by `questionId` (so 3 reports on the LCR circuit appear as one card) and ranks `faculty_review` items above `auto_apply` audits and `no_change` noise, ordered by **Student Harm Severity × Report Count**.
* **Pedagogical, Non-Dismissive Student Replies**: When a student is wrong (`no_error`), our reply never says *"Question is correct."* It pinpoints the exact step they missed—e.g., forgetting to subtract $V_S = 8\text{ V}$ from $V_P = 22\text{ V}$ (`R044`), converting $0.08\text{ m}$ to $8\text{ cm}$ (`R032`), or multiplying total charge by $64$ on coalescing drops (`R043`)—turning a frustrating error report into a 10-second micro-tutoring moment.

---

## 2. What We Would NEVER Let the AI Auto-Apply — and Why

Even beyond `taxonomy.json`'s six `auto: false` categories (`identical_options`, `diagram`, `wrong_question`, `unsound`, `wrong_chapter`, `syllabus`), we enforce **four hard red lines** that the AI may *suggest* in the console diff preview but may **never** write to production without human click-approval:

1. **Inventing or Restoring Distractor Options (e.g., `R009`/`R010` vs. `R011`, and `R015`)**:
   If the missing/blank option is the *keyed answer* and the stored solution proves its exact value (`R011`: Option C is blank, key is C, solution proves $|\vec{F}_{12}| = |\vec{F}_{21}| \implies 1:1$), auto-apply is safe. If the missing or duplicate option is a *distractor* (`R009`/`R010` missing Option D when C is the key; `R015` duplicate `0 W` options), a poorly chosen distractor can accidentally create a *second* correct answer or give away the key by scale. Distractors are authored pedagogy—always human-approved.
2. **Any Edit Where the Independent Solver and Stored Solution Disagree**:
   We only auto-apply an `answer_key` or `stem_data` change when our **Stage 1 Blind Solver** and the **stored solution** independently converge on the exact same value. If the solution itself is self-contradictory or physically broken (`R034`, where both Assertion and Reason are false and the stored solution hallucinates $I = 2I_0\cos^2(\phi/2)$), the AI must halt and escalate as `unsound`.
3. **Mutating Numbers or Conditions in the Question Stem When Not Backed 100% by the Solution**:
   Changing a stem value to match a wrong key can break physical realizability or invalidate historical attempt analytics for thousands of past test-takers.
4. **Diagram Generation, Question Deactivation, or Syllabus/Chapter Re-Tagging (`R023`, `R025`, `R026`, `R042`)**:
   Moving a question across chapters (`R023`, `R042`) affects active test-series blueprints and adaptive practice pools; faculty must confirm the target concept/sub-concept node.

---

## 3. One Metric We Would Watch in Week 1

**Metric:** **Verified-Defect Student Exposure Rate (VDSER)** — *the number of student question attempts served on questions that currently have an unresolved true defect, divided by total student attempts, paired with a **0% Harmful Auto-Edit Rate** (faculty rollback rate on `auto_apply` commits).*

$$\text{VDSER} = \frac{\sum_{q \in \text{ConfirmedDefects}} \text{StudentAttemptsWhileBroken}(q)}{\text{TotalStudentAttempts}} \quad \text{and} \quad \text{Auto-Edit Precision} = 1 - \frac{\text{FacultyRollbacks}}{\text{TotalAutoApplies}}$$

* **Why this metric (and not "average ticket resolution time")**: Ticket resolution time can be gamed by auto-closing everything. VDSER measures what actually hurts Acadza's learners: *how many students stepped on a known broken question after the first student reported it?* With our engine auto-fixing deterministic defects in $<5\text{ seconds}$ and floating `faculty_review` blockers to the top of the 10 PM console, VDSER on deterministic defects drops to **0 additional harmed students after the first report**, while tracking Faculty Rollback Rate (target: **$0\%$ rollbacks**) keeps the AI honest.

---

## 4. One Idea Beyond This Brief We Would Pitch to Acadza

### **"Zero-Report Telemetry Triage + Retroactive Marks Reconciliation"**
Why wait for a student to type *"ans galat hai"*? Only ~2% of students who hit a broken question actually tap "Report error"—the other 98% silently lose marks and trust.
1. **Pre-Report Telemetry Trigger**: Whenever a question with $>50$ attempts exhibits a **Top-Decile Cohort Inversion** (i.e., students in the $90\text{th}+$ percentile of that test select Option A $>70\%$ of the time while the stored key is Option C, as in `R001`–`R003`, or $0\%$ of top students get an MCQ right, as in `R020`/`R021`), automatically trigger our **Stage 1 Blind Solver + Proactive Bank Scanner** *before a single student files a report*.
2. **Retroactive Marks Healing + Push Notification**: When an `answer_key` or `type_mismatch` fix is applied (auto or faculty-approved), automatically recompute scores for every student who attempted that question in the last 30 days and send a 1-line notification: *"Good news! Question #14 in Mock Test 7 had a key error (C → A). Your score has been updated by +5 marks (from 172 to 177)."* Nothing builds deeper student word-of-mouth trust in a JEE/NEET platform than proactively giving back marks they unfairly lost.
