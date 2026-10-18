---
record_kind: design_note
status: candidate
knowledge_status: candidate
project_id: VAKS
action_basis_allowed: false
truth_mutation_allowed: false
---

# Retrieval Layer North Star

## 说人话

普通检索系统想做的是：

```text
你问什么，我最快找出最像的内容。
```

VAKS 检索层要做的是：

```text
你问什么，我先判断哪些内容有资格参与这次回答，
再在有资格的内容里找最相关的，
还要把支持、反例、风险、过期和缺口都暴露出来。
```

## North Star

```text
High recall without authority collapse.
Fast retrieval without truth mutation.
Smart context without action-basis leakage.
```

## Candidate Pipeline

```text
1. Query Intent Router
   Decide the task type:
   recovery / exploration / intake / review / implementation / evidence / action.

2. Scope And Authority Filter
   Decide allowed buckets:
   raw / candidate / reviewed / overlay / feedback / archived.

3. Hybrid Recall Inside Allowed Buckets
   Use lexical, vector, entity, tag, and relation signals only where allowed.

4. Bucket-Local Rerank
   Rerank inside each bucket.
   Do not let a candidate outrank a reviewed note as if both had the same authority.

5. Anchor Queue
   Return source/chunk/heading/span anchors, not vague documents.

6. Context Pack Assembly
   Assign roles:
   core / support / risk / cold / challenge / missing.

7. Sufficiency Gate
   For action-facing use, check whether evidence is enough.
   For ordinary exploration, stay lightweight.

8. Query-Run Feedback
   Record what helped or failed.
   Feedback changes future activation, not truth.
```

## What turbovec Might Become

`turbovec` can fit at step 3/4:

```text
Hybrid Recall Inside Allowed Buckets
Bucket-Local Rerank
```

Its best role:

```text
compressed local vector cache
allowlist dense rerank
stable ID mapping from vector slots to source/chunk anchors
```

Its forbidden role:

```text
truth confidence
evidence support
reviewed relation creation
action readiness
```

## What Mnemosyne Might Become

`mnemosyne` can fit across steps 3-6:

```text
Hybrid Recall Inside Allowed Buckets
Bucket-Local Rerank
Anchor Queue
Context Pack Assembly
```

Its best role:

```text
local SQLite-derived retrieval cache pattern
hybrid lexical + vector recall pattern
polyphonic activation voices: vector / graph / fact / temporal
query cache and retrieval diagnostics
embedding refresh / stale-index cleanup rule
```

Its forbidden role:

```text
truth store
evidence support
review authority
agent memory authority
benchmark proof
```

VAKS adaptation:

```text
bucket filter before relevance
source hash before vector trust
same-authority-bucket RRF only
retrieval score as activation only
context-pack use with warnings and gaps
```

## What cBrain Official Mindmap Might Become

`cBrain official mindmap` can fit around steps 1, 5, and 6:

```text
Query Intent Router
Anchor Queue
Context Pack Assembly
```

Its best role:

```text
structure-first retrieval home
visible drawers before blank-box search
layered search: title / note / source text
node workbench for anchors, allowed use, and next moves
knowledge-quantity style activation and coverage hints
```

Its forbidden role:

```text
truth schema
evidence support
reviewed relation
action readiness
confidence score
```

VAKS adaptation:

```text
choose task or structure area first
derive allowed buckets before search
show layer/status/use limits on every result
turn search hits into anchor cards
send action-facing use through evidence and sufficiency gates
```

## What cBrain Offline Package Might Become

`cBrain 1.3.2 offline package` can fit around steps 3, 5, and 6:

```text
Hybrid Recall Inside Allowed Buckets
Anchor Queue
Context Pack Assembly
```

Its best role:

```text
graph + markdown + domain-object data-shape reference
anchor manifest inspiration
rebuildable relation cache inspiration
AI-friendly export mode inspiration
lazy migration workflow reference
```

Its forbidden role:

```text
private implementation source
truth schema
evidence support
review authority
action readiness
```

VAKS adaptation:

```text
markdown/yaml remains durable authority
derived graph/cache/index stays rebuildable
domain records link to anchors but do not prove claims
context exports carry authority and allowed-use labels
```

## What cBrain Quality Label Might Become

`cBrain quality transparency label` can fit around steps 5, 6, and 7:

```text
Anchor Queue
Context Pack Assembly
Sufficiency Gate
```

Its best role:

```text
readable quality label on retrieval result cards
transparent rigor for personal models and method notes
source / trust / consensus / scope / risk hints
last-checked and reviewer visibility
allowed-use explanation before context-pack inclusion
```

Its forbidden role:

```text
truth confidence
evidence support
reviewed relation
action readiness
automatic promotion
```

VAKS adaptation:

```text
backend fields stay strict
frontend label explains them plainly
personal models get transparent boundaries
review/action gates remain separate
```

## What Graphify Might Become

`safishamsi/graphify` can fit around steps 3, 5, and 6:

```text
Hybrid Recall Inside Allowed Buckets
Anchor Queue
Context Pack Assembly
```

Its best role:

```text
derived code/document graph cache
AST-first source and symbol anchors
community-neighborhood activation
query/path/explain style agent orientation
MCP-style read-only graph tools
incremental graph rebuild hygiene
graph-output safety guardrails
```

Its forbidden role:

```text
truth store
evidence support
reviewed relation
action readiness
default forced hook system
```

VAKS adaptation:

```text
bucket filter before graph traversal
graph distance/community as activation only
edge confidence as review routing only
query result becomes anchor queue, not answer
source/chunk drilldown remains mandatory for support
```

## What OneFeed Might Become

`arXiv:2606.07972 OneFeed` can fit around steps 1, 3, and 8:

```text
Query Intent Router
Hybrid Recall Inside Allowed Buckets
Query-Run Feedback
```

Its best role:

```text
controlled query variants from explicit query + active context
intent-anchor alignment
candidate usefulness as a query-generation quality signal
feedback for activation and routing
leakage-check checklist for retrieval pilots
```

Its forbidden role:

```text
benchmark evidence
truth confidence
reviewed relation
action readiness
feedback-driven truth mutation
```

VAKS adaptation:

```text
generate query variants only as candidates
filter by authority bucket before running variants
record why each variant exists
return anchor queue, not direct answer
feedback adjusts future activation only
```

## The Design Bet

The likely winning design is not:

```text
one giant RAG pipeline
```

It is:

```text
a governed retrieval stack
where each speed/recall trick is allowed only inside a declared boundary.
```
