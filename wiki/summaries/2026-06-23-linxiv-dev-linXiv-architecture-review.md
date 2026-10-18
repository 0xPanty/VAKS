---
type: summary
status: draft
title: "linXiv architecture review for VAKS source intake and local runtime boundaries"
created: "2026-06-23"
library_name: "linXiv"
repo_url: "https://github.com/linxiv-dev/linXiv"
source_url: "raw/repos/2026-06-23-linxiv-dev-linXiv-source.md"
checked_commit: "8085eeb61d03cadeb74eff2352afc148a3fa202c"
commit_time: "2026-06-20T03:26:41Z"
source_status: active
reviewed_at: "2026-06-23"
domain: "local-first research paper manager / source adapters / MCP / Tauri sidecars"
related_projects: "[verified-action-knowledge-system]"
current_branch: "paper/source intake, source identity, MCP permission boundary, local runtime hygiene"
extracted_patterns: "[provider-prefixed source identity, runtime data root separate from source tree, source adapter interface, API/service/storage boundary, read-write MCP risk surface, sidecar lifecycle, case-collision source snapshot hygiene]"
fusion_decision: adapt-design-only
inspection_confidence: medium
evidence_count: 18
cross_validated_with: "[SOURCE_INTAKE.md, REFERENCE_REVIEW_PROTOCOL.md, outputs/review/2026-06-23-linxiv-dev-linXiv-strong-distillation.md]"
negative_evidence: "[runtime/tests not executed, MCP mutation/destructive operations, Windows case-colliding SQL paths, Obsidian export not authority model]"
extension_potential: "Medium-high for source adapters and runtime hygiene; low for VAKS authority model."
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
tags: "[summary, architecture-review, linxiv, source-intake, paper-intake, mcp, candidate-only]"
---

# linXiv 架构评审：VAKS 源采集与本地运行态候选

## 一句话判断

linXiv 对 VAKS 的价值是窄而实用：

```text
它适合当 paper/source adapter、source identity、runtime pathing、MCP permission 的候选参考。
```

它不适合当：

```text
VAKS truth model
reviewed knowledge workflow
action-basis engine
```

最小融合：

```text
linXiv-like paper adapter lessons
+ VAKS raw/source card
+ candidate distillation
+ review/action gates
+ read-only MCP first
```

## 它解决什么问题

linXiv 解决的是：

```text
研究者如何在本地管理论文、PDF、项目、笔记、标签、图谱和导出
```

它通过这些层实现：

```text
sources/*          academic metadata and PDF acquisition
storage/*          SQLite schema and versioned paper roots
service/*          app-domain service layer
api/app.py         FastAPI surface
linxiv_cli.py      CLI surface
linxiv_mcp.py      MCP tool surface
src/ + src-tauri/  React/Tauri desktop surface
formats/*          BibTeX/Markdown/Obsidian import-export
docs/adr/*         architecture decision record
```

VAKS 当前需要吸收的是：

```text
how source acquisition should identify, preserve, and route materials
```

不是：

```text
how an app database becomes memory truth
```

## 核心设计

### Data / Source Identity

```text
PAPER_ROOTS.SOURCE_ID
-> provider-prefixed identity
-> PAPER rows with versions
-> PAPER_META / notes / tags / projects
```

VAKS 可借：

```text
stable provider-scoped source identity
identity repair / merge-needed awareness
version rows separate from source root
```

### Source Acquisition

```text
arXiv
DOI
CrossRef
OpenAlex
PDF metadata
BibTeX
Markdown / Obsidian export
```

VAKS 可借：

```text
adapter interface and source metadata normalization
```

VAKS 不可借：

```text
adapter result as reviewed evidence
```

### Runtime / App Surface

```text
FastAPI
CLI
MCP
Tauri desktop shell
Python sidecars
```

VAKS 可借：

```text
permission tiers and sidecar lifecycle lessons
```

VAKS 不可借：

