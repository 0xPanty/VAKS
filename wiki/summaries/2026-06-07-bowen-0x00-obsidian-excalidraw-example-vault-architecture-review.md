---
type: library_review
status: draft
library_name: "Obsidian Excalidraw Example Vault"
repo_url: https://github.com/Bowen-0x00/obsidian-excalidraw-example-vault
source_url: https://github.com/Bowen-0x00/obsidian-excalidraw-example-vault
checked_commit: 3da586cc520d77c7f250d3765bf1fca1c91d70bd
commit_time: "2026-05-19 11:50:29 +0800"
source_status: active
reviewed_at: 2026-06-07
domain: obsidian excalidraw demo vault and visual sidecar scripts
related_projects:
  - verified-action-knowledge-system
current_branch:
  - visual-workbench
  - activation-tier
  - context-pack-sidecar
  - dev-context-navigation
extracted_patterns:
  - visual-sidecar-is-activation-not-truth
  - canvas-customdata-as-local-semantics
  - markdown-mindmap-bridge-with-source-anchors
  - source-line-linked-code-overlay
  - demo-vault-as-sandbox
fusion_decision: watch
borrow_value: medium
tag_level: medium-borrow
confidence: medium-low
evidence_count: 14
cross_validated_with:
  - VAKS project overlay boundary
  - Obsidian source intake rules
negative_evidence:
  - no repository root license detected
  - modified plugin dependency
  - incomplete feature dependency table
  - runtime was not executed in Obsidian
extension_potential: medium
relations: []
tags:
  - obsidian-excalidraw-example-vault
  - library-review
  - medium-borrow
  - visual-workbench
  - canvas-sidecar
  - markdown-mindmap-bridge
  - source-anchored-overlay
  - modified-plugin-risk
  - candidate-only
---

# 库分析：Obsidian Excalidraw Example Vault

## 它解决什么问题

这个仓库解决的是：

```text
用户想体验一组改造后的 Obsidian Excalidraw 功能
但不想自己安装插件、配置脚本、搭画布示例
```

所以它把 Obsidian vault、改版 Excalidraw 插件、自定义脚本、库设置、示例画布、附件素材打包到一起，让用户直接用 Obsidian 打开试验。

对 VAKS 来说，它不是 source intake、review queue、truth maintenance、agent gateway、feedback ledger 的直接参考。它的价值集中在：

```text
visual workbench
canvas sidecar
Markdown <-> Excalidraw bridge
source/code navigation overlay
plugin/script sandbox packaging
```

## 核心设计

它的核心不是复杂后端，而是一个 Obsidian runtime 包：

```text
packaged vault
-> bundled modified Excalidraw plugin
-> custom scripts under Excalidraw/Scripts
-> Excalidraw canvas examples
-> element customData stores local semantics
-> hook-based engines draw or mutate UI behavior
```

两条最有 VAKS 参考价值的链：

```text
Markdown outline / clipboard
-> import script
-> Excalidraw elements with customData.mindmap
-> background engine layout / keyboard / collapse
-> export script
-> Markdown outline with group anchors
```

```text
code text / pasted payload
-> codeHighlight customData
-> highlight.js backed render engine
-> SVG export hook
-> ymjr://open source-line link
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:5-11` | Packaged Obsidian vault with modified Excalidraw plugin, custom scripts, example canvases, and video. | Demo vault as onboarding/sandbox for visual tooling. | Not architecture proof. |
| `README.md:17-23` | Backup warning with git/OneDrive/core file recovery suggestions. | Author signals vault mutation/saving risk. | Backup advice is not safety validation. |
| `README.md:30-34` | Some features need modified plugin plus custom scripts; dependency table incomplete. | Direct adoption risk and dependency opacity. | Blocks strong-borrow/direct use. |
| `docs/README_ZH.md:4-30` | Chinese README confirms same packaged-vault and porting caveats. | Source identity and intended usage are clear. | Still no runtime validation. |
| `.obsidian/plugins/obsidian-excalidraw-plugin-ymjr/manifest.json:2-10` | Bundled modified plugin manifest. | Runtime depends on non-upstream plugin fork. | Plugin must be treated as unreviewed runtime. |
| `Excalidraw关系.excalidraw.md:11-19`, `503-507`, `714-719` | Canvas explicitly names modified plugin and script dependency. | Dependency map itself is visualized. | Visual map is orientation only. |
| `Feature-Mindmap-Engine.md:7-12` | Background mindmap engine for `customData.mindmap`, collapse/expand, keyboard creation, navigation, layout, `window.MindmapAPI`. | Canvas-local metadata drives interaction. | UI semantics are not reviewed knowledge. |
| `Feature-Mindmap-Engine.md:594`, `748-763` | `MindMapLayouter` and exposed `runLayout`. | Layout can be recomputed from metadata. | Layout is not relation evidence. |
| `Feature-Mindmap-Engine.md:1208-1218` | Hook registration/unregistration through `window.EA_Core`. | Modified plugin hook system is the runtime backbone. | Main-vault adoption requires separate review. |
| `Action-Create-Mindmap.md:98-145`, `270-277` | Reads shared settings, toggles `customData.mindmap`, invokes layout. | Small scripts mutate canvas metadata and request recompute. | Script mutation must remain outside truth layer. |
| `Action-Export-Mindmap-To-Md.md:66`, `example/思维导图/导出.md:12-23` | Root selection and group-anchor Markdown embeds. | Markdown/canvas bridge can preserve anchors. | Exported outline is candidate context. |
| `Action-Import-Mindmap-From-Clipboard.md:96`, `251`, `291-306` | Clipboard outline import, `customData.mindmap`, layout run. | Source outline can become visual sidecar. | Imported hierarchy is not ontology. |
| `Feature-Code-Highlight-Engine.md:7-10`, `122-126`, `218-221`, `262-263` | CodeHighlight render interception, highlight.js to SVG, export hooks. | Source/code visualization overlay. | Rendered visuals do not validate source. |
| `example/代码高亮/代码高亮.excalidraw.md:28`, `65` | `ymjr://open` source-line link examples. | Good dev-context navigation affordance. | Environment-specific and not evidence. |

