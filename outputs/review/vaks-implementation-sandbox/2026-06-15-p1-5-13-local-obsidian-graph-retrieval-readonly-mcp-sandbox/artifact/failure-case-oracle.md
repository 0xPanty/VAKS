---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox
status: implemented_pending_review
truth_boundary: sandbox_oracle_only
---

# Failure Case Oracle

| Failure case | Primary expected code |
|---|---|
| `real-vault-access-requested.json` | `OG_REAL_VAULT_ACCESS_REQUESTED` |
| `vault-write-sync-requested.json` | `OG_VAULT_WRITE_OR_SYNC_REQUESTED` |
| `mcp-write-tool-exposed.json` | `OG_MCP_WRITE_TOOL_EXPOSED` |
| `mcp-server-started-background-hook.json` | `OG_MCP_SERVER_STARTED` |
| `triple-reviewed-relation.json` | `OG_TRIPLE_CLAIMS_REVIEWED_RELATION` |
| `triple-auto-promoted.json` | `OG_TRIPLE_AUTO_PROMOTION` |
| `graph-index-source-of-record.json` | `OG_GRAPH_INDEX_AS_SOURCE_OF_RECORD` |
| `cache-manifest-incomplete.json` | `OG_CACHE_MANIFEST_INCOMPLETE` |
| `cache-model-mismatch-used.json` | `OG_CACHE_MISMATCH_USED` |
| `md5-provenance-hash.json` | `OG_WEAK_HASH_AS_PROVENANCE` |
| `cloud-model-locality-unreviewed.json` | `OG_MODEL_LOCALITY_UNREVIEWED` |
| `hybrid-selected-by-missing.json` | `OG_HYBRID_SELECTED_BY_MISSING` |
| `receipt-buckets-missing.json` | `OG_RECEIPT_BUCKETS_MISSING` |
| `receipt-claims-authority.json` | `OG_RECEIPT_CLAIMS_AUTHORITY` |
| `receipt-vector-score-claims-support.json` | `OG_RANK_AS_SUPPORT_OR_CONFIDENCE` |
| `rank-as-support.json` | `OG_RANK_AS_SUPPORT_OR_CONFIDENCE` |
| `candidate-context-as-support.json` | `OG_CANDIDATE_CONTEXT_AS_SUPPORT` |
| `file-citation-action-basis.json` | `OG_CITED_ANSWER_ACTION_BASIS` |
| `answer-claims-authority.json` | `OG_ANSWER_CLAIMS_AUTHORITY` |
| `prompt-review-approval.json` | `OG_PROMPT_AS_REVIEW_APPROVAL` |
| `real-vault-path-disguised-fixture.json` | `OG_REAL_VAULT_ACCESS_REQUESTED` |
| `file-citation-claims-support-even-after-check.json` | `OG_CITED_ANSWER_ACTION_BASIS` |
| `triple-claims-support.json` | `OG_TRIPLE_CLAIMS_REVIEWED_RELATION` |
| `cache-claims-authority.json` | `OG_CACHE_CLAIMS_AUTHORITY` |

Expected failures are sandbox validation results only. Passing this suite does
not approve a real Obsidian graph, MCP runtime, support claim, reviewed
relation, action basis, commit, push, or sync.
