---
type: schema
status: active
version: 0.1
created: 2026-05-26
updated: 2026-05-30
scope:
  - verified-knowledge-system
  - markdown-system-of-record
  - schema-contract
sources:
  - "[[2026-05-26-architecture-layering-v0-1]]"
  - "[[knowledge-graph-index]]"
  - "[[source-verification-and-trust-model]]"
  - "[[semantic-relation-edge-schema]]"
  - "[[2026-05-27-codex-mediated-ingest-and-review-gate]]"
  - "[[2026-05-27-traceability-first-graduated-verification]]"
  - "[[SOURCE_INTAKE]]"
  - "[[REFERENCE_REVIEW_PROTOCOL]]"
verification_status: active
evidence_level: synthetic
confidence: high
last_verified: 2026-05-30
next_review: 2026-06-03
---

# SCHEMA.md v0.1

本文件是资料库的结构契约。它规定什么可以进入 verified knowledge system、如何记录证据、如何连接关系、如何从原始资料晋级为可复用决策。

当前资料库不是普通 Obsidian 笔记库，而是：

```text
raw source -> summary -> claim -> pattern / anti-pattern -> decision -> context pack
```

Markdown/YAML 是主记录。Obsidian Bases、BM25、vector、QMD、Zilliz、graph score、API、context pack 都是派生层或调用层，不能替代本文件定义的 reviewed knowledge layer。

实现范围说明：本文件不是要把系统缩小成“只有契约”。最终实现应完整包含 Karpathy LLM Wiki 和 llm-wiki-compiler 代表的操作能力：ingest、compile、index、log、query、lint、review queue、provenance、context pack、API/MCP、viewer/Obsidian view。`SCHEMA.md` 的作用是规定这些能力写入和调用时必须服从什么真值契约。

架构口径说明：

```text
对外主架构:
  Capture -> Understand -> Review -> Connect -> Act and Learn

Schema 负责:
  reviewed knowledge 的字段、状态、关系、晋级、降级和自动化边界。

Schema 不负责:
  把第二大脑模型拆成工程模块。
  让 dashboard、retrieval、association score、feedback、brief 或 context pack 决定 truth。
```

知识校准口径：

```text
外部资料不会直接变成 truth。
外部资料先被理解成 candidate points。
candidate points 再和本地 reviewed knowledge 做双向校准。
校准输出是 review input，不是 reviewed relation，也不是 confidence 更新。
```

Review 口径说明：

```text
Review 不只是检查来源。
Review 要判断一个 candidate 在支持、挑战、范围限制和风险下是否仍然站得住。
```

人类可读的 review families：

```text
support:
  支持

attack:
  反对 / 挑战

qualification:
  限定条件 / 适用范围

risk:
  风险

provenance:
  来源 / 派生路径
```

它们大致映射到关系类型：

```text
supports     -> support
contradicts  -> attack
refines      -> qualification
risk_of      -> risk
derived_from -> provenance
```

硬边界：

```text
provenance 只说明来源，不自动构成 support。
有引用不等于有证据。
支持关系变多，不自动提高 confidence。
confidence 只能通过 review 修改。
```

总原则：

```text
Strict checks are lazy gates.

Capture should preserve source identity without forcing full review.
Candidate points may stay lightweight until they are promoted, used for action,
used as evidence for a strong reviewed relation, included in an action basis,
high-impact, stale, contested, or explicitly challenged.

When a strict gate opens, evidence_support, support/challenge review,
coverage_map, action_readiness, and optional point_graph_fragment may be required.
For important promotion or action use, the review input should be an
Evidence Packet: point + source anchor + evidence item + warrant + scope/risk +
minimal revision. Evidence Packet is review input, not a new truth layer.
```

## 1. 核心原则

### 1.1 文件为准

任何重要结论必须写入文件。对话、临时回答、搜索结果、LLM 推理都不能单独成为事实来源。

### 1.2 Raw 不改，Wiki 可编译

- `raw/` 保存来源记录、原文摘录、repo snapshot、文章、论文、视频/播客转录等原始材料。
- `wiki/` 保存编译后的 summary、claim、pattern、anti-pattern、decision、concept、project note。
- `outputs/` 保存问答、分析、健康检查、阶段复盘。
- `products/` 保存对外发布或业务成品，不污染 verified knowledge layer。

### 1.3 搜索只召回，不能裁决

BM25、vector、QMD、Zilliz、GraphRAG、rerank 只能帮助找到候选资料。它们不能替代：

- source provenance
- evidence_level
- verification_status
- confidence
- negative_evidence
- human/AI review
- decision record

### 1.4 先人工/AI 辅助写入，程序做校验

v0.1 阶段允许 AI 辅助生成节点，但必须写入 Markdown/YAML，并接受人类复查。程序第一阶段只做 lint、schema validation、health report，不做 background rewrite、scheduled agents、自动冲突裁决或重型 RAG。

注意：这是阶段边界，不是最终能力边界。后续可以实现完整 ingest/query/lint/context/API/viewer 栈；限制只在于这些运行时能力不能绕过 review 和 reviewed knowledge layer。

### 1.5 Traceability-first, graduated verification

v0.1 的默认规则改为：

```text
先保证来源可追溯。
再按晋级等级增加验证。
```

Raw capture 和 source record 不需要一开始填满 evidence、confidence、relations、rollback、feedback 等字段。它们的底线是：

```text
原始内容在哪里
什么时候收录
谁/哪个作者/组织产生
发布或更新时间
版本、commit、DOI 或 source status
为什么收录
谁/什么流程收录
后续处理状态是什么
```

轻量 provenance 口径借 W3C PROV 的三个问题，但不实现完整 PROV、RDF、OWL、validator 或 provenance graph：

```text
这个资料是什么？        -> source identity
它经历过什么处理动作？  -> capture / extraction activity
谁或什么工具处理过？    -> human / model / tool agent
```

默认 Source 记录保持扁平和轻量；只有 medium / heavy source 才补可选审计轨迹：

```yaml
source_id:
source_uri:
source_type:
version_or_commit:
captured_at:
captured_by:
processing_level: light | medium | heavy

extraction:
  extracted_at:
  extracted_by:
  model:
  tool:
  source_ranges: []
  verbatim_input:
  model_interpretation:

provenance:
  model: PROV-lite
  activities: []
  agents: []
```

边界：

```text
provenance 只负责追溯，不负责判真。
有清楚来源链，不等于 claim 已经成立。
引用不自动构成 support。
review、confidence、action_readiness 仍然按 reviewed knowledge 规则处理。
reviewed_by 属于 reviewed node / relation。
promoted_by 属于 promotion event / reviewed node。
used_sources 属于 context pack / use ledger。
```

When a user directive, explicit correction, preference, or decision is important enough to affect durable knowledge or action, preserve:

```text
verbatim_input:
  the user's exact words

model_interpretation:
  the system's understanding or analysis
```

Do not treat `model_interpretation` as the user's original intent.

Use `verbatim_input` / `model_interpretation` for user directives, explicit corrections, preferences, decisions, and action instructions.
Do not require them for ordinary article, repository, paper, or source capture.

严格验证只在内容晋级或被用于行动时触发：

```text
candidate:
  需要 source refs / source ranges / extracted point / uncertainty。

claim / pattern / anti-pattern:
  需要 evidence、confidence、negative evidence、gaps、关键 relations。

decision / implementation-note / context pack:
  需要 risk、preconditions、rollback、success metric、feedback path。
```

原则：验证不能阻碍 capture。验证应该阻止未经审查的内容变成正式结论或行动依据。

这也意味着验证可以积累完成，而不是单条资料当场完成。只要每条 source 和 candidate 保留清楚来源，后续相似内容就可以形成：

```text
supports
contradicts
refines
risk_of
derived_from
```

这些跨来源信号可以帮助 claim、pattern、decision 晋级。重复出现不是自动真理，但它是比单条当场判断更便宜、更自然的验证入口。

资料处理分级见 `SOURCE_INTAKE.md`：

