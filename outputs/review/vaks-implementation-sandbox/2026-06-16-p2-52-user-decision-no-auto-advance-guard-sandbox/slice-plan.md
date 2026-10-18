---
record_kind: sandbox_slice_plan
slice_id: 2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox
status: built_pending_review
---

# Slice Plan

## Target

Create a no-auto-advance guard for the p2-51 user decision request packet.

## Why This Slice Exists

p2-51 asks the user whether to keep the sandbox as reference, open a future
read-only promotion review planning slice, ask for a separately scoped mainline
merge review, or park/reject the sandbox chain. This slice makes the next-agent
behavior explicit: none of those options can be executed by inference.

## In Scope

- Define the response-handling contract for no reply, A, B, C, D, ambiguous
  replies, multiple options, and execution-word replies.
- Preserve p2-51 as the source packet.
- Provide fixtures, failure cases, a static readout/prototype, and a verifier.
- Run p2-51 final gate as an upstream dependency in this slice final gate.

## Out of Scope

- No mainline merge.
- No promotion.
- No formal vault write or Obsidian sync.
- No reviewed knowledge, evidence support, or action basis.
- No commit, push, dependency install, hook, service, automation, or MCP write tool.

## Acceptance Criteria

- Default no-reply behavior is `A_keep_sandbox_reference`.
- Options B and C are future scoped conversations only.
- Ambiguous or conflicting replies stop for clarification.
- Execution words stop and require separate explicit scope.
- All forbidden operation flags are false.
- Local final gate passes, including the p2-51 upstream final gate.
- Reviewer, Boundary Auditor, and GPT-5.5 extra-high Product Acceptance pass.
