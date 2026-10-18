---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
title: "semantica-agi/semantica 候选蒸馏"
source_ref: "raw/repos/2026-08-02-semantica-agi-semantica-source.md"
derived_from:
  - "raw/repos/2026-08-02-semantica-agi-semantica-source.md"
source_url: "https://github.com/semantica-agi/semantica"
checked_commit: "0d447560bc3c9a8dfa0bfb5e78d32dbe77416cd3"
reviewed_at: "2026-08-02"
review_scope: "architecture, authority boundaries, provenance, decisions, reasoning, temporal model, conflicts, MCP, persistence, CI, security, packaging"
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - architecture_comparison
  - authority_boundary_review
possible_project_refs:
  - verified-action-knowledge-system
source_annotation_refs:
  - ann-semantica-001-default-llm-extraction
  - ann-semantica-002-conflict-after-persistence
  - ann-semantica-003-declared-and-heuristic-causality
  - ann-semantica-004-decision-provenance-wiring-gap
  - ann-semantica-005-provenance-integrity-boundary
  - ann-semantica-006-rete-unconditional-matches
  - ann-semantica-007-ontology-validator-placeholder
  - ann-semantica-008-bitemporal-normalization
  - ann-semantica-009-agent-mcp-direct-write
  - ann-semantica-010-ci-build-only
point_anchor_refs: []
tags:
  - candidate
  - provisional
  - semantica
project_overlay_ref: "outputs/review/project_overlays/VAKS/VAKS-semantica-agi-semantica-2026-08-02.md"
architecture_review_ref: "wiki/summaries/2026-08-02-semantica-agi-semantica-architecture-review.md"
---

# Semantica 候选蒸馏

## 先说人话

Semantica 想把知识图谱、实体关系抽取、推理、溯源、时态、冲突处理、Agent 记忆、MCP 和可视化放进一个 Python 平台。

它最有价值的地方是：把许多“可信知识系统应该记录什么”做成了可读的代码形状，例如决策记录、推理链、双时态事实、来源记录和冲突对象。

它最大的问题是：这些形状还没有被统一成一条可靠的证据与权限链。部分自动抽取结果会直接进图，冲突检测发生在持久化之后，因果关系可由调用者声明或由时间邻近推断，MCP/REST 有直接写入口，而主 CI 并不运行 pytest。

因此本次结论是：

> 可以借它的记录结构和失败案例；不要把它直接接成 VAKS 的真理库、 reviewed relation 写入口或可写 Agent runtime。

## 本次边界

- 固定源码提交：0d447560bc3c9a8dfa0bfb5e78d32dbe77416cd3。
- 只做源码、配置、文档、测试目录和工作流的静态核查。
- 没有安装依赖、运行代码、测试、benchmark、MCP、REST、Explorer 或后端。
- README、FAQ、发布说明和性能数字只作为项目方陈述；代码与门禁不支持的地方单独标出。
- 本文件是 candidate comprehension，不创建 reviewed truth、reviewed relation、架构决策或 action basis。

## 它真正提供了什么

| 能力面 | 代码中的实际形态 | 当前判断 |
|---|---|---|
| 知识图谱构建 | 结构化输入或文本抽取进入实体、关系、GraphStore | 结构完整，但默认文本路径依赖 LLM，写入边界过松 |
| 决策记录 | 决策类别、场景、理由、结果、置信度、Actor、相关实体 | 值得借 envelope；本身不是证据审查 |
| 推理 | 基础 forward chaining、Datalog、Rete 外壳 | 前两者有真实逻辑；当前 Rete 的匹配/连接是无条件通过 |
| 溯源 | Entity、Activity、Agent、source/location/quote 等 schema | 词汇值得参考；导出、校验和 wiring 不完整，不能等同证据支持 |
| 时态 | valid time、recorded time、superseded 的 BiTemporalFact | 值得借字段；目前是 wrapper，不是完整历史真相层 |
| 冲突 | 检测器、策略、投票与来源信誉 | 可借冲突包；自动选赢家不适合 VAKS |
| 本体校验 | pySHACL 路径与 HermiT/Pellet 接口 | SHACL 可作结构 lint；部分 reasoner 路径仍是 placeholder |
| Agent / MCP | 记忆、实体、关系和决策的直接写工具 | 对 VAKS 是 authority risk；缺少审批和 operation receipt |
| 多后端 / Explorer | 多种图、向量、云和 UI 接口 | 覆盖面广，但依赖、持久化与接口漂移的维护面很大 |

## 十个候选点

### CP-S-01：结构化输入可重复，文本输入默认并不确定

GraphBuilder 的原始文本路径默认选择 LLM NER、LLM relation 和 LLM triplet。所谓 deterministic graph construction 只能较稳地描述已结构化输入与确定性 adapter，不能覆盖默认文本抽取链。

