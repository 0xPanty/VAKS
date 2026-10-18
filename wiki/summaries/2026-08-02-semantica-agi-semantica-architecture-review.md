---
type: library_review
status: candidate
knowledge_status: candidate
library_name: "semantica-agi/semantica"
repo_url: "https://github.com/semantica-agi/semantica"
source_url: "https://github.com/semantica-agi/semantica/tree/0d447560bc3c9a8dfa0bfb5e78d32dbe77416cd3"
checked_commit: "0d447560bc3c9a8dfa0bfb5e78d32dbe77416cd3"
commit_time: "2026-08-01T20:52:55+05:30"
source_status: active
reviewed_at: "2026-08-02"
domain: "knowledge graph, provenance, reasoning, ontology, agent memory, MCP"
related_projects:
  - verified-action-knowledge-system
current_branch: "v0.2 architecture hardening / candidate-only reference review"
extracted_patterns:
  - decision_record_envelope
  - premise_rule_conclusion_receipt
  - bitemporal_applicability_fields
  - shacl_structural_lint
  - conflict_packet_not_auto_truth
  - backend_projection_receipt
fusion_decision: adapt
confidence: high
evidence_count: 20
cross_validated_with:
  - "FUSION_ARCHITECTURE_V0_2_DRAFT.md"
  - "ARCHITECTURE_PRINCIPLES.md"
  - "SCHEMA.md"
  - "REFERENCE_REVIEW_PROTOCOL.md"
  - "wiki/indexes/knowledge-graph-index.md"
negative_evidence:
  - "default LLM extraction can write before review"
  - "conflict detection follows persistence and resolution is incomplete"
  - "provenance fields, export, checksum, and decision wiring do not close"
  - "Rete and ontology reasoner paths contain unconditional placeholders"
  - "MCP and REST expose direct mutation without VAKS authority gates"
  - "main CI and release workflow do not run pytest"
extension_potential: "narrow, isolated record-shape and adapter experiments only"
relations: []
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
---

# 库分析：semantica-agi/semantica

## 它解决什么问题

Semantica 试图提供一套 Graph-Native AI 基础设施，把非结构化文本与结构化数据转成知识图谱，并在同一个项目中提供语义抽取、图存储、向量检索、本体、推理、溯源、双时态、冲突处理、决策追踪、Agent 记忆、MCP、REST 和 Explorer。

它解决的是“功能面如何装进一个 Python SDK”的问题；它尚未证明“这些能力如何形成一条可审计、可授权、可回滚的 verified action knowledge chain”。

## 核心设计

大体路径是：

1. 抽取或接收 entity / relationship / triplet。
2. GraphBuilder 做 entity resolution、图构造和可选 GraphStore 持久化。
3. ContextGraph 承载 event、decision、causal relation、state query 与 agent context。
4. ProvenanceManager 记录 entity/activity/agent lineage。
5. Reasoner、OntologyValidator、ConflictDetector 提供推理、约束和冲突接口。
6. MCP、REST/Explorer 和 AgentMemory 暴露读写入口。

