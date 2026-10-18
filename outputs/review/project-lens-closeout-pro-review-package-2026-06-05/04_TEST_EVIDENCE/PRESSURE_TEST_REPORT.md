---
type: pressure_test_report
status: pass_after_patches
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-mainline-integration-pressure-test
truth_boundary: sandbox test report only; not reviewed knowledge; not mainline architecture
---

# Project Lens Mainline Integration Pressure Test Report

## Current Verdict

```text
pass_after_patches
```

Human-readable verdict:

```text
Project Lens is better than the old Project Borrowing Ledger logic as a candidate sidecar.
High-intensity retesting found and fixed real operational issues.
```

Why:

```text
The sidecar is now readable, parseable, isolated, and less authority-leaky.
The simulated mainline wording stays minimal and does not require schema/template changes.
After the high-intensity run, no blocking issue remains inside this sandbox; the remaining risk is scoped commit / future governance, not concept shape.
```

## Automated Evidence

Structured sidecar check:

```text
block_count=10
structured_block_check=pass
duplicate_ids=none
wide_table_present=false
anchor_health_values=mixed,conceptual
structured_target_hint_statuses=healthy,conceptual inside target_hint objects
structured_target_hint_check=pass
formal_code_anchor_field_mentions=0
```

High-intensity follow-up:

```text
kp_ref_check=pass
source_routing_missing_pattern_routes=0 after patch
candidate_pattern_source_refs_missing=0
pattern_to_lens_mismatch=0
outcome_refs=2
missing_outcome_refs=0
snapshot_candidate_files=4
blocking_issue_remaining=none_found_in_current_sandbox
```

Mainline non-pollution check:

```text
Project Lens mentions in FUSION / ARCHITECTURE_PRINCIPLES / SCHEMA / REVIEW_QUEUE / templates: none
Core / Lens / Snapshot or Grok additions in mainline: none
formal Core_KP / Lenses / Snapshots folders created: none
```

Obsidian sandbox check:

```text
obsidian_target=H:\Obsidian\资料库\outputs\review\project-lens-mainline-sandbox-2026-06-05
copied_files=21 after high-intensity sync
hash_mismatches=0
root_hash_unchanged FUSION_ARCHITECTURE_V0_2_DRAFT.md=True
root_hash_unchanged ARCHITECTURE_PRINCIPLES.md=True
SCHEMA.md present at Obsidian root=False
REVIEW_QUEUE.md present at Obsidian root=False
SCHEMA.md / REVIEW_QUEUE.md root hash comparison=not_applicable_not_written
```

## Test Results

| ID | Verdict | Evidence / Finding |
|---|---|---|
| T01 Format scalability | pass after patch | Wide table removed; 10 `Lens Entry` blocks detected; block format is easier in Obsidian. |
| T02 Source boundary | pass | Source routing now uses `Project Routes Optional`; remaining adopt wording is negative boundary text only. |
| T03 Generic knowledge pollution | pass | Project Lens fields stay in `outputs/review/project_lens_overlays/VAKS.md`; no original knowledge-point YAML/body was changed. |
| T04 Ledger drift | pass | `project_borrowing_ledgers/VAKS.md` now declares itself a derived view and points to the sidecar as source overlay. |
| T05 ADR leakage | pass with caveat | Candidate wording says not ADR/action basis; still needs real-agent repetition testing because "Project Lens" can drift if written too narratively. |
| T06 Truth leakage | pass | Guardrails explicitly reject stance/reuse/source/dashboard/retrieval/GraphRAG/AI summary as support strength. |
| T07 Outcome confusion | pass | `landed` is not a stance; `outcome_ref` is blank in live entries; snapshots are separate. |
| T08 v0.2.13 false trigger | pass | Ordinary lens entries do not create action-basis packets. |
| T09 v0.2.13 missed trigger | pass in design | Candidate mainline patch requires warrant gate for decision / promotion / action basis; no live action-basis use was attempted. |
| T10 target_hint drift | fixed then pass | Initial anchor health was too coarse; checked concrete docs and changed module/workflow hints to `conceptual`. |
| T11 Candidate Pattern bloat | pass with caveat | Index now says pattern bank is high-threshold; current bank still has many pilot entries and should be watched. |
| T12 Obsidian isolation | pass | Sandbox copied to isolated Obsidian path; existing root architecture hashes unchanged; SCHEMA / REVIEW_QUEUE were not present at Obsidian root and were not written. |
| T13 Agent recovery | pass | Handoff, memory alignment, usage guide, sidecar index, and sandbox README all point to Project Lens sidecar. |
| T14 Negative knowledge | pass with caveat | Boundary snapshot seed shape exists; no real boundary snapshot has been tested yet. |
| T15 AI authority | pass | AI can suggest lens entries but cannot confirm landed / avoid / boundary / action basis. |
| T16 Cross-project reuse | pass in structure | Sidecar is project-scoped (`project: VAKS`); no other project stance is written into VAKS entries. Needs a second project sample later. |
| T17 Search/readability | pass | `rg "Lens Entry"` and `rg "kp_id"` directly locate entries; no horizontal table scan required. |
| T18 Mainline patch minimality | pass | Candidate patch is paragraph-level and includes explicit non-goals: no schema/template/formal workspace/all-intake-heavy. |
| T19 Obsidian readability | pass | Block-form sidecar copied as `VAKS-project-lens-overlay.md` to Obsidian sandbox. |
| T20 Commit scope | pass with caveat | No staging/commit performed; workspace is very dirty, so any future commit must be scoped and must not use `git add .`. |
| T21 Three-layer clarity | pass | Core / Lens / Snapshot added only as sandbox vocabulary, not as formal folders or schema. |
| T22 Structured target hints | pass | `target_hint` now uses typed objects with `type`, `value`, `status`, and `anchor_version`; field name stays weak to avoid decision semantics. |
| T23 Graph-lite overreach | pass | Knowledge Graph Lite was deferred; no `related_kp`, `depends_on`, or `conflicts_with` fields were added to Core. |
| T24 Pipeline overreach | pass | Warrant Gate pipeline was deferred; no checklist templates or staged workflow were created. |
| T25 Governance overreach | pass | Ownership/deprecation/annual review were recorded as future only; no governance layer was created. |
| T26 Future extension leakage | pass | Integrations/export/agent-write ideas were recorded as reserve only; no automation or write authority was added. |
| T27 Agent navigation chain | pass after patch | Added `kp_ref`; Lens -> candidate pattern -> raw source chain validates. |
| T28 Source routing integrity | pass after patch | Fixed missing `agent-memory-quarantine` route; all 10 pattern routes resolve. |
| T29 Snapshot linkage | pass | Created 4 candidate snapshots and linked 2 Lens entries through existing outcome_ref paths. |
| T30 Automation patch safety | pass with rule | Repeated YAML fields require block-context patching and line-bounded parsing. |

