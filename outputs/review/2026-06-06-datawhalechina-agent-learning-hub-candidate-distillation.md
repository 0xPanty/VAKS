---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/repos/2026-06-06-datawhalechina-agent-learning-hub-source.md
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
  - agent-gateway
  - skill-packaging
  - misa-vaks-integration
  - evaluation-safety
  - source-intake
possible_project_refs:
  - verified-action-knowledge-system
  - misa
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/datawhalechina-Agent-Learning-Hub-d7967513ace303618ac2e37732468f6e127e4de1.zip
    selector_type: markdown
    selector_value: README.md:34-59
  - snapshot_ref: raw/repos/_snapshots/datawhalechina-Agent-Learning-Hub-d7967513ace303618ac2e37732468f6e127e4de1.zip
    selector_type: markdown
    selector_value: README.md:92-156
  - snapshot_ref: raw/repos/_snapshots/datawhalechina-Agent-Learning-Hub-d7967513ace303618ac2e37732468f6e127e4de1.zip
    selector_type: markdown
    selector_value: README.md:175-218
  - snapshot_ref: raw/repos/_snapshots/datawhalechina-Agent-Learning-Hub-d7967513ace303618ac2e37732468f6e127e4de1.zip
    selector_type: html
    selector_value: index.html:634-917
tags:
  - candidate
  - provisional
  - agent-learning-hub
  - datawhale
  - hermes
  - skills
  - evaluation
---

# Agent Learning Hub Candidate Distillation

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## Source

```yaml
derived_from:
  - raw/repos/2026-06-06-datawhalechina-agent-learning-hub-source.md
checked_commit: d7967513ace303618ac2e37732468f6e127e4de1
snapshot: raw/repos/_snapshots/datawhalechina-Agent-Learning-Hub-d7967513ace303618ac2e37732468f6e127e4de1.zip
snapshot_sha256: 8FA4BFE8D9FEA4854AEE1C09959777F9D5D318AC9856142D0CE3D921390593C5
```

## 人话压缩

这个源最值得压榨成一句话：

```text
别一上来就说“接入 agent”。
先问为什么需要 agent，
再证明最小 loop 能跑，
再补 permission / session / memory / trace / compaction，
再把重复流程做成 skill，
最后才谈 Hermes / OpenClaw 这种 personal agent gateway。
```

对 VAKS / MISA 的说人话版本：

```text
MISA 接资料库，不应该是 MISA 直接读写整个 vault。
它应该先像一个受控调用方：
提出上下文请求，
拿到带边界的 context pack，
把使用结果写成 feedback event，
需要写入候选材料时过 permission / review gate，
永远不能直接改 reviewed truth。
```

## Candidate Points

### 1. `agent-roadmap-as-integration-gate`

候选结论：Agent Learning Hub 的分阶段路线可以借来做 MISA-VAKS 接入成熟度检查。它不是告诉我们采用哪个框架，而是提醒接入要先过几个台阶。

锚点：

- `README.md:34-59`
- `README.md:92-113`
- `README.md:175-218`

对 VAKS / MISA 的适配：

```text
Stage 0: 为什么是 agent，不是 workflow/script？
Stage 1: 最小 tool loop 能不能稳定跑？
Stage 2: memory / retrieval / citation 是否分层？
Stage 3: permission / session / compaction / trace 是否有明确 owner？
Stage 5: 重复流程是否能包成 skill？
Stage 7: 是否有固定 eval / failure trace？
Stage 8: 是否能以真实任务定义 success standard？
```

边界：

```text
roadmap stage != reviewed maturity
progress checkbox != architecture readiness
```

Review question:

```text
MISA 第一次接 VAKS 时，应该卡在 read-only context provider，还是可以同时做 feedback-event writeback？
```

### 2. `workflow-before-agent-intent-check`

候选结论：Stage 0 先要求区分 agent、chatbot、workflow、multi-agent，这可以成为 VAKS/MISA 接入前的 intent confirmation：很多场景只需要一次 deterministic context-pack assembly，不需要 always-on agent。

锚点：

- `README.md:34-42`

对 VAKS / MISA 的适配：

- 用户问资料库问题：优先普通 retrieval/context pack。
- MISA 需要持续跟踪任务：才考虑 session/gateway。
- 需要自动执行文件或外部工具：必须进入 permission / action guardrail。

边界：

```text
intent confirmation != user approval to execute
workflow enough != no future agent value
```

### 3. `minimal-tool-loop-before-harness`

候选结论：在引入 MCP/A2A/ACP、Hermes gateway、long-term memory 之前，应先有一个最小可测 loop：输入任务、选择工具、执行工具、观察结果、停止或重试。

锚点：

- `README.md:44-59`

对 VAKS / MISA 的适配：

最小 loop 可以只做：

```text
context_request
-> VAKS read-only retrieval
-> context_pack_response
-> MISA answer/use
-> feedback_event draft
```

验收不看“像不像智能”，只看：

```text
是否有 max steps
是否有 timeout
是否有 structured output
是否有 failure reason
是否有 no-write boundary
```

边界：

```text
loop works != safe integration
tool output parsed != source support
```

