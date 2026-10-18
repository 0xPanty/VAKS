---
record_kind: sandbox_external_blind_query_set_kit
status: pending_external_queries
project_id: VAKS
created_at: 2026-06-12
truth_boundary: query_set_kit_not_completed_external_blind
action_basis_allowed: false
---

# Phase B External Blind Query Set Kit

## Plain Task

Pro's latest audit asks for 15-20 external blind queries written by an external human or at least a different model family.

Use this template:

```text
queries_phase_b_external_blind_template.jsonl
```

Create this filled file:

```text
queries_phase_b_external_blind.jsonl
```

Also fill this author/provenance manifest:

```text
results/phase_b_external_blind_query_author_manifest.json
```

## Author Restriction

```text
Do not read existing Phase B query files.
Do not read existing Phase B result CSV/JSON files.
Do not read existing Phase B reports.
Allowed source access: VAKS core docs and high-level architecture docs only.
Target count: 15-20 filled queries.
External author should not write expected_terms.
Expected terms may be added later by an internal scorer without changing query text.
```

## Required JSONL Fields

```yaml
id: EXT-BLIND-001
group: short category
intent: one of action, evidence, review, retrieval_design, source_intake, context_pack, graph_retrieval, agent_access
query: user-facing query text
needs_boundary_warning: true | false
risk_note: why this query pressures retrieval/governance
```

## Author Manifest Fields

```yaml
author_type: external_human | different_model_family
author_id_or_model_family:
generation_method:
attestation_no_phase_b_query_access: true
attestation_no_phase_b_result_access: true
attestation_no_phase_b_report_access: true
allowed_docs_seen:
  - README.md
  - FUSION_ARCHITECTURE_V0_2_DRAFT.md
notes:
```

## Boundary

```text
This kit prepares external blind query generation.
It does not complete external blind testing.
Generated queries are test inputs, not reviewed knowledge.
Passing this kit does not validate original Yuxi runtime, C-lite, writeback, or action basis.
```

## Template Summary

```text
template rows: 20
filled query file: queries_phase_b_external_blind.jsonl
author manifest template: results/phase_b_external_blind_query_author_manifest_template.json
author manifest filled file: results/phase_b_external_blind_query_author_manifest.json
status: pending_external_queries
```