```text
light:
  普通资料，只做来源和简要记录。

medium:
  项目或复用资料，做摘要、路由、context 候选。

heavy:
  论文、高价值仓库、官方文档、关键决策资料，做完整 provenance、源码/章节锚点、candidate points、review、pattern/anti-pattern/decision。
```

强资料才进入重流程。普通资料不应该被迫填写完整 verified-action 字段。

v0.1 的具体承载位置见 `REVIEW_QUEUE.md`：

```text
source trace
candidate point
calibration / collision signal
point cluster
```

这些是 review queue 记录，不是新的 truth node 类型。正式 truth node 仍然是 source、summary、claim、pattern、anti-pattern、decision、qa、implementation-note。

校准输出可以包括：

```text
candidate_relation
contradiction_candidate
scope_mismatch
stale_assumption_candidate
missing_evidence
synthesis_needed
decision_superseded
review_question
review_due
```

这些输出只能推动 review，不能直接创建 reviewed claim、reviewed relation、truth confidence update、automatic promotion 或 automatic conflict resolution。

查询后的反馈见 `FEEDBACK.md`。反馈字段不直接改变 truth：

```text
truth confidence:
  只能通过 review/promotion 修改。

usefulness:
  可以由用户反馈影响下次排序。

scope fit:
  可以由用户反馈收窄适用范围。
```

反馈记录和 query-run 是 operation records，不是 formal reviewed knowledge nodes。

```text
explicit feedback:
  用户直接纠正、确认、指出遗漏或范围错误。

conversation-derived feedback:
  从连续追问、问题变窄、纠偏、换题等行为中推断的弱信号。
```

它们只能影响：

```text
usefulness
scope fit
activation ranking
route / keyword boost
review_due
```

它们不能影响：

```text
truth confidence
verification_status
source reliability
recorded decision outcome
```

Feedback ledger 的硬规则：

```text
Positive feedback is weak.
Negative feedback creates review pressure.
Explicit correction creates review_due.
```

Allowed event families:

```text
explicit_correction
missing_evidence
scope_mismatch
answer_helpful
contradiction_missed
action_outcome
decision_outcome
```

Decision outcome calibration records action-basis recommendation quality:

```yaml
decision_outcome:
  decision_ref:
  action_basis_ref:
  recommendation:
  confidence_at_decision:
  user_choice:
  outcome_precondition:
    - recommendation_recorded
    - user_choice_or_explicit_override_recorded
  outcome: succeeded | failed | mixed | unresolved
  outcome_note:
  affects:
    - future_recommendation
    - risk_calibration
    - scope_fit
    - option_framing
  never_affects_directly:
    - truth_confidence
    - verification_status
    - source_reliability
```

Decision outcome tells whether the recommendation worked. It does not prove the underlying claim true. Do not record a final decision outcome unless the recommendation and user choice, or explicit user override, are both recorded.

### 1.6 Activation is not truth

冷热分层是 activation layer，不是 truth layer。

```text
memory_tier:
  控制资料在某个 scope 下应该多早被唤起。

verification_status / evidence_level / confidence:
  控制资料能否作为可信结论或行动依据。
```

二者不能混用：

```text
hot != true
warm != verified
cold != useless
```

开发模式下可以临时生成 dev context pack，把相关资料锁定为当前任务的工作记忆。这个 pack 可以包含 core / support / risk / cold references，但它不改变原始节点的 truth status，也不要求把所有相关资料永久升为 hot。

### 1.7 Association neighborhood activation is not truth

HippoRAG-style association retrieval belongs to activation and context-pack preparation.

It can help a query light up:

```text
supporting points
challenging points
risk / anti-pattern
old decisions
scope notes
source / evidence anchors
gaps and review_due
```

But it cannot decide:

```text
truth
support
confidence
evidence_level
action_readiness
reviewed relation creation
```

Rules:

```text
graph traversal / PPR / association score is recall, not evidence.
activated neighbor does not mean supported point.
association path does not replace evidence_support.
association neighborhood prepares a draft context envelope; coverage_map and evidence_sufficiency still decide whether the answer/action basis is auditable enough.
ordinary capture does not trigger association neighborhood activation.
```

### 1.8 Graph retrieval stratification is not truth

GraphRAG / LightRAG-style retrieval can organize context-pack preparation into strata:

```text
low-level retrieval:
  source / text_unit / claim / entity

high-level retrieval:
  pattern / theme / community / community_report

relation neighborhood:
  reviewed relation neighborhood around the query seed
```

This helps the system recall both concrete anchors and broader context.
It cannot decide:

```text
truth
trust
support
confidence
verification_status
evidence_level
reviewed relation creation
action_readiness
```

Rules:

```text
TextUnit anchor is provenance, not support.
Community report is briefing, not truth.
Graph rank is retrieval priority, not trust.
Auto-extracted relation remains candidate material until reviewed.
LLM-derived claim status does not become verification_status.
If graph traversal uses candidate relations, label it candidate_relation_neighborhood, not reviewed_relation_neighborhood.
```

## 2. 节点类型

`type` 是每个节点的第一身份。v0.1 的核心节点类型如下。

| type | 目录建议 | 作用 |
|---|---|---|
| `source` | `raw/articles/`, `raw/repos/`, `raw/papers/` | 记录资料来源、来源质量、采集信息、可验证内容和疑点。 |
| `summary` | `wiki/summaries/` | 对 source 的结构化摘要，不直接等同 truth。 |
| `claim` | `wiki/claims/` | 可被验证或反驳的具体主张。 |
| `pattern` | `wiki/patterns/` | 可复用设计模式，必须说明适用场景、失败条件和最小实现。 |
| `anti-pattern` | `wiki/anti-patterns/` | 反模式、踩坑、失败路线、负面证据。 |
| `decision` | `wiki/decisions/` | 明确采纳、暂缓、拒绝或替换某个方案的决策记录。 |
| `qa` | `outputs/qa/` | 一次问题、分析、结论、引用来源和不确定性的记录。 |
| `implementation-note` | `wiki/projects/` 或项目目录 | 具体项目落地、迁移、验证、回退和操作记录。 |

兼容说明：旧文件中出现的 `anti_pattern` 应逐步迁移为 `anti-pattern`。在迁移前，校验程序可以把二者视为同类。

## 3. 通用字段

以下是正式知识节点的通用字段。v0.1 采用分级要求：raw/source capture 只要求 provenance 底线；candidate 要求可审；claim、pattern、decision、context pack 才要求完整验证字段。

```yaml
type:
status:
created:
updated:
tags:
sources:
verification_status:
evidence_level:
confidence:
last_verified:
next_review:
relations: []
```

以下字段属于可选 activation metadata，不是可信度字段：

```yaml
memory_tier: hot | warm | cold
activation_status: active | dormant | archived
scope_key:
last_activated:
activation_reason:
```

Public concept name:

```text
Activation Tier
```

Compatibility field:

```text
memory_tier
```

Rule:

```text
The vault has activation tiers, not truth tiers.
Hot means read early, not believe more.
```

以下字段属于可选 review / action metadata，用来表达当前是否站得住、能否用于行动：

完整 Evidence-Aware Review 面板是 lazy gate，不是普通 capture 的必填表。

```text
普通 candidate:
  只需要 uncertainty / risk 短注，除非要晋级或用于行动。

必须展开完整 support / challenge / qualification / risk 面板:
  claim / pattern / anti-pattern / decision promotion
  context pack / action basis
  strong reviewed relation
  explicit contradiction
  stale or contested claim
  reviewer-requested standing check
```

