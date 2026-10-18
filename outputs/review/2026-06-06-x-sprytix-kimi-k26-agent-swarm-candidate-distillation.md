---
type: article_candidate_distillation
status: candidate_only
created_at: 2026-06-06
source_record: raw/articles/2026-06-06-x-sprytix-kimi-k26-agent-swarm-source.md
source_type: x_post_pasted_text
raw_text_location: raw/articles/2026-06-06-x-sprytix-kimi-k26-agent-swarm-source/pasted-text.txt
verification_sources:
  - https://www.kimi.com/help/agent/agent-swarm
  - https://www.kimi.com/help/agent/agent-overview
  - https://www.kimi.com/help/agent/use-skills-in-agent
  - https://www.kimi.com/blog/kimi-k2-6
truth_boundary: candidate distillation only; not reviewed knowledge; not architecture decision; not action basis
review_priority: medium
projects:
  - verified-action-knowledge-system
tags:
  - kimi
  - agent-swarm
  - parallel-research
  - procedural-memory
  - candidate-only
---

# Kimi K2.6 Agent Swarm Candidate Distillation

## 一句话人话结论

这条材料对 VAKS 有帮助，但帮助点不是“300 个 agent 很厉害，所以我们也要上 swarm”。

真正可借的是：

```text
把天然可并行的资料侦察任务拆开跑，
每个 worker 留下可追溯 notebook / source anchors，
最后由 coordinator 汇总成候选包，
再交给 VAKS review gate。
```

它不能借成：

```text
agent 数量越多越可信
自动汇总报告就是 reviewed knowledge
Document to Skill 就是领域 truth
```

## 这条帖子的核心主张

帖子的主张可以拆成五点：

1. Kimi K2.6 Agent Swarm 可以自动把目标拆成大量并行调查。
2. K2.6 相比 K2.5 把并行 agent 数从 100 提到 300，步骤 / tool calls 从约 1500 提到 4000+。
3. 输出不是单条聊天回复，而是报告、表格、PPT、dashboard 等文件化交付物。
4. Document to Skill 可以把 PDF、DOCX、表格或演示文稿转为可复用 skill。
5. 这能显著缩短市场研究、竞品监控、内容变体生成等任务。

官方 Kimi 文档支持其中的产品能力主干：

```text
300 sub-agents
4000+ tool calls
Agent Swarm beta
file / document / spreadsheet / presentation deliverables
Office Document to Skill
```

但帖子的 ROI 估算、成本替代、具体市场研究质量，仍然只是营销主张。

## 候选提炼

### 1. parallel_agent_scouting_as_candidate_research

候选理解：

```text
VAKS 可以把大规模外部资料侦察拆成并行 worker：
每个 worker 只负责一个来源集合、一个关键词族、一个竞品、一个论文簇或一个反例方向。
```

适合场景：

```text
paper scouting
repo/source discovery
competitor/reference scan
known omission check
coverage gap hunting
counterevidence search
```

边界：

```text
worker output = raw source / candidate point / missing evidence / review question
not reviewed claim
not reviewed relation
not action basis
```

### 2. orchestrator_decomposition_needs_trace

候选理解：

```text
自动拆解很有用，但 VAKS 不能接受黑盒拆解。
如果 coordinator 自动决定怎么分工，必须留下 decomposition trace。
```

VAKS 最小需要：

```text
goal
worker scope
source query / source set
collected anchors
what was skipped
worker uncertainty
aggregation rule
coordinator synthesis warrant
```

边界：

```text
没有拆解轨迹的 swarm report 只能当普通候选摘要。
```

### 3. document_to_skill_as_procedural_memory

候选理解：

```text
Document to Skill 不是把文档变成 truth。
更像把一套格式、流程、评估方法、写作风格或操作规程变成可复用 procedural memory。
```

对 VAKS 的用法：

```text
source-review playbook
paper-scouting checklist
market-research template
evidence-packet drafting routine
context-pack assembly routine
```

边界：

```text
Skill 可以指导怎么做。
Skill 不能决定什么是真的。
Skill 更新也不能直接改 reviewed knowledge。
```

### 4. file_deliverables_are_review_inputs

候选理解：

```text
Agent Swarm 输出报告、表格、PPT、dashboard 的能力，适合 VAKS 的 outputs/review 层。
```

可借：

```text
让多 agent 产出结构化候选包
让候选包包含 source anchors、coverage map、gaps、risk flags
让 reviewer 从文件而不是聊天记录里复核
```

不可借：

```text
报告好看 = 证据充分
表格很多 = 结论可信
PPT 成熟 = action-ready
dashboard 指标 = truth
```

### 5. parallelism_improves_coverage_not_confidence

候选理解：

```text
并行 agent 的主要收益是覆盖面和速度，不是 truth confidence。
```

VAKS 解释：

```text
300 个 agent 可以更快找到 300 个候选线索。
但如果它们用同一个模型、同一套搜索、同一类来源和同一个 aggregation prompt，
它们不是 300 份独立证据。
```

边界：

```text
parallel breadth may raise review pressure or coverage confidence.
It cannot directly raise truth confidence.
```

### 6. context_sharding_for_large_evidence_collection

候选理解：

```text
官方 Agent Swarm 文档里的 context sharding 思路，适合 VAKS 大规模 evidence collection。
每个 worker 有自己的 notebook，只上报关键结论给 coordinator。
```

VAKS 需要补的纪律：

```text
notebook retained
source anchors retained
known misses retained
aggregation summary links back to worker notes
```

边界：

```text
只保留最终 synthesis 会丢失 provenance。
```

## 对 VAKS 的采用判断

当前判断：

```text
watch_for_candidate_research_lane
use_as_parallel_scouting_reference
do_not_promote_to_truth_core
do_not_add_mainline_mechanism_yet
```

可立即吸收为说法：

```text
并行 agent 适合做 candidate discovery / coverage scan。
review 仍然要回到 evidence packet / support-challenge review。
```

暂不做：

```text
不新增 VAKS swarm runtime。
不改主架构。
不把 Kimi Agent Swarm 变成默认 intake 方式。
不把 Document to Skill 变成知识晋级机制。
```

## 风险和反模式

### swarm_as_authority

```text
用 agent 数量、tool call 数或输出文件数量证明结论可靠。
```

VAKS 处理：

```text
数量只能说明覆盖或成本，不说明 support。
```

### hidden_decomposition

```text
系统自动拆解，但 reviewer 看不到每个 worker 查了什么、漏了什么、怎么汇总。
```

VAKS 处理：

```text
没有 worker trace，不进 review-ready。
```

### synthetic_consensus

```text
多个 agent 得出一致意见，但它们共享模型、prompt、搜索偏差或来源集合。
```

VAKS 处理：

```text
一致意见是 review signal，不是 independent evidence。
```

### auto_ingest_to_truth

```text
Deep Research 或 Agent Swarm 自动把网页结果写成知识结论。
```

VAKS 处理：

```text
自动 ingest 只能进 raw / candidate / review queue。
```

## 最小可试方向

如果未来要试，不从 300 agent 开始。

最小试法：

```text
3-5 个 worker
每个 worker 一个明确 source scope
每个 worker 产出 source anchors + candidate points + uncertainty
coordinator 只产出 review packet
reviewer 决定是否晋级
```

成功标准：

```text
找到更多可核查 source anchors
暴露更多 known gaps / counterevidence
减少人工侦察时间
不增加 truth pollution
```

## 结论

```text
有用，但只放候选研究 / scouting / procedural memory 层。
不进入 truth core。
不改变 VAKS 主架构。
```
