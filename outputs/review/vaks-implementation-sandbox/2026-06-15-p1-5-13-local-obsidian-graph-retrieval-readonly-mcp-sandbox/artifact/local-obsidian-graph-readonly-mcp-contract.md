---
record_kind: sandbox_local_obsidian_graph_readonly_mcp_contract
slice_id: 2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox
status: implemented_pending_review
truth_boundary: sandbox_contract_only
---

# Local Obsidian Graph Read-Only MCP Contract

## Purpose

This sandbox proves a narrow contract:

```text
Obsidian-style graph extraction can create candidate graph fragments.
Derived graph caches can help retrieval.
MCP can expose a read-only query surface.
None of those can create support, reviewed relations, truth, or action basis.
```

It validates synthetic JSON manifests. It does not access `H:\Obsidian\资料库`,
does not sync Obsidian, does not start an MCP server, and does not create
production tooling.

## Input Format

```json
{
  "record_kind": "local_obsidian_graph_readonly_mcp_manifest",
  "scenario_id": "example",
  "expected_valid": true,
  "expected_codes": [],
  "vault_access": {},
  "mcp_contract": {},
  "structural_triples": [],
  "derived_cache_manifest": {},
  "retrieval_receipt": {},
  "retrieved_context": [],
  "generated_answer": {}
}
```

## Required Boundaries

- `vault_access.sandbox_fixture_only` must be true.
- Vault access must be read-only.
- Real vault writes, sync, delete, export, hooks, and background services are
  forbidden.
- The MCP contract must expose `query_graph` or `query_vault_graph` as
  read-only/suggest-only.
- MCP tools must not expose write/save/delete/sync/promote/update/append/export.
- Structural triples from wikilinks/frontmatter/tags must remain
  `candidate_graph_fragment`.
- Derived cache manifests must record source state, indexer, model, and rebuild
  boundary.
- Stale or mismatched derived caches must not be used silently.
- Hybrid graph retrieval receipts must expose vector/BM25/temporal/synonym
  `selected_by` channels.
- Retrieval receipts must list included and excluded authority buckets.
- Derived caches, retrieval receipts, retrieved context, and generated answers
  must not claim support, truth, reviewed knowledge/relation, reviewer approval,
  action basis, promotion, or mainline readiness.
- Rank and score fields at receipt or context level must not claim support,
  confidence, trust, truth, reviewed status, or action authority.

## Blocking Codes

| Code | Meaning |
|---|---|
| `OG_INVALID_RECORD_KIND` | Wrong record kind. |
| `OG_MISSING_SCENARIO_ID` | Missing scenario id. |
| `OG_MISSING_VAULT_ACCESS` | Missing vault access block. |
| `OG_REAL_VAULT_ACCESS_REQUESTED` | Manifest requests real vault access instead of fixtures. |
| `OG_VAULT_NOT_READ_ONLY` | Vault access is not read-only. |
| `OG_VAULT_WRITE_OR_SYNC_REQUESTED` | Vault write/sync/delete/export requested. |
| `OG_MISSING_MCP_CONTRACT` | Missing MCP contract. |
| `OG_MCP_QUERY_TOOL_MISSING` | Read-only query tool is missing. |
| `OG_MCP_WRITE_TOOL_EXPOSED` | MCP write/save/delete/sync/promote operation exposed. |
| `OG_MCP_SERVER_STARTED` | Manifest starts a real MCP server. |
| `OG_MCP_BACKGROUND_OR_HOOK_ENABLED` | Background service or hook enabled. |
| `OG_TRIPLES_MISSING` | Missing structural triples. |
| `OG_TRIPLE_MISSING_SOURCE` | Triple lacks source/from/to. |
| `OG_TRIPLE_MISSING_SOURCE_HASH` | Triple lacks sha256 source hash. |
| `OG_TRIPLE_STATUS_NOT_CANDIDATE` | Triple status is not candidate graph fragment. |
| `OG_TRIPLE_CLAIMS_REVIEWED_RELATION` | Triple claims reviewed relation or authority. |
| `OG_TRIPLE_AUTO_PROMOTION` | Triple auto-promotes. |
| `OG_WEAK_HASH_AS_PROVENANCE` | MD5 used as VAKS provenance hash. |
| `OG_MISSING_CACHE_MANIFEST` | Missing cache manifest. |
| `OG_CACHE_MANIFEST_INCOMPLETE` | Cache manifest lacks source/indexer/model/rebuild fields. |
| `OG_GRAPH_INDEX_AS_SOURCE_OF_RECORD` | Derived graph index is treated as source of record/truth. |
| `OG_CACHE_CLAIMS_AUTHORITY` | Derived cache claims support/truth/approval/action/mainline authority. |
| `OG_CACHE_MISMATCH_USED` | Stale/mismatched cache used silently. |
| `OG_MODEL_LOCALITY_UNREVIEWED` | Cloud/unknown model locality not reviewed. |
| `OG_MISSING_RETRIEVAL_RECEIPT` | Missing retrieval receipt. |
| `OG_RECEIPT_BUCKETS_MISSING` | Receipt lacks included/excluded buckets. |
| `OG_RECEIPT_CLAIMS_AUTHORITY` | Retrieval receipt claims support/truth/approval/action/mainline authority. |
| `OG_BUCKET_FILTER_NOT_FIRST` | Ranking/fusion before bucket filtering. |
| `OG_HYBRID_SELECTED_BY_MISSING` | Hybrid graph route lacks vector/BM25/temporal/synonym channels. |
| `OG_CROSS_BUCKET_FUSION` | Graph retrieval fuses across authority buckets. |
| `OG_RANK_AS_SUPPORT_OR_CONFIDENCE` | Graph/rank/retrieval score claims support/confidence/trust. |
| `OG_CANDIDATE_CONTEXT_AS_SUPPORT` | Candidate graph/context item becomes support/action basis. |
| `OG_CONTEXT_CLAIMS_AUTHORITY` | Retrieved context claims support/truth/approval/action/promotion. |
| `OG_ANSWER_CLAIMS_AUTHORITY` | Generated answer claims support/truth/approval/action/mainline authority. |
| `OG_CITED_ANSWER_ACTION_BASIS` | File citations create support/action basis without gates. |
| `OG_PROMPT_AS_REVIEW_APPROVAL` | Prompt discipline claims review approval. |

## Non-Claims

Passing this sandbox is not evidence support, reviewer approval, reviewed
knowledge, reviewed relation, action basis, production MCP, Obsidian sync,
mainline readiness, commit permission, or push permission.
