---
type: source
status: source-captured
title: "Bowen-0x00/obsidian-excalidraw-plugin-ymjr"
source_id: "repo:github:Bowen-0x00/obsidian-excalidraw-plugin-ymjr@3fa4ace442c3d455c05172e1b1894033572e6b47"
source_uri: "github:Bowen-0x00/obsidian-excalidraw-plugin-ymjr"
source_url: "https://github.com/Bowen-0x00/obsidian-excalidraw-plugin-ymjr"
source_type: repository
author: "Bowen-0x00"
publisher: GitHub
published_at:
updated_at: 2026-06-06T08:00:00Z
captured_at: 2026-06-07T03:17:28+08:00
captured_by: Codex
version_or_commit: "3fa4ace442c3d455c05172e1b1894033572e6b47"
source_status: active
raw_location: "raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-plugin-ymjr-3fa4ace442c3d455c05172e1b1894033572e6b47.zip"
snapshot_sha256: "E91EEDE1A56FF9AC17B68F4EB5E4F7767957CB31228094D2C0FD235F23EA0149"
processing_mode: repo-intake
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
formalization_status: raw-only
topics:
  - obsidian
  - excalidraw
  - visual-pkm
  - plugin-fork
  - canvas-workbench
  - custom-scripts
projects:
  - VAKS
source_family: bowen-excalidraw-cluster
upstream_sources:
  - "https://github.com/zsviczian/obsidian-excalidraw-plugin"
verification_status: metadata-and-source-inspected
candidate_relation_suggestions: []
tags:
  - repo-source
  - obsidian-excalidraw
  - visual-workbench
  - modified-plugin-risk
  - candidate-only
---

# 来源记录：Bowen-0x00/obsidian-excalidraw-plugin-ymjr

## 为什么收录

用户连续给了 Bowen 的 Excalidraw 三件套：example vault、scripts、plugin fork。本仓库是其中的改版插件本体，README 明说当自定义脚本无法满足需求时才改动原 `obsidian-excalidraw-plugin`，并且需要和自定义 scripts 搭配使用。

对 VAKS 的价值不是直接安装插件，而是理解“视觉画布 sidecar 需要哪些插件级能力”：元素级 tag / customData、鼠标和键盘 hook、导出时渲染本地 md/code/echarts、局部引用跳转、图层、固定元素、连接点、素材库按需加载等。

## 来源信息

- 作者：Bowen-0x00
- 发布方：GitHub
- 原始链接：https://github.com/Bowen-0x00/obsidian-excalidraw-plugin-ymjr
- default_branch: `main`
- checked_commit: `3fa4ace442c3d455c05172e1b1894033572e6b47`
- commit_time: `2026-05-24T22:07:12+08:00`
- commit_subject: `2.23.5-1`
- latest_release: `2.23.5-1`
- latest_release_published_at: `2026-05-24T14:08:47Z`
- GitHub metadata checked_at: `2026-06-07T03:17+08:00`
- stars: `163`
- forks: `14`
- open_issues: `14`
- license: none reported by GitHub API; no root LICENSE file observed
- upstream check: official `zsviczian/obsidian-excalidraw-plugin` release API showed `2.23.10` published at `2026-06-06T17:37:14Z`, so this fork was behind official upstream at capture time.
- local_clone: `C:\Users\Administrator\.codex\repo-research\Bowen-0x00-obsidian-excalidraw-plugin-ymjr-20260607-031728`
- snapshot: `raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-plugin-ymjr-3fa4ace442c3d455c05172e1b1894033572e6b47.zip`
- snapshot_sha256: `E91EEDE1A56FF9AC17B68F4EB5E4F7767957CB31228094D2C0FD235F23EA0149`

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

此 source card 只记录来源和可追溯锚点，不代表 VAKS 采纳该插件，也不代表其中任何功能已经通过安全、运行或证据审查。

## 仓库形态

```text
files: 42
main.js: 8,681,564 bytes
styles.css: 202,684 bytes
src/main.js: same SHA256 as root main.js
src/styles.css: same SHA256 as root styles.css
manifest.json: same SHA256 as src/manifest.json
src/obsidian-excalidraw-plugin.7z: 4,069,475 bytes
```

Observed file type counts:

```text
.gif 24
.PNG 6
.css 2
.js 2
.json 2
.md 2
.7z 1
.jpg 1
.svg 1
.gitignore 1
```

`src/obsidian-excalidraw-plugin.7z` was not extracted in this run because local `7z`, `py7zr`, `libarchive`, and `patoolib` were unavailable; Windows `tar` reported unsupported LZMA codec. The archive is therefore retained as source material but not used as a trusted source-code anchor.