这些模块在仓库中广泛存在，但常以 optional manager、adapter 或独立子系统耦合；“all modules unified”更接近产品方向，不是已经闭环的单一一致性协议。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| semantica/kg/graph_builder.py:231-285 | 文本构图默认 LLM NER / relation / triplet | 抽取策略应显式进入 receipt | 默认路径不确定，不能直写 reviewed graph |
| semantica/kg/graph_builder.py:582-693 | resolution -> construct -> persist -> conflict detect | pipeline 阶段顺序必须可审计 | 冲突检测晚于持久化 |
| semantica/kg/conflict_detector.py:1346-1417 | resolve_conflicts 返回统计，实体更新留作“real system” | conflict packet 与 resolution receipt 可分离 | 当前并非闭环 resolver |
| semantica/context/context_graph.py:2445-2589 | 决策节点记录 category/scenario/reasoning/outcome/confidence/actor/entities | decision envelope 值得借 | 调用者输入不是 evidence review |
| semantica/context/context_graph.py:2005-2043 | 直接写 CAUSED / INFLUENCED / PRECEDENT_FOR | 因果关系需要独立 warrant | 标签本身不构成因果证据 |
| semantica/context/context_graph.py:2829-2858 | 共享 entity 且时间更早被当作 influence | 可作候选线索 | path/time heuristic 不是 causality |
| semantica/context/decision_recorder.py:587-618 | decision provenance helper | wiring 应由 contract tests 固定 | 参数与 API 不一致，异常被日志化 |
| semantica/provenance/schemas.py:31-106 | source/location/quote/confidence 等字段 | 轻量 PROV vocabulary 可参考 | provenance 不等于 support |
| semantica/provenance/manager.py:804-862 | PROV 导出 entity/agent/activity/used/parent | 导出必须有 loss report | 未导出若干 source/evidence 字段 |
| semantica/provenance/integrity.py:27-71 | checksum 覆盖部分 provenance 字段 | checksum coverage 应显式 | 未覆盖 quote/location/metadata/agent 等 |
| semantica/reasoning/reasoner.py:238-269 | forward chaining 保留 premises/rule/conclusion | inference receipt 值得借 | 结论仍须 review |
| semantica/reasoning/rete_engine.py:72-104 | alpha match 与 beta join 无条件 true | placeholder 必须 fail closed | 当前不能作为可靠 Rete |
| semantica/ontology/ontology_validator.py:138-229 | pySHACL 真实校验路径 | 结构 lint 可选采用 | shape conformance 不是真理 |
| semantica/ontology/ontology_validator.py:271-327 | HermiT/Pellet/constraint 部分直接 pass/true | 能力声明需要 maturity flag | 当前是 placeholder |
| semantica/kg/temporal_model.py:28-65 | BiTemporalFact 区分 valid/recorded/superseded | 最小双时态字段值得借 | wrapper 不是完整历史存储 |
| semantica/agent_memory.py:369-395 | 内容直接写 vector/graph | agent write 要经过 quarantine | 无 promotion/review boundary |
| mcp/tools/graph.py:15-69 | MCP add_entity/add_relationship 直接 mutation | 写工具需要权限/审批/receipt | 不可直连正式 VAKS |
| semantica/mcp_server/__init__.py:56-72,538-550 | 发布版 MCP 使用内存图并直派发 handler | 默认状态与 mutation policy 必须显式 | persistence 与 approval 不可靠 |
| semantica/vector_store/vector_store.py:542-589 | save/load 使用 pickle | 不可信 artifact 必须安全解析 | pickle load 有代码执行风险 |
| .github/workflows/ci.yml:20-55 | 构建 Explorer 与 wheel | CI 证据应精确到实际 gate | 不运行 pytest |
| .github/workflows/release.yml:11-52 | tag 后 build/release/publish | 发布应依赖验证 receipt | 同样无测试门禁 |
| pyproject.toml:46-244 | 40+ 基础依赖与大量 extras/backends | adapter registry 思路可参考 | core 不轻，供应链和兼容面大 |

## 当前支线价值

当前支线：

```text
v0.2 architecture hardening / candidate-only reference review
```

它对当前支线：

```text
refines / risk_of / no new formal lane
```

具体价值：

- 给 Decision / Action 层提供 decision envelope 的实现参考。
- 给 Temporal Applicability Check 提供 valid/recorded/superseded 的最小字段参考。
- 给 Evidence Packet 提供 inference receipt 与 conflict packet 的候选形状。
- 以直接写图、因果启发式和 provenance 漏损，反向验证现有严格 promotion boundary。
- 为未来 graph projection adapter 提醒字段丢失、部分失败和 round-trip receipt。

风险：

