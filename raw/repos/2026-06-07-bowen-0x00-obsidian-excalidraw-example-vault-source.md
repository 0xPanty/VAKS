---
type: source
status: source-captured
title: "Obsidian Excalidraw Example Vault"
source_id: 2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source
source_uri: https://github.com/Bowen-0x00/obsidian-excalidraw-example-vault
source_url: https://github.com/Bowen-0x00/obsidian-excalidraw-example-vault
source_type: repository
author: Bowen-0x00
publisher: GitHub
published_at:
updated_at: 2026-05-23
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: 3da586cc520d77c7f250d3765bf1fca1c91d70bd
commit_time: "2026-05-19 11:50:29 +0800"
commit_subject: "fix code highlight error"
default_branch: main
latest_release: none
source_status: active
license: none-detected-at-repository-root
dynamic_metadata_checked_at: 2026-06-07T02:44:42+08:00
dynamic_metadata:
  stars: 110
  forks: 11
  open_issues: 2
raw_location: raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source.md
snapshot_location: raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-example-vault-3da586cc520d77c7f250d3765bf1fca1c91d70bd.zip
snapshot_sha256: 53EB073E2E740C73CD1368B0CC77CB9A84501B5ABB59B8FA403FEE56B30BB0AA
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
  - visual-workbench
  - canvas-sidecar
  - markdown-mindmap-bridge
  - code-highlight-overlay
  - modified-plugin-bundle
projects:
  - verified-action-knowledge-system
source_family:
  - obsidian-vault
  - visual-workbench
  - demo-vault
upstream_sources:
  - https://github.com/Bowen-0x00/obsidian-excalidraw-plugin-ymjr
  - https://github.com/Bowen-0x00/obsidian-excalidraw-scripts
verification_status: primary-source-captured
candidate_relation_suggestions:
  - target: "[[Activation Tier]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The repository shows how visual canvases can activate nearby context without becoming reviewed knowledge."
  - target: "[[Source Intake]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Markdown-to-canvas and canvas-to-markdown flows suggest a source-anchored visual sidecar path."
  - target: "[[Action Basis]]"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "Canvas layout, visual proximity, and plugin-generated metadata could be mistaken for reviewed relation or action-ready support."
tags:
  - obsidian-excalidraw-example-vault
  - obsidian
  - excalidraw
  - visual-workbench
  - canvas-sidecar
  - candidate-only
---

# Obsidian Excalidraw Example Vault Source Record

## 为什么收录

`Bowen-0x00/obsidian-excalidraw-example-vault` 是一个打包好的 Obsidian 示例库，包含改版 Excalidraw 插件、若干自定义脚本、画布示例、库设置和附件素材。它不是 VAKS 的知识架构参考，也不是要直接 fork 的主 vault。

它值得收录的原因很窄：

```text
Obsidian markdown
-> Excalidraw canvas
-> element customData
-> mindmap / code highlight / source-line link visual overlay
-> demo vault for trying visual workflows
```

对 VAKS 来说，它主要是未来“可视化侧车 / 画布工作台”的候选参考。它不能作为 reviewed knowledge、truth、action basis 或主线插件方案。

## 来源信息

- Repository: `Bowen-0x00/obsidian-excalidraw-example-vault`
- URL: https://github.com/Bowen-0x00/obsidian-excalidraw-example-vault
- Checked commit: `3da586cc520d77c7f250d3765bf1fca1c91d70bd`
- Checked branch: `main`
- Commit time: `2026-05-19 11:50:29 +0800`
- Commit subject: `fix code highlight error`
- Latest release: none found
- Repository root license: none detected
- GitHub dynamic metadata checked: `2026-06-07T02:44:42+08:00`
- Stars / forks / open issues at check: `110 / 11 / 2`
- Snapshot: `raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-example-vault-3da586cc520d77c7f250d3765bf1fca1c91d70bd.zip`
- Snapshot SHA256: `53EB073E2E740C73CD1368B0CC77CB9A84501B5ABB59B8FA403FEE56B30BB0AA`
- Files in checked tree outside `.git`: 331
- Inspected mode: source/docs/config read; no Obsidian runtime execution; no plugin/script execution.

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
| `.md` | 97 |
| `.svg` | 82 |
| `.png` | 81 |
| `.json` | 29 |
| `.sample` | 14 |
| `.js` | 13 |
| `.css` | 12 |
| no extension | 12 |
| `.excalidrawlib` | 8 |
| `.gif` | 4 |
| `.woff2` | 3 |

Notable source surfaces:

- `README.md`
- `docs/README_ZH.md`
- `.obsidian/plugins/obsidian-excalidraw-plugin-ymjr/manifest.json`
- `Excalidraw/Scripts/Downloaded(Custom)/Feature-Mindmap-Engine.md`
- `Excalidraw/Scripts/Downloaded(Custom)/Action-Create-Mindmap.md`
- `Excalidraw/Scripts/Downloaded(Custom)/Action-Export-Mindmap-To-Md.md`
- `Excalidraw/Scripts/Downloaded(Custom)/Action-Import-Mindmap-From-Clipboard.md`
- `Excalidraw/Scripts/Downloaded(Custom)/Feature-Code-Highlight-Engine.md`
- `Excalidraw/Scripts/Downloaded(Custom)/Action-Toggle-Code-Highlight.md`
- `example/思维导图/导出.md`
- `example/代码高亮/代码高亮.excalidraw.md`
- `Excalidraw关系.excalidraw.md`

