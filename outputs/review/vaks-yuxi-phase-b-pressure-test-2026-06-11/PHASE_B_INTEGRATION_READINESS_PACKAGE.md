---
record_kind: sandbox_integration_readiness_package
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: integration_candidate_not_mainline_adoption
action_basis_allowed: false
---

# Phase B Integration Readiness Package

## Decision

Phase B is ready for the next sandbox integration review package.

It is not ready for mainline adoption.

Plain-language version:

```text
keep testing the VAKS-adapted Yuxi-style retrieval layer
do not let it become VAKS truth, review, action, Skills, MCP, or writeback
```

## Compared Against Previous Version

Previous version:

```text
contract-passing adapter skeleton
```

This package changes:

```text
integration documentation and readiness checks
```

This package does not change:

```text
ranking policy
retrieval behavior
authority bucket ordering
manifest schema
receipt schema
reviewed write path
```

Current skeleton metrics remain the comparison floor:

| Set | Corpus | hit@5 | hit@10 | MRR | Leakage | Forbidden top1 | Cross-bucket violation |
|---|---|---:|---:|---:|---:|---:|---:|
| main | primary | 30/30 | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| main | full | 30/30 | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| holdout | primary | 12/15 | 13/15 | 0.7811 | 0.0000 | 0.0000 | 0.0000 |
| holdout | full | 13/15 | 13/15 | 0.7591 | 0.0000 | 0.0000 | 0.0000 |

Contract floor:

```text
contract status: pass
error count: 0
```

## Adapter API Shape

Current sandbox implementation:

```text
tools/vaks_phase_b_adapter.py
```

CLI shape:

```powershell
python tools/vaks_phase_b_adapter.py manifest --corpus primary --corpus full --result-prefix phase_b_skeleton_main
python tools/vaks_phase_b_adapter.py receipts --query-file queries_phase_b.jsonl --corpus primary --corpus full --result-prefix phase_b_skeleton_main --top-k 10
python tools/vaks_phase_b_adapter.py receipts --query-file queries_phase_b_holdout.jsonl --corpus primary --corpus full --result-prefix phase_b_skeleton_holdout --top-k 10
```

Internal object shape:

```python
adapter = VaksPhaseBAdapter(
    corpus="primary | full",
    stale_paths={"SCHEMA.md", "SOURCE_INTAKE.md", "FEEDBACK.md"},
    indexed_at="ISO-8601 timestamp",
)

adapter.chunk_manifest_rows()
adapter.query(query, top_k=10)
adapter.adapter_result(query, result)
```

Allowed methods:

```text
read VAKS files
emit chunk manifest
emit retrieval receipts
return adapter-shaped result objects
```

Not allowed methods:

```text
write reviewed knowledge
promote candidate points
create reviewed relations
change truth confidence
mark action basis
execute Skills
execute MCP writes
run subagents as production evidence
```

## Inputs

The adapter accepts only read-oriented inputs:

```yaml
vaks_root:
  kind: read_only_markdown_yaml_vault
  source_of_truth: VAKS main repository

corpus:
  allowed:
    - primary
    - full
  meaning: sandbox evaluation scope only

query_file:
  shape:
    id: string
    group: string
    intent: orientation | evidence | action
    query: string
    expected_terms: evaluation_only

stale_paths:
  shape: list of vault-relative paths
  purpose: stale-index warning simulation
```

`expected_terms` is evaluation scaffolding. It must not be used as production ranking input.

Plain rule for reviewers:

```text
expected_terms is evaluation scaffolding, not adapter memory or production ranking input
```

## Outputs

The adapter emits derived artifacts only:

```yaml
chunk_manifest_jsonl:
  purpose: indexed chunk inventory with VAKS boundary fields
  example:
    - results/phase_b_skeleton_main_primary_chunk_manifest.jsonl
    - results/phase_b_skeleton_main_full_chunk_manifest.jsonl

retrieval_receipt_jsonl:
  purpose: query result receipt with rank, policy, hashes, warnings, and click-back
  example:
    - results/phase_b_skeleton_main_primary_retrieval_receipts.jsonl
    - results/phase_b_skeleton_main_full_retrieval_receipts.jsonl
    - results/phase_b_skeleton_holdout_primary_retrieval_receipts.jsonl
    - results/phase_b_skeleton_holdout_full_retrieval_receipts.jsonl

pressure_reports:
  purpose: sandbox diagnostics only
  example:
    - results/phase_b_summary.csv
    - results/phase_b_holdout_summary.csv
    - results/phase_b_adapter_contract_test.json
```

