---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
source_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source.md
derived_from:
  - raw/articles/2026-08-02-opus-5-obsidian-research-system-source.md
  - raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
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
  - research-workflow-design
  - model-routing-evaluation
  - review-queue
  - weekly-digest
  - temporal-scope-review
  - outcome-calibration
  - mcp-write-risk
possible_project_refs:
  - verified-action-knowledge-system
source_annotation_refs:
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/workload-shaped-model-routing.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/protocol-review-boundary-gap.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/weekly-digest-bounded-pointer.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/contradiction-review-and-audit-gap.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/direct-vault-write-mcp-risk.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/topic-scope-before-ingest.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/outcome-calibration-manual-first.md
point_anchor_refs:
  - "pasted-text.txt:3-9"
  - "pasted-text.txt:28-48"
  - "pasted-text.txt:59-80"
  - "pasted-text.txt:88-95"
  - "pasted-text.txt:103-107"
  - "pasted-text.txt:108-121"
  - "pasted-text.txt:122-131"
related_prior_distillation:
  - outputs/review/2026-06-06-x-damidefi-obsidian-claude-research-stack-candidate-distillation.md
  - raw/articles/2026-05-27-automated-obsidian-daily-brief-source.md
  - raw/articles/2026-05-27-jarvis-obsidian-claude-code-source.md
  - wiki/summaries/2026-05-obsidian-claude-ai-superbrain-content-factory.md
related_patterns:
  - wiki/patterns/claude-md-index-md-navigation-layer.md
  - wiki/patterns/operational-session-capture-loop.md
  - wiki/patterns/agent-tool-access-tiering.md
  - outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
  - outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
  - outputs/review/candidate_pattern_bank/simple-first-retrieval-baseline.md
verification_status: partially_verified
candidate_reliability_note: "Medium for workflow mechanisms; high for model identity and listed official pricing; low for the inference that Opus 5 is the correct VAKS default and for claimed weekly time savings."
borrow_value: medium_incremental
borrow_order: P2_support
candidate_pattern_bank: no_new_entry
avoid:
  - "Do not treat processed wiki notes as reviewed or trustworthy merely because a model created them."
  - "Do not add /raw, /wiki, /questions, and /digests as a new formal VAKS lane structure."
  - "Do not hard-code Opus 5/Fable 5 routing without representative local evaluation."
  - "Do not install Local REST API, grant full-vault write access, or schedule unattended writes from this source alone."
  - "Do not silently overwrite or delete prior judgments when a contradiction appears."
  - "Do not treat a 500-word digest or time-saved estimate as coverage proof."
tags:
  - candidate
  - provisional
  - obsidian
  - research-workflow
  - outcome-calibration
  - mcp-risk
---

# 候选蒸馏：Opus 5 + Obsidian Research System

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

此次处理没有安装 Obsidian 插件、连接 MCP、创建定时任务、修改 reviewed wiki、生成正式 pattern，或把任何模型设为 VAKS 默认值。

## 一句话结论

这篇文章不是新的架构蓝图。它与已有 Dami-Defi research-stack 记录高度同构，适合做“重复强化 + 少量增量”的 medium candidate。

最值得留下的新增是：

```text
模型按任务形状路由，但必须用本地任务评测
未决问题持续进入 no-guessing 队列
摄入前先确定主题/项目作用域
digest 价值要用遗漏与实际查询使用来校准
```

最重要的修正是：

```text
文章：raw -> processed wiki -> trustworthy
VAKS：raw -> candidate -> calibration/review -> reviewed standing
```

## Source

```yaml
derived_from:
  - raw/articles/2026-08-02-opus-5-obsidian-research-system-source.md
  - raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
source_annotation_refs:
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/workload-shaped-model-routing.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/protocol-review-boundary-gap.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/weekly-digest-bounded-pointer.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/contradiction-review-and-audit-gap.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/direct-vault-write-mcp-risk.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/topic-scope-before-ingest.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/outcome-calibration-manual-first.md
```

## 来源与实体卫生

### 可确认

- Opus 5 与 Fable 是当前官方型号，文章列出的 API 价格与官方页面一致。
- Anthropic 把 Opus 5 定位为适合日常高频使用；官方还给出了相对 Opus 4.8 的 Frontier-Bench 结果。
- Harvey 确实报告了法律任务中的 26% 平均 token 降幅。
- Local REST API 插件确实提供本地 API/MCP 读写能力。

### 只能保留为候选

