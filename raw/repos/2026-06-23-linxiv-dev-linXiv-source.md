---
type: source
record_kind: source_card
status: source-captured
title: "linXiv"
source_id: "repo:linxiv-dev/linXiv@8085eeb61d03cadeb74eff2352afc148a3fa202c"
source_uri: "github:linxiv-dev/linXiv@8085eeb61d03cadeb74eff2352afc148a3fa202c"
source_url: "https://github.com/linxiv-dev/linXiv"
source_type: repository
author: "linxiv-dev"
publisher: GitHub
published_at: "2026-03-27T00:02:23Z"
updated_at: "2026-06-22T17:56:21Z"
captured_at: "2026-06-23"
captured_by: Codex
version_or_commit: "8085eeb61d03cadeb74eff2352afc148a3fa202c"
source_integrity:
  source_hash: null
  snapshot_hash: "sha256:4FF7D4564CC0F5AE3CC25639C03060EC37D2CD51B05B85DB33DB888C55693356"
  ingest_state: new
adapter_ingest:
  adapter_name: "manual-github-review"
  adapter_version: "2026-06-23"
  capture_method: "GitHub API metadata, git ls-remote, local shallow clone, source reads, and commit zip snapshot"
  extraction_trace: "GitHub API metadata; git ls-remote; commit zip snapshot; shallow clone; manual source/ADR/config/API/MCP/storage/service/test inventory inspection"
  known_limits: "runtime/tests not executed; Windows clone case-collision observed; issues/PRs/discussions/CI not exhaustively reviewed; frontend/graph viewer sampled not fully read"
source_status: active
raw_location: "raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip"
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
review_priority: normal
review_owner: Codex
formalization_status: raw-only
why_saved: "User asked to strongly distill linxiv-dev/linXiv for VAKS."
topics: "[local-first-research-library, academic-paper-intake, source-identity, sqlite, obsidian-export, mcp, tauri-sidecar, graph-viewer]"
projects: "[verified-action-knowledge-system]"
source_family: "[research-paper-manager, local-first-desktop-app, source-adapter-reference, agent-access-reference]"
upstream_sources: "[https://github.com/linxiv-dev/linXiv]"
verification_status: source_identity_checked
source_annotation_refs: "[ann-linxiv-001-namespaced-source-id, ann-linxiv-002-data-dir-source-of-truth, ann-linxiv-003-obsidian-export, ann-linxiv-004-mcp-mutation-surface, ann-linxiv-005-case-collision, ann-linxiv-006-vault-path-containment]"
candidate_relation_suggestions: "derived_from:outputs/review/2026-06-23-linxiv-dev-linXiv-strong-distillation.md"
tags: "[source, repository, candidate-only, linxiv, research-library, paper-intake, mcp]"
---

# 来源记录：linXiv

## 为什么收录

用户给出：

```text
[linxiv-dev/linXiv](https://github.com/linxiv-dev/linXiv) 强蒸馏这个
```

这个仓库不是 VAKS 的核心架构替代品。它的价值更窄：

```text
local-first academic paper app
-> source adapters for arXiv / DOI / CrossRef / OpenAlex / local PDFs
-> namespaced source identity and versioned local SQLite storage
-> project-scoped notes and tags
-> Obsidian/BibTeX/Markdown export
-> FastAPI / CLI / MCP / Tauri desktop surfaces
```

对 VAKS 最值得看的是：

```text
source identity registry
paper/source acquisition adapters
local runtime data boundary
read-only-vs-write-capable MCP boundary
cross-platform source snapshot hygiene
```

不该直接借的是：

```text
generic paper app schema as VAKS truth model
Obsidian export as reviewed knowledge
write-capable MCP as agent permission model
Tauri sidecar runtime as current VAKS mainline dependency
```

## 来源信息

- 作者/组织：linxiv-dev
- 发布方：GitHub
- 原始链接：https://github.com/linxiv-dev/linXiv
- 默认分支：`main`
- checked commit：`8085eeb61d03cadeb74eff2352afc148a3fa202c`
- commit time：`2026-06-20T03:26:41Z`
- commit subject：`Merge pull request #146 from linxiv-dev/dev`
- GitHub API metadata captured：`2026-06-23`
- GitHub API：public, active, GPL-3.0, Python, 20 stars, 1 fork, 6 open issues
- GitHub topics：`local-first`, `research`, `research-paper`, `tauri`
- 本地快照：`raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip`
- 快照 SHA256：`4FF7D4564CC0F5AE3CC25639C03060EC37D2CD51B05B85DB33DB888C55693356`

## Intake Boundary

```yaml
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
```

This source record is provenance and findability only. It does not adopt linXiv,
does not validate its runtime, and does not make any extracted implementation
pattern reviewed knowledge or action basis.

## Inspected Repository Areas

