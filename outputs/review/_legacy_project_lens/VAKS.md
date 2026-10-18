---
type: project_lens_overlay
record_kind: project_overlay
status: pilot
project_id: VAKS
project_name: Verified Action Knowledge System / 资料库
created_at: 2026-06-05
truth_boundary: project lens sidecar only; not reviewed knowledge; not ADR; not action
  basis; not schema; not template
authoring_surface: pilot sidecar overlay
derived_view: outputs/review/project_borrowing_ledgers/VAKS.md
overlay_state: confirmed
retrieval_scope: active_project_only
default_retrieval: false
review_pressure: none
target_ref: outputs/review/project_borrowing_ledgers/VAKS.md
project_borrow_scope: For project VAKS, borrow only the listed target_layers/target_hint
  and body Borrow Scope as orientation or review input, not reviewed support or action
  basis.
project_non_borrow_scope: For project VAKS, do not borrow listed non_target_layers/body
  non-borrow scope as reviewed truth, reviewed relation, or action basis.
project_reopen_trigger: Reopen if active project scope, source evidence, target layers,
  or review gate requirements change.
legacy_overlay_compatibility: true
canonical_p0_included: false
canonical_current_lint_scope: false
legacy_storage: outputs/review/_legacy_project_lens
---
# VAKS Project Lens Overlay

## 说人话

这份文件是 VAKS 当前项目的 Project Lens sidecar。

它的意思不是：

```text
这个知识点是真的
VAKS 已经采用
VAKS 已经拒绝
这是架构决定
```

它的意思只是：

```text
VAKS 当前从项目视角怎么看这个通用知识点。
```

通用知识点本体保持干净。这个文件只是项目侧联标记层。

## Field Contract

Required candidate fields:

```text
project
kp_id
kp_ref
stance
borrow_scope
target_hint
reason_1liner
```

Optional candidate fields:

```text
non_borrow_scope
gate_hint
review_origin
outcome_ref
updated_at
anchor_health
```

Allowed stance values:

```text
watch   = looks relevant; observe
partial = some part may be borrowed, but not the whole source/pattern
avoid   = current project should not borrow this move
park    = pause until conditions change
```

`landed` is not a stance. If something really lands, create or link a `landed_snapshot`.

`踩坑 / rejected` is not just a stance. If something becomes reusable negative knowledge, create or link a `boundary_snapshot`.

## Target Hint Convention

Use structured locators that future agents can inspect quickly:

```yaml
target_hint:
  - type: doc | repo_symbol | repo_line | module | workflow | pr | unknown
    value: "<locator>"
    status: active | healthy | conceptual | not_checked | drifted | unanchored
    anchor_version: "<optional version, date, commit, or file-check note>"
```

Keep the field name `target_hint`, not `code_anchor`, because it is still only a possible action location. A hint can help navigation, but it is not a decision to modify that file/module.

Prefer `path + heading/symbol/module`. Line numbers are only auxiliary because they can drift.

## Anchor Health

If a lens points to a specific heading, symbol, selector, or line, track whether it can still be resolved.

Candidate values:

```text
not_checked
healthy
conceptual
drifted
unanchored
pattern_id_only
mixed
```

`healthy` means the file or heading anchor was checked where a concrete `doc:` target exists. Conceptual `module:` and `workflow:` hints may still need future implementation mapping.

`mixed` means an entry has at least one checked target and at least one conceptual or unresolved target.

`conceptual` means the target names a workflow/module idea that helps routing, but does not yet have a stable file, heading, symbol, or registry entry.

## Lens Entries

Each entry is a block instead of a wide table. This keeps the sidecar readable in Obsidian and makes it easier for agents to parse one knowledge point at a time.

### Lens Entry: `source-structure-first-rag`