- 宽功能面容易诱导整个平台引入，破坏当前轻量 spine。
- 文档成熟度与实际门禁存在落差。
- 自动抽取、图 rank、confidence、vote 和 provenance 容易被误读为 truth authority。
- MCP/REST/AgentMemory 直接 mutation 与 VAKS agent memory quarantine 冲突。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | 功能过宽，不适合替代轻量 capture-understand-review spine | no |
| Dusk workbench | Explorer 可作交互参考，但默认权限与持久化不足 | watch |
| source ingest | 多 extractor/adapter；失败 fallback 风险高 | design-only |
| review queue | conflict 对象可作输入；auto winner 不可采用 | adapt packet only |
| schema / reviewed knowledge | entity/relation/ontology 丰富，但缺 promotion authority | no direct adoption |
| memory / dev context | AgentMemory 易用但直写 | reject direct write |
| feedback | 与 Use Ledger / truth mutation 边界不闭环 | no |
| retrieval / cache | graph/vector/backend registry 有参考价值 | adapter-only |
| API / MCP / agent access | mutation、接口漂移、默认内存状态 | reject for formal path |
| viewer / workbench | 只读查询限时、限并发可借 | selective |
| publishing | wheel/release 自动化存在，验证 gate 不足 | no architecture value |
| risk / anti-pattern | 权限、因果、fallback、pickle、CI 是高价值反例 | yes, candidate only |

## 值得提炼的模式

### 1. Decision envelope plus VAKS gates

Semantica 的 decision record 字段足够解释“谁在什么场景下为什么做了什么”。VAKS 若吸收，只吸收字段形状，并补：verbatim intent、Evidence Packet、review state、approval identity、operation receipt、outcome calibration、supersession。

### 2. Inference receipt

premises、rule、conclusion 三元结构可让推理结果可检查。它必须记录 engine/version、failed premises、scope、source anchors；输出只进入 candidate/review queue。

### 3. Temporal normalization

valid time 与 recorded time 分离能够避免“现在记录的旧事实”与“现在才生效的事实”混淆。supersession 应保留旧记录，而不是覆盖。

### 4. Conflict packet

可保留 competing assertions、source identity、time/scope、resolver suggestion 和 unresolved state。vote/recency/credibility 只能产生 review pressure，不能改 truth confidence。

### 5. Projection receipt

Semantica 的 GraphStore 投影会压缩字段且对部分异常继续执行。未来任何 VAKS projection 都应输出 attempted/written/failed/lost_fields/adapter_version/round_trip_hash。

## 标签与量化

- domain: knowledge infrastructure
- problem: graph-native AI, provenance, decisions, reasoning, agent memory
- pattern: record envelopes plus broad adapters
- maturity: emerging / experimental despite Production/Stable classifier
- complexity: high
- problem_fit: 3/5
- reuse_value: 3/5
- implementation_cost: 5/5
- integration_fit: 2/5
- evidence_strength: 4/5 for static source findings
- reversibility: 5/5 for candidate-only intake

## 交叉验证

- 相似设计来源：W3C PROV、GraphRAG/LightRAG、Graphiti/Zep、Dung/TMS、Evidence Packet 与 Agent Memory Quarantine 的现有本地记录。
- 用户历史项目里的相似问题/影子：Source Annotation 不是 support；activation/rank 不是 truth；feedback 和 agent memory 不得直改 reviewed knowledge。
- 支持证据：固定 commit 源码、工作流、pyproject、测试树和本地 VAKS 架构文档。
- 反例或失败边界：unconditional matcher、placeholder validator、晚冲突检查、因果启发式、MCP 直写、无 pytest CI。
- 最小验证方式：若未来实验，单独固定 adapter，隔离临时数据，fail closed，跑 contract/round-trip/restart/security tests；不接正式 vault。

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| provenance model | provenance is not evidence support | candidate_relation | 是否只借 identity/activity vocabulary？ |
| default text-to-KG | candidate extraction cannot promote itself | reinforces boundary | 是否应把 fallback 状态做成强制 receipt？ |
| conflict resolver | Point Collision is review input | scope_mismatch | 如何保存冲突而不自动选赢家？ |
| BiTemporalFact | Temporal Applicability Check | candidate_relation | 哪些字段是最小实现？ |
| decision record | Decision / Action / Use Ledger | missing_evidence | evidence、approval、outcome 如何接入？ |
| inference trace | Evidence Packet | candidate_relation | 何时只需 receipt，何时必须人工 review？ |
| Agent/MCP mutation | Agent memory quarantine | contradiction_candidate | 是否全部 mutation 默认禁用？ |
| graph backend | Markdown source of truth | scope_mismatch | 如何证明 projection 不丢字段？ |

