---
record_kind: source_annotation
annotation_id: ann-linxiv-004-mcp-mutation-surface
status: candidate
knowledge_status: candidate
processing_tier: light
annotation_scope: source_local_anchor
source_ref: "raw/repos/2026-06-23-linxiv-dev-linXiv-source.md"
source_snapshot_ref: "raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip"
selector_type: file_line_range
selector_value: "linxiv_mcp.py:83-108; linxiv_mcp.py:133-148; linxiv_mcp.py:287-426; linxiv_mcp.py:431-555; linxiv_mcp.py:667-814; linxiv_mcp.py:998-1045"
anchor_status: anchored
annotation_role: risk_signal
support_checked: false
evidence_support_status: not_checked
retrieval_policy: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
candidate_refs: "[outputs/review/2026-06-23-linxiv-dev-linXiv-strong-distillation.md]"
project_overlay_refs: "[outputs/review/project_overlays/2026-06-23-linxiv-dev-linXiv-vaks-local-research-library-overlay.md]"
---

# Source Annotation：MCP mutation surface

## Locator

```text
raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip
linxiv_mcp.py:83-108
linxiv_mcp.py:133-148
linxiv_mcp.py:287-426
linxiv_mcp.py:431-555
linxiv_mcp.py:667-814
linxiv_mcp.py:998-1045
```

## Why Pin This

linXiv's MCP server exposes useful read tools, but also project/note/tag
mutation, import/export, restore, and hard-delete tools.

This is a strong VAKS permission-boundary warning: agent access must start
read-only, and write/destructive tools require explicit approval and operation
receipts.

## Boundary

This is a risk locator, not a claim that linXiv is unsafe in its own context.
It does not decide VAKS MCP design by itself.
