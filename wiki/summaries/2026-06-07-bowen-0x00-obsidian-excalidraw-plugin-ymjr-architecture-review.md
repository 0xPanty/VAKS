---
type: library_review
status: candidate
library_name: "obsidian-excalidraw-plugin-ymjr"
repo_url: "https://github.com/Bowen-0x00/obsidian-excalidraw-plugin-ymjr"
source_url: "raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-source.md"
checked_commit: "3fa4ace442c3d455c05172e1b1894033572e6b47"
commit_time: "2026-05-24T22:07:12+08:00"
source_status: active
reviewed_at: 2026-06-07T03:40:00+08:00
domain: obsidian-visual-workbench
related_projects:
  - VAKS
current_branch: source-intake / project-overlay / visual-workbench candidate
extracted_patterns:
  - plugin-level-canvas-hooks
  - element-local-customdata
  - visual-sidecar-export
  - modified-plugin-risk
fusion_decision: watch
confidence: medium
evidence_count: 9
cross_validated_with:
  - "Bowen-0x00/obsidian-excalidraw-scripts"
  - "Bowen-0x00/obsidian-excalidraw-example-vault"
negative_evidence:
  - no-root-license
  - minified-bundle-dominant
  - direct-plugin-replacement
  - upstream-drift
extension_potential: sandbox-only
knowledge_status: candidate
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
action_basis_allowed: false
truth_mutation_allowed: false
relations: []
tags:
  - architecture-review
  - candidate-only
  - visual-workbench
  - medium-borrow
---

# 库分析：obsidian-excalidraw-plugin-ymjr

## 它解决什么问题

它把官方 Obsidian Excalidraw 插件改成一个更适合作者自定义 scripts 的视觉 PKM 工作台底座。核心问题不是“保存知识”，而是“当脚本层不够时，怎样让画布元素支持更多交互、局部元数据、导出渲染和视觉控件”。

## 核心设计

```text
official Excalidraw plugin fork
-> plugin-level changes
-> custom scripts hook into modified capabilities
-> demo vault shows workflows
```

这说明 Bowen 的三件套不是三个独立项目：

