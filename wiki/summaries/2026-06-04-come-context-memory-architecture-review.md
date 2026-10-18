---
type: library_review
status: draft
library_name: "CoMe ContextMemory"
repo_url: https://github.com/Ricoz217/CoMe_context_memory
source_url: https://github.com/Ricoz217/CoMe_context_memory
checked_commit: 726a5abcaaab3cc8477a356443590693caa2f44e
commit_time: "2026-05-23 12:37:30 +0800"
source_status: active
reviewed_at: 2026-06-04
domain: context-memory
related_projects:
  - verified-action-knowledge-system
current_branch: external-source-candidate-intake
extracted_patterns:
  - bucket_tree_as_activation_structure
  - budgeted_traversal_query
  - alias_only_llm_payload
  - append_only_event_with_latest_view
  - gray_expiry_cooling
  - model_plan_plus_local_guardrails
fusion_decision: watch
confidence: medium
evidence_count: 18
cross_validated_with:
  - RF-Mem
  - MemGAS
  - GraphRAG
  - RKA
negative_evidence:
  - no-auth JSON-RPC
  - multi-writer unsafe
  - no direct rollback for batch ingest
  - incomplete time management
extension_potential: medium
relations: []
---

# 库分析：CoMe ContextMemory

## 它解决什么问题

CoMe 解决的是“长期记忆怎么在 LLM 上下文里被组织、维护、递归检索”的问题。它不走典型 vector DB first 路线，而是把 memory 放进 bucket tree，通过本地检索、LLM 判断、本地重排、递归子桶来做 candidate recall。

对 VAKS 来说，它解决的不是“什么是真的”，而是：

```text
当前 query 需要激活哪一片上下文？
上下文太大时如何压缩、分桶、优化？
Agent 面对 memory tool 时如何减少真实 key/path 暴露？
```

## 核心设计

```text
Memory record:
  title / summary / content / relations / evidence_ref / expires_at / weight / gray

Bucket tree:
  ROOT -> bucket -> bucket / memory

Query:
  global BFS recall
  local BM25 + char n-gram scores
  alias-only key hints to LLM
  LLM returns answer + matches
  local rerank and merge
  recursive child bucket query

Maintenance:
  clean / ingest
  compress
  split
  optimize
  gray
  expiry cleanup
  forgetting penalty
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:5-6` | bucket tree memory, no vector DB requirement | Context-first memory claim | README claim is not proof |
| `README.md:146-159` | multi-process unsafe, no rollback, no-auth JSON-RPC, weak time handling | direct operational risks | no direct runtime adoption |
| `docs/project_introduction.md:9-20` | append-only event memory and latest view | useful for reversible memory history | not reviewed truth |
| `docs/project_introduction.md:56-81` | BFS -> LLM -> rerank query path | activation pipeline | not evidence review |
| `docs/python_api_guide.md:144-185` | traversal/scoring distinction and multi-round query strategy | query budget knobs | not confidence knobs |
| `docs/python_api_guide.md:212-288` | `advance_query` for full-view review, non-persistent | candidate context reading | summary is not knowledge |
| `src/context_memory/memory/models.py:8-17` | relation categories | schema inspiration | LLM relations are not reviewed relations |
| `src/context_memory/memory/models.py:120-139` | `MemoryRecord` lifecycle/source fields | activation metadata | `confidence_type` is not VAKS truth confidence |
| `src/context_memory/memory/storage.py:17-43` | local FS layout and ledgers | operational structure | index/cache not source of truth |
| `src/context_memory/memory/services/query_service.py:54-127` | budgeted query parameters | adaptive activation depth | no truth effect |
| `src/context_memory/memory/services/query_service.py:219-343` | BM25, alias hints, LLM, local merge | hybrid retrieval | retrieval only |
| `src/context_memory/memory/services/query_service.py:530-716` | recursive bucket query | scoped traversal | context prep only |
| `src/context_memory/memory/rerank.py:29-60` | BM25Lite | local retrieval fallback | candidate recall |
| `src/context_memory/memory/rerank.py:184-233` | Louvain or balanced split groups | maintenance grouping | not reviewed taxonomy |
| `src/context_memory/memory/services/optimize_service.py:28-176` | LLM plan plus coverage/duplicate/pressure checks | good maintenance guardrail | guardrail, not truth gate |
| `src/context_memory/memory/services/maintenance_service.py:13-31` | expiry sets records gray | cooling/reactivation reference | not truth mutation |
| `src/context_memory/memory/engine.py:3199-3339` | clean/ingest/evidence copy/append event/auto manage | full write pipeline reference | candidate processing |
| `src/context_memory/rpc_server.py:132-190` | JSON-RPC write/query methods | tool surface reference | needs auth/path-scope/quarantine |

## 当前支线价值

当前支线：

```text
external source candidate accumulation before Direction Review
```

它对当前支线：

```text
refines
```

具体价值：

- 给 RF-Mem 之后的 activation-depth 讨论增加一个工程侧样本：不是只问“该快检索还是慢检索”，还问“记忆结构如何被显式维护”。
- 给 agent memory quarantine 增加一个候选模式：alias-only payload 和 alias audit。
- 给 VAKS workbench 增加一个候选维护模式：LLM 提计划，本地 coverage/duplicate/pressure 拦截。

风险：

