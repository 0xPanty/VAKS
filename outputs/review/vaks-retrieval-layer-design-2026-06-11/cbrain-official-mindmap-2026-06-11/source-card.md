---
type: source
status: source-captured
title: "cBrain 官网脑图"
source_id: cbrain-official-mindmap-1066086058e5b2e0
source_uri: cbrain:share-mindmap:1066086058e5b2e0
source_url: https://cbrain.site/cbrain/share/mindmap?nodeid=1066086058e5b2e0
api_url: https://cbrain.site/prod-api/cbrain/map/1066086058e5b2e0/4
source_type: interactive-web-mindmap
captured_at: 2026-06-11
captured_by: Codex
processing_mode: explicit_strong_distill
processing_level: heavy
processing_tier: heavy
knowledge_status: raw
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: raw_provenance_only
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
target_workspace: outputs/review/vaks-retrieval-layer-design-2026-06-11
raw_location: outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/source-card.md
html_snapshot_location: outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/share-page.html
api_snapshot_location: outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/cbrain-official-mindmap-type4.json
node_details_location: outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/node-details/
source_integrity:
  share_page_sha256: 9edbc386f9fa354dbe93cd77103f89dd6e2b5f9eabd5f56aff21dd77e9165fb5
  type4_api_sha256: b902222d31d2f02ab0e3e76dfa0d4039a64d330d903dd2a7c383ff1b7e683a9d
  root_node_sha256: 503eaa4e49361f069e06ad1dd5533a4f9797cd5a5f95f4da4794daedb9b1f5fd
adapter_ingest:
  adapter_name: public cBrain share page + public cBrain map/node API
  adapter_version: manual-codex-2026-06-11
  capture_method: share page HTML, type-4 map JSON, selected public node JSON
  known_limits:
    - Public share page is a SPA and initially returns a loading shell.
    - Type-4 map snapshot exposes node tree but not every possible private detail.
    - Selected node details were sampled for design analysis, not exhaustive content review.
topics:
  - retrieval-workbench
  - activation-surface
  - layered-search
  - tree-navigation
  - node-note-model
  - knowledge-quantity-signal
projects:
  - verified-action-knowledge-system
tags:
  - source/web-mindmap
  - candidate-only
  - retrieval-layer-design
---

# Source Card: cBrain 官网脑图

## Why Captured

The user explicitly requested strong distillation and asked to place this source
inside the VAKS retrieval-layer design workspace.

This source is relevant because it shows a productized personal knowledge
workbench where navigation, node notes, search, learning method, and lightweight
knowledge quantity signals are visible to the user.

## Snapshot Summary

Captured public data on 2026-06-11:

```yaml
root_topic: cBrain官网
root_id: 1066086058e5b2e0
map_type: 4
map_node_count: 72
top_level_branches:
  - 1 关于
  - 2 教程
  - 4 价格
  - 5 更多
selected_node_details:
  - root
  - about
  - learning-method
  - knowledge-management
  - search-system
  - up-left-down-center
  - knowledge-management-standard
  - knowledge-quant-analysis
```

## Source Boundary

```text
public web mindmap = source provenance
tree / kq / color / ordering = UI and activation signal
candidate distillation = design extraction
promotion = later VAKS review only
```

This source does not provide reviewed evidence for VAKS truth claims and does
not justify a mainline architecture change by itself.