```yaml
review_state: candidate | reviewed | rejected
knowledge_state: standing | limited | contested | stale | superseded | rejected | not_enough_evidence | retired
relation_state: candidate | reviewed | rejected | stale
attack_assessment:
  severity: fatal | major | minor | out_of_scope | unresolved
  reason:
  affected_scope:
  requires_review_due: true | false
qualification:
  applies_when:
  does_not_apply_when:
  version_scope:
  project_scope:
  domain_scope:
  time_scope:
  environment_scope:
  assumptions:
temporal_applicability:
  valid_from:
  valid_until:
  supersedes:
  superseded_by:
  invalidated_by:
  applies_to:
    project:
    version:
    environment:
    timeframe:
    conditions:
  check_state: in_scope | out_of_scope | stale | superseded | unknown | needs_review
  reviewer_note:
review_summary:
  why_it_still_holds:
  strongest_challenge:
  scope_limits:
  known_risks:
  review_due_when:
action_readiness:
  state: ready | not_ready | risky | needs_review
  reason:
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for: context_pack | action_basis | decision | promotion | reviewed_relation | risk_sensitive_answer
  missing: []
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
intent_confirmation:
  required: true | false
  restated_intent:
  assumptions: []
  scope_in: []
  scope_out: []
  success_criteria: []
  verification_plan:
  user_confirmed: true | false
  confirmation_ref:
backbrief:
  plan_summary:
  acceptance_criteria_interpretation:
  numbered_assumptions: []
  risks: []
  verification_method:
  approved_by:
```

规则：

- `review_state` 表示是否经过 review。
- `knowledge_state` 表示当前在知识库里是否还站得住。
- `action_readiness` 表示当前行动场景能不能用，不等于 truth status。
- `evidence_sufficiency` 表示当前证据是否足够支撑这次用途，不等于 truth status。
- `intent_confirmation` 表示重大行动前是否对齐用户意图，不等于 truth status。
- `backbrief` 表示执行方如何理解任务、风险和验证方法，不等于 truth status。
- `temporal_applicability` 表示当前时间、版本、项目、环境和 supersession 状态下是否适用，不等于 truth status。
- 一个节点可以 `knowledge_state: contested`，但在低风险、可回滚场景下仍可作为参考。
- 一个节点可以 `knowledge_state: standing`，但对当前项目 `action_readiness: not_ready`。
- 一个节点可以 `knowledge_state: standing`，但 `temporal_applicability.check_state: stale | superseded | out_of_scope`，因此不能直接作为当前 action basis。
- `evidence_sufficiency` 只在 promotion、decision、context pack / action basis、strong reviewed relation、risk_sensitive_answer 或用户明确问“证据够不够”时触发；普通 capture / ordinary query 不强制。
- `intent_confirmation` / `backbrief` 只在重大行动、架构改动、执行任务、部署、高影响 decision 或风险敏感 action basis 前触发；普通问答和普通 capture 不触发。

以下字段属于 candidate / review queue routing metadata。它们用于决定怎么 review，不直接决定 truth：

```yaml
point_type: claim | interpretation | hypothesis | pattern | risk | preference | decision | open_question | implementation_note
verifiability:
  state: verifiable | partially_verifiable | not_verifiable | unknown
  reason:
review_route: evidence_check | rationale_check | instance_check | risk_check | action_basis_check | personalization_only | research_question | code_anchor_check
```

Review queue items classify why a candidate, cluster, collision signal, decision, or dependency needs attention.
They do not create truth and do not replace candidate point types.
They are optional queue routing metadata, not mandatory fields for every candidate point.

```yaml
review_queue_item:
  item_type: low_confidence_claim | contradiction | missing_evidence | synthesis_needed | decision_superseded
  target_refs: []
  triggered_by:
    - candidate_point
    - calibration_signal
    - point_cluster
    - reviewed_node
    - decision
    - feedback_event
    - action_outcome
  suggested_action: approve | reject | merge | override | request_evidence | mark_review_due | create_missing_point
  status: open | in-review | resolved | rejected | parked
  resolution_note:
```

Rules:

- `review_queue_item.item_type` says why attention is needed, not what the point is.
- `low_confidence_claim` can enter review, but cannot be promoted until evidence support and sufficiency are checked.
- `contradiction` stays visible until a reviewer resolves or scopes it.
- `missing_evidence` points to a specific missing support target.
- `synthesis_needed` asks for a reviewed summary judgment across multiple candidates or clusters.
- `decision_superseded` starts an audit-preserving replacement flow; it does not delete the old decision.

以下字段属于 lightweight evidence discipline metadata。它们用于把重要 candidate 的 review 输入收束为 Evidence Packet；普通 capture 和 ordinary query 不强制填写：

```yaml
evidence_packet:
  point:
  point_type:
  evidence_items:
    - source_anchor:
      evidence_granularity: metadata_only | abstract_or_summary | excerpt_or_passage | table_or_code_anchor | full_source_reviewed
      rationale:
      evidence_support:
        span_supports_target: supported | partial | unsupported | unclear
        evidence_role: direct_support | inferential_support | background_context | counterexample
        reviewer_note:
  grounds:
  warrant:
  qualifier:
  strongest_rebuttal:
  challenge_kind: rebuttal | undercut | scope_limit | source_hygiene | stale_assumption | action_failure
  scope_limit:
  risk_flags: []
  omission_check:
    missing_risks:
    missing_scope_limits:
    possible_omissions:
    omission_questions:
    needs_full_source_read: true | false
  review_question:
  minimal_revision_needed: keep | refine_scope | mark_contested | mark_stale | supersede | reject
  review_due_when:
    - new_primary_source
    - contradiction
    - correction_or_retraction
    - source_version_change
    - dependency_release_change
    - action_failure
    - missed_feedback
    - stale_assumption
```

Rules:

- Evidence Packet does not create truth, confidence, reviewed relation, or action readiness by itself.
- `grounds` records the evidence basis; `warrant` records why the evidence supports or weakens the point.
- Source anchors live on `evidence_items`; do not maintain a second top-level `source_anchors` list that can drift from the evidence item.
- CI-08 sandbox rule: source ranges are provenance and review handles until the evidence item names the exact target and fills `span_supports_target`, `evidence_role`, warrant, and scope.
- `evidence_support.evidence_role` is the canonical support/challenge role; avoid a second `relation_to_point` field unless it is a freeform reviewer note.
- `challenge_kind` explains what kind of challenge exists; it does not automatically reject the point.
- `minimal_revision_needed` is a review recommendation, not an automatic edit.
- `evidence_granularity` caps how far a point can be used before stronger evidence is gathered.
- `omission_check` is required only for heavy source digest, important repositories, long papers, high-impact decisions, or reviewer request.
- `review_due_when` records trigger conditions; review_due is pressure to recheck, not proof that the old judgment is false.

默认映射：

```text
claim -> evidence_check
interpretation -> rationale_check
hypothesis -> research_question
pattern -> instance_check
risk -> risk_check
preference -> personalization_only
decision -> action_basis_check
open_question -> research_question
implementation_note -> code_anchor_check
```

规则：

- candidate point 是 atomic review unit，不默认等于 atomic claim。
- `point_type` 表示这个点是什么。
- `verifiability.state` 表示它能不能事实验证。
- `review_route` 默认由 `point_type` 推导，必要时人工覆盖。
- `anti_pattern` 先用 `point_type: risk` + `risk_kind: anti_pattern` 表达。
- `heuristic` 先用 `point_type: pattern` 或 `point_type: interpretation` 表达。
- 只有可验证的 `claim` 可以有 truth / evidence confidence。
- `implementation_note` 的代码位置、版本、行为描述可以部分 evidence-check；从实现泛化出的架构原则必须另走 pattern 或 interpretation review。
- `preference`、`hypothesis`、`open_question` 不允许 truth confidence，但可以有 usefulness、research_value、scope_fit 或 personalization_scope。

以下字段属于 optional candidate decomposition metadata。它只在复杂、高影响、多跳、跨文档、行动相关或有歧义的 candidate 上使用：

```yaml
point_graph_fragment:
  purpose: collision_check | evidence_review | scope_clarification | action_basis | ambiguity_resolution
  entities:
    - id:
      label:
      type:
      aliases: []
      resolution:
        status: resolved | unresolved | ambiguous
        note:
  relation_triplets:
    - subject:
      predicate:
      object:
      qualifier:
      scope:
      source_anchor:
      note:
  open_questions:
    - question:
      blocks_review: true | false
```