```text
write-capable agent surface by default
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Local-first desktop paper manager with SQLite, optional AI, Obsidian integration, graph view, Tauri. | Product-level orientation and scope. | README is not runtime proof. |
| `pyproject.toml` | Python package, CLI/MCP scripts, FastAPI, pydantic, pypdf, Gemini/OpenAI dependencies. | Shows app/backend packaging and source adapter dependency surface. | Not a VAKS dependency proposal. |
| `package.json` | React/Vite/Tauri frontend plus `build:sidecar`. | Product/cockpit build reference. | Current VAKS should not absorb the stack. |
| `src-tauri/tauri.conf.json` | Bundles API/CLI/MCP binaries, local API CSP, GitHub update endpoints. | Sidecar/capability boundary reference. | Product-stage only. |
| `docs/adr/0002-namespaced-source-id.md` | Provider-prefixed `source_id`. | Strong source identity candidate. | Not a reviewed schema change. |
| `docs/adr/0007-q-class-for-storage-queries.md` | Query builder and named SQL constants. | Storage/query discipline. | App-layer only. |
| `docs/adr/0010-service-layer-as-api-boundary.md` | Service layer is API write boundary. | Single write path lesson. | Does not equal VAKS authority gate. |
| `docs/adr/0014-data-dir-single-source-of-truth.md` | `LINXIV_DATA_DIR` for runtime data. | Strong future derived-cache pattern. | Markdown/YAML remains VAKS durable source. |
| `docs/adr/0017-editor-as-downloaded-cached-plugin.md` | Explicit install, sha256, no silent background auto-update. | Plugin lifecycle guardrail. | Future product reference. |
| `docs/adr/0018-sidecar-lifecycle-and-reaping.md` | Health token, stale process rejection, orphan cleanup. | Sidecar reliability pattern. | Future runtime reference. |
| `sources/base.py` | `PaperMetadata` and `PaperSource` protocol. | Source adapter shape. | Paper-centric; needs VAKS boundary fields. |
| `formats/markdown.py` | Markdown and Obsidian export. | User-facing export shape. | Export is not reviewed knowledge. |
| `linxiv_mcp.py` | Many MCP tools, including write/delete/import/restore/export. | Permission boundary warning. | VAKS must not expose this by default. |
| `service/vault.py` | Path containment for editor vault files. | Useful file operation safety pattern. | Runtime file safety, not knowledge authority. |
| `storage/config/sql/tables/*` | SQL schema includes case-colliding `.SQL` and `.sql` variants. | Snapshot hygiene warning. | Not a VAKS design pattern to copy. |
| `tests/*` | Broad test suite for app domains. | Good maturity sign for source-adapter code. | Tests were not run locally. |

## 当前支线价值

当前支线：

```text
source intake / paper scouting / MCP permission boundary / runtime artifact hygiene
```

它对当前支线：

```text
supports / refines / risk_of
```

具体价值：

- Supports: provider-prefixed identity helps paper/source adapters avoid collision.
- Supports: acquisition adapters show a practical arXiv/DOI/OpenAlex/CrossRef/PDF intake map.
- Refines: runtime data root discipline helps future derived indexes/caches.
- Risk_of: MCP write/delete tools show exactly why VAKS needs permission tiers and operation receipts.

风险：

- App database can be mistaken for source-of-truth.
- Obsidian export can be mistaken for reviewed knowledge.
- MCP can be mistaken for safe agent access.
- Desktop/runtime stack can pull VAKS away from Markdown-first core.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Helps acquisition and export, not raw/wiki loop itself. | adapt narrowly |
| Dusk workbench | Product surface ideas for local research cockpit. | watch |
| source ingest | Strongest fit: paper/source adapters and source identity. | adapt |
| review queue | Can feed candidate points; no review authority. | adapt with VAKS gates |
| schema / reviewed knowledge | App schema not suitable as reviewed knowledge schema. | reject |
| memory / dev context | Good Support/Cold Reference for paper-intake work. | adapt |
| feedback | No VAKS-like feedback ledger. | low |
| retrieval / cache | FTS/search and graph UI are useful product references. | watch |
| API / MCP / agent access | Great warning case: MCP must be permission-tiered. | adapt as guardrail |
| viewer / workbench | Tauri/React graph UI may inspire future cockpit. | watch |
| publishing | Export formats useful, but not publishing pipeline. | low |
| risk / anti-pattern | Case collisions, write-capable MCP, app DB as truth. | adopt as risks |

## 值得提炼的模式

### 1. Provider-scoped source identity

```text
source_id = provider + raw id
source root = stable identity
version rows = observations/versions
repair/merge = explicit operation
```

VAKS adaptation:

```text
source card id should be provider-aware where possible
local fallback should be explicit and repairable
```

### 2. Runtime data root

```text
source tree != runtime data
runtime data has one explicit root
all entry points agree on it
```

VAKS adaptation:

```text
derived caches/indexes can have a runtime root
but must remain rebuildable and non-authoritative
```

### 3. Source adapter acquisition, not support

```text
adapter fetches metadata/content
source card preserves provenance
candidate distillation extracts points
review checks support later
```

### 4. Read-only MCP first

linXiv shows why a rich MCP is tempting and risky. VAKS should start with:

```text
search/list/get/context-pack only
```

and delay:

```text
create/update/delete/import/export/restore/hard-delete
```

until operation receipts, approval prompts, and path scopes exist.

### 5. Case-collision scan for repo intake

The Windows clone warning is a concrete reminder:

```text
local checkout != complete source snapshot on case-insensitive filesystems
```

VAKS source intake should prefer a zip/tar source snapshot plus a collision scan for repo review.

## 标签与量化

- domain: local-first research paper manager / source adapters / MCP / Tauri sidecars
- problem: academic source acquisition and local research-library management
- pattern: provider-scoped source identity plus local runtime app shell
- maturity: emerging / active pre-stable
- complexity: high
- problem_fit: 4/5 for paper/source intake, 1/5 for truth/review
- reuse_value: 4/5 as design reference, 2/5 as direct implementation
- implementation_cost: 4/5 if adopted directly, 2/5 if only source-id lessons borrowed
- integration_fit: 4/5 for source adapter sandbox, 1/5 for VAKS core
- evidence_strength: 3/5 for source-inspected design, 1/5 for runtime behavior in this run
- reversibility: 5/5 if kept candidate/reference only

## 交叉验证

相似设计来源：

- VAKS SOURCE_INTAKE: raw/candidate/reviewed/action-basis separation.
- Previous source-adapter and paper-scouting sandbox notes.
- Kwipu/kk-knowledge-agent/agentmemory as MCP and local knowledge access comparison references.

支持证据：

- Source files expose concrete adapter, schema, CLI/API/MCP, and ADR decisions.
- Test suite breadth suggests non-trivial engineering maturity.
- README and ADRs acknowledge schema/paper ID churn and runtime pathing.

反例或失败边界：

- Runtime not executed locally.
- MCP includes destructive/write capabilities.
- Case-colliding SQL files break ordinary Windows checkout completeness.
- Obsidian export is not VAKS-aware.

最小验证方式：

```yaml
pilot_scope: sandbox_only
inputs:
  - one arxiv id
  - one DOI
  - one PDF fixture
  - one BibTeX fixture
checks:
  - source_identity_is_provider_prefixed
  - raw_source_card_created
  - candidate_points_created
  - no_reviewed_knowledge_created
  - no_action_basis_created
  - write_mcp_tools_blocked
  - repo_snapshot_case_collision_reported
```

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed / Candidate Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Provider-prefixed source IDs reduce identity collisions. | VAKS source cards already require source identity and provenance. | refines | Should VAKS add provider-scoped ID conventions for papers/repos/videos? |
| Runtime data root should be separate from source tree. | VAKS treats runtime artifacts as non-authoritative derived layers. | supports_with_boundary | Where should VAKS derived caches live, and how are they hash/manifests tied to vault commit? |
| Source adapters can automate paper intake. | VAKS says adapter output may create raw/source or candidate material only. | supports | What minimum adapter output fields should be required? |
| MCP exposes useful agent access. | Agent memory quarantine forbids direct reviewed truth mutation. | risk_of | Which tools are read-only enough for first MCP exposure? |
| Obsidian export creates useful Markdown. | VAKS says candidate/export material cannot become action basis. | scope_mismatch | How should exported paper cards be routed into raw/candidate layers? |

## Support / Challenge Review

What supports it:

- Source adapter code and CLI/API surfaces show concrete source acquisition workflows.
- ADRs show thoughtful identity, data-dir, service-boundary, plugin, and sidecar decisions.
- MCP implementation gives a real permission-surface specimen.
- Tests cover many app domains, though not run in this intake.

What challenges it:

- It is a product app, not a VAKS-style verified-action knowledge architecture.
- App DB and export formats can confuse authority layers if copied blindly.
- Mutation-heavy MCP tools are unsafe as a default VAKS agent interface.
- Case-colliding paths create intake fidelity risk on Windows.

Challenge severity:

```text
major for direct adoption
minor-to-medium for design-only paper/source intake borrowing
```

Scope limits:

```text
Use as source-adapter/runtime/MCP-boundary reference only.
Do not use as reviewed knowledge, reviewed relation, action basis, or current core dependency.
```

Known risks:

- Source acquisition becomes source support.
- Runtime DB becomes truth store.
- MCP write tools bypass approval.
- Exported Markdown bypasses candidate/review.
- Desktop sidecar complexity arrives before VAKS gates are stable.

Review again when:

- Paper intake sandbox begins.
- VAKS MCP tool design begins.
- A local cockpit/Tauri product surface is explicitly reopened.
- Repo snapshot hygiene validator is designed.

Action readiness:

```text
not_ready
```

## 对当前项目的适配点

Best VAKS shape:

```text
Provider source
  -> source adapter
  -> source identity registry
  -> raw/source card
  -> retained snapshot/hash
  -> candidate distillation
  -> review queue / Evidence Packet only when needed
```

MCP shape:

```text
read-only search/get first
candidate write only after operation receipt
reviewed write no
destructive operations no
```

Runtime shape:

```text
derived cache root
manifest with vault commit/source hashes
rebuildable
non-authoritative
```

## 可拓展性

- 是否适合作为插件/适配层：yes, for source adapters or future cockpit references.
- 是否会绑定核心结构：should not; keep source adapters outside truth core.
- 未来替换成本：low if only ideas are borrowed; high if app stack is adopted directly.
- 可迁移路径：start with source identity and paper adapter fixture before any UI/runtime.

## 复杂度和风险

- High product complexity.
- Medium source-adapter usefulness.
- High permission risk for MCP.
- Medium source hygiene risk due case-colliding paths.
- Low license compatibility for direct code borrowing should still be reviewed because GPL-3.0 differs from many permissive refs.

## 不可行点 / 避坑

- Do not install or fork linXiv as VAKS core.
- Do not treat `papers.db`/SQLite as VAKS canonical memory.
- Do not expose `delete`, `hard_delete`, `import`, `restore`, or env writes through VAKS MCP by default.
- Do not treat Obsidian export as reviewed notes.
- Do not inspect only the Windows checkout when case collisions exist; keep the zip snapshot.
- Do not add Tauri/React sidecar before source/review/action gates are product-ready.

## 融合判断

- 结论：adapt-design-only now; sandbox later.
- 理由：strong fit for source identity, paper intake, and runtime guardrails; weak fit for VAKS authority model.
- 验证方式：small paper-source-adapter sandbox with raw/candidate-only outputs and operation-receipt blocked write tools.

## 直接判断

- Direct use: no.
- Fork: no.
- Design-only: yes.
- Reject: reject as VAKS truth/review/action architecture.
- Current branch value: medium-high for paper/source adapter and MCP boundary.
- Whole architecture value: medium as local research-library product reference.
- Risk: high if app database/export/MCP output is treated as authority.
- Next action: keep candidate reference; consider a paper-intake sandbox only after explicit user approval.

## 后续行动

Do not update core architecture from this file alone.

If implementation starts later, first build:

```text
source_identity_registry.example.yml
paper_source_adapter_contract.md
repo_snapshot_case_collision_check.md
mcp_readonly_tool_contract.md
mcp_write_requires_operation_receipt.failure.md
obsidian_export_not_reviewed.failure.md
```