## Problems Found

### P1. Wide Table Was Not Scalable

Status:

```text
fixed
```

Patch:

```text
Converted `outputs/review/project_lens_overlays/VAKS.md` from a wide Markdown table to one `Lens Entry` block per knowledge point.
```

### P2. Anchor Health Was Too Coarse

Status:

```text
fixed
```

Problem:

```text
Every entry originally said `anchor_health: pattern_id_only`, even entries with concrete `doc:` targets.
```

Patch:

```text
Checked `SOURCE_INTAKE.md` and `MEMORY_TIER.md#Activation Tier`.
Concrete checked doc anchors now use `healthy`.
Conceptual module/workflow hints use `conceptual`.
```

### P3. Grok Suggestions Could Re-Inflate The Design

Status:

```text
fixed_by_triage
```

Problem:

```text
Core/Lens/Snapshot, graph fields, pipeline stages, governance, and integrations are all plausible,
but adding all of them now would turn Project Lens back into a heavy platform architecture.
```

Patch:

```text
Added `GROK_RECOMMENDATION_TRIAGE.md`.
Kept Core / Lens / Snapshot as sandbox vocabulary.
Absorbed structured `target_hint`.
Deferred graph-lite fields, Warrant Gate pipeline, governance, and integrations.
```

### P4. Source Routing Had A Broken Candidate Pattern Route

Status:

```text
fixed
```

Issue:

```text
`agent-memory-quarantine` appeared in source routing but did not exist in Candidate Pattern Bank.
```

Patch:

```text
Replace with `memory-granularity-and-quarantine`.
```

### P5. Project Lens Needed Agent-Navigable Refs

Status:

```text
fixed
```

Issue:

```text
`kp_id` was meaningful but not directly navigable.
```

Patch:

```text
Add `kp_ref` to every Lens Entry.
```

### P6. Repeated YAML Fields Are Easy To Patch Wrong

Status:

```text
mitigated
```

Issue:

```text
Naive repeated-field patching misplaced outcome_ref during testing.
```

Mitigation:

```text
Patch with Lens Entry block context and validate outcome_ref paths after edits.
```

### P7. Regex Newline Parsing Can Lie

Status:

```text
mitigated
```

Issue:

```text
`outcome_ref:\s*(.*)` misread blank outcome_ref as the next line.
```

Mitigation:

```text
Use line-bounded parsing.
```

## Remaining Weak Spots

```text
1. target_hint still lacks a small registry for module/workflow names.
2. Candidate Pattern Bank may still bloat if future agents promote pretty names too eagerly.
3. Obsidian test proves isolated visibility, not that ordinary users will prefer the format.
4. Core / Lens / Snapshot is useful vocabulary, but formal folders would be premature.
5. The repo worktree is very dirty, so any commit must be manually scoped.
```

## Real Case Trials

Additional real-case trials were run in:

```text
outputs/review/project-lens-mainline-sandbox-2026-06-05/REAL_CASE_TRIALS.md
```

Results:

```yaml
ordinary_source_route_false_upgrade: pass
action_facing_mainline_merge_attempt: pass_blocked_mainline_merge
negative_knowledge_dry_run: pass_with_caveat
```

Most important result:

```text
The current evidence supports Project Lens as an operational candidate sidecar.
It does not authorize an automatic mainline merge or commit.
```

## Final Sandbox Judgment

```yaml
project_lens_direction: stronger_than_old_ledger_logic
sidecar_format: block_form_passes_current_tests
obsidian_sandbox: pass
mainline_merge_without_user_approval: no
schema_change_now: no
template_change_now: no
formal_workspace_directory_now: no
recommended_next_step: scoped review/commit decision by user
grok_additions: absorb_three_layer_vocabulary_and_structured_target_hint_only
kp_ref: keep
conceptual_target_status: keep
snapshot_trial: pass
blocking_issue_remaining: none_found_in_current_sandbox
```
