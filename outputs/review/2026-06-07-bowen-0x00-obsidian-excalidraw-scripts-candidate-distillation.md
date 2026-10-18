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
  - raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source.md
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
  - visual-workbench
  - activation-tier
  - context-pack-sidecar
  - source-anchored-overlay
  - obsidian-script-sandbox
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-scripts-1d0edb6beac48efe92b5a19c22cef701bc3a54e5.zip
    selector_type: source_code
    selector_value: README.md:5-11
  - snapshot_ref: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-scripts-1d0edb6beac48efe92b5a19c22cef701bc3a54e5.zip
    selector_type: source_code
    selector_value: Scripts/mindmap/Feature-Mindmap-Engine.md:2-15
  - snapshot_ref: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-scripts-1d0edb6beac48efe92b5a19c22cef701bc3a54e5.zip
    selector_type: source_code
    selector_value: Scripts/clipboard/Feature-Paste-Engine.md:2-14
  - snapshot_ref: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-scripts-1d0edb6beac48efe92b5a19c22cef701bc3a54e5.zip
    selector_type: source_code
    selector_value: Scripts/tag/Action-Set-Tags.md:55-74
tagging_decision: tagged
tag_level: medium-borrow
tag_level_reason: "More implementation-dense than the example vault and useful for VAKS visual workbench/script-sandbox design, but kept at medium because it is future-sidecar work, root licensing is unclear, README links are stale, modified plugin dependency exists, and runtime was not tested."
borrow_value: medium
borrow_order:
  - "P1: Action script vs Feature engine separation for visual workbench behavior"
  - "P1: EA_Core hook lifecycle as a candidate plugin/script sandbox reference"
  - "P1: customData as canvas-local semantic metadata, not reviewed schema"
  - "P1: paste/link/export scripts for source-anchored visual sidecars"
  - "P2: element tags, code-highlight links, tables, ECharts, and mindmaps as visual navigation affordances"
  - "P2: generated script index/category structure as a discoverability reference"
  - "P3: individual drawing utilities, style helpers, libraries, and GIF demos as cold references"
avoid:
  - "Do not install or run this script collection in the main VAKS vault from this intake."
  - "Do not treat Excalidraw customData.tags as VAKS review tags, taxonomy, or truth labels."
  - "Do not treat mindmap/table/echarts/link layout as reviewed relations or evidence support."
  - "Do not reuse code/assets directly while repository-root license is unclear and vendored library licensing is not reviewed."
  - "Do not let paste/link/export hooks import private or untrusted clipboard/protocol data without a sandbox and explicit user control."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "approved VAKS task designs or implements an Obsidian/Excalidraw visual workbench, script sandbox, source-linked visual context pack, or dev-context canvas."
  support_when: "exploring Action/Feature script structure, EA_Core hook lifecycle, canvas-local metadata, Markdown/mindmap bridges, visual tags, paste/link/export sidecars, or source-line navigation."
  risk_when: "canvas metadata could be confused with reviewed knowledge, scripts could mutate vault/UI state, hooks could intercept private data, or license/supply-chain ambiguity blocks direct reuse."
  cold_references:
    - raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source.md
    - raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-scripts-1d0edb6beac48efe92b5a19c22cef701bc3a54e5.zip
tags:
  - candidate
  - provisional
  - obsidian-excalidraw-scripts
  - excalidraw
  - custom-scripts
  - visual-workbench
  - canvas-sidecar
  - ea-core-hooks
  - action-feature-split
  - canvas-local-metadata
  - source-anchored-visual-overlay
  - markdown-mindmap-bridge
  - visual-tags-not-vaks-tags
  - script-sandbox-risk
  - medium-borrow
  - candidate-only
---

# Obsidian Excalidraw Scripts Candidate Distillation

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## Source

```yaml
derived_from:
  - raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source.md
checked_commit: 1d0edb6beac48efe92b5a19c22cef701bc3a54e5
snapshot: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-scripts-1d0edb6beac48efe92b5a19c22cef701bc3a54e5.zip
snapshot_sha256: B2CB8E4C4BE76FD05F7869263BB6872363F614DC893B9081273D8DF2395E9E70
runtime_executed: false
```

## 人话压缩

这个仓库比刚才的 example vault 更像“工具箱本体”。

它对 VAKS 有用的不是某个按钮，而是这套结构：

```text
Action = 用户主动点一下，创建/修改画布元素
Feature = 后台常驻，接管某个 hook
customData = 元素自己的局部语义
EA_Core hook = 让画布有粘贴、链接、导出、绘制、键盘等行为
```

VAKS 可以借它的思路：

```text
画布可以做 source/candidate/context 的可视化侧车。
脚本可以帮人导航和理解。
但脚本和画布都不能变成 truth/review/action basis。
```

## 打标签结论

```yaml
tagging_decision: tagged
tag_level: medium-borrow
borrow_value: medium
```

为什么不是 strong：

```text
这条价值集中在未来 visual workbench，不是当前 VAKS 核心。
脚本会接管粘贴、链接、导出、键盘、渲染等运行时行为。
有 modified plugin 依赖。
root license 不明确。
README 有旧路径链接。
本次没有在 Obsidian 里实际跑。
```

为什么仍然要打：

```text
如果 VAKS 以后做 Excalidraw visual context pack、review map、dev context canvas、source-line navigation，它是目前很具体的实现参考。
```

## Candidate Points

### 1. `action-feature-split-for-canvas-tools`

