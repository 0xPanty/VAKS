---
type: candidate_distillation
record_kind: candidate_distillation
status: candidate
title: "zhizhuodemao/ai-reverse-toolkit candidate distillation for VAKS"
source_ref: "raw/repos/2026-06-11-zhizhuodemao-ai-reverse-toolkit-source.md"
source_id: "github:zhizhuodemao/ai-reverse-toolkit@02799de7420ea78c57bf7af8cc0f2d38fef017bd"
source_uri: "https://github.com/zhizhuodemao/ai-reverse-toolkit"
created_at: "2026-06-11"
created_by: Codex
processing_tier: heavy
knowledge_status: candidate
overlay_state: none
truth_status: not_reviewed
evidence_status: source_files_inspected_not_executed
action_basis_allowed: false
truth_mutation_allowed: false
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
borrow_value: strong
borrow_order:
  - "VAKS skill/workflow design"
  - "black-box analysis workflow"
  - "retrieval/query-run diagnostics"
  - "context-pack builder skill evaluation"
  - "security-specific tactics excluded"
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "VAKS is designing AI-executable workflows, black-box product analysis, retrieval diagnostics, or skill evaluation."
  support_when: "The task is about structuring agent workflows, progressive disclosure, diagnostic loops, completion standards, or evals."
  risk_when: "A proposal imports security bypass tactics, private-code extraction, or lets a workflow output become reviewed truth."
  cold_references:
    - "JS-specific signing, anti-debug, and env-patch details"
    - "platform-specific reverse-engineering tactics"
routing_hint:
  - ai-skill-design
  - source-intake-workflow
  - blackbox-product-analysis
  - retrieval-diagnostics
  - context-pack-evaluation
tags:
  - candidate
  - ai/skill-workflow
  - vaks/process-inspiration
  - vaks/retrieval-diagnostics
  - vaks/source-intake
  - risk/security-bypass-excluded
  - boundary/not-action-basis
provisional: true
---

# ai-reverse-toolkit Candidate Distillation

## 一句话

`ai-reverse-toolkit` 对 VAKS 最有价值的不是“逆向技术”，而是：

```text
把复杂专家流程做成 AI 可执行 skill。
```

说人话：它教 AI 不要瞎猜，而是按阶段查、按错误分流、按证据收口。这个思路和 VAKS 非常像。

## 它主要讲什么

这个库把逆向分析拆成几类 skill：

```text
find-crypto-entry:
  找关键参数从哪里生成，只定位入口，不继续越界。

env-patch:
  把浏览器环境拆成可运行环境，通过诊断报告一轮轮补缺。

ast-deobfuscate:
  把混淆代码按步骤还原，中间产物可回退，不确定的代码保留。

skill-creator:
  把新的专家流程写成 skill，并用测试、baseline、评分、反馈迭代。

rules/js-reverse:
  提供领域手册，不是每次都全量塞进主流程。
```

它的核心架构不是一个程序，而是一套：

```text
skill frontmatter
-> trigger rules
-> task scope
-> strategy selection
-> domain pitfalls
-> diagnostic loop
-> reference files
-> completion standard
-> eval loop
```

## 为什么像 VAKS

VAKS 的核心也是：

```text
不要让 AI 凭感觉直接给答案。
先分层，再检索，再找证据，再决定能不能行动。
```

这个库的核心是：

```text
不要让 AI 凭感觉逆向。
先定位，再验证，再补环境，再输出证据。
```

共同点：

```text
任务分阶段
每阶段有边界
工具动作和判断逻辑分开
中间产物可回看
失败要分类
完成标准要明确
```

## VAKS 可以借鉴什么

### 1. Skill 化 VAKS 流程

VAKS 后面不应该只有一堆文档规则，而应该把高频复杂流程 skill 化：

```text
source-intake-skill
candidate-distill-skill
blackbox-product-analysis-skill
retrieval-query-run-skill
context-pack-builder-skill
evidence-sufficiency-gate-skill
feedback-ledger-skill
review-queue-calibration-skill
```

每个 skill 都要像这个库一样明确：

```text
什么时候触发
什么时候不触发
输入是什么
输出是什么
做到哪里就停
什么不能顺手做
```

### 2. Query Intent Router 可以借 trigger 设计

这个库靠 skill description / trigger 来决定该不该用某个 skill。

VAKS 检索层可以借成：

```text
用户是在恢复上下文？
还是找来源？
还是问某个候选点是否可信？
还是要做 action basis？
还是只是探索？
```

不同意图进入不同检索路径，不要所有问题都扔给一个全库相似度搜索。

