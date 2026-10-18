---
type: project_scoped_sidecar_overlay
status: phase2_pressure_sample
project_id: MISA
project_name: misa-cybernetic-evolution
created_at: 2026-06-05
truth_boundary: sandbox sidecar overlay only; not reviewed knowledge; not ADR; not action basis; not Misa project decision
source_project_path: C:\Users\Administrator\Documents\New project\misa-cybernetic-evolution
write_scope: outputs/review sandbox only
---

# MISA Project-Scoped Sidecar Overlay

## Boundary

This is a second-project pressure-test sample for VAKS. It does not modify Misa.

It tests whether the same reusable candidate patterns can carry a project-scoped
Misa view without rewriting the generic candidate pattern, becoming an ADR,
creating action basis, or bypassing v0.2.13.

Plain rule:

```text
Misa overlay = temporary project view and navigation hint.
Misa decision = separate decision/control record in Misa, if ever needed.
Misa action basis = v0.2.13 warrant gate first.
```

## Entry Count

```text
entries: 11
concrete target entries: 10
conceptual-only entries: 1
intended lifecycle coverage:
  candidate experience snapshot: 1
  candidate boundary snapshot: 2
  archive: 3
  delete+tombstone: 1
  carry-forward: 1
  supersede/withdraw: 1
  action-facing escalation: 1
```

## Lens Entries

### Entry: `retrieval-is-activation-not-truth`

```yaml
project: MISA
kp_id: retrieval-is-activation-not-truth
kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
stance: partial
borrow_scope: Use as a hard boundary for perception digest, vector ranker, and runtime adapter outputs.
non_borrow_scope: Do not let suggested_priority, route pressure, vector rank, attention queues, or digest hints become route authority, confidence, promotion, or action readiness.
target_hint:
  - type: repo_symbol
    value: scripts/lib/perception-sidecar.mjs::buildPerceptionDigest
    status: healthy
    anchor_version: 2026-06-05-file-and-symbol-read
  - type: repo_symbol
    value: scripts/lib/component-health.mjs::buildComponentHealthDiagnostics
    status: healthy
    anchor_version: 2026-06-05-file-and-symbol-read
  - type: doc
    value: README.md#Current Local Review Path
    status: not_checked
    anchor_version: heading-approx
reason_1liner: Misa already produces many hint/digest/ranker surfaces; this boundary prevents them from becoming control authority.
updated_at: 2026-06-05
```

### Entry: `memory-granularity-and-quarantine`

```yaml
project: MISA
kp_id: memory-granularity-and-quarantine
kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
stance: partial
borrow_scope: Preserve Misa's no-persistent-memory-write and candidate-only memory/update posture.
non_borrow_scope: Do not allow runtime-thread, health diagnostics, perception digest, or Hermes adapter output to write durable memory directly.
target_hint:
  - type: repo_symbol
    value: scripts/lib/runtime-thread.mjs::SAFETY
    status: healthy
    anchor_version: 2026-06-05-file-and-symbol-read
  - type: repo_symbol
    value: scripts/lib/component-health.mjs::SAFETY
    status: healthy
    anchor_version: 2026-06-05-file-and-symbol-read
  - type: test
    value: test/v028-runtime-thread.test.mjs
    status: healthy
    anchor_version: 2026-06-05-file-read
outcome_ref: outputs/review/project-sidecar-seven-candidate-pressure-test-2026-06-05/snapshots/landed/misa-runtime-memory-quarantine-no-effect-gate.md
reason_1liner: Misa already has a non-self-referential runtime no-effect gate that matches memory quarantine.
updated_at: 2026-06-05
```

### Entry: `file-first-agent-workbench`

