---
type: source
record_kind: source_card
status: source-captured
title: "safishamsi/graphify"
source_id: 2026-06-11-safishamsi-graphify-source
source_uri: https://github.com/safishamsi/graphify
source_url: https://github.com/safishamsi/graphify
source_type: repository
author: Safi Shamsi
publisher: GitHub / PyPI
published_at: 2026-04-03
updated_at: 2026-06-10
captured_at: 2026-06-11
captured_by: Codex
version_or_commit: 565026d3d10fb2d69bd01a5437433f278683fd8b
source_integrity:
  repository_head: 565026d3d10fb2d69bd01a5437433f278683fd8b
  default_branch: v8
  snapshot_location: raw/repos/_snapshots/2026-06-11-safishamsi-graphify-565026d3d10f.zip
  snapshot_sha256: 3f46033bd26a9199e74037b30605e65bfcca58f0ee2d9fd4728d478bf45e1eef
  ingest_state: new
adapter_ingest:
  adapter_name: web + GitHub API + git ls-remote + source snapshot + static source inspection
  adapter_version: manual-codex-2026-06-11
  capture_method: repository metadata, codeload snapshot, README/docs/security/architecture/source files, selected tests
  extraction_trace:
    - GitHub repository metadata checked 2026-06-11.
    - git ls-remote checked HEAD/default branch and main branch.
    - codeload snapshot captured and SHA256 verified.
    - README, ARCHITECTURE, SECURITY, docs/how-it-works, pyproject, skill-codex, and core graphify Python modules inspected.
    - No local Graphify CLI install, extraction run, server, hook, MCP service, or benchmark was executed.
  known_limits:
    - Repository is young and active; metadata such as stars, issues, and version can change quickly.
    - README benchmark claims were recorded as project claims, not independently rerun.
    - Static inspection focused on retrieval-layer architecture, not full security audit.
source_status: active
raw_location: raw/repos/_snapshots/2026-06-11-safishamsi-graphify-565026d3d10f.zip
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: high
review_owner: Codex
formalization_status: candidate-generated
topics:
  - knowledge-graph
  - graph-retrieval
  - code-understanding
  - agent-context
  - graph-rag
  - tree-sitter
  - community-detection
  - retrieval-governance
projects:
  - verified-action-knowledge-system
source_family:
  - graph-retrieval
  - codebase-knowledge-graph
  - agent-skill
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - source/repo
  - candidate-only
  - retrieval-layer
  - graph-retrieval
  - code-graph
why_saved: see_body_or_legacy_record
---

# Graphify Source Record

## Why Captured

The user requested a strong distillation of `safishamsi/graphify` for the VAKS
retrieval-layer design workspace.

This source matters because it is not a normal vector-search library. It builds
a queryable knowledge graph from code, docs, papers, images, and video/audio
transcripts, then gives AI coding assistants graph-first commands and MCP tools
for scoped codebase/context retrieval.

## Source Information

- Repository: https://github.com/safishamsi/graphify
- Homepage: https://graphifylabs.ai/
- Package name in `pyproject.toml`: `graphifyy`
- Main CLI command: `graphify`
- Checked commit: `565026d3d10fb2d69bd01a5437433f278683fd8b`
- Default branch at capture: `v8`
- License: MIT
- Primary language: Python
- Snapshot: `raw/repos/_snapshots/2026-06-11-safishamsi-graphify-565026d3d10f.zip`
- Snapshot SHA256: `3f46033bd26a9199e74037b30605e65bfcca58f0ee2d9fd4728d478bf45e1eef`

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
action_basis_allowed: false
truth_mutation_allowed: false
```

This source record is provenance only. It does not adopt Graphify, promote a
VAKS pattern, create reviewed relations, or make action-facing claims.

## Source / Code Anchors Inspected

| Anchor | What Was Checked | Why It Matters |
|---|---|---|
| `README.md` | Project description, install flow, assistant integration, output artifacts | Public product promise and usage shape |
| `ARCHITECTURE.md` | Pipeline modules and extraction schema | Overall graphify architecture |
| `docs/how-it-works.md` | Three-pass extraction, community detection, confidence labels, cache, graph format | Retrieval and compression model |
| `SECURITY.md` | SSRF, path, XSS, prompt-injection, secret-handling posture | Boundary and safety ideas |
| `pyproject.toml` | Package name, CLI entrypoints, dependency/extras layout | Runtime surface and optional integrations |
| `graphify/extract.py` | Tree-sitter/code extraction, relation/context labels, source locations | Local deterministic graph extraction |
| `graphify/build.py` | NetworkX graph construction, ID normalization, dedup, direction preservation | Graph assembly and merge behavior |
| `graphify/cluster.py` | Leiden/Louvain community detection and stability behavior | Structure-based context grouping |
| `graphify/serve.py` | query_graph, get_node, get_neighbors, get_community, stats, MCP tools | Agent-facing retrieval API |
| `graphify/__main__.py` | CLI query/affected/path/explain/hook/export commands | User-facing workflow |
| `graphify/cache.py` and `graphify/detect.py` | content hashes, manifest, incremental detection, sensitive-file skipping | Rebuildable derived cache pattern |
| `graphify/hooks.py` | post-commit/post-checkout background rebuild hooks | Freshness automation and risk surface |
| `graphify/security.py` | safe fetch, graph path validation, size caps, label/metadata sanitization | Guardrail pattern |
| `tests/test_confidence.py`, `tests/test_cli_export.py`, `tests/test_codebuddy.py` | Confidence preservation, export behavior, assistant hook behavior | Evidence that key behaviors are tested |

## Initial Candidate Points

1. Graphify's useful center is a structural graph retrieval layer, not a vector
   database.
2. Local AST/tree-sitter extraction is valuable for source anchors and cheap
   code structure recall.
3. Community detection and graph traversal are useful activation signals, but
   cannot become truth, support, or action readiness in VAKS.
4. Assistant-first query habits are useful, but forced hooks are risky for VAKS
   unless they respect explicit mode and authority buckets.
5. Graphify's safety posture gives VAKS useful guardrail ideas for any future
   derived retrieval cache or agent gateway.

## Obvious Open Questions

- How stable are Graphify's extracted edges on a large mixed VAKS vault?
- Can its graph output preserve VAKS authority buckets without custom adapter
  work?
- Does its query expansion improve actual source-anchor correctness, or only
  improve orientation?
- How much prompt-injection risk remains when untrusted docs become graph node
  labels and MCP context?
- Would VAKS benefit more from borrowing the design pattern than from adopting
  the package?

## Next Step

Keep this source in the VAKS retrieval-layer design workspace as P1 candidate
input. Any future implementation must be a sandbox adapter first, with bucket
filtering before graph traversal or rank fusion.
