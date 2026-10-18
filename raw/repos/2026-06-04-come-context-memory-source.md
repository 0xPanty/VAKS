---
type: source
status: source-captured
title: "CoMe ContextMemory"
source_id: 2026-06-04-come-context-memory-source
source_uri: https://github.com/Ricoz217/CoMe_context_memory
source_url: https://github.com/Ricoz217/CoMe_context_memory
source_type: repository
author: RicoZ
publisher: GitHub
published_at:
updated_at: 2026-05-23
captured_at: 2026-06-04
captured_by: Codex
version_or_commit: 726a5abcaaab3cc8477a356443590693caa2f44e
release_or_tag: v0.3.3
commit_time: "2026-05-23 12:37:30 +0800"
source_status: active
license: MIT
raw_location: raw/repos/2026-06-04-come-context-memory-source.md
snapshot_location: raw/repos/_snapshots/CoMe_context_memory-726a5abcaaab3cc8477a356443590693caa2f44e.zip
processing_mode: immediate
processing_level: heavy
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - context-memory
  - agent-memory
  - activation
  - retrieval
  - bucket-tree
  - local-rerank
  - json-rpc
projects:
  - verified-action-knowledge-system
source_family:
  - memory-system
  - retrieval-alternative
  - agent-context
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - target: "[[Activation Tier]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Bucket-tree memory and budgeted recursive query may refine activation depth, but not truth confidence."
  - target: "[[Agent memory quarantine]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Alias-only LLM payload and audit logs are useful as a quarantine pattern for agent-facing memory tools."
tags:
  - come-context-memory
  - bucket-tree-memory
  - activation
  - candidate-only
---

# CoMe ContextMemory Source Record

## 为什么收录

CoMe ContextMemory 是一个面向 LLM 的本地记忆库。README 将它描述为“不依赖向量数据库”的记忆方案：通过 bucket tree 组织记忆，并用 `query / optimize / compress / split` 维护与检索。

它和当前 VAKS 的关系不是 truth layer，而是：

```text
memory structure
-> candidate retrieval
-> activation / context-pack preparation
-> optional workbench or agent tool reference
```

它不能直接证明任何知识点为真，也不能创建 reviewed relation 或 action basis。

## 来源信息

- Repository: `Ricoz217/CoMe_context_memory`
- URL: https://github.com/Ricoz217/CoMe_context_memory
- Checked commit: `726a5abcaaab3cc8477a356443590693caa2f44e`
- Commit time: `2026-05-23 12:37:30 +0800`
- Commit subject: `更新 v0.3.3`
- Tag / version: `v0.3.3`, `pyproject.toml` version `0.3.3`
- License: MIT
- GitHub public metadata at capture: public repo, Python, 74 commits, 6 stars, latest release `0.3.3` on 2026-05-23
- Snapshot: `raw/repos/_snapshots/CoMe_context_memory-726a5abcaaab3cc8477a356443590693caa2f44e.zip`

