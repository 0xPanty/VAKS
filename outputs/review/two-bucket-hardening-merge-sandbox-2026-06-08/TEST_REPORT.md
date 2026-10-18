# Two-Bucket Hardening Merge Sandbox Test

Date: 2026-06-08

## Scope

This sandbox tests the Opus-reviewed two-bucket merge plan without touching the
main architecture files.

Sandbox path:

```text
outputs/review/two-bucket-hardening-merge-sandbox-2026-06-08/
```

Architecture copy:

```text
outputs/review/two-bucket-hardening-merge-sandbox-2026-06-08/architecture/
```

## Bucket Split Tested

Bucket 1: SCHEMA-locked merge candidates.

```text
CI-02.5 Candidate lint before approval
CI-03 Source hash / incremental ingest
CI-04 Decision outcome precondition
CI-09 Source adapter ingest contract
```

Bucket 2: SCHEMA-sensitive candidates.

```text
CI-06 Context pack evidence envelope
CI-07 Context pack budget guardrails
CI-08 Claim-level provenance source ranges
```

## Landing Shape

Bucket 1 landed in sandbox architecture files only:

```text
architecture/REVIEW_QUEUE.md
architecture/SOURCE_INTAKE.md
architecture/FEEDBACK.md
architecture/templates/review-candidate.md
architecture/templates/source-record.md
architecture/templates/decision-record.md
```

Bucket 2 used a split strategy:

```text
architecture/DEV_CONTEXT.md
architecture/templates/dev-context-pack.md
architecture/templates/review-candidate.md
```

The locked architecture SCHEMA was not edited:

```text
architecture/SCHEMA.md
```

Optional SCHEMA unlock candidate is isolated here:

```text
schema-unlocked-candidate/SCHEMA.md
```

The optional SCHEMA candidate differs from the locked baseline by only 3 added
boundary lines:

```text
source ranges / quote selectors are provenance handles, not support by themselves
important or agent-facing context packs preserve primary / neighbors / warnings / gaps / suggested actions
budget trimming cannot hide critical warnings, gaps, missing evidence, source-window loss, or action risk
```

## Pressure Test

Command:

```powershell
powershell -ExecutionPolicy Bypass -File outputs/review/two-bucket-hardening-merge-sandbox-2026-06-08/tests/pressure-test.ps1
```

Result:

```text
Pass: 43
Fail: 0
```

The test checked:

```text
SCHEMA locked architecture unchanged
schema-unlocked candidate exists and is separate
CI-02.5 lint records review input only
CI-03 hash remains source hygiene only
CI-09 adapter contract remains ingest hygiene only
CI-04 outcome requires recommendation plus user choice or explicit override
CI-06 envelope fields exist outside locked SCHEMA
CI-07 budget guardrails block hidden warnings/gaps/source-window loss
CI-08 source ranges remain provenance handles until evidence_support checks them
new blocks do not introduce runtime/API/MCP/dashboard/SQLite/auto-promotion language
```

## Verdict

Positive.

The two-bucket plan is cleaner than a single merge plan. Bucket 1 can be treated
as low-risk hardening because it does not need SCHEMA edits. Bucket 2 should stay
behind an explicit SCHEMA unlock decision, even though the proposed SCHEMA delta
is only 3 boundary lines.

## Overdesign Check

Not overdesigned in this sandbox.

No runtime, dashboard, SQLite, MCP, API, background rewrite, auto-promotion,
scripted repair, or Obsidian sync was added.

## Compatibility Check

No conflict found.

The tested rules strengthen existing VAKS boundaries:

```text
candidate lint = review input, not verdict
hash / adapter = source hygiene, not truth
decision outcome = future calibration, not truth mutation
context envelope = action-facing visibility, not truth
budget guardrails = cannot hide risk
source range = provenance handle, not support by itself
```

## Recommendation

Use this plan for Opus review.

Suggested next merge decision:

```text
1. Approve Bucket 1 for mainline, one atomic commit per CI item.
2. Keep Bucket 2 separate.
3. For Bucket 2, first merge what fits in DEV_CONTEXT/templates.
4. Only then decide whether to unlock SCHEMA for the 3-line boundary delta.
```
