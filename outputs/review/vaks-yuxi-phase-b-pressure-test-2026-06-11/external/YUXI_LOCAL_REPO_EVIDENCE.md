---
record_kind: external_repo_evidence
status: diagnostic
project_id: VAKS
created_at: 2026-06-11
action_basis_allowed: false
---

# Yuxi Local Repo Evidence

Yuxi was temporarily shallow-cloned for code/document inspection during this sandbox run.

Repository:

```text
https://github.com/xerrors/Yuxi.git
```

Observed HEAD:

```text
a8536a2e8520d1992a31bb6c22f219e60deca131
```

Local full-stack run status:

```text
not run
```

Reason:

```text
docker command not available on this machine
```

Key evidence from inspected files:

```text
README.md:
  Docker Compose is required for normal startup.

AGENTS.md:
  Project development/debugging is managed through Docker Compose.

backend/package/yuxi/knowledge/implementations/milvus.py:
  MilvusRetrievalConfig supports vector, keyword, hybrid retrieval,
  optional graph retrieval, optional reranker, and final top-k controls.
  The query flow uses vector + BM25 hybrid search, WeightedRanker,
  optional graph retrieval, and an RRF-like fusion for graph chunks.

backend/package/yuxi/knowledge/graphs/milvus_graph_service.py:
  Builds graph data from chunks and can rank chunks using PPR over graph seeds.

backend/package/yuxi/agents/toolkits/kbs/tools.py:
  Exposes query_kb, find_kb_document, and open_kb_document as knowledge tools
  with visible knowledge-base checks.

backend/package/yuxi/agents/backends/knowledge_base_backend.py:
  Resolves visible knowledge bases from user/context before query tools.
```

Comparator used in this sandbox:

```text
yuxi_native_profile =
  global visible-corpus hybrid chunk retrieval
  + vector-like recall
  + graph-like recall
  + global fusion/rerank
  + click-back
  - VAKS authority-bucket ordering
  - VAKS adapter/hash/receipt/governance fields
```

Boundary:

```text
This evidence supports a diagnostic comparator only.
It is not proof that original Yuxi was run end to end.
```