```yaml
project: MISA
kp_id: file-first-agent-workbench
kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
stance: partial
borrow_scope: Keep Misa's runtime contracts, schemas, examples, tests, and handoff surfaces visible as files.
non_borrow_scope: File visibility is not truth, execution permission, or owner approval.
target_hint:
  - type: doc
    value: ARCHITECTURE.md
    status: healthy
    anchor_version: 2026-06-05-file-read
  - type: doc
    value: docs/current/runtime-thread-v0.28.md
    status: healthy
    anchor_version: 2026-06-05-file-read
  - type: doc
    value: docs/current/component-health-diagnostics-v0.29.md
    status: healthy
    anchor_version: 2026-06-05-file-read
  - type: module
    value: docs/templates/distillation
    status: not_checked
    anchor_version: path-listed
reason_1liner: Misa's safety posture is reviewable because contracts and reducers are visible in repo files.
updated_at: 2026-06-05
```

### Entry: `adaptive-retrieval-depth`

```yaml
project: MISA
kp_id: adaptive-retrieval-depth
kp_ref: outputs/review/candidate_pattern_bank/adaptive-retrieval-depth.md
stance: park
borrow_scope: Consider only after current local/shadow retrieval checks show repeated recall failure.
non_borrow_scope: Do not add adaptive depth as a runtime controller or automatic route mutation path.
target_hint:
  - type: command
    value: npm run vector-memory:rank
    status: not_checked
    anchor_version: package-json-script-found
  - type: repo_symbol
    value: scripts/lib/perception-sidecar.mjs::priorityFor
    status: healthy
    anchor_version: 2026-06-05-file-and-symbol-read
reason_1liner: Misa already has enough control complexity; adaptive retrieval should wait for concrete failures.
updated_at: 2026-06-05
```

### Entry: `adaptive-retrieval-depth-duplicate-vector-priority`

```yaml
project: MISA
kp_id: adaptive-retrieval-depth
kp_ref: outputs/review/candidate_pattern_bank/adaptive-retrieval-depth.md
stance: watch
borrow_scope: Tune vector priority in Misa based on attention queue scores.
non_borrow_scope:
target_hint:
  - type: unknown
    value: vector priority everywhere
    status: unanchored
    anchor_version: none
reason_1liner: Duplicate low-value entry intentionally included to test delete+tombstone.
updated_at: 2026-06-05
```

### Entry: `graph-and-ontology-as-candidate-context`

```yaml
project: MISA
kp_id: graph-and-ontology-as-candidate-context
kp_ref: outputs/review/candidate_pattern_bank/graph-and-ontology-as-candidate-context.md
stance: avoid
borrow_scope: Use graph or LangGraph only as carrier/context shape when deterministic control stays outside it.
non_borrow_scope: Do not let graph nodes, community summaries, or LangGraph routes own winner authority, route authority, or policy mutation.
target_hint:
  - type: doc
    value: ARCHITECTURE.md#LangGraph Bridge Boundary
    status: not_checked
    anchor_version: heading-approx
  - type: doc
    value: docs/current/control-boundaries.md
    status: healthy
    anchor_version: 2026-06-05-file-read
reason_1liner: Misa can use graph/carrier layers, but Qianxuesen must own deterministic control authority.
updated_at: 2026-06-05
```

### Entry: `visual-workbench-for-retrieval-diagnostics`

```yaml
project: MISA
kp_id: visual-workbench-for-retrieval-diagnostics
kp_ref: outputs/review/candidate_pattern_bank/visual-workbench-for-retrieval-diagnostics.md
stance: partial
borrow_scope: Use diagnostic outputs to expose component health and retrieval/tool-loop failure modes.
non_borrow_scope: Do not treat dashboards, health colors, or clean reports as readiness or action basis.
target_hint:
  - type: repo_symbol
    value: scripts/lib/component-health.mjs::diagnosticCandidateForComponent
    status: healthy
    anchor_version: 2026-06-05-file-and-symbol-read
  - type: test
    value: test/component-health.test.mjs
    status: healthy
    anchor_version: 2026-06-05-file-read
reason_1liner: Misa health surfaces are useful only because they remain replayable diagnostic candidates for humans.
updated_at: 2026-06-05
```

