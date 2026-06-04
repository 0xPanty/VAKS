# VAKS Targeted Testing Plan

This note distills the previous Grok testing advice into a VAKS-specific test plan. It removes generic Obsidian advice and risky shortcuts that do not fit the current architecture.

## Purpose

Use this document after Deep Research returns. The goal is not to prove that VAKS is "right" in one run. The goal is to compare the current baseline against small, narrow design candidates and find where the workflow is too noisy, too heavy, unclear, or unsafe.

The main question:

```text
Can VAKS become lighter in ordinary use while preserving evidence discipline at promotion, review, strong relation, context-pack, and action-basis gates?
```

## Architecture Boundary

Test the VAKS evidence workflow, not only the Obsidian container.

VAKS workflow under test:

```text
source
-> candidate point
-> review / evidence packet
-> reviewed claim or review-ready claim
-> relation / point collision when needed
-> context pack
-> action basis
-> feedback / use ledger
```

Obsidian container checks are secondary:

```text
folders
properties
templates
Dataview / Bases dashboards
graph performance
search performance
mobile ergonomics
```

Container tests can show whether the vault is usable at scale. They cannot prove evidence support, source independence, action readiness, or truth confidence.

## Current Pain Points To Test

| Pain point | Plain-language meaning | What to test |
| --- | --- | --- |
| Source independence unclear | We often cannot tell whether two sources are genuinely independent, copied from the same origin, or derived from each other. | Whether the review form helps humans mark `independent`, `same-origin`, `derived`, or `unknown` without pretending the system can compute it automatically. |
| `processing_level` vs `source_access` confusing | "How deeply did we process this?" is easy to mix up with "how much of the source did we actually access?" | Whether templates and examples make the distinction obvious enough during real source intake. |
| `coverage_map` too heavy | For small claims or normal answers, the coverage map can become more work than the judgment itself. | Whether compact coverage cards or progressive disclosure reduce lines and fields without hiding important gaps. |
| Feedback / activation still manual | Feedback changes activation and scope fit, but there is no runtime proof yet. | Whether feedback records can stay short while still making future activation changes auditable. |
| Small claims too heavy | Tiny reviewed claims may trigger full machinery. | Whether a review-lite path can handle low-risk claims without weakening promotion/action-basis gates. |
| Support/refine collision format awkward | Some evidence does not cleanly support or refute; it refines scope. | Whether a compact support/refine collision format works better than a full collision packet. |

## Data Source Strategy

Use a mixed test set. Do not rely on random dummy notes for evidence-aware testing.

| Source type | Use it for | Do not use it for |
| --- | --- | --- |
| SciFact | Scientific claim, evidence abstract, support/refute/not-enough labels, rationale-style evidence checks. Good first dataset for reviewed claims and evidence packets. | Full real-world web provenance or long-horizon feedback testing. |
| AVeriTeC | Real-world fact-checking style claims with web evidence, question-answer evidence, and justifications. Good for query-scope, multi-evidence sufficiency, and action-basis style testing. | Cheap large-scale testing. It is heavier than SciFact. |
| AmbiFC | Ambiguous or conflicting factual claims. Good for testing `unknown`, scope limits, and avoiding overconfident review. | Simple happy-path throughput testing. |
| FEVER | Large claim-evidence corpus. Good for scale, field empty-rate, dashboard, and retrieval/noise stress tests. | Domain-specific scientific judgment or source-independence proof. |
| OpenDebateEvidence | Large argument/evidence material. Good for support/refine collision, evidence summarization, and argument mining style stress. | Verdict-style fact verification. It is not a clean claim-verdict dataset. |
| SciClaimHunt | Candidate scientific claim mining reference. Useful as an exploratory supplement. | Main benchmark until its shape and fit are verified. |
| Loki / OpenFactVerification-style repos | Reference implementations for fact-verification pipelines, logging, and evaluation harnesses. | Direct dependency or truth authority. Borrow mechanisms only. |
| Generic Obsidian sample vaults / Testing Vault plugin | Obsidian container tests: properties, templates, graph, Dataview/Bases, performance. | VAKS evidence support, source independence, review-lite correctness, or action readiness. |
| Full papers / repos / articles | Final anchor tests with real messy sources and exact source spans. | Thousand-scale testing. Too expensive and noisy for early iteration. |

## Test Phases

### Phase 0: Baseline From Existing Trial

Use the current E2E trial and lightweight variant as the starting point.

Baseline artifacts:

```text
06_e2e_trial/
07_lightweight_variant/
```