规则：

- `point_graph_fragment` 是 review aid，不是 reviewed relation。
- triplet extraction 不是 truth。
- triplet similarity 不是 support。
- triplet conflict 不是 automatic rejection。
- 只有 reviewed relation 可以进入 formal knowledge graph。
- 普通 candidate 不需要 graph fragment。
- 如果一个 fragment 需要超过 3-5 个 essential triplets，应拆成多个 candidate points。
- 无法 source-anchor 的 triplet 只能作为 review question。

以下字段属于 evidence item support metadata。它用于检查某个 source span 是否真的支持当前 candidate point、reviewed node 或 reviewed relation，不属于 Source node 主字段：

```yaml
evidence_support:
  span_supports_target: supported | partial | unsupported | unclear
  evidence_role: direct_support | inferential_support | background_context | counterexample
  reviewer_note:
```

规则：

- URL-only source reference 是 provenance，不是 evidence support。
- Source-range-only reference is provenance, not evidence support; a valid line range still needs target-specific support judgment and warrant.
- 要计入 support，evidence item 必须包含 `source_range`、`quote_or_excerpt`、code anchor、table anchor 或等价 source span。
- `background_context` 可以作为上下文保留，但不能计入 supported，不能提高 `evidence_level` 或 `confidence`。
- `inferential_support` 需要 `reviewer_note`，否则不能作为 promotion support。
- `counterexample` 应进入 `challenge_refs` 或 `risk_refs`。
- `span_supports_target: unsupported | unclear` 不能作为 promotion support。
- 强 reviewed relation 的 evidence 必须支持 relation edge 本身，而不只是分别支持两个端点。
- evidence support 不自动改变 confidence；confidence 仍只能通过 review 修改。
- `supported` + `direct_support` 可计入 supported。
- `partial` + `inferential_support` + `reviewer_note` 可计入 weakly_supported，或由 reviewer 接受为 promotion support。
- `background_context` 永远不能计入 support。
- `counterexample` 应进入 `challenge_refs` 或 `risk_refs`，不应放在 `support_refs`。

### 3.1 字段定义

| 字段 | 必填 | 定义 |
|---|---|---|
| `type` | 是 | 节点类型，使用第 2 节枚举。 |
| `status` | 是 | 节点生命周期状态。 |
| `created` | 是 | 文件首次创建日期，格式 `YYYY-MM-DD`。 |
| `updated` | 是 | 文件最后主动更新日期，格式 `YYYY-MM-DD`。 |
| `tags` | 建议 | Obsidian/Bases 过滤用标签，不作为 truth source。 |
| `sources` | 建议 | 支撑本节点的来源列表，可为 wiki link、URL 或 source record。 |
| `verification_status` | 晋级时 | 该节点当前验证状态。raw/source 可默认为 `unverified`，不阻塞 capture。 |
| `evidence_level` | 晋级时 | 当前证据等级。raw/source 可留空或写 `unknown`。 |
| `confidence` | 晋级时 | 对当前结论的置信度。raw/source 和普通 candidate 不强制。 |
| `last_verified` | 建议 | 最近一次人工/AI 复核日期。 |
| `next_review` | 建议 | 下一次应复查日期。 |
| `relations` | 晋级时 | 语义关系边列表。raw/source 可先写 `[]`，强关系只在晋级时补齐。 |

### 3.6 Activation Metadata / Activation Tier

| 字段 | 必填 | 定义 |
|---|---|---|
| `memory_tier` | 可选 | 当前 scope 下的默认 Activation Tier：`hot`、`warm`、`cold`。字段名保留兼容；概念名优先说 Activation Tier。 |
| `activation_status` | 可选 | 当前是否活跃：`active`、`dormant`、`archived`。 |
| `scope_key` | 可选 | 激活适用的项目、问题、领域或工作流。 |
| `last_activated` | 可选 | 最近一次被主动调取或放入工作上下文的日期。 |
| `activation_reason` | 可选 | 为什么它在该 scope 下被加热或冷却。 |

规则：

- activation metadata 只影响读取顺序和上下文优先级。
- activation metadata 不能提升 `confidence`。
- activation metadata 不能改变 `verification_status`。
- hot means read early, not believe more.
- 如果目标是具体开发任务，应优先创建 dev context pack，而不是把全库文件永久改成 hot。

### 3.2 Status 枚举

通用 `status`：

```text
draft
captured
summarized
unverified
in-review
active
needs-review
superseded
deprecated
rejected
archived
```

节点可使用更具体状态：

```text
source-captured
summary-draft
claim-candidate
pattern-candidate
adopted
avoid
pending
field-tested
```

原则：`status` 表示节点生命周期，`verification_status` 表示可信度状态。二者不要混用。

### 3.3 Verification Status 枚举

```text
unverified
single-source
cross-checked
primary-source
field-tested
conflicted
deprecated
rejected
active
```

含义：

- `unverified`：已记录，但未验证。
- `single-source`：只有单一来源支持。
- `cross-checked`：至少两个独立来源互相支持。
- `primary-source`：来自官方文档、原始论文、源码、实测数据或直接证据。
- `field-tested`：已在项目、工作流或实际样本中验证。
- `conflicted`：存在重要冲突证据，不能直接采用。
- `deprecated`：曾经可用，但现在过时。
- `rejected`：明确不采用。
- `active`：当前作为有效契约、决策或规则使用。

兼容说明：模板中的 `source_status` 和 `validation_status` 暂时保留，但新节点优先写 `verification_status`。后续模板升级时统一。

### 3.4 Evidence Level 枚举

```text
primary
secondary
anecdotal
synthetic
unknown
```

- `primary`：源码、官方文档、论文原文、直接实验、原始数据。
- `secondary`：文章解读、教程、架构分析、他人总结。
- `anecdotal`：个案经验、截图、社媒观点、未复现说法。
- `synthetic`：由本资料库综合多个节点形成的二级判断。
- `unknown`：来源或证据等级尚不明确。

### 3.5 Confidence 枚举

`confidence` 可以用数字或文字，但同一批新文件应优先使用文字：

```text
low
medium
high
```

兼容旧模板时允许：

```text
1
2
3
4
5
```

推荐映射：

```text
1-2 = low
3 = medium
4-5 = high
```

### 3.6 Confidence Cap Without Full Text

Confidence is capped by source access quality.

```yaml
source_access:
  access_level: full_text | source_span | abstract_only | snippet_only | url_only | summary_only | unknown
  has_direct_quote: true | false
  has_source_range: true | false
  confidence_cap: low | medium | high
  cap_reason:
```

Rules:

- `url_only` and `summary_only` cannot support a high-confidence claim.
- `abstract_only` or `snippet_only` should normally cap at medium unless the point is explicitly scoped to what the abstract/snippet says.
- High confidence requires a direct source span, full text, source range, direct observation, or equivalent primary anchor.
- A confidence cap is not a truth judgment; it prevents weak source access from looking stronger than it is.

## 4. Epistemic Fields

gbrain 启发本资料库区分事实、观点、假设、下注和决策。重要 claim、pattern、anti-pattern、decision 应加入以下字段。

```yaml
epistemic_type: fact | take | hypothesis | bet | decision
holder:
valid_from:
valid_until:
supersedes:
superseded_by:
invalidated_by:
applies_to:
  project:
  version:
  environment:
  timeframe:
  conditions:
learned_at:
gaps: []
evidence_timeline: []
```

### 4.1 Epistemic Type

| epistemic_type | 含义 |
|---|---|
| `fact` | 可由来源、源码、数据或直接观察支持的事实。 |
| `take` | 带解释立场的判断，可能合理但不是纯事实。 |
| `hypothesis` | 待验证假设。 |
| `bet` | 在不完全确定下的策略性选择。 |
| `decision` | 已记录依据、风险和回退方案的采纳/拒绝动作。 |