候选结论：可视化脚本工具可以拆成 Action 和 Feature 两类。Action 负责用户触发的创建/修改，Feature 负责常驻 hook、渲染、导航、粘贴、导出等生命周期行为。

锚点：

- `Scripts/index.md:1-240`
- `Scripts/mindmap/Action-Create-Mindmap.md:2-15`
- `Scripts/mindmap/Feature-Mindmap-Engine.md:2-15`
- `Scripts/code-highlight/Feature-Code-Highlight-Engine.md:261-268`

对 VAKS 的适配：

- 未来 script sandbox 可以先区分 action vs background feature。
- background feature 要有明确 mount/unmount、scope、权限、日志。
- action mutation 要有可撤回/可审计记录。

边界：

```text
script structure != approval
hook registration != safety
runtime success != reviewed knowledge
```

### 2. `canvas-customdata-as-ui-semantics`

候选结论：`customData` 很适合存画布局部语义：`mindmap`、`codeHighlight`、`tags`、`echarts`、`table`。VAKS 可以借这个作为 visual sidecar 的局部状态，但 reviewed schema 仍要在 Markdown/review 层。

锚点：

- `Scripts/mindmap/Feature-Mindmap-Engine.md:160-214`
- `Scripts/tag/Action-Set-Tags.md:55-74`
- `Scripts/echarts/Feature-Echarts-Engine.md:433`
- `Scripts/table/Feature-Table-Engine.md:109-138`

对 VAKS 的适配：

- `customData` 可以保存视觉状态、局部标签、画布结构、显示参数。
- 主体 source/candidate/reviewed note 仍留在 Markdown 文件。
- 画布状态可以回链 source path/block id/selector。

边界：

```text
customData.tags != VAKS tags
customData.table != data source
customData.mindmap != ontology
```

### 3. `source-linked-paste-and-link-sidecar`

候选结论：Paste/link engines 可以把外部摘录、PDF 注释、图片、代码和本地文件行号变成画布元素。这对 VAKS future visual source map 有价值，但必须把输入视作 raw/candidate。

锚点：

- `Scripts/clipboard/Feature-Paste-Engine.md:2-14`
- `Scripts/clipboard/Feature-Paste-Engine.md:247-280`
- `Scripts/link/Feature-Link-Engine.md:2-15`
- `Scripts/link/Feature-Link-Engine.md:125-132`
- `Scripts/code-highlight/Feature-Code-Highlight-Engine.md:241`

对 VAKS 的适配：

- 可用于把 source snippets、code anchors、review comments 拉到画布。
- 可用于同文件 `#^group=` 导航和返回。
- 可用于 dev context canvas 的 source-line navigation。

边界：

```text
clipboard data is raw input
link route is navigation
navigation is not evidence support
```

### 4. `visual-export-is-presentation-not-proof`

候选结论：导出引擎可以把 Markdown/网页/图表/code highlight 渲染到 SVG 或图像中，适合做 review map 或解释图的输出；但导出的截图/图像不等于 source text，也不等于证据支持。

锚点：

- `Scripts/export/Feature-Export-Embeddable.md:2-14`
- `Scripts/export/Feature-Export-Embeddable.md:154-159`
- `Scripts/code-highlight/Feature-Code-Highlight-Engine.md:10-11`
- `Scripts/echarts/Feature-Echarts-Engine.md:10-11`

对 VAKS 的适配：

- 后续做 visual report、context pack image、review map 时有参考。
- Export artifact 应该标注为 presentation layer。
- Evidence support 仍要回到 source span / reviewed evidence item。

边界：

```text
exported SVG != evidence packet
screenshot != source support
chart render != verified data
```

### 5. `script-sandbox-required-before-main-vault`

候选结论：此类脚本能力越丰富，越需要 sandbox 和准入门。VAKS 若未来使用，应该先做独立 demo vault、兼容性检查、权限说明、license/supply-chain review、private-data guard，而不是直接复制进主 vault。

锚点：

- `README.md:9-11`
- `Scripts/clipboard/Feature-Paste-Engine.md:7-14`
- `Scripts/export/Feature-Export-Embeddable.md:170`
- `Scripts/mindmap/Feature-Mindmap-Engine.md:1255-1267`

对 VAKS 的适配：

- 先 sandbox，再主 vault。
- 先明确脚本读写能力，再启用。
- 对剪贴板、协议链接、外部网页、文件写入、导出 hooks 设红线。

边界：

```text
demo success != production approval
frontmatter license != root license resolution
plugin dependency != VAKS dependency decision
```

## Open Questions

- README 旧路径是否意味着文档滞后、仓库迁移未完成，还是只是链接未更新？
- 125 个脚本 frontmatter MIT 与 root no-license 状态如何解释？
- Modified Excalidraw plugin 是否必需，哪些脚本可以在 upstream plugin 下运行？
- VAKS 如果做 visual workbench，最小可用脚本集合是什么？
- 如何在脚本层记录 mutation ledger，避免 UI 脚本悄悄改变重要文件？

## Routing Hint

```yaml
route_to:
  - visual-workbench
  - activation-tier
  - context-pack-sidecar
  - source-anchored-overlay
  - obsidian-script-sandbox
  - dev-context-navigation
do_not_route_to:
  - reviewed-knowledge
  - truth-confidence
  - action-basis
  - main-vault-plugin-adoption
  - VAKS-taxonomy
```

## Forbidden

```text
project_borrow_scope outside project overlay
decision outcome
formal pattern
action basis
truth confidence
direct script installation
```