These outputs are not reviewed knowledge.

## Required Result Fields

Every manifest or receipt row must keep these VAKS adapter fields:

```yaml
vaks_record_id:
vault_path:
heading_or_anchor:
selector_or_line_range:
source_hash:
indexed_source_hash:
chunk_hash:
source_family_id:
record_kind:
knowledge_status:
review_state:
relation_state:
retrieval_policy:
  policy_kind:
  pack_allowed:
  action_basis_allowed:
  authority_bucket:
authority_badge:
usage_badge:
temporal_badge:
warning_code:
retrieval_reasons:
graph_path:
source_clickback:
generated_by:
indexed_at:
```

Receipt rows must also include:

```yaml
query_id:
query_group:
query_intent:
mode:
rank:
retrieval_receipt:
```

## Insertion Point

Correct topology:

```text
VAKS Markdown/YAML authoritative vault
  -> read-only Phase B adapter
  -> chunk manifest / future index mirror
  -> VAKS authority-bucket filter before ranking
  -> bucket-local retrieval receipt
  -> context-pack candidate
  -> VAKS review / action gate
```

Wrong topology:

```text
Yuxi runtime database becomes VAKS source of truth
Yuxi graph edge becomes reviewed relation
retrieval score becomes evidence support
context pack becomes action basis without VAKS gate
AGENTS.md / Skills / MCP output becomes long-term VAKS rule
```

Phase B belongs between the authoritative vault and context-pack candidate assembly.

It must stay outside:

```text
reviewed write path
truth-confidence updates
reviewed relation creation
action-gate approval
Skills / MCP write tools
subagent production evidence
```

## Failure Modes

The adapter must fail closed or stay sandbox-only if any of these appears:

| Failure mode | Why it matters | Required response |
|---|---|---|
| stale source hash | index no longer represents source | emit stale warning, refresh before action use |
| missing click-back file | user cannot inspect evidence | block readiness |
| line range past EOF | click-back is unreliable | block readiness |
| missing risk warning | raw/candidate/feedback can sound authoritative | block readiness |
| `action_basis_allowed` leak | unsafe result may be used for action | block readiness |
| risky bucket claims reviewed relation | graph or candidate edge sounds reviewed | block readiness |
| cross-bucket RRF | raw/candidate can outrank reviewed as if same authority | reject change |
| manifest or receipt missing required fields | downstream cannot enforce VAKS boundary | block readiness |
| main or holdout regression | ranking got worse than previous version | hold in sandbox |
| Yuxi dependency confusion | original runtime database becomes hidden authority | keep as external runtime only |

## Rollback Path

Rollback is simple because this phase is read-only:

```text
1. Disable `vaks_b_adapter_skeleton` mode.
2. Delete or ignore derived `phase_b_skeleton_*` artifacts.
3. Fall back to `vaks_b_adapter_v1_1` for ranking comparison, or to `vaks_b_bucket_local` for the earlier keep baseline.
4. Keep VAKS Markdown/YAML vault unchanged.
5. No truth rollback is required because Phase B writes no reviewed knowledge.
```

Rollback trigger:

```text
any leakage
any contract failure
any readiness failure
unexplained holdout regression
any attempt to attach Skills, MCP writes, subagents, or formal writeback
```

## Required Gates Before Mainline Discussion

The next discussion may continue only if all gates pass:

```text
main pressure MRR >= contract-passing skeleton
holdout MRR >= contract-passing skeleton
action_leakage_rate = 0.0000
forbidden_top1_rate = 0.0000
cross_bucket_violation_rate = 0.0000
clickback_coverage = 1.0000
hash_coverage = 1.0000
adapter contract validator = pass
integration readiness validator = pass
insertion point = explicit
rollback path = explicit
failure modes = explicit
```

If a later version improves retrieval but weakens governance, reject it.

## Next Candidate Step

Next step after this package:

```text
run readiness validator
write readiness-vs-contract decision
then prepare a Pro/mainline-readiness review packet before touching core docs
```

No C-lite, no Skills, no MCP writes, no subagent production path, and no formal writeback are approved by this package.
