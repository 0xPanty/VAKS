---
record_kind: retrieval_pilot_report
status: candidate
knowledge_status: candidate
project_id: VAKS
created_at: 2026-06-11
action_basis_allowed: false
truth_mutation_allowed: false
---

# VAKS + Yuxi-Like Retrieval Pilot Report

## 说人话结论

有帮助，而且是正向明显的帮助。

这轮没有部署完整 Yuxi，因为本机没有 Docker；但用本地脚本模拟了 Yuxi 类运行时的核心检索逻辑：

```text
document parsing
chunk anchors
metadata extraction
lexical + vector-like retrieval
RRF fusion
light graph/link boost
boundary labels / warnings
```

结果说明：

```text
VAKS 的脑子已经有边界规则。
Yuxi 这种运行时/检索层能明显增强 Agent 怎么拿资料。
第一阶段可以先只做边界提醒，不急着硬约束。
```

## What Was Tested

Three retrieval modes were compared:

```text
T0 baseline:
  file-level lexical retrieval.

T1 yuxi_like_no_labels:
  chunk-level lexical + vector-like retrieval + RRF + graph/link boost.
  No VAKS hard constraints.

T2 yuxi_like_boundary_labels:
  same retrieval as T1, but each result carries VAKS labels/warnings.
```

Two corpora were tested:

```text
primary:
  268 files, 3002 chunks.
  Main knowledge assets: wiki/raw/outputs qa/project overlays/current retrieval design.

full:
  4132 files, 17869 chunks.
  All Markdown in the repository, including old sandbox/noisy artifacts.
```

The query set had 12 real VAKS-style questions covering retrieval score, Mnemosyne, turbovec, candidate/action-basis boundary, context pack, feedback, agent access, source integrity, GraphRAG, Obsidian Bases, and strong distillation.

## Results

### Primary Corpus

| Mode | hit@5 | hit@10 | candidate/raw top1 | warning when needed |
|---|---:|---:|---:|---:|
| T0 baseline file lexical | 9/12 | 9/12 | 11/12 | 0/10 |
| T1 yuxi-like no labels | 11/12 | 12/12 | 9/12 | 0/10 |
| T2 yuxi-like boundary labels | 11/12 | 12/12 | 9/12 | 7/10 |

### Full Noisy Corpus

| Mode | hit@5 | hit@10 | candidate/raw top1 | warning when needed |
|---|---:|---:|---:|---:|
| T0 baseline file lexical | 6/12 | 7/12 | 9/12 | 0/10 |
| T1 yuxi-like no labels | 10/12 | 12/12 | 11/12 | 0/10 |
| T2 yuxi-like boundary labels | 10/12 | 12/12 | 11/12 | 10/10 |

## Interpretation

### 1. Retrieval got better

The Yuxi-like retrieval mode improved expected-source hit rate:

```text
primary hit@5:
  9/12 -> 11/12

full noisy hit@5:
  6/12 -> 10/12

full noisy hit@10:
  7/12 -> 12/12
```

The improvement is stronger in the noisy full corpus, which matters because VAKS has many outputs, raw records, overlays, old sandboxes, summaries, and reviewed wiki files mixed in the same repository.

### 2. Chunk anchors help

The baseline often found a whole file. The Yuxi-like mode returned heading-level chunks. For Agent work, that is more useful because the Agent can open a smaller anchor instead of rereading an entire source file.

This supports borrowing Yuxi's document-processing / chunk / metadata / retrieval pipeline.

### 3. Boundary reminders help, but they are not complete yet

T2 did not block retrieval. It only added VAKS labels and warnings.

That worked well in the full noisy corpus:

```text
warning-needed cases covered:
  10/10
```

In the primary corpus:

```text
warning-needed cases covered:
  7/10
```

The misses mostly came from core architecture docs inferred as `active` rather than raw/candidate/reviewed. That means the reminder layer needs a clearer status model for core docs:

```text
core_framework
reviewed
candidate
raw
overlay
feedback
diagnostic
```

This is a fixable adapter issue, not a reason to abandon soft governance.

### 4. Soft governance is a good first move

This pilot supports the user's hypothesis:

```text
Do not bind the Agent's hands first.
Give the Agent stronger retrieval plus visible boundary labels first.
Measure whether the Agent misuses results.
Only hard-gate high-risk operations.
```

Recommended phase split:

```text
exploration / research:
  soft labels only

review / evidence:
  labels + warning + required source anchors

action basis:
  labels + evidence sufficiency gate

formal writeback:
  review queue

external tool execution:
  user approval / intent gate
```

## How Yuxi Should Be Added

Do not put Yuxi above VAKS. Put it under VAKS as a runtime layer.

```text
VAKS Markdown/YAML
-> Yuxi-style document processing
-> derived chunk / vector / graph / metadata indexes
-> Agent retrieval through labels and warnings
-> VAKS context-pack / review / action-basis checks
```

Minimum adapter fields per chunk:

```text
path
heading
selector_or_line_range
source_hash
chunk_hash
knowledge_status
authority_bucket
retrieval_policy.policy_kind
retrieval_policy.pack_allowed
retrieval_policy.action_basis_allowed
warning_code
overlay_scope
review_pressure
generated_by
indexed_at
```

Yuxi-native pieces to test later when Docker is available:

```text
document parser -> Markdown
PostgreSQL chunk metadata
Milvus vector retrieval
Neo4j entity/relation retrieval
RRF fusion
Agent Context filtering
Skills / MCP tools
sandbox artifact generation
evaluation dashboard
```

## Risks

The biggest risk is not retrieval quality. It is authority confusion.

Risk cases:

```text
candidate top result sounds like final answer
graph edge sounds like reviewed relation
RRF score sounds like support
Yuxi evaluation score sounds like action readiness
Agent writes directly to formal knowledge
```

Mitigation for first integration:

```text
soft labels always visible
query-run trace saved
no formal writeback
no confidence mutation
no reviewed relation creation
no external action without intent gate
```

## Verdict

Yuxi-like logic is worth continuing.

It appears to be a strong complement to VAKS:

```text
VAKS = boundary brain
Yuxi-like runtime = retrieval hands and workbench
Agent = operator using the hands
```

The first integration should be:

```text
sandbox mirror
full-corpus indexing
soft boundary labels
no hard filtering except destructive/write/action paths
query-run evaluation
```

This should remain candidate-only until a real Yuxi deployment or equivalent runtime pilot reproduces the result.