```yaml
project: VAKS
kp_id: source-structure-first-rag
kp_ref: outputs/review/candidate_pattern_bank/source-structure-first-rag.md
stance: partial
borrow_scope: Preserve source structure when preparing source intake and context packs.
non_borrow_scope: Do not treat source structure as truth, support strength, or action readiness.
target_hint:
  - type: workflow
    value: source-intake
    status: conceptual
    anchor_version: workflow-name-only
  - type: doc
    value: SOURCE_INTAKE.md
    status: healthy
    anchor_version: 2026-06-05-file-exists
reason_1liner: VAKS depends on raw/source/candidate/review boundaries, and structure loss can corrupt later activation.
gate_hint: design-review
review_origin: ai_suggested
outcome_ref:
updated_at: 2026-06-05
anchor_health: mixed
reuse_closeout:
  status: original_architecture_covered
  checked_at: 2026-06-08
  result: "No new merge from this Project Lens entry; source structure is already covered by SOURCE_INTAKE, source anchors, and graph retrieval stratification."
  do_not_repeat_as_new_candidate: true
```

### Lens Entry: `retrieval-is-activation-not-truth`

```yaml
project: VAKS
kp_id: retrieval-is-activation-not-truth
kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
stance: partial
borrow_scope: Reuse as a boundary reminder for activation, context packs, and review wording.
non_borrow_scope: Do not use retrieval hit, rerank, GraphRAG, dashboard, or feedback as truth confidence.
target_hint:
  - type: doc
    value: MEMORY_TIER.md#Activation Tier
    status: healthy
    anchor_version: 2026-06-05-heading-found
  - type: workflow
    value: context-pack-preparation
    status: conceptual
    anchor_version: workflow-name-only
reason_1liner: This already matches the VAKS spine; retrieval can activate context, not create reviewed truth.
gate_hint: design-review
review_origin: ai_suggested
outcome_ref: outputs/review/project-lens-mainline-sandbox-2026-06-05/snapshots/boundary/retrieval-score-is-not-support.md
updated_at: 2026-06-05
anchor_health: mixed
reuse_closeout:
  status: original_architecture_covered
  checked_at: 2026-06-08
  result: "No new merge from this Project Lens entry; retrieval-is-activation-not-truth is already a strong mainline boundary."
  do_not_repeat_as_new_candidate: true
```

### Lens Entry: `file-first-agent-workbench`

```yaml
project: VAKS
kp_id: file-first-agent-workbench
kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
stance: watch
borrow_scope: Explore visible files for future dev context, workbench, or inspector surfaces.
non_borrow_scope: Do not let memory/tool output bypass quarantine or reviewed boundaries.
target_hint:
  - type: module
    value: future-agent-workbench
    status: conceptual
    anchor_version: conceptual-module
  - type: workflow
    value: dev-context-inspection
    status: conceptual
    anchor_version: workflow-name-only
reason_1liner: File visibility may reduce black-box agent behavior, but editable memory/prompt surfaces can pollute knowledge.
gate_hint: prototype
review_origin: ai_suggested
outcome_ref:
updated_at: 2026-06-05
anchor_health: conceptual
reuse_closeout:
  status: future_workbench_only
  checked_at: 2026-06-08
  result: "Not merged in this hardening line; file-first agent workbench remains a future workbench/runtime idea, while Markdown-as-system-of-record is already mainline."
  do_not_repeat_as_new_candidate: true
```

### Lens Entry: `adaptive-retrieval-depth`

```yaml
project: VAKS
kp_id: adaptive-retrieval-depth
kp_ref: outputs/review/candidate_pattern_bank/adaptive-retrieval-depth.md
stance: watch
borrow_scope: Consider query-mode or activation-budget hints.
non_borrow_scope: Do not build a heavy retrieval runtime before ordinary query needs prove it.
target_hint:
  - type: module
    value: activation-tier
    status: conceptual
    anchor_version: conceptual-module
  - type: workflow
    value: context-pack-budgeting
    status: conceptual
    anchor_version: workflow-name-only
reason_1liner: Fast/slow retrieval ideas are useful, but VAKS currently needs boundary clarity more than runtime complexity.
gate_hint: prototype
review_origin: ai_suggested
outcome_ref:
updated_at: 2026-06-05
anchor_health: conceptual
reuse_closeout:
  status: original_architecture_covered
  checked_at: 2026-06-08
  result: "No new merge from this Project Lens entry; ordinary query stays light, strict gates are lazy, and context-pack budget ideas are already covered enough for now."
  do_not_repeat_as_new_candidate: true
```

