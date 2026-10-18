# CI-06 Sandbox Test Report: Context Pack Evidence Envelope

Date: 2026-06-08

Scope:

```text
CI-06 is a read-only context/evidence envelope.
It is not a truth layer, review verdict, reviewed relation engine, action basis,
wiki writeback, candidate promotion, API implementation, MCP implementation, or runtime.
```

## Sandbox

Sandbox root:

```text
outputs/review/ci-06-context-pack-evidence-envelope-2026-06-08/
```

Base architecture copied from:

```text
outputs/review/ci-05-scope-dashboard-live-context-surface-2026-06-08/architecture/
```

This sandbox tests CI-06 on top of CI-02, CI-02.5, CI-03, CI-04, and CI-05.

No permanent Obsidian sync was performed.

## Existing Architecture Check

CI-06 is already strongly covered by the current architecture.

Existing architecture says:

```text
Context pack is a calling/activation layer, not a reviewed knowledge layer.
Context pack must expose warnings/gaps.
Context pack/action basis needs evidence sufficiency before action-ready finalization.
Retrieval, graph neighbors, citation, and context pack do not decide truth.
```

So CI-06 is not a new layer. It is a clearer envelope contract.

## Source Evidence Added

Local source snapshot:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
```

Retained sandbox evidence snapshots:

```text
evidence/llm-wiki-compiler/context-types-anchor-snapshot.md
evidence/llm-wiki-compiler/context-build-anchor-snapshot.md
```

Confirmed anchors:

```text
src/context/types.ts:1-11
src/context/types.ts:49-55
src/context/types.ts:93-99
src/context/types.ts:150-161
src/context/build.ts:1-20
src/context/build.ts:56-76
src/context/build.ts:104-119
src/context/build.ts:227-264
src/context/build.ts:449-505
src/context/build.ts:513-565
```

Observed source behavior:

- Stable v1 JSON envelope.
- Top-level envelope contains `version`, `prompt`, `budget`, `project`, `primary`, `neighbors`, `warnings`, `gaps`, and `suggestedActions`.
- Source windows are emitted only when include-sources is explicitly requested.
- Project warnings surface pending candidates, lint errors, and source-window unavailability.
- Budget trimming mutates structured sections, not serialized JSON.

## Sandbox Rule

Minimum VAKS envelope:

```yaml
version: 1
prompt:
budget:
  requested_tokens:
  estimated_tokens:
  truncated: true | false
  trimmed_sections: []
project:
  root:
  pages:
  pending_candidates:
  lint:
primary: []
neighbors: []
warnings: []
gaps: []
suggested_actions: []
source_windows: []
read_only: true
not_truth_layer: true
not_action_basis: true
```

Allowed:

```text
prepare context
show primary candidates
show neighbor context
show citations
show warnings and gaps
suggest next actions
include bounded source windows only when explicitly requested
```

Blocked:

```text
truth_confidence mutation
verification_status mutation
reviewed relation creation
action_basis_readiness
wiki writeback
candidate promotion
automatic suggested action execution
default raw source snippets
budget trimming that hides gaps
```

## Pressure Test

Command:

```powershell
& "outputs\review\ci-06-context-pack-evidence-envelope-2026-06-08\tests\pressure-test.ps1"
```

Result:

```text
RESULT pass=107 fail=0
```

Test dimensions:

- Source anchor snapshots exist and contain the required line anchors.
- CI-06 pattern references the snapshots and states read-only envelope boundaries.
- `SCHEMA.md` sandbox copy contains the minimal v1 context pack shape.
- `templates/dev-context-pack.md` sandbox copy exposes the envelope boundary.
- Knowledge graph index sandbox copy records the CI-06 boundary.
- PASS fixture validates a read-only envelope with warnings/gaps.
- PASS fixture validates explicit source windows.
- BLOCK fixtures catch default source windows, pack-as-truth, neighbor-as-reviewed-relation, suggested-action auto-exec, action-basis-ready, truncated-hiding-gaps, and wiki writeback.
- Compatibility checks confirm CI-02 through CI-05 still exist in the same sandbox.
- Root pollution checks confirm formal root files were not changed by CI-06 sandbox-only wording.

## Result

Positive.

CI-06 is useful and architecture-compatible. It is not overdesigned if kept as a small envelope contract.

It becomes overdesigned if it turns into:

```text
API/MCP runtime
automatic action executor
truth/review authority
wiki writer
context pack as action basis
source snippet leakage by default
```

## Recommendation

CI-06 can be kept as a strong sandbox-positive candidate.

It is closer to lightweight merge readiness than CI-05 because the source-code anchors are stronger and the existing architecture already has the context-pack layer.

If merged later, merge only the contract:

```text
stable read-only envelope
warnings/gaps required
source_windows opt-in
suggested_actions not automatic
primary/neighbors not truth or reviewed relation
context pack alone not action-ready
```

Do not merge:

```text
tests/fixtures/
tests/pressure-test.ps1
API/MCP implementation
runtime resolver
automatic pack generator
automatic suggested action execution
raw source snippets by default
```

## Final Judgment

```text
positive: yes
overdesigned: no, if kept as a read-only envelope contract
conflict_with_existing_architecture: no
promotion_ready_like_CI01_to_CI04: close, but still sandbox-only until final review
recommend_keep_candidate: yes
recommend_mainline_merge_later: yes, lightweight only
```