- 厂商 benchmark 和法律领域评估不能证明 Opus 5 在 VAKS 的锚点覆盖、遗漏率、冲突发现、纠错量或成本上最优。
- 文章没有作者、日期和 canonical URL；不能把它归因给现有 Dami 来源，也不能把高度相似当成独立证据收敛。
- “每周节省数小时”和“两分钟 digest”没有实验设计、遗漏记录或对照数据。

## 新颖度检查

| 主题 | 与既有记录关系 | 本次处理 |
|---|---|---|
| 单一 Markdown vault / 降低连接成本 | Dami 已覆盖 | 不另起 point |
| 查重、扩展旧笔记、建立连接 | Dami 已覆盖 | 仅保留协议完成检查的细化 |
| weekly synthesis | Dami 与 daily brief 已覆盖 | 保留 recent-delta + pointer 的细化 |
| 冲突暴露、不自动裁决 | Dami 已覆盖 | 保留时间/范围判断与审计缺口 |
| 先手动再自动化 | Dami 已覆盖 | 与 outcome calibration 合并 |
| REST/MCP 作为连接器 | 既有工具访问分层已覆盖 | 只保留权限风险注释 |
| 模型按工作负载路由 | 增量新增 | candidate，需本地评测 |
| 未决问题持续队列 | 增量新增 | 映射到现有 review queue，不加新 lane |
| 主题作用域先于摄入 | 增量新增 | 映射 Project Overlay/context scope |
| 漏项与实际查询使用度量 | 增量新增 | 优先借用到 Use Ledger/outcome calibration |

结论：`candidate_pattern_bank: no_new_entry`，`v0_2_13_trigger: no`。

## Candidate Points

### 1. workload_tiered_model_routing_requires_local_eval

Candidate point:

```text
高频、重复的提取/交叉引用/digest，与少量高风险深度综合，应分开评测和路由；默认档位由代表性任务验收决定，困难任务才升级。
```

Anchor: `pasted-text.txt:3-9`。

增量价值：文章正确区分 volume work 与 single-shot depth，但把外部 benchmark 直接推导为 VAKS 默认路由。可借的是“按任务形状评测”，不是具体品牌绑定。

最低评测维度：

```text
source-anchor coverage
significant omission rate
contradiction surfacing quality
human correction count
token/cost/latency
run-to-run stability
```

### 2. visible_protocol_file_as_ingestion_contract

Candidate point:

```text
根目录可见协议文件可以编码目录角色、查重、链接、冲突、未决问题路由，并把“确实检查已有材料”设为完成条件。
```

Anchor: `pasted-text.txt:28-48`。

适配到 VAKS：AGENTS/manual/template 可以承担协议可见性，但完成检查只能证明流程动作发生，不证明提取正确或知识已审核。

### 3. unresolved_questions_as_persistent_no_guessing_queue

Candidate point:

```text
现有材料无法回答的问题应持续保留，并在后续 digest/review 中重新暴露；模型不应猜答案。
```

Anchors: `pasted-text.txt:37-39`, `pasted-text.txt:70-71`。

适配方式：不新增正式 `/questions` lane；映射到现有 `missing_evidence`、`synthesis_needed` 或 contradiction review queue item，并保留 source anchor 与 scope。

### 4. weekly_digest_is_recent_delta_pointer

Candidate point:

```text
周报只覆盖最近增量，突出关键变化、冲突、未决问题和异常活跃主题，并以完整笔记链接为主体；它是导航指针，不是原文替代品。
```

Anchor: `pasted-text.txt:59-80`。

VAKS 边界：digest 是 activation/orientation artifact。长度上限可帮助注意力管理，但不能充当 coverage proof、review verdict 或 action basis。

### 5. contradiction_requires_human_temporal_scope_judgment

Candidate point:

```text
冲突出现后，人工应判断旧资料是否错误、现实是否已变化/被替代，或双方是否在不同适用范围内成立，并保留判断演化历史。
```

Anchor: `pasted-text.txt:88-95`。

这强化了 VAKS 的 Point Collision、Temporal Applicability 和 decision superseding 边界。文章示例“直接更新旧 note”仍然缺少旧判断保留、replacement link、review receipt 和下游 review_due。

### 6. topic_scope_precedes_ingest_and_cross_topic_links_are_explicit

Candidate point:

```text
多主题研究应在摄入前确定 topic/project scope；真正跨主题时显式记录连接，默认按作用域生成 digest，只有完全不希望交叉召回时才考虑分 vault。
```

Anchor: `pasted-text.txt:108-121`。