| Anchor | What exists | VAKS extraction | Boundary |
|---|---|---|---|
| `README.md` | Local-first academic paper desktop app with SQLite, optional AI tagging, Obsidian integration, graph view, Tauri shell. | Orientation for paper/source acquisition and local research library UX. | README is project claim, not runtime validation. |
| `pyproject.toml` | Python package `linxiv` v0.2.0, CLI and MCP entry points, FastAPI, pydantic, pypdf, OpenAI/Gemini dependencies. | Shows multi-surface source app packaging. | Dependency list is not a VAKS adoption recommendation. |
| `package.json` | React/Vite/Tauri frontend scripts and sidecar build pipeline. | Useful if VAKS later builds a desktop cockpit. | Too heavy for current Markdown-first VAKS core. |
| `src-tauri/tauri.conf.json` | Bundles API, CLI, and MCP as external binaries; CSP allows local API and GitHub update endpoints. | Sidecar/runtime boundary reference. | Runtime packaging is parked for VAKS. |
| `src-tauri/Cargo.toml` | Tauri v2 app plus plugin dependencies, including `tauri-plugin-texbrain`. | App-shell/plugin separation reference. | Do not import as current VAKS dependency. |
| `docs/adr/0002-namespaced-source-id.md` | Provider-prefixed source IDs: `arxiv:`, `openalex:`, `local:`. | Strong source identity lesson for VAKS source adapters. | Not a reviewed VAKS schema change by itself. |
| `docs/adr/0010-service-layer-as-api-boundary.md` | API should route through service layer, not direct storage writes. | Useful write-path boundary lesson. | Local app layering, not VAKS authority model. |
| `docs/adr/0014-data-dir-single-source-of-truth.md` | `LINXIV_DATA_DIR` separates runtime data from repo source tree. | Strong lesson for future VAKS derived caches/runtime surfaces. | VAKS Markdown vault remains file source-of-truth. |
| `docs/adr/0017-editor-as-downloaded-cached-plugin.md` | Explicit install, cached artifact, sha256 verification, no silent background auto-update. | Useful plugin/update lifecycle guardrail. | Product-stage reference only. |
| `docs/adr/0018-sidecar-lifecycle-and-reaping.md` | Per-launch health token and orphan sidecar cleanup. | Strong runtime reliability lesson. | Not current VAKS mainline. |
| `sources/base.py` | `PaperMetadata` model and `PaperSource` protocol. | Source adapter interface candidate. | Paper-centric; needs VAKS source-card boundary fields. |
| `sources/*` | arXiv, CrossRef, OpenAlex, DOI, PDF metadata acquisition. | Paper scouting/intake reference. | External API retrieval is acquisition, not evidence support. |
| `storage/config/sql/*` and `storage/db.py` | SQLite schema, `PAPER_ROOTS`, versions, FTS, soft delete/restore. | Source identity and versioned record lessons. | SQLite should not become VAKS truth source. |
| `formats/markdown.py` | Markdown and Obsidian-style export. | Export shape reference for paper cards. | Exported Markdown is not VAKS reviewed knowledge. |
| `linxiv_mcp.py` | MCP exposes search/fetch/list plus project, note, tag, import, restore, hard-delete operations. | Strong permission-boundary warning. | VAKS should borrow read-only subset first, not write tools. |
| `service/vault.py` | Editor vault path containment for on-disk project files. | Useful path safety pattern for any future editor/workbench. | Runtime file ops are not source intake authority. |
| `tests/` | Broad pytest suite for CLI/API/DB/projects/notes/sources/PDF/import/export. | Better maturity signal than README-only repos. | Test suite was not run locally. |
| `raw zip snapshot` | Contains both `.SQL` and `.sql` variants for `TAG` and `PROJECT_TO_TAG`. | Cross-platform path hygiene warning. | Source hygiene issue, not proof of runtime failure. |

## 初步看点

linXiv 是一个偏产品化的本地研究论文管理器：

```text
papers and PDFs
-> source identity / versioned SQLite rows
-> projects, notes, tags
-> search / graph / export
-> CLI / API / MCP / Tauri app
```

它对 VAKS 的强价值不是“怎么写 Obsidian 笔记”，而是：

```text
paper intake and source identity
runtime data location discipline
API/service/storage write boundary
agent-facing MCP permission risk
desktop sidecar lifecycle
```

## 明显疑点

- MCP surface includes many mutation and destructive tools; VAKS cannot copy this as default agent access.
- Obsidian export is convenient output, not reviewed knowledge, not source support.
- SQLite is the application runtime source of state; VAKS cannot let SQLite replace Markdown/YAML truth records.
- Runtime stack is heavy for current VAKS: Python backend, React frontend, Tauri, Rust sidecar, PyInstaller, MCP.
- Local clone on Windows reported case-colliding SQL files; source snapshots must be checked with case-sensitive paths.
- Settings/API keys are product concerns; VAKS should not absorb secret-writing UI patterns without its own secret hygiene.
- GitHub issues and CI history were not exhaustively reviewed.

## 可抽取 Candidate Points

1. Provider-prefixed `source_id` is a useful source identity pattern for future paper/repo/video/source adapters.
2. Runtime data must not fall back into the source tree; derived caches need an explicit data root and manifest.
3. Source acquisition adapters can feed VAKS raw/source cards, but cannot create reviewed knowledge or support.
4. Obsidian export is useful as user-facing convenience, but VAKS needs stricter candidate/review/action boundaries.
5. MCP should start read-only in VAKS; write/delete/import/restore tools require operation receipts and explicit approval.
6. Sidecar lifecycle needs identity tokens, process ownership, and cleanup if VAKS ever ships desktop/runtime components.
7. Case-sensitive path collisions are a real source snapshot hygiene issue for Windows-based agent work.

## 当前处理等级

```text
heavy source review, candidate only
```

Upgrade/reopen conditions:

- VAKS starts a paper-intake/source-adapter sandbox.
- VAKS designs a desktop cockpit or local runtime cache.
- MISA/VAKS MCP access moves from read-only query to any write-capable operation.
- A source snapshot/zip validator is added to catch case-folding collisions.

## 下一步

Read:

- `outputs/review/2026-06-23-linxiv-dev-linXiv-strong-distillation.md`
- `wiki/summaries/2026-06-23-linxiv-dev-linXiv-architecture-review.md`
- `outputs/review/project_overlays/2026-06-23-linxiv-dev-linXiv-vaks-local-research-library-overlay.md`
