---
type: source
status: source-captured
title: "Obsidian Excalidraw Scripts"
source_id: 2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source
source_uri: https://github.com/Bowen-0x00/obsidian-excalidraw-scripts
source_url: https://github.com/Bowen-0x00/obsidian-excalidraw-scripts
source_type: repository
author: Bowen-0x00
publisher: GitHub
published_at:
updated_at: 2026-06-06
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: 1d0edb6beac48efe92b5a19c22cef701bc3a54e5
commit_time: "2026-05-24 22:05:51 +0800"
commit_subject: "1. add title in pick colors for extra colors 2. revise echarts hook 3. revise link hook"
default_branch: main
latest_tag: "1.0.1"
latest_tag_commit: 2cf8eb245589985879169ab54d36c775f5a16c13
source_status: active
license: none-detected-at-repository-root
dynamic_metadata_checked_at: 2026-06-07T03:10:56+08:00
dynamic_metadata:
  stars: 126
  forks: 8
  open_issues: 7
raw_location: raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source.md
snapshot_location: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-scripts-1d0edb6beac48efe92b5a19c22cef701bc3a54e5.zip
snapshot_sha256: B2CB8E4C4BE76FD05F7869263BB6872363F614DC893B9081273D8DF2395E9E70
processing_mode: immediate
processing_level: medium
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - obsidian
  - excalidraw
  - custom-scripts
  - visual-workbench
  - canvas-sidecar
  - ea-core-hooks
  - canvas-local-metadata
  - markdown-mindmap-bridge
  - source-linked-overlays
projects:
  - verified-action-knowledge-system
source_family:
  - obsidian-scripts
  - visual-workbench
  - canvas-sidecar
upstream_sources:
  - https://github.com/zsviczian/obsidian-excalidraw-plugin
  - https://github.com/Bowen-0x00/obsidian-excalidraw-plugin-ymjr
  - https://github.com/Bowen-0x00/obsidian-excalidraw-example-vault
verification_status: primary-source-captured
candidate_relation_suggestions:
  - target: "[[Activation Tier]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The scripts implement visual activation helpers through canvas-local metadata and hook-based rendering."
  - target: "[[Source Intake]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Paste/link/export scripts show source-linked visual sidecar mechanics that could inform future source context maps."
  - target: "[[Action Basis]]"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "Canvas tags, diagrams, exports, and generated structures could be mistaken for reviewed knowledge or evidence support."
tags:
  - obsidian-excalidraw-scripts
  - obsidian
  - excalidraw
  - custom-scripts
  - visual-workbench
  - canvas-sidecar
  - candidate-only
---

# Obsidian Excalidraw Scripts Source Record

## 为什么收录

`Bowen-0x00/obsidian-excalidraw-scripts` 是作者的 Obsidian Excalidraw custom scripts 仓库。它和前一个 `obsidian-excalidraw-example-vault` 是配套关系：example vault 是 demo/sandbox，这个仓库是脚本集合本体。

对 VAKS 来说，它值得收录，但不能直接吸收：

```text
Action scripts
-> Feature engines
-> EA_Core hooks
-> element customData
-> paste/link/tag/mindmap/code/export/table visual behavior
```

最有价值的地方，是它把 Excalidraw 画布变成可交互的 visual sidecar。最危险的地方，也是同一件事：这些脚本会改 UI、改元素、读剪贴板、接管链接和粘贴、挂钩导出流程。

## 来源信息

- Repository: `Bowen-0x00/obsidian-excalidraw-scripts`
- URL: https://github.com/Bowen-0x00/obsidian-excalidraw-scripts
- Checked commit: `1d0edb6beac48efe92b5a19c22cef701bc3a54e5`
- Checked branch: `main`
- Commit time: `2026-05-24 22:05:51 +0800`
- Commit subject: `1. add title in pick colors for extra colors 2. revise echarts hook 3. revise link hook`
- Latest tag observed: `1.0.1`
- Repository root license: none detected
- Script frontmatter MIT count: 125 of 127 script markdown files
- GitHub dynamic metadata checked: `2026-06-07T03:10:56+08:00`
- Stars / forks / open issues at check: `126 / 8 / 7`
- Snapshot: `raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-scripts-1d0edb6beac48efe92b5a19c22cef701bc3a54e5.zip`
- Snapshot SHA256: `B2CB8E4C4BE76FD05F7869263BB6872363F614DC893B9081273D8DF2395E9E70`
- Inspected mode: source/docs/scripts read; no Obsidian runtime execution; no plugin/script execution.

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

This source record is provenance and findability only. It does not create reviewed patterns, truth confidence, relation strength, or action basis.

## Repo Shape

Observed file-type counts:

| Extension | Count |
|---|---:|
| `.md` | 129 |
| `.gif` | 26 |
| `.svg` | 8 |
| `.excalidrawlib` | 2 |
| `.gitignore` | 1 |
| `.jpg` | 1 |
| `.json` | 1 |
| `.png` | 1 |

Observed script category shape:

```text
127 script markdown files
43 script categories under Scripts/
Action-* files: user-triggered scripts
Feature-* files: autorun/background engines
```

Notable categories:

- `mindmap`
- `code-highlight`
- `clipboard`
- `link`
- `tag`
- `export`
- `echarts`
- `table`
- `outline`
- `library`
- `text`
- `connection`
- `arrow`
- `callout`
- `checkbox`

README hygiene note:

```text
README still contains 41 links to Scripts/Encrypted and 1 link to Templaters, but those directories were not present in the checked tree.
```

## Source / Code Anchors

