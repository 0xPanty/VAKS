---
record_kind: sandbox_enterprise_gate_spec
status: active
created_at: 2026-06-14
scope: source-annotation-scale-enterprise-stress
truth_boundary: sandbox_only_not_adopted_architecture
---

# Enterprise Gate Spec

## Goal

Prove whether the source annotation design can move from product-grade sandbox
to enterprise-ready candidate.

Enterprise-ready here means:

```text
large file-backed corpus
clear queues
no authority contamination
measurable runtime
visible maintenance debt
safe default AI export
```

It does not mean:

```text
formally adopted main schema
finished Obsidian UI polish
automatic anchor repair
automatic evidence review
```

## Required Tests

| Test | Pass condition |
|---|---|
| Large corpus validation | >= 5,000 source annotation files, 0 schema errors |
| Mutation suite | every intentionally bad annotation is caught |
| Bad context packs | every intentionally bad context pack is caught |
| AI ready contamination | no broken / ambiguous / source_changed / stale / archived annotation in AI ready |
| Support contamination | no source_annotation appears as support in selected items or coverage_map |
| Project pollution | no source_annotation contains project_borrow_scope or project_non_borrow_scope |
| Repair queue | every active bad anchor appears in repair queue |
| Stale queue | every active stale anchor appears in stale queue |
| Scale debt | dense sources and repeated selectors surface in scale-debt report |
| Support checked audit | support_checked requires evidence_packet_ref |
| Runtime | 5,000-file validation under 30 seconds |
| Default context pack | <= 60 selected annotations and <= 250 KB JSON |
| Working inbox load | <= 250 actionable rows at 5k; <= 500 at 10k stretch |
| Locator pool separation | stable bulk locators are queryable but not daily inbox rows |
| Source digest backlog | every dense source has digest route, next action, and due date |
| Digest backlog age | p95 digest backlog age <= 14 days |

## Enterprise Readiness Levels

```text
L0 concept only
L1 product model
L2 sandbox validated
L3 stress validated
L4 pilot-ready in real vault
L5 enterprise production with real operations
```

This sandbox can at most prove L3.

L4 requires a real Obsidian pilot batch and human workflow measurement.
L5 requires operational ownership, backups, migration policy, and real repair
procedures.
