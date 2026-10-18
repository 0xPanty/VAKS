---
record_kind: sandbox_iteration_decision
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: diagnostic_not_mainline_decision
action_basis_allowed: false
---

# Phase B Pro Review Prompt Decision

## Decision

Keep the Pro review prompt.

Do not edit core VAKS docs yet.

## Compared Against Previous Version

Previous version:

```text
mainline-readiness / Pro review packet
```

This step added:

```text
copy-pasteable Pro review prompt
prompt validator
prompt check report
```

It preserved:

```text
mainline readiness: pass / 0 errors
integration readiness: pass / 0 errors
contract: pass / 0 errors
core docs dirty lines: 0
```

## Why This Is Positive

This step is positive because it converts the previous review packet into a
usable external-review request without loosening the boundary.

It adds:

```text
explicit Pro role
explicit no-edit / no-merge instruction
explicit must-preserve VAKS boundaries
exact evidence files to inspect
current metric floor
candidate touch set
candidate wording to review
required answer format
hidden-risk question
```

It does not claim:

```text
mainline adoption
retrieval-score improvement
production readiness
C-lite approval
Skills / MCP / subagent approval
```

## Boundary

This decision supports:

```text
send `PHASE_B_PRO_REVIEW_PROMPT.md` to Pro or another review window
```

It does not support:

```text
editing SOURCE_INTAKE.md
editing IMPLEMENTATION_BLUEPRINT.md
editing DEV_CONTEXT.md
editing MEMORY_TIER.md
editing SCHEMA.md
editing REVIEW_QUEUE.md
```

## Next Step

Next step should be external review.

If Pro returns `APPROVE_MINIMAL_DOC_PATCH`, prepare a separate minimal
documentation-only patch and compare it against this prompt.

If Pro returns `REVISE_BEFORE_PATCH`, revise the prompt or packet in sandbox.

If Pro returns `REJECT_FOR_NOW`, keep Phase B in sandbox and do not touch core
docs.
