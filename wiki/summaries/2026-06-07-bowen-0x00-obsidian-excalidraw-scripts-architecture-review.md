---
type: library_review
status: draft
library_name: "Obsidian Excalidraw Scripts"
repo_url: https://github.com/Bowen-0x00/obsidian-excalidraw-scripts
source_url: https://github.com/Bowen-0x00/obsidian-excalidraw-scripts
checked_commit: 1d0edb6beac48efe92b5a19c22cef701bc3a54e5
commit_time: "2026-05-24 22:05:51 +0800"
source_status: active
reviewed_at: 2026-06-07
domain: obsidian excalidraw custom scripts and visual sidecar runtime
related_projects:
  - verified-action-knowledge-system
current_branch:
  - visual-workbench
  - activation-tier
  - context-pack-sidecar
  - obsidian-script-sandbox
extracted_patterns:
  - action-feature-split-for-canvas-tools
  - ea-core-hook-lifecycle
  - canvas-customdata-as-ui-semantics
  - source-linked-paste-and-link-sidecar
  - visual-export-is-presentation-not-proof
  - script-sandbox-required-before-main-vault
fusion_decision: watch
borrow_value: medium
tag_level: medium-borrow
confidence: medium-low
evidence_count: 18
cross_validated_with:
  - Obsidian Excalidraw Example Vault
  - VAKS project overlay boundary
negative_evidence:
  - no repository root license detected
  - README contains stale missing-path links
  - modified plugin dependency
  - runtime was not executed in Obsidian
  - hooks can intercept paste/link/export and mutate vault/canvas state
extension_potential: medium
relations: []
tags:
  - obsidian-excalidraw-scripts
  - library-review
  - medium-borrow
  - visual-workbench
  - canvas-sidecar
  - ea-core-hooks
  - action-feature-split
  - canvas-local-metadata
  - source-anchored-overlay
  - script-sandbox-risk
  - candidate-only
---

# 库分析：Obsidian Excalidraw Scripts

## 它解决什么问题

这个仓库解决的是：

```text
Obsidian Excalidraw 原生能力不够
-> 通过 custom scripts 增加脑图、标签、链接、粘贴、导出、代码高亮、表格、ECharts 等功能
```

它和 `obsidian-excalidraw-example-vault` 的区别：

```text
example vault = 可以打开试的 demo/sandbox
scripts repo = 真正的脚本集合和实现参考
```

对 VAKS 来说，它不是知识系统架构，也不是 source/review/truth 的直接参考。它的价值集中在：

```text
visual workbench
canvas sidecar
script sandbox
source-linked visual context
dev context navigation
```

## 核心设计

核心结构是：

```text
Scripts/<category>/
  Action-*.md
  Feature-*.md

Action:
  user-triggered
  create/edit selected elements
  write customData or files

Feature:
  autorun background engine
  register hooks into EA_Core
  intercept paste/link/export/render/keyboard/drag
  render or mutate canvas behavior
```

多处脚本共享同一个设计习惯：

