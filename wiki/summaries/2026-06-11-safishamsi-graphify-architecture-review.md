---
type: summary
status: draft
title: "Graphify architecture review for VAKS retrieval layer"
created: 2026-06-11
source:
  - raw/repos/2026-06-11-safishamsi-graphify-source.md
source_repo: https://github.com/safishamsi/graphify
source_commit: 565026d3d10fb2d69bd01a5437433f278683fd8b
source_status: active
domain:
  - graph-retrieval
  - code-understanding
  - agent-context
related_projects:
  - verified-action-knowledge-system
current_branch: VAKS retrieval-layer design workspace
extracted_patterns:
  - derived graph cache
  - AST-first source anchoring
  - community-based context activation
  - graph query MCP tools
  - query-first agent orientation
fusion_decision: adapt-after-sandbox
confidence: medium
evidence_count: 13
cross_validated_with:
  - local source snapshot
  - GitHub API metadata
  - git ls-remote
negative_evidence:
  - Benchmarks not rerun locally.
  - Rapidly changing young repository.
  - Graph confidence labels are not evidence support.
extension_potential: high
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - summary
  - architecture-review
  - candidate-only
  - graph-retrieval
  - retrieval-layer
---

# Graphify 架构评审：VAKS 检索层候选

## 它解决什么问题

Graphify 解决的是“AI 看一个大项目/资料夹时，别一上来就全量 grep 或读 raw 文件”的问题。

它先把文件抽成图，再让 agent 用 query/path/explain/neighbor/community 等方式缩小范围。对代码库尤其明显：类、函数、导入、调用、文件位置这些结构，可以本地抽出来，不必先靠 LLM 猜。

## 核心设计

```text
file detect
-> code AST extraction
-> optional media/doc semantic extraction
-> graph build and dedup
-> community detection
-> report/export
-> CLI/MCP/assistant hooks
```

它的核心资产不是“答案”，而是一个可查询的结构图。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `docs/how-it-works.md` | Three-pass pipeline, community detection, confidence tags, cache, graph format | Clear source-to-graph-to-query story | README/doc claim, not independent benchmark |
| `ARCHITECTURE.md` | Module map: detect/extract/build/cluster/analyze/report/export/serve/watch | Good separation of ingestion, graph, report, serving | Module map is not runtime proof |
| `graphify/extract.py` | Tree-sitter language configs, source locations, relation/context fields | AST-first anchors and typed edges | Extracted edges still need VAKS policy labels |
| `graphify/build.py` | Normalized IDs, ghost duplicate merge, direction preservation, semantic dedup | Graph merge hygiene | Merge logic may still drop/reshape relations |
| `graphify/cluster.py` | Leiden/Louvain, oversized community splitting, stable ID remapping | Useful context grouping | Community is activation, not trust |
| `graphify/serve.py` | MCP tools: query_graph, get_node, get_neighbors, get_community, stats, PR impact | Agent Gateway inspiration | MCP output must stay read-only / candidate |
| `graphify/__main__.py` | CLI query parses budget/context/graph options and logs query results | Query-first workflow | Query logs and forced usage need privacy/mode gates |
| `graphify/cache.py` | SHA256 content cache, AST/semantic cache separation, portable source paths | Rebuildable derived cache | Cache is not authority |
| `graphify/detect.py` | file classification, sensitive-file skipping, incremental manifest | Source intake hygiene | Heuristics must be auditable |
| `graphify/hooks.py` | post-commit/post-checkout graph rebuild hooks | Freshness automation pattern | Dangerous as default in VAKS |
| `graphify/security.py` | safe fetch, path validation, size caps, sanitization | Guardrail checklist | Needs VAKS-specific threat model |
| `tests/test_confidence.py` | confidence_score round-trip and report checks | Some confidence behavior is tested | Test pass is diagnostic, not truth |
| `tests/test_cli_export.py` | export behavior for Obsidian/wiki/Neo4j/GraphML | Output-shape inspiration | Exported graph remains derived |

## 当前支线价值

当前支线：

```text
VAKS retrieval-layer design workspace
```

它对当前支线：

```text
refines
```

具体价值：

- 给 VAKS 一个“结构图检索层”的具体工程参照。
- 证明 query-first agent context 可以比盲读 raw files 更省上下文。
- 把 AST extraction、community activation、MCP graph tools、incremental cache、hook freshness、安全消毒这些点放到同一个可参考系统里。

风险：

- Graph rank / community / confidence label 很容易被误读成“可信”。
- Assistant hook 可能强迫 agent 越过用户意图和 VAKS authority bucket。
- semantic extraction 对文档/图片/论文/视频可能产出幻觉边。
- query log 和 source graph 可能泄露敏感语义。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Simple generated graph/report gives AI readable map | Adapt |
| Dusk workbench | graph.html/report/community view resembles project workbench | Adapt later |
| source ingest | detect/classify/skip-sensitive/convert sidecars | Adapt |
| review queue | AMBIGUOUS/INFERRED edges can route review | Adapt as review hints only |
| schema / reviewed knowledge | Not suitable as truth schema | Do not adopt |
| memory / dev context | query-first context and graph neighborhoods help activation | Adapt |
| feedback | query log can inform retrieval tuning | Adapt with privacy/off switch |
| retrieval / cache | strong value: derived graph cache, BFS/DFS, context filters | P1 candidate |
| API / MCP / agent access | read-only graph tools are useful Agent Gateway reference | Adapt in sandbox |
| viewer / workbench | graph.html/community/report useful for inspection | Watch |
| publishing | exports to Obsidian/wiki/Neo4j/GraphML are reference only | Watch |
| risk / anti-pattern | graph rank as trust; forced hooks; inferred edge as reviewed relation | Avoid |

