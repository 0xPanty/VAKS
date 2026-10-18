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
target_ref: raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source.md
target_selector: checked_commit:3da586cc520d77c7f250d3765bf1fca1c91d70bd
target_hint: "Use as a VAKS visual-workbench / canvas-sidecar / dev-context-navigation reference, not as reviewed knowledge or a plugin adoption decision."
tagging_decision: tagged
tag_level: medium-borrow
tag_level_reason: "Helpful for VAKS visual sidecars and source-anchored canvas overlays; not strong because it is a demo vault with modified-plugin dependency, no root license, incomplete dependency table, and no runtime verification."
project_borrow_scope:
  - visual sidecar for source/candidate/project-overlay navigation
  - Excalidraw customData as canvas-local semantic metadata
  - Markdown <-> mindmap bridge with source/group anchors
  - source-line linked code highlight overlay for dev context navigation
  - separate demo vault / sandbox packaging for risky plugin-script workflows
project_non_borrow_scope:
  - bundled modified Excalidraw plugin as VAKS main-vault dependency
  - custom script execution in main vault without separate review
  - canvas arrows, proximity, layout, or hierarchy as reviewed relations
  - generated Markdown export as evidence support
  - code highlight rendering as source validation
  - direct code/assets reuse while repository-root license is unclear
project_reopen_trigger:
  - "VAKS starts designing an Excalidraw/Obsidian visual workbench."
  - "VAKS needs a visual context pack or review map for candidate points."
  - "VAKS wants source-line navigation overlays for MISA/VAKS dev context."
  - "VAKS considers installing modified plugins or running Obsidian custom scripts."
  - "A separate sandbox validates plugin compatibility, safety, and licensing."
confirmation_basis:
  - user switched from low-value Bilibili video to this repository in the same distillation/tagging lane
  - GitHub repository metadata checked on 2026-06-07
  - checked commit 3da586cc520d77c7f250d3765bf1fca1c91d70bd
  - snapshot hash verified locally
  - source/docs/scripts read only
  - no runtime execution; no promotion to reviewed knowledge
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: medium
borrow_order:
  - "P1: visual sidecar as activation/context overlay, not reviewed knowledge"
  - "P1: Excalidraw customData as canvas-local semantic metadata"
  - "P1: Markdown <-> mindmap bridge with source/group anchors"
  - "P2: source-line linked code highlight overlay for dev context"
  - "P2: demo vault/sandbox packaging for risky visual workflows"
  - "P3: libraries, fonts, CSS, settings, and bundled examples as cold references"
avoid:
  - "Do not promote this overlay into reviewed knowledge."
  - "Do not install or copy bundled modified plugins/scripts into the main VAKS vault from this intake."
  - "Do not treat visual graph/layout/mindmap as reviewed relation or evidence support."
  - "Do not let a demo vault become VAKS architecture before a concrete visual-workbench task exists."
  - "Do not reuse code/assets directly while licensing is unclear."
tags:
  - VAKS
  - project-overlay
  - obsidian-excalidraw-example-vault
  - medium-borrow
  - visual-workbench
  - canvas-sidecar
  - markdown-mindmap-bridge
  - source-anchored-visual-overlay
  - code-highlight-overlay
  - modified-plugin-risk
  - candidate-only
---

# VAKS Project Overlay: Obsidian Excalidraw Example Vault

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source.md
target_selector: checked_commit:3da586cc520d77c7f250d3765bf1fca1c91d70bd
target_hint: visual-workbench / canvas-sidecar / dev-context-navigation / plugin-script sandbox
```

## 标签等级

```yaml
tagging_decision: tagged
tag_level: medium-borrow
borrow_value: medium
```

人话：

```text
有帮助，所以打标签。
但不是强帮助。
它适合当 VAKS 未来画布工作台的参考，不适合直接进主线或当插件方案。
```

## Project Borrow Scope

VAKS 当前可以借：

1. **画布侧车**：用 Excalidraw 展示 source/candidate/project overlay/risk/context，而不是写 truth。
2. **`customData` 局部语义**：把 mindmap/code highlight 这类 UI 状态放在画布元素上，避免污染 reviewed schema。
3. **Markdown <-> mindmap anchor bridge**：让导入/导出保留 source/group anchor，方便回链。
4. **source-line code overlay**：把代码片段、文件路径、行号做成可点击视觉导航。
5. **demo vault sandbox**：插件、脚本、CSS、字体、库素材先放独立试验库，不碰主 vault。

## Project Non-Borrow Scope

VAKS 当前不要借：

- 不要把 bundled modified Excalidraw plugin 当 VAKS 主 vault 依赖。
- 不要在主 vault 直接跑这些 custom scripts。
- 不要把 canvas arrow / layout / proximity / mindmap hierarchy 当 reviewed relation。
- 不要把导出的 Markdown outline 当 evidence support。
- 不要把 code highlight 视觉结果当 source validation。
- 不要在 root license 不明确时直接复用代码或素材。

## Reopen Trigger

重新打开这条 overlay 的条件：

- VAKS 要做 Excalidraw/Obsidian visual workbench。
- VAKS 要做 visual context pack / review map。
- VAKS 要做 source-line dev context navigation。
- VAKS 考虑安装修改版插件或运行 Obsidian custom scripts。
- 单独 sandbox 已经验证兼容性、安全边界和许可问题。

## Confirmation

```yaml
confirmation_basis:
  - user_requested_switch_to_repo: true
  - checked_commit: 3da586cc520d77c7f250d3765bf1fca1c91d70bd
  - current_github_metadata_checked: 2026-06-07
  - snapshot_hash_verified: true
  - artifact_paths:
      - raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source.md
      - outputs/review/2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-candidate-distillation.md
      - wiki/summaries/2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-architecture-review.md
      - outputs/review/project_overlays/VAKS-obsidian-excalidraw-example-vault-2026-06-07.md
      - raw/repos/_snapshots/Bowen-0x00-obsidian-excalidraw-example-vault-3da586cc520d77c7f250d3765bf1fca1c91d70bd.zip
  - runtime_executed: false
last_checked_at: 2026-06-07
expires_at: 2026-07-07
```

## 人话结论

打标签，等级是 `medium-borrow`。

最值得 VAKS 记住的是：

```text
画布可以帮人看懂关系、跳转来源、组织候选上下文。
但画布不负责证明、不负责审查、不负责决策。
```

现在可以把它放进 VAKS 的 Support/Risk 层：

```text
support_when:
  - 做 visual workbench
  - 做 context pack 可视化
  - 做 code/source-line 导航
risk_when:
  - 有人想把 Excalidraw 图当 reviewed graph
  - 有人想直接安装改版插件
  - 有人想把脚本生成物当 truth
```
