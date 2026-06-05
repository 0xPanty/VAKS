# Pro Research Prompt: Development Borrowing Tags / Knowledge Flywheel

请基于前面 VAKS v0.2.13 的上下文，继续调研并复核一个更具体、更核心的设计想法。

## 背景

我们现在澄清：所谓“开发区 / Project Borrowing Ledger”，原始意思不是正式决策区，不是长期知识库，也不是新文件夹系统。

真正意思是：

```text
外部资料先由 AI 蒸馏成通用、独立、原子化的知识点。
当前项目开发时，只在相关知识点旁边打轻量“项目借鉴标签”。
标签标明当前项目能借什么、不能借什么、借到哪里、当前状态是什么。
项目结束后，这些标签可以取消、归档、快照，或链接到正式决策 / action basis。
成功采用的知识点回流成架构模式 / 经验指南。
踩过坑或不适合的点回流成负向知识 / 项目边界 / 雷区。
```

也就是说：

```text
通用知识点保持干净、可跨项目复用。
项目标签只是开发期间的透明蒙版。
项目结束后的快照沉淀正向经验和负向边界。
```

## 想验证的核心判断

这套逻辑是否合理：

```text
参考资料
-> AI 蒸馏成通用知识点
-> 当前项目给知识点打借鉴标签
-> 开发中验证 / 采用 / 避开 / 踩坑
-> 项目结束快照
-> landed 回流成架构模式 / best practice
-> avoid 回流成负向知识 / 项目边界 / 自动预警
-> 下个项目优先复用这些经验和边界
```

## 标签初始设想

```text
watch   = 看起来相关，先观察
borrow  = 当前项目可以借鉴某一部分
avoid   = 当前场景不要借，或有明确雷区
landed  = 已经被当前项目吸收或落地
parked  = 暂停，不处理；条件变化再看
```

最小备注：

```text
知识点
当前项目标签
可借鉴什么
不可借鉴什么
借到哪里
为什么
落地前还要过什么 gate
项目结束后怎么处理：remove / archive / snapshot / link-to-decision
```

## 请调研和判断

请重点回答：

1. 这个思路是否合理？
2. 它是否比“正式开发区文件夹 / Project Borrowing Ledger”更轻、更不污染知识库？
3. 有没有成熟实践支撑？请从这些方向调研：
   - annotation overlay / Web Annotation style overlay
   - design rationale
   - pre-ADR / decision backlog
   - issue labels / tags
   - software architecture knowledge management
   - knowledge reuse workspace
   - postmortem / lessons learned
   - negative knowledge management / failure knowledge / boundary knowledge
4. 它和 VAKS 当前 Candidate Pattern Bank / Project Borrowing Ledger 应该怎么对齐？
5. 是否建议把 Project Borrowing Ledger 的口径降重为 “development borrowing tags”？
6. 最小字段应该是什么？
7. 标签生命周期应该怎么设计？
8. landed 后如何回流成架构模式 / 经验指南？
9. avoid / rejected 后如何回流成负向知识 / 项目边界？
10. 怎么防止它变成正式决策区、schema、template、truth layer 或永久项目状态？
11. 有没有更聪明的补充或更好的命名？

## 请给出 verdict

请按这个格式回复：

```text
Verdict: accept_direction | revise_direction | reject_direction

One-sentence reason:

What is strongest:

What is risky:

Best name:

Recommended minimum fields:

Recommended lifecycle:

How to handle landed tags:

How to handle avoid / negative tags:

How to keep generic knowledge points clean:

Mature-practice support:

Suggested VAKS wording:

What should stay sandbox-only:

What to test before any mainline change:
```
