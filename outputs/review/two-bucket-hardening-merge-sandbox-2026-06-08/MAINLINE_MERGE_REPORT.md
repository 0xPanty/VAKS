# Two-Bucket Hardening Mainline Merge Report

Date: 2026-06-08

## Summary

The two-bucket hardening plan has been landed into the mainline architecture
files as small boundary hardening, not as a runtime or schema rewrite.

No commit or push was made.

## Landed Items

Bucket 1:

```text
CI-03 source hash / incremental ingest
CI-09 source adapter ingest contract
CI-02.5 candidate lint before approval
CI-04 decision outcome precondition
```

Bucket 2 non-SCHEMA:

```text
CI-06 context pack evidence envelope
CI-07 context pack budget guardrails
CI-08 source range provenance handle wording
```

SCHEMA unlock:

```text
CI-08 source ranges / quote selectors are provenance handles until evidence_support checks them
CI-07 budget trimming cannot hide warnings / gaps / missing evidence / source-window loss / action risk
```

CI-06 field enumeration stayed out of SCHEMA. The field list remains in
`DEV_CONTEXT.md` and `templates/dev-context-pack.md`.

## Files Changed

```text
SOURCE_INTAKE.md
REVIEW_QUEUE.md
FEEDBACK.md
DEV_CONTEXT.md
SCHEMA.md
templates/source-record.md
templates/review-candidate.md
templates/decision-record.md
templates/dev-context-pack.md
wiki/indexes/knowledge-graph-index.md
```

## Verification

Command:

```powershell
powershell -ExecutionPolicy Bypass -File outputs/review/two-bucket-hardening-merge-sandbox-2026-06-08/mainline-merge-check.ps1
```

Result:

```text
Pass: 27
Fail: 0
HEAD: 4abb84a
```

Checks covered:

```text
CI-03 source hash is source hygiene only
CI-09 adapter ingest does not create reviewed writeback
CI-02.5 candidate lint is review input only
CI-04 decision outcome requires recommendation and user choice or explicit override
CI-06 envelope exists in DEV_CONTEXT/template but not SCHEMA
CI-07 budget trimming cannot hide critical warnings/gaps/source-window loss
CI-08 source ranges remain provenance handles until evidence_support checks them
SCHEMA diff contains exactly two added boundary lines
new hardening blocks do not add runtime/API/MCP/dashboard/SQLite/auto-promotion
```

## SCHEMA Diff Boundary

SCHEMA received exactly two added boundary lines:

```text
1. Source ranges, line ranges, quote selectors, and source spans are provenance handles. They only become support when evidence_support checks that the span bears on the specific target.
2. Budget trimming may reduce context size, but it must not hide critical warnings, gaps, missing evidence, source-window loss, or action risk. If key support is trimmed out, the pack cannot remain action-ready.
```

The CI-06 envelope field enumeration was intentionally not added to SCHEMA.

## Verdict

Positive.

This merge strengthens existing VAKS boundaries without changing the main spine:

```text
source hygiene is not truth
adapter output is not reviewed writeback
candidate lint is not verdict
decision outcome is not truth mutation
context envelope is not truth
budget trimming cannot hide risk
source range is not support by itself
```
