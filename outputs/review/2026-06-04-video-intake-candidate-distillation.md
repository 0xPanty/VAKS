---
type: review-candidate
status: pending-review
created: 2026-06-04
proposed_node_type: candidate-pattern-set
proposed_title: "Video Intake Candidate Distillation: Light Capture, Workbench, and Feedback Surface"
proposed_by: Codex
sources:
  - raw/videos/2026-06-04-bilibili-obsidian-usage-barriers-source.md
  - raw/videos/2026-06-04-bilibili-notion-vs-obsidian-system-source.md
  - raw/videos/2026-06-04-bilibili-obsidian-exam-knowledge-graph-source.md
  - raw/videos/2026-06-04-bilibili-obsidian-one-page-workbench-source.md
evidence_level: video-derived candidate comprehension
verification_status: unverified
confidence: medium for workflow themes, low for plugin/repository adoption
relations: []
reviewer:
review_result:
---

# Video Intake Candidate Distillation: Light Capture, Workbench, and Feedback Surface

## 边界

本文件是四条视频 source card 的候选蒸馏，不是 reviewed knowledge。

这些视频的字幕/转写来自本地 ASR，属于 raw/source text；source card 里的摘要、反漏提取和 candidate points 属于 candidate comprehension。本文只把它们整理成后续 review 可看的候选包，不直接修改 `wiki/claims/`、`wiki/patterns/`、`wiki/anti-patterns/` 或 `wiki/decisions/`。

## 人话总览

这四条视频合起来给 VAKS 一个很一致的提醒：

资料库不能只做“能收进来”，也不能一上来就要求用户填完整 schema、标签、关系、结论和行动依据。入口太重会让 Capture 死掉；只保存不加工会变成高级仓库；只有 schema 没有工作台，用户感受不到“下一步该做什么”；反馈和使用痕迹如果被误当 truth，又会污染 reviewed knowledge。

更适合吸收的方向是：

```text
轻入口 Capture
-> 候选理解 / 反漏提取
-> 当前项目和行动面 workbench
-> 使用反馈 / 诊断信号回写
-> 需要 promotion 或 action basis 时再进入严格 review
```

## 四条视频分别解决什么问题

### 1. Obsidian 三大使用障碍

来源：`raw/videos/2026-06-04-bilibili-obsidian-usage-barriers-source.md`

它把 Obsidian 卡住拆成记录、处理、输出三段。对 VAKS 的候选价值是提醒我们：Capture 必须轻，Understand 才加工，Review 才变严格，Act and Learn 必须保留输出和反馈。

它不能直接提供心理学 reviewed claim，因为视频没有给出可核验论文或实验来源，ASR 也有术语误识别。

### 2. Notion vs Obsidian: 先建系统

来源：`raw/videos/2026-06-04-bilibili-notion-vs-obsidian-system-source.md`

它把“选哪个工具”降级为“有没有系统”。对 VAKS 的候选价值是强调工具层、插件层、图谱层不能替代 source -> candidate -> review -> action -> feedback 的结构。

它不能把 PARA 直接变成 VAKS truth schema，也不能把 Notion/Obsidian 分工当正式工具评测。

### 3. 备考知识图谱插件

来源：`raw/videos/2026-06-04-bilibili-obsidian-exam-knowledge-graph-source.md`

它展示了一个更具体的行动闭环：教材考点 -> 真题节点 -> 答题面板 -> AI 批改 -> 掌握度回写 -> 热力图。对 VAKS 的候选价值是把 Use Ledger / Feedback 变成一个可见的学习工作台。

它不能直接进入 mainline，因为视频没有给完整代码、字段、仓库、安全边界或 AI 批改可靠性验证。掌握度和热力图只能是 diagnostic / activation 信号，不是 truth confidence。

### 4. APEX Dashboard 一页纸工作台

来源：`raw/videos/2026-06-04-bilibili-obsidian-one-page-workbench-source.md`

它展示了 Memo、Todo、Project docs、Quick links、Recently edited 聚合成一个 Obsidian 工作台。对 VAKS 的候选价值是说明 activation surface 可以很轻，但能显著降低日常接续工作成本。

它不能直接作为插件采纳结论。插件名、仓库、许可证、权限、维护状态和代码质量都还没有 review。

## 共同模式

