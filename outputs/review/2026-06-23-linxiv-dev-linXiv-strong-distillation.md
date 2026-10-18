---
record_kind: candidate_distillation
status: draft
provisional: true
title: "linXiv：VAKS 论文源采集 / 本地研究库 / MCP 权限边界候选"
created_at: "2026-06-23"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
source_ref: "raw/repos/2026-06-23-linxiv-dev-linXiv-source.md"
derived_from: "[raw/repos/2026-06-23-linxiv-dev-linXiv-source.md, raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip, wiki/summaries/2026-06-23-linxiv-dev-linXiv-architecture-review.md, outputs/review/project_overlays/2026-06-23-linxiv-dev-linXiv-vaks-local-research-library-overlay.md]"
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint: "[paper-intake, source-identity, local-runtime-cache, obsidian-export-boundary, mcp-permission-boundary, tauri-sidecar-reference]"
possible_project_refs: "[verified-action-knowledge-system]"
source_annotation_refs: "[ann-linxiv-001-namespaced-source-id, ann-linxiv-002-data-dir-source-of-truth, ann-linxiv-003-obsidian-export, ann-linxiv-004-mcp-mutation-surface, ann-linxiv-005-case-collision, ann-linxiv-006-vault-path-containment]"
point_anchor_refs: "[source card inspected areas, snapshot README, ADR0002, ADR0014, linxiv_mcp.py, formats/markdown.py]"
borrow_value: medium
borrow_order: "P1 source identity and runtime data root; P2 source adapters/path containment/sidecar lifecycle; P3 Obsidian export and graph UI as product references"
avoid: "SQLite as VAKS truth; Obsidian export as reviewed knowledge; write-capable MCP without receipts/approval; current-core Tauri/PyInstaller/React complexity; ignoring case-colliding paths"
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "the task is specifically about VAKS paper/source adapters, source identity, runtime cache roots, MCP permission design, or desktop sidecar lifecycle"
  support_when: "designing source acquisition, local research-library workbench, export/import, runtime data pathing, or read-only agent access"
  risk_when: "someone proposes SQLite/app state, exported Markdown, MCP output, or write tools as reviewed truth/action basis"
  cold_references: "raw/repos/2026-06-23-linxiv-dev-linXiv-source.md; raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip"
tags: "[candidate, provisional, strong-distillation, linxiv, paper-intake, source-identity, local-first, mcp, candidate-only]"
---

# 候选蒸馏：linXiv

## 说人话

linXiv 不是 VAKS 的替代品。它更像一个成熟一些的本地论文管理应用：

```text
论文/PDF/DOI/arXiv/OpenAlex/CrossRef
-> 本地 SQLite
-> 项目、笔记、标签、图谱、导出
-> CLI / API / MCP / Tauri 桌面壳
```

对 VAKS 有价值的是“怎么管理研究源和本地运行态”，不是“怎么判断真理”。

一句话判断：

```text
linXiv 可以作为 VAKS 未来 paper/source adapter 和本地 cockpit 的候选参考。
它不配进入 VAKS 的 reviewed/truth/action 核心。
```

## 直接评分

| 维度 | 分数 | 判断 |
|---|---:|---|
| 论文/学术源采集参考 | 8/10 | arXiv、DOI、CrossRef、OpenAlex、PDF、BibTeX 都有实现痕迹。 |
| source identity 参考 | 8/10 | provider-prefixed `source_id` 很值得借鉴。 |
| 本地 runtime / cache pathing | 7.5/10 | `LINXIV_DATA_DIR` 这条非常实用。 |
| VAKS Obsidian 知识模型参考 | 3/10 | 它的 Obsidian export 太浅，不能当 VAKS 分层模型。 |
| MCP agent access 参考 | 5/10 | read/query 有价值，但写/删/导入工具风险很高。 |
| 直接拿来用 | 2/10 | 太产品化、太重，且和 VAKS source-of-truth 不同。 |

结论：

```text
design-only / source-adapter-reference now
sandbox later for paper intake or local cockpit
mainline authority no
```

## Candidate Point 1: source identity should be provider-prefixed

linXiv 的 `source_id` 设计很清楚：

```text
arxiv:2204.12985
openalex:W3123456789
doi:10....
local:{uuid/hash}
```

这对 VAKS 有直接参考价值。我们现在有 source cards，但未来做 paper/repo/video/API adapters 时，也需要避免：

