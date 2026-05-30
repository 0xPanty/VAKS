---
type: source-review
status: draft
created: 2026-05-30
project: verified-action-knowledge-system
source_name: MemGAS / From Single to Multi-Granularity
source_urls:
  - https://arxiv.org/abs/2505.19549
  - https://arxiv.org/pdf/2505.19549
  - https://openreview.net/forum?id=i2yIvZARnG
  - https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS
  - https://github.com/quqxui/MemGAS
checked_commit: c2d4e9fdc331074802a711baf4371197f9194399
review_mode: paper and read-only code review
fusion_decision: adapt
confidence: medium
tags:
  - memgas
  - agent-memory
  - multi-granularity-memory
  - activation-tier
  - context-pack
  - alpha-detail-mining
---

# MemGAS Alpha Review: Multi-Granularity Memory Activation

## One-Line Judgment

MemGAS 的核心不是知识库审查，而是：

```text
Agent 聊久以后，历史太多，不能全塞上下文，也不能只靠一层摘要。
所以把记忆拆成多种粒度，再按问题选择最合适的那几层。
```

对我们来说，能借鉴的是一个小而硬的 alpha：

```text
Multi-Granularity Activation Views
```

说人话：

```text
它帮 Misa / Codex 更聪明地找“该看哪类历史”。
它不帮资料库判断“什么是真的”。
```

## Source Identity

Paper:

```text
From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents
```

Paper URLs:

```text
https://arxiv.org/abs/2505.19549
https://arxiv.org/pdf/2505.19549
https://openreview.net/forum?id=i2yIvZARnG
```

Official code URL from the ICLR / arXiv paper:

```text
https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS
```

Also observed same-head mirror / author-linked repo:

```text
https://github.com/quqxui/MemGAS
```

Checked commit:

```text
c2d4e9fdc331074802a711baf4371197f9194399
```

Local read-only sandbox clones:

```text
C:\Users\Administrator\Documents\资料库_alpha_lab_2026-05-30\repos\ICLR2026_MemGAS
C:\Users\Administrator\Documents\资料库_alpha_lab_2026-05-30\repos\MemGAS
```

Note:

```text
Both official repo and quqxui/MemGAS resolved to the same HEAD commit on 2026-05-30.
Use the Applied-Machine-Learning-Lab URL as the primary source identity.
```

## What It Is

MemGAS is a long-term memory retrieval and association system for conversational agents.

Its target problem:

```text
An agent accumulates many past conversations.
Full history is too noisy.
One summary is too lossy.
Single-granularity retrieval often misses either detail or cross-session context.
```

Its solution:

```text
Represent each dialogue memory at several granularities.
Associate related old and new memories.
At query time, route to the granularity that looks most certain.
Use graph propagation and filtering to return compact relevant memory.
```

It is not:

```text
a source provenance system
a truth review framework
an evidence warrant model
a reviewed relation system
a replacement for our evidence-aware review chain
```

## Core Logic

### 1. Four Memory Views

For each conversation session, MemGAS keeps several views:

```text
session
turn
summary
keyword
```

Code anchors:

- Memory add path generates summary, keywords, and vectors: `quickstart/memory.py:40`
- Summary / keyword generation: `quickstart/memory.py:119`
- Embedding views: `quickstart/memory.py:124`
- Returned hit exposes summary, keywords, and granularity scores: `quickstart/memory.py:87`

GitHub anchors:

- https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS/blob/c2d4e9fdc331074802a711baf4371197f9194399/quickstart/memory.py#L40-L62
- https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS/blob/c2d4e9fdc331074802a711baf4371197f9194399/quickstart/memory.py#L87-L108
- https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS/blob/c2d4e9fdc331074802a711baf4371197f9194399/quickstart/memory.py#L119-L145

Design extraction:

```text
Do not store only one memory shape.
Keep raw-ish detail, session-level context, compressed summary, and keyword/theme view.
Pick among them at use time.
```

### 2. Query-Time Granularity Routing

MemGAS does not always use the same view. It computes similarity distributions per granularity and uses entropy as a certainty signal.

Plain meaning:

```text
If one granularity has a clear best match, trust that granularity more for this query.
If a granularity has many fuzzy matches, reduce its weight.
```

Code anchors:

- Retrieval modes include session / turn / summary / keyword / hybrid: `quickstart/retriever.py:16`
- MemGAS mode invokes multi-granularity fusion: `quickstart/retriever.py:46`
- Entropy router weights: `quickstart/retriever.py:94`
- Lower normalized entropy creates higher weight: `quickstart/retriever.py:102`

GitHub anchors:

- https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS/blob/c2d4e9fdc331074802a711baf4371197f9194399/quickstart/retriever.py#L16-L47
- https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS/blob/c2d4e9fdc331074802a711baf4371197f9194399/quickstart/retriever.py#L94-L110

Design extraction:

```text
Routing can be based on how decisive a retrieval view is, not only on raw score.
```

Our translation should stay lighter:

```text
No need to implement entropy math immediately.
But keep the design concept: choose activation view by query type and match certainty.
```

### 3. Association Graph Is Retrieval Infrastructure

MemGAS builds an association graph across memory views. It uses GMM to select related old memories and Personalized PageRank to propagate query relevance.

Code anchors:

- GMM edge selection: `src/construct/construct_asso.py:11`
- Node ids include session / turn / summary / keyword: `src/construct/construct_asso.py:72`
- Association graph construction: `src/construct/construct_asso.py:87`
- Runtime graph and PPR path in quickstart retriever: `quickstart/retriever.py:67`
- Personalized PageRank call: `quickstart/retriever.py:79`
- GMM edge selection in quickstart: `quickstart/retriever.py:161`

GitHub anchors:

