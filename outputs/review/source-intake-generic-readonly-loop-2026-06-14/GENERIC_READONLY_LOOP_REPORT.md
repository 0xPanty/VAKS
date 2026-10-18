# VAKS Source Intake Generic Read-Only Loop Report

Generated: 2026-06-22T15:34:42+00:00

## Verdict

This package addresses the specific Pro blocker about case-scripted pack role assignment by replacing case_id-based support selection with a generic read-only assembler.

It also implements the first step of the Pro retrieval-plane recommendation: a sandbox `QueryPolicy` is generated before retrieval, a bucket-first filter hook executes before ranking, and each query-run/context-pack carries a bucket receipt. Retrieval is still local lexical only; dense/vector, sparse, graph overlay, RRF fusion, and rerank are explicitly not implemented in this package.

This revision adds a dedicated receipt-effect suite: paired same-query cases restrict allowed buckets and demonstrate non-zero pre-ranking bucket exclusions, so the hook is now observable as more than bookkeeping under restricted policies. It also adds two restricted-policy cases to the main harness, one source_annotation bucket receipt-effect pair, and one reviewed-bucket receipt-effect pair.

The query set is still scripted, but pack roles are assigned by the same record_kind / knowledge_status / query_mode / raw-anchor-resolution rules for every hit. No case_id branch chooses a support item.

Anchor resolution remains intentionally narrow: support extraction is limited to a small stable-anchor heading vocabulary, section-content lexical overlap, and selector resolution. This is generic pack role assignment over a narrow anchor vocabulary, not general semantic support extraction.

## Results

- Cases: 20
- Expected decisions passed: 20 / 20
- Decisions: {'blocked_or_downgraded': 9, 'allowed_readonly': 11}
- Pack assembly: generic_record_kind_status_anchor_rules_no_case_id_role_branching
- QueryPolicy receipts: 20 / 20 (`results/generic_query_policy_receipts.csv`)
- Receipt-effect tests: pass / non-zero exclusions 4 / 4 / changed top-k pairs 4
- Default restricted policy cases: 2 / 2 passed with non-zero exclusions 2 / 2
- Source-annotation receipt-effect coverage: 2 cases / retained 1 / excluded 1
- Reviewed-bucket receipt-effect coverage: 2 cases / retained 1 / excluded 1
- Retrieval channels implemented: ['local_lexical']
- Retrieval channels not implemented: ['dense_vector', 'sparse_semantic', 'graph_overlay', 'second_stage_rerank', 'rrf_hybrid_fusion']
- New non-FlexNote read-only allow smoke cases: 3
- Low-cue allow cases: 5
- Decoy cases: 5
- Broken-anchor negative cases: 1 / 1 blocked as expected
- Cue-depleted paraphrase pressure: 1 allowed / 9 diagnostic queries; intended anchor selected in 1 / 9
- Clean corpus rerun: pass with default runtime fixture exclusion; excluded 0 additional runtime test fixture docs; expected decisions passed 20 / 20
- Full frozen replay: pass over 210 collected Markdown docs
- Semantic support self-check: author_side_scripted_self_check_completed_external_not_judged (author-side self-check completed; independent/external judgment still pending)

## Case Results

- `G3-01-candidate-query-generic-downgrade`: blocked_or_downgraded / top=`outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` / support_count=0
- `G3-02-raw-anchor-generic-allow`: allowed_readonly / top=`raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` / support_count=1
- `G3-03-mixed-pack-generic-selection`: allowed_readonly / top=`outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` / support_count=1
- `G3-04-project-overlay-generic-downgrade`: blocked_or_downgraded / top=`outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md` / support_count=0
- `G3-05-web-annotation-source-anchor-fresh-allow`: allowed_readonly / top=`raw/articles/2026-05-30-w3c-web-annotation-source.md` / support_count=1
- `G3-06-w3c-prov-boundary-fresh-allow`: allowed_readonly / top=`raw/articles/2026-05-29-w3c-prov-source.md` / support_count=1
- `G3-07-rag-attribution-fresh-allow`: allowed_readonly / top=`raw/papers/2026-05-29-rag-attribution-faithfulness-source.md` / support_count=1
- `G3-08-web-annotation-text-context-low-cue-allow`: allowed_readonly / top=`raw/articles/2026-05-30-w3c-web-annotation-source.md` / support_count=1
- `G3-09-w3c-prov-truth-boundary-low-cue-allow`: allowed_readonly / top=`raw/articles/2026-05-29-w3c-prov-source.md` / support_count=1
- `G3-10-rag-attribution-citation-split-low-cue-allow`: allowed_readonly / top=`outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` / support_count=1
- `G3-11-web-annotation-selector-fields-low-cue-allow`: allowed_readonly / top=`raw/repos/2026-06-11-awesome-obsidian-vault/maggieappleton-digital-gardeners-source.md` / support_count=1
- `G3-12-w3c-prov-entity-activity-agent-low-cue-allow`: allowed_readonly / top=`raw/articles/2026-05-29-w3c-prov-source.md` / support_count=1
- `G3-13-web-annotation-action-basis-decoy`: blocked_or_downgraded / top=`raw/articles/2026-05-30-w3c-web-annotation-source.md` / support_count=0
- `G3-14-w3c-prov-action-confidence-decoy`: blocked_or_downgraded / top=`outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md` / support_count=0
- `G3-15-rag-attribution-action-faithfulness-decoy`: blocked_or_downgraded / top=`outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` / support_count=0
- `G3-16-web-annotation-runtime-stack-decoy`: blocked_or_downgraded / top=`raw/articles/2026-05-30-w3c-web-annotation-source.md` / support_count=0
- `G3-17-w3c-prov-full-ontology-decoy`: blocked_or_downgraded / top=`raw/articles/2026-05-29-w3c-prov-source.md` / support_count=0
- `G3-18-broken-raw-anchor-negative`: blocked_or_downgraded / top=`raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` / support_count=0
- `G3-19-restricted-review-raw-anchor-policy`: allowed_readonly / top=`raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` / support_count=1
- `G3-20-restricted-action-evidence-buckets-policy`: blocked_or_downgraded / top=`raw/videos/2026-06-04-youtube-hermes-obsidian-source.md` / support_count=0

## Boundary

This is still sandbox runtime evidence. It does not prove Source Intake P0 passed, live LLM/tool runtime validation, live embedding/vector/graph retrieval, independent/external semantic support, or runtime adoption readiness.

The allowed raw/stable anchors have an author-side scripted semantic support self-check in `results/internal_semantic_support_self_check.csv`. This is still not independent manual review, external/blind judgment, or production groundedness validation.
