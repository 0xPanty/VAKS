---
slice_id: 2026-06-19-p2-104-post-opus-user-approval-decision-packet-sandbox
status: planned
---

# Slice Plan

## Goal

Create a dry-run user approval decision packet for the future post-Opus-PASS state.

## Why This Slice Now

p2-103 says `OPUS_PASS_SANDBOX_CLOSEOUT` may only prepare a user approval decision packet. This slice makes that packet explicit and verifies that Opus PASS is not itself user approval, mainline merge permission, reviewed knowledge, evidence support, action basis, commit, push, or sync.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-104-post-opus-user-approval-decision-packet-sandbox/
```

## Non-Write Scope

- No old slice edits.
- No root architecture document edits.
- No README edits.
- No wiki truth layer edits.
- No templates or tools edits.
- No Obsidian vault writes or sync.
- No commit, push, promotion, or mainline merge.
- No claim that Opus or the user has approved anything.

## Acceptance Criteria

- Read p2-103 outcome matrix.
- Generate a post-Opus user decision packet template.
- Define an exact future approval phrase for a later user approval event.
- Include safe and unsafe fixtures.
- Verify no packet can request or execute user approval before a validated Opus PASS exists.
- Verify even validated Opus PASS does not authorize automatic merge or truth/action writes.
- Pass local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance.

## Stop Conditions

- A real Opus PASS is needed.
- A real user approval is needed.
- Any old slice or protected path would need modification.
- The packet would treat Opus PASS as user approval or merge permission.
