---
record_kind: sandbox_design_hardening_candidate
status: candidate
created_at: 2026-06-07
topic_id: source-intake-routing
truth_boundary: sandbox_design_only_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
allowed_use:
  - sandbox_review
  - workbench_design
  - pro_review_packet
forbidden_use:
  - truth
  - reviewed_relation
  - action_basis
  - platform_adoption
---

# Source Intake Routing Workbench Hardening

## Plain Summary

The first landing proved that source-intake-routing can be found and packed.
This hardening pass makes it harder to misuse:

```text
question -> intent mode -> lane-filtered retrieval -> lane-internal ranking
-> selector/snippet navigation -> action anchor_queue only
```

Nothing here promotes candidate material, project overlay, audit output, or
tool output into truth.

## Reference Set

Repository freshness and stars were checked on 2026-06-07 with the GitHub API.

| reference | checked value | used for |
|---|---:|---|
| https://github.com/langgenius/dify | 144156 stars, pushed 2026-06-06 | app front door and common question workflow |
| https://github.com/open-webui/open-webui | 140358 stars, pushed 2026-06-06 | workbench-style user entrypoints |
| https://github.com/elastic/elasticsearch | 76868 stars, pushed 2026-06-06 | pinned/boosted retrieval as navigation, not authority |
| https://github.com/run-llama/llama_index | 49958 stars, pushed 2026-06-04 | citation/query engine and source-node granularity |
| https://github.com/deepset-ai/haystack | 25467 stars, pushed 2026-06-05 | ConditionalRouter and DocumentSplitter patterns |
| https://github.com/explodinggradients/ragas | 14261 stars, pushed 2026-02-24 | faithfulness/support evaluation boundary |
| https://github.com/vespa-engine/vespa | 6950 stars, pushed 2026-06-06 | phased ranking / ranking profile separation |
| https://github.com/aurelio-labs/semantic-router | 3584 stars, pushed 2026-05-23 | lightweight semantic/intent routing |
| https://github.com/truera/trulens | 3359 stars, pushed 2026-06-05 | RAG triad / groundedness check boundary |
| https://www.w3.org/TR/annotation-model/ | W3C Recommendation | selector model inspiration |

Supporting docs / papers:

```text
Haystack ConditionalRouter:
  https://docs.haystack.deepset.ai/docs/conditionalrouter

Haystack DocumentSplitter:
  https://docs.haystack.deepset.ai/docs/documentsplitter

Elasticsearch pinned query:
  https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-pinned-query.html

Vespa ranking / phased ranking:
  https://docs.vespa.ai/en/ranking.html
  https://docs.vespa.ai/en/phased-ranking.html

LlamaIndex CitationQueryEngine:
  https://docs.llamaindex.ai/en/stable/api_reference/query_engine/citation/

Ragas faithfulness:
  https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/

TruLens RAG triad:
  https://www.trulens.org/getting_started/core_concepts/rag_triad/

W3C Web Annotation selectors:
  https://www.w3.org/TR/annotation-model/#selectors
```

## 1. Query Intent Router

Borrowed idea:

```text
Semantic Router / Haystack ConditionalRouter:
  classify the query before choosing the route.
```

VAKS adaptation:

```text
fixtures/query-intent-router-v0.json
tools/vaks-query-intent-router-v0.ps1
```

The router maps ordinary questions into:

```text
source-inspection
research
action
audit
project-exploration
```

What we did not borrow:

```text
No LLM classifier.
No vector router.
No autonomous agent route.
No authority score.
```

Reason:

```text
The router should be explainable and boring. It chooses a workbench lane, not a
truth status.
```

## 2. Lane-Internal Ranking

Borrowed idea:

```text
Elasticsearch pinned query:
  selected docs can be promoted for retrieval presentation.

Vespa phased ranking:
  first retrieve/filter, then rank within a controlled ranking profile.
```

VAKS adaptation:

```text
fixtures/source-intake-route-map.json
tools/vaks-context-pack-builder-v0.ps1
```

Ranking order:

```text
pinned_ref
> exact_topic_match
> entity_match
> recent_scout_or_current_sandbox
> ordinary_match
```

Guard:

```text
selection_priority is navigation priority.
selection_priority is not confidence, authority, truth, or action readiness.
```

What we did not borrow:

```text
No cross-lane RRF.
No global relevance score.
No trust score.
No semantic/vector dependency.
```

## 3. Obsidian Workbench Entrypoints

Borrowed idea:

```text
Dify / Open WebUI:
  make common user starts visible and repeatable.
```

VAKS adaptation:

```text
workbench/source-intake-routing.md
```

The page now includes common questions such as:

```text
Can this candidate be used as action basis?
Show me the source cards behind this scout.
What did the GitHub scout teach the workbench?
Why are candidate and overlay excluded from action mode?
What does the VAKS project overlay borrow?
```

What we did not borrow:

```text
No chat app clone.
No prompt library as truth.
No Obsidian plugin requirement.
```

## 4. Selector / Snippet v0

Borrowed idea:

```text
W3C Web Annotation selectors:
  selectors point to a location.

LlamaIndex CitationQueryEngine / Haystack DocumentSplitter:
  answers and chunks need smaller source units than a whole file.
```

VAKS adaptation:

```text
context pack item:
  selector_or_offset: line:N
  snippet: small preview
  snippet_status: navigation_snippet_not_evidence
```

Guard:

```text
A selector helps the reader open the right place.
A snippet is not evidence support.
A citation/clickback link is not enough for action-facing support.
```

What we did not borrow:

```text
No automatic quote-level proof.
No support score.
No span-level reviewed evidence mutation.
```

## 5. Action Anchor Queue

Borrowed idea:

```text
Ragas faithfulness / TruLens RAG triad:
  generated claims must be checked against retrieved context before being
  treated as supported.
```

VAKS adaptation:

```text
action pack:
  final_support.state: none
  anchor_queue.total: N
  action_readiness.state: not_ready
  required_next_step: evidence support check
```

Raw source role:

```text
raw_drilldown -> anchor_queue_raw_provenance
```

Guard:

```text
Raw source can be queued for checking.
Raw source is not automatically support.
Candidate / overlay / audit output is excluded from action support.
```

What we did not borrow:

```text
No automatic faithfulness evaluator.
No model-judged support as truth.
No benchmark score as authority.
```

## Implementation Map

```text
fixtures/query-intent-router-v0.json
tools/vaks-query-intent-router-v0.ps1
fixtures/source-intake-route-map.json
tools/vaks-context-pack-builder-v0.ps1
tools/vaks-context-pack-lint.ps1
workbench/source-intake-routing.md
checks/source-intake-routing-workbench-hardening-v0-1-test.md
```

## Design Verdict

This pass is stronger than copying any single reference because it combines:

```text
explicit intent routing
lane-filtered retrieval
lane-internal navigation ranking
selector/snippet clickback
action anchor_queue boundary
lint-enforced misuse checks
```

But it stays light:

```text
No service.
No database.
No plugin.
No new truth schema.
No automatic evidence evaluator.
No mainline change.
```

