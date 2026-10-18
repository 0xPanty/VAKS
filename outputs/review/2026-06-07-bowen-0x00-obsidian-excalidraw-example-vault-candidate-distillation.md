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
  - raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source.md
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
  - obsidian-sandbox
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-example-vault-3da586cc520d77c7f250d3765bf1fca1c91d70bd.zip
    selector_type: source_code
    selector_value: README.md:5-32
  - snapshot_ref: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-example-vault-3da586cc520d77c7f250d3765bf1fca1c91d70bd.zip
    selector_type: source_code
    selector_value: Excalidraw/Scripts/Downloaded(Custom)/Feature-Mindmap-Engine.md:7-12
  - snapshot_ref: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-example-vault-3da586cc520d77c7f250d3765bf1fca1c91d70bd.zip
    selector_type: source_code
    selector_value: Excalidraw/Scripts/Downloaded(Custom)/Action-Export-Mindmap-To-Md.md:66
  - snapshot_ref: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-example-vault-3da586cc520d77c7f250d3765bf1fca1c91d70bd.zip
    selector_type: source_code
    selector_value: example/代码高亮/代码高亮.excalidraw.md:28
tagging_decision: tagged
tag_level: medium-borrow
tag_level_reason: "Useful VAKS reference for visual sidecars, canvas-local metadata, Markdown-mindmap bridges, and source-linked code overlays; downgraded from strong because it is a demo vault, depends on a modified plugin, has no root license, and was not runtime-tested."
borrow_value: medium
borrow_order:
  - "P1: visual sidecar as activation/context overlay, not reviewed knowledge"
  - "P1: Excalidraw element customData as canvas-local semantic metadata"
  - "P1: Markdown <-> mindmap bridge with anchors back to source notes/elements"
  - "P2: source-line linked code highlight overlay for developer context navigation"
  - "P2: packaged demo vault as sandbox/onboarding shape for visual workflows"
  - "P3: Excalidraw libraries, fonts, CSS, plugin settings, and bundled examples as cold references"
avoid:
  - "Do not copy bundled modified plugins or scripts into the main VAKS vault without a separate security and compatibility review."
  - "Do not treat Excalidraw arrows, visual proximity, mindmap parent/child fields, or layout order as reviewed relations."
  - "Do not treat generated Markdown exports or code-highlight visuals as evidence support."
  - "Do not let a demo vault become VAKS core architecture before a concrete visual-workbench task exists."
  - "Do not reuse code/assets directly while root repository licensing remains unclear."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "approved VAKS task designs or implements an Obsidian/Excalidraw visual workbench, canvas sidecar, or source-linked developer context overlay."
  support_when: "exploring visual context packs, source-anchored diagrams, Markdown-mindmap bridges, Excalidraw demo vaults, or code/source-line navigation overlays."
  risk_when: "canvas layout could be mistaken for reviewed relation, plugin/script runtime could mutate vault content, or bundled assets/plugins could create licensing/supply-chain risk."
  cold_references:
    - raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source.md
    - raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-example-vault-3da586cc520d77c7f250d3765bf1fca1c91d70bd.zip
tags:
  - candidate
  - provisional
  - obsidian-excalidraw-example-vault
  - excalidraw
  - visual-workbench
  - canvas-sidecar
  - markdown-mindmap-bridge
  - source-anchored-visual-overlay
  - code-highlight-overlay
  - obsidian-plugin-bundle
  - modified-plugin-risk
  - medium-borrow
  - candidate-only
---

# Obsidian Excalidraw Example Vault Candidate Distillation

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## Source

```yaml
derived_from:
  - raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source.md
checked_commit: 3da586cc520d77c7f250d3765bf1fca1c91d70bd
snapshot: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-example-vault-3da586cc520d77c7f250d3765bf1fca1c91d70bd.zip
snapshot_sha256: 53EB073E2E740C73CD1368B0CC77CB9A84501B5ABB59B8FA403FEE56B30BB0AA
runtime_executed: false
```

## 人话压缩

这个库对 VAKS 有帮助，但不是“大核心”。

它最像一个视觉实验包：

```text
Markdown note
-> Excalidraw element
-> customData keeps local semantics
-> canvas shows mindmap / code / source-line link
-> user can visually navigate context
```

VAKS 可以借的是：

```text
把画布当侧车
让它帮人理解、导航、激活上下文
但不要让画布决定 truth / relation / action basis
```

## 打标签结论

```yaml
tagging_decision: tagged
tag_level: medium-borrow
borrow_value: medium
```

为什么不是 strong：

```text
它是 demo vault，不是知识系统架构。
部分能力依赖修改版 Excalidraw 插件。
README 明说功能依赖表还不完整。
顶层仓库没有检测到 license。
本次只读源码和文档，没有在 Obsidian 里跑插件/脚本。
```

为什么仍然要打：

```text
VAKS 以后做 visual context pack / canvas sidecar / dev context overlay 时，它有直接参考价值。
```

## Candidate Points

### 1. `visual-sidecar-is-activation-not-truth`