## 当前支线价值

当前支线：

```text
visual-workbench / activation-tier / context-pack-sidecar / dev-context-navigation
```

它对当前支线：

```text
refines
```

具体价值：

- 给 VAKS future visual workbench 一个 concrete Obsidian/Excalidraw shape。
- 强化“画布是 activation，不是 truth”的边界。
- 给 source/candidate/project overlay 的可视化展示提供锚点思路。
- 给 MISA/VAKS dev context 提供 code/source-line navigation overlay 参考。
- 给 risky plugin/script workflow 提供 demo vault/sandbox 包装思路。

打标签等级：

```yaml
tag_level: medium-borrow
borrow_value: medium
```

为什么压到 medium：

- demo vault 价值高于架构价值。
- 依赖 modified plugin。
- 顶层 license 不明确。
- 功能依赖表不完整。
- 未执行 Obsidian runtime。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | No direct file-first LLM wiki mechanism. | no |
| Dusk workbench | Strongest value: visual workbench/demo vault. | candidate-only |
| source ingest | Useful only as source-anchored visual overlay idea. | adapt later |
| review queue | Can visualize candidate pressure, but cannot perform review. | support only |
| schema / reviewed knowledge | No reviewed schema contribution. | no |
| memory / dev context | Code/source-line visual links are useful for dev context navigation. | support |
| feedback | No direct feedback ledger. | no |
| retrieval / cache | Visual activation can complement retrieval but is not retrieval authority. | support |
| API / MCP / agent access | No relevant agent gateway. | no |
| viewer / workbench | Main reusable zone: Excalidraw sidecar and demo vault. | medium |
| publishing | SVG/code highlight export may be later publishing reference. | cold |
| risk / anti-pattern | Modified plugin bundle, custom script mutation, license ambiguity. | strong risk note |

## 值得提炼的模式

### 1. Visual Sidecar

Use Excalidraw as a sidecar that helps humans see candidates, sources, risks, and paths.

Boundary:

```text
sidecar helps activate context
sidecar does not create truth
```

### 2. Canvas-Local Semantics

Use element metadata like `customData` for local UI behavior.

Boundary:

```text
canvas metadata belongs to UI layer
reviewed schema stays in Markdown/reviewed layer
```

### 3. Markdown / Canvas Anchor Bridge

Allow Markdown outlines and canvas elements to refer to each other through stable anchors.

Boundary:

```text
anchor enables navigation
anchor does not prove support
```

### 4. Demo Vault Sandbox

Package risky visual tools in a separate vault before main-vault adoption.

Boundary:

```text
demo vault first
main vault only after explicit review
```

## 标签与量化

- domain: Obsidian visual workbench / Excalidraw scripts
- problem: make visual canvas workflows easy to try and anchor to Markdown/code
- pattern: canvas sidecar with local metadata
- maturity: experimental
- complexity: medium
- problem_fit: 3/5
- reuse_value: 3/5
- implementation_cost: 3/5
- integration_fit: 3/5
- evidence_strength: 2/5
- reversibility: 4/5 if kept sandbox-only

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Visual canvas as activation sidecar | Activation Tier is not truth tier. | candidate_relation | How can visual activation remain explicitly non-authoritative? |
| `customData` as canvas-local semantics | Reviewed schema and relations must stay review-controlled. | scope_mismatch risk | What fields may live only in visual UI metadata? |
| Markdown/canvas bridge with anchors | Evidence support must be source-span specific. | candidate_relation with warning | Which anchors are navigation only, and which could later enter evidence review? |
| Demo vault for risky plugin/script workflows | Main vault should not absorb unreviewed runtime. | risk_of | What minimal sandbox acceptance gate is needed before VAKS uses plugins/scripts? |

## Support / Challenge Review

What supports it:

- README and Chinese README clearly identify the packaged demo-vault purpose.
- Source files show concrete `customData.mindmap`, `customData.codeHighlight`, layout, import/export, and hook patterns.
- Examples show group anchors and source-line links.

What challenges it:

- No root license detected.
- Modified plugin dependency.
- Incomplete feature/script dependency table.
- No runtime execution in this review.
- Obsidian custom scripts can mutate vault/UI state.

Challenge severity:

```text
major for direct adoption
minor for design-only visual-sidecar borrowing
```

Action readiness:

```text
not_ready
```

## 对当前项目的适配点

适配：

- Future VAKS visual context pack.
- Review map for candidate points / source anchors / risks.
- Dev context canvas with source-line code links.
- Separate visual tooling sandbox vault.

不适配：

- Main vault plugin bundle.
- Automatic Excalidraw-to-reviewed-relation import.
- Treating mindmap hierarchy as ontology.
- Treating visual layout as action-ready evidence.

## 融合判断

- 结论：watch / adapt later
- Direct use: no
- Fork: no
- Design-only: yes
- Current branch value: medium for visual-workbench only
- Whole architecture value: low-medium
- Risk: modified plugin, license ambiguity, runtime mutation
- Next action: keep VAKS project overlay as `medium-borrow`; reopen only when visual workbench work starts.

## 后续行动

- Keep as candidate-only reference.
- Use only as support/risk context for visual workbench tasks.
- Do not promote to `wiki/patterns` or `wiki/decisions` without a later evidence-aware review.
- Do not install or run bundled plugins/scripts in the main VAKS vault during this intake.
