---
type: library_review
status: draft
library_name: "Project N.O.M.A.D."
repo_url: https://github.com/Crosstalk-Solutions/project-nomad
source_url: https://github.com/Crosstalk-Solutions/project-nomad
checked_commit: d5f7c3f615c92c07b798b6512b2483fd9d64a89d
commit_time: "2026-05-27 22:36:20 +0000"
source_status: active
reviewed_at: 2026-06-07
domain: offline-first knowledge appliance, local AI assistant, curated content package manager
related_projects:
  - verified-action-knowledge-system
current_branch:
  - source-intake
  - activation-tier
  - retrieval-activation
  - maintenance-diagnostics
  - agent-gateway-risk
extracted_patterns:
  - tiered-offline-content-manifest
  - kb-ingest-state-is-separate-from-vector-presence
  - silent-ingest-failure-warning-surface
  - local-first-operator-cockpit-with-risk
  - rag-as-activation-not-evidence
  - manifest-cache-with-spec-version
fusion_decision: adapt
borrow_value: medium
confidence: medium
evidence_count: 18
cross_validated_with:
  - VAKS Source Intake
  - VAKS Activation Tier
  - VAKS Evidence Support Check
  - VAKS Agent Gateway
negative_evidence:
  - runtime was not executed in this review
  - no authentication by design
  - Docker socket and host filesystem mounts appear in management compose
  - RAG and benchmark surfaces can be mistaken for authority
  - content-package inclusion does not equal source reliability
extension_potential: medium
relations: []
tags:
  - project-nomad
  - library-review
  - offline-knowledge-appliance
  - source-intake
  - curated-content-manifest
  - rag-ingest-guardrails
  - operator-cockpit
  - maintenance-diagnostics
  - security-risk
  - medium-borrow
  - candidate-only
---

# 库分析：Project N.O.M.A.D.

## 它解决什么问题

Project N.O.M.A.D. 解决的是“没有互联网或网络不稳定时，怎样把关键知识、地图、教育资源、工具、本地 AI 和管理面板放在同一台本地设备里”的问题。

它的产品链路大概是：

```text
install local command center
-> choose offline content packages
-> download / store Kiwix ZIM, maps, tools
-> optionally ingest content into KB / Qdrant
-> query through local AI assistant
-> monitor jobs, services, updates, disk and health
```

对 VAKS 的价值不是“照搬一个离线生存电脑”，而是提取几组工程边界：

```text
content package manifests are not trust labels
ingestion state must be visible before retrieval use
vector-store presence is not review
warnings are maintenance lint
operator cockpit must not become unsafe privilege surface
```

## 核心设计

Project N.O.M.A.D. 是 Docker 编排的本地知识 appliance。核心 Command Center 管理容器化工具、离线内容、下载、更新、KB ingestion、RAG search、服务状态和本地 AI。

主要层次：