### 4. `retrieval-memory-source-boundary`

候选结论：Stage 2 把 RAG、short-term context、session memory、long-term memory、source-backed answers 放在同一层学习，但这对 VAKS 来说必须拆清：activation/memory 可以帮 MISA 找上下文，只有 reviewed evidence / reviewed relation 才能支撑 action。

锚点：

- `README.md:61-90`

对 VAKS / MISA 的适配：

MISA 可读取：

```text
reviewed support
candidate orientation
raw source drilldown
known gaps
project overlay
feedback hints
```

MISA 不可把下面这些当成 truth：

```text
session memory
recent context
retrieval rank
community summary
agent summary
positive feedback
```

边界：

```text
memory helps activation
memory does not become truth
```

### 5. `harness-anatomy-checklist`

候选结论：Stage 3 对 modern coding-agent harness 的拆解非常适合变成 VAKS/MISA 接入检查表：agent loop、tool registry、permission gate、session store、context compaction、trace。

锚点：

- `README.md:92-113`

对 VAKS / MISA 的适配：

```text
agent loop: 谁决定继续/停止？
tool registry: MISA 能调用哪些 VAKS 操作？
permission gate: 哪些操作必须 human confirm？
session store: 对话/任务状态保存在哪里？
context compaction: 历史压缩是否带 provenance？
trace: 每次读取/写入/拒绝是否可回放？
```

边界：

```text
harness component exists != policy enforced
trace exists != reviewed support
```

### 6. `personal-agent-connector-map`

候选结论：OpenClaw/Hermes/CyberClaw 被放在 personal/always-on agent 类别里，这对 MISA 很贴：MISA 如果接 VAKS，应当被视为一个有 message gateway、memory、skills、permission 的长期 agent，而不是一次性脚本。

锚点：

- `README.md:242-254`
- `README.md:266-282`

对 VAKS / MISA 的适配：

建议把接入拆成：

```text
message gateway
-> intent classification
-> VAKS context request
-> context pack assembly
-> MISA reasoning/action
-> action/feedback trace
-> review_due if correction/conflict appears
```

边界：

```text
personal agent memory != vault truth
always-on != always-authorized
```

### 7. `skills-as-reusable-process-not-truth`

候选结论：Stage 5 把 skill 定义成可以复用的过程包：SKILL.md、使用时机、步骤、验收标准、脚本、模板、smoke test。这非常适合 VAKS/MISA，但必须保持“skill 管流程，不管真理”。

锚点：

- `README.md:133-156`

对 VAKS / MISA 的适配：

未来可以做的 skill：

```text
retrieve-vaks-context
draft-evidence-packet
record-feedback-event
prepare-source-intake
assemble-action-basis-candidate
compare-project-overlay
```

每个 skill 必须声明：

```text
allowed paths
write policy
authority boundary
acceptance checks
smoke test
failure mode
```

边界：

```text
skill output != reviewed knowledge
skill success != promotion
```

### 8. `protocol-separation-mcp-a2a-acp`

候选结论：Agent Learning Hub 对 MCP/A2A/ACP 的拆分可作为项目词汇表：MCP 偏工具/数据，A2A 偏 agent-agent，ACP 偏编辑器/终端/host app 与 agent。MISA 接 VAKS 不要笼统说“接入”，要明确是哪种边界。

锚点：

- `README.md:256-264`

对 VAKS / MISA 的适配：

```text
MISA 只读资料库上下文：更像 MCP/data tool boundary
MISA 与另一个 agent 协作：才像 A2A boundary
Codex/IDE/terminal host 调 MISA：才像 ACP boundary
```

边界：

```text
protocol label != security model
MCP exposed != reviewed write access
```

### 9. `eval-before-more-agents`

候选结论：Stage 7 把 eval 放在扩 agent 之前：固定任务、成功/失败、成本、延迟、工具调用次数、trace、dangerous tool confirmation、prompt injection/data exfiltration/tool abuse。这很适合做 MISA-VAKS connector 的上线门。

锚点：

- `README.md:175-192`
- `README.md:368-377`

对 VAKS / MISA 的适配：

最小 eval set 可以覆盖：

```text
普通查询只给候选/已审分层 context
高风险动作触发 action_basis warning
raw source 不被当成 support evidence
project overlay 不越权成 reviewed decision
feedback event 不改 truth confidence
explicit correction 创建 review_due
stale/superseded source 暴露 temporal warning
```

边界：

```text
eval pass != truth
LLM judge != reviewer
trace coverage != source support
```

### 10. `multi-agent-coordination-not-magic`

候选结论：Stage 4 明确 multi-agent 的核心是 supervisor/graph、roles、schemas、stopping conditions，以及避免 loop/drift/context bloat。这对 VAKS 的意义是：多 agent 只能帮助 scouting / coverage / comparison，不能替代 review。

锚点：

- `README.md:115-131`

对 VAKS / MISA 的适配：

如果未来 MISA 调多个 worker：

```text
每个 worker 留 source anchors
coordinator 留 merge/drop/conflict manifest
final output 只能进入 candidate/review input
高风险 action 仍要 human gate
```

