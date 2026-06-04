# Deep Research Prompt

I am building a Verified Action Knowledge System (VAKS).

Public story:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

Internal loop:

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

Important boundaries:

```text
provenance is not support
support is not truth
retrieval is not authority
source count is not independence
feedback changes activation/scope-fit, not truth
test/benchmark/LLM-judge results are diagnostic lint, not truth or runtime readiness
strict checks are lazy gates
```

We just ran the first real manual end-to-end trial in a sandbox. Four real papers were used:

```text
ALCE
Attributed QA
GopherCite
FRONT
```

The VAKS spine ran end to end:

```text
raw source
-> candidate
-> manual review
-> wiki claim
-> context pack
-> feedback
```

The system can run. The remaining problems are operational pain points.

Please do deep research on whether existing papers, libraries, standards, or product patterns can help with these four pain points:

## Pain Point 1: Source Independence Is Unclear

Multiple sources may support the same point, but they may:

```text
share origin
copy each other
cite the same upstream source
belong to the same research family
be benchmark variants from one community
```

We need mechanisms for source lineage, family hints, dependence tracking, claim-level deduplication, or independence review.

Do not suggest simple source counts as independent support.

## Pain Point 2: `processing_level` vs `source_access` Is Confusing

A source can be important enough for heavy processing, but the actual evidence access may be:

```text
abstract_only
snippet_only
source_span
full_text
```

We need clearer conceptual separation or naming patterns.

## Pain Point 3: `coverage_map` Is Too Heavy

Coverage maps are useful for context packs and action basis, but full coverage rows are too heavy for ordinary design answers.

Research progressive disclosure, evidence cards, minimal coverage maps, claim coverage UI, argument maps, audit cards, or similar patterns.

Goal: keep action-basis auditable without making every ordinary answer a full audit report.

## Pain Point 4: No Runtime Means Activation Change Is Manual

Feedback should alter:

```text
activation
scope-fit
future retrieval / framing
```

Feedback must not alter:

```text
truth confidence
verification status
source reliability
```

Right now activation change is represented only by before/after query-run notes.

Research lightweight activation logs, retrieval traces, feedback ledgers, query audit trails, memory reflection logs, or runtime-optional activation evidence.

## Research Requirements

Prioritize primary sources:

```text
papers
official docs
standards
open-source repos
technical docs
```

Avoid recommending:

```text
full platform rewrite
new truth core
SCHEMA rewrite
graph DB migration as the first move
LLM judge as truth
benchmark pass as truth
retrieval score as confidence
automatic promotion
automatic truth updates from feedback
```

For each candidate reference, provide:

```text
1. name and link
2. which pain point it addresses
3. key mechanism
4. smallest design VAKS could borrow
5. what VAKS should not absorb
6. whether it requires schema change: yes/no, prefer no
7. possible landing place:
   - operation convention
   - review-lite
   - anti-pattern
   - future runtime
   - parked
8. risk
```

Final table:

```text
pain point | external reference | borrowable mechanism | adoption degree | schema change? | suitable now?
```

Do not make final VAKS architecture decisions. Provide candidates, evidence, and tradeoffs only.