边界：相似不是支持；冲突不是自动推翻；本表不创建 reviewed relation。

## Support / Challenge Review

- What supports it：固定源码确实提供丰富 record shapes、真实 pySHACL 路径、基础 forward chaining、后端接口与大量测试代码。
- What challenges it：关键 authority 链不闭环，部分接口/validator/reasoner 是 placeholder，MCP/REST 默认可写，CI/发布无 pytest gate，持久化和版本存在漂移。
- Challenge severity：major；若直接作为 truth/runtime 是 fatal。
- Scope limits：静态核查，没有执行包、后端、服务或测试。
- Known risks：错误自动进入图、provenance 漏损、伪因果、部分失败静默、untrusted pickle/tar、接口漂移、供应链面过大。
- Review again when：出现窄 adapter、时间模型、inference receipt 或 read-only MCP 的具体实验。
- Action readiness：not_ready。

## 对当前项目的适配点

只保留六个候选方向：decision envelope、inference receipt、bitemporal fields、SHACL lint、conflict packet、projection receipt。它们分别进入以后具体设计窗口，不在本次写入 SCHEMA、pattern、decision 或主架构文档。

## 可拓展性

- 是否适合作为插件/适配层：个别后端接口可以，必须隔离。
- 是否会绑定核心结构：全量采用会严重绑定。
- 未来替换成本：全平台高；单一 record shape 低。
- 可迁移路径：Markdown remains source of truth -> optional one-way projection -> verified round trip -> disposable cache。

## 复杂度和风险

基础安装已有 40+ 直接依赖并覆盖 ML、NLP、图、向量、可视化和媒体处理；extras 又扩展到多个数据库、云和 LLM provider。若为了少量 record shape 引入整个 runtime，复杂度明显不成比例。

安全上，VectorStore 仍加载 pickle，backup restore 需要额外路径验证，embedding / extraction 有 random/hash/adjacency fallback，REST 默认可监听 0.0.0.0 且没有认证。任何未来试验都必须隔离、最小权限、fail closed。

## 不可行点 / 避坑

- 可能失败的条件：把文档声明当实测保证；把内存默认当持久层；让 Agent/MCP 获得正式写权限。
- 已知反例：当前 Rete 与 ontology reasoner placeholder、MCP API 漂移、主 CI 无 pytest。
- 相似踩坑：把 confidence、vote、recency、rank 或 provenance 当 truth。
- 应该避开的实现方式：全量 fork、直连 vault、自动 promotion、untrusted pickle/tar、fallback 后继续给正常结果。
- 更稳的替代方案：借小字段、写 project-local candidate spec、做隔离 contract test、失败显式生成 receipt。

## 融合判断

- 结论：adapt，且仅 design-only / candidate-only。
- 理由：记录形状和反例有价值；运行时 authority、correctness 和 release gates 不满足 VAKS。
- 验证方式：未来按单一实验重新固定 commit，补真实测试与 round-trip receipt。

## 直接判断

- Direct use：no。
- Fork：no。
- Design-only：yes, selective。
- Reject：truth store、reviewed KG writer、writable agent runtime、production adoption claims。
- Current branch value：high as boundary and record-shape reference。
- Whole architecture value：medium-high as comparative material。
- Risk：high if runtime-integrated；low if retained as candidate notes only。
- Next action：close review; reopen only for a concrete narrow experiment。

## 后续行动

本次不改变正式 schema、pattern、decision、handoff 或 index。源卡、候选蒸馏、项目覆盖层与源码锚点保留在 formal vault；源码快照用于以后按同一 commit 复核。