### Lens Entry: `memory-granularity-and-quarantine`

```yaml
project: VAKS
kp_id: memory-granularity-and-quarantine
kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
stance: watch
borrow_scope: Reuse as pressure for agent memory quarantine and feedback boundaries.
non_borrow_scope: Do not allow agent-written memory to mutate reviewed truth.
target_hint:
  - type: doc
    value: MEMORY_TIER.md
    status: healthy
    anchor_version: 2026-06-05-file-exists
  - type: workflow
    value: feedback-ledger
    status: conceptual
    anchor_version: workflow-name-only
reason_1liner: Multi-granularity memory is useful only if write authority stays quarantined.
gate_hint: design-review
review_origin: ai_suggested
outcome_ref:
updated_at: 2026-06-05
anchor_health: mixed
reuse_closeout:
  status: original_architecture_covered
  checked_at: 2026-06-08
  result: "No new merge from this Project Lens entry; feedback-not-truth, agent memory quarantine, and review_due pressure are already mainline boundaries."
  do_not_repeat_as_new_candidate: true
```

### Lens Entry: `graph-and-ontology-as-candidate-context`

```yaml
project: VAKS
kp_id: graph-and-ontology-as-candidate-context
kp_ref: outputs/review/candidate_pattern_bank/graph-and-ontology-as-candidate-context.md
stance: watch
borrow_scope: Use graph/ontology ideas as candidate context or optional point fragments.
non_borrow_scope: Do not let graph rank, community summaries, or auto-extracted relations become reviewed relations.
target_hint:
  - type: module
    value: relation-review
    status: conceptual
    anchor_version: conceptual-module
  - type: workflow
    value: context-neighborhood-activation
    status: conceptual
    anchor_version: workflow-name-only
reason_1liner: Graph structure can organize review context, but cannot create support or truth by itself.
gate_hint: design-review
review_origin: ai_suggested
outcome_ref: outputs/review/project-lens-mainline-sandbox-2026-06-05/snapshots/boundary/graph-lite-core-pollution.md
updated_at: 2026-06-05
anchor_health: conceptual
reuse_closeout:
  status: original_architecture_covered
  checked_at: 2026-06-08
  result: "No new merge from this Project Lens entry; optional point graph fragments, candidate_relation, reviewed relation boundaries, and graph-rank-not-trust are already covered."
  do_not_repeat_as_new_candidate: true
```

### Lens Entry: `visual-workbench-for-retrieval-diagnostics`

```yaml
project: VAKS
kp_id: visual-workbench-for-retrieval-diagnostics
kp_ref: outputs/review/candidate_pattern_bank/visual-workbench-for-retrieval-diagnostics.md
stance: partial
borrow_scope: Prototype diagnostic surfaces for retrieval/context-pack failures.
non_borrow_scope: Do not let dashboards or clean diagrams become confidence or readiness signals.
target_hint:
  - type: module
    value: future-reviewer-workbench
    status: conceptual
    anchor_version: conceptual-module
  - type: workflow
    value: retrieval-diagnostics
    status: conceptual
    anchor_version: workflow-name-only
reason_1liner: Visual workbenches can reveal failure points, but are diagnostic surfaces only.
gate_hint: prototype
review_origin: ai_suggested
outcome_ref:
updated_at: 2026-06-05
anchor_health: conceptual
reuse_closeout:
  status: future_workbench_only
  checked_at: 2026-06-08
  result: "CI-05 sandbox evidence is positive, but this remains a future reviewer/operator surface, not a mainline truth or approval mechanism."
  do_not_repeat_as_new_candidate: true
```

### Lens Entry: `skills-and-prompts-as-visible-files`