### 4.2 Holder

`holder` 记录该结论是谁持有的，不默认等同资料库真相。

示例：

```yaml
holder: user
holder: Codex
holder: gbrain repo
holder: llm_wiki author
holder: Misa
holder: official docs
```

### 4.3 Time Validity / Applicability

```yaml
valid_from: 2026-05-26
valid_until:
supersedes:
superseded_by:
invalidated_by:
applies_to:
  project:
  version:
  environment:
  timeframe:
  conditions:
learned_at: 2026-05-26
```

- `valid_from`：该结论在现实世界中开始成立的时间。
- `valid_until`：该结论在现实世界或当前 scope 下不再适用的时间。
- `supersedes`：本结论替代的旧判断、旧决策或旧关系。
- `superseded_by`：替代本结论的新判断、决策或关系。
- `invalidated_by`：使本结论失效或不再适用的来源、证据、事件或 review。
- `applies_to`：本结论适用的 project、version、environment、timeframe 和 conditions。
- `learned_at`：本资料库学习/记录该结论的时间。

如果不清楚，留空，不要编造。

`valid_until` 留空不代表永久有效。
它只表示尚未记录经过 review 的失效边界。

Staleness is separate from validity:

```text
valid_until:
  applicability boundary

stale / review_due:
  review pressure
```

不要把“需要复查”直接写成“已经失效”；也不要把“已过适用范围”当成历史上从未成立。

Graphiti / Zep 的启发是 temporal validity window：

```text
created / learned time:
  资料库何时知道这件事。

valid time:
  这件事在现实世界何时成立，何时不再成立。
```

本资料库不照搬自动构图或自动 invalidation。
只吸收结构化 applicability check：

```text
Truth is source-backed.
Applicability is time-, version-, and scope-bound.
```

### 4.4 Evidence Timeline

高影响 claim、pattern、decision 应维护证据时间线。

```yaml
evidence_timeline:
  - date: 2026-05-26
    source: "[[source-node]]"
    observation: "What was observed."
    effect: supports | contradicts | refines | risk_of | derived_from | weakens
    confidence: low | medium | high
```

正文中也应保留“支持证据 / 反例 / 当前结论 / 复查计划”四段，便于人读。

### 4.5 Gaps

`gaps` 记录当前缺口，不要把缺口藏进结论里。

```yaml
gaps:
  - "Only README reviewed; source code not checked."
  - "No field test yet."
  - "Conflicting evidence exists but not resolved."
```

## 5. Relations 关系边

`relations` 是核心字段，不是装饰字段。可信图谱以 YAML 关系边为准，Obsidian 双链和 tags 只是辅助。

Reviewed relation 来自 review 后的校准结果，不来自相似度本身：

```text
Similarity can suggest calibration.
Similarity is not support.
Candidate relation is not reviewed relation.
```

### 5.1 Candidate Relation Suggestions

```yaml
candidate_relation_suggestions:
  - target: "[[node-name]]"
    relation_type: supports | contradicts | refines | risk_of | derived_from
    relation_state: candidate
    why_suggested:
    source_anchor:
    evidence_support:
      span_supports_target: supported | partial | unsupported | unclear
      evidence_role: direct_support | inferential_support | background_context | counterexample
      reviewer_note:
    suggested_at: 2026-05-26
```

Candidate relation suggestions are review input.
They cannot create reviewed relations, relation strength, or truth confidence.
They may guide Point Collision, context activation, or review queue routing.
If a candidate relation is promoted, it must become a reviewed relation with evidence for the edge itself.

### 5.2 Reviewed Relation Format

```yaml
relations:
  - target: "[[node-name]]"
    relation_type: supports | contradicts | refines | risk_of | derived_from
    relation_state: reviewed | contested | stale | superseded
    strength: 1-5
    confidence: low | medium | high
    evidence:
      - source_id: "[[source-or-claim]]"
        source_range:
        quote_or_excerpt:
        evidence_support:
          span_supports_target:
          evidence_role:
          reviewer_note:
    rationale: "One sentence explaining why this reviewed edge exists."
    created: 2026-05-26
    last_verified: 2026-05-26
```

Reviewed relations belong to reviewed nodes, promoted patterns, decisions, context-pack/action-basis records, or other reviewed knowledge surfaces.
They do not belong to raw Source nodes.
Compatibility note: old records may contain weak relation-like lists. Treat those as `candidate_relation_suggestions` until a review upgrades them.

### 5.3 关系类型

MVP 只启用五种核心关系。关系类型少一点，review 质量会更高，也更不容易把普通相关性误写成正式边。

| type | 含义 |
|---|---|
| `supports` | 当前节点支持目标节点。 |
| `contradicts` | 当前节点反驳或冲突于目标节点。 |
| `refines` | 当前节点细化目标节点。 |
| `derived_from` | 当前节点从某来源、摘要或主张提炼而来。 |
| `risk_of` | 当前节点指出目标节点可能产生的风险。 |

先 parked 的扩展关系：

```text
replaces
implements
applies_to
inspired_by
alternative_to
blocked_by
```

这些不是被拒绝，只是不进入第一版核心关系集合。需要它们时，先用正文说明或 decision metadata 记录，不急着扩展 YAML relation enum。

### 5.4 Reviewed Relation Strength

For reviewed relations only, `strength` 表示语义关系强度，范围 `1-5`。

| strength | 含义 |
|---|---|
| `1` | 弱相关，只是背景线索。 |
| `2` | 有相关性，但证据较弱。 |
| `3` | 明确相关，可用于上下文召回。 |
| `4` | 强相关，应进入分析或 context pack。 |
| `5` | 核心关系，影响 claim/pattern/decision 判断。 |

规则：

- `strength >= 4` 必须有 `evidence` 和 `rationale`。
- `contradicts`、`risk_of` 不得省略 `rationale`。
- `supports`、`contradicts`、`refines`、`risk_of` 的强边 evidence 必须能说明证据如何支持这条边本身。
- `derived_from` 是 provenance relation，不自动构成 support。
- 无证据的强边应被 health check 标记。
- 双向关系需要两条边分别记录，不默认自动互逆。
- Candidate relation suggestions do not have `strength` or `confidence`.

### 5.5 派生分数

程序未来可以从主记录派生：

- source overlap
- common neighbor
- type affinity
- vector similarity
- graph score
- Personalized PageRank / association score
- graph traversal path
- context pack ranking

但这些都是派生分数，不能写回替代人工记录的 `relations`。

## 6. Node Contracts

### 6.1 Source

最小 frontmatter。Source 的重点是 provenance，不是验证结论：

```yaml
type: source
status: source-captured
title:
source_id:
source_uri:
source_url:
source_type:
version_or_commit:
captured_at:
captured_by:
raw_location:
processing_mode: inbox | immediate
processing_level: light | medium | heavy
review_priority: normal
review_owner: Codex
formalization_status: raw-only
topics:
projects:
verification_status: unverified
candidate_relation_suggestions: []
tags:
```

可选字段：

```yaml
author:
publisher:
published_at:
extraction:
  extracted_at:
  extracted_by:
  model:
  tool:
  source_ranges: []
provenance:
  model: PROV-lite
  activities: []
  agents: []
source_metadata_quality:
freshness:
relevance:
source_hygiene_note:
source_independence_hint:
last_verified:
next_review:
```

正文建议包含：

- 为什么收录
- 来源信息
- 原始内容位置或摘录范围
- 初步看点
- 明显疑点
- 下一步

Source 允许低摩擦写入。只要来源可追溯，就可以先成为 raw evidence。`processing_mode` 决定处理节奏，不决定可信度。
Source node 不拥有 truth `confidence` 或 `cross_source_count`。来源卫生、元数据质量和独立性只能作为 hygiene hints；truth confidence 属于 reviewed claim / reviewed node / reviewed relation，交叉来源数量属于 review aggregation 或 coverage，不属于 Source 自身。