候选结论：VAKS 可以把 Excalidraw 画布用作 activation/context sidecar，让人快速看到 source、candidate、project overlay、风险和关系草图，但画布本身不创造 reviewed relation。

锚点：

- `README.md:5-11`
- `docs/README_ZH.md:4-8`
- `Excalidraw关系.excalidraw.md:11-19`

对 VAKS 的适配：

- 画布适合承载“我现在该看什么”的导航。
- 画布适合展示 candidate relation pressure、source anchor、risk note。
- 画布不适合直接写入 truth layer。

边界：

```text
visual proximity != support
arrow != reviewed relation
layout != evidence
```

### 2. `canvas-customdata-as-local-semantics`

候选结论：Excalidraw element 的 `customData` 可以作为画布局部语义缓存，例如 mindmap root/parent/level/status、codeHighlight language/style 等。VAKS 可以借这个思路做可视层局部状态，而不是污染 Markdown truth schema。

锚点：

- `Feature-Mindmap-Engine.md:7-12`
- `Action-Create-Mindmap.md:145`
- `Action-Create-Mindmap.md:270`
- `Action-Toggle-Code-Highlight.md:52`
- `Feature-Code-Highlight-Engine.md:122-126`

对 VAKS 的适配：

- `customData` 可作为 visual workbench 的 transient/local metadata。
- Markdown source card / candidate note 仍是可追踪主体。
- 画布 metadata 可以回链 source path、block id、selector。

边界：

```text
customData is UI state
customData is not reviewed schema
customData is not evidence support
```

### 3. `markdown-mindmap-bridge-with-source-anchors`

候选结论：Markdown outline 和 Excalidraw mindmap 可以互转，并通过 group/block anchor 回到具体画布元素。VAKS 借这个时，应强调“来源锚点”和“候选理解”，而不是自动生成知识图谱。

锚点：

- `Action-Export-Mindmap-To-Md.md:66`
- `example/思维导图/导出.md:12-23`
- `Action-Import-Mindmap-From-Clipboard.md:96`
- `Action-Import-Mindmap-From-Clipboard.md:251`
- `Action-Import-Mindmap-From-Clipboard.md:291-306`

对 VAKS 的适配：

- 可以用于把 source/candidate/project overlay 做成 review map。
- 可以让导出 Markdown 保留画布 block/group anchor。
- 可以帮助 reviewer 看到结构，但不能替代 Evidence Packet。

边界：

```text
mindmap hierarchy != ontology
exported outline != reviewed relation set
imported outline != truth mutation
```

### 4. `source-line-linked-code-overlay`

候选结论：代码高亮画布元素可以带 `ymjr://open?...&line=...` 这类源文件行链接。对 VAKS/MISA 一类开发上下文，这可以成为 dev context 的可视导航层。

锚点：

- `Feature-Code-Highlight-Engine.md:7-10`
- `Feature-Code-Highlight-Engine.md:262-263`
- `example/代码高亮/代码高亮.excalidraw.md:28`
- `example/代码高亮/代码高亮.excalidraw.md:65`

对 VAKS 的适配：

- 可以把 code anchor、source card、candidate point、risk note 放在一张图里。
- 可以给项目上下文包提供“点哪里打开哪里”的视觉入口。
- 适合作为 Support layer，不适合作为 Core rule。

边界：

```text
source-line link is navigation
navigation is not validation
highlighted code is not reviewed claim
```

### 5. `demo-vault-as-sandbox`

候选结论：把插件、脚本、库设置、示例画布打成一个独立 demo vault，是一种适合高风险可视化工具试验的包装方式。VAKS 可以借“独立 sandbox vault”这个方式，而不是把插件包直接塞进主 vault。

锚点：

- `README.md:9`
- `README.md:17-23`
- `README.md:30-34`
- `docs/README_ZH.md:13-30`

对 VAKS 的适配：

- 未来如果做 Excalidraw visual workbench，先做独立 demo/sandbox。
- 主 vault 只保留源卡、候选蒸馏、overlay 和必要说明。
- 插件 runtime、脚本运行、CSS、字体、库素材在 sandbox 里验证。

边界：

```text
demo vault != production vault
plugin bundle != architecture decision
script success != safety approval
```

## Open Questions

- Modified Excalidraw plugin `obsidian-excalidraw-plugin-ymjr` 与当前 Obsidian/Excalidraw 版本兼容性如何？
- Custom script frontmatter license 与 repo root no-license 状态如何冲突或并存？
- 是否有最小脚本集合可支持 VAKS 需要的 visual sidecar，而不引入全套插件包？
- 画布 `customData` 如何稳定回链到 Markdown source/candidate/review nodes？

## Routing Hint

```yaml
route_to:
  - visual-workbench
  - activation-tier
  - context-pack-sidecar
  - source-anchored-overlay
  - dev-context-navigation
do_not_route_to:
  - reviewed-knowledge
  - truth-confidence
  - action-basis
  - main-vault-plugin-adoption
```

## Forbidden

```text
project_borrow_scope outside project overlay
decision outcome
formal pattern
action basis
truth confidence
direct plugin adoption
```