```yaml
project: VAKS
kp_id: skills-and-prompts-as-visible-files
kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
stance: watch
borrow_scope: Consider visible skill/prompt files for future agent workbench reviewability.
non_borrow_scope: Do not allow prompt/skill edits to become unreviewed knowledge writes.
target_hint:
  - type: module
    value: future-agent-workbench
    status: conceptual
    anchor_version: conceptual-module
  - type: workflow
    value: skill-registry
    status: conceptual
    anchor_version: workflow-name-only
reason_1liner: Visible prompts reduce black-box behavior, but editable agent instructions need quarantine.
gate_hint: design-review
review_origin: ai_suggested
outcome_ref:
updated_at: 2026-06-05
anchor_health: conceptual
reuse_closeout:
  status: future_tool_safety_only
  checked_at: 2026-06-08
  result: "Not merged in this hardening line; visible skills/prompts require later tool-safety, permission, and quarantine design."
  do_not_repeat_as_new_candidate: true
```

### Lens Entry: `search-to-analysis-before-answer`

```yaml
project: VAKS
kp_id: search-to-analysis-before-answer
kp_ref: outputs/review/candidate_pattern_bank/search-to-analysis-before-answer.md
stance: watch
borrow_scope: Use as a drafting discipline for context-pack or evidence-envelope preparation.
non_borrow_scope: Do not make every ordinary answer a heavy evidence packet.
target_hint:
  - type: workflow
    value: context-pack-drafting
    status: conceptual
    anchor_version: workflow-name-only
  - type: workflow
    value: evidence-envelope-preparation
    status: conceptual
    anchor_version: workflow-name-only
reason_1liner: Analysis before answer can improve synthesis, but v0.2.13 only triggers for action-facing use.
gate_hint: design-review
review_origin: ai_suggested
outcome_ref:
updated_at: 2026-06-05
anchor_health: conceptual
reuse_closeout:
  status: original_architecture_covered
  checked_at: 2026-06-08
  result: "No new merge from this Project Lens entry; important answer preparation and independent support boundaries already cover this without burdening ordinary queries."
  do_not_repeat_as_new_candidate: true
```

### Lens Entry: `simple-first-retrieval-baseline`

```yaml
project: VAKS
kp_id: simple-first-retrieval-baseline
kp_ref: outputs/review/candidate_pattern_bank/simple-first-retrieval-baseline.md
stance: watch
borrow_scope: Test simple search baselines before complex vector/graph retrieval.
non_borrow_scope: Do not treat simple-first as proof that vectors or graphs are always unnecessary.
target_hint:
  - type: workflow
    value: ordinary-query
    status: conceptual
    anchor_version: workflow-name-only
  - type: module
    value: retrieval-baseline
    status: conceptual
    anchor_version: conceptual-module
reason_1liner: BM25/SQLite/FTS can lower complexity, but scope fit must decide retrieval depth.
gate_hint: prototype
review_origin: ai_suggested
outcome_ref:
updated_at: 2026-06-05
anchor_health: conceptual
reuse_closeout:
  status: original_architecture_covered
  checked_at: 2026-06-08
  result: "No new merge from this Project Lens entry; Karpathy-simple UX and simple local search before heavier retrieval are already mainline implementation heuristics."
  do_not_repeat_as_new_candidate: true
```

## Explicit Avoid Boundaries

These are current VAKS boundaries, not `boundary_snapshot` records yet:

```text
Do not borrow retrieval score / rerank / dashboard / feedback heat as truth confidence.
Do not borrow AI summary as reviewed knowledge.
Do not borrow source-family repetition as independent support.
Do not borrow terminal-tool safety based only on a simple blacklist.
Do not borrow "single source of truth" framing that mixes raw source, insight, decision, and action basis.
```

If one of these becomes a reusable negative-knowledge asset, create a separate `boundary_snapshot` with trigger conditions, failure context, why it failed, warning text, and safer alternative.

## Boundary Snapshot Seed Shape

Candidate negative-knowledge snapshot fields:

```text
trap_title:
bad_move_or_non_fit:
failure_context:
trigger_conditions:
why_it_failed:
boundary_of_applicability:
similar_keywords:
warning_1liner:
safer_alternative_or_escalation:
evidence_refs:
```

## Current Disposition

```yaml
status: candidate_sidecar_pilot
mainline_change: no
schema_change: no
template_change: no
formal_workspace_directory: no
authoring_surface: this_sidecar
ledger_role: derived_project_view
v0_2_13_triggered_by_lens_itself: no
```