- 状态：candidate
- 对 VAKS：强化“抽取只是候选理解，不能直写 reviewed graph”的既有边界。
- 源码定位：ann-semantica-001-default-llm-extraction

### CP-S-02：冲突检测晚于图写入

构图流程先把实体和边持久化到 GraphStore，随后才做 conflict detection；resolve_conflicts 主要返回计数，未完成回滚或实体修订。

- 状态：candidate risk
- 对 VAKS：验证 Review / Consolidation 必须位于 reviewed relation 写入之前。
- 源码定位：ann-semantica-002-conflict-after-persistence

### CP-S-03：图关系不自动成为因果证据

ContextGraph 允许调用者直接写 CAUSED、INFLUENCED、PRECEDENT_FOR；另一条 trace 又把“共享实体且时间更早”当作 influence 候选。两者都缺少 source anchor、warrant 与反事实检查。

- 状态：candidate risk
- 对 VAKS：因果边必须进入 Evidence Packet / review，不能由路径、邻近或调用者标签直接成立。
- 源码定位：ann-semantica-003-declared-and-heuristic-causality

### CP-S-04：决策 envelope 有用，但 provenance wiring 不能直接信任

DecisionRecorder 的字段形状值得借；不过当前 provenance helper 调用的参数和方法与 ProvenanceManager API 不一致，异常只被记录日志。AgentContext 还把 source_documents 留为空列表。

- 状态：candidate pattern plus implementation risk
- 对 VAKS：借“决策输入/理由/结果/Actor/关联对象”，补上 evidence packet、reviewer、approval、operation receipt 和 outcome calibration。
- 源码定位：ann-semantica-004-decision-provenance-wiring-gap

### CP-S-05：provenance 是身份与活动记录，不是支持检查

schema 声明了 source_document、source_location、source_quote 与 confidence，但 PROV 导出只保留部分关系；完整性 checksum 也遗漏 location、quote、metadata、agent 等字段。

- 状态：candidate boundary
- 对 VAKS：与既有规则一致——URL/PROV 只能证明“从哪里来、怎么处理”，不能证明“是否支持具体 point”。
- 源码定位：ann-semantica-005-provenance-integrity-boundary

### CP-S-06：推理收据值得借，当前 Rete 不能当成熟实现

基础 Reasoner 会保留 premises、rule 与 conclusion，这个 receipt 形状有价值；ReteEngine 的 alpha matching 和 beta join 当前都无条件返回 true。

- 状态：candidate pattern plus fatal implementation gap
- 对 VAKS：若未来做推理实验，只借 premise-rule-conclusion trace，并保持输出 candidate-only。
- 源码定位：ann-semantica-006-rete-unconditional-matches

### CP-S-07：SHACL 可作 lint，不是 truth gate

pySHACL 路径有真实校验；HermiT/Pellet 的 consistency、satisfiability 与 constraint check 部分路径仍直接 pass/true。

- 状态：candidate pattern plus scope limit
- 对 VAKS：SHACL 只可检查结构和约束形状，不授予 reviewer、support、truth confidence 或 promotion。
- 源码定位：ann-semantica-007-ontology-validator-placeholder

### CP-S-08：valid / recorded / superseded 是有价值的最小时间模型

BiTemporalFact 明确区分事实适用时间、系统记录时间和 superseded 状态。这与 VAKS Temporal Applicability Check 高度契合。

- 状态：candidate pattern
- 对 VAKS：可借字段和解释层，但需要不可变历史、替代链和查询语义后才可实现。
- 源码定位：ann-semantica-008-bitemporal-normalization

### CP-S-09：Agent / MCP 直写会绕过审核边界

Agent memory 与 MCP 工具可以直接写 entity、relationship 和 decision，没有证据审查、权限分级、二次确认或 operation receipt。发布版与根目录两套 MCP 还存在 API、打包和持久化漂移。

- 状态：candidate authority risk
- 对 VAKS：只能隔离实验、只写 candidate、默认关闭 mutation；不能写 reviewed knowledge。
- 源码定位：ann-semantica-009-agent-mcp-direct-write

### CP-S-10：代码量和测试文件数量不等于发布门禁

固定提交下静态可见 243 个 tests 目录 Python 文件，其中 218 个以 test_ 命名，约 4,119 个 test definition；但主 CI 只构建前端和 wheel，没有运行 pytest，发布工作流也没有测试门禁。benchmark workflow 引用的 benchmarks 目录在当前树中不存在。

- 状态：candidate maturity risk
- 对 VAKS：Production/Stable、1,000+ tests、100% coverage 与性能倍数不能作为采用依据。
- 源码定位：ann-semantica-010-ci-build-only