边界：

```text
more agents != more truth
agreement != evidence support
```

### 11. `project-ladder-for-misa-vaks`

候选结论：Project Ladder 可以转成 MISA-VAKS 的接入台阶，不要直接从“资料库问答”跳到“production always-on personal agent”。

锚点：

- `README.md:204-218`

候选台阶：

```text
1. Read-only context request
2. Source drilldown with anchors
3. Candidate distillation draft
4. Review packet draft
5. Feedback-event writeback
6. Skill-pack wrapper
7. Gateway permission gate
8. Fixed eval / trace replay
9. Optional personal-agent loop
10. Production harness with rollback
```

边界：

```text
ladder is sequencing aid
not required product roadmap
```

### 12. `curated-resource-quality-bar`

候选结论：CONTRIBUTING 的质量标准可以借给 VAKS 外部源侦察：优先官方文档、论文、benchmark、可运行 repo、具体项目想法；避免广告、私有/付费/爬取内容、绕平台规则、链接堆。

锚点：

- `CONTRIBUTING.md:1-41`

对 VAKS 的适配：

```text
source scouting 可以并行
source card 必须具体
候选蒸馏必须有锚点
外部链接列表不能直接变成知识
```

边界：

```text
resource quality bar != evidence review
official source != automatically true
```

## 压榨后的 MISA 接入草图

最小安全说法：

```text
MISA 先接 VAKS 的 read-only activation layer。
它拿 context pack，不拿 truth mutation 权限。
它可以返回 feedback event / review pressure。
它不能直接改 wiki/claims、wiki/decisions、reviewed relations 或 truth confidence。
```

可候选接口：

```yaml
context_request:
  task: string
  project: misa
  requested_scope: hot|warm|cold|source_drilldown
  risk_level: low|medium|high
  max_authority_bucket: reviewed_only|reviewed_plus_candidate|raw_allowed

context_pack_response:
  reviewed_support: []
  candidate_orientation: []
  project_overlays: []
  raw_source_drilldown: []
  known_gaps: []
  warnings: []
  action_basis_allowed: false

feedback_event:
  context_pack_id: string
  usefulness: useful|partial|wrong_scope|missing|unsafe
  explicit_correction: string|null
  review_pressure: none|review_due
```

## Knowledge Calibration / Point Collision

| Candidate Point | Local Boundary | Calibration Output | Review Question |
|---|---|---|---|
| `agent-roadmap-as-integration-gate` | VAKS strict checks are lazy gates, not universal burden. | candidate_relation | Which MISA gate is worth testing first? |
| `retrieval-memory-source-boundary` | Activation Tier is hot/warm/cold, not truth tier. | refines | What fields should context pack expose so MISA cannot confuse activation with support? |
| `skills-as-reusable-process-not-truth` | Agent memory quarantine forbids direct reviewed truth mutation. | candidate_relation | Should VAKS create a MISA-facing skill pack before any MCP/API endpoint? |
| `eval-before-more-agents` | Tests/benchmarks are diagnostics, not authority. | refines | What 10-20 regression tasks define "MISA reads VAKS safely"? |
| `multi-agent-coordination-not-magic` | Approval integrity is process evidence, not evidence support. | risk_of | How do we prevent agent agreement from looking like review? |

边界：

- 相似不是支持。
- 排名不是证据。
- 学习路线不是 adoption decision。
- 校准输出是 review input，不是 reviewed relation。

## Support / Challenge Review

What supports it:

- The repo contains a concrete staged roadmap, project ladder, protocol vocabulary, and contribution quality bar.
- The roadmap explicitly emphasizes small reliable agents, strict schemas, evals, traces, permission gates, and human confirmation for risky actions.
- The project neighborhood includes Hermes/OpenClaw/CyberClaw, which matches the MISA integration concern.

What challenges it:

- The source is a curated guide, not an implementation.
- External links and resource claims were not independently verified in this intake.
- Current priorities and project statuses may drift quickly.
- The guide's usefulness for MISA is indirect: it informs integration design, not runtime code.

Challenge severity:

```text
major for direct adoption
minor for design-only extraction
```

Scope limits:

- Useful for MISA-VAKS integration planning, skill packaging, eval gates, and source scouting quality.
- Not a VAKS architecture replacement.
- Not a reviewed standard for MCP/A2A/ACP semantics.
- Not enough to authorize write access from MISA to reviewed knowledge.

Known risks:

- Turning a learning checklist into a mandatory architecture ceremony.
- Mistaking protocol names for permission models.
- Letting "personal agent" imply always-authorized background action.
- Treating localStorage progress or eval pass as knowledge status.
- Using the linked resource list as proof without source-specific review.

## Suggested Handling

```text
keep_as_candidate_distillation
use_for_misa_overlay
use_as_future_source_queue_seed
no_mainline_writeback_now
no_reviewed_pattern_now
```

Reopen when:

- User asks to design or implement a MISA-VAKS connector.
- User asks for a VAKS-facing skill pack for MISA.
- User asks to compare Hermes/OpenClaw/CyberClaw/Claude Code style gateways.
- User asks to build evals for agent access to the vault.