### Entry: `skills-and-prompts-as-visible-files`

```yaml
project: MISA
kp_id: skills-and-prompts-as-visible-files
kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
stance: watch
borrow_scope: Carry forward to the next Misa skill-control phase for visible prompt/template review.
non_borrow_scope: Do not allow prompt/template edits to publish skills, install skills, or mutate runtime authority.
target_hint:
  - type: doc
    value: docs/current/skill-control-intake-template.md
    status: not_checked
    anchor_version: path-listed
  - type: module
    value: prompts
    status: not_checked
    anchor_version: root-dir-listed
reason_1liner: Misa has visible prompt/skill surfaces, but the current pressure test is not a skill-control phase.
updated_at: 2026-06-05
```

### Entry: `search-to-analysis-before-answer`

```yaml
project: MISA
kp_id: search-to-analysis-before-answer
kp_ref: outputs/review/candidate_pattern_bank/search-to-analysis-before-answer.md
stance: partial
borrow_scope: Use as drafting discipline before answering whether Misa should promote a sidecar diagnostic or route change.
non_borrow_scope: Do not make every Misa status question a heavy evidence packet.
target_hint:
  - type: doc
    value: CONTROL_CONTRACT.md
    status: healthy
    anchor_version: 2026-06-05-file-read
  - type: doc
    value: docs/current/control-boundaries.md
    status: healthy
    anchor_version: 2026-06-05-file-read
  - type: repo_symbol
    value: scripts/lib/component-health.mjs::buildComponentHealthDiagnostics
    status: healthy
    anchor_version: 2026-06-05-file-and-symbol-read
reason_1liner: This becomes useful only when a Misa candidate is about to affect action-facing control decisions.
updated_at: 2026-06-05
```

### Entry: `simple-first-retrieval-baseline`

```yaml
project: MISA
kp_id: simple-first-retrieval-baseline
kp_ref: outputs/review/candidate_pattern_bank/simple-first-retrieval-baseline.md
stance: partial
borrow_scope: Prefer local deterministic command/test evidence before adding heavier vector/GraphRAG behavior to the control loop.
non_borrow_scope: Do not claim vector retrieval is unnecessary in all Misa cases.
target_hint:
  - type: command
    value: npm run runtime:thread -- --json
    status: not_checked
    anchor_version: package-json-script-found
  - type: command
    value: npm run health:components -- --json
    status: not_checked
    anchor_version: package-json-script-found
  - type: test
    value: test/v028-runtime-thread.test.mjs
    status: healthy
    anchor_version: 2026-06-05-file-read
reason_1liner: Misa's current-line review already starts from local deterministic checks.
updated_at: 2026-06-05
```

### Entry: `source-structure-first-rag`

```yaml
project: MISA
kp_id: source-structure-first-rag
kp_ref: outputs/review/candidate_pattern_bank/source-structure-first-rag.md
stance: park
borrow_scope: Preserve event-log and fixture structure if future Misa evidence windows become long source packets.
non_borrow_scope: Do not introduce heavy document chunking for ordinary runtime events or small JSON fixtures.
target_hint:
  - type: module
    value: test/fixtures
    status: not_checked
    anchor_version: path-listed
  - type: repo_symbol
    value: scripts/lib/runtime-thread.mjs::event_log
    status: healthy
    anchor_version: 2026-06-05-file-and-symbol-read
reason_1liner: Misa's current sources are already structured event logs and fixtures; heavy source-structure RAG is premature.
updated_at: 2026-06-05
```

## Current Interpretation

Misa is a strong second-project sample because most entries can point to concrete docs, modules, tests, commands, or schemas. The overlay also exposes exactly the leakage risk Pro warned about: many Misa surfaces look operational, so an unsafe overlay could easily start sounding like route authority, action basis, or ADR.
