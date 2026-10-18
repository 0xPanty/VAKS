---
record_kind: design_questions
status: candidate
knowledge_status: candidate
project_id: VAKS
action_basis_allowed: false
truth_mutation_allowed: false
---

# VAKS Retrieval Layer Design Questions

## 1. What Are We Optimizing?

Not just:

```text
top-k semantic similarity
```

But:

```text
best allowed anchors for the user's task
```

Questions:

- Is the user asking for recovery, exploration, review, implementation, evidence, or action?
- Which authority buckets are allowed?
- Which retrieval signal is valid inside that bucket?
- Does the result need support, challenge, risk, stale, or gap material?

## 2. What Are the Buckets?

Candidate buckets:

```text
raw source
candidate distillation
review-ready summary
reviewed claim / pattern / decision
project overlay
feedback / query-run
archive / superseded
```

Questions:

- Which buckets can enter ordinary context packs?
- Which buckets can enter action-facing packs?
- Which buckets should be excluded by default?
- Can a bucket be active-project-only?

## 3. What Signals Are Allowed?

Potential signals:

```text
exact path / pinned ref
metadata filter
BM25
vector similarity
entity / alias match
topic / tag match
recency
review status
relation-neighborhood activation
feedback usefulness
```

Questions:

- Which signals are relevance only?
- Which signals are authority gates?
- Which signals are disallowed for action basis?
- Which signals can be fused, and only inside which bucket?

## 4. What Is the Anchor Unit?

Possible anchor units:

```text
file
heading
paragraph
chunk
line/span
source quote/span
reviewed claim ID
decision ID
relation ID
```

Questions:

- What is the smallest useful context unit?
- How do we prevent tiny chunks from losing meaning?
- How do we preserve source trace, hash, and heading context?
- How do we invalidate embeddings when text or model changes?

## 5. How Does a Context Pack Get Built?

Candidate path:

```text
query intent
-> allowed buckets
-> candidate anchors
-> rerank inside bucket
-> pack roles
-> coverage / omission check when needed
-> action-basis gate only for high-stakes/action use
```

Questions:

- What makes something `core` vs `support` vs `risk` vs `cold`?
- When do we require counterevidence retrieval?
- When do we stop and say evidence is insufficient?
- What trace must be recorded for later feedback?

## 6. What Should Be Cached?

Rebuildable cache candidates:

```text
BM25 index
vector index
entity/alias index
topic index
chunk manifest
query-run traces
relation-neighborhood activation map
```

Questions:

- If cache is deleted, can VAKS rebuild from Markdown/YAML?
- If cache disagrees with Markdown/YAML, which wins?
- How do we keep cache fast without making it a shadow truth store?

## 7. What Should the Pilot Prove?

Pilot should measure:

```text
recall@5 / recall@10
source-anchor correctness
authority-bucket violations
candidate-as-action-basis violations
counterevidence/risk recall
latency
memory footprint
cache rebuild/update/delete behavior
```

Questions:

- What query set represents real VAKS use?
- What negative tests catch boundary failure?
- What is good enough for a first retrieval layer?