```text
inbox      = 普通自动捕获，先进入 raw/inbox 或对应 raw 目录，等待批处理。
immediate  = 用户明确点名“提炼这篇/分析这个链接/马上入库”，由 Codex 立刻处理。
```

### 6.2 Summary

最小 frontmatter：

```yaml
type: summary
status: summary-draft
created:
updated:
sources:
topics:
verification_status: single-source
evidence_level:
confidence:
last_verified:
next_review:
relations: []
tags:
```

规则：

- summary 必须指向至少一个 source。
- summary 是编译结果，不是最终 truth。
- summary 中提到的重要结论应晋级为独立 claim。

### 6.3 Claim

最小 frontmatter：

```yaml
type: claim
status: claim-candidate
claim:
created:
updated:
topics:
related_projects:
sources:
supporting_sources:
conflicting_sources:
evidence:
  - source_id:
    source_range:
    quote_or_excerpt:
    evidence_support:
      span_supports_target:
      evidence_role:
      reviewer_note:
verification_status: unverified
evidence_level: unknown
confidence:
impact:
last_verified:
next_review:
epistemic_type: hypothesis
holder:
valid_from:
valid_until:
learned_at:
gaps: []
evidence_timeline: []
relations: []
tags:
```

规则：

- claim 必须能被支持或反驳。
- claim 进入 decision 前至少应达到 `single-source`，高影响 claim 应达到 `cross-checked` 或 `field-tested`。
- claim 必须显式记录反例或说明“暂未发现反例”。

### 6.4 Pattern

最小 frontmatter：

```yaml
type: pattern
status: draft
created:
updated:
source_libraries:
sources:
related_concepts:
related_projects:
adoption_status: watch
verification_status: single-source
evidence_level:
evidence_count:
confidence:
negative_evidence:
replaces:
superseded_by:
extension_points:
last_verified:
next_review:
epistemic_type: take
gaps: []
evidence_timeline: []
relations: []
tags:
```

规则：

- pattern 必须说明解决的问题、适用场景、不适用场景。
- pattern 必须有反例与避坑。
- pattern 不能只因为“外部库厉害”就进入 adopted。

### 6.5 Anti-pattern

最小 frontmatter：

```yaml
type: anti-pattern
status: draft
created:
updated:
domain:
failure_mode:
severity:
likelihood:
complexity_cost:
cross_validated_with:
related_projects:
replacement:
verification_status: single-source
evidence_level:
confidence:
last_verified:
next_review:
epistemic_type: take
gaps: []
evidence_timeline: []
relations: []
decision: avoid
tags:
```

规则：

- anti-pattern 必须记录失败条件。
- anti-pattern 必须说明替代方案或回退方式。
- 与 decision 相关的 anti-pattern MVP 先通过 `risk_of` 连接；阻塞关系可以先写在正文或 decision metadata，暂不扩展 relation enum。

### 6.6 Decision

最小 frontmatter：

```yaml
type: decision
status: draft
created:
updated:
decision:
decision_scope:
related_projects:
based_on:
patterns:
anti_patterns:
outcome: pending
verification_status: in-review
evidence_level:
evidence_strength:
confidence:
negative_evidence:
replaces:
supersedes:
superseded_by:
supersession_reason:
affected_claims_review_due: []
affected_patterns_review_due: []
affected_relations_review_due: []
affected_context_packs_review_due: []
intent_confirmation:
  required: true | false
  restated_intent:
  assumptions: []
  scope_in: []
  scope_out: []
  success_criteria: []
  verification_plan:
  user_confirmed: true | false
backbrief:
  plan_summary:
  acceptance_criteria_interpretation:
  numbered_assumptions: []
  risks: []
  verification_method:
decision_outcome:
  recommendation:
  confidence_at_decision:
  user_choice:
  outcome_precondition:
    - recommendation_recorded
    - user_choice_or_explicit_override_recorded
  outcome: succeeded | failed | mixed | unresolved
  outcome_note:
migration_path:
rollback_path:
last_verified:
next_review:
epistemic_type: decision
gaps: []
evidence_timeline: []
relations: []
tags:
```

规则：

- decision 必须记录背景、依据、备选方案、风险、验证方式、回退路径。
- 高影响 decision 不能只依赖单一 source。
- 如果只能单源决策，必须把 `gaps` 和 `next_review` 写清楚。
- 新决策替代旧决策时，旧 decision 不删除；新旧决策必须双向链接，并保留替代原因、适用 scope 和 audit trail。
- 被旧决策支撑过的 claim、pattern、relation、context pack 或 action basis，应按影响范围标记 `review_due`，而不是被静默改写。
- `superseded_by` 改变当前适用性，不等于抹掉旧决策在历史时间窗口内的有效性。
- 重大 decision 应有 intent confirmation 或同等用户确认记录。
- decision outcome 只用于校准未来建议、风险感和选项 framing，不直接改变 claim truth confidence。

### 6.7 QA

最小 frontmatter：

```yaml
type: qa
status: archived
created:
updated:
question:
answer_summary:
sources:
related_claims:
related_patterns:
related_decisions:
verification_status:
evidence_level:
confidence:
last_verified:
next_review:
relations: []
tags:
```

规则：

- qa 是一次分析记录，不默认成为 truth。
- qa 中产生的高价值结论应拆成 claim、pattern、anti-pattern 或 decision。
- qa 应反向连接到相关节点。

### 6.8 Implementation Note

最小 frontmatter：

```yaml
type: implementation-note
status: draft
created:
updated:
project:
related_decisions:
related_patterns:
related_anti_patterns:
sources:
verification_status:
evidence_level:
confidence:
validated_by:
rollback_path:
last_verified:
next_review:
relations: []
tags:
```

规则：

- implementation-note 记录具体落地事实，不替代 design decision。
- 必须写清验证命令、验证结果、失败边界和回退方式。

## 7. 晋级流程

### 7.1 标准链路

```text
raw source
  -> summary
  -> claim
  -> pattern / anti-pattern
  -> decision
  -> implementation-note
  -> context pack
```

### 7.2 入库模式

所有材料无论来自自动捕获、用户粘贴、链接、语音转写、截图还是外部 agent，都先保留 raw 记录。区别只在于什么时候处理。

```yaml
processing_mode: inbox | immediate
review_priority: low | normal | high
review_owner: Codex | user | external-agent
formalization_status: raw-only | candidate-generated | reviewed | promoted | rejected
```

规则：

- `inbox` 是默认模式。自动捕获、Readwise、Telegram、Whisper、N8N、浏览器剪藏都只能先写入 `raw/inbox/` 或对应 raw source 目录。
- `immediate` 只在用户明确点名时使用，例如“提炼这篇”“分析这个链接”“马上整理”“把这篇入库”。
- `immediate` 也必须先保存 raw source，再由 Codex 生成 summary / claim / pattern / anti-pattern / decision 候选。
- daily brief 和 weekly synthesis 只能写入 `outputs/review/` 或 `outputs/qa/`，不能直接写入 formal reviewed knowledge layer。
- 候选内容只有经过 Codex/用户 review，并按晋级等级补齐必要字段后，才能成为正式节点。source/candidate 只要求可追溯；claim/pattern/decision/context pack 才要求更严格的 evidence、confidence、negative evidence、relations、risk 或 rollback。

### 7.3 晋级门槛

| 阶段 | 进入条件 | 输出 |
|---|---|---|
| source -> summary | source 已记录来源、采集时间、疑点 | 结构化摘要 |
| summary -> claim | 摘要中出现可验证判断 | 独立 claim |
| claim -> pattern | claim 可复用，能解释一类问题 | pattern |
| claim -> anti-pattern | claim 指向失败路线或风险 | anti-pattern |
| pattern -> decision | pattern 和项目目标匹配，有证据和回退方案 | decision |
| decision -> implementation-note | 决策进入项目执行 | 验证和落地记录 |
| nodes -> context pack | 任务需要 Agent 调用 | 带证据、反例、关系边和 gaps 的上下文包 |

### 7.4 降级和拒绝