```text
element.customData.<feature>
-> background engine reads it
-> hook renders/updates behavior
-> action scripts create/toggle/change it
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:5-11` | Personal Excalidraw custom scripts repo; some scripts depend on modified plugin; demo vault linked. | Clear relation to upstream plugin and example vault. | No safety or compatibility proof. |
| `README.md:14-40` | Feature catalog: mindmap, md/ex mindmap, code highlight, SVG export, tag, link, ECharts, etc. | Broad visual workbench feature map. | README links are partly stale. |
| `docs/README_ZH.md:19-40` | Chinese mirror of features. | Confirms intended Chinese-facing feature set. | Still source orientation. |
| `Scripts/index.md:1-240` | Generated list by categories. | Discoverability and taxonomy for scripts. | Index is not runtime proof. |
| `Scripts/mindmap/Feature-Mindmap-Engine.md:2-15` | Autorun engine for `customData.mindmap`. | Background engine owns visual semantics. | UI semantics only. |
| `Scripts/mindmap/Feature-Mindmap-Engine.md:160-214`, `1255-1267` | Reads/writes parent/root/level/hide state and registers pointer/key/drag/delete/render hooks. | Hook lifecycle and local state maintenance. | High mutation surface. |
| `Scripts/mindmap/Action-Export-Mindmap-To-Md.md:55-87`, `145-150` | Export mindmap to Markdown file with group anchors. | Markdown/canvas anchor bridge. | Export is candidate orientation, not review. |
| `Scripts/mindmap/Action-Import-Mindmap-From-Clipboard.md:140-169`, `248-306` | Clipboard outline import into `customData.mindmap`, then layout. | Raw outline to visual sidecar. | Clipboard input is untrusted. |
| `Scripts/code-highlight/Feature-Code-Highlight-Engine.md:10-11`, `122`, `241`, `261-268` | Draw/export/paste hooks; `ymjr://open` source-line link; codeHighlight metadata. | Dev-context navigation overlay. | Source-line link is not validation. |
| `Scripts/clipboard/Feature-Paste-Engine.md:2-14`, `247-280` | Parses BookxNote/Zotero/Eagle/ymjr formats into linked elements. | Source capture into canvas sidecar. | Private/protocol data risk. |
| `Scripts/link/Feature-Link-Engine.md:2-15`, `125-132` | Intercepts link clicks; handles group anchors and cross-file opening. | Navigation and return path. | UI routing only. |
| `Scripts/tag/Action-Set-Tags.md:2-14`, `55-74` | Floating tag editor writes `customData.tags`. | Visual-local tagging affordance. | Not VAKS tags. |
| `Scripts/export/Feature-Export-Embeddable.md:2-14`, `154-159`, `170` | html2canvas export of Markdown/web/embeddable to SVG image. | Presentation/export layer. | Screenshot is not evidence. |
| `Scripts/echarts/Feature-Echarts-Engine.md:2-14`, `433`, `569-575` | Chart engine stores `customData.echarts`, intercepts paste/render/export. | Visualization of structured data on canvas. | Chart render is not data verification. |
| `Scripts/table/Feature-Table-Engine.md:7-12`, `109-138`, `430-436` | Table engine uses `customData.table` and hooks editing/transform/drag/keyboard. | Canvas-local structured UI. | Not source data model. |

## 当前支线价值

当前支线：

```text
visual-workbench / activation-tier / context-pack-sidecar / script-sandbox
```

它对当前支线：

```text
refines
```

具体价值：

- 给 VAKS future visual workbench 一个实装级脚本库参考。
- 给 script sandbox 提供 hook/mutation/read-clipboard/file-write 风险清单。
- 给 source-anchored visual sidecar 提供 paste/link/export/code-line examples。
- 给 local visual tags 提供 UI 参考，同时暴露“标签权威混淆”风险。
- 给 context pack 可视化导出提供 presentation-layer 参考。

打标签等级：

```yaml
tag_level: medium-borrow
borrow_value: medium
```

为什么不是 strong：

- 当前 VAKS 主线并没有批准 visual workbench implementation。
- 直接运行风险大于直接架构收益。
- root license 不明确。
- README 旧路径说明维护面有混乱。
- 未 runtime test。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | No direct LLM-maintained wiki contribution. | no |
| Dusk workbench | Strongest zone: visual workbench/action scripts. | candidate-only |
| source ingest | Paste/source-link sidecars can inform visual source capture. | adapt later |
| review queue | Can show review maps, but cannot review. | support only |
| schema / reviewed knowledge | `customData` should stay outside reviewed schema. | no |
| memory / dev context | Code/source-line links and visual tags can help dev context navigation. | support |
| feedback | No durable feedback ledger. | no |
| retrieval / cache | Link/group navigation can complement activation, not rank/trust. | support |
| API / MCP / agent access | No direct agent gateway. | no |
| viewer / workbench | Main reusable zone. | medium |
| publishing | SVG/export rendering may help presentation outputs. | cold/support |
| risk / anti-pattern | Script hooks, clipboard interception, root license ambiguity, stale docs. | strong risk note |

