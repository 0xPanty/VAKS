---
type: source_record
status: processed
source_kind: github_repo
repo: nashsu/llm_wiki
source_url: https://github.com/nashsu/llm_wiki
captured_at: 2026-05-26
reviewed_at: 2026-05-26
refreshed_at: 2026-06-06
latest_checked_commit: 21bab39766a387cc161b3d4a56eb8be099dffca7
latest_checked_commit_time: 2026-06-05T09:48:49Z
latest_checked_version: 0.4.20
latest_snapshot_location: raw/repos/_snapshots/nashsu-llm-wiki-21bab39766a387cc161b3d4a56eb8be099dffca7.zip
latest_snapshot_sha256: 05F8984B5713F5B8B8295749946C664FB7D00BB6B72E828EFABD9C463EF78E82
verification_status: code-inspected
evidence_level: primary
confidence: high
tags:
  - llm-wiki
  - knowledge-graph
  - agent-api
  - verified-vault
  - karpathy-pattern
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

## 2026-06-06 Short Post Refresh

Trigger:

- User sent a short Chinese summary / image describing `nashsu/llm_wiki` as a desktop application version of Karpathy's LLM Wiki pattern.

Current source refresh:

- Repository: `https://github.com/nashsu/llm_wiki`
- Checked commit: `21bab39766a387cc161b3d4a56eb8be099dffca7`
- Commit time: `2026-06-05T09:48:49Z`
- Commit message: `fix: harden CLI command resolution`
- Package version in `package.json`: `0.4.20`
- Snapshot: `raw/repos/_snapshots/nashsu-llm-wiki-21bab39766a387cc161b3d4a56eb8be099dffca7.zip`
- Snapshot SHA256: `05F8984B5713F5B8B8295749946C664FB7D00BB6B72E828EFABD9C463EF78E82`
- GitHub API metadata at refresh: 10578 stars, 1309 forks, 177 open issues.
- GitHub API license field returned `NOASSERTION`; repository `LICENSE` file is GPL v3 text.

Refresh finding:

The short post accurately points to the same high-signal features already extracted in the 2026-05-26 review:

- Karpathy-style `Raw Sources -> Wiki -> Schema` compiled-knowledge pattern.
- `[[wikilink]]` / Obsidian-compatible Markdown wiki output.
- Two-step ingest: analysis first, wiki generation second.
- Multimodal image ingestion and factual image captions.
- Four-signal knowledge graph: direct links, source overlap, Adamic-Adar, type affinity.
- Louvain community detection and graph insights.
- Deep Research as query expansion plus web result ingest.
- Local HTTP API at `127.0.0.1:19828`.
- MCP server and agent skill for Claude Code / Codex.

VAKS refresh judgment:

This is not a new architecture source for VAKS. It confirms and refreshes an already-processed source.

The useful part remains engineering reference:

- source lifecycle
- two-step ingest
- async review queue
- local API / MCP shape
- graph health and relation-signal diagnostics

The blocked part remains unchanged:

- generated wiki pages are candidate comprehension, not reviewed knowledge
- graph score / Louvain / vector search are activation or diagnostic signals, not truth
- Deep Research auto-ingest cannot become automatic promotion
- full desktop app is still too heavy before VAKS Markdown contracts and review gates are stable

Related refresh output:

- `outputs/review/2026-06-06-nashsu-llm-wiki-short-refresh.md`
