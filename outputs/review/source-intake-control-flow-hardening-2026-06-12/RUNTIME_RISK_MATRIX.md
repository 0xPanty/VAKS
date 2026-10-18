---
type: source_intake_runtime_risk_matrix
status: proposed_read_only_runtime_tests
created_at: 2026-06-13
scope: Source Intake runtime / answer-loop risks not proven by static validator
truth_boundary: test backlog only; not runtime readiness; not Source Intake P0 approval
---

# Runtime Risk Matrix

## Plain Verdict

The current validator is a static frontmatter plus synthetic-receipt guard. It
is necessary, but it cannot prove runtime behavior.

This matrix lists the minimum read-only runtime checks needed before anyone can
claim Source Intake P0 readiness, answer-loop safety, C-lite readiness, or
runtime adoption.

## Risks And Minimal Tests

| Runtime risk | Why static validator may miss it | Minimal read-only test | Current status |
|---|---|---|---|
| Stale index cache still retrieves archived or `default_retrieval: false` overlays | Frontmatter is correct, but the derived index may be stale. | Rebuild index before/after, run the same query, diff receipts for excluded items. | not run |
| Answer loop cites source-card summary as support | Source frontmatter can be valid while the answerer skips drilldown or independent anchor checks. | Read-only answer-loop with citation audit and support-check replay. | not run |
| Graph compiler reads raw relations and emits formal-looking graph edges | Static lint can move or flag fields, but downstream graph build may still consume old paths or cached artifacts. | Graph build sandbox; inspect edge provenance/status labels and source paths. | not run |
| Raw confidence becomes UI/reranker authority score | Structure can be legal while UI or ranking code interprets a capture score as trust. | UI badge/reranker audit; verify confidence appears only as capture/extraction diagnostic. | not run |
| Feedback aggregation suppresses across projects | Individual feedback can have scope while an aggregator accidentally globalizes it. | Multi-project negative-feedback replay; verify suppression stays project/scope-local. | not run |
| Heavy Review anchor points to stale, empty, or mismatched content | Anchor field exists, but existence and content match are runtime facts. | Anchor existence/content replay against source snapshots or stable raw text. | not run |
| Pack builder computes `pack_role` incorrectly and marks candidates as support | Templates are correct, but runtime pack assembly may mislabel items. | Top-k replay plus receipt assertion: candidate/overlay/feedback cannot become support. | not run |
| Active-project filter is bypassed by subagent/tool chain | Main validator does not execute tool calls, subagents, or external runtime filters. | Read-only agent tool-loop pressure test with active/non-active project queries. | not run |
| Promotion gate bypasses through a non-writeback path | Static files cannot prove every write path uses the same gate. | Dry-run writeback and forbidden-action tests across all known write surfaces. | not run |
| Legacy lens content is manually or agent-copied into a new pack | Validator may not know human/agent copy provenance if the new pack omits source lineage. | Pack manifest provenance audit; every copied legacy item must point to excluded legacy source and remain non-support. | not run |
| `legacy_raw_metadata` is selected by retrieval, graph, pack, or support code | Current lint can block serialized misuse, but it cannot prove runtime compilers ignore the subtree. | Read-only retrieval/graph/pack run with canary `legacy_raw_metadata`; assert no selected item or support check uses it. | static guard only; runtime not run |

## Minimum Runtime Evidence Before P0

Do not open runtime adoption or C-lite from the current package alone.

Minimum next evidence should be:

1. Frozen read-only query set with rebuilt index and receipt diff.
2. Read-only answer-loop run with citation/support audit.
3. Graph/compiler sandbox proving raw/candidate/legacy fields do not become reviewed edges.
4. Pack-builder replay proving `pack_role` and active-project filtering survive real assembly.
5. Dry-run writeback/forbidden-action tests proving promotion gates are not bypassed.

## Boundary

Passing this matrix in the future would still be runtime evidence, not reviewed
truth. Runtime traces can create review pressure and implementation confidence;
they must not create reviewed claims, reviewed relations, or action basis by
themselves.