## 值得提炼的模式

1. **AST-first anchor extraction**
   Deterministic structure should be extracted before model interpretation.

2. **Derived graph cache**
   A graph index can be rebuilt from authority sources and used for activation.

3. **Community activation**
   Communities can group context-pack candidates and reveal bridge/risk areas.

4. **Agent-facing query adapter**
   Agents need a small, typed retrieval API, not just raw file access.

5. **Confidence-as-routing, not truth**
   EXTRACTED/INFERRED/AMBIGUOUS is useful as review pressure, not final authority.

## 标签与量化

- domain: graph-retrieval / codebase knowledge graph / agent context
- problem: reduce context bloat and improve project/source orientation
- pattern: derived structural graph index
- maturity: emerging
- complexity: high
- problem_fit: 5
- reuse_value: 4
- implementation_cost: 4
- integration_fit: 3
- evidence_strength: 3
- reversibility: 4

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Graph traversal can improve retrieval orientation. | VAKS already allows association neighborhood activation. | candidate_relation | What graph fields must be bucket-filtered before traversal? |
| Graph confidence labels help triage review. | VAKS separates processing effort, retrieval policy, and truth confidence. | scope_mismatch risk | How to keep Graphify confidence from being read as VAKS confidence? |
| Agent should query graph before raw grep. | VAKS requires intent and authority gates before context. | candidate_relation with boundary | When is query-first useful, and when must raw evidence be inspected directly? |
| Hooks keep derived graph fresh. | VAKS avoids unapproved automation. | risk_of | Can freshness be manual/scheduled/sandboxed rather than default hook? |

Boundary:

- Similarity is not support.
- Graph edge is not reviewed relation.
- Community is not evidence.
- Query result is not action basis.

## Support / Challenge Review

- What supports it:
  - Primary repo source shows a coherent end-to-end graph pipeline and agent query surface.
  - Source files implement extraction, graph building, clustering, query traversal, MCP tools, cache, and security helpers.
  - Tests cover confidence round-trip/export/hook-adjacent behavior.
- What challenges it:
  - No local benchmark run inside VAKS.
  - The repo is active and young.
  - Graphify's own confidence tags are not designed for VAKS truth governance.
  - Forced assistant hooks can conflict with VAKS explicit-mode boundaries.
- Challenge severity: major for direct adoption; minor for design borrowing.
- Scope limits:
  - Best for code/source orientation and derived retrieval.
  - Not enough for evidence review, action basis, or truth maintenance.
- Known risks:
  - Prompt injection through source-derived labels.
  - Sensitive source/query leakage.
  - Graph cache staleness.
  - Overtrust in structural proximity.
- Review again when:
  - VAKS retrieval pilot exists.
  - A small adapter proves bucket-first graph traversal.
  - Local recall and anchor correctness are measured.
- Action readiness: not_ready.

## 对当前项目的适配点

Best VAKS adaptation:

```text
authority bucket filter
-> allowed source/chunk/node set
-> graph seed search
-> graph neighborhood expansion
-> community/risk/challenge hints
-> anchor queue
-> context pack
-> evidence/action gate only when needed
```

This lets VAKS borrow the useful graph intelligence without letting the graph
become authority.

## 不可行点 / 避坑

- Do not install Graphify hooks in VAKS mainline by default.
- Do not send candidate/reviewed/feedback buckets into one graph without policy labels.
- Do not treat `EXTRACTED` as reviewed support.
- Do not treat `INFERRED` as reviewed relation.
- Do not let graph visualizations become dashboards of truth.
- Do not rely on Graphify benchmark claims as VAKS evidence.

## 融合判断

- 结论：adapt-after-sandbox
- 理由：Graphify is highly relevant to retrieval-layer design, but VAKS needs stronger authority filtering and source-anchor governance than Graphify provides out of the box.
- 验证方式:
  1. Build a small VAKS sandbox graph from raw/candidate/reviewed notes.
  2. Apply bucket filtering before graph traversal.
  3. Compare against current rg/BM25/vector candidates.
  4. Measure anchor correctness, recall, and boundary violations.

## 直接判断

- Direct use: no
- Fork: no current need
- Design-only: yes, strong
- Reject: no
- Current branch value: P1 candidate for retrieval-layer design
- Whole architecture value: high as derived graph/cache/agent adapter reference
- Risk: authority collapse through graph rank/confidence/hooks
- Next action: keep in retrieval-layer design workspace; wait for broader frontier comparison before custom VAKS design.
