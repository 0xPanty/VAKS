---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
review_pressure: none
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: verified-action-knowledge-system
target_ref: "raw/repos/2026-08-02-semantica-agi-semantica-source.md"
target_selector: "repo:semantica-agi/semantica@0d447560bc3c9a8dfa0bfb5e78d32dbe77416cd3"
target_hint: "implementation reference for decision records, inference receipts, bitemporal applicability, SHACL lint, conflict packets, storage adapters, and agent/MCP authority risks"
source_annotation_refs:
  - ann-semantica-001-default-llm-extraction
  - ann-semantica-002-conflict-after-persistence
  - ann-semantica-003-declared-and-heuristic-causality
  - ann-semantica-004-decision-provenance-wiring-gap
  - ann-semantica-005-provenance-integrity-boundary
  - ann-semantica-006-rete-unconditional-matches
  - ann-semantica-007-ontology-validator-placeholder
  - ann-semantica-008-bitemporal-normalization
  - ann-semantica-009-agent-mcp-direct-write
  - ann-semantica-010-ci-build-only
project_borrow_scope: "decision record envelope; premise-rule-conclusion inference receipt; valid/recorded/superseded temporal fields; SHACL as structural lint; conflict packet as review input; backend projection receipts and explicit failure lists"
project_non_borrow_scope: "Semantica as VAKS truth store; automatic text extraction into reviewed KG; source/PROV as support; graph path/similarity as causal evidence; voting/recency/confidence as truth resolution; current Rete/OntologyValidator; direct agent-memory/MCP writes; Production/Stable or regulator-ready claims as adoption proof"
project_reopen_trigger: "VAKS opens a graph retrieval cache sandbox, inference-receipt experiment, temporal applicability implementation, read-only MCP permission design, or backend projection round-trip test"
confirmation_basis: "User explicitly requested distillation of semantica-agi/semantica in the VAKS workspace on 2026-08-02."
last_checked_at: "2026-08-02"
expires_at: null
---

# Project Overlay：Semantica -> VAKS

## Boundary

This sidecar records what the active VAKS project may borrow or avoid. It does
not rewrite the source, promote a pattern, approve a dependency, or provide
action basis.

## Target

```yaml
target_ref: raw/repos/2026-08-02-semantica-agi-semantica-source.md
target_selector: repo:semantica-agi/semantica@0d447560bc3c9a8dfa0bfb5e78d32dbe77416cd3
target_hint: accountable-KG implementation reference and authority-boundary counterexample
```

## Project Borrow Scope

For VAKS, borrow only these shapes:

```text
1. Decision record envelope
   stable id + actor + scenario + stated reasoning + outcome + timestamps.
   Evidence packet, reviewer, approval receipt, and outcome calibration remain external.

2. Inference receipt
   premises + rule id/version + conclusion + engine version.
   Output remains candidate inference.

3. Bitemporal applicability fields
   valid_from / valid_until + recorded_at / superseded_at.
   This refines applicability, not truth.

4. SHACL as structural lint
   Check exported RDF/graph shape only.

5. Conflict packet
   Competing values + source anchors + conflict kind + severity + review route.
   Route to Point Collision / Evidence-Aware Review; do not pick a winner.

6. Storage projection receipt
   Record schema version, projected fields, successes, failures, rollback state,
   and round-trip loss before trusting a graph backend.
```

Most of these ideas already exist in VAKS conceptually. Semantica is therefore
an implementation reference, not a reason to add a new formal lane, pattern,
schema family, runtime, or graph database.

## Project Non-Borrow Scope

Do not currently borrow:

```text
Semantica as canonical truth or memory
automatic LLM extraction into reviewed nodes/relations
automatic dedup as confirmed entity identity
voting / recency / source score / caller confidence as truth resolution
declared or heuristic causal edges as causal evidence
PROV-O export as evidence support or regulator acceptance
Rete and OntologyValidator placeholder paths
graph rank / community / similarity as trust
direct agent-memory, MCP, REST, or CLI writes into VAKS authority layers
one large dependency bundle as VAKS core
test count or package classifier as production readiness
```

## Reopen Trigger

Reconsider selected parts only when:

```text
derived graph-cache sandbox starts
inference-receipt micro-trial starts
Temporal Applicability implementation needs a concrete adapter
read-only MCP permission contract is being designed
graph backend round-trip/projection test is available
representative VAKS fixtures and explicit rollback/receipt gates exist
```

## Operational Verdict

```text
borrow_value: medium as code/reference, low as direct dependency
borrow_now: record shapes and negative boundary lessons
borrow_later: tiny isolated adapter experiments only
do_not_borrow_now: mainline dependency, truth semantics, graph runtime, write-capable agent surface
formal_pattern_needed: no
schema_change_needed: no
```

## Forbidden

```text
truth mutation
reviewed relation
automatic promotion
action basis
dependency adoption approval
regulatory or causal assurance
```