## Source / Code Anchors

| Anchor | What exists | 初步看点 | Boundary |
|---|---|---|---|
| `README.md:5-11` | Repo says it is a packaged Obsidian vault with modified Excalidraw plugin, custom scripts, and pre-made canvas examples. | Clear demo-vault positioning. | README is source identity, not runtime proof. |
| `README.md:17-32` | Backup warning and porting note: some features require custom scripts plus modified plugin; dependency table is incomplete. | Good risk signal for any direct adoption. | Incomplete dependency map blocks direct copy. |
| `docs/README_ZH.md:4-30` | Chinese README repeats packaged vault, direct Obsidian open, backup, and feature-porting dependency caveat. | Confirms intended user flow and dependency risk. | Does not prove compatibility with current VAKS vault. |
| `.obsidian/plugins/obsidian-excalidraw-plugin-ymjr/manifest.json:2-10` | Bundled plugin id/name/version/help URL: `obsidian-excalidraw-plugin-ymjr`, `Excalidraw-ymjr`, `2.22.0-5`. | Modified plugin is part of the example environment. | Bundled plugin is not VAKS-approved runtime. |
| `Excalidraw关系.excalidraw.md:11-19`, `503-507`, `714-719` | Example canvas points to modified plugin and says scripts depend on modified plugins. | Visual map of plugin/script dependency. | Canvas statement is dependency orientation only. |
| `Feature-Mindmap-Engine.md:7-12` | Background engine for `customData.mindmap`: collapse/expand icons, keyboard node creation, direction-key navigation, layout, `window.MindmapAPI`. | Canvas-local semantic metadata can drive interaction. | Canvas metadata is not reviewed relation. |
| `Feature-Mindmap-Engine.md:748-763` | `window.MindmapAPI.runLayout` calls `MindMapLayouter` and commits layout changes. | Visual layout can be recomputed from element metadata. | Layout state is UI state, not truth. |
| `Feature-Mindmap-Engine.md:1208-1218` | Hooks register/unregister pointer, key, drag, delete, and render handlers through `window.EA_Core`. | Modified plugin hook surface is central. | High runtime risk without plugin review. |
| `Action-Create-Mindmap.md:98-145`, `270-277` | Action reads shared engine settings, toggles `customData.mindmap`, stores root settings, and invokes layout API. | Small action scripts write element-level semantic hints. | Script mutation must not write reviewed knowledge. |
| `Action-Export-Mindmap-To-Md.md:66` and `example/思维导图/导出.md:12-23` | Export finds mindmap root and emits Markdown embeds like `![[...#^group=...]]`. | Markdown <-> canvas bridge can preserve anchors. | Exported outline is candidate orientation only. |
| `Action-Import-Mindmap-From-Clipboard.md:96`, `251`, `291-306` | Import reads settings, sets `customData.mindmap`, and calls `window.MindmapAPI.runLayout`. | Clipboard/outline can become a structured canvas sidecar. | Imported structure is not a reviewed graph. |
| `Feature-Code-Highlight-Engine.md:7-10`, `122-126`, `218-221`, `262-263` | Background engine renders `customData.codeHighlight` elements using highlight.js and SVG export hooks. | Code snippets can become visual overlays. | Rendered code display is not source validation. |
| `example/代码高亮/代码高亮.excalidraw.md:28`, `65` | Example writes `ymjr://open?app=code...&line=...` links to code/file locations. | Source-line links are useful as visual navigation anchors. | Local file links are environment-specific. |

## 初步看点

- `customData` is used as canvas-local metadata, not just visual decoration.
- Mindmap scripts show a Markdown/outline <-> Excalidraw bridge with group anchors.
- Code-highlight scripts show a source-line linked visual overlay.
- Packaged demo vault is a useful onboarding/sandbox shape for visual tooling.
- The strongest value is a visual sidecar concept: a canvas can activate nearby context without becoming the authority layer.

## 明显疑点

- No top-level repository license was detected; custom scripts may carry their own license text, but direct reuse is not cleared by this source card.
- Some features depend on a modified Excalidraw plugin, and README says the feature-script dependency table is incomplete.
- The review did not run the vault in Obsidian, did not execute custom scripts, and did not validate plugin compatibility.
- Bundled plugins/assets create a supply-chain and maintenance surface.
- Canvas proximity, arrows, layout, mindmap hierarchy, and generated embeds can be confused with reviewed relations if imported carelessly.

## 可抽取 Candidate Points

1. Visual sidecars can preserve orientation and navigation without mutating reviewed knowledge.
2. Excalidraw element `customData` can carry local UI semantics such as mindmap membership or code-highlight state.
3. Markdown <-> canvas bridges should preserve anchors back to source notes or elements.
4. Source-line visual links can help developer context activation, but cannot count as evidence support.
5. Demo vaults are useful for trying risky plugin/script workflows away from the main vault.

## 当前处理等级

```text
medium
```

Upgrade to heavy only if VAKS actively starts a visual workbench / Excalidraw sidecar implementation and we need runtime validation inside Obsidian.

## 下一步

- Keep as candidate-only visual workbench reference.
- Use the project overlay for VAKS-specific borrow / non-borrow tags.
- Do not copy plugin bundles or run scripts in the main VAKS vault without a separate approved test.