### 3. Retrieval Run 要有诊断树

`env-patch` 的诊断树思路可以改造成 VAKS 检索诊断：

```text
NO_HITS:
  先检查 scope / bucket / alias / language / source path

TOO_MANY_HITS:
  加 project / time / status / source-family 过滤

AUTHORITY_MIXED:
  raw/candidate/reviewed 混在一起，必须拆桶

STALE_INDEX:
  source hash 变化，索引过期

NO_EVIDENCE:
  检索命中只是相关，不是支持

ACTION_REQUESTED:
  进入 evidence sufficiency gate
```

这比“搜不到就换关键词”聪明很多。

### 4. Context Pack Builder 要有完成标准

`find-crypto-entry` 的好处是明确“只找入口，不做算法还原”。

VAKS 也需要这种停止点：

```text
source card:
  只记录来源，不做采用判断。

candidate distillation:
  只做理解和路由，不做 reviewed truth。

context pack:
  只组装上下文，不自动变成 action basis。

evidence packet:
  只判断支撑/挑战/缺口，不自动改 truth。
```

### 5. Progressive Disclosure 很适合 VAKS

这个库主 skill 不塞满全部知识，而是把细节放在 references 里按需读。

VAKS 可以借成：

```text
普通查询:
  读少量 hot context

重要判断:
  加 source anchors / candidate points

行动依据:
  加 evidence packet / challenge / omission / risk

维护任务:
  加 lint / manifests / stale checks
```

也就是严格性按需加载，而不是每次都把系统压满。

### 6. Skill Eval 可以成为 VAKS 流程质量门

`skill-creator` 的 baseline/eval 思路很适合 VAKS：

```text
有 skill vs 无 skill
旧 skill vs 新 skill
人工反馈 + 可检查指标
失败样例进入下一轮修订
```

VAKS 可以用它测试：

```text
检索 skill 是否更少漏掉来源？
context pack 是否更少混入候选当证据？
source intake 是否保留了关键 provenance？
feedback ledger 是否没有修改 truth？
```

## 不要借鉴什么

```text
不要借签名绕过。
不要借登录/会员/风控绕过。
不要借反调试对抗细节。
不要借还原闭源实现的操作路线。
不要把“逆向成功”当作 VAKS 的价值目标。
不要让工具能力凌驾于授权边界。
```

VAKS 只借流程设计，不借攻击性用途。

## 对 VAKS 的候选设计点

### Candidate Point 1: VAKS should encode complex workflows as skills

VAKS 现在有很多原则，如果只停留在文档里，AI 执行时容易漏。应该把复杂流程变成可触发、可测试、可停止的 skill。

Candidate status: strong.

### Candidate Point 2: Retrieval should have diagnostic failure classes

检索失败不应该只有“没搜到”。要像诊断树一样区分：

```text
scope 问题
bucket 问题
alias 问题
index stale
source missing
authority mixed
evidence missing
action gate missing
```

Candidate status: strong.

### Candidate Point 3: Context-pack workflows need completion standards

每个输出要知道自己到哪里停。没有这个，context pack 很容易变成隐形 action basis。

Candidate status: strong.

### Candidate Point 4: General knowledge should be separated from project overlay

这个源的通用价值是 expert workflow as skill。VAKS 特定价值是 source/retrieval/review/context-pack skills。两者要分开存。

Candidate status: strong.

## Borrow / Avoid

Borrow strongly:

- Expert workflow as AI skill.
- Trigger / do-not-trigger boundaries.
- Strategy selection by evidence signal.
- Domain pitfalls and anti-patterns in the skill body.
- Diagnostic loop and reference lookup.
- Completion standards.
- Progressive disclosure.
- Eval and baseline loop for skills.

Borrow carefully:

- Browser tooling idea as a generic "tool adapter" pattern.
- Black-box product analysis workflow.
- Controlled probes and before/after diffs.

Do not borrow:

- Security bypass operations.
- Anti-debug or signing evasion details.
- Any private implementation extraction route.

## Fusion Judgment

```yaml
fusion_decision: adapt-for-vaks-workflow-and-skill-design
borrow_value: strong
borrow_order: P1_for_skill_design_P2_for_blackbox_learning_P3_for_security_specific_details_excluded
core_schema_change_now: no
mainline_change_now: no
best_layer:
  - source intake workflow
  - retrieval query-run workflow
  - black-box product analysis workflow
  - context-pack builder
  - evidence sufficiency gate
  - feedback workflow
avoid_layer:
  - truth core
  - reviewed relation
  - action basis
  - security bypass operations
```
