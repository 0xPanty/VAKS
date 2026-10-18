---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from: "raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-source.md"
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
borrow_value: medium
borrow_order:
  - "P1: Canvas sidecar needs plugin-level hooks only when script-level behavior cannot cover the workflow."
  - "P2: Element customData/tags can support local visual navigation but must remain separate from VAKS truth tags."
  - "P3: Export/render and library/loading features are future visual-workbench references."
avoid:
  - "Do not install the fork in the main VAKS vault now."
  - "Do not treat canvas tags, links, or exported SVG as reviewed knowledge or action support."
  - "Do not reuse bundled/minified plugin code while license/source clarity and upstream drift are unresolved."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "An approved VAKS visual-workbench or Excalidraw sandbox task explicitly needs plugin-level hook behavior."
  support_when: "Designing canvas sidecars, visual navigation, source-anchored overlays, or interaction affordances."
  risk_when: "A plan proposes direct plugin installation, canvas tags as taxonomy, or visual export as evidence."
  cold_references:
    - "raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-source.md"
    - "raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-plugin-ymjr-3fa4ace442c3d455c05172e1b1894033572e6b47.zip"
routing_hint:
  - visual-workbench
  - canvas-sidecar
  - plugin-hook-sandbox
  - modified-plugin-risk
possible_project_refs:
  - VAKS
point_anchor_refs:
  - "README.md:3-18"
  - "README.md:20-80"
  - "README.md:87-103"
  - "manifest.json:2-11"
  - "main.js bundle symbol search and byte snippets"
tags:
  - candidate
  - provisional
  - obsidian-excalidraw
  - visual-workbench
  - canvas-sidecar
  - medium-borrow
  - modified-plugin-risk
---

# Candidate Distillation

## Boundary

This note is provisional orientation. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## Source

```yaml
derived_from: raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-source.md
snapshot_ref: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-plugin-ymjr-3fa4ace442c3d455c05172e1b1894033572e6b47.zip
checked_commit: 3fa4ace442c3d455c05172e1b1894033572e6b47
```

## Distillation Verdict

打标签，等级：`medium-borrow`。

原因：

- 它是前两个 Bowen Excalidraw 仓库的插件底座，能解释 visual workbench、mindmap、tag、code-highlight、echarts、export 等脚本为什么需要插件级改动。
- 它对 VAKS 有候选价值：未来如果要做画布 sidecar，可以借鉴“元素级元数据 + hook + export/render + 局部引用”的能力模型。
- 它不适合 strong：仓库主要是打包产物，没有清晰源码工程和 root license；需要关闭官方插件；捕获时落后官方 upstream；未运行测试。

## Candidate Points

1. **Plugin-level hook as visual sidecar substrate**

   README 明说这些功能是“需要修改才能实现”的部分，说明脚本层并不足以承载所有交互。VAKS 若未来做 visual workbench，应先问：哪些能力能用普通 Obsidian/Excalidraw 脚本解决，哪些才需要插件层 hook。

2. **Element-local metadata is useful, but not truth**

   Bundle search found `customData` and `customData.tags` paths。可借的是“元素局部元数据适合做画布导航和局部状态”，不可借的是把这些 tag 当成 VAKS 的正式标签、证据分类或 reviewed relation。

3. **Mouse / keyboard / hover hooks enable operational canvas**

   README 的鼠标/键盘 hook、展开折叠 mindmap、table resize、hover shadow、fixed element 等功能，说明 canvas 可以从静态图变成工作台。VAKS 可借作 project overlay / source navigation UI 的想象，不借作知识系统核心。

4. **Export/render is a presentation path, not evidence path**

   README 提到导出/嵌入 SVG 时渲染本地 md、代码高亮、echarts。对 VAKS 来说，这适合生成可读 visual snapshot，不适合作为 Evidence Packet 或 action-facing support。

5. **Modified plugin is a risk anchor**

   README 要求关闭原 Excalidraw 并启用 fork，且有备份提示。捕获时官方 upstream 已到 `2.23.10`，本 fork 是 `2.23.5-1`。这应该进入风险标签，不进入主库默认依赖。

## Borrow Gradient

```yaml
borrow_value: medium
tag_level: medium-borrow
direct_use: no
fork: no
design_only: yes
watch: yes
```

P1:

- 借插件级 hook 能力模型：只在脚本层确实不够时才考虑插件层。
- 借 canvas sidecar 的元素级 metadata / link / local tag / hover / keyboard model。

P2:

- 借导出和渲染思路作为 visual snapshot 或 project briefing。
- 借 library grouping、thumbnail、fixed element、connection 等 UX affordance 做未来工作台参考。

P3:

- 作为 Bowen Excalidraw scripts/example-vault 的背景依赖保留。
- 作为以后评估官方 Excalidraw 插件能力缺口的对照样本。

Avoid:

- 不直接装进 VAKS 主库。
- 不把 `customData.tags` 当 VAKS tag taxonomy。
- 不把画布 link/highlight/export SVG 当 evidence support。
- 不从 minified `main.js` 直接复制代码。
- 不在 root license、上游同步、保存行为、sandbox 测试未完成前推进采用。

## Open Questions

- `src/obsidian-excalidraw-plugin.7z` 是否包含可读源码或上游 patch？本轮未展开。
- 具体 fork delta 和官方插件差异是什么？需要对照 upstream source 后才能回答。
- 在纯 scripts/official plugin 下，有多少能力已经能实现，不必换 fork？
- 该 fork 在 VAKS 使用的 Obsidian 版本、移动端、同步工具下保存是否稳定？

## Routing Hint

- Route to: `visual-workbench`, `canvas-sidecar`, `plugin-hook-sandbox`, `modified-plugin-risk`.
- Keep out of: `wiki/claims`, `wiki/patterns`, `wiki/decisions`, reviewed relation pools.

## Forbidden

```text
project_borrow_scope as universal adoption
decision outcome
formal pattern
action basis
truth confidence
reviewed relation
```
