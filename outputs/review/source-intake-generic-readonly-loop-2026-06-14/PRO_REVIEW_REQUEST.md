# Pro Review Request

Please reverse-audit this generic read-only loop package.

Focus:

1. Does pack role assignment avoid case_id-based support selection?
2. Do the generated query-run/context-pack/answer-use artifacts show generic routing of candidate/overlay/raw hits?
3. Does the new sandbox `QueryPolicy` receipt correctly show authority-bucket filtering before ranking, allowed roles, support-candidate buckets, implemented local lexical channel, and explicitly disabled dense/vector/sparse/graph/RRF/rerank channels?
4. Do `results/receipt_effect_*` demonstrate non-zero bucket exclusions when allowed buckets are restricted, and do paired same-query cases show changed top-k behavior without changing scorer or corpus?
5. Do the new default restricted policy cases in the main harness produce non-zero exclusions, rather than leaving all exclusion evidence only in the dedicated paired suite?
6. Does the new source_annotation receipt-effect pair show source_annotation bucket retention/exclusion behavior?
7. Does the new reviewed-bucket receipt-effect pair exercise a real reviewed bucket document in baseline and exclude it in treatment?
7. Is legacy fallback truly gone from the packaged generic path? Check that the old known-anchor constant, forced-hit helper, known-anchor resolution label, forced-anchor marker, and high-score injection pattern are absent from packaged scripts and generated artifacts.
8. Does the full collected Markdown corpus snapshot and replayer reproduce this package's top-k order?
9. Do the three new non-FlexNote read-only allow smoke cases (W3C Web Annotation, W3C PROV, RAG attribution faithfulness) reduce the single-anchor-family concern without overclaiming semantic support?
10. Do the low-cue allow queries avoid directly naming support headings while still resolving support through section-content overlap?
11. Does the cue-depleted paraphrase pressure suite honestly expose robustness limits rather than tuning every natural query to pass?
12. Do the decoy queries avoid false support, especially action-mode and implementation/runtime decoys?
13. Does the clean corpus rerun still pass after excluding `_runtime_test_fixtures`, without changing scorer, query set, anchor vocabulary, or pack rules?
14. Is the judge-only semantic support packet actually ready-but-not-judged for independent double-judge use: opaque row_id, no case_id, no expected outcome, no mapping, no author-side self-check?
15. Does the package avoid overclaiming P0, live LLM/tool runtime, vector/graph retrieval, semantic support, or adoption readiness?

Truth boundary: the new QueryPolicy is a sandbox receipt contract plus receipt-effect test only. Live local lexical retrieval here means local Markdown lexical retrieval only. Dense/vector/sparse/graph/RRF/rerank are not implemented. Independent/external semantic support judgment is still not completed until judges fill the judge-only packet.
