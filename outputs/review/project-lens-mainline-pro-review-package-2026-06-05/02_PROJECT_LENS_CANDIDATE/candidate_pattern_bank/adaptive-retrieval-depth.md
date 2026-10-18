---
type: candidate_pattern
status: active
pattern_id: adaptive-retrieval-depth
created_at: 2026-06-05
truth_boundary: candidate pattern only; not reviewed knowledge
source_family_ids:
  - sf-memory-retrieval
  - sf-rag-engineering
project_fit_refs:
  - outputs/review/project_borrowing_ledgers/VAKS.md
---

# Adaptive Retrieval Depth

## One-Line Pattern

不同问题不一定用同样检索深度；熟悉、明确的问题走快路径，模糊、长尾、证据不足的问题才启动更深的扩展检索。

## Problem Addressed

统一 Top-K 快但可能召回浅；统一深检索又慢、贵、噪声多。系统需要根据问题熟悉度、不确定性和预算切换检索深度。

## Mechanism

- 先做 probe retrieval。
- 用相似度、熵、分布、候选覆盖等作为不确定性代理。
- 快路径返回少量候选。
- 慢路径做聚类、扩展、多轮检索或 beam/fanout 控制。
- 预算和最大轮数显式限制。

## Applicability

- 个性化记忆检索。
- 长历史用户记忆。
- 大型知识库问答。
- VAKS future activation tier / context-pack budget。

## Non-Goals and Trade-Offs

- 不等于 similarity/entropy 是 truth。
- 不等于所有 query 都要 agentic retrieval。
- 不确定性代理依赖 embedding 校准。
- 快慢路径只是 activation 策略，不是 review。

## Derived From Sources

- `raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source.md`
- `raw/papers/2026-06-04-rf-mem-recollection-familiarity-source.md`
- `raw/repos/2026-06-04-come-context-memory-source.md`
- `raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source.md`

## Aliases or Near-Duplicates

- fast/slow retrieval
- familiarity/recollection retrieval
- uncertainty-guided activation
- budgeted context expansion

## Risk of Overreach

- 把检索深度策略写成认知真理。
- 对普通 query 增加复杂度。
- 用模型不确定性代理替代证据充分性检查。

## Project Fit Refs

- VAKS: `watch`; maybe useful for activation/context-pack budget.