- `obsidian-excalidraw-plugin-ymjr`: 插件底座。
- `obsidian-excalidraw-scripts`: 功能脚本。
- `obsidian-excalidraw-example-vault`: 演示库。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:3-18` | Modified upstream plugin, changed where custom scripts were insufficient, linked scripts and demo vault. | Plugin layer exists to extend what scripts alone cannot do. | Candidate design only. |
| `README.md:20-80` | Long feature list: fonts, tags, hooks, mindmap, layers, thumbnail, export, library, code, ECharts, calendar, flow animation. | Visual workbench capability map. | README claims not runtime-tested. |
| `README.md:87-103` | Backup warning, manual/BRAT install, disable original plugin, use matching scripts folder. | Direct use has operational risk and plugin conflict. | Strong non-borrow anchor for main vault. |
| `docs/README_ZH.md:19-79` | Chinese feature list mirrors README. | Confirms intended Chinese Obsidian usage context. | Documentation only. |
| `manifest.json:2-11` | id/version/minAppVersion/modified author/helpUrl. | Installed plugin identity is distinct from official plugin. | Metadata only. |
| `git log --max-count=35` | Recent commits mention hook refactor, paste-engine fix, upstream restore, snap/binding/arrow/latex/library fixes. | Fork is active and touches interaction mechanics. | Commit message evidence only. |
| `main.js` bundle symbol counts | `customData` 57, `tags` 49, `EA_Core` 6, `exportSVG` 15, `onKeyDown` 20. | Supports the existence of metadata/hook/export mechanisms. | Minified bundle, weak code anchor. |
| `main.js` byte snippets | `addAppendUpdateCustomData`, `customData.tags`, `EA_Core.dispatchSync("onAfterLoadScene")`, `createSVG` path. | Candidate mechanism anchors. | No code reuse without readable source review. |
| GitHub metadata | Release `2.23.5-1`; official upstream had `2.23.10` by 2026-06-06. | Fork is behind upstream at capture time. | Risk evidence. |

## 当前支线价值

当前支线：

```text
VAKS source intake / project overlay / possible visual workbench
```

它对当前支线：

```text
refines + risk_of
```

具体价值：

- Refines: shows what a future canvas-sidecar might need beyond normal notes and scripts.
- Refines: explains why the companion scripts store `customData` and need hook-style lifecycle events.
- Risk_of: modified plugin replacement can confuse source authority, tags, evidence, and vault stability if used in main VAKS.

风险：

- Direct install requires disabling original Excalidraw.
- No root license observed.
- Bundled/minified code makes delta review difficult.
- Upstream official plugin was newer at capture time.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | No direct value for raw/wiki/index/log simplicity. | no |
| Dusk workbench | Strong candidate inspiration for a visual project workbench. | adapt |
| source ingest | Can visualize source clusters, but cannot replace source cards. | watch |
| review queue | Canvas tags may help local review navigation, not review state. | adapt carefully |
| schema / reviewed knowledge | `customData` must not become reviewed schema. | no |
| memory / dev context | Could support visual context maps for Support/Risk/Cold references. | watch |
| feedback | Hover/highlight could surface feedback/risk warnings visually. | watch |
| retrieval / cache | No direct retrieval mechanism. | no |
| API / MCP / agent access | Hook bus hints at script extension, but no VAKS agent boundary. | watch |
| viewer / workbench | Main candidate value: interactive canvas sidecar. | adapt |
| publishing | Export/render features may help visual summaries. | watch |
| risk / anti-pattern | Direct plugin replacement and canvas tag authority confusion. | adopt risk warning |

## 值得提炼的模式

1. **Script-layer vs plugin-layer split**

   Start with scripts and official plugin. Only introduce plugin-layer changes when the target interaction cannot be achieved otherwise.

2. **Canvas-local semantics**

   Store interaction state and local visual tags in element metadata, but keep them outside the knowledge truth layer.

3. **Visual export as briefing**

   Render md/code/chart into SVG for readable summaries, but treat the export as presentation, not evidence support.

4. **Modified plugin quarantine**

   Forked plugins that replace official plugins belong in sandbox vaults until licensing, upstream drift, data safety, and runtime behavior are reviewed.

## 标签与量化

- domain: Obsidian visual workbench
- problem: canvas interaction and visual sidecar extension
- pattern: plugin-level hook substrate
- maturity: experimental / fork-maintained
- complexity: high
- problem_fit: 3/5
- reuse_value: 3/5
- implementation_cost: 4/5
- integration_fit: 2/5
- evidence_strength: 2/5
- reversibility: 4/5 for design-only, 1/5 for direct install

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Canvas sidecar can improve project comprehension. | VAKS treats dashboards/workbenches as non-truth surfaces. | candidate_relation | How can a visual sidecar help without becoming authority? |
| Element tags can organize a canvas. | VAKS has strict candidate/reviewed/action-basis boundaries. | scope_mismatch risk | How to prevent canvas tags from looking like reviewed tags? |
| Plugin hook layer enables richer scripts. | VAKS avoids overbuilding before need. | review_due if pursued | Which abilities are impossible with official plugin/scripts only? |
| Exported SVG can include md/code/chart rendering. | Evidence support must anchor to raw/stable source material. | risk_of | How to label visual exports as presentation only? |

边界：

- Similarity is not support.
- Hook availability is not adoption readiness.
- Canvas metadata is not reviewed relation.

## Support / Challenge Review

- What supports it: README and manifest, companion repo relationship, bundle symbol search, recent commit messages.
- What challenges it: no root license, minified bundle, unextracted 7z, direct plugin replacement, upstream drift, no runtime test.
- Challenge severity: major for direct use, minor/acceptable for design-only reference.
- Scope limits: VAKS visual workbench / sidecar only.
- Known risks: authority confusion, plugin instability, source hygiene, fork drift.
- Review again when: VAKS explicitly starts an Excalidraw sandbox or visual workbench branch.
- Action readiness: not_ready.

## 对当前项目的适配点

- Keep as `support_with_required_risk` dev-context reference.
- Use it to label future visual-sidecar requirements:
  - element metadata
  - local tags
  - hook lifecycle
  - export renderer
  - link/highlight/navigation
  - library/group loading
- Use it to block premature direct plugin adoption.

## 不可行点 / 避坑

- Do not use this as a main-vault plugin now.
- Do not fork from bundled `main.js`.
- Do not treat README feature list as runtime proof.
- Do not treat canvas tags as VAKS tags.
- Do not let exported visuals substitute for raw evidence anchors.

## 融合判断

- 结论：watch / design-only adapt
- 理由：对 visual workbench 有中等借鉴价值，但代码和运行风险不支持直接采用。
- 验证方式：future sandbox vault, compare official plugin features, inspect readable source/delta, test save/export behavior.

## 直接判断

- Direct use: no
- Fork: no
- Design-only: yes
- Reject: reject direct main-vault install
- Current branch value: medium for visual-sidecar thinking; low for source-intake core
- Whole architecture value: medium as workbench/risk reference
- Risk: high for direct adoption
- Next action: keep tagged as `medium-borrow` candidate reference

## 后续行动

No immediate implementation. If VAKS later opens a visual workbench branch, make a sandbox vault and compare this fork with the official Excalidraw plugin before any runtime use.
