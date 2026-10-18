---
type: candidate_general_pattern
record_kind: candidate_general_pattern
status: candidate
title: "AI Reverse Toolkit: 通用 AI 专家流程编码模式"
source_ref: "raw/repos/2026-06-11-zhizhuodemao-ai-reverse-toolkit-source.md"
source_id: "github:zhizhuodemao/ai-reverse-toolkit@02799de7420ea78c57bf7af8cc0f2d38fef017bd"
created_at: "2026-06-11"
created_by: Codex
processing_tier: heavy
knowledge_status: candidate
overlay_state: none
truth_status: not_reviewed
action_basis_allowed: false
truth_mutation_allowed: false
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_general_pattern_not_reviewed
promotion_gate: evidence_aware_review_required
borrow_value: strong
borrow_order:
  - "expert-workflow-as-skill"
  - "progressive-disclosure"
  - "diagnostic-loop"
  - "completion-standard"
  - "eval-driven-skill-improvement"
tags:
  - candidate
  - general-knowledge
  - ai/skill-workflow
  - workflow/diagnostic-loop
  - workflow/progressive-disclosure
  - workflow/eval-driven
---

# 通用候选模式：把专家流程编码成 AI Skill

## 说人话

这个库最通用的价值不是逆向工程，而是：

```text
把一个专家脑子里的流程，拆成 AI 能执行、能停、能查证、能复盘的步骤。
```

它的核心套路可以脱离逆向工程，迁移到任何复杂知识工作。

## 通用结构

```text
1. trigger boundary
   什么时候该用这个 skill，什么时候不该用。

2. task scope
   这个 skill 只解决哪一段，不顺手越界。

3. strategy selection
   根据现场信号选策略，而不是死板流水线。

4. domain knowledge
   把专家才知道的坑、常见结构、反模式写进去。

5. diagnostic loop
   每轮读报告，按错误类型进入下一步。

6. reference lookup
   主 skill 不塞满所有细节，遇到场景再读 reference。

7. completion standard
   明确做到什么就停。

8. intermediate artifacts
   中间产物可回退、可审计、可比较。

9. validation gate
   先验证形态，再验证结果；先验证小样本，再扩展。

10. evaluation loop
   skill 本身也要用测试、基线、评分、反馈迭代。
```

## 值得保留的通用原则

### 1. 工具和经验分层

源库的关键判断是：

```text
tool = hand
skill = brain
```

通用化后就是：

```text
工具负责执行动作。
skill 负责判断什么时候做什么动作。
```

这能防止 AI 拿到工具后乱跑。

### 2. 一个 skill 只做一个阶段

`find-crypto-entry` 的完成标准是只找到入口，不继续做算法还原。

通用化后就是：

```text
定位问题 != 解决问题
提取证据 != 做决策
构建候选包 != 变成行动依据
```

这和 VAKS 的层级边界高度一致。

### 3. 反模式要写进流程

这个库把反模式写得很具体，例如不要盲目单步、不要在错误位置搜索、不要频繁刷新导致状态失效。

通用化后：

```text
一个好 skill 不只告诉 AI 做什么，
还要告诉 AI 哪些看似勤奋的动作其实会浪费时间或破坏证据。
```

### 4. 诊断树优于一口气自动化

`env-patch` 的强点是诊断循环：

```text
ERRORS -> 先修
UNDEFINED -> 查浏览器真实值
HANG -> 查卡死原因
格式不一致 -> 不要被 HTTP 200 骗
到达天花板 -> 读 limitations
```

通用化后：

```text
先分类失败，再选下一步。
不要把失败隐藏成“继续自动重试”。
```

### 5. Progressive Disclosure

主 skill 只保留流程骨架，具体场景放到 references。

通用化后：

```text
常用路径短。
复杂细节按需加载。
上下文不被参考资料淹没。
```

这对 VAKS 很重要，因为 VAKS 的严格 review、evidence packet、context pack 都不该压到每次普通查询里。

### 6. 中间产物是安全网

`ast-deobfuscate` 强调中间文件、逐步转换、可回退、保留不确定代码。

通用化后：

```text
每一步都要留下可回看的状态。
不确定的东西保留，不要为了“看起来完成”而强行改写。
```

这可以直接迁移到 VAKS 的 source intake、candidate distillation、review queue。

### 7. Skill 自己也要评测

`skill-creator` 的核心是：

```text
写 skill
跑测试 prompt
跑有 skill 和无 skill 的 baseline
写 assertions
评分
看人类反馈
迭代
```

通用化后：

```text
流程不是写完就可信。
流程要被真实任务检验。
```

## 不要保留为通用知识的部分

```text
签名绕过细节
反调试对抗代码
补环境绕风控步骤
还原闭源实现的操作路线
可直接用于规避平台保护的流程
```

这些不进入 VAKS 通用知识层，只作为源库存在过的安全风险背景。

## 可迁移到 VAKS 的通用模板

```text
VAKS Skill Template:

1. Trigger:
   用户说什么时触发；什么时候不触发。

2. Scope:
   只做本阶段，不顺手升级为 review/action。

3. Inputs:
   需要的文件、来源、查询、目标。

4. Strategy:
   根据输入信号选路径。

5. Artifacts:
   每步输出什么文件或记录。

6. Diagnostics:
   常见失败怎么分类。

7. Boundaries:
   什么不能当 truth/support/action basis。

8. Completion:
   做到什么就停，下一阶段另开 gate。

9. Eval:
   用什么小样本判断这个 skill 真有帮助。
```

## 候选结论

```yaml
candidate_pattern_name: expert_workflow_as_ai_skill
borrow_value: strong
general_reuse: high
vaks_fit: strong
promotion_ready: no
needs_review_for:
  - how VAKS should define skill evals
  - how skill outputs enter review queue
  - how to prevent workflow skills from mutating truth
```
