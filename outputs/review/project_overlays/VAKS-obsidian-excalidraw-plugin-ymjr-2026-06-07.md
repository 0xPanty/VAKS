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
project_id: VAKS
target_ref: "raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-source.md"
target_selector: "repo:github:Bowen-0x00/obsidian-excalidraw-plugin-ymjr@3fa4ace442c3d455c05172e1b1894033572e6b47"
target_hint: visual-workbench / canvas-sidecar / plugin-hook-risk
tagging_decision: tagged
tag_level: medium-borrow
borrow_value: medium
project_borrow_scope:
  - "For VAKS, borrow the plugin-level hook capability model as a future visual-workbench reference."
  - "Borrow element-local metadata/tag/link/highlight ideas only as canvas navigation and project-context UI."
  - "Borrow export/render ideas as visual snapshot or briefing support, not as evidence support."
  - "Borrow the risk lesson that modified plugins replacing official plugins require sandbox quarantine."
project_non_borrow_scope:
  - "For VAKS, do not currently install this fork in the main Obsidian vault because it replaces the official Excalidraw plugin, has no observed root license, is mainly bundled/minified, and was behind upstream at capture time."
  - "Do not treat `customData.tags` or canvas-local tags as VAKS taxonomy, reviewed labels, truth confidence, review routing, or action-basis markers."
  - "Do not treat link highlights, mindmap layout, ECharts/table/code render, or exported SVG/image as evidence support."
  - "Do not copy code from the minified bundle or depend on the unextracted 7z archive without later readable-source review."
project_reopen_trigger:
  - "Reopen if VAKS explicitly starts a visual workbench / Excalidraw sidecar sandbox."
  - "Reopen if official Excalidraw cannot provide needed hooks through normal scripts."
  - "Reopen if readable source, license clarity, upstream delta, and sandbox runtime tests are available."
confirmation_basis: "User asked to continue repo strong distillation and tag only if helpful; this repo is helpful as a candidate visual-workbench reference, not as direct adoption."
last_checked_at: 2026-06-07T03:45:00+08:00
expires_at:
tags:
  - VAKS
  - project-overlay
  - candidate-only
  - medium-borrow
  - visual-workbench
  - canvas-sidecar
  - plugin-hook
  - modified-plugin-risk
  - no-action-basis
---

# Project Overlay：VAKS x obsidian-excalidraw-plugin-ymjr

## Boundary

This is a project-scoped sidecar. It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

```yaml
knowledge_status: candidate
overlay_scope: project_sidecar_only
retrieval_scope: active_project_only
action_basis_allowed: false
truth_mutation_allowed: false
tagging_decision: tagged
tag_level: medium-borrow
```

## Target

```yaml
target_ref: raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-source.md
target_selector: repo:github:Bowen-0x00/obsidian-excalidraw-plugin-ymjr@3fa4ace442c3d455c05172e1b1894033572e6b47
target_hint: visual-workbench / canvas-sidecar / plugin-hook-risk
```

## Project Borrow Scope

For VAKS, this repo may be borrowed only in a narrow design sense:

1. **Visual workbench capability map**

   Use the README feature list as a candidate map for future canvas-sidecar needs: local element tags, hook lifecycle, mindmap interactions, code/chart rendering, layer/fixed elements, thumbnail, library loading, link highlight, and SVG export.

2. **Plugin-vs-script boundary**

   Borrow the lesson that scripts are the first layer, plugin modifications are a later sandbox layer. If official Excalidraw plus scripts can solve the workflow, do not fork/replace the plugin.

3. **Canvas-local metadata**

   Borrow `customData` and local tag ideas only as visual navigation state. They can help a human see a project map, but they cannot become VAKS truth.

4. **Presentation export**

   Borrow export/render ideas for visual briefings, snapshots, or project maps. They are display artifacts, not evidence anchors.

## Project Non-Borrow Scope

For VAKS, do not currently borrow this repo as an installable main-vault plugin.

Reasons:

- It replaces official Excalidraw and README asks users to disable the original plugin.
- No root LICENSE was observed and GitHub API did not report a license.
- The repo is dominated by bundled `main.js`, CSS, images, and an unextracted `.7z` archive, not a clean source tree.
- At capture time official upstream Excalidraw was already newer (`2.23.10`) than this fork (`2.23.5-1`).
- It was not runtime-tested in the VAKS vault.

Do not borrow these meanings:

- `customData.tags` as VAKS tags.
- Canvas links as reviewed relations.
- Exported SVG/image as Evidence Packet.
- Mindmap/table/chart layout as proof or action support.
- README feature list as runtime verification.

## Reopen Trigger

Reopen this overlay only if:

- VAKS explicitly starts a visual workbench / Excalidraw sidecar sandbox.
- A concrete task proves official Excalidraw and normal scripts cannot supply the needed hook.
- The fork's readable source or patch delta is inspected.
- License and upstream drift are clarified.
- Runtime tests pass in a throwaway or sandbox vault.

## Confirmation

```yaml
confirmation_basis: "The user asked to continue the Bowen Excalidraw repo sequence and tag only if useful. It is useful for VAKS as visual-workbench candidate context."
last_checked_at: 2026-06-07T03:45:00+08:00
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
main-vault plugin adoption
```