- 很容易被误读成“我们应该直接做自己的记忆 runtime”。
- 很容易把 LLM-generated relation 当成 reviewed relation。
- JSON-RPC 无鉴权、多写者不安全、批量入库无直接回退，都不适合直接给 agent 写权限。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | raw/wiki/index/log 思路有相邻性，但 CoMe 是 runtime，不是 Markdown-first vault | no direct |
| Dusk workbench | bucket tree 和 stats 可启发 operator workbench | adapt later |
| source ingest | text/image ingest 有参考，pdf/docx 缺失 | weak |
| review queue | 没有 evidence-aware review queue | no |
| schema / reviewed knowledge | relation labels丰富，但来源是 LLM/runtime | no direct |
| memory / dev context | 最强价值：bucket tree + context view + full-view query | watch/adapt |
| feedback | query_hits / forgetting penalty 可启发 activation feedback | adapt cautiously |
| retrieval / cache | BM25、char n-gram、BFS、rerank、cache 有参考 | adapt |
| API / MCP / agent access | JSON-RPC surface 有参考，但无鉴权 | risk_of |
| viewer / workbench | 暂无 GUI | no |
| publishing | 无明显价值 | no |
| risk / anti-pattern | no-auth RPC、multi-writer unsafe、no rollback 是明确反面锚点 | adopt as risk note |

## 值得提炼的模式

1. `bucket_tree_as_activation_structure`

用 bucket tree 管 activation scope，而不是让 vector/top-k 独占“召回”的想象。

2. `budgeted_traversal_query`

把 traversal budget 与 scoring mode 分开。VAKS 以后若做查询工具，也应区分“看多远”和“怎么算相关”。

3. `alias_only_llm_payload`

LLM 不直接拿真实 key/path，而是拿 alias，并保留审计。这个适合未来 agent memory tool。

4. `full_view_query_separate_from_normal_query`

普通 query 轻；全景 query 单独入口、可分片、可审计。这和 VAKS 的“ordinary query stays light, promotion/action basis gets strict”方向一致。

5. `maintenance_plan_guarded_by_local_checks`

LLM 可提出结构调整，但本地规则必须检查覆盖率、重复、压力和失败边界。

## 标签与量化

- domain: context-memory / agent-memory
- problem: long-memory organization and retrieval
- pattern: bucket-tree activation, budgeted recursive retrieval
- maturity: emerging
- complexity: high
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 4
- integration_fit: 3
- evidence_strength: 3
- reversibility: 3

这些数字只表示候选设计压力，不表示 truth confidence。

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Bucket tree can structure activation | Activation Tier is not truth tier | candidate_relation | Should VAKS support explicit scope buckets for hot/warm context? |
| Query should expose traversal budget separately from scoring | Retrieval is activation/context-pack prep only | candidate_relation | What is the minimal query budget surface that does not burden ordinary query? |
| Alias-only LLM payload protects real identifiers | Agent memory quarantine forbids direct reviewed truth writes | candidate_relation | Should future agent memory tools require alias/path indirection? |
| Gray/expiry/forgetting can cool memory | Feedback changes activation/usefulness/scope fit, not truth | candidate_relation | How to ensure cooling never becomes truth mutation? |
| LLM relation extraction can organize memory | Reviewed relations require evidence-aware review | risk_of | How to prevent extracted relations from being displayed as reviewed? |

## Support / Challenge Review

What supports it:

- README, docs, and code all align on bucket tree, query, compress/split/optimize, local rerank, JSON-RPC.
- Code has explicit BM25Lite, recursive query, alias audit, stats, maintenance, and tests for query mode semantics.

What challenges it:

- Public scale is small.
- Runtime not validated in this session.
- Tests were not executed because local Python lacks `pytest`.
- Project docs state no-auth RPC, no multi-writer safety, no direct rollback, incomplete time management.

Challenge severity:

```text
major for direct adoption
minor for design-only review
```

Action readiness:

```text
not_ready
```

## 关系边 / 关联强度

```yaml
relations:
  - target: "[[Activation Tier]]"
    type: refines
    relation_state: candidate
    strength: 3
    confidence: medium
    evidence:
      - "[[2026-06-04-come-context-memory-source]]"
    rationale: "CoMe gives a concrete bucket-tree and budgeted traversal pattern for activation, not truth."
    created: 2026-06-04
    last_verified: 2026-06-04
  - target: "[[Agent memory quarantine]]"
    type: refines
    relation_state: candidate
    strength: 3
    confidence: medium
    evidence:
      - "[[2026-06-04-come-context-memory-source]]"
    rationale: "Alias-only payload and audit logs are useful for future agent-facing memory boundaries."
    created: 2026-06-04
    last_verified: 2026-06-04
```

关系建议保持 candidate，不创建 reviewed edge。

## 直接判断

- Direct use: no
- Fork: no
- Design-only: yes
- Reject: no
- Current branch value: medium-high
- Whole architecture value: medium
- Risk: high if exposed as agent write runtime or truth layer
- Next action: keep for Direction Review, especially with RF-Mem / MemGAS / GraphRAG memory-retrieval cluster

## 后续行动

```text
不改主架构。
不接入 runtime。
不创建 reviewed relation。
保留 source record + architecture review summary。
等同类资料足够后进入 Direction Review。
```
