---
record_kind: sandbox_adapter_spec
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: spec_candidate_not_mainline_adoption
action_basis_allowed: false
---

# VAKS Phase B Adapter Spec

## Plain-Language Shape

VAKS can borrow Yuxi's retrieval habits, but VAKS must own the boundary.

Allowed borrowing:

```text
parse -> chunk -> metadata -> hybrid retrieval -> graph-neighborhood hint -> click-back
```

Required VAKS wrapper:

```text
authority bucket filter -> bucket-local ranking -> adapter warning -> retrieval receipt -> context-pack candidate
```

Not allowed:

```text
global Yuxi-style ranking becomes truth
graph edge becomes reviewed relation
retrieval score becomes evidence support
eval score becomes action readiness
runtime output writes reviewed knowledge
```

## Required Result Fields

Every adapter result must carry:

```yaml
vaks_record_id:
vault_path:
heading_or_anchor:
selector_or_line_range:
source_hash:
chunk_hash:
record_kind:
knowledge_status:
review_state:
relation_state:
retrieval_policy:
  policy_kind:
  pack_allowed:
  action_basis_allowed:
authority_badge:
usage_badge:
temporal_badge:
warning_code:
retrieval_reasons:
  - lexical
  - vector
  - graph_neighbor
source_clickback:
indexed_at:
```

## Ranking Rules

### v0 Passing Rule

`vaks_b_bucket_local` proved the basic rule:

```text
do not let raw/candidate/diagnostic/feedback compete against reviewed/core material in one global authority-like ranking
```

For action/evidence intents:

```text
core_framework / reviewed first
candidate / raw / diagnostic / overlay later
feedback never as truth
```

### v1 Candidate Rule

`vaks_b_adapter_v1` adds only intra-bucket ordering:

```text
within the allowed bucket:
  prefer path / heading / exact phrase alignment
  prefer main core docs over templates for action/evidence boundary questions
  keep the same warning/hash/receipt layer
```

This is allowed because it changes "which safe result comes first", not "what is allowed to count as support".

## Current Evidence

Main pressure set through skeleton:

```text
locked v0 primary MRR: 0.9083
v1 primary MRR:        1.0000
v1.1 primary MRR:      1.0000
skeleton primary MRR:  1.0000

locked v0 full MRR:    0.8528
v1 full MRR:           1.0000
v1.1 full MRR:         1.0000
skeleton full MRR:     1.0000

skeleton action leakage: 0.0000
```

Contract test through skeleton:

```text
initial contract status: fail
initial error count:     5569

fixed contract status:   pass
fixed error count:       0

validated:
  manifest primary:      3991 rows
  manifest full:         18785 rows
  main receipts:         600 rows
  holdout receipts:      300 rows
```

Holdout pressure set through skeleton:

```text
primary hit@5:
  v0: 9/15
  v1: 10/15
  v1.1: 12/15
  skeleton: 12/15

full hit@5:
  v0: 9/15
  v1: 11/15
  v1.1: 13/15
  skeleton: 13/15

primary MRR:
  v0: 0.4771
  v1: 0.6144
  v1.1: 0.7811
  skeleton: 0.7811

full MRR:
  v0: 0.3665
  v1: 0.5868
  v1.1: 0.7591
  skeleton: 0.7591

skeleton action leakage: 0.0000
```

## Known Weaknesses

Do not hide these:

- Yuxi middleware/resource-filter questions needed topic-anchor routing; v1.1 fixed the measured holdout regression, but the top anchor can still be candidate/diagnostic for retrieval-design questions.
- Benchmark/lint/diagnostic boundary questions now route better in v1.1, but the rule is still a sandbox ranking rule, not a reviewed policy.
- Original Yuxi was not run end to end because Docker is unavailable locally.
- The current implementation is a sandbox read-only skeleton, not a production adapter.
- The contract test is structural and local; it does not prove production performance, concurrency behavior, or integration safety.

## Next-Step Gate

The integration readiness package now passes.

Current readiness evidence:

```text
readiness status: pass
readiness errors: 0
contract status:  pass
contract errors:  0
```

The mainline-readiness / Pro review packet now passes.

Current mainline-readiness evidence:

```text
mainline readiness status: pass
mainline readiness errors: 0
core docs dirty lines: 0
```

The next step should be external / Pro review of the packet before any core doc
edits.

The external Pro review prompt now passes:

```text
prompt status: pass
prompt errors: 0
core docs dirty lines: 0
```

Use `PHASE_B_PRO_REVIEW_PROMPT.md` as the next review handoff.

The external review result and minimal documentation patch now pass:

```text
external review verdict: APPROVE_MINIMAL_DOC_PATCH
external review errors: 0
minimal doc patch errors: 0
```

The accepted mainline note is documentation-only and limited to:

```text
SOURCE_INTAKE.md
IMPLEMENTATION_BLUEPRINT.md
DEV_CONTEXT.md
MEMORY_TIER.md
```

