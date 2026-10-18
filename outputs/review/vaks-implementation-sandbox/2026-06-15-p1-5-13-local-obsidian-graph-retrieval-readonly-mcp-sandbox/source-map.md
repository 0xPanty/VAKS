---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox
status: implemented_pending_review
truth_boundary: sandbox_trace_only
---

# Source Map

## Project Rules Used

| Source | Rule used |
|---|---|
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1168-1208 | Kwipu-style sidecar finds local context; VAKS receipt/support/sufficiency/action gates decide use. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1210-1243 | Required candidate artifacts and acceptance cases KW-01 through KW-08. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1244-1255 | Forbidden imports: graph index as source of record, auto triple as reviewed relation, rank as support/action, generated citations as support, prompt as approval, MCP write tools, MD5 provenance, unreviewed cloud model. |
| `SOURCE_INTAKE.md` lines 738-879 | Bucket-first retrieval, selected_by as trace metadata only, read-only adapter returns context-pack candidates, graph paths/edges are recall metadata only. |
| `SOURCE_INTAKE.md` lines 1395-1460 | Graph/rank score cannot support; action-facing support must anchor to raw/stable material; retrieval rank is not trust. |
| `REVIEW_QUEUE.md` lines 433-448 | Similarity, graph neighbor, and association path are pending signals, not support/confidence/truth. |
| `REVIEW_QUEUE.md` lines 649-657 | Community report is briefing/review cue, graph rank is retrieval priority, auto-extracted relation is candidate relation, TextUnit anchor is provenance. |
| `REVIEW_QUEUE.md` lines 810-826 | Similarity/vector score/graph traversal cannot auto-support, increase confidence, promote, or create reviewed relations. |
| P1.5-12 Product Acceptance report | P1.5-13 should reuse JSON manifest / `issue_codes` / item result / non-claims style; real Obsidian graph and MCP runtime were intentionally not validated in P1.5-12. |

## Artifact Mapping

| Requirement | Artifact coverage |
|---|---|
| KW-01 triples are candidate graph fragments only | `fixtures/valid-readonly-query-graph-contract.json`, `failure-cases/triple-reviewed-relation.json` |
| KW-02 hybrid retrieval emits selected_by channels | `fixtures/valid-hybrid-graph-retrieval-receipt.json`, `failure-cases/hybrid-selected-by-missing.json` |
| KW-03 receipt lists included/excluded buckets | all fixtures, `failure-cases/receipt-buckets-missing.json` |
| KW-04 graph rank/retrieval score cannot support | `failure-cases/rank-as-support.json` |
| KW-05 cited answer cannot become action basis | `fixtures/valid-cited-answer-orientation-only.json`, `failure-cases/file-citation-action-basis.json` |
| KW-06 MCP read-only query only | `fixtures/valid-readonly-query-graph-contract.json`, `failure-cases/mcp-write-tool-exposed.json` |
| KW-07 derived cache records source/indexer/model/rebuild | `fixtures/valid-cache-mismatch-blocked-for-rebuild.json`, `failure-cases/cache-manifest-incomplete.json` |
| KW-08 cache/model mismatch blocks silent use | `fixtures/valid-cache-mismatch-blocked-for-rebuild.json`, `failure-cases/cache-model-mismatch-used.json` |
| Real vault access/write/sync forbidden | `failure-cases/real-vault-access-requested.json`, `failure-cases/vault-write-sync-requested.json` |
| Real vault path cannot be disguised as fixture-only | `failure-cases/real-vault-path-disguised-fixture.json` |
| MCP server/background/hooks forbidden | `failure-cases/mcp-server-started-background-hook.json` |
| Graph index not source of record | `failure-cases/graph-index-source-of-record.json` |
| MD5 not VAKS provenance hash | `failure-cases/md5-provenance-hash.json` |
| Cloud/unknown model locality needs review | `failure-cases/cloud-model-locality-unreviewed.json` |
| Prompt discipline not reviewer approval | `failure-cases/prompt-review-approval.json` |
| File citation cannot claim support even after a checked-looking field | `failure-cases/file-citation-claims-support-even-after-check.json` |
| Candidate structural triple cannot claim plain support | `failure-cases/triple-claims-support.json` |
| Derived cache cannot claim support/action/mainline authority | `failure-cases/cache-claims-authority.json` |
| Retrieval receipt cannot claim support/action/mainline authority | `failure-cases/receipt-claims-authority.json` |
| Receipt vector/rank/score cannot set support or confidence | `failure-cases/receipt-vector-score-claims-support.json` |
| Generated answer cannot claim support/action/mainline authority | `failure-cases/answer-claims-authority.json` |

## Boundaries

- No real Obsidian vault access is performed.
- No MCP server is started.
- No production `tools/` validator is created.
- No mainline docs, protected wiki paths, templates, tools, or Obsidian vault are
  edited.
- No evidence support, reviewed knowledge, reviewed relation, reviewer approval,
  action basis, promotion, commit, push, or sync is created.