任何节点发现冲突证据后，应执行之一：

- `verification_status: conflicted`
- `status: needs-review`
- `status: deprecated`
- `status: rejected`
- 新增 anti-pattern 或 decision 说明不采用

不允许静默覆盖旧结论。重要变化应进入 `evidence_timeline`。

## 8. AI 写入规则

### 8.1 AI-readable Preamble

每个重要节点正文开头应有短 preamble，用 3-6 行说明：

- 这个节点是什么
- 当前结论是什么
- 可信度和证据状态
- 主要风险或缺口

### 8.2 Never Create in Isolation

新增或修改节点时，应检查是否需要同步更新：

- `wiki/indexes/knowledge-graph-index.md`
- 对应 source / summary / claim / pattern / anti-pattern / decision
- 相关 `relations`
- `outputs/qa/` 分析记录
- 后续 context pack 或 handoff

v0.1 不要求每次都全量同步，但不允许关键节点完全孤立。

### 8.3 Two-output Rule

高信号分析默认产生两个输出：

1. 给用户的回答。
2. 写入资料库的 source、summary、claim、pattern、anti-pattern、decision 或 qa。

如果只回答不写入，必须是低价值临时问题，或用户明确要求只读/不改文件。

### 8.4 Progressive Context Loading

Agent 使用本资料库时按层加载：

```text
L0: purpose.md
L1: SCHEMA.md + wiki/indexes/knowledge-graph-index.md
L2: relevant decision / pattern / anti-pattern / claim
L3: supporting summary / source / qa / implementation-note
L4: raw snapshot or external source, only when needed
```

禁止默认把全库塞进上下文。

### 8.5 Agent Access Levels

外部 agent，尤其是 Misa/gbrain/Hermes runtime，不默认拥有资料库写权限。

```text
Level 1: read-only
  Agent 只能读取 SCHEMA、index、context pack 和 verified 节点。

Level 2: suggest-only
  Agent 可以提出候选 source / claim / pattern / anti-pattern / decision，
  但只能进入 review 队列或返回给 Codex/用户把关。

Level 3: reviewed write
  Codex 或用户完成来源、证据、反例、关系边和风险检查后，
  才能把候选内容写入正式 wiki 节点。

Level 4: limited auto-write
  未来只允许低风险区域自动写入，例如 outputs/qa 或 outputs/review。
  不允许自动改 decision、SCHEMA、templates 或 raw。

Level 5: full write
  v0.1 禁止。
```

当前默认：

```text
Misa/gbrain: Level 1 read-only
Misa candidate output: Level 2 suggest-only
Codex: Level 3 reviewed write
User: final authority
```

Review 队列不是 reviewed knowledge layer。候选内容只有在通过 Codex/用户复核并迁移到 `wiki/claims/`、`wiki/patterns/`、`wiki/anti-patterns/` 或 `wiki/decisions/` 后，才算正式知识节点。

## 9. Health Check

程序第一阶段应该先报告问题，不自动修复。

### 9.1 必查项

- 按节点等级缺少必填字段：raw/source 缺 provenance，candidate 缺 source refs，promoted node 缺 verification/action fields。
- claim 没有 source。
- pattern 没有反例或失败条件。
- decision 没有 negative_evidence、migration_path 或 rollback_path。
- anti-pattern 没有 replacement 或替代方案。
- `relations` 中 `strength >= 4` 但没有 evidence。
- `relations` 中有 evidence 但目标文件不存在。
- 高影响 claim 孤立，没有 pattern/decision/anti-pattern 连接。
- `verification_status: active` 但 `last_verified` 为空。
- `next_review` 过期。
- qa 产生了重要结论但没有拆分成 claim/pattern/decision。
- source 标记 `deprecated` 但下游 claim/decision 未复查。
- 高影响 action basis / decision 缺少 intent confirmation 或 success criteria。
- claim 标记 high confidence 但只有 `abstract_only`、`snippet_only`、`url_only` 或 `summary_only` source access。
- `valid_until` 已过但下游 action basis 未标 out_of_scope / review_due。
- `stale` / `review_due` 被当成 `valid_until` 使用，或过期信息被当成 false 处理。
- 已记录 decision outcome 但没有 action_basis_ref / confidence_at_decision / outcome_note。

### 9.2 健康检查输出

健康检查应输出：

```text
missing-required-fields
unsupported-claims
stale-decisions
validity-window-mismatch
conflicted-nodes
orphan-high-impact-nodes
weak-relations
missing-negative-evidence
missing-intent-confirmation
confidence-cap-violations
missing-outcome-calibration
review-due
```

### 9.2.1 Maintenance Manifest

Maintenance manifest is a lint queue, not an automatic repair worker.

```yaml
maintenance_manifest:
  generated_at:
  scope:
  items:
    - item_type: missing_required_field | unsupported_claim | stale_dependency | validity_window_mismatch | confidence_cap_violation | missing_intent_confirmation | missing_outcome_calibration | orphan_review_candidate | missing_relation_target
      target_ref:
      severity: low | medium | high
      reason:
      suggested_action: add_source_anchor | add_evidence_support | mark_review_due | add_intent_confirmation | record_outcome | narrow_scope | ask_user | needs_review
      status: open | resolved | parked
```

It may create review queue items. It may not rewrite reviewed knowledge automatically.

### 9.3 不做事项

health check 不得在 v0.1 自动：

- 改写正文结论
- 替换旧节点
- 自动解决冲突
- 批量生成关系边
- 把向量相似度当作证据

## 10. Context Pack

Context pack 是调用层输出，不是新的 reviewed knowledge layer。

未来 `POST /context-pack` 或脚本生成的 context pack 应包含：

```yaml
version: 1
prompt:
budget:
  requested_tokens:
  estimated_tokens:
  truncated: true | false
  trimmed_sections: []
project:
  root:
  pages:
  pending_candidates:
  lint:
primary: []
neighbors: []
warnings: []
gaps: []
suggested_actions: []
source_windows: []
read_only: true
not_truth_layer: true
not_action_basis: true
question:
answer_scope:
supporting_claims:
contradicting_claims:
patterns:
anti_patterns:
decisions:
sources:
gaps:
confidence:
last_verified:
association_neighborhood:
  seed_points: []
  activation_basis: []
  support_refs: []
  challenge_refs: []
  risk_refs: []
  decision_refs: []
  scope_refs: []
  gaps: []
retrieval_strata:
  low_level:
    source_refs: []
    text_unit_refs: []
    claim_refs: []
    entity_refs: []
  high_level:
    pattern_refs: []
    theme_refs: []
    community_refs: []
    community_report_refs: []
  relation_neighborhood:
    seed_refs: []
    relation_refs: []
    traversal_basis:
    boundary_note:
temporal_applicability:
  valid_from:
  valid_until:
  superseded_by:
  invalidated_by:
  applies_to:
    project:
    version:
    environment:
    timeframe:
    conditions:
  check_state: in_scope | out_of_scope | stale | superseded | unknown | needs_review
  reviewer_note:
decision_superseding:
  old_decision:
  replacement_decision:
  supersession_reason:
  affected_claims: []
  affected_patterns: []
  affected_relations: []
  affected_context_packs: []
  mark_review_due: true | false
  audit_note:
intent_confirmation:
  required: true | false
  restated_intent:
  assumptions: []
  scope_in: []
  scope_out: []
  success_criteria: []
  verification_plan:
  user_confirmed: true | false
decision_outcome:
  decision_ref:
  recommendation:
  confidence_at_decision:
  user_choice:
  outcome_precondition:
    - recommendation_recorded
    - user_choice_or_explicit_override_recorded
  outcome: succeeded | failed | mixed | unresolved
  outcome_note:
context_pack_trace:
  used_sources: []
  ignored_sources: []
  ignored_reason:
  activation_role: core | support | risk | cold_reference
  unresolved_contradictions: []
  risk_flags: []
coverage_overview:
  supported:
  weakly_supported:
  challenged:
  missing_evidence:
  out_of_scope:
  risk_flags:
coverage_map:
  - point:
    point_type:
    coverage_status: supported | weakly_supported | challenged | missing_evidence | out_of_scope | not_verifiable
    support_refs: []
    challenge_refs: []
    risk_refs: []
    critical_omissions: []
    note:
action_readiness:
  state: ready | not_ready | risky | needs_review
  reason:
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for: context_pack | action_basis | decision | promotion | reviewed_relation | risk_sensitive_answer
  missing: []
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
```