适配方式：作用域是 retrieval/context/applicability 约束，不是真值边界。文件夹或 vault 划分只是实现选择，不自动建立 reviewed relation，也不应成为新的 VAKS 模块树。

### 7. research_system_value_needs_coverage_and_use_metrics

Candidate point:

```text
研究系统不能只报告摘要节省了多少分钟；还应记录重要项是否漏掉、人工纠错、跨来源查询是否被实际使用、成本和运行稳定性。
```

Anchor: `pasted-text.txt:122-131`。

这是本文最值得保留的增量点。可进入 Use Ledger / decision outcome calibration，但反馈只改善激活、实用性和适用范围判断，不能直接修改 truth confidence。

## 核心碰撞与融合

### 1. Processed Is Not Reviewed

文章将 `/wiki` 描述为 processed and trustworthy。VAKS 必须拆开：

```text
processed = 模型已加工
candidate = 可供理解和路由
reviewed = 已经通过证据、冲突、范围和风险审查
```

因此自动流程最多写 raw/candidate/review input；不能直接扩写 reviewed notes、创建 reviewed relations 或改变 truth confidence。

### 2. Updating Is Not Superseding

文章的“直接更新旧 note”没有表达：

```text
旧判断保留
replacement/supersedes link
变更理由
影响的下游内容
review_due
```

VAKS 若借用冲突流程，必须保留认识演化，而不是把历史改成看似从未犯错的静态文本。

### 3. Direct Write Is A Separate Authority Decision

Local REST API/MCP 的实际工具表面包括读、写、append、patch、delete、move 和 command execute。文章把“能列文件”当成连接成功测试，但这不能证明权限最小化、写入安全或无人值守可接受。

任何未来 pilot 至少需要：

```text
candidate/output path scope
minimal tool allowlist
API key isolation
prompt-injection boundary
backup and rollback
operation preflight and receipt
explicit user trigger/approval
no direct reviewed-wiki writes
```

### 4. Digest Is A Pointer, Not Coverage

recent-delta 和 500-word budget 值得借用，但只能降低注意力成本。Coverage 需要独立记录 known support、known counterevidence、known gaps、known conflicts 和重要遗漏；短并不等于完整。

## 借用顺序

### P1：最值得进入后续设计讨论

- 用遗漏、纠错、实际查询使用、成本和稳定性做 outcome calibration。
- 冲突进入人工的时间、版本、作用域判断，并保留 supersede/audit 历史。
- 未决问题进入现有 review queue，不猜测、不丢失。

### P2：作为支持性机制

- recent-delta bounded digest 作为 activation pointer。
- 可见协议文件与“已查重”完成检查。
- ingestion 前的 topic/project scope。
- manual-first 两到三周，收集真实遗漏和纠错，再讨论自动化。

### P3：满足条件后再看

- 在代表性 VAKS 任务上比较模型路由。
- 设计 path-scoped MCP/REST candidate-writer pilot。
- scheduled ingestion/digest。

## 明确不借

```text
raw -> automatically trusted wiki
直接覆盖旧判断
无人值守 full-vault write
从一次 list-files 成功推导连接安全
把厂商/法律 benchmark 当 VAKS 默认模型证据
把 500 字 digest 当遗漏证明
把“节省数小时”当已验证 outcome
把 /raw /wiki /questions /digests 原样复制成新正式 lane
```

## Open Questions

1. 什么是“genuinely new claim”？没有 claim identity、source anchor 和 scope/version 时，自动扩写会不会把多来源混成无出处文本？
2. 如何记录一个 raw file 是否已处理、用哪个协议版本处理、重跑是否幂等、差异是什么？
3. VAKS 的代表性模型评测集应如何覆盖锚点忠实、遗漏、冲突、scope 和 digest 任务？
4. 什么阈值说明应分 vault，而不是 Project Overlay、scope field 或 retrieval filter？
5. “重要内容没被埋掉”怎样形成可检查的 omission/coverage receipt，而不是靠事后偶然发现？
6. 若未来连接 Local REST API/MCP，最小可用的路径和工具权限是什么？

## Routing Hint

```yaml
default_layer: support_with_required_risk
use_for:
  - outcome-calibration design
  - review-queue open-question handling
  - bounded weekly digest design
  - topic/project scope controls
  - representative model-routing evaluation
risk_when:
  - processed notes are treated as reviewed knowledge
  - direct write access is treated as harmless plumbing
  - scheduled output is treated as coverage or action basis
  - vendor benchmarks select the default model without local evaluation
```

## Not Promoted

This note does not promote the source to reviewed knowledge, evidence support, a formal pattern, a VAKS decision, or action basis.