## 值得提炼的模式

### 1. Action / Feature Split

Actions are explicit user operations; Features are background engines mounted by hooks.

Boundary:

```text
separation improves clarity
separation does not approve runtime mutation
```

### 2. Hook Lifecycle

Feature engines register and unregister with `EA_Core`.

Boundary:

```text
hook lifecycle needs sandbox rules
hook success is not safety
```

### 3. Canvas-Local Metadata

`customData` stores UI semantics for mindmap, table, tags, chart, code.

Boundary:

```text
UI metadata stays UI metadata
reviewed knowledge stays reviewed layer
```

### 4. Source-Linked Visual Sidecar

Paste/link/code-line features can turn source fragments into navigable canvas elements.

Boundary:

```text
navigation is not support
visual grouping is not relation
```

### 5. Presentation Export

SVG/image export can produce shareable visual maps.

Boundary:

```text
presentation output is not source evidence
```

## 标签与量化

- domain: Obsidian Excalidraw custom scripts
- problem: enhance visual canvas interaction and source-linked navigation
- pattern: Action/Feature scripts with canvas-local metadata and hook lifecycle
- maturity: experimental
- complexity: high
- problem_fit: 3/5
- reuse_value: 3/5
- implementation_cost: 4/5
- integration_fit: 2/5 now, 4/5 if visual workbench is approved
- evidence_strength: 2/5
- reversibility: 4/5 if sandbox-only

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Visual sidecar can use `customData` for UI semantics. | Activation Tier is not truth tier. | candidate_relation | What fields are allowed as UI-only metadata? |
| Script hooks can create source-linked visual maps. | Source provenance and evidence support are separate. | candidate_relation with warning | How do we prevent visual source maps from acting as support? |
| Visual tags help navigation. | VAKS tags/review routing are not truth. | risk_of | How do we mark Excalidraw tags as local only? |
| Exported SVG can present context. | Evidence Packet requires source anchor/support. | risk_of | How do we label exports as presentation layer? |
| Runtime scripts need sandbox. | Agent/tool memory writes are quarantined. | candidate_relation | Should Obsidian custom scripts follow the same quarantine idea? |

## Support / Challenge Review

What supports it:

- README and Chinese README state the custom script purpose and modified-plugin dependency.
- The script tree contains many concrete Action/Feature scripts.
- Key scripts show `customData` and `EA_Core` hook lifecycle patterns.
- Paste/link/export/tag/code/mindmap scripts align with future visual context needs.

What challenges it:

- Root license absent.
- README links to missing old paths.
- Modified plugin dependency.
- Runtime not executed.
- Hooks intercept sensitive user flows: paste, links, export, keyboard, file writes.

Challenge severity:

```text
major for direct adoption
minor/acceptable for design-only candidate borrowing
```

Action readiness:

```text
not_ready
```

## 对当前项目的适配点

适配：

- Future VAKS visual workbench.
- Script sandbox design.
- Source-linked review map.
- Dev context canvas with code/source-line links.
- Presentation/export sidecar.

不适配：

- Main vault direct install.
- Treating canvas tags as VAKS tags.
- Automatic import of mindmap/table/chart structure into reviewed relations.
- Treating exported visuals as evidence support.

## 融合判断

- 结论：watch / adapt later
- Direct use: no
- Fork: no
- Design-only: yes
- Current branch value: medium for visual workbench/script sandbox only
- Whole architecture value: low-medium
- Risk: high runtime mutation and license/supply-chain ambiguity
- Next action: keep VAKS overlay as `medium-borrow`; reopen only when visual workbench or script sandbox work starts.

## 后续行动

- Keep as candidate-only reference.
- Use only as Support/Risk context for visual workbench tasks.
- Do not promote to `wiki/patterns` or `wiki/decisions` without later review.
- Do not run or install scripts in main VAKS vault during this intake.
