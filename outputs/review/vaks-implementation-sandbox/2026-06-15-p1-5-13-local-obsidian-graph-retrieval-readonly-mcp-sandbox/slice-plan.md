---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox
status: implemented_pending_review
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Slice ID

```text
2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox
```

## Why This Slice

P1.5-12 received `PASS_PRODUCT_GRADE`. Its Product Acceptance report explicitly
left real Obsidian graph / MCP runtime validation for later. The next required
item is P1.5-13:

```text
local Obsidian graph retrieval / read-only MCP sandbox
```

This slice proves a fixture-only contract for:

- wikilink/frontmatter/tag structural triples as candidate graph fragments;
- derived graph cache lifecycle;
- hybrid graph retrieval receipt;
- read-only MCP query surface.

## Only Write Path

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox/
```

## Non-Write Paths

No changes are allowed to:

```text
SCHEMA.md
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
README.md
wiki/claims/
wiki/patterns/
wiki/decisions/
templates/
tools/
H:\Obsidian\资料库
```

No commit, push, sync, dependency installation, long-running automation,
background service, hook, real MCP server, or MCP write tool is allowed.

## Artifact

- `artifact/local_obsidian_graph_readonly_mcp_sandbox.py`
- `artifact/verify_local_obsidian_graph_readonly_mcp_sandbox.py`
- `artifact/local-obsidian-graph-readonly-mcp-contract.md`
- `artifact/failure-case-oracle.md`
- `fixtures/*.json`
- `failure-cases/*.json`

The implementation uses Python standard library only and validates synthetic
JSON manifests.

## Acceptance Criteria

- Fixture-only vault access is required; real vault access, writes, sync, delete,
  and export are blocked.
- MCP contract exposes `query_graph` / `query_vault_graph` as read-only or
  suggest-only only.
- MCP write tools, server start, background service, and hooks are blocked.
- Structural triples must stay `candidate_graph_fragment`.
- Structural triples cannot claim reviewed relation, support, truth, approval,
  promotion, or action basis.
- Derived cache manifest records source state, indexer, model, and rebuild
  boundary.
- Derived graph index cannot become source of record or truth source.
- Cache/model/source mismatch blocks silent use.
- MD5 cannot be used as VAKS provenance hash.
- Hybrid graph receipt records included/excluded authority buckets and
  vector/BM25/temporal/synonym selected_by channels.
- Graph rank/retrieval score cannot become support/confidence.
- Candidate graph/context items cannot become support/action basis.
- File citations and anti-hallucination prompts cannot become support/action or
  reviewer approval.
- Local verification passes.
- Reviewer returns `REVIEW_PASS_NO_BLOCKER`.
- Boundary Auditor returns `BOUNDARY_PASS_NO_BLOCKER`.
- GPT-5.5 extra-high Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Stop Conditions

Stop and ask the user if this slice would require:

- accessing or writing the real Obsidian vault;
- starting a real MCP server;
- exposing MCP write tools;
- editing protected docs, wiki truth layers, templates, tools, or Obsidian vault;
- installing dependencies;
- starting a watcher, background service, or hook;
- commit, push, sync, or promotion;
- Product Acceptance returns `BLOCKED_NEEDS_USER`.

## Non-Claims

Passing this slice is not production MCP, production graph retrieval, evidence
support, reviewer approval, reviewed knowledge, reviewed relation, action basis,
mainline readiness, commit approval, push approval, or Obsidian sync approval.
