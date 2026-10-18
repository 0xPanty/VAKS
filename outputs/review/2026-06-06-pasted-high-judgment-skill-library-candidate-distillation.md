---
type: article_candidate_distillation
status: candidate_only
created_at: 2026-06-06
source_record: raw/articles/2026-06-06-pasted-high-judgment-skill-library-source.md
source_type: pasted_article
raw_text_location: raw/articles/2026-06-06-pasted-high-judgment-skill-library-source/pasted-text.txt
truth_boundary: candidate distillation only; not reviewed knowledge; not architecture decision; not action basis
review_priority: medium
projects:
  - verified-action-knowledge-system
related_existing_records:
  - wiki/patterns/skills-as-action-modules.md
  - wiki/patterns/artifact-trigger-and-body-alignment-eval.md
  - wiki/patterns/skill-artifact-iteration-workspace-rollback.md
tags:
  - skill-library
  - procedural-memory
  - high-judgment-work
  - candidate-only
---

# High-Judgment Skill Library Candidate Distillation

## 一句话人话结论

这篇文章对 VAKS 有用，因为它把 skill library 从“prompt 文件夹”拉回到“可继承的判断流程”。

它最值得借的一句话是：

```text
Skill 不该先记录轻任务怎么写。
Skill 应该先记录高判断任务里：先看什么、信谁、哪里停、错了怎么修。
```

对 VAKS 来说，这属于 agent procedural memory / runtime workbench 候选，不是 reviewed truth。

## 文章的核心判断

文章反对从轻量 prompt collection 开始建 skill library。

它认为轻任务已经能被现代 agent 做到不错的一稿，例如：

```text
rewrite report
summarize meeting minutes
categorize emails
polish paragraph
```

真正值得做成 skill 的是：

```text
重复发生
流程相似
关键节点需要判断
错误代价高
需要资深人员兜底
需要明确 stop rules
```

例子：

```text
PRD review
launch QA
support escalation
code review
brand voice review
sales call prep
customer feedback handling
```

## 候选提炼

### 1. high_judgment_work_first_for_skill_library

候选理解：

```text
第一批 skill 应从“重复 + 高判断 + 高风险/高成本”的 workflow 里选，而不是从最容易整理的 prompt 里选。
```

对 VAKS 的意义：

```text
未来 VAKS skill library 如果要建，优先从 source review、evidence packet、context pack、feedback triage、action guardrail 这些高判断流程开始。
```

边界：

```text
选择 skill 的标准不是使用频率 alone，而是频率 + 判断密度 + 错误代价。
```

### 2. skill_library_as_sequence_of_judgment

候选理解：

```text
Skill library 保存的是 sequence of judgment：
先查什么、信哪个状态源、遇到冲突怎么处理、何时停下问人、失败后怎么修规则。
```

对 VAKS 的意义：

```text
这和 VAKS 的 review gate / action guardrails / source-of-truth discipline 高度兼容。
```

边界：

```text
Skill 可以封装判断流程。
Skill 不能封装最终真值。
```

### 3. failure_records_over_prompt_collections

候选理解：

```text
失败记录比成功 prompt 更值得沉淀。
```

文章给的失败类型可以泛化为：

```text
phase changed but old rule kept applying
materials conflicted and model copied stale reference
feedback was ambiguous and agent over-corrected
old project preference polluted current project
```

对 VAKS 的意义：

```text
这可以补强 Use Ledger / feedback-event：
失败不是只写“用户不满意”，而要写成可修 skill 的 failure mode。
```

边界：

```text
failure mode 进入 skill maintenance，不直接改 reviewed knowledge。
```

### 4. skill_map_boundaries_state_routing_maintenance

候选理解：

文章提出 skill library 五层：

```text
Skill Map:
  按 workflow 组织，不按 tool 组织。

Boundaries:
  每个 skill 知道何时进入、何时退出、拥有什么、不拥有什么。

State Source:
  每个跨天/跨版本/跨文件任务必须知道当前 source of truth。

Routing:
  先匹配入口，再渐进加载 full skill 和 deeper references。

Maintenance:
  触发失败修 description，误触发收窄 boundary，引用旧状态修 source of truth，重复错误加 failure mode。
```

对 VAKS 的意义：

```text
这可以作为未来 agent skill registry / procedural memory 的候选组织法。
```

边界：

```text
它是 runtime organization，不是 VAKS truth architecture。
```

### 5. state_source_before_action

候选理解：

```text
每个 skill 在执行前应知道当前状态源：
当前版本、锁定内容、待定事项、上次为什么改、哪些方向已被否决。
```

对 VAKS 的意义：

```text
这对应 DEV_CONTEXT / handoff / context pack：
agent 不应从旧聊天、旧偏好或旧项目残影里行动。
```

边界：

```text
state source 是 activation/action context，不是自动 truth confidence。
```

### 6. progressive_disclosure_for_skills

候选理解：

```text
不要把所有 skill 和历史资料一次性塞进 context。
Skill library 应该像接待台：先判断任务类型，再加载对应 skill，必要时再加载 references / failure modes / state source。
```

对 VAKS 的意义：

```text
这和 Activation Tier、Association Neighborhood Activation、DEV_CONTEXT 分层一致。
```

边界：

```text
路由决定读什么，不决定信什么。
```

### 7. trigger_eval_for_skill_maintenance

候选理解：

```text
每个 skill 应有 should-trigger / should-not-trigger 小测试。
漏触发修入口描述，误触发收窄边界。
```

对 VAKS 的意义：

```text
这和已有 artifact-trigger-and-body-alignment-eval 可合并观察。
Skill 维护可以用轻量 trigger eval，而不是等真实任务出事故。
```

边界：

```text
trigger eval 是维护诊断，不是 skill correctness 或 truth。
```

## 与现有 VAKS 记录的关系

已有：

```text
skills-as-action-modules:
  skill 可以表达重复工作流。

artifact-trigger-and-body-alignment-eval:
  skill 需要 trigger accuracy / body alignment 检查。

skill-artifact-iteration-workspace-rollback:
  generated skills 需要版本、diff、rollback。

langchain-miniopenclaw review:
  SKILL.md / prompt / memory 可见化有利于复盘，但需要 quarantine。
```

这篇新增的不是“skill 可以做什么”，而是：

```text
哪些 skill 值得先做
skill library 如何分层
如何避免 prompt warehouse
如何从 failure records 维护 skill
```

## VAKS 采用判断

当前判断：

```text
watch_as_skill_library_selection_and_maintenance_reference
candidate_only
no_mainline_architecture_change
```

可立即吸收为操作口径：

```text
未来做 VAKS skill，不从轻 prompt 开始；
从 source review / evidence packet / context pack / feedback triage / action guardrail 这些高判断流程开始。
```

暂不做：

```text
不新增正式 Skill Library 模块。
不改 AGENTS.md。
不把文章方法写成主架构规则。
不自动创建 VAKS skills。
```

## 结论

```text
high_signal_for_future_agent_procedural_memory
not_truth_core
use_for_future_skill_registry_design
```
