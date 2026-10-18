---
type: project_borrowing_ledger_index
status: pilot
created_at: 2026-06-05
truth_boundary: project fit ledger only; not ADR; not action basis
---

# Project Borrowing Ledgers

Project Borrowing Ledger 是项目级借鉴账本。它回答：

```text
这个项目看过哪些 candidate pattern？
借没借？
借到哪里？
为什么？
下一步需要过什么 gate？
```

它不是 source card，不复制外部资料内容。

它也不是 ADR，不直接形成架构决策。

## Disposition

```text
watch:
  先观察，暂不做实现。

prototype:
  值得做小原型，但还不是正式采用。

adapt:
  方向上适合本项目，准备在后续 review/decision 后吸收。

reject:
  当前项目明确不借。

superseded:
  被新的模式或项目判断替代。
```

`reviewed_at`、`review_note`、`reviewer` 是流程元数据，不和 disposition 混在一起。

## Ledgers

- [[VAKS]]

