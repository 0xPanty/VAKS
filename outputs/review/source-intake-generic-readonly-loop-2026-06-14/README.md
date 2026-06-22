# Source Intake Generic Read-Only Loop Package

Generated: 2026-06-22T15:34:42+00:00

## Human Summary

This package moves one step past v2: live local Markdown retrieval now flows through a generic read-only pack assembler.

It also adds the first Pro retrieval-plane contract: every query gets a `QueryPolicy` before retrieval, a bucket-first filter hook executes before ranking, and query-run/context-pack artifacts include the policy and bucket receipt.

This revision includes dedicated receipt-effect tests where restricted bucket policies create visible pre-ranking exclusions. The main harness now also includes default restricted review/action policy cases, so non-zero exclusion behavior is visible outside the dedicated paired suite too.

The assembler uses shared rules:

- candidate distillations become `review_input`;
- project overlays become `review_input`;
- raw source cards become `support` only in read-only support modes and only with a resolved raw/stable anchor;
- rank/score/diagnostic signals never become support anchors;
- action-mode queries do not become action basis.

Implemented retrieval channel: local Markdown lexical only.

Not implemented here: dense/vector retrieval, sparse semantic retrieval, graph overlay retrieval, RRF/hybrid fusion, or second-stage rerank.

## Supported Conclusion

In this packaged 20-query sandbox harness, a generic read-only assembler can route live top-k results into query-run / context-pack / answer-use artifacts while restricting final support to structurally resolved raw/stable anchors.

This package additionally supports the narrow claim that a sandbox `QueryPolicy` / authority-bucket receipt can be generated before retrieval and preserved through query-run/context-pack artifacts. The dedicated receipt-effect suite further demonstrates that the bucket-first hook can produce non-zero corpus exclusions under restricted policies.

The allow cases now include new non-FlexNote raw source-family smoke cases and low-cue allow queries that do not directly name the support heading. The package also includes decoy queries that should not pass as final support, plus a cue-depleted paraphrase pressure suite that is diagnostic rather than tuned to all-green. An author-side scripted semantic support self-check self-scored the allowed raw-anchor cases as relevant and sufficient for their narrow read-only query/use. Independent manual or external/blind semantic judgment is still not completed.

The default corpus now excludes `_runtime_test_fixtures`; the package also includes a clean corpus rerun as a no-op guard while keeping the scorer, query set, anchor vocabulary, and generic pack rules unchanged.

## Unsupported Conclusions

- Source Intake P0 passed: no.
- Generic production runtime validated: no.
- Live LLM/tool runtime validated: no.
- Live embedding/vector/graph retrieval validated: no.
- Independent/external/blind semantic support completed: no.
- Runtime adoption ready: no.
