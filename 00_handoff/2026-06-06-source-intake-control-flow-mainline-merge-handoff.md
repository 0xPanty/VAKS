---
type: handoff
status: active_recovery_entry
created_at: 2026-06-06
project: verified-action-knowledge-system
scope: Source Intake Control Flow round1 + round2 mainline merge
truth_boundary: recovery handoff only; not reviewed knowledge; not architecture decision; not action basis
---

# Source Intake Control Flow Mainline Merge Handoff

## One Sentence

Source Intake Control Flow 的两轮测试逻辑现在已经并入主线运行规则和模板：

```text
Round1 mainline audit: 11/11
Round2 mainline audit: 16/16
```

人话：

```text
不是把测试产物搬进主线，而是把测试里发现的运行边界补进 SOURCE_INTAKE 和模板。
```

## Why This Handoff Exists

本轮先做了 Source Intake Control Flow sandbox，再按 Pro 的第二轮建议增强测试。

后续用户追问时发现：虽然核心规则大体写进了 `SOURCE_INTAKE.md`，但两轮测试的设计逻辑没有完全收干净。

缺口包括：

```text
1. Round1 抓到的 retrieval_policy 机器可执行小块没有完整进入主线模板。
2. candidate-distillation 没有正式模板承接。
3. query-run 没有正式承接 suggested overlay trace。
4. RRF 禁止跨 authority bucket 的规则写得太像人话，不够机器可查。
5. project_non_borrow_scope 的 universal-ban 禁止没有在主线中钉死。
```

这些缺口已补齐。

## Mainline Files Updated

```text
SOURCE_INTAKE.md
templates/source-record.md
templates/video-source.md
templates/candidate-distillation.md
templates/review-candidate.md
templates/query-run.md
templates/project-overlay.md
templates/feedback-event.md
```

Key merged design logic:

```text
processing_tier != authority
knowledge_status controls boundary status
retrieval_policy is a machine-filterable block, not a loose warning string
candidate cannot be action basis
suggested overlay is trace-only
confirmed overlay is active-project-only
archived overlay is excluded from default retrieval
feedback is append-only and cannot mutate truth
final action-facing support must anchor to raw/stable source material
RRF can fuse relevance only inside one authority bucket
```

## New / Updated Templates

New:

```text
templates/candidate-distillation.md
templates/project-overlay.md
```

Updated:

```text
templates/source-record.md
templates/video-source.md
templates/review-candidate.md
templates/query-run.md
templates/feedback-event.md
```

Important template fields now include:

```text
retrieval_policy.policy_kind
retrieval_policy.pack_allowed
retrieval_policy.action_basis_allowed
retrieval_policy.warning_code
candidate_not_action_basis
overlay_unconfirmed
overlay_not_authority
archived_overlay_excluded
feedback_not_truth
forbidden_truth_mutation_fields_absent
reviewed_note_mutation_allowed: false
source_reliability_mutation_allowed: false
rrf_scope: same_authority_bucket_only
```

## Sandbox / Audit Evidence

Sandbox package:

```text
outputs/review/source-intake-control-flow-sandbox-2026-06-06/
```

Key check files:

```text
checks/pressure-test-results.md
checks/pro-round2-strength-results.md
checks/mainline-merge-audit.md
```

Results:

```text
Original sandbox final rerun: 11/11
Pro round2 sandbox final rerun: 16/16
First mainline merge audit after manual merge: round1 10/11, round2 14/16
Final mainline merge audit after patch: round1 11/11, round2 16/16
```

The important recovery file is:

```text
outputs/review/source-intake-control-flow-sandbox-2026-06-06/checks/mainline-merge-audit.md
```

## Boundary Clarification

This does not mean the old Project Overlay lightweight sandbox was fully promoted.

The earlier handoff remains correct for the full object-model boundary:

```text
00_handoff/2026-06-06-project-overlay-lightweight-sandbox-closeout-handoff.md
```

Meaning:

```text
Full Project Lens / Project Overlay object model, stance taxonomy, snapshots,
closeout lifecycle, and Obsidian usage manual remain sandbox/use-layer.
```

What did enter mainline here is narrower:

```text
Source Intake may use project_overlay as a project-scoped sidecar record,
with candidate status, active-project-only retrieval, no action basis,
and v0.2.13 promotion gate for any action-facing use.
```

So the split is:

```text
full Project Overlay system: not promoted
minimal Source Intake sidecar boundary/template: promoted into intake operation
```

## Obsidian Sync

Synced to:

```text
H:\Obsidian\资料库
```

Latest sync check before this handoff:

```text
hash_match=30/30
```

This handoff and index update should also be synced after creation.

## Truth Layer / Git State

Truth layer not changed:

```text
wiki/claims
wiki/decisions
wiki/patterns
SCHEMA.md
IMPLEMENTATION_BLUEPRINT.md
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

No commit has been made.

Expected dirty/untracked surfaces include:

```text
SOURCE_INTAKE.md
templates/source-record.md
templates/video-source.md
templates/candidate-distillation.md
templates/review-candidate.md
templates/query-run.md
templates/project-overlay.md
templates/feedback-event.md
outputs/review/source-intake-control-flow-sandbox-2026-06-06/
00_handoff/2026-06-06-source-intake-control-flow-mainline-merge-handoff.md
wiki/indexes/knowledge-graph-index.md
```

There may also be older dirty/untracked files from previous work, including the
Project Overlay closeout handoff and audit-shell handoff. Do not `git add .`.

## Next Window Startup

For a new Codex window continuing Source Intake work:

```text
Read this handoff first.
Then read SOURCE_INTAKE.md.
Then read:
templates/candidate-distillation.md
templates/source-record.md
templates/video-source.md
templates/query-run.md
templates/project-overlay.md
templates/feedback-event.md
Then read:
outputs/review/source-intake-control-flow-sandbox-2026-06-06/checks/mainline-merge-audit.md
```

Do not reopen the “did we merge the two rounds?” question unless new evidence
appears. Current audited answer:

```text
Round1 design logic: merged.
Round2 design logic: merged.
Sandbox evidence: retained as diagnostic output.
Truth layer: unchanged.
```
