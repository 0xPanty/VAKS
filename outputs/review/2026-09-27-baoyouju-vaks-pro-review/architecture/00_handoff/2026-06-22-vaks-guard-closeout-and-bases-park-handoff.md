# VAKS Guard 收尾 & p2-18 Bases Park — Handoff (2026-06-22)

## 这轮做了什么

VAKS Guard 已正式落地为 VAKS 的只读工具层：

- `tools/vaks_guard.py` + `tools/tests/vaks_guard/`，read-only lazy gate，
  非服务 / 非 hook / 非 Obsidian 插件，不自动运行，不写库。
- commit `75d757af`：新增 VAKS Guard 工具层。
- commit `e5540997`：在 `AGENTS.md` 记录 Agent 按需调用约定。

## 20 个 sandbox slice 的处理

20 个 sandbox 中，**当前主线只收编 7 个 Guard 能力**：

- `body_hash`
- `support_boundary`
- `action_readiness`
- `feedback`
- `failure_matrix`
- `receipt`（检索 + 操作，含 P0-01 / P0-02 收据契约）
- `runtime_artifacts`

其余 slice **保持 sandbox / reference 状态，不自动并入主线**：

- P1-09 查询循环：待查询运行时存在后再议。
- P1-11 语义锚点：待真实 evidence / review 记录与 anchor 形态成熟后再议。
- P1.5-12 到 P1.5-16（RAG / MCP / 解析器 / mdvs / MISA）：运行时边界，parked。
- p2-17 / p2-19 / p2-20（use-surface / 产品筛选 / workflow）：未来产品阶段参考。

这些保留未来价值，但当前不构成主线能力，也不自动合并。

## p2-18 Bases cockpit — PARK_FOR_LATER

p2-18 的两个 Bases 视图设计合理、属 display-only、契合现有 `wiki/bases/` 线，
但当前零真实数据源，故 `PARK_FOR_LATER`（非 `REJECT`）：

- `review-candidates.base`：依赖真实 `review_candidate` 记录（现存真实记录 0）。
- `feedback-events.base`：依赖真实 `feedback_event` 记录（现存真实记录 0）。

现存匹配项来自 VAKS Guard 测试 fixture，不是 vault 知识记录；
`REVIEW_QUEUE.md` / `FEEDBACK.md` 是散文台账，不是逐条结构化记录。

`operator-cockpit.base` / `context-packs.base` 数据更不成熟，继续排除。

### 解锁条件

满足后再轻量采纳，且仅新增 `wiki/bases/*.base`：

- `review-candidates.base`：真实 `review_candidate` 记录落到固定 wiki 文件夹，
  约 5 条以上，且带 `review_status` / `body_hash` / `missing_evidence` / `risk_flags`。
- `feedback-events.base`：真实 `feedback_event` 以独立 Markdown 存在，
  约 5 条以上，且带 `event_kind` / `target_ref` / `review_pressure_effect`。
- 采纳时照 `decisions.base` 套路，filter 按文件夹收口（防抓 fixture）。
  首版采纳应只新增 `wiki/bases/*.base`，不顺手改 `SCHEMA.md` /
  `FUSION_ARCHITECTURE_V0_2_DRAFT.md` / `README.md` / `templates/` / `tools/`。

## 边界

本 handoff 为收尾记录，非架构扩张。主架构、知识流、权威关系均未改变。

没有新增 `.base` 文件，没有修改 Obsidian vault，没有 sync，没有 push。