`coverage_map` 是 Context Pack / Action Basis 的审计面，不是新的 truth layer。

规则：

- Context pack evidence envelope is read-only: it may prepare context, expose warnings/gaps, and suggest actions, but it must not write wiki, promote candidates, or mutate reviewed knowledge.
- `source_windows` default to empty. Raw snippets require explicit include_sources / includeSources and must stay path-confined.
- `suggested_actions` are suggestions only; they are not automatic actions, review verdicts, or approvals.
- `primary` and `neighbors` explain activation and retrieval context; they do not provide support by relatedness alone.
- `budget.truncated` and `trimmed_sections` are warnings about missing context, not permission to hide known gaps.
- context pack 必须 coverage-aware，但不默认展开完整审计表。
- `association_neighborhood` 是 query/context-pack 的激活草稿，不是 proof、coverage 或 truth layer。
- association neighborhood 可以帮助找 support / challenge / risk / decision / scope，但每个关键判断仍要走 coverage_map / evidence_support / evidence_sufficiency。
- graph traversal、PPR、similarity 或 association score 不能计入 `support_refs`，除非另有 reviewed evidence item 支持具体 point 或 relation。
- `retrieval_strata` 只是 context-pack preparation 的召回结构：low_level 找具体 source / text_unit / claim / entity，high_level 找 pattern / theme / community，relation_neighborhood 找 reviewed relation 周边上下文。
- TextUnit anchor 是 provenance，不是 support；community report 是 briefing，不是 truth；graph rank 是 retrieval priority，不是 trust。
- auto-extracted relation / claim / community summary 只能进入 candidate material 或 review input，不能直接成为 reviewed relation、verification_status 或 action basis。
- 如果 relation-neighborhood 检索使用的是候选关系，应标成 `candidate_relation_neighborhood`，不能叫 `reviewed_relation_neighborhood`。
- `temporal_applicability` 是 Context Pack / Action Basis 的适用性检查，不是 truth layer；truth is source-backed，applicability is time-, version-, and scope-bound。
- `decision_superseding` 是 action-basis 审计提示：旧决策不删除，新决策只在 scope 内替代它，受影响内容应先 review_due。
- `intent_confirmation` 是重大行动前的对齐提示；没有确认时不应把高影响 context pack 标成 ready。
- `decision_outcome` 是后续 use ledger / calibration 输入，不是 context pack 当下判真的证据。
- `context_pack_trace` 解释什么被使用、什么被忽略、为什么忽略，以及它在 pack 里是什么 activation role；它是 trace/use ledger surface，不是 truth layer。
- stale / superseded / out_of_scope 的点可以作为背景或历史，但不能直接输出 `action_readiness: ready`，除非 context pack 明确采用了替代依据或收窄 scope。
- 完整 `coverage_map` 只要求覆盖回答或行动依据中实际使用的关键判断。
- ordinary query / 普通回答不强制生成完整 `coverage_map`。
- citation 不等于 coverage。
- `coverage_status` 不能自动提高 `confidence`。
- `missing_evidence` 不等于 false，只说明当前行动依据缺证据。
- `challenged` 不等于 rejected，只说明存在 contradiction、attack、counterexample 或 risk。
- `out_of_scope` 表示证据或判断不适用于当前 project / version / time / action。
- `not_verifiable` 用于 preference、open_question、hypothesis、interpretation 等不走 claim-style truth verification 的点。
- `risk_flags` 只做 overview 风险提示；具体风险仍放在 `risk_refs`，行动可用性仍看 `action_readiness: risky | needs_review`。
- coverage_map 消费 `evidence_support`：`direct_support` 可计入 supported；带 `reviewer_note` 的 `inferential_support` 默认计入 weakly_supported 或 reviewer-accepted support；`background_context` 不能计入 supported；`counterexample` 进入 challenged 或 risk。
- `evidence_sufficiency` 在 draft evidence envelope / draft context pack 组好后、Context Pack / Action Basis 被定稿为 action-ready 前运行：证据不足不能输出 ready action basis；`retrieve_more` 是建议动作，不是自动检索；`out_of_scope` 可以要求 `narrow_scope`。
- `critical_omissions` 只记录已知重大遗漏，不做全库/全 source 遗漏扫描。
- 默认只显示 `coverage_overview`、高风险项、被挑战项和缺证据项；需要决策、行动、agent context pack、高影响回答、显式 audit 或回答被挑战时，再展开完整 key-point detail。
- 非可验证点仍然可以有 rationale、risk 或 action-basis coverage。

排序优先级：

1. `verification_status`
2. `evidence_level`
3. `confidence`
4. `relation strength`
5. 是否包含 negative evidence
6. freshness / last_verified
7. 搜索相似度

搜索相似度永远排在可信字段之后。

## 10.1 Dev Context Pack

Dev context pack 是 context pack 的开发模式变体，详见 `DEV_CONTEXT.md`。

它用于把某个项目或任务的相关资料临时锁定为工作记忆：

```text
Core:
  必须读、必须遵守。

Support:
  需要时展开的正向参考。

Risk:
  决策前必须检查的反模式、负证据、冲突和边界。

Cold References:
  可追溯来源和历史资料，只在查证据时打开。
```

Dev context pack 是 operation record，不是 formal reviewed knowledge node。

它可以临时激活 cold source，但不能因此修改该 source 的 truth status。

## 11. 自动化边界

### 11.1 v0.1 允许

- Markdown/YAML schema lint。
- 文件命名检查。
- 缺字段报告。
- 过期 review 报告。
- orphan node 报告。
- relation target 存在性检查。
- source / claim / pattern / decision dashboard。
- 人工触发的 context pack 生成。
- 外部 agent 读取资料库。
- 外部 agent 生成候选建议到 review 队列。

### 11.2 v0.1 不做

- background rewrite。
- scheduled agents。
- 自动冲突裁决。
- 自动把 LLM 提取内容升为 truth。
- 自动发布到 products。
- 允许 Misa/gbrain/Hermes runtime 直接修改正式 wiki 节点。
- 允许外部 agent 修改 `SCHEMA.md`、`templates/` 或 `raw/`。
- 完整桌面 App。
- 重型 RAG / HNSW / reranker / query cache。
- 用 vector search 替代 source/claim/decision。

## 12. 文件命名建议

日期型记录：

```text
YYYY-MM-DD-short-slug.md
```

稳定概念/模式：

```text
short-kebab-case-name.md
```

外部 repo source：

```text
raw/repos/YYYY-MM-DD-repo-name-source.md
```

qa：

```text
outputs/qa/YYYY-MM-DD-question-topic.md
```

## 13. v0.1 到 v0.2 的迁移任务

下一阶段再做，不在本文件创建时强行完成：

- 升级 `templates/source-record.md`、`claim-record.md`、`design-pattern.md`、`anti-pattern.md`、`decision-record.md`，统一 `verification_status`。
- 创建 `templates/summary-record.md`、`templates/qa-record.md`、`templates/implementation-note.md`。
- 创建 `templates/review-candidate.md`。
- 写 schema lint 脚本。
- 写 health check 报告脚本。
- 创建第一批 Obsidian Bases dashboard。
- 为 context pack 定义最小 JSON 输出。

## 14. 当前硬边界

本资料库的核心不是“资料越多越好”，而是：

```text
每个重要结论都有来源。
每个可采纳模式都有反例。
每个决策都有证据、风险、回退。
每条强关系边都有理由。
每次自动化都服从 Markdown 主记录。
```
