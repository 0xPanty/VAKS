---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: verified-action-knowledge-system
target_ref: raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source.md
target_selector: checked_commit:1d0edb6beac48efe92b5a19c22cef701bc3a54e5
target_hint: "Use as a VAKS visual-workbench / canvas-sidecar / script-sandbox implementation reference, not as reviewed knowledge or a main-vault script adoption decision."
tagging_decision: tagged
tag_level: medium-borrow
tag_level_reason: "Useful and implementation-dense for VAKS visual workbench/script sandbox design; kept medium because it is future-sidecar work with root license ambiguity, stale README paths, modified-plugin dependency, and no runtime verification."
project_borrow_scope:
  - Action vs Feature split for canvas tools
  - EA_Core hook lifecycle as script-sandbox reference
  - customData as canvas-local semantic metadata
  - paste/link/export scripts as source-anchored visual sidecars
  - source-line code overlay for dev context navigation
  - visual tags as local canvas navigation only
  - generated script index/categories for discoverability
project_non_borrow_scope:
  - direct installation or execution in the main VAKS vault
  - customData.tags as VAKS tags, taxonomy, review routing, or truth labels
  - mindmap/table/chart/layout as reviewed relation or evidence support
  - exported SVG/image as Evidence Packet or source text
  - code/assets reuse while repository-root license and vendored libraries are unresolved
  - paste/link/export hooks without explicit sandbox and user control
project_reopen_trigger:
  - "VAKS starts designing an Obsidian/Excalidraw visual workbench."
  - "VAKS creates a script/plugin sandbox or custom-script permission model."
  - "VAKS needs visual source maps, review maps, or dev context canvas navigation."
  - "VAKS considers using Excalidraw element tags or customData for project-local context."
  - "A separate sandbox validates compatibility, safety, and licensing."
confirmation_basis:
  - user provided this repository after the paired example-vault intake
  - GitHub repository metadata checked on 2026-06-07
  - checked commit 1d0edb6beac48efe92b5a19c22cef701bc3a54e5
  - snapshot hash verified locally
  - source/docs/scripts read only
  - no runtime execution; no promotion to reviewed knowledge
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: medium
borrow_order:
  - "P1: Action script vs Feature engine split for visual tool behavior"
  - "P1: EA_Core hook lifecycle as a script-sandbox design reference"
  - "P1: customData as canvas-local semantics, not reviewed schema"
  - "P1: paste/link/export scripts for source-anchored visual sidecars"
  - "P2: source-line code overlay and local visual tags for dev/context navigation"
  - "P2: table/ECharts/mindmap as visual workbench widgets"
  - "P3: individual drawing utilities, GIF demos, libraries, style helpers"
avoid:
  - "Do not promote this overlay into reviewed knowledge."
  - "Do not install or copy this script collection into the main VAKS vault from this intake."
  - "Do not treat Excalidraw visual tags as VAKS tags."
  - "Do not treat hook-generated canvas structure as reviewed relation or evidence support."
  - "Do not reuse code/assets directly while licensing and vendored libraries remain unresolved."
tags:
  - VAKS
  - project-overlay
  - obsidian-excalidraw-scripts
  - medium-borrow
  - visual-workbench
  - canvas-sidecar
  - ea-core-hooks
  - action-feature-split
  - canvas-local-metadata
  - source-anchored-visual-overlay
  - visual-tags-not-vaks-tags
  - script-sandbox-risk
  - candidate-only
---

# VAKS Project Overlay: Obsidian Excalidraw Scripts

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source.md
target_selector: checked_commit:1d0edb6beac48efe92b5a19c22cef701bc3a54e5
target_hint: visual-workbench / canvas-sidecar / script-sandbox / source-linked visual context
```

## 标签等级

```yaml
tagging_decision: tagged
tag_level: medium-borrow
borrow_value: medium
```

人话：

```text
有帮助，打标签。
比 example vault 更有实现细节，但仍然不是 strong。
它适合当 VAKS 未来 visual workbench/script sandbox 的参考，不适合现在直接进主 vault。
```

## Project Borrow Scope

VAKS 当前可以借：

1. **Action / Feature 拆分**：把用户手动动作和后台常驻引擎分开。
2. **hook 生命周期**：`registerHook` / `unregisterHook` 可作为 script sandbox 设计参考。
3. **`customData` 局部语义**：画布元素可以保存 UI 状态，但不写进 reviewed schema。
4. **paste/link/export visual sidecar**：把 source snippets、代码行、外部摘录做成可导航画布元素。
5. **source-line code overlay**：对 dev context 很有用，但只是导航。
6. **visual tags**：可以当画布局部筛选/导航，不是 VAKS 标签。
7. **脚本目录/index**：可借它的分类与 discoverability 形式。

## Project Non-Borrow Scope

VAKS 当前不要借：

- 不要直接安装或运行整套脚本到主 VAKS vault。
- 不要把 `customData.tags` 当成 VAKS tag / taxonomy / review routing / truth label。
- 不要把 mindmap/table/ECharts/layout 当 reviewed relation。
- 不要把 SVG/image export 当 Evidence Packet 或 source support。
- 不要在 root license 和 vendored libraries 未审完时复用代码/素材。
- 不要在没有 sandbox 和用户明确控制时启用 paste/link/export hooks。

## Reopen Trigger

重新打开这条 overlay 的条件：

- VAKS 要做 Obsidian/Excalidraw visual workbench。
- VAKS 要做 custom script/plugin sandbox。
- VAKS 要做 visual source map / review map / dev context canvas。
- VAKS 要用 Excalidraw element tags 或 `customData` 承载项目局部上下文。
- 独立 sandbox 已验证兼容性、安全边界和许可问题。

## Confirmation

```yaml
confirmation_basis:
  - user_provided_repo_after_example_vault: true
  - checked_commit: 1d0edb6beac48efe92b5a19c22cef701bc3a54e5
  - current_github_metadata_checked: 2026-06-07
  - snapshot_hash_verified: true
  - artifact_paths:
      - raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source.md
      - outputs/review/2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-candidate-distillation.md
      - wiki/summaries/2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-architecture-review.md
      - outputs/review/project_overlays/VAKS-obsidian-excalidraw-scripts-2026-06-07.md
      - raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-scripts-1d0edb6beac48efe92b5a19c22cef701bc3a54e5.zip
  - runtime_executed: false
last_checked_at: 2026-06-07
expires_at: 2026-07-07
```

## 人话结论

打标签，等级是 `medium-borrow`。

最值得 VAKS 记住的是：

```text
脚本能让画布变成强交互工作台。
但越强交互，越要 sandbox。
画布可以帮人理解和跳转，不能负责证明和决策。
```

现在把它放进 VAKS 的 Support/Risk 层：

```text
support_when:
  - 做 visual workbench
  - 做 source/review map 可视化
  - 做 dev context canvas
  - 做 Obsidian custom script sandbox
risk_when:
  - 有人想把 canvas tags 当 VAKS tags
  - 有人想直接跑脚本包
  - 有人想把 hook 生成的结构当 truth
```