Baseline findings to preserve:

```text
The VAKS spine can run.
Ordinary capture and ordinary query were not made heavier.
Friction concentrated in review records, coverage_map, collision format, and feedback logs.
The lightweight variant helped, but did not solve source independence, naming confusion, coverage_map compression, or runtime proof.
```

### Phase 1: Small High-Fidelity Test

Size:

```text
10 to 50 cases
```

Recommended mix:

```text
SciFact: 10 to 20 cases
AVeriTeC: 5 to 10 cases
AmbiFC: 5 to 10 cases
Full real source anchors from papers/repos: 3 to 5 cases
```

Run manually or semi-manually. The point is to see where the form hurts.

Each candidate design must include:

```text
1 true failure case that should trigger the stricter rule
3 ordinary cases that should not trigger extra burden
1 to 2 boundary cases
```

Output:

```text
candidate | true failure caught | ordinary false positive | added burden | overlap/conflict with current rules | recommendation
```

### Phase 2: Medium Metrics Test

Size:

```text
100 to 300 cases
```

Recommended mix:

```text
SciFact for claim/evidence review
AVeriTeC for real-world multi-evidence review
FEVER for volume and field-noise statistics
AmbiFC for ambiguity and conflict handling
```

Goal:

```text
Measure where records become noisy.
Measure which fields are frequently empty, unknown, guessed, or repeatedly confusing.
Compare baseline vs review-lite vs compact coverage variants.
```

This phase should not force every case through full review. Most cases should remain candidate, lite, or diagnostic unless their gate requires stricter treatment.

### Phase 3: Large-Scale Stress Test

Size:

```text
1000+ cases
```

Use mostly already labeled datasets and cached outputs.

Goal:

```text
field empty-rate
unknown-rate
review-lite coverage
full evidence packet trigger rate
average record length
feedback/event log growth
dashboard/query performance
```

Do not manually review every case. Use random audit samples and deep dives only on suspicious clusters.

### Phase 4: Obsidian Container Test

This is separate from evidence testing.

Use:

```text
Testing Vault plugin
sample vaults
generated dummy markdown notes
distilled fake notes with realistic properties
```

Test:

```text
folder layout
template ergonomics
Dataview / Bases queries
dashboard speed
search
graph noise
mobile behavior
file count scaling
```

This phase can use hundreds or thousands of dummy notes because it tests the container, not the evidence logic.

## Metrics To Record

| Metric | Meaning | Use |
| --- | --- | --- |
| Average required fields per record | How much manual structure each note asks for. | Detect template heaviness. |
| Average record lines | How long records become. | Detect log noise. |
| Field empty-rate | How often a field stays blank. | High empty-rate means optional, rename, merge, or remove from ordinary path. |
| `unknown` / `guessed` rate | How often reviewers cannot responsibly fill a value. | Identify fields that are hard in reality. |
| Full Evidence Packet trigger rate | How often strict review opens. | If too high, the gate may be over-triggering. |
| Review-lite coverage rate | How many cases can safely avoid full packets. | Estimate how much friction can be removed. |
| Coverage map average rows | How large answer/action coverage records become. | Test compact coverage designs. |
| Source independence unknown rate | How often independence cannot be determined. | This should guide reviewer prompts, not fake automation. |
| Feedback average lines / fields | How heavy each feedback event becomes. | Test feedback stub vs full use-ledger record. |
| False-lite rate | Cases that took the light path but should have escalated. | Key safety metric. Any serious miss means the gate is too loose. |
| Ordinary-flow false positive rate | Ordinary capture/query cases that got dragged into strict review. | Protect lazy-gate principle. |
| Conflict / omission catch rate | Known conflicts or gaps caught during review. | Diagnostic only, not truth confidence. |
| Action-basis upgrade rate | How many reviewed items become action basis. | Observe only. Do not optimize upward as a success metric. |

## Design Variants To Compare

### Variant A: Current Baseline

Run the current documented flow without new changes.

Use it as the control group.

### Variant B: Review-Lite For Small Claims

Use for low-risk, narrow, non-action-basis claims.

Must still escalate when:

```text
promotion requested
strong relation requested
action basis requested
risk-sensitive answer
explicit contradiction
stale / contested claim
important scope limit
known omission or counterevidence
```

Measure:

```text
record length reduction
field empty-rate reduction
false-lite rate
ordinary-flow false positive rate
```

### Variant C: Compact Coverage Card

Use a short coverage card by default, with full `coverage_map` only when the answer or action basis depends on multiple key claims.

