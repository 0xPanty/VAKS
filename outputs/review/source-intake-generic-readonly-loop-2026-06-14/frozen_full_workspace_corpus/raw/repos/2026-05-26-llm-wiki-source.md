---
type: source_record
record_kind: source_card
status: processed
source_kind: github_repo
repo: nashsu/llm_wiki
source_url: https://github.com/nashsu/llm_wiki
captured_at: 2026-05-26
reviewed_at: 2026-05-26
verification_status: code-inspected
evidence_level: primary
source_integrity:
  capture_confidence: high
tags:
  - llm-wiki
  - knowledge-graph
  - agent-api
  - verified-vault
  - karpathy-pattern
knowledge_status: raw
processing_tier: light
source_id: nashsu/llm_wiki
title: nashsu/llm_wiki
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---
# Source: nashsu/llm_wiki

## What It Is

`nashsu/llm_wiki` is a concrete desktop implementation of the Karpathy LLM Wiki pattern. It is not just an Obsidian template or article. The inspected source shows a Tauri + React + Rust app that imports sources, compiles wiki files, renders graph views, exposes a local API, and keeps app state.

Inspected files:

- `README.md`
- `llm-wiki.md`
- `package.json`
- `src/lib/graph-relevance.ts`
- `src/lib/graph-insights.ts`
- `src-tauri/src/api_server.rs`

Local snapshot path during review:

- `C:\Users\Administrator\AppData\Local\Temp\llm_wiki-src-20260526183817\llm_wiki-main`

## Confirmed Source Facts

- App stack: Tauri 2, React 19, TypeScript, Rust backend.
- Graph stack: `graphology`, `graphology-communities-louvain`, `sigma`, ForceAtlas2.
- Retrieval and storage stack includes LanceDB and optional vector search.
- Recommended wiki shape includes `purpose.md`, `schema.md`, `raw/sources/`, `wiki/index.md`, `wiki/log.md`, `wiki/overview.md`, `.llm-wiki/`.
- It implements four relevance signals:
  - direct link weight 3.0
  - source overlap weight 4.0
  - Adamic-Adar common neighbor weight 1.5
  - type affinity weight 1.0
- `graph-insights.ts` detects:
  - surprising cross-community / cross-type / peripheral-to-hub links
  - isolated nodes
  - sparse communities
  - bridge nodes
- Local API is bound to `127.0.0.1:19828`.
- API supports health, project listing, file listing/content, search, graph, source rescan.
- Chat API in the Rust API server is explicitly not implemented yet.
- API has practical safety details: token auth, rate limiting, in-flight request cap, body/content size caps, safe path join tests, and public path filtering.

## Why It Matters To Our Vault

This repo directly validates several ideas already in our design:

- `raw -> wiki -> outputs` style compiled knowledge.
- Markdown-first, Obsidian-compatible source of truth.
- Index-first agent orientation.
- Verified vault API for external agents.
- Graph-based relation discovery.
- Health checks for knowledge gaps and blind spots.

It also adds several stronger concrete designs:

- `purpose.md` as a separate mission layer from `schema.md`.
- Quantified multi-signal relation scoring.
- Graph insight metrics that can become health checks.
- Local HTTP API as a real agent integration surface.
- Async review queue as a quality gate for AI-ingested material.

## Reliability Notes

Evidence strength is high for "the repo implements these structures" because it was checked in source code. We have not run the app end to end, so product quality and real-world UX remain unverified.

Star count and popularity were not used as core evidence in this review because those numbers are time-sensitive and should be refreshed before citing.