```text
同一个裸 ID 在不同 provider 下撞名
本地文件没有外部 ID 时没有稳定身份
后来修复身份时丢掉 notes / links / versions
```

VAKS 适配方式：

```yaml
source_identity:
  provider: arxiv | doi | openalex | crossref | github | bilibili | local
  provider_scoped_id:
  vaks_source_id: "<provider>:<provider_scoped_id>"
  source_card_ref:
  captured_snapshot_ref:
  identity_status: provisional | canonical | repaired | merged_needed
```

边界：

```text
source identity = provenance / dedupe / routing
not evidence support
not truth confidence
not action basis
```

## Candidate Point 2: runtime data root must not pollute the source tree

ADR 0014 的价值很实在：

```text
runtime data has one explicit root
repo/source tree is not the fallback data dir
CLI/MCP/API/desktop all agree on it
```

这对 VAKS 未来很重要，因为我们迟早会有：

```text
derived indexes
search caches
source snapshots
viewer/cockpit state
MCP runtime receipts
temporary downloaded artifacts
```

VAKS 最小借法：

```yaml
runtime_artifact_root:
  source_of_truth: false
  derived_from_vault_commit:
  artifact_kind: retrieval_index | graph_cache | import_scratch | viewer_state
  location:
  rebuildable: true
  action_basis_allowed: false
  truth_mutation_allowed: false
```

不要借成：

```text
SQLite/runtime cache = VAKS source of truth
```

## Candidate Point 3: source adapters are useful, but only as acquisition

linXiv 的 adapter 面很完整：

```text
arXiv search/fetch
DOI resolution
CrossRef / OpenAlex
PDF metadata extraction
BibTeX import/export
Obsidian Markdown export
```

对 VAKS 的启发：

```text
source acquisition should become boring, repeatable, and provider-aware
```

但 VAKS 要比 linXiv 多两层：

```text
acquisition -> raw/source card
candidate extraction -> candidate points
evidence support -> only later, for specific point/relation/action
```

所以 linXiv 不能直接给 VAKS “论文可信结论”。它只能帮我们更稳地拿到和标识来源。

## Candidate Point 4: Obsidian export is a convenience layer, not VAKS knowledge

linXiv 能导出 Obsidian 风格 Markdown：

```text
paper metadata
YAML frontmatter
project paper list
```

这对普通研究者有用，但对 VAKS 太浅。VAKS 不能把这种 export 当作：

```text
reviewed claim
reviewed relation
decision
action basis
```

正确吸收方式：

```text
linXiv-like export
-> raw/source card or retained source text
-> candidate distillation
-> Evidence Packet only if later要 promotion/action
```

## Candidate Point 5: MCP must be permission-tiered before VAKS can use it

linXiv 的 MCP 很有意思，也很危险。

它不只是 search/list/fetch，还包含：

```text
create/update/delete project
add/remove tags
create/update/delete notes
import/export projects
download/import PDFs
restore/hard-delete trash
write env/settings surfaces elsewhere in API
```

对 VAKS 的结论很明确：

```text
read-only MCP first
write MCP later
destructive MCP almost never by default
```

VAKS MCP 权限分层候选：

```yaml
mcp_permission_tier:
  read:
    allowed:
      - search_sources
      - list_candidates
      - get_context_pack
  candidate_write:
    requires:
      - explicit_user_approval
      - operation_receipt
      - target_path_whitelist
  reviewed_write:
    allowed: false
  destructive:
    allowed: false
```

## Candidate Point 6: service boundary is useful, authority boundary still missing

ADR 0010 说 API 不能绕过 service layer 直接写 storage。这个工程纪律是好的：

```text
API -> service -> storage
```

VAKS 可以借它的“单写入路径”思想，但要补更强的层：

```text
capture service
candidate service
review service
action service
feedback service
```

不能把普通 service boundary 误读成 VAKS authority boundary。一个 API 走了 service，不代表它有资格写 reviewed truth。

## Candidate Point 7: sidecar lifecycle is future product reference, not current core

linXiv 的 Tauri sidecar/health-token/reaping 设计有价值：

```text
desktop app starts backend sidecar
health response carries per-launch token
do not adopt stale process
quit/rebuild cleans orphan processes
```

这对未来 VAKS cockpit 或本地 indexer 有帮助。但当前不要借太早：

```text
VAKS current core = Markdown/YAML + lazy gates
runtime product shell = future stage
```

