# Task Plan

## Goal

按 Pro 的轻量化建议，在 `outputs/review` 沙盒里落地一版
`Project Overlay` 操作模式，并做全量沙盒测试。

成功标准不是把对象模型推主线，而是证明：

```text
小便签模式能保留维护功能
不污染 truth / ADR / action basis
不修改主线 schema / review queue / templates
非作者不容易误读
```

## Scope

Allowed:

- Create or update files under
  `outputs/review/project-overlay-lightweight-landing-test-2026-06-06/`.
- Copy this sandbox package to `H:\Obsidian\资料库\outputs\review\...`.
- Zip the sandbox package for Pro review.
- Run read-only scans and project tests.

Not allowed unless user explicitly widens scope:

- Edit real `ARCHITECTURE_PRINCIPLES.md`.
- Edit real `FUSION_ARCHITECTURE_V0_2_DRAFT.md`.
- Edit `SCHEMA.md`, `REVIEW_QUEUE.md`, or `templates/`.
- Commit, push, clean, delete, reset, or stage unrelated files.

## Phases

| Phase | Status | Evidence |
|---|---|---|
| Recover current state | complete | git status/log checked; old sandbox scanned |
| Write lightweight protocol | complete | `protocol/PROJECT_OVERLAY_ONE_PAGE_PROTOCOL.md` |
| Build project overlay samples | complete | `project_overlays/MISA.md`, `project_overlays/VAKS.md` |
| Convert snapshot idea to candidate notes | complete | `candidate_notes/experience`, `candidate_notes/boundary` |
| Run closeout drain sample | complete | `closeout/MISA-closeout-drain-note.md` |
| Run scans and anchor checks | complete | `checks/` |
| Run Misa deterministic tests | complete | `checks/misa-test-run.md` |
| Repeat full sandbox testing | complete | `checks/repeated-full-sandbox-test-2.md` |
| Completion audit | complete | `checks/completion-audit.md` |
| Sync to Obsidian and zip | in_progress | `checks/obsidian-sync.md`, `package/MANIFEST.md` |
| Final audit | complete | `FINAL_REPORT.md` |

## Pro Requirements To Land

1. Keep `project-scoped overlay note` as the only lightweight mode.
2. Keep `kp_ref`, optional `target_hint`, stance/outcome separation,
   closeout drain, archive/tombstone hygiene, and return to v0.2.13.
3. Stop advancing formal Project Lens naming, field contract, constant
   snapshots, lifecycle state machine, formal workspace directory, retrieval
   priority/preference mechanism, and schema/template/mainline expansion.
4. Use only `watch / partial / avoid / defer` as live stance words.
5. Do a 6-8 entry blind non-author style confusion check.

## Errors Encountered

| Error | Attempt | Resolution |
|---|---|---|
| Wrong skill path | Tried `.agents/skills/planning-with-files` | Read from `.codex/skills/planning-with-files` |
