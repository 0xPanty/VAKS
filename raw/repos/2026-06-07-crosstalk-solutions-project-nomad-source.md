---
type: source
status: source-captured
title: "Project N.O.M.A.D."
source_id: 2026-06-07-crosstalk-solutions-project-nomad-source
source_uri: https://github.com/Crosstalk-Solutions/project-nomad
source_url: https://github.com/Crosstalk-Solutions/project-nomad
source_type: repository
author: Crosstalk-Solutions
publisher: GitHub
published_at:
updated_at: 2026-06-06T17:56:42Z
pushed_at: 2026-06-06T18:01:21Z
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: d5f7c3f615c92c07b798b6512b2483fd9d64a89d
commit_time: "2026-05-27 22:36:20 +0000"
commit_subject: "docs(release): finalize v1.32.1 release notes [skip ci]"
default_branch: main
latest_release: v1.32.1
latest_release_published_at: 2026-05-27T22:36:15Z
source_status: active
license: Apache-2.0
dynamic_metadata_checked_at: 2026-06-07T02:03:32+08:00
dynamic_metadata:
  stars: 29201
  forks: 2891
  open_issues: 67
raw_location: raw/repos/2026-06-07-crosstalk-solutions-project-nomad-source.md
snapshot_location: raw/repos/_snapshots/Crosstalk-Solutions-project-nomad-d5f7c3f615c92c07b798b6512b2483fd9d64a89d.zip
snapshot_sha256: A59965A0C7AA3D7CC3D4CC61212E657A1C270900F08F1395894103C864CD198E
processing_mode: immediate
processing_level: heavy
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: medium
review_owner: Codex
formalization_status: candidate-generated
topics:
  - offline-knowledge-appliance
  - local-first
  - curated-content-manifest
  - kiwix-zim
  - ollama
  - qdrant-rag
  - kb-ingest-state
  - maintenance-diagnostics
  - service-orchestration
  - unauthenticated-local-ui
  - docker-socket-risk
source_family:
  - source-intake
  - offline-content-packaging
  - retrieval-activation
  - operator-cockpit
  - maintenance-diagnostics
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - target: "[[Source Intake]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The repository separates content selection, download/install state, KB ingestion state, vector-store presence, and warning surfaces."
  - target: "[[Activation Tier]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Offline content tiers and local knowledge packs are useful activation/package signals, not trust signals."
  - target: "[[Evidence Sufficiency Gate]]"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "RAG chunks, benchmark scores, and collection membership can be mistaken for evidence support unless kept as diagnostics and activation aids."
  - target: "[[Agent Gateway]]"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "Unauthenticated local UI, Docker socket access, host mounts, and updater sidecars are useful caution anchors for future tool/agent boundaries."
tags:
  - project-nomad
  - repo-source
  - offline-knowledge-appliance
  - local-first
  - curated-content-manifest
  - kiwix-zim
  - rag-ingest
  - qdrant
  - ollama
  - operator-cockpit
  - maintenance-diagnostics
  - security-risk
  - candidate-only
---

# Project N.O.M.A.D. Source Record

## 为什么收录

`Crosstalk-Solutions/project-nomad` 是一个 offline-first knowledge and education server。它把 Kiwix / ZIM 离线资料、Kolibri、ProtoMaps、CyberChef、FlatNotes、本地 AI chat、Qdrant RAG、下载/更新/健康检查等组合成一个本地浏览器访问的 Command Center。

对 VAKS 来说，它不是 truth maintenance 系统，也不是 reviewed knowledge 主干。它值得强蒸馏，是因为它把“离线知识包 + 本地 RAG + 操作面板 + 摄取失败提示”做成了一个工程闭环：

```text
curated content manifest
-> download / install
-> local library / storage
-> optional KB ingestion
-> vector search / context injection
-> health / warning / update surface
```

人话判断：

```text
有帮助，但只打 candidate / medium-borrow 标签。
不要打成 VAKS core、reviewed relation、truth confidence 或 action basis。
```

## 来源信息