Runtime/full-stack feasibility was checked after the documentation patch:

```text
Yuxi HEAD: a8536a2e8520d1992a31bb6c22f219e60deca131
Docker: unavailable
Docker Compose: unavailable
runtime feasibility: pass by blocking false runtime claim
```

Do not claim original Yuxi runtime parity until Docker/Compose or an approved
remote runner is available.

Context-pack candidate assembly now passes at adapter level:

```text
pack count: 90
context pack status: pass
context pack errors: 0
pack action_basis_allowed_count: 0
packs with suppressed receipt action flags: 36
```

This supports using Phase B retrieval receipts as context-pack candidates only.
It does not approve action basis, evidence sufficiency, runtime adoption, or
original Yuxi full-stack parity.

Evidence-envelope / warrant-draft assembly now passes at adapter level:

```text
envelope count: 90
evidence envelope status: pass
evidence envelope errors: 0
action_basis_allowed_count: 0
evidence_packet_allowed_count: 0
evidence_sufficiency_passed_count: 0
envelopes with suppressed receipt action flags: 36
```

This supports using Phase B context-pack candidates to prepare review work only.
It does not approve Evidence Packet creation, evidence support, evidence
sufficiency, action basis, runtime adoption, or original Yuxi full-stack parity.

Evidence Support Check candidate assembly now passes at adapter level:

```text
support check count: 90
evidence support check status: pass
evidence support check errors: 0
evidence item count: 389
source_span_available_count: 389
current_source_hash_match_count: 321
source_refresh_needed_count: 68
blocked_no_source_anchor_count: 2
support_passed_count: 0
support_counts_for_promotion_count: 0
action_basis_allowed_count: 0
```

This supports using Phase B evidence envelopes to prepare Evidence Support Check
work only. It does not approve semantic support, reviewed support, Evidence
Packet creation, evidence sufficiency, action basis, runtime adoption, or
original Yuxi full-stack parity.

Source-refresh candidate assembly now passes at adapter level:

```text
source refresh count: 90
source refresh status: pass
source refresh errors: 0
refresh item count: 389
source_span_available_count: 389
pre_refresh_mismatch_count: 68
post_refresh_mismatch_count: 0
refreshed_item_count: 68
already_current_item_count: 321
blocked_no_source_anchor_count: 2
support_passed_count: 0
action_basis_allowed_count: 0
```

This supports using Phase B support-check candidates to refresh source-span/hash
snapshots before review only. It does not approve semantic support, reviewed
support, Evidence Packet creation, evidence sufficiency, action basis, runtime
adoption, or original Yuxi full-stack parity.

Refreshed support-check rebuild now passes at adapter level:

```text
refreshed support check count: 90
refreshed support check status: pass
refreshed support check errors: 0
evidence item count: 389
source_span_available_count: 389
previous_source_refresh_needed_count: 68
current_source_refresh_needed_count: 0
current_source_hash_match_count: 389
refreshed_item_count: 68
already_current_item_count: 321
blocked_no_source_anchor_count: 2
support_passed_count: 0
action_basis_allowed_count: 0
```

This supports using refreshed Phase B source-span/hash snapshots in the
review-facing support-check view. It does not approve semantic support, reviewed
support, Evidence Packet creation, evidence sufficiency, action basis, runtime
adoption, or original Yuxi full-stack parity.

Review queue packet assembly now passes at adapter level:

```text
review packet count: 90
review queue packet status: pass
review queue packet errors: 0
open packet count: 88
blocked_no_source_anchor_count: 2
review item count: 389
source_span_available_count: 389
current_source_hash_match_count: 389
current_source_refresh_needed_count: 0
review_result_not_reviewed_count: 90
support_passed_count: 0
action_basis_allowed_count: 0
automatic_promotion_allowed_count: 0
```

This supports using refreshed Phase B support-check candidates as manual review
queue input. It does not approve semantic support, reviewed support, Evidence
Packet creation, evidence sufficiency, promotion, action basis, runtime adoption,
or original Yuxi full-stack parity.

Simulated reviewer outcome assembly now passes at adapter level:

```text
outcome record count: 90
simulated reviewer outcome status: pass
simulated reviewer outcome errors: 0
simulated_packet_count: 12
simulated_item_outcome_count: 57
simulated_direct_support_count: 12
simulated_inferential_support_count: 12
human_reviewed_support_count: 0
support_passed_count: 0
support_counts_for_promotion_count: 0
action_basis_allowed_count: 0
automatic_promotion_allowed_count: 0
formal_writeback_allowed_count: 0
```

This supports testing reviewer-outcome data shape before real human review is
connected. It does not approve semantic support, reviewed support, Evidence
Packet creation, evidence sufficiency, promotion, formal writeback, action
basis, runtime adoption, or original Yuxi full-stack parity.

Promotion-gate / sufficiency-block evaluation now passes at adapter level:

