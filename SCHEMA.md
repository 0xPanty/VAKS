---
type: schema
status: active
version: 0.1
created: 2026-05-26
updated: 2026-05-27
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
last_verified: 2026-05-27
next_review: 2026-06-03
---

# SCHEMA.md v0.1

本文件是资料库的结构契约。它规定什么可以进入 verified knowledge system、如何记录证据、如何连接关系、如何从原始资料晋级为可复用决策。

当前资料库不是普通 Obsidian 笔记库，而是：

```text
raw source -> summary -> claim -> pattern / anti-pattern -> decision -> context pack
```

Markdown/YAML 是主记录。Obsidian Bases、BM25、vector、QMD、Zilliz、graph score、API、context pack 都是派生层或调用层，不能替代本文件定义的 verified truth layer。

实现范围说明：本文件不是要把系统缩小成“只有契约”。最终实现应完整包含 Karpathy LLM Wiki 和 llm-wiki-compiler 代表的操作能力：ingest、compile、index、log、query、lint、review queue、provenance、context pack、API/MCP、viewer/Obsidian view。`SCHEMA.md` 的作用是规定这些能力写入和调用时必须服从什么真值契约。

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

注意：这是阶段边界，不是最终能力边界。后续可以实现完整 ingest/query/lint/context/API/viewer 栈；限制只在于这些运行时能力不能绕过 review 和 verified truth layer。

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
replaces
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
collision signal
point cluster
```

这些是 review queue 记录，不是新的 truth node 类型。正式 truth node 仍然是 source、summary、claim、pattern、anti-pattern、decision、qa、implementation-note。

查询后的反馈见 `FEEDBACK.md`。反馈字段不直接改变 truth：

```text
truth confidence:
  只能通过 review/promotion 修改。

usefulness:
  可以由用户反馈影响下次排序。

scope fit:
  可以由用户反馈收窄适用范围。
```

反馈记录和 query-run 是 operation records，不是 formal truth nodes。

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
```

它们不能影响：

```text
truth confidence
verification_status
source reliability
decision outcome
```

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

### 3.6 Activation Metadata

| 字段 | 必填 | 定义 |
|---|---|---|
| `memory_tier` | 可选 | 当前 scope 下的默认激活优先级：`hot`、`warm`、`cold`。 |
| `activation_status` | 可选 | 当前是否活跃：`active`、`dormant`、`archived`。 |
| `scope_key` | 可选 | 激活适用的项目、问题、领域或工作流。 |
| `last_activated` | 可选 | 最近一次被主动调取或放入工作上下文的日期。 |
| `activation_reason` | 可选 | 为什么它在该 scope 下被加热或冷却。 |

规则：

- activation metadata 只影响读取顺序和上下文优先级。
- activation metadata 不能提升 `confidence`。
- activation metadata 不能改变 `verification_status`。
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

## 4. Epistemic Fields

gbrain 启发本资料库区分事实、观点、假设、下注和决策。重要 claim、pattern、anti-pattern、decision 应加入以下字段。

```yaml
epistemic_type: fact | take | hypothesis | bet | decision
holder:
valid_from:
valid_until:
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

### 4.3 Time Validity

```yaml
valid_from: 2026-05-26
valid_until:
learned_at: 2026-05-26
```

- `valid_from`：该结论在现实世界中开始成立的时间。
- `valid_until`：该结论失效或预计需要重审的时间。
- `learned_at`：本资料库学习/记录该结论的时间。

如果不清楚，留空，不要编造。

### 4.4 Evidence Timeline

高影响 claim、pattern、decision 应维护证据时间线。

```yaml
evidence_timeline:
  - date: 2026-05-26
    source: "[[source-node]]"
    observation: "What was observed."
    effect: supports | contradicts | refines | replaces | weakens
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

### 5.1 关系边格式

```yaml
relations:
  - target: "[[node-name]]"
    type: supports | contradicts | refines | replaces | implements | applies_to | derived_from | inspired_by | risk_of | alternative_to | blocked_by
    strength: 1
    confidence: low
    evidence:
      - "[[source-or-claim]]"
    rationale: "One sentence explaining why this edge exists."
    created: 2026-05-26
    last_verified: 2026-05-26
```

### 5.2 关系类型

| type | 含义 |
|---|---|
| `supports` | 当前节点支持目标节点。 |
| `contradicts` | 当前节点反驳或冲突于目标节点。 |
| `refines` | 当前节点细化目标节点。 |
| `replaces` | 当前节点替代目标节点。 |
| `implements` | 当前节点实现目标节点。 |
| `applies_to` | 当前节点适用于某项目、场景或问题。 |
| `derived_from` | 当前节点从某来源、摘要或主张提炼而来。 |
| `inspired_by` | 当前节点受某来源启发，但不是严格证据推导。 |
| `risk_of` | 当前节点指出目标节点可能产生的风险。 |
| `alternative_to` | 当前节点是目标节点的替代方案。 |
| `blocked_by` | 当前节点受目标节点阻塞。 |

### 5.3 Strength

`strength` 表示语义关系强度，范围 `1-5`。

| strength | 含义 |
|---|---|
| `1` | 弱相关，只是背景线索。 |
| `2` | 有相关性，但证据较弱。 |
| `3` | 明确相关，可用于上下文召回。 |
| `4` | 强相关，应进入分析或 context pack。 |
| `5` | 核心关系，影响 claim/pattern/decision 判断。 |

规则：

- `strength >= 4` 必须有 `evidence` 和 `rationale`。
- `contradicts`、`risk_of`、`replaces` 不得省略 `rationale`。
- 无证据的强边应被 health check 标记。
- 双向关系需要两条边分别记录，不默认自动互逆。

### 5.4 派生分数

程序未来可以从主记录派生：

- source overlap
- common neighbor
- type affinity
- vector similarity
- graph score
- context pack ranking

但这些都是派生分数，不能写回替代人工记录的 `relations`。

## 6. Node Contracts

### 6.1 Source

最小 frontmatter。Source 的重点是 provenance，不是验证结论：

```yaml
type: source
status: source-captured
title:
source_url:
source_type:
captured_at:
captured_by:
raw_location:
processing_mode: inbox | immediate
review_priority: normal
review_owner: Codex
formalization_status: raw-only
topics:
projects:
verification_status: unverified
relations: []
tags:
```

可选字段：

```yaml
author:
publisher:
published_at:
source_quality:
freshness:
relevance:
confidence:
cross_source_count:
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
- 与 decision 相关的 anti-pattern 应通过 `risk_of` 或 `blocked_by` 连接。

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
superseded_by:
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
- daily brief 和 weekly synthesis 只能写入 `outputs/review/` 或 `outputs/qa/`，不能直接写入 formal wiki truth layer。
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

Review 队列不是 truth layer。候选内容只有在通过 Codex/用户复核并迁移到 `wiki/claims/`、`wiki/patterns/`、`wiki/anti-patterns/` 或 `wiki/decisions/` 后，才算正式知识节点。

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

### 9.2 健康检查输出

健康检查应输出：

```text
missing-required-fields
unsupported-claims
stale-decisions
conflicted-nodes
orphan-high-impact-nodes
weak-relations
missing-negative-evidence
review-due
```

### 9.3 不做事项

health check 不得在 v0.1 自动：

- 改写正文结论
- 替换旧节点
- 自动解决冲突
- 批量生成关系边
- 把向量相似度当作证据

## 10. Context Pack

Context pack 是调用层输出，不是新的 truth layer。

未来 `POST /context-pack` 或脚本生成的 context pack 应包含：

```yaml
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
```

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

Dev context pack 是 operation record，不是 formal truth node。

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