Compact card should preserve:

```text
answer claim
source/evidence anchor
covered / partial / missing
known counterevidence or gap
scope limit
escalation note if needed
```

Measure:

```text
coverage_map rows avoided
missed gap rate
reviewer time
answer usefulness
```

### Variant D: Feedback Stub

Use short feedback by default.

Positive feedback stays weak:

```text
scope-fit improved
useful in this context
no truth confidence change
```

Negative or corrective feedback escalates:

```text
review_due
affected claim / relation / context pack
reason
next review note
```

Measure:

```text
feedback record length
activation usefulness
review_due precision
manual activation trace clarity
```

### Variant E: Source Independence Prompting

Do not try to auto-prove source independence.

Instead test whether the reviewer prompt makes these states easier to choose:

```text
independent
same-origin
derived
unknown
```

Measure:

```text
unknown rate
reviewer disagreement
cases where source count was mistaken for independence
cases where copied summaries were mistaken for independent support
```

### Variant F: `processing_level` vs `source_access` Clarification

Test whether template wording separates:

```text
source_access = what source material was actually accessible
processing_level = how deeply VAKS processed that material
```

Examples to include:

```text
full text accessed, light processing only
abstract accessed, heavy review on one claim
repo skimmed, no code execution
paper fully read, no promotion
```

Measure:

```text
misfilled fields
reviewer correction count
field empty-rate
time to fill source record
```

## Bad Ideas Removed From The Grok Advice

Do not use these as VAKS evidence tests:

```text
random dummy notes as the main test set
graph beauty as evidence quality
generic starter vaults as proof that VAKS works
```

Do not use these as review rules:

```text
evidence count >= 3 means review-lite is safe
same URL/date means same evidence
high benchmark score means truth confidence
LLM judge agreement means reviewed support
Dataview dashboard pass means knowledge is correct
positive feedback means truth confidence increases
action-basis upgrade rate should be maximized
```

These are allowed only as diagnostics:

```text
benchmarks
LLM judge outputs
dashboard summaries
field statistics
retrieval scores
feedback counts
```

## Recommended Sandbox Layout

Keep the main vault read-only during tests.

Suggested path:

```text
C:\Users\Administrator\Documents\资料库_vaks_testing_sandbox_YYYY-MM-DD
```

Suggested structure:

```text
datasets/
  scifact/
  averitec/
  ambifc/
  fever/
  open-debate-evidence/

samples/
  phase1-small/
  phase2-medium/
  phase3-large/
  full-source-anchors/

runs/
  baseline/
  review-lite/
  compact-coverage/
  feedback-stub/
  source-independence-prompt/
  processing-vs-access/

metrics/
  field-empty-rate.md
  record-length.md
  gate-trigger-rate.md
  false-lite-audit.md
  feedback-noise.md

friction/
  reviewer-notes.md
  confusing-fields.md
  escalation-misses.md

audit/
  random-sample-review.md
  known-failure-cases.md
  overlap-with-main-rules.md
```

## Final Decision Table

Every tested candidate should end with this table:

| Candidate | Dataset / sample | True failure caught? | Ordinary cases overburdened? | Log noise reduced? | Safety regression? | Overlaps current rule? | Recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Review-lite small claim | TBD | TBD | TBD | TBD | TBD | TBD | land / narrow / reject |
| Compact coverage card | TBD | TBD | TBD | TBD | TBD | TBD | land / narrow / reject |
| Feedback stub | TBD | TBD | TBD | TBD | TBD | TBD | land / narrow / reject |
| Source independence prompt | TBD | TBD | TBD | TBD | TBD | TBD | land / narrow / reject |
| Processing vs access wording | TBD | TBD | TBD | TBD | TBD | TBD | land / narrow / reject |

## Mainline Writeback Rule

Only consider mainline writeback after a candidate passes all checks below:

```text
It solves a measured pain point.
It does not move truth authority into retrieval, dashboards, tests, or feedback.
It does not require SCHEMA changes as the first move.
It does not make ordinary capture or ordinary query heavier.
It does not duplicate an existing REVIEW_QUEUE / SOURCE_INTAKE / FEEDBACK rule.
It has at least one true-failure case, ordinary no-trigger cases, and boundary cases.
```

Preferred landing order:

```text
1. operating convention
2. template wording
3. REVIEW_QUEUE narrow check
4. anti-pattern note
5. maintenance-manifest lint
6. SCHEMA only if repeated sandbox evidence proves the field is structurally necessary
```