- https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS/blob/c2d4e9fdc331074802a711baf4371197f9194399/src/construct/construct_asso.py#L11-L27
- https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS/blob/c2d4e9fdc331074802a711baf4371197f9194399/src/construct/construct_asso.py#L72-L101
- https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS/blob/c2d4e9fdc331074802a711baf4371197f9194399/quickstart/retriever.py#L67-L92
- https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS/blob/c2d4e9fdc331074802a711baf4371197f9194399/quickstart/retriever.py#L146-L186

Design extraction:

```text
Associations help recall related memory.
They are not proof.
They are not reviewed relations.
They are activation edges.
```

This matches our existing boundary:

```text
Association Neighborhood Activation is retrieval / activation, not truth.
```

### 4. LLM Filtering After Retrieval

MemGAS retrieves candidate memory, then asks an LLM to filter irrelevant and redundant parts before answer generation.

Code anchors:

- Multi-granularity filtering prompt: `src/generation/generation_multigran.py:87`
- Prompt explicitly filters history, summaries, and keywords: `src/generation/generation_multigran.py:89`
- Retrieved context includes session, summary, and keyword: `src/generation/generation_multigran.py:108`

GitHub anchors:

- https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS/blob/c2d4e9fdc331074802a711baf4371197f9194399/src/generation/generation_multigran.py#L87-L112

Design extraction:

```text
Retrieved memory should be filtered before it becomes answer context.
But filtering is context preparation, not review.
```

## What We Should Borrow

### Alpha: Multi-Granularity Activation Views

Add a lightweight activation idea:

```text
The vault can expose different views of remembered material depending on the question.
```

For our system, possible activation views are:

```text
source_span
candidate_point
summary_view
keyword_or_theme_view
reviewed_node
reviewed_relation
decision_or_action_trace
feedback_event
review_due_item
```

This is not a new truth layer. It is only a smarter context-selection layer.

## Where It Fits In Our Architecture

Keep the public story unchanged:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

Keep the main internal chain unchanged:

```text
source
-> candidate point
-> calibration / point collision
-> evidence-aware review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback / review_due
```

MemGAS-style alpha fits here:

```text
query / agent need
-> Activation Tier
-> multi-granularity activation view selection
-> candidate context set
-> context pack trace
-> answer / action basis
```

It does not fit here:

```text
evidence-aware review
truth confidence
reviewed relation creation
promotion
source support judgment
```

## Misa vs Codex Fit

### Misa

Best fit.

Misa will likely accumulate:

```text
conversation history
user preference
prior instructions
failed attempts
successful actions
feedback events
query traces
review_due signals
```

MemGAS teaches us:

```text
Misa should not blindly search one flat memory pile.
Misa should choose the memory view based on the question.
```

Example:

```text
User asks: 我之前为什么说 Misa 只能查询，不能改资料库？

Misa should activate:
decision_or_action_trace
reviewed_node about agent memory quarantine
feedback_event / user instruction
possibly summary_view for surrounding rationale

Misa should not:
create a new reviewed relation
mutate truth confidence
write into main vault
```

### Codex

Secondary fit.

Codex can use it locally for:

```text
finding relevant review artifacts
finding source/code anchors
finding stale review_due records
assembling context packs faster
```

But Codex should still rely on:

```text
source files
review docs
schema rules
explicit evidence packets
```

## Minimal Adoption Version

Do not implement full MemGAS now.

Adopt only the conceptual rule:

```text
Activation should choose among memory/source views, not always retrieve one flat chunk type.
```

Possible future lightweight fields, if needed:

```yaml
activation_view_used:
  - source_span
  - reviewed_node
  - decision_or_action_trace
activation_reason: "query asks for prior design rationale"
activation_rank_basis: "query_type + local match"
activation_is_truth: false
```

This belongs on context-pack / activation records, not on reviewed knowledge records.

## What Not To Borrow

Do not borrow these into the main architecture now:

```text
full GMM association pipeline
full Personalized PageRank memory graph
automatic memory graph as knowledge graph
LLM-generated summary/keyword as fact
retrieval score as confidence
entropy score as truth signal
automatic relation creation from association edges
```

Reason:

```text
Our system is source-backed and review-backed.
MemGAS is activation-backed.
Mixing those would blur the most important boundary in the vault.
```

## Comparison With Prior Alpha Sources

MemGAS is complementary, not a replacement.

```text
PageIndexRAG-Web:
  source-internal structure navigation

GraphRAG-Example:
  graph context as activation / exploration

thirdspace vault/dashboard:
  operating protocol and health/risk surface

ZLAgent:
  agent operation gate and write-origin safety

MiniOpenClaw:
  skill-routed evidence locator

MemGAS:
  long-term agent memory chooses the right granularity at query time
```

Plain version:

```text
PageIndex helps read big documents.
MiniOpenClaw helps choose how to search.
MemGAS helps choose what memory shape to search.
ZLAgent helps stop agents from writing unsafe things.
Our vault still decides what counts as reviewed knowledge.
```

## Fusion Decision

Decision:

```text
adapt, but only as an activation/context-pack alpha
```

Accepted alpha detail:

```text
Multi-Granularity Activation Views
```

Rejected expansion:

```text
Do not make MemGAS a new memory truth layer.
Do not make its association graph a reviewed knowledge graph.
Do not make summary/keyword memory count as source evidence.
```

Best formulation for the main framework later:

```text
Activation may use multiple derived views of the same remembered material
such as raw span, candidate point, summary, keyword/theme, reviewed node,
decision trace, and feedback event. The selected view helps assemble a
context pack, but only reviewed evidence and reviewed relations can support
action.
```

## Status

This is an external alpha review artifact only.

No mainline architecture file has been changed.