- Content manifest 层：`collections/*.json` 描述 Wikipedia、Kiwix categories、maps 等可下载资源。
- Download / install 层：根据 manifest 选择资源并落到 storage。
- KB ingestion 层：扫描 embeddable files，维护 per-file state，dispatch embedding jobs。
- Vector retrieval 层：Qdrant 保存 chunks，RAG search 做 similarity、rerank、source diversity。
- Chat/context 层：Ollama/OpenAI-compatible endpoint + query rewrite + adaptive context injection。
- Operator 层：healthcheck、job health、warnings、Dozzle logs、updater sidecar、disk collector。
- Security/risk 层：README 明示无认证、网络层控暴露；compose 使用 Docker socket 和 host mount。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:17-53` | Offline-first knowledge/education server, browser Command Center, Docker orchestration, local AI, Kiwix, Kolibri, maps, tools, notes, benchmark. | Local-first knowledge appliance pattern. | Product bundle is broader than VAKS needs. |
| `README.md:105-115` | Offline use, zero built-in telemetry, no authentication, network-level controls, not direct internet exposure. | Clear privacy/security posture. | No-auth is a risk, not a VAKS adoption target. |
| `FAQ.md:11-19` | Storage path and external drive are host-level concerns. | Host-level storage config boundary. | Host flexibility does not remove backup/security duties. |
| `FAQ.md:70-76` | AI features are optional; Ollama/Qdrant/custom RAG not required for core use. | Optional AI layer. | AI layer should not be assumed in VAKS source intake. |
| `collections/wikipedia.json:1-51` | Wikipedia options with ids, sizes, URLs, versions. | Versioned source-package manifest. | Package choice is not reliability. |
| `collections/kiwix-categories.json:1-75` | Categories, tiers, recommended, includesTier, resources. | Tiered offline content package model. | recommended/include means coverage, not truth. |
| `collections/kiwix-categories.json:120-175` | Survival video/resources with versions, URLs, sizes. | Mixed media packages need extraction warning. | Video ZIM may produce zero text chunks. |
| `collections/kiwix-categories.json:580-615` | Computing/docs resources with tiny DevDocs packages and large StackExchange packages. | Size/cost variety requires manifest-aware estimates. | Size is not importance. |
| `admin/app/services/collection_manifest_service.ts:27-91` | Fetch, validate, cache specs by type with spec_version/fetched_at. | Refreshable manifest cache. | Cached manifest is not reviewed knowledge. |
| `admin/app/services/collection_manifest_service.ts:103-170` | In-flight downloads affect visible tier intent. | Operator UI can show user intent before completion. | Intent is not completion. |
| `admin/app/services/collection_manifest_service.ts:193-245` | Tier resolution, includesTier recursion, installed tier detection. | Completion logic for hierarchical packages. | Installed completeness is not evidence sufficiency. |
| `admin/app/utils/kb_ingest_decision.ts:3-70` | skip/dispatch/backfill_indexed/create_pending state machine. | Ingestion process state separated from vector presence. | State is process, not review. |
| `admin/app/services/rag_service.ts:1513-1648` | Storage scan, embeddable filter, policy Always/Manual, state rows, dispatch jobs. | Lazy/manual ingestion policy. | Dispatch does not equal extracted successfully. |
| `admin/app/services/rag_service.ts:1076-1130` | Stored files union Qdrant sources with state-machine file paths. | UI includes zero-chunk / browse-only / failed cases. | Qdrant-only view would hide failures. |
| `admin/app/utils/kb_warning_decision.ts:1-70` | zero_chunks and partial_stall warning decisions. | Failure lint for silent extraction problems. | Warning is not truth confidence. |
| `admin/app/utils/kb_ratio_lookup.ts:31-97` | Estimate chunks, unknown handling, longest-prefix match. | Pre-ingest cost estimate with uncertainty. | Estimate is not proof of completeness. |
| `admin/app/services/rag_service.ts:1159-1235` | computeFileWarnings returns ok=false when computation fails. | Avoid false healthy reporting. | ok=true/no warnings still not evidence support. |
| `admin/app/utils/kb_job_health.ts:1-50` | waiting/healthy/slow/stalled/failed status from activity timestamps. | Long-running job health model. | Health is operational, not source quality. |
| `admin/app/services/rag_service.ts:791-929` | Similarity search, threshold, metadata, rerank input. | Retrieval activation sample. | Rank/score is not support. |
| `admin/app/services/rag_service.ts:945-1053` | Semantic score quality gate, keyword boost, source diversity penalty. | Conservative reranking and diversity. | Diversity does not prove coverage. |
| `admin/app/controllers/ollama_controller.ts:74-130` | Query rewrite, retrieve top chunks, adaptive context budget, inject system context. | Context pack caution sample. | Injected context is still model input only. |
| `admin/app/controllers/ollama_controller.ts:366-445` | Model-size context limits and query rewrite fallback. | Budgeted activation. | Rewrite can distort query. |
| `admin/app/validators/common.ts:1-80` | URL guards for downloads and remote AI endpoints, with LAN-specific allowances. | Local appliance security tradeoff. | Needs dedicated VAKS threat model before borrowing. |
| `install/management_compose.yaml:11-69` | Admin and Dozzle expose ports and mount Docker socket; Dozzle actions/shell disabled. | Operator/log surface with explicit privilege concern. | No-auth + socket is high risk. |
| `install/management_compose.yaml:98-117` | Updater sidecar has Docker socket and writable project path; disk collector sees host FS read-only. | Sidecar/update/disk visibility pattern. | Privileged sidecars need least privilege and auth. |

## 当前支线价值

当前支线：

```text
Source Intake / Activation Tier / Retrieval Activation / Maintenance Lint / Agent Gateway risk
```

它对当前支线：

```text
refines, with risk
```

具体价值：

- 给 source package / offline package manifest 一个现实样本。
- 给 ingestion state 和 vector-store presence 的分离一个清楚样本。
- 给“摄取失败不要装作健康”一个具体 warning surface。
- 给 context pack / activation retrieval 一个 RAG-as-activation 的现实样本。
- 给 VAKS agent/tool/operator 面板一个安全反例：可见性有用，但权限边界必须更严。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Capture / Provenance | Offline content packages need source identity, URL, version, size, and local location. | adapt |
| Candidate Comprehension | Extraction state and zero/partial chunks must be visible before summarization or RAG use. | adapt |
| Knowledge Calibration | Package tier, installed state, vector chunk count, and RAG score cannot become truth confidence. | avoid confusion |
| Review / Consolidation | No direct review model exists here; VAKS must keep its own evidence-aware review. | do not adopt |
| Association / Activation | RAG search and source diversity can help activate context. | adapt carefully |
| Context Pack | Query rewrite, adaptive budget, and top chunks are useful but need source-span review for action basis. | adapt carefully |
| Decision / Action | Operator health and warnings can inform readiness, but cannot approve decisions. | support only |
| Use Ledger / Feedback | Job health, warnings, and update status can feed maintenance feedback. | adapt |
| Risk / Inhibition | No-auth, Docker socket, host mounts, updater sidecar are high-value cautions. | risk anchor |

## Borrow Judgment

```yaml
borrow_value: medium
tag_level: medium-borrow
fusion_decision: adapt
```

Why medium, not strong:

- The useful ideas are concrete but local to packaging, ingestion, retrieval activation, and operator surfaces.
- The project is not a knowledge truth/review system.
- Its default appliance security assumptions do not fit VAKS without major hardening.
- Runtime was not executed in this review.

## Risks

- RAG chunks can be mistaken for reviewed evidence.
- Kiwix package inclusion can be mistaken for trusted source selection.
- Benchmark / hardware scores can be mistaken for readiness.
- No authentication plus LAN exposure is not acceptable for VAKS agent/tool control.
- Docker socket and host filesystem mounts are high privilege and need a separate threat model.
- Local-first and no telemetry are good values, but they do not replace access control.

## Recommended VAKS Handling

Use this source as a candidate reference when:

- designing offline source package manifests;
- improving source intake state visibility;
- adding maintenance lint for extraction/indexing problems;
- designing local operator dashboards;
- clarifying that retrieval activation is not evidence support;
- threat-modeling future agent/tool dashboards.

Do not use it as:

- reviewed knowledge;
- truth maintenance architecture;
- action basis;
- a security-approved implementation;
- a reason to add an all-in-one appliance layer to VAKS core.