```text
pattern_1:
  name: 轻入口不是弱系统
  summary: 普通 capture 不应该要求用户同时完成标签、分类、关系、摘要、结论和输出。
  VAKS_fit: 支持 light / medium / heavy intake；严格检查应是 lazy gate。

pattern_2:
  name: 工具层不能替代系统层
  summary: Obsidian、Notion、Dashboard、图谱插件都是载体；没有 source/candidate/review/action/feedback 结构时，工具会变成仓库或杂物间。
  VAKS_fit: 支持继续把工具和 workbench 放在 activation/context 层，而不是 truth core。

pattern_3:
  name: 工作台是行动入口，不是知识真理
  summary: Memo、Todo、Project cards、Quick links、Recently edited、热力图都能降低行动摩擦。
  VAKS_fit: 可作为 Activation / Context Pack / Use Ledger UI 的候选 surface。

pattern_4:
  name: 反馈回写有价值，但必须隔离 truth
  summary: 答题结果、AI 批改、掌握度、任务完成和最近编辑能帮助下次行动，却不能直接改变知识可信度。
  VAKS_fit: 支持 Use Ledger / Feedback 边界：feedback 改善激活和范围匹配，不直接改 truth confidence。
```

## 可进入 REVIEW_QUEUE 的候选点

1. `light_capture_lazy_gate`

候选结论：普通 source capture 应保持低摩擦，标签、关系、摘要、反漏、review 和 action basis 应按价值逐步打开。

为什么值得 review：它能把“防止终态前置”写成 VAKS source intake 的设计理由。

风险：如果解释过度，可能被误解为取消 review 严格性。

2. `workbench_as_activation_surface`

候选结论：VAKS 可以有一个轻 workbench surface，聚合当前项目、待办、最近使用、候选材料和下一步入口，但它只是 activation/context surface。

为什么值得 review：四条视频都指向同一个痛点：没有行动入口时，资料库价值不容易被用户感知。

风险：Dashboard 容易看起来像系统本体，必须明确它不是 truth layer。

3. `feedback_event_diagnostic_not_truth`

候选结论：答题、任务完成、使用频率、最近编辑、AI 批改、掌握度等都可以成为 feedback-event 或 diagnostic signal，但不能自动变成 truth confidence、reviewed relation 或 action readiness。

为什么值得 review：备考图谱视频给了一个很具体的反馈回写例子，适合压实 Use Ledger 的边界。

风险：用户很容易把热力图、进度条和 AI 批改当成“系统已经判断可靠”。

4. `system_before_tool_explanation`

候选结论：对外解释 VAKS 时，可以用“系统先于工具”作为人话解释：工具负责承载，结构负责让资料进入行动和反馈。

为什么值得 review：这能降低 Obsidian/Notion/插件争论对架构判断的干扰。

风险：PARA 或普通 GTD 结构不能替代 VAKS 的 source/candidate/review/action schema。

## 暂不吸收的东西

```text
do_not_absorb:
  - 视频里的心理学解释，不作为 reviewed claim。
  - PARA，不直接替代 VAKS schema。
  - APEX Dashboard，不直接推荐安装或采纳。
  - 备考知识图谱插件，不直接照搬到 VAKS mainline。
  - AI 批改，不作为 evidence review。
  - 热力图/掌握度/最近编辑/任务完成，不作为 truth confidence。
  - Bilibili metadata 的播放量、点赞、收藏，不作为 source quality 或 source independence。
```

## 对当前 VAKS 的最小优雅吸收版

不新增核心模块，只保留三条候选改进方向：

1. 在 source intake / video batch intake 的说明里继续强调轻入口和分级加工。
2. 在未来 workbench 讨论里，把 `Memo / Todo / Project Docs / Quick Links / Recently Edited / Heatmap` 作为候选 UI vocabulary。
3. 在 Use Ledger / Feedback 讨论里，把 `diagnostic signal != truth confidence` 写得更硬。

## 需要进一步核验

```text
source_verification:
  - 四条视频都没有拿到公开字幕，当前转写来自本地 ASR。
  - 关键插件名、仓库、UI 字段和许可证需要画面/评论区/GitHub 核验。
  - 心理学术语、PARA 原始解释、AI 批改可靠性都需要更强来源。

review_needed_before_promotion:
  - 是否把 light capture lazy gate 写入 SOURCE_INTAKE 或 README 的解释层。
  - 是否把 workbench as activation surface 写成 candidate pattern。
  - 是否把 feedback diagnostic boundary 写入 FEEDBACK 或 MEMORY_TIER。
  - 是否需要单独 review APEX Dashboard 或备考知识图谱插件仓库。
```

## 建议下一步

保持当前文件为 `pending-review`。如果进入正式 review，建议先只审三件事：

1. `light_capture_lazy_gate` 是否可以成为 VAKS source intake 的明确设计理由。
2. `workbench_as_activation_surface` 是否值得写成候选 pattern，而不是马上实现。
3. `feedback_event_diagnostic_not_truth` 是否需要补强到 FEEDBACK / MEMORY_TIER 的边界说明里。

这批视频暂时不要进入 reviewed knowledge；它们更适合作为 VAKS 工作流和工作台方向的 candidate pressure。