## Source / Code Anchor Matrix

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:3-7` | States this is a modified version of upstream Obsidian Excalidraw, changed when custom scripts were insufficient. | Plugin-level changes are used to unlock behavior scripts cannot provide alone. | Provenance only; not direct adoption. |
| `README.md:11-13` | Links to companion `obsidian-excalidraw-scripts` and demo vault. | Confirms this plugin is part of a three-piece visual workflow cluster. | Cross-repo relation is candidate context only. |
| `README.md:20-80` / `docs/README_ZH.md:19-79` | Feature list: fonts, tags, mouse/keyboard hooks, mindmap, table resize, layers, Chinese wrap fix, thumbnail, hover hook, SVG export, library loading, code highlight, ECharts, calendar, flow animation, highlight link. | Useful feature map for future VAKS visual sidecar / canvas workbench. | Feature claims were not runtime-tested. |
| `README.md:87-103` / `docs/README_ZH.md:85-101` | Backup warning, manual/BRAT install, disable original Excalidraw, use matching scripts folder. | Direct use can conflict with official Excalidraw and requires backup discipline. | Risk anchor; do not install in main VAKS vault. |
| `manifest.json:2-11` | Plugin id `obsidian-excalidraw-plugin-ymjr`, version `2.23.5-1`, minAppVersion `1.8.7`, modified author description, not desktop-only. | Confirms release identity and modified plugin metadata. | Metadata only. |
| `git log --max-count=35` | Recent commits include hook refactor, paste-engine fix, upstream restore, arrow/snap/binding fixes, latex and library features. | Shows ongoing fork maintenance around hooks, binding, snap, render, library. | Commit messages are hints, not reviewed implementation evidence. |
| `main.js` bundle search | Search found `customData` 57, `tags` 49, `EA_Core` 6, `exportSVG` 15, `onKeyDown` 20, `onMouseMove` 5, `customData.tags` 3. | Confirms bundle contains the symbols expected from README and companion scripts. | Minified bundle gives weak line anchors; no direct code reuse. |
| `main.js` byte `7138011` | `addAppendUpdateCustomData` snippet mutates `element.customData`. | Canvas-local metadata channel is central. | Candidate design only. |
| `main.js` byte `7338334` | Snippet filters `scene.elements` by `customData.tags` and emits markdown tags. | Element tags can be exported or surfaced, but they are local canvas tags. | Must not become VAKS truth tags. |
| `main.js` byte `7750589` | Snippet dispatches `window.EA_Core.dispatchSync("onAfterLoadScene", {view:this})`. | Hook bus supports script-driven lifecycle. | Sandbox-only if ever tested. |
| `main.js` byte `7183122` | Snippet involves `createSVG`, `exportSVGFont`, embedded files, and SVG export path. | Export/render enhancements may inspire visual sidecar exports. | Exported visuals are not evidence support. |

## 初步看点

- 这是 scripts/example-vault 的插件底座，解释了为何 scripts 仓库里有大量 hook、mindmap、tag、code-highlight、echarts、export 逻辑。
- 设计价值集中在“把画布元素变成可交互、可局部引用、可导出的视觉工作台”，而不是知识验证。
- 对 VAKS 有用的是 sidecar/workbench 思路：画布可以作为项目理解和导航界面，但不能升级成 truth layer。

## 明显疑点

- 没有 root LICENSE，GitHub API license 为 null；虽然上游插件有自己的许可背景，但本 fork 的可复用许可边界没有在根目录明确。
- 仓库主要是打包产物和演示图片，不是清晰的源码工程；`main.js` 是 minified/bundled 形态。
- 需要关闭官方 Excalidraw 插件并启用 fork，主库直接安装风险高。
- 捕获时 fork 版本 `2.23.5-1` 已落后官方 upstream `2.23.10`。
- 功能未在本机 Obsidian/VAKS vault 中运行测试。

## 可抽取 Candidate Points

1. 当脚本层能力不足时，插件层 hook 可以补足画布交互、渲染、导出和元素元数据能力。
2. `customData` 可以作为画布内局部语义存储，但不能直接变成 VAKS 的 reviewed schema 或 tag taxonomy。
3. 元素级 tag、link、highlight、thumbnail、layer、fixed element 可以作为 visual workbench 的导航/关注机制。
4. 导出 SVG 时渲染本地 md、code、echarts 的思路有助于“可视化快照”，但不能作为 Evidence Packet 或 action support。
5. 改版插件直接替换官方插件，是强风险路径；未来只能在 sandbox vault / branch 中试。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- VAKS 明确要做 Excalidraw visual sidecar / canvas workbench。
- 有单独 sandbox vault 可以运行测试，不影响主 Obsidian vault。
- root license、上游同步状态、插件安全边界、数据保存行为被审查。
- 能对照官方插件源码或展开 7z 源码归档，定位具体改动。

## 候选关系建议

```yaml
candidate_relation_suggestions:
  - target: "VAKS visual-workbench / canvas-sidecar candidate"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Shows plugin-level hooks and element metadata needed by companion Excalidraw scripts."
    source_anchor: "README.md:20-80; manifest.json:2-11; main.js bundle symbol search"
    evidence_support:
      span_supports_target: partial
      evidence_role: design-orientation
      reviewer_note: "Needs sandbox runtime review before any adoption."
    suggested_at: 2026-06-07
```

## 下一步

- Keep as candidate-only visual workbench reference.
- If revisited, inspect official upstream `zsviczian/obsidian-excalidraw-plugin` and compare fork deltas.
- Do not install or load it in the main VAKS Obsidian vault without explicit sandbox plan.