| Anchor | What exists | 初步看点 | Boundary |
|---|---|---|---|
| `README.md:5-11` | Personal repository of Obsidian Excalidraw custom scripts; some scripts rely on modified Excalidraw; demo vault linked. | Clear source identity and dependency relationship. | README does not establish runtime safety. |
| `README.md:14-40` | Feature table lists mindmap, md/ex mindmap, code highlight, export SVG, link highlight, element tags, etc. | Visual workbench feature catalog. | Several README links point to missing old paths. |
| `docs/README_ZH.md:19-40` | Chinese feature table mirrors the main README. | Confirms intended usage in Chinese. | Still orientation only. |
| `Scripts/index.md:1-240` | Generated list of available scripts by category. | Good high-level script inventory. | Index does not prove all scripts work. |
| `Scripts/mindmap/Feature-Mindmap-Engine.md:2-15` | Background mindmap engine with `customData.mindmap`, collapse/layout/keyboard/navigation, autorun true. | Strong canvas-local metadata pattern. | Mindmap hierarchy is not reviewed relation. |
| `Scripts/mindmap/Feature-Mindmap-Engine.md:160-214`, `1255-1267` | Parent/root/level state is read/written; hooks register pointer/key/drag/delete/render handlers. | Feature engine owns UI lifecycle through hooks. | High runtime mutation surface. |
| `Scripts/mindmap/Action-Export-Mindmap-To-Md.md:55-87`, `145-150` | Exports selected mindmap to Markdown, including `#^group=` embeds, then modifies/creates a vault file. | Markdown/canvas bridge with anchors. | Exported outline is not reviewed knowledge. |
| `Scripts/mindmap/Action-Import-Mindmap-From-Clipboard.md:140-169`, `248-306` | Reads clipboard outline, sets `customData.mindmap`, calls `MindmapAPI.runLayout`. | Clipboard-to-canvas candidate structure. | Clipboard input is untrusted raw input. |
| `Scripts/code-highlight/Feature-Code-Highlight-Engine.md:10-11`, `122`, `241`, `261-268` | Code highlight render/export/paste hooks; source-line link via `ymjr://open?...line=...`. | Dev-context source navigation overlay. | Highlight/link is navigation, not validation. |
| `Scripts/clipboard/Feature-Paste-Engine.md:2-14`, `247-280` | Paste engine parses BookxNote/Zotero/Eagle/ymjr protocols into linked Excalidraw elements and code-highlight metadata. | Source/excerpt capture into visual canvas. | Clipboard/protocol parsing can import bad or private data. |
| `Scripts/link/Feature-Link-Engine.md:2-15`, `125-132` | Link engine intercepts `onLinkClick`, handles same-file `#^group=` navigation and back stack. | Visual source navigation and return path. | Link routing is UI behavior, not evidence support. |
| `Scripts/tag/Action-Set-Tags.md:2-14`, `55-74` | Floating tag editor writes tags to selected element `customData.tags`. | Useful local visual tags. | These are not VAKS taxonomy/review tags. |
| `Scripts/export/Feature-Export-Embeddable.md:2-14`, `154-159`, `170` | Exports embeddable/Markdown/web content using html2canvas into SVG. | Visual export pipeline. | Exported screenshot is not source text or support evidence. |
| `Scripts/echarts/Feature-Echarts-Engine.md:2-14`, `433`, `569-575` | ECharts engine stores chart data in `customData.echarts`, hooks paste/render/export. | Data visualization sidecar. | Chart render is not source verification. |
| `Scripts/table/Feature-Table-Engine.md:7-12`, `109-138`, `430-436` | Table engine uses `customData.table` and hooks WYSIWYG/transform/drag/key events. | Canvas-local structured UI metadata. | Table state is UI state. |

## 初步看点

- The repository is a concrete catalog of Excalidraw custom scripts, not just a demo vault.
- The Action/Feature split is a useful operating pattern: user-triggered actions create or edit metadata; background engines render, route, or maintain behavior.
- `customData` is repeatedly used as a local semantic cache: `mindmap`, `codeHighlight`, `tags`, `echarts`, `table`.
- `EA_Core.registerHook` / `unregisterHook` gives the scripts a lifecycle shape that VAKS could study before designing a plugin/script sandbox.
- Paste/link/export scripts show how visual canvases can become source-linked context maps.

## 明显疑点

- No root license file was detected, despite many script frontmatters saying `license: MIT`.
- README still links to missing `Scripts/Encrypted` and `Templaters` paths in the checked tree.
- Some scripts rely on a modified Excalidraw plugin; the repo does not make direct VAKS compatibility clear.
- Several engines inject or bundle large third-party libraries such as highlight.js/html2canvas/ECharts; license and supply-chain review is separate.
- Runtime was not executed; source-level inspection cannot verify Obsidian/plugin compatibility.
- Hooks can mutate canvas state, intercept paste/link/export, create/modify vault files, and read clipboard content.

## 可抽取 Candidate Points

1. Action scripts and Feature engines can be separated to keep user-triggered mutations and background rendering behavior understandable.
2. Canvas-local `customData` can hold UI semantics without polluting VAKS reviewed schema.
3. Paste/link/export hooks can create a visual sidecar for source navigation, but they must remain non-authoritative.
4. Element-level visual tags are useful for local navigation, but must not be confused with VAKS tags, truth labels, or reviewed taxonomy.
5. Script/plugin workflows need a sandbox, compatibility check, and license/supply-chain review before main-vault use.

## 当前处理等级

```text
medium
```

Upgrade to heavy only if VAKS starts a visual workbench or Obsidian script sandbox implementation.

## 下一步

- Keep as candidate-only visual workbench implementation reference.
- Use the project overlay for VAKS-specific borrow / non-borrow tags.
- Do not run or install these scripts in the main VAKS vault from this intake.