如果以后要做本地 cockpit，linXiv 的 ADR 0018 是 P2/P3 参考。

## Candidate Point 8: case-colliding paths are a real source hygiene warning

本地 clone 在 Windows 提示：

```text
storage/config/sql/tables/PROJECT_TO_TAG.SQL
storage/config/sql/tables/PROJECT_TO_TAG.sql
storage/config/sql/tables/TAG.SQL
storage/config/sql/tables/TAG.sql
```

zip 快照里四个条目都存在，但 Windows 工作树只能保留其中一组。

这对 VAKS 很重要，因为我们常在 Windows 上做 repo intake：

```text
git clone result may lose information
zip snapshot may retain information
source review should record case-folding collisions
```

候选检查：

```yaml
repo_snapshot_hygiene:
  case_collision_detected: true
  affected_paths:
    - storage/config/sql/tables/PROJECT_TO_TAG.SQL
    - storage/config/sql/tables/PROJECT_TO_TAG.sql
    - storage/config/sql/tables/TAG.SQL
    - storage/config/sql/tables/TAG.sql
  review_pressure: review_due
```

## VAKS 融合方案

最小合理版不是“装 linXiv”，而是：

```text
P1-source-adapter-paper-intake-sandbox
```

输入：

```text
arXiv ID
DOI
PDF file
BibTeX file
OpenAlex ID
source card template
candidate distillation template
```

输出：

```text
source_identity_registry.example.yml
paper_source_card.example.md
source_snapshot_manifest.example.yml
provider_collision_case.example.md
obsidian_export_not_reviewed.failure.md
mcp_write_requires_operation_receipt.failure.md
```

验收：

```text
source identity stable
raw/source card created
snapshot hash recorded
candidate points separated
no reviewed knowledge created
no action basis created
MCP/write operations blocked by default
```

## Borrow / Adapt / Avoid

### Borrow

- Provider-prefixed source IDs.
- Source roots separate from version rows.
- Paper/source adapter interface.
- Runtime data root as explicit single source of truth for derived/runtime artifacts.
- Service boundary before storage writes.
- Path containment checks for local editor/workbench files.
- Health-token/orphan-reaping lesson for future sidecars.
- Broad test coverage as a maturity expectation for source-adapter code.

### Adapt

- Translate paper-centric source adapters into VAKS source-card creation.
- Convert Obsidian export into raw/candidate intake, not reviewed knowledge.
- Convert MCP into read-only-first tool tiers.
- Replace app-specific SQLite truth with Markdown/YAML source-of-truth plus rebuildable caches.
- Add VAKS operation receipts for any write/import/delete tool.
- Add case-collision scan to repo source snapshot hygiene.

### Avoid

- SQLite as VAKS canonical memory.
- Exported paper markdown as reviewed knowledge.
- API/MCP write paths without explicit approval.
- Hard-delete/restore/import tools exposed to agents by default.
- React/Tauri/PyInstaller stack inside current VAKS core.
- Product UI complexity before source/review/action gates are proven.

## Open Questions

- Should VAKS create a `source_identity` helper for provider-prefixed IDs?
- Should paper intake use arXiv/OpenAlex/CrossRef directly, or stay manual until review gates are stronger?
- What is the minimal source-adapter output that feeds existing `raw/papers/` without creating new lane complexity?
- Should repo intake add a case-collision detector before local clone inspection?
- If VAKS exposes MCP, should first release be read-only search/get/context-pack only?
- Where should derived runtime data live relative to `C:\Users\Administrator\Documents\资料库` and `H:\Obsidian\资料库`?

## Routing Hint

Route this source to:

```text
paper intake
source identity
source adapter hygiene
runtime artifact root
MCP permission tiers
sidecar lifecycle
cross-platform repo snapshot hygiene
```

Do not route to:

```text
reviewed truth
reviewed relation
action basis
Obsidian knowledge model
current VAKS core implementation
```

## Bottom Line

linXiv 对 VAKS 最有价值的一句话：

```text
以后如果 VAKS 要更系统地吃论文/DOI/PDF，source identity 和 adapter 边界要先设计稳。
```

它最危险的一句话：

```text
因为它有 MCP 和 Obsidian export，所以 agent 可以直接写知识库。
```

VAKS 的正确回应：

```text
source acquisition 可以借。
authority boundary 必须自己守。
```