## 文件 / 代码锚点

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:5-6` | 项目自称基于 LLM context 的记忆库，不依赖向量数据库，使用 bucket tree 和 `query / optimize / compress / split` | 它的主张是 context-first memory，而不是 vector-first RAG | README 主张不是效果证明 |
| `README.md:146-159` | 多进程写入不安全、无回退接口、JSON-RPC 无鉴权、时间管理不足 | 这些是直接风险边界 | 不能直接接入 VAKS runtime |
| `docs/project_introduction.md:9-20` | bucket 作为上下文容器；记忆事件流 append-only；通过重建/压缩得到最新视图 | append-only event + latest view 可作为 activation/source-history 候选模式 | append-only 不等于 reviewed provenance |
| `docs/project_introduction.md:56-81` | query = BFS 本地路由增强 + LLM + rerank；模式为 auto/semantic/hybrid | 检索链路是预算化 activation，不是一次性 truth retrieval | query score 不能变成 truth confidence |
| `docs/project_introduction.md:134-172` | 单写者安全模型、读并发、写串行、RPC 默认本地无鉴权 | 适合本地工具参考，不适合开放服务 | agent access 需要单独网关和权限 |
| `docs/python_api_guide.md:144-185` | Query 参数区分 traversal 和 scoring；建议多轮从广召回到精确验证 | 与 RF-Mem 的快慢/深浅检索路由相邻 | 只控制召回预算和噪声，不控制可信度 |
| `docs/python_api_guide.md:212-288` | `advance_query` 是全景查询，超窗时分片汇总，不落持久化 | 可作为“全景候选阅读”参考 | 全景总结仍是 candidate comprehension |
| `src/context_memory/memory/models.py:8-17` | relation 类型包括 supports、corroborates、contradicts、supersedes 等 | 关系 schema 有启发，但由 LLM/系统产生 | 不能借这些关系名作为 reviewed relation |
| `src/context_memory/memory/models.py:120-139` | `MemoryRecord` 有 title、summary、content、weight、event、gray、relations、evidence_ref、expires_at、source_hash、confidence_type | 字段覆盖 activation、lifecycle、source attachment | `confidence_type` 不是 VAKS truth confidence |
| `src/context_memory/memory/storage.py:17-43` | 文件系统布局：memories/evidence/buckets/snapshots/index/events/cache/tree/migration | 本地文件系统加索引的工作台结构 | VAKS Markdown source-of-truth 不应让 runtime index 反客为主 |
| `src/context_memory/memory/storage.py:57-123` | 初始化 events、alias audit、state、meta、cache、bucket tree | 有用的 operational ledger 设计 | ledger 是诊断，不是 evidence support |
| `src/context_memory/memory/services/query_service.py:54-127` | query 参数含 top_k、max_depth、global_recall_*、time budget、branch_expand_k | 预算化 activation depth | 预算不是 truth gate |
| `src/context_memory/memory/services/query_service.py:219-343` | BM25 index、本地分数、alias key hints、LLM query、本地融合 | hybrid local+LLM retrieval | LLM 选择和 BM25 rank 都不是 evidence review |
| `src/context_memory/memory/services/query_service.py:530-716` | 命中 bucket node 后递归子桶，并合并 parent/child 分数 | 显式层级递归检索 | 适合 context-pack preparation |
| `src/context_memory/memory/rerank.py:29-60` | BM25Lite 实现 | 轻量本地检索参考 | 与 vector/RAG 一样只负责 candidate recall |
| `src/context_memory/memory/rerank.py:184-233` | Louvain 或 balanced split 分组 | 自动分桶/分组可辅助维护 | 自动分组不能创建 reviewed categories |
| `src/context_memory/memory/services/ingest_service.py:14-88` | 文件入库支持 text/image，文本读入后调用 `add_memory`，图片走 image extraction | intake workbench 参考 | 当前不支持 pdf/docx |
| `src/context_memory/memory/services/optimize_service.py:28-176` | optimize 收集候选，构造 payload，LLM 产出计划，并检查 coverage/duplicates/pressure | LLM 计划后有本地 guardrails | 可借“计划覆盖率检查”，不能借“模型计划即可信” |
| `src/context_memory/memory/services/maintenance_service.py:13-31` | `cleanup_expired` 将过期记录设为 gray | 过期/灰化适合 activation cooling | 不等于删除真理或降低 truth confidence |
| `src/context_memory/memory/engine.py:3199-3339` | `add_memory` 做 clean、ingest、evidence copy、append context event、auto manage | 完整 write pipeline 有工程启发 | clean/ingest 都是 candidate processing |
| `src/context_memory/memory/engine.py:4689-4743` | `query` 暴露 with_evidence/cache/max_depth/global recall 等参数 | 可控 query surface | `with_evidence` 是附带原文，不是 VAKS evidence support check |
| `src/context_memory/memory/engine.py:6112-6219` | auto manage、compress/split threshold、forgetting penalty、query_hits 抵消 | 可参考 cooling/reactivation | 自动遗忘不能改 reviewed truth |
| `src/context_memory/rpc_server.py:61-78` | RPC config 默认 base_dir/preset/mock/no_clean/no_forgetting/auto_manage 等 | 本地工具服务形态 | 无鉴权，不能暴露为 agent authority |
| `src/context_memory/rpc_server.py:132-190` | JSON-RPC 映射 add/get/update/query/compress/cleanup 等写操作 | 工具 API 完整 | 如果接入 agent，必须 path-scope + auth + quarantine |
| `tests/test_query_mode_semantics.py:12-68` | mock test 覆盖 literal mode rejected、auto route、char ngram | 有部分语义测试 | 本机未安装 pytest，未执行 |
| `tests/test_advance_query_mock.py:22-80` | mock test 覆盖 `advance_query` single-shot 与 overflow best-effort dispatch | 有全景查询测试入口 | 不等于生产可用验证 |

## 人话总结

CoMe 的有用点不是“它替代 RAG”，而是它把记忆库当成一棵可维护的上下文树：

```text
bucket = 局部上下文容器
memory = append-only 事件和最新视图
query = BFS 预算召回 + LLM 判断 + 本地重排 + 子桶递归
maintenance = compress / split / optimize / gray / expiry
```

这对 VAKS 有启发，因为 VAKS 已经把 retrieval 和 activation 放在 truth 外面。CoMe 提醒我们：activation 不一定只能是 vector top-k，也可以是可解释的 bucket tree + budgeted traversal + local rerank。

## Candidate Points

1. `bucket_tree_as_activation_structure`

候选结论：VAKS 可把某些热/暖上下文组织成显式 scope bucket，而不是只依赖 tag、folder、vector 或最近编辑。

边界：bucket 只是 activation structure，不是 reviewed relation。

2. `budgeted_traversal_query`

候选结论：query 可暴露少量预算参数，例如 depth、branch width、time budget，用来平衡漏召回和噪声。

边界：预算参数只影响 context-pack preparation，不影响 truth confidence。

3. `alias_only_llm_payload`

候选结论：对 agent-facing memory tool，可用 alias map 避免 LLM 直接操纵真实 key/path，并记录 alias audit。

边界：alias audit 是 tool-safety trace，不是 evidence support。

4. `append_only_event_with_latest_view`

候选结论：外部 agent memory 或临时 workbench 可以保留 append-only event，再生成 latest view，避免覆盖历史。

边界：append-only history 只是 provenance/operation trace，不能绕过 review。

5. `gray_expiry_cooling`

候选结论：灰化、过期、query_hits、idle-days 这类机制可启发 Cooling / Reactivation 和 feedback-driven activation。

边界：冷却和灰化不等于知识为假，不直接改变 truth。

6. `model_plan_plus_local_guardrails`

候选结论：让 LLM 提 restructure/optimize plan，但由本地 coverage、duplicate、pressure checks 拒绝坏计划，是有价值的维护模式。

边界：这些 checks 是 maintenance lint，不是 truth gate。

## VAKS 归位

适合放在：

```text
Activation Tier
Context Pack preparation
Retrieval / cache
Agent memory quarantine
Workbench / maintenance diagnostics
Cooling / Reactivation
```

不适合放在：

```text
Reviewed Knowledge
Evidence Support Check
Evidence Sufficiency Gate
Reviewed Relations
Truth confidence
Action basis
```

## 可借鉴

- Scope bucket / bucket tree 作为 activation structure。
- BFS + local rank + LLM + local rerank 的检索链路分层。
- Query 参数区分 traversal 与 scoring。
- `advance_query` 这种“全景候选阅读”和普通 query 分开。
- Alias-only payload + alias audit。
- LLM 维护计划后加本地 coverage / duplicate / pressure guard。
- Gray / expiry / recall history 作为 cooling/reactivation 的参考。

## 不能借鉴

- 不借“Context 本身就是向量数据库”这种强话术。
- 不借“RAG 没有全局观，所以 ContextMemory 更准”作为架构事实。
- 不把 LLM 生成的 relation 当 reviewed relation。
- 不把 query result、BM25 score、bucket score、query_hits 或 cache hit 当 truth confidence。
- 不直接接 JSON-RPC 到 agent 写权限。
- 不把自动遗忘、灰化、过期当作 truth 变化。
- 不采用无回退批量入库作为 VAKS source intake。

## 风险和不确定

- README 明确说同一记忆库多进程/多实例写入不安全。
- JSON-RPC 默认无鉴权，需要外部网关。
- 批量入库没有直接回退接口，只能按结果手动删除新增记忆。
- 暂无完整时间管理；时间要素需要显式写进记忆，query 也不会自动传时间。
- 暂不支持 pdf/docx，这对 VAKS 普通资料 intake 不够。
- 当前 GitHub 规模较小；它是有价值候选，不是成熟基础设施证明。
- 本机没有安装 pytest，未执行测试；只做了源码和文档 review。

## 与 RF-Mem / MemGAS 的关系

```text
RF-Mem:
  online retrieval depth routing based on familiarity/uncertainty

MemGAS:
  memory structure / multi-granularity association candidate

CoMe ContextMemory:
  explicit bucket-tree context memory with budgeted traversal and maintenance
```

三者可互补，但都必须停留在 activation / retrieval / context-pack preparation，不能跨到 reviewed knowledge。

## 融合判断

```text
Direct use: no
Fork: no
Design-only: yes
Watch: yes
Reject: no
Current branch value: medium-high for activation / agent memory quarantine
Whole architecture value: medium for retrieval/cache/workbench/cooling
Risk: high if treated as truth or exposed as agent write runtime
Next action: add to Direction Review candidate set; no main architecture change now
```

## 当前处理等级

```text
heavy source record
candidate-only
no promotion
no reviewed relation
no action basis
```

升级条件：

- 用户要求把 memory/activation 实验扩成 local sandbox。
- 后续 Direction Review 发现 RF-Mem / MemGAS / CoMe 等多个来源反复指向同一最小设计。
- 先写清楚 agent memory quarantine、path-scope、no truth mutation、rollback ledger，再考虑任何工具接入。

## 下一步

```text
保留为候选库。
不改主架构。
进入 Direction Review 的 activation / memory-structure / agent-memory quarantine 分组。
```