- Repository: `Crosstalk-Solutions/project-nomad`
- URL: https://github.com/Crosstalk-Solutions/project-nomad
- Checked branch: `main`
- Checked commit: `d5f7c3f615c92c07b798b6512b2483fd9d64a89d`
- Commit time: `2026-05-27 22:36:20 +0000`
- Commit subject: `docs(release): finalize v1.32.1 release notes [skip ci]`
- Latest release observed: `v1.32.1`, published `2026-05-27T22:36:15Z`
- GitHub dynamic metadata observed: stars `29201`, forks `2891`, open issues `67`
- License: Apache-2.0
- Snapshot: `raw/repos/_snapshots/Crosstalk-Solutions-project-nomad-d5f7c3f615c92c07b798b6512b2483fd9d64a89d.zip`
- Snapshot SHA256: `A59965A0C7AA3D7CC3D4CC61212E657A1C270900F08F1395894103C864CD198E`

## Primary Anchors

| Anchor | What exists | Why it matters |
|---|---|---|
| `README.md:17-53` | Offline-first knowledge and education server, browser Command Center, Docker-orchestrated tools, local AI + Qdrant RAG, Kiwix, Kolibri, ProtoMaps, CyberChef, FlatNotes. | Shows the project is a local knowledge appliance, not just a link list. |
| `README.md:105-115` | Offline usage, no built-in telemetry, no authentication, network-level controls recommended, not designed for direct internet exposure. | Important for VAKS privacy posture and security boundary. |
| `collections/wikipedia.json:1-51` | Wikipedia options with ids, descriptions, size_mb, URLs, versions. | Useful source-package manifest shape. |
| `collections/kiwix-categories.json:1-75` | Kiwix categories and tiers with recommended flag, includesTier, resources, versions, URLs, sizes. | Useful tiered offline-content package model. |
| `admin/app/services/collection_manifest_service.ts:27-91` | Fetches remote collection specs, validates, caches spec_version/spec_data/fetched_at, and falls back to cache. | Good candidate pattern for refreshable but cached source manifests. |
| `admin/app/services/collection_manifest_service.ts:193-245` | Resolves included tiers and detects installed tier from resource completeness. | Useful for package/coverage completion semantics. |
| `admin/app/utils/kb_ingest_decision.ts:3-70` | KB scan action state machine: skip, dispatch, backfill_indexed, create_pending; state row is authoritative, Qdrant is corroborating. | Strong candidate for VAKS ingestion-state vs vector-presence separation. |
| `admin/app/utils/kb_warning_decision.ts:1-70` | Conditional warnings for zero chunks and partial stalls. | Useful for maintenance lint without pretending to be truth review. |
| `admin/app/utils/kb_ratio_lookup.ts:31-97` | Batch and chunk-count estimates, unknown handling, longest-prefix match. | Useful for pre-ingest cost/size warnings. |
| `admin/app/utils/kb_job_health.ts:1-50` | Waiting / healthy / slow / stalled / failed job status based on activity timestamps. | Useful operator surface for long-running source ingestion. |
| `admin/app/services/rag_service.ts:1076-1235` | Stored-file union, chunk counts, filesystem scan, warning computation, ok=false on computation failure. | Good example of surfacing silent ingestion failures. |
| `admin/app/services/rag_service.ts:1513-1648` | Scans storage, filters embeddable files, uses ingest policy and state rows, dispatches jobs. | Useful candidate for lazy/manual/always source ingestion policy. |
| `admin/app/services/rag_service.ts:791-929` | Similarity search, query preprocessing, score threshold, metadata, reranking, source diversity. | Useful as retrieval/activation sample, not evidence support. |
| `admin/app/controllers/ollama_controller.ts:74-130` | Query rewriting, top RAG results, adaptive context budgets, context injection. | Useful context-pack caution sample. |
| `install/management_compose.yaml:11-69` | Admin + Dozzle with Docker socket; Dozzle actions/shell disabled due unauthenticated LAN risk. | Useful security caution. |
| `install/management_compose.yaml:98-117` | Updater sidecar with Docker socket and writable project path; disk collector with read-only host FS. | Useful caution for future VAKS agent/tool surfaces. |

## Boundary

This source record is provenance plus orientation only.

It does not create reviewed knowledge, reviewed relations, action basis, truth confidence, or a VAKS implementation decision.

