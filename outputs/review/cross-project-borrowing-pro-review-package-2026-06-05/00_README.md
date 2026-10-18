---
type: pro_review_package_readme
status: package-entry
created_at: 2026-06-05
project: verified-action-knowledge-system
package: cross-project-borrowing-pro-review-package-2026-06-05
truth_boundary: review package only; not reviewed knowledge; not architecture decision
---

# Cross-Project Borrowing Pro Review Package

## 这是什么

这是 VAKS / 资料库 的一个候选流程试点包。

我们正在测试一个新的外部资料蒸馏方式：

```text
Source Card
-> Candidate Pattern Bank
-> Project Borrowing Ledger
```

人话版：

```text
资料卡记录资料本身；
候选方法库记录可复用方法；
项目借鉴账本记录某个项目借不借、借到哪里、为什么。
```

## 为什么需要 Pro 复核

这个试点看起来能减少“每条资料都写适合 VAKS / 不适合 VAKS”的耦合，但它也可能带来新问题：

- 会不会变重？
- 会不会多建一层反而乱？
- Source Card 要不要写“可能路由到哪个项目”？
- Project Borrowing Ledger 会不会长得太像 ADR？
- Candidate Pattern Bank 会不会变成漂亮名词目录？
- 这套流程哪些部分能进主线规则，哪些必须留在 `outputs/review` 观察？

## 当前边界

本包里的内容全部是候选试点：

```text
not reviewed knowledge
not architecture decision
not action basis
not truth confidence
not reviewed relation
```

它现在只放在 `outputs/review`，没有合并主架构。

## Pro 重点看什么

请优先看：

1. `UPLOAD_TO_PRO_PROMPT.md`
2. `pilot/2026-06-05-cross-project-borrowing-pilot-implementation.md`
3. `pilot/2026-06-05-cross-project-borrowing-4-item-pilot-test.md`
4. `project_borrowing_ledgers/VAKS.md`
5. `candidate_pattern_bank/INDEX.md`

如果时间不够，不需要逐字读完 10 张 pattern 卡；可以先看 index 和 VAKS ledger。

