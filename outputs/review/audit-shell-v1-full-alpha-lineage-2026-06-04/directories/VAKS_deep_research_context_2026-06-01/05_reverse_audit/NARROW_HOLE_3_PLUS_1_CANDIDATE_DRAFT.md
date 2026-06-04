---
status: candidate-only
created: 2026-06-01
scope:
  - alpha-lab-closeout
  - narrow-hole-candidate-draft
  - user-final-triage
main_vault_write: false
mainline_merge: false
schema_change: false
---

# 3+1 真窄洞候选草稿

本文档是沙盒内候选草稿，只用于用户最终拍板。

它不合并主线，不修改 `SCHEMA.md`，不修改 `SOURCE_INTAKE.md`，不下最终架构结论。

## 候选草稿

| 1. 对应主库现有边界 | 2. 一个具体失败案例 | 3. 一行候选措辞 |
|---|---|---|
| `context-memory/source 混淆 -> REVIEW_QUEUE`。主库已有相邻边界：`background_context` 不能计入 support，`context_pack_trace` 记录 used / ignored sources 和 activation role；但还没有直指“当前 source context、历史会话、memory、模型背景知识之间的来源混淆”。 | 回答声称“论文 A 支持 X”，但 X 实际来自历史会话记忆或模型背景知识；当前 source span 只是背景材料，并不支持 X。 | `REVIEW_QUEUE`: 若 point 可能来自 memory / prior context / model background，而不是当前 source span，标记 `origin_confusion_review_needed`；在 source span 支持目标 point 前，不得放入 `support_refs`。 |
| `转换证据锚点(表格/OCR/翻译/bbox) -> anti-pattern`。主库已有部分覆盖：`evidence_granularity` 包含 `table_or_code_anchor`，source anchor 可记录 quote / position；但 OCR、翻译、版面 bbox 这类转换风险没有被点名。 | OCR 把表格列错位，翻译漏掉限定条件，或 bbox 指向图注而不是数据区域，却被当成直接证据。 | `anti-pattern`: 转换证据只有能回到原始表格格、OCR 片段、翻译原文段落或 page / bbox 区域时，才可进入 support review；转换产物本身不能单独作为 evidence support。 |
| `动态数据 query-scope 身份 -> REVIEW_QUEUE`。主库已有相邻边界：source identity 和 temporal applicability 覆盖 URL、版本、时间范围；但没有明说 query / filter / subset / as-of / result scope 会构成不同证据身份。 | 同一数据 URL 在同一天被引用两次；一次 query 过滤 2024 行，另一次过滤 2025 行，却被当成同一份证据支撑 action basis。 | `REVIEW_QUEUE`: 动态数据证据缺少 `query/filter/subset/as_of/result_scope` 时，标记 `query_scope_identity_missing`；补齐前只能作为 provenance，不能支持 action basis。 |
| `oracle 类型 -> maintenance-manifest(轻)`。主库已覆盖 test / benchmark / fixture / LLM-judge 只能是 lint / diagnostic，不能产生 truth、mainline readiness 或 runtime readiness；但没有区分不同 oracle 类型的可靠性。 | 测试通过是因为 oracle 只是 snapshot 或 string match；它验证输出形状没变，但不验证底层 claim 为真或行动安全。 | `maintenance-manifest`: 重要 test / fixture 报告应记录 `oracle_type` 与 `claim_scope`；weak / indirect oracle 只能生成 diagnostic/lint，不能暗示 truth、mainline readiness 或 runtime readiness。 |

## 明确不纳入

以下候选不属于本次 3+1 草稿，因为主库已经有字段、规则或检查闭环：

- 同源独立性
- approval 完整性
- LLM 辅助污染

它们可以在执行中继续检查，但不应消耗本次收口的新 review 名额。
