---
record_kind: sandbox_contract
slice_id: 2026-06-15-p2-17-use-surface-optimization-pass
status: implemented_pending_review
truth_boundary: sandbox_contract_only
---

# Use Surface Contract

## Intent

Make the strict VAKS workflow easier to operate by exposing clear entry, state,
navigation, receipt, hash, and dirty-state surfaces while preserving all
authority boundaries.

## Manifest Inputs

A valid use-surface blueprint has:

- `scope`: sandbox-only write and runtime boundaries.
- `entries`: product entry buttons/routes and their backend artifact class.
- `user_questions`: answers to the six P2 acceptance questions.
- `status_surfaces`: short status surfaces before long manuals.
- `search_surface`: receipt-backed search rules.
- `layer_badges`: display-only layer state markers.
- `guardrails`: dirty-state, hash, sync, and action-mode constraints.

## Required Entries

| Entry | Backend artifact | Boundary |
|---|---|---|
| `add_source` | source card | provenance only |
| `process_this` | candidate distillation | candidate only |
| `ask_vault` | query-run trace | orientation unless action mode |
| `check_vault` | maintenance manifest | diagnostic only |
| `make_context_pack` | context pack manifest | not action basis by itself |
| `review_candidates` | Evidence Packet / review candidate | review input only |
| `record_feedback` | feedback event | activation and review pressure only |
| `prepare_action` | context pack + support + readiness checks | blocked until VAKS action readiness passes |

## Non-Claims

Passing this sandbox is not:

- reviewed knowledge;
- evidence support;
- reviewer approval;
- action basis;
- promotion readiness;
- mainline readiness;
- production UI approval;
- Obsidian sync permission;
- commit or push permission.

## Output Contract

The validator returns:

```json
{
  "valid": true,
  "issues": [],
  "non_claims": {
    "surface_pass_not_reviewed_knowledge": true,
    "surface_pass_not_evidence_support": true,
    "surface_pass_not_action_basis": true,
    "surface_pass_not_mainline_readiness": true
  }
}
```

Failure cases must use exact expected issue codes. Overlapping guards are
allowed only when explicitly listed in `allowed_extra_codes`.
