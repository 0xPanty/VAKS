---
type: sandbox_readme
status: active_test_sandbox
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-mainline-integration-pressure-test
truth_boundary: sandbox only; not reviewed knowledge; not mainline architecture; not schema; not template; not action basis
---

# Project Lens Mainline Integration Sandbox

## 说人话

这个目录测试一个问题：

```text
如果未来把 Project Lens 并入 VAKS 主架构，它会不会污染主线、加重流程、制造假权威，或者让 agent 误判？
```

当前结论：

```text
Project Lens passed high-intensity sandbox testing as a candidate sidecar.
It is not committed or pushed.
It is not yet merged into main architecture docs.
```

## Files

```text
00_README.md
CANDIDATE_MAINLINE_PATCH.md
OBSIDIAN_SANDBOX_CHECK.md
OBSIDIAN_HIGH_INTENSITY_SYNC.md
PRESSURE_TEST_MATRIX.md
PRESSURE_TEST_REPORT.md
ISSUES_AND_PATCHES.md
REAL_CASE_TRIALS.md
COMPLETION_AUDIT.md
GROK_RECOMMENDATION_TRIAGE.md
THREE_LAYER_ARCHITECTURE_CANDIDATE.md
AGENT_EXPERIENCE_VALUE_REPORT.md
HIGH_INTENSITY_GAUNTLET.md
ANCHOR_AND_CHAIN_AUDIT.md
SNAPSHOT_TRIALS.md
snapshots/
```

## Hard Boundaries

This sandbox must not modify:

```text
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
SCHEMA.md
REVIEW_QUEUE.md
templates/
```

Obsidian test copies must stay under:

```text
H:\Obsidian\资料库\outputs\review\project-lens-mainline-sandbox-2026-06-05\
```

They must not write into Obsidian root architecture docs or ordinary notes.

## Pass Bar

The design only passes sandbox pressure if it proves all of these:

```text
1. Project Lens does not change truth authority.
2. Project Lens does not become ADR or action basis.
3. Source Card routing remains routing-only.
4. Candidate Pattern Bank stays high-threshold.
5. Sidecar overlay does not pollute generic knowledge points.
6. outcome_ref is separate from stance.
7. target_hint helps navigation but cannot imply a decision.
8. v0.2.13 triggers only at decision / promotion / action-basis time.
9. Obsidian sandbox is readable and isolated.
10. A future agent can recover the rules without guessing.
11. Grok-style platform expansions do not re-inflate the design before repeated use proves need.
12. Structured target hints help agent navigation without becoming code decisions.
13. Lens entries can trace back through `kp_ref` to candidate patterns and raw sources.
14. Snapshot refs can be attached without changing stance into landed/avoid.
15. Markdown/YAML automation risks are documented, especially repeated-field patching and line-bounded parsing.
```
