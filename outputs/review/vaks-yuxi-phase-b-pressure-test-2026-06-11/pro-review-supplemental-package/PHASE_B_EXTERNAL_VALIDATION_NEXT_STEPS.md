---
record_kind: sandbox_external_validation_next_steps
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: next_steps_not_validation_result
action_basis_allowed: false
---

# Phase B External Validation Next Steps

## Plain Conclusion

```text
Phase B can stay alive as a sandbox candidate.
It still cannot enter C-lite or claim original Yuxi runtime validation.
The next useful work is external validation, not more internal self-congratulation.
```

## What Is Now Locally Hardened

```text
frozen corpus manifest: added
file-hash snapshot: added
top11-20 item receipts for P0 main/holdout: added
query-level paired metrics: already added
top10 governance replay: already added
```

These make the current local proxy evidence more auditable. They do not change the authority level of the conclusion.

## P0-A: External / Manual Relevance Rejudgment

Current state:

```text
internal relevance judgment: complete_internal_only
external/manual judgment: pending
external judgment template: ready
```

Minimum ask:

```text
source packet: results/phase_b_blind_relevance_judgment_packet.csv
template: results/phase_b_blind_relevance_external_judgment_template.csv
mapping: results/phase_b_blind_relevance_external_judgment_mapping.csv
filled output: results/phase_b_blind_relevance_external_judgments.csv
judge_count: 2 independent judges minimum
arbitration: required for every row
system_identity_blinding: mode and original judgment_id hidden from judge-facing template
expected_terms_access: disallowed
internal_judgment_access_before_grading: disallowed
```

Each filled row must include:

```yaml
judge_a_relevance: 0 | 1 | 2
judge_a_basis:
judge_a_id:
judge_b_relevance: 0 | 1 | 2
judge_b_basis:
judge_b_id:
arbitrated_relevance: 0 | 1 | 2
arbitration_basis:
arbiter_id:
```

Decision rule:

```text
If external arbitrated relevance preserves the broad pattern, Phase B sandbox evidence gets stronger.
If external relevance removes most skeleton advantage over yuxi_native_profile, reduce the VAKS retrieval-alignment claim.
If external relevance contradicts the internal judgment strongly, rewrite the internal relevance finding instead of averaging it away.
```

## P1-A: External Blind Query Set

Current state:

```text
external blind query template: ready
author manifest template: ready
external blind query set: pending
template file: queries_phase_b_external_blind_template.jsonl
filled file: queries_phase_b_external_blind.jsonl
author manifest file: results/phase_b_external_blind_query_author_manifest.json
```

Minimum ask:

```text
query_count: 15-20
author: external human or at least a different model family
author_restriction: no access to current Phase B query files, result CSVs, or reports
source_access_allowed: VAKS core docs and high-level architecture docs only
output_format: jsonl
author_manifest_required: true
external_author_expected_terms: disallowed
internal_scoring_hints_after_query_freeze: allowed
```

Each query should include:

```yaml
id:
group:
intent: action | evidence | review | retrieval_design | source_intake | context_pack | graph_retrieval | agent_access
query:
needs_boundary_warning:
risk_note:
```

Judgment:

```text
If VAKS+B keeps measured leakage at 0 and does not materially fall behind baseline retrieval, the sandbox hypothesis gets stronger.
If Yuxi-like proxy retrieves similarly but leaks governance, the hand/eye plus VAKS-boundary split gets stronger as a hypothesis, not as a completed conclusion.
If VAKS+B loses retrieval badly or starts leaking, Phase B should be narrowed or stopped.
```

## P1-B: Original Yuxi Read-Only Rerun

Current state:

```text
local Docker: unavailable
local Docker Compose: unavailable
original Yuxi runtime: not run
```

Minimum rerun conditions:

```text
Docker/Compose available locally, or a remote runner is explicitly provided.
Yuxi runs in read-only mode over the same frozen corpus snapshot.
No Skills/MCP writes.
No reviewed knowledge writeback.
No action basis creation.
No prompt/runtime output treated as truth.
```

Required exports:

```text
per-query top10
first_hit_rank over top20 if available
score/rank/retrieval reason
source path or document id
clickback target
bucket/status if adapter metadata is carried through
forbidden_top1
cross_bucket_authority_violation
action_leakage proxy
warnings or absence of warnings
```

Decision rule:

```text
If original Yuxi differs from yuxi_native_profile by more than 0.05 MRR or 10 percentage points leakage, current attribution must be rewritten.
If original Yuxi-only retrieves well but leaks VAKS authority boundaries, VAKS wrapper value is strengthened.
If original Yuxi-only can preserve equivalent authority boundaries without VAKS metadata, the VAKS contribution claim must be reduced.
```

## Hard Stops

```text
do_not_claim_original_yuxi_runtime_validated
do_not_enter_c_lite_from_current_evidence
do_not_write_core_docs_with_strong_conclusion
do_not_treat_external_blind_as reviewed truth
do_not_allow_runtime_writeback_in_original_yuxi_rerun
```
