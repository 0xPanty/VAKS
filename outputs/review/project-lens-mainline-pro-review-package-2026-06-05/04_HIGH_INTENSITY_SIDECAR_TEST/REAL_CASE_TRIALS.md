---
type: real_case_trials
status: completed
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-real-case-pressure-trials
truth_boundary: sandbox trial only; not reviewed knowledge; not mainline architecture; not action basis for external use
---

# Real Case Trials

## Trial A: Ordinary Source Route Should Stay Light

### Setup

Source route:

```text
raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md
```

Potential routes:

```text
visual-workbench-for-retrieval-diagnostics
source-structure-first-rag
retrieval-is-activation-not-truth
```

### Pressure

Try to force this ordinary routing note into a decision:

```text
Because the RAGLab source has visual diagnostics and RAGAS, VAKS should adopt a visual retrieval workbench.
```

### Expected Behavior

```text
Block the adoption claim.
Allow only routing hint / Project Lens suggestion.
Do not trigger v0.2.13 unless a real decision/action-basis is being made.
```

### Observed Behavior

Current source routing language says:

```text
may route to VAKS Project Lens: watch/partial for future context-pack workbench
```

It does not say:

```text
VAKS should adopt a visual retrieval workbench
```

### Verdict

```yaml
result: pass
v0_2_13_triggered: no
allowed_output: routing_hint_or_lens_suggestion
blocked_output: project_adoption_decision
```

## Trial B: Action-Facing Mainline Merge Attempt

### Question

```text
Should VAKS merge Project Lens into the main architecture now?
```

This is action-facing because it would modify main architecture docs and future agent recovery behavior.

### Action-Facing Claim

```text
Do not merge Project Lens into the main architecture now.
Keep it as a candidate sidecar pilot in outputs/review until repeated real use proves it stays light and non-authoritative.
```

### Anchored Evidence

Evidence 1:

```text
outputs/review/2026-06-05-v0-2-13-project-lens-pro-response-landing.md
```

Support:

```text
Pro accepts the direction but frames it as project-scoped sidecar overlay, not schema/template/mainline object.
```

Evidence 2:

```text
outputs/review/project-lens-mainline-sandbox-2026-06-05/PRESSURE_TEST_REPORT.md
```

Support:

```text
Pressure test verdict is now pass_after_patches for the candidate sidecar.
It still does not authorize automatic mainline merge without user approval.
```

Evidence 3:

```text
outputs/review/project_lens_overlays/VAKS.md
```

Support:

```text
Sidecar has working block-form entries, direct kp_ref, structured target_hint, conceptual target status, and 2 resolved outcome_ref links.
```

Evidence 4:

```text
outputs/review/project-lens-mainline-sandbox-2026-06-05/OBSIDIAN_SANDBOX_CHECK.md
```

Support:

```text
Obsidian sandbox visibility works and root architecture hashes stayed unchanged.
```

### Non-Circular Warrant

The evidence supports treating Project Lens as an operational candidate sidecar because the sidecar is readable, isolated, source-chain traceable, and tested against snapshot linkage and source-routing integrity.

The same evidence does not by itself authorize automatic mainline merge, because mainline merge is an architecture decision and commit-scope decision. It requires explicit user approval and scoped staging.

### Scope / Assumptions

Scope:

```text
Project Lens concept and sidecar format only.
Not v0.2.13 minimal action-facing review rule.
Not the already-landed mainline wording.
```

Assumptions:

```text
outputs/review remains acceptable for candidate-only VAKS architecture experiments.
No downstream workflow currently requires Project Lens as a formal architecture object.
```

### Known Challenges / Gaps

```text
50+ entry scale not tested.
Module/workflow conceptual target registry not created.
Commit scope is risky because the worktree is very dirty.
Candidate Pattern Bank bloat remains a possible failure mode.
```

### Residual Review / Risk

```text
Risk: if merged without explicit scope, Project Lens may become a hidden decision layer or be committed with unrelated dirty files.
Mitigation: keep mainline unchanged unless the user explicitly requests a scoped mainline patch / scoped commit.
```

### Verdict

```yaml
result: pass
candidate_sidecar_ready: yes
mainline_merge_without_user_approval: blocked
keep_candidate_sidecar: yes
v0_2_13_triggered: yes
reason: warrant supports candidate-sidecar viability, not automatic architecture absorption
```

## Trial C: Negative Knowledge Dry Run

### Candidate Trap

```text
retrieval score / rerank score / dashboard pass is treated as truth confidence
```

### Boundary Snapshot Draft

```yaml
trap_title: Retrieval score treated as truth
bad_move_or_non_fit: Using retrieval/rerank/dashboard success as evidence support or truth confidence.
failure_context: Context-pack preparation, GraphRAG summaries, retrieval diagnostics, or source routing.
trigger_conditions:
  - A result is called supported because it was retrieved or ranked highly.
  - A dashboard or RAG evaluation score is cited as action readiness.
  - A community summary or graph hit is treated as reviewed relation.
why_it_failed: Retrieval and diagnostics can activate context, but they do not review evidence, check scope, or establish a non-circular warrant.
boundary_of_applicability: Applies to VAKS reviewed knowledge, action basis, strong relation promotion, and risk-sensitive answers.
similar_keywords:
  - retrieval score
  - rerank
  - RAGAS
  - GraphRAG summary
  - dashboard pass
warning_1liner: Retrieval can bring material into view; it cannot make the material true.
safer_alternative_or_escalation: Treat as activation/diagnostic signal; if action-facing, run v0.2.13 warrant gate.
evidence_refs:
  - outputs/review/project_lens_overlays/VAKS.md
  - outputs/review/2026-06-05-v0-2-13-usage-guide.md
```

### Verdict

```yaml
result: pass_with_caveat
useful_as_boundary_snapshot_shape: yes
ready_as_reviewed_negative_knowledge: no
reason: shape is triggerable, but evidence review and real failure context are still missing
```

### High-Intensity Follow-Up

Candidate snapshots were created after this dry run:

```text
outputs/review/project-lens-mainline-sandbox-2026-06-05/snapshots/boundary/retrieval-score-is-not-support.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/snapshots/boundary/graph-lite-core-pollution.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/snapshots/boundary/project-lens-as-adr.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/snapshots/landed/project-lens-sidecar-agent-maintenance-sandbox.md
```

Updated verdict:

```yaml
snapshot_shape_tested: yes
outcome_ref_resolution_tested: yes
reviewed_negative_knowledge: no
candidate_snapshot_layer: pass
```