## 宣称与实现的关键落差

| 项目方叙述 | 固定提交中的静态证据 | 蒸馏判断 |
|---|---|---|
| deterministic graph construction | 文本路径默认 LLM 抽取 | 仅对受控结构化路径成立 |
| regulator-ready provenance | provenance 字段、导出、checksum 与决策 wiring 不闭环 | 有 vocabulary，不等于审计可接受 |
| causal reasoning / decision trace | 调用者声明关系，另有时间邻近启发式 | 只能当候选线索，不是因果证据 |
| production/stable | 0.x、主 CI 无 pytest、接口与版本漂移 | 更接近活跃实验平台 |
| permanent agent memory / MCP | 默认内存图、mutation 无自动 save，load API 还存在错配 | 默认不能视为可靠持久化 |
| 多后端统一 | 大量 extras、部分 mock、缺少 live matrix | 接口思想可参考，兼容性需独立验证 |

## 候选复用方向（正式项目范围以 Project Overlay 为准）

1. 决策记录 envelope：intent/scenario、reasoning、outcome、actor、related entities；VAKS 额外要求 evidence、review、approval、receipt 和 outcome calibration。
2. 推理收据：premises -> rule -> conclusion；结论保持 candidate，不能自动晋升。
3. 双时态字段：valid_at / valid_until、recorded_at、superseded_by。
4. SHACL 结构 lint：只报告 schema/shape 问题。
5. 冲突 packet：保留 competing values、来源、时间、范围和 resolver trace，交给 review queue；不自动选真值。
6. 后端投影 receipt：写了哪些字段、丢了哪些字段、失败项、round-trip 结果和 adapter version。
7. 只读查询防护：allowlist、timeout、并发限制、结果截断；如果未来开放诊断接口可参考。

这些都应先进入候选设计讨论，不新建正式 lane、schema、pattern 或 decision。

## 候选风险边界（正式项目范围以 Project Overlay 为准）

- Semantica 作为 VAKS Markdown source of truth 或 reviewed KG。
- LLM/启发式抽取结果直接创建 reviewed entity/relation。
- 把 provenance、confidence、vote、recency、source credibility 或 graph rank 当作 truth confidence。
- 把共享实体、时间先后、路径或相似度当作因果证据。
- 当前 Rete/OntologyValidator placeholder 路径。
- 可写 MCP/REST 直接连正式资料库。
- pickle / 未验证 tar restore、不透明 random/hash fallback。
- 全量依赖与全平台 fork；维护面与当前需求不匹配。

## 与本地架构的碰撞结果

| Semantica candidate | 本地既有边界 | 输出 |
|---|---|---|
| 自动文本构图 | Candidate Comprehension 不直写 reviewed knowledge | reinforces existing boundary |
| 冲突检测与 voting | Point Collision 是 review input，不是真理机 | scope mismatch for auto resolution |
| provenance | Source provenance 不等于 Evidence Support Check | confirms existing distinction |
| BiTemporalFact | Temporal Applicability Check | candidate implementation shape |
| Agent/MCP memory writes | Agent memory quarantine | authority risk / reject direct write |
| decision record | Decision / Action + Use Ledger | candidate envelope, missing gates |
| inference trace | Evidence Packet / review | candidate receipt, no promotion |
| multi-backend graph | Markdown source of truth + optional projections | adapter-only, receipt required |

没有发现需要立即修改当前架构主脊的新增原则。它主要提供实现形状、反例和未来实验清单。

## 候选路由判断

- Direct use：候选评估不支持直接采用；最终项目判断见 library review 与 Project Overlay。
- Fork：候选评估未发现整库 fork 的充分理由。
- Design-only：可路由到选择性设计参考。
- 当前支线价值：高，尤其是 authority、provenance、temporal、projection 和 maturity 的负面案例。
- 全貌架构价值：中高，因覆盖面广，但可信边界未闭环。
- 复用价值：3/5。
- 集成适配：2/5。
- 证据强度：4/5（对固定源码的静态判断）；运行时成熟度未验证。
- 实现成本：5/5（若整合整个平台）。
- 可逆性：5/5（本次仅保存候选记录和源码快照）。

## 重新打开条件

只有出现以下具体任务时再回看代码：

- VAKS 要做 graph projection round-trip receipt。
- 要实现 Temporal Applicability 的最小字段与 supersession 查询。
- 要试验 premise-rule-conclusion inference receipt。
- 要设计 read-only MCP 权限层或 mutation approval/receipt。
- 要隔离验证 Semantica 某一个 adapter，而不是引入全平台。

重新打开时必须重新固定 commit，并执行真实的 resolver、pytest、持久化重启、MCP contract、后端 round-trip 和安全验证。
