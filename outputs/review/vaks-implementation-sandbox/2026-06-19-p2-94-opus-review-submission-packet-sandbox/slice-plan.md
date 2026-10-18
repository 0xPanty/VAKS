---
slice_id: 2026-06-19-p2-94-opus-review-submission-packet-sandbox
status: planned
---

# Slice Plan

## Goal

Create a directly usable Opus review submission packet for the VAKS sandbox closeout evidence.

## Why This Slice Now

p2-93 produced an Opus-reviewable closeout packet. The remaining practical gap is execution: Opus needs a concise prompt, evidence manifest, and result intake gate so the user can obtain an external conclusion without guessing what to send or how to interpret it.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-94-opus-review-submission-packet-sandbox/
```

## Non-Write Scope

- No old slice edits.
- No root architecture document edits.
- No README edits.
- No wiki truth layer edits.
- No templates or tools edits.
- No Obsidian vault writes or sync.
- No commit, push, promotion, or mainline merge.
- No claim that Opus has already approved anything.

## Acceptance Criteria

- Produce a copy-paste Opus review prompt.
- Produce an evidence manifest with exact local paths and required review questions.
- Produce a result intake gate defining acceptable Opus conclusions and what each means.
- Include fixtures and failure cases.
- Verify locally that the packet is coherent, references p2-93 evidence, and keeps all authority flags false.
- Pass Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance.

## Stop Conditions

- The work requires calling Opus directly.
- Any protected path or old slice edit is required.
- The packet would need to claim Opus approval before external review occurs.
- Reviewer, Boundary Auditor, or Product Acceptance returns a blocking result.