```text
gate record count: 90
promotion gate status: pass
promotion gate errors: 0
blocked gate count: 90
simulated support-like count: 24
blocked_due_support_like_not_human_reviewed_count: 12
human_reviewed_support_count: 0
promotion_support_count: 0
promotion_allowed_count: 0
action_basis_allowed_count: 0
evidence_packet_created_count: 0
evidence_sufficiency_passed_count: 0
formal_writeback_allowed_count: 0
truth_confidence_change_allowed_count: 0
reviewed_relation_creation_allowed_count: 0
```

This supports carrying Phase B support-like metadata through the promotion and
action gates while preserving VAKS governance. It does not approve semantic
support, reviewed support, Evidence Packet creation, evidence sufficiency,
promotion, formal writeback, action basis, runtime adoption, or original Yuxi
full-stack parity.

Keep/stop synthesis now passes at adapter level:

```text
keep stop synthesis status: pass
keep stop synthesis errors: 0
keep_stop_decision: keep_phase_b_as_sandbox_candidate
positive_value_confirmed: true
no_boundary_leak_confirmed: true
promotion_allowed_count: 0
action_basis_allowed_count: 0
evidence_sufficiency_passed_count: 0
runtime_adoption_allowed: false
c_lite_allowed: false
original_yuxi_runtime_validated: false
```

This supports keeping Phase B as a positive sandbox and documentation candidate
only. It does not approve runtime/default adoption, C-lite, Skills/MCP/subagent
execution, formal writeback, Evidence Packet creation, action basis, original
Yuxi full-stack parity, truth-confidence changes, or reviewed relation creation.

Commit-readiness now passes at sandbox level:

```text
commit readiness check status: pass
commit readiness errors: 0
commit_readiness_status: ready_pending_user_approval
commit_without_user_approval_allowed: false
recommended docs:
  SOURCE_INTAKE.md
  IMPLEMENTATION_BLUEPRINT.md
  DEV_CONTEXT.md
  MEMORY_TIER.md
recommended sandbox evidence:
  outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/
excluded files:
  SCHEMA.md
  REVIEW_QUEUE.md
  templates/architecture-review-window-prompt.md
```

This supports a future user-approved commit of the validated four-file doc patch
plus the Phase B sandbox evidence bundle. It does not authorize this agent to
commit without user approval, and it does not approve runtime/default adoption,
C-lite, original Yuxi full-stack parity, formal writeback, reviewed truth, or
action basis.

Next-action gate now passes:

```text
next action gate check status: pass
next action gate errors: 0
recommended_next_action: await_user_approved_commit_or_runner_choice
commit_path: ready_pending_user_approval
commit_without_user_approval_allowed: false
original_yuxi_runtime_path: blocked_until_docker_or_remote_runner
original_yuxi_runtime_validated: false
c_lite_path: not_allowed_from_current_evidence
c_lite_allowed: false
runtime_adoption_path: not_allowed
runtime_adoption_allowed: false
```

This supports only a branch decision: approve the commit, provide a runtime
runner, or explicitly open a new gated sandbox. It does not itself approve any
commit, runtime/default adoption, C-lite, formal writeback, reviewed truth, or
action basis.

Pre-commit manifest now passes:

```text
pre commit manifest check status: pass
pre commit manifest errors: 0
pre_commit_manifest_status: ready_pending_user_approval
file_count: 166
commit_without_user_approval_allowed: false
stage_performed: false
commit_performed: false
```

This adds file-level hash evidence for the proposed commit scope. It still does
not authorize staging or committing, and it does not approve runtime/default
adoption, C-lite, original Yuxi full-stack parity, formal writeback, reviewed
truth, or action basis.

Branch-decision brief now passes:

```text
branch decision brief check status: pass
branch decision brief errors: 0
branch_decision_brief_status: ready_for_user_choice
recommended_branch: user_approved_commit
commit_without_user_approval_allowed: false
stage_performed: false
commit_performed: false
original_yuxi_full_stack_test: blocked_until_docker_or_remote_runner
c_lite_sandbox: not_allowed_without_new_user_gate
runtime_adoption: not_allowed
```

This improves handoff clarity only. It does not authorize staging, committing,
C-lite, runtime/default adoption, original Yuxi full-stack parity, formal
writeback, reviewed truth, or action basis.

It may continue only if it beats or ties the contract-passing skeleton on:

```text
action_leakage_rate = 0.0000
forbidden_top1_rate = 0.0000
cross_bucket_violation_rate = 0.0000
main pressure MRR >= skeleton
holdout MRR >= skeleton
manifest completeness = pass
receipt completeness = pass
click-back target existence = pass
no action-basis permission leaks = pass
integration insertion point = explicit
rollback path = explicit
failure modes = explicit
no new holdout query-level regression without written explanation
```

If a change improves recall but creates boundary leakage, reject it.

If a change improves the original 30 queries but hurts holdout, keep it in sandbox and do not promote.
