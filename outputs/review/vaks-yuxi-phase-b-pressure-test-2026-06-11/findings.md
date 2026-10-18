---
record_kind: sandbox_findings
status: active
project_id: VAKS
created_at: 2026-06-11
truth_boundary: sandbox_notes_not_reviewed_knowledge
action_basis_allowed: false
---

# Findings

## Initial Grounding

- User requires quantitative pressure testing before keeping Phase B.
- Scope is sandbox-only.
- Phase B means retrieval/index/click-back/receipt only.
- No Skills, MCP write tools, subagents, formal writeback, or mainline architecture edits.

## Prior Pilot Baseline

Previous local Yuxi-like pilot showed:

```text
primary hit@5:
  baseline 9/12
  yuxi-like 11/12

full noisy hit@5:
  baseline 6/12
  yuxi-like 10/12

full noisy hit@10:
  baseline 7/12
  yuxi-like 12/12
```

Limit: it did not yet separate bucket-local VAKS+B from a Yuxi-native/global-fusion profile.

## Pro Review Points To Test

- VAKS authority-bucket filter should happen before Yuxi-style ranking.
- RRF must not merge across authority buckets as if they had equal authority.
- Vector similarity, graph rank, and eval score are activation signals, not evidence.
- Yuxi native runtime can be useful, but databases/graph/eval/tools must not become authority.

## Original Yuxi Feasibility And Shape

Local original Yuxi full-stack run is blocked because `docker` is not installed on this machine.

Yuxi repo was temporarily shallow-cloned into:

```text
outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/external/Yuxi
```

The full clone was removed after extracting the evidence summary to:

```text
external/YUXI_LOCAL_REPO_EVIDENCE.md
```

Observed HEAD:

```text
a8536a2e8520d1992a31bb6c22f219e60deca131
```

Relevant Yuxi shape from local code/docs:

- `README.md` and `AGENTS.md` say the project is Docker Compose managed.
- `backend/package/yuxi/knowledge/implementations/milvus.py` defines `MilvusRetrievalConfig` with vector, keyword, hybrid retrieval, optional graph retrieval, optional reranker, and final top-k controls.
- The same file uses vector + BM25 hybrid search and `WeightedRanker`, then optionally fuses graph chunks with base chunks using an RRF-like `1 / (60 + rank)` score.
- `backend/package/yuxi/knowledge/graphs/milvus_graph_service.py` builds graph indexes from chunks and can rank chunks by PPR over graph seeds.
- `backend/package/yuxi/agents/toolkits/kbs/tools.py` exposes `query_kb`, `find_kb_document`, and `open_kb_document` as Agent knowledge tools with visible-KB checks.
- `backend/package/yuxi/agents/backends/knowledge_base_backend.py` resolves visible knowledge bases by user/context before query tools.

Therefore the fair local comparator is:

```text
yuxi_native_profile =
  global visible-corpus hybrid chunk retrieval
  + vector-like recall
  + graph-like recall
  + global fusion/rerank
  + click-back/hash receipt
  - VAKS authority-bucket filtering
  - VAKS action-basis leakage prevention
```

This is not a claim that original Yuxi was run end to end.

## Pressure Test Result

The Phase B bucket-local mode passed the sandbox keep bar.

Primary corpus:

```text
baseline hit@5: 27/30
VAKS+B bucket-local hit@5: 30/30
Yuxi-native profile hit@5: 29/30

baseline action leakage: 1.0000
VAKS+B bucket-local action leakage: 0.0000
Yuxi-native profile action leakage: 1.0000
```

Full noisy corpus:

```text
baseline hit@5: 27/30
VAKS+B bucket-local hit@5: 30/30
Yuxi-native profile hit@5: 28/30

baseline action leakage: 1.0000
VAKS+B bucket-local action leakage: 0.0000
Yuxi-native profile action leakage: 1.0000
```

Important finding:

```text
Yuxi-like retrieval with labels but without bucket-local authority ordering is not enough.
It still lets risky candidate/diagnostic material take top1 on action/evidence queries.
```

Therefore the value is not "add Yuxi retrieval" alone.

The value is:

```text
Yuxi-like hybrid retrieval
+ VAKS authority bucket ordering before final ranking
+ VAKS adapter/hash/receipt/badge layer
```

Status:

```text
Keep Phase B as a sandbox candidate.
Do not promote to mainline yet.
Do not approve C-lite, Skills, MCP writes, subagents, or formal writeback.
```

## Iteration v1 Finding

`vaks_b_adapter_v1` adds anchor/path/exact-phrase aware ordering inside VAKS
authority buckets. It does not change which buckets are allowed to support
action/evidence answers.

Against the locked v0 baseline:

```text
main primary MRR:
  locked v0: 0.9083
  v1:        1.0000

main full MRR:
  locked v0: 0.8528
  v1:        1.0000

v1 action leakage:
  primary: 0.0000
  full:    0.0000
```

Holdout pressure test:

```text
primary hit@5:
  v0: 9/15
  v1: 10/15

full hit@5:
  v0: 9/15
  v1: 11/15

primary MRR:
  v0: 0.4771
  v1: 0.6144

full MRR:
  v0: 0.3665
  v1: 0.5868
```

Boundary stayed intact:

```text
action_leakage_rate: 0.0000
forbidden_top1_rate: 0.0000
cross_bucket_violation_rate: 0.0000
```

Known issues:

- `h13_resource_filter_before_search` regressed on primary; Yuxi middleware/resource-filter questions need a better retrieval anchor.
- `h10_old_sandbox_benchmark_truth` regressed on full; benchmark/lint/diagnostic boundary questions need canonical anchoring or metric review.

Decision:

```text
Keep v1 as the next sandbox candidate.
Do not promote to mainline.
Next step must be a v1.1 regression pass.
```

## Iteration v1.1 Finding

`vaks_b_adapter_v1_1` keeps the v1 authority boundary and adds topic-anchor
routing for:

- resource-filter / visible-resource / before-search questions
- benchmark / lint / diagnostic / mainline-readiness boundary questions

Main pressure set:

```text
primary:
  v1 MRR:   1.0000
  v1.1 MRR: 1.0000

full:
  v1 MRR:   1.0000
  v1.1 MRR: 1.0000

v1.1 leakage:
  action_leakage_rate: 0.0000
  forbidden_top1_rate: 0.0000
  cross_bucket_violation_rate: 0.0000
```

Holdout pressure set:

```text
primary hit@5:
  v1:   10/15
  v1.1: 12/15

full hit@5:
  v1:   11/15
  v1.1: 13/15

primary MRR:
  v1:   0.6144
  v1.1: 0.7811

full MRR:
  v1:   0.5868
  v1.1: 0.7591
```

Query-level regressions:

```text
main pressure: 0
holdout:       0
```

Decision:

```text
Keep v1.1 as the next sandbox candidate.
Do not promote to mainline.
Next step should be a minimal real adapter skeleton tested against v1.1.
```

## Minimal Skeleton Finding

The minimal read-only adapter skeleton now exists as:

```text
tools/vaks_phase_b_adapter.py
```

It emits:

```text
chunk manifest JSONL
retrieval receipt JSONL
adapter-shaped result objects
```

Generated artifacts:

```text
primary chunk manifest: 3947 chunks
full chunk manifest:    18708 chunks

main receipts:
  primary: 30 queries / 300 results
  full:    30 queries / 300 results

holdout receipts:
  primary: 15 queries / 150 results
  full:    15 queries / 150 results
```

Skeleton vs v1.1:

```text
main primary MRR:
  v1.1:     1.0000
  skeleton: 1.0000

main full MRR:
  v1.1:     1.0000
  skeleton: 1.0000

holdout primary MRR:
  v1.1:     0.7811
  skeleton: 0.7811

holdout full MRR:
  v1.1:     0.7591
  skeleton: 0.7591

action leakage:
  skeleton: 0.0000
```

Query-level regressions:

```text
main pressure: 0
holdout:       0
```

Decision:

```text
Keep the read-only skeleton as the next sandbox candidate.
Do not promote to mainline.
Next step should be an adapter contract test.
```

## Contract Test Finding

The first adapter contract test failed and exposed real skeleton defects:

```text
contract status: fail
error count: 5569
```

Failures were mainly:

- click-back line ranges sometimes pointed one line past EOF
- raw manifest rows did not carry warning codes
- receipt rows were missing `indexed_source_hash`

The adapter output was fixed, then the contract test passed:

```text
contract status: pass
error count: 0
```

Validated rows:

```text
manifest primary: 3991 rows / 0 errors
manifest full:    18785 rows / 0 errors
main receipts:    600 rows / 0 errors
holdout receipts: 300 rows / 0 errors
```

The contract test covers:

```text
manifest required fields
receipt required fields
policy kind and policy booleans
source/chunk hash shape
click-back target existence and line range
no action-basis permission leaks
risky action/evidence warning coverage
risky rows cannot claim reviewed relation state
```

Decision:

```text
Keep the contract-passing skeleton as the next sandbox candidate.
Do not promote to mainline.
Next step should be an integration readiness package.
```

## Integration Readiness Finding

The integration readiness package passed after two validator-driven fixes:

```text
readiness status: pass
error count: 0
```

Compared against the previous contract-passing skeleton, the readiness step:

```text
preserved main primary MRR:      1.0000
preserved main full MRR:         1.0000
preserved holdout primary MRR:   0.7811
preserved holdout full MRR:      0.7591
preserved action leakage:        0.0000
preserved contract status:       pass / 0 errors
added readiness status:          pass / 0 errors
```

The positive value is not a new retrieval improvement. The value is that the
same contract-passing skeleton now has:

```text
explicit adapter API shape
explicit read-only input boundary
explicit derived-output boundary
explicit mainline insertion point
explicit failure modes
explicit rollback path
machine-checkable readiness validation
```

Decision:

```text
Keep Phase B as a read-only sandbox integration candidate.
Do not promote to mainline.
Next step should be a mainline-readiness / Pro review packet before any core doc edits.
```

## Mainline-Readiness Finding

The mainline-readiness packet passed:

```text
mainline readiness status: pass
error count: 0
```

Compared against the previous integration readiness package, it preserved:

```text
readiness status: pass / 0 errors
contract status:  pass / 0 errors
core docs dirty lines: 0
metric floors: unchanged
```

The packet proposes a minimal first patch candidate only if later approved:

```text
SOURCE_INTAKE.md
IMPLEMENTATION_BLUEPRINT.md
DEV_CONTEXT.md
MEMORY_TIER.md
```

Deferred unless Pro asks:

```text
SCHEMA.md
REVIEW_QUEUE.md
templates/architecture-review-window-prompt.md
```

Decision:

```text
Keep the mainline-readiness / Pro review packet.
Do not edit core VAKS docs yet.
Next step should be Pro or human review of `PHASE_B_MAINLINE_READINESS_PACKET.md`.
```

## Pro Review Prompt Finding

The Pro review prompt passed:

```text
prompt status: pass
error count: 0
```

Compared against the previous mainline-readiness packet, it preserved:

```text
mainline readiness: pass / 0 errors
integration readiness: pass / 0 errors
contract: pass / 0 errors
core docs dirty lines: 0
```

The prompt adds a direct external-review shape:

```text
explicit no-edit / no-merge instruction
must-preserve VAKS boundary list
evidence files to inspect
current metric floor
candidate minimal touch set
candidate wording to review
required verdict format
hidden-risk question
```

Decision:

```text
Keep `PHASE_B_PRO_REVIEW_PROMPT.md`.
Do not edit core VAKS docs yet.
Next step should be external / Pro review.
```

## External Review Finding

The independent read-only review returned:

```text
Verdict: APPROVE_MINIMAL_DOC_PATCH
```

The external review result validator passed:

```text
external review status: pass
error count: 0
```

The reviewer approved only:

```text
SOURCE_INTAKE.md
IMPLEMENTATION_BLUEPRINT.md
DEV_CONTEXT.md
MEMORY_TIER.md
```

and deferred:

```text
SCHEMA.md
REVIEW_QUEUE.md
templates/architecture-review-window-prompt.md
```

## Minimal Documentation Patch Finding

The approved four-file patch passed:

```text
minimal doc patch status: pass
error count: 0
```

Changed core docs:

```text
DEV_CONTEXT.md
IMPLEMENTATION_BLUEPRINT.md
MEMORY_TIER.md
SOURCE_INTAKE.md
```

The patch records Phase B as documentation-only:

```text
read-only derived retrieval adapter
not runtime/default/production adoption
graph/retrieval metadata is not reviewed relation or support
retrieval receipts are not action basis
retrieval activation is not truth
no Skills / MCP writes / subagents / formal writeback
```

Decision:

```text
Keep the minimal documentation-only patch.
Do not expand beyond the four approved files without a new review gate.
```

## Runtime / Full-Stack Feasibility Finding

Current Yuxi HEAD remains:

```text
a8536a2e8520d1992a31bb6c22f219e60deca131
```

Local runtime check:

```text
Docker: unavailable
Docker Compose: unavailable
uv-managed Python 3.12: available
default python: 3.10.6
node / pnpm: available
```

Yuxi runtime path:

```text
official quick start requires Docker and Docker Compose
Lite mode still calls docker compose
documented unit/integration/e2e tests use docker compose exec api
```

Runtime feasibility validator passed:

```text
runtime feasibility status: pass
error count: 0
```

Decision:

```text
Do not run partial host-only smoke as evidence of original Yuxi runtime value.
Original Yuxi full-stack remains unvalidated locally until Docker/Compose or a remote runner is available.
Keep the four-file documentation patch as the current positive mainline state.
```

## Context-Pack Candidate Finding

The context-pack candidate builder produced:

```text
pack count: 90
action_basis_allowed_count: 0
packs with suppressed receipt action flags: 36
```

The validator passed:

```text
context pack status: pass
error count: 0
```

Compared against runtime feasibility, this step preserved:

```text
runtime feasibility: pass / 0 errors
minimal doc patch: pass / 0 errors
contract: pass / 0 errors
approved four-file doc patch only
no original Yuxi runtime claim
```

Decision:

```text
Keep context-pack candidate assembly as an adapter-level sandbox candidate.
Generated packs are not action basis.
Next adapter-level step may test evidence-envelope / warrant draft assembly.
```

## Evidence-Envelope Candidate Finding

The evidence-envelope builder produced:

```text
envelope count: 90
action_basis_allowed_count: 0
evidence_packet_allowed_count: 0
evidence_sufficiency_passed_count: 0
envelopes with suppressed receipt action flags: 36
```

The validator passed:

```text
evidence envelope status: pass
error count: 0
```

Compared against context-pack candidate assembly, this step added:

```text
warrant draft
support-looking source anchors marked as candidate review input
challenge / scope candidates
required next gates
```

It preserved:

```text
context pack: pass / 0 errors
runtime feasibility: pass / 0 errors
minimal doc patch: pass / 0 errors
contract: pass / 0 errors
approved four-file doc patch only
no original Yuxi runtime claim
```

Important finding:

```text
Phase B can move from retrieval receipt -> context-pack candidate ->
evidence-envelope candidate without granting action basis or evidence authority.
```

Decision:

```text
Keep evidence-envelope / warrant-draft assembly as an adapter-level sandbox candidate.
Generated envelopes are not Evidence Packets, evidence support, sufficiency passes, or action basis.
Next adapter-level step may test an Evidence Support Check sandbox.
```

## Evidence Support Check Candidate Finding

The support-check builder produced:

```text
support check count: 90
evidence item count: 389
source_span_available_count: 389
current_source_hash_match_count: 321
source_refresh_needed_count: 68
blocked_no_source_anchor_count: 2
support_passed_count: 0
support_counts_for_promotion_count: 0
action_basis_allowed_count: 0
```

The validator passed:

```text
evidence support check status: pass
error count: 0
```

Compared against evidence-envelope assembly, this step added:

```text
actual source-span snapshots
current source hash verification
per-item evidence_support placeholders
explicit blocked_no_source_anchor cases
```

It preserved:

```text
evidence envelope: pass / 0 errors
context pack: pass / 0 errors
runtime feasibility: pass / 0 errors
minimal doc patch: pass / 0 errors
contract: pass / 0 errors
approved four-file doc patch only
no original Yuxi runtime claim
```

Important finding:

```text
Phase B can prepare Evidence Support Check work from retrieval output while
still refusing to assert semantic support. It also surfaces stale-source risk:
68 extracted spans need source refresh before any support review can rely on
the indexed receipt hash.
```

Decision:

```text
Keep Evidence Support Check candidate assembly as an adapter-level sandbox candidate.
Generated checks are not reviewed support, Evidence Packets, sufficiency passes, or action basis.
Next adapter-level step may test source-refresh / reindex behavior.
```

## Source Refresh Candidate Finding

The source-refresh builder produced:

```text
source refresh count: 90
refresh item count: 389
source_span_available_count: 389
pre_refresh_mismatch_count: 68
post_refresh_mismatch_count: 0
refreshed_item_count: 68
already_current_item_count: 321
blocked_no_source_anchor_count: 2
support_passed_count: 0
action_basis_allowed_count: 0
```

The validator passed:

```text
source refresh status: pass
error count: 0
```

Compared against Evidence Support Check candidate assembly, this step added:

```text
source hash refresh
source span refresh
post-refresh mismatch validation
refresh status per evidence item
```

It preserved:

```text
evidence support check: pass / 0 errors
evidence envelope: pass / 0 errors
context pack: pass / 0 errors
runtime feasibility: pass / 0 errors
minimal doc patch: pass / 0 errors
contract: pass / 0 errors
approved four-file doc patch only
no original Yuxi runtime claim
```

Important finding:

```text
Phase B can refresh stale source-span/hash snapshots before support review:
68 pre-refresh mismatches dropped to 0 post-refresh mismatches.
This improves freshness hygiene, not truth authority.
```

Decision:

```text
Keep source-refresh assembly as an adapter-level sandbox candidate.
Refreshed hashes/spans are not semantic support, Evidence Packets, sufficiency passes, or action basis.
Next adapter-level step may test refreshed support-check rebuild / delta behavior.
```

## Refreshed Support Check Candidate Finding

The refreshed support-check builder produced:

```text
refreshed support check count: 90
evidence item count: 389
source_span_available_count: 389
previous_source_refresh_needed_count: 68
current_source_refresh_needed_count: 0
current_source_hash_match_count: 389
refreshed_item_count: 68
already_current_item_count: 321
blocked_no_source_anchor_count: 2
support_passed_count: 0
action_basis_allowed_count: 0
```

The validator passed:

```text
refreshed support check status: pass
error count: 0
```

Compared against the original Evidence Support Check candidate assembly and the
source-refresh assembly, this step added:

```text
rebuilt support-check view with refreshed source spans/hashes
refresh-needed delta validation
clean current hash match count for review-facing evidence items
```

It preserved:

```text
source refresh: pass / 0 errors
evidence support check: pass / 0 errors
evidence envelope: pass / 0 errors
context pack: pass / 0 errors
runtime feasibility: pass / 0 errors
minimal doc patch: pass / 0 errors
contract: pass / 0 errors
approved four-file doc patch only
no original Yuxi runtime claim
```

Important finding:

```text
The refreshed support-check view keeps the freshness improvement where the
reviewer will actually use it: source_refresh_needed dropped from 68 to 0 and
current_source_hash_match_count rose to 389 / 389.
```

Decision:

```text
Keep refreshed support-check rebuild as an adapter-level sandbox candidate.
Generated checks are not reviewed support, Evidence Packets, sufficiency passes, or action basis.
Next adapter-level step may test manual-review packet / reviewer queue behavior.
```

## Review Queue Packet Finding

The review-queue packet builder produced:

```text
review packet count: 90
open packet count: 88
blocked_no_source_anchor_count: 2
review item count: 389
source_span_available_count: 389
current_source_hash_match_count: 389
current_source_refresh_needed_count: 0
review_result_not_reviewed_count: 90
support_passed_count: 0
action_basis_allowed_count: 0
automatic_promotion_allowed_count: 0
```

The validator passed:

```text
review queue packet status: pass
error count: 0
```

Compared against refreshed support-check assembly, this step added:

```text
review queue packet shape
manual evidence_support review route
per-item allowed review outcomes
approval integrity left unchecked
open vs blocked queue state
```

It preserved:

```text
refreshed support check: pass / 0 errors
source refresh: pass / 0 errors
evidence support check: pass / 0 errors
evidence envelope: pass / 0 errors
context pack: pass / 0 errors
runtime feasibility: pass / 0 errors
minimal doc patch: pass / 0 errors
contract: pass / 0 errors
approved four-file doc patch only
no original Yuxi runtime claim
```

Important finding:

```text
Phase B can hand clean source-span material to the VAKS review queue without
becoming the reviewer: 88 packets are open for manual evidence_support review,
2 no-anchor packets stay blocked/parked, and 90 / 90 packets remain not_reviewed.
```

Decision:

```text
Keep review queue packet assembly as an adapter-level sandbox candidate.
Generated packets are not reviewed support, Evidence Packets, sufficiency passes, promotion approval, or action basis.
Next adapter-level step may test simulated reviewer outcome behavior.
```

## Simulated Reviewer Outcome Finding

The simulated-outcome builder produced:

```text
outcome record count: 90
previous_review_result_not_reviewed_count: 90
simulated_packet_count: 12
not_reviewed_packet_count: 76
blocked_no_source_anchor_count: 2
simulated_item_outcome_count: 57
simulated_direct_support_count: 12
simulated_inferential_support_count: 12
simulated_background_count: 23
simulated_counterexample_count: 10
human_reviewed_support_count: 0
support_passed_count: 0
action_basis_allowed_count: 0
automatic_promotion_allowed_count: 0
formal_writeback_allowed_count: 0
```

The validator passed:

```text
simulated reviewer outcome status: pass
error count: 0
```

Compared against review queue packet assembly, this step added:

```text
simulation-only reviewer outcomes
simulated evidence_support metadata
support-like and challenge-like item outcomes
explicit approval-integrity non-approval boundary
```

It preserved:

```text
review queue packet: pass / 0 errors
refreshed support check: pass / 0 errors
source refresh: pass / 0 errors
evidence support check: pass / 0 errors
evidence envelope: pass / 0 errors
context pack: pass / 0 errors
runtime feasibility: pass / 0 errors
minimal doc patch: pass / 0 errors
contract: pass / 0 errors
approved four-file doc patch only
no original Yuxi runtime claim
```

Important finding:

```text
Phase B can test reviewer-outcome shapes without treating simulated support as
human-reviewed support. 24 support-like simulated item outcomes were recorded,
but 0 counted as promotion support, Evidence Packet, writeback, or action basis.
```

Decision:

```text
Keep simulated reviewer outcome assembly as an adapter-level sandbox candidate.
Generated outcomes are not human review, reviewed support, Evidence Packets, sufficiency passes, promotion approval, formal writeback, or action basis.
Next adapter-level step may test promotion-gate / sufficiency-block behavior.
```

## Promotion Gate Finding

The promotion-gate builder produced:

```text
gate record count: 90
blocked gate count: 90
simulated support-like count: 24
blocked_due_simulation_only_count: 12
blocked_due_support_like_not_human_reviewed_count: 12
blocked_due_missing_source_anchor_count: 2
human_reviewed_support_count: 0
reviewed_support_count: 0
promotion_support_count: 0
promotion_allowed_count: 0
action_basis_allowed_count: 0
action_ready_count: 0
evidence_packet_created_count: 0
evidence_sufficiency_passed_count: 0
formal_writeback_allowed_count: 0
truth_confidence_change_allowed_count: 0
reviewed_relation_creation_allowed_count: 0
```

The validator passed:

```text
promotion gate status: pass
error count: 0
```

Compared against simulated reviewer outcome assembly, this step added:

```text
promotion gate evaluation
action-basis gate evaluation
sufficiency block state
explicit blockers for simulation-only support-like metadata
```

It preserved:

```text
simulated reviewer outcome: pass / 0 errors
review queue packet: pass / 0 errors
refreshed support check: pass / 0 errors
source refresh: pass / 0 errors
evidence support check: pass / 0 errors
evidence envelope: pass / 0 errors
context pack: pass / 0 errors
runtime feasibility: pass / 0 errors
minimal doc patch: pass / 0 errors
contract: pass / 0 errors
approved four-file doc patch only
no original Yuxi runtime claim
```

Important finding:

```text
Phase B can carry support-like metadata all the way to a promotion/action gate
and still block it: 24 support-like simulated item outcomes were visible, but
90 / 90 gate records were blocked and no promotion, writeback, relation,
truth-confidence change, sufficiency pass, or action basis was created.
```

Decision:

```text
Keep promotion-gate / sufficiency-block evaluation as an adapter-level sandbox candidate.
Generated gates are not promotion approvals, Evidence Packets, sufficiency passes, formal writeback, reviewed relations, truth changes, or action basis.
Next adapter-level step may synthesize the Phase B keep/stop evidence packet.
```

## Keep / Stop Synthesis Finding

The keep/stop synthesis produced:

```text
keep_stop_decision: keep_phase_b_as_sandbox_candidate
positive_value_confirmed: true
no_boundary_leak_confirmed: true
mainline_status: documentation_only_patch_validated_not_committed
runtime_status: original_yuxi_full_stack_unvalidated_docker_unavailable
promotion_allowed_count: 0
action_basis_allowed_count: 0
evidence_sufficiency_passed_count: 0
formal_writeback_allowed: false
original_yuxi_runtime_validated: false
runtime_adoption_allowed: false
c_lite_allowed: false
```

The validator passed:

```text
keep stop synthesis status: pass
error count: 0
```

Compared against promotion-gate / sufficiency-block, this step added:

```text
whole-chain keep/stop judgment
retrieval value + governance safety in one decision
explicit stop list for runtime, C-lite, writeback, and action basis
```

It preserved:

```text
promotion gate: pass / 0 errors
simulated reviewer outcome: pass / 0 errors
review queue packet: pass / 0 errors
refreshed support check: pass / 0 errors
source refresh: pass / 0 errors
evidence support check: pass / 0 errors
evidence envelope: pass / 0 errors
context pack: pass / 0 errors
runtime feasibility: pass / 0 errors
minimal doc patch: pass / 0 errors
contract: pass / 0 errors
approved four-file doc patch only
no original Yuxi runtime claim
```

Important finding:

```text
Local proxy evidence suggests Phase B is positive for VAKS as a governed
retrieval-adapter sandbox: main and holdout retrieval improved or tied where
required inside this harness, yuxi_native_profile governance leakage stayed
visible under the proxy metric, and the VAKS wrapper kept action leakage /
promotion / writeback / truth-change / reviewed-relation permissions at zero.
This does not validate original Yuxi runtime or external relevance quality.
```

Decision:

```text
Keep Phase B as a sandbox and documentation candidate only.
Next safe step is a user-approved commit of the validated four-file documentation patch, or original Yuxi full-stack testing after Docker/remote runner is available.
Do not start C-lite or runtime adoption from this packet alone.
```

## Commit-Readiness Finding

The commit-readiness packet produced:

```text
commit_readiness_status: ready_pending_user_approval
commit_without_user_approval_allowed: false
recommended mainline docs:
  SOURCE_INTAKE.md
  IMPLEMENTATION_BLUEPRINT.md
  DEV_CONTEXT.md
  MEMORY_TIER.md
recommended sandbox evidence bundle:
  outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/
excluded files:
  SCHEMA.md
  REVIEW_QUEUE.md
  templates/architecture-review-window-prompt.md
```

The validator passed:

```text
commit readiness check status: pass
error count: 0
```

Compared against keep/stop synthesis, this step added:

```text
exact commit scope recommendation
explicit no-approval/no-commit boundary
deferred-file and runtime/C-lite stop list
```

It preserved:

```text
keep stop synthesis: pass / 0 errors
minimal doc patch: pass / 0 errors
promotion gate: pass / 0 errors
adapter contract: pass / 0 errors
runtime feasibility: pass / 0 errors
no staged paths
no commit
```

Decision:

```text
Phase B is ready for a user-approved sandbox evidence-package commit, not a
core-doc conclusion commit or stronger architecture adoption.
This is not commit approval, runtime adoption, C-lite approval, original Yuxi runtime validation, formal writeback, reviewed truth, or action basis.
```

## Next-Action Gate Finding

The next-action gate produced:

```text
next_action_gate_status: pass
recommended_next_action: await_user_approved_commit_or_runner_choice
commit_path: ready_pending_user_approval
commit_without_user_approval_allowed: false
original_yuxi_runtime_path: blocked_until_docker_or_remote_runner
original_yuxi_runtime_validated: false
c_lite_path: not_allowed_from_current_evidence
c_lite_allowed: false
runtime_adoption_path: not_allowed
runtime_adoption_allowed: false
```

The validator passed:

```text
next action gate check status: pass
error count: 0
```

Compared against commit-readiness, this step added:

```text
branch choice gate
commit vs runtime vs C-lite separation
explicit external-condition and user-approval requirements
```

It preserved:

```text
commit-readiness: pass / 0 errors
keep-stop: pass / 0 errors
minimal doc patch: pass / 0 errors
promotion gate: pass / 0 errors
adapter contract: pass / 0 errors
runtime feasibility: pass / 0 errors
no staged paths
no commit
```

Decision:

```text
The next action is gated, not automatic.
The best available branch is a user-approved commit of the validated documentation/evidence bundle.
Original Yuxi runtime testing remains blocked until Docker/Compose or a remote runner exists.
C-lite and runtime adoption remain not allowed from current evidence.
```

## Pre-Commit Manifest Finding

The pre-commit manifest produced:

```text
pre_commit_manifest_status: ready_pending_user_approval
file_count: 166
commit_without_user_approval_allowed: false
stage_performed: false
commit_performed: false
```

The validator passed:

```text
pre commit manifest check status: pass
error count: 0
```

Compared against next-action gate, this step added:

```text
file-level manifest
sha256 fingerprints
pre-commit scope evidence
```

It preserved:

```text
next-action gate: pass / 0 errors
commit-readiness: pass / 0 errors
keep-stop: pass / 0 errors
no staged paths
no commit
runtime_adoption_allowed: false
c_lite_allowed: false
```

Decision:

```text
The proposed Phase B commit scope now has file-level hash evidence.
This is still not approval to stage or commit.
```

## Branch-Decision Brief Finding

The branch-decision brief produced:

```text
branch_decision_brief_status: ready_for_user_choice
recommended_branch: user_approved_commit
commit_without_user_approval_allowed: false
stage_performed: false
commit_performed: false
user-approved commit: ready_pending_user_approval
original Yuxi full-stack test: blocked_until_docker_or_remote_runner
C-lite sandbox: not_allowed_without_new_user_gate
runtime adoption: not_allowed
```

The validator passed:

```text
branch decision brief check status: pass
error count: 0
```

Compared against pre-commit manifest, this step added:

```text
human-readable branch choice brief
copy-paste recovery prompt
no new authority
```

It preserved:

```text
pre-commit manifest: pass / 0 errors
next-action gate: pass / 0 errors
commit-readiness: pass / 0 errors
keep-stop: pass / 0 errors
no staged paths
no commit
runtime_adoption_allowed: false
c_lite_allowed: false
```

Decision:

```text
The branch decision is now summarized for the user or next window.
This is not approval to stage, commit, start C-lite, or claim runtime adoption.
```

## P0/P1 Supplemental Pressure Finding

After Pro's critique, the sandbox was strengthened with P0/P1补测.

New P0 evidence:

```text
P0 query-level replay check: pass / 0 errors
replay rows: 7200
query metric rows: 720
summary rows: 32
clean VAKS-only lexical control: included
metric dictionary: included
```

Important correction:

```text
The old package had summary-only evidence and an ambiguous stale denominator.
The P0 replay now separates top20 paired query outcomes from top10 replay/governance checks.
The P0 summary includes holdout_stale in stale_detection_rate.
```

New P1 fresh adversarial evidence:

```text
query count: 30
resolvable: 30/30 primary, 30/30 full
P1 adversarial audit check: pass / 0 errors
criteria passed: 10/10
```

Key adversarial comparison:

```text
primary:
  baseline_file_lexical: hit@5 15/30, MRR 0.3861, leakage 1.0000
  clean VAKS-only:       hit@5 26/30, MRR 0.7537, leakage 0.0000
  skeleton:              hit@5 28/30, MRR 0.8556, leakage 0.0000
  Yuxi proxy:            hit@5 28/30, MRR 0.8167, leakage 1.0000

full:
  baseline_file_lexical: hit@5 17/30, MRR 0.4933, leakage 1.0000
  clean VAKS-only:       hit@5 26/30, MRR 0.7211, leakage 0.0000
  skeleton:              hit@5 28/30, MRR 0.8611, leakage 0.0000
  Yuxi proxy:            hit@5 27/30, MRR 0.8028, leakage 1.0000
```

Interpretation:

```text
VAKS contribution is materially visible: clean VAKS-only keeps leakage at 0.
Yuxi-like retrieval contribution is also visible: skeleton beats clean VAKS-only on hit@5/MRR.
The combination is positive in this local sandbox: skeleton keeps VAKS boundary behavior while recovering stronger retrieval.
The retrieval advantage over yuxi_native_profile is directional local evidence, not decisive proof of retrieval superiority.
The action_leakage_rate is a ranking/governance proxy, not an answer-level safety verdict or original Yuxi runtime verdict.
```

Promotion gate calibration:

```text
promotion gate calibration check: pass / 0 errors
positive cases: 12
negative cases: 12
TPR: 1.0000
FPR: 0.0000
auto promotion/writeback/relation mutation: 0
```

Remaining hard boundary:

```text
Original Yuxi runtime was not run.
Docker and Docker Compose are unavailable in this environment.
The P1 adversarial set is fresh/local, not externally blind.
C-lite, runtime adoption, writeback adoption, and mainline strong conclusions remain not allowed.
```

## Supplemental Pro Package Finding

A Pro-facing supplemental package was created for reverse audit:

```text
directory: pro-review-supplemental-package/
zip: vaks-yuxi-phase-b-p0-p1-supplemental-pro-review-package.zip
file_count: 42
zip_bytes: 1324533
package_check: pass / 0 errors
```

The package includes:

```text
P0 query-level replay report/check
P1 fresh adversarial report/check
P1 promotion gate calibration report/check
metric dictionary
original Yuxi runtime feasibility blocker
query files
CSV/JSON result tables
validation scripts
non-leading Pro supplemental review prompt
```

Decision:

```text
This package is ready for Pro review.
It is not a mainline adoption decision, not C-lite approval, and not original Yuxi runtime validation.
```

## Agent-Blind Adversarial Finding

An independent sub-agent generated a separate 30-query adversarial set without parent context and without reading existing Phase B query/results/report files.

Result:

```text
agent blind audit check: pass / 0 errors
criteria passed: 10/10
query count: 30
```

Key comparison:

```text
primary:
  baseline_file_lexical: hit@5 20/30, MRR 0.4311, leakage 1.0000
  clean VAKS-only:       hit@5 23/30, MRR 0.6245, leakage 0.0000
  bucket_local:          hit@5 28/30, MRR 0.8478, leakage 0.0000
  skeleton:              hit@5 30/30, MRR 0.9250, leakage 0.0000
  Yuxi proxy:            hit@5 27/30, MRR 0.8339, leakage 1.0000

full:
  baseline_file_lexical: hit@5 16/30, MRR 0.4368, leakage 1.0000
  clean VAKS-only:       hit@5 21/30, MRR 0.5698, leakage 0.0000
  bucket_local:          hit@5 28/30, MRR 0.7940, leakage 0.0000
  skeleton:              hit@5 30/30, MRR 0.9278, leakage 0.0000
  Yuxi proxy:            hit@5 26/30, MRR 0.8229, leakage 1.0000
```

Interpretation:

```text
This strengthens the combination-effect claim beyond the locally authored fresh adversarial set.
The result is still sandbox evidence.
It does not validate original Yuxi runtime or approve C-lite/runtime/writeback.
It also does not prove original Yuxi would produce unsafe answers; the measured leakage is a proxy-harness governance signal.
```

## P0 Reproducibility Hardening Finding

Pro's second review said the P0 evidence was much better than summary-only, but still had two practical audit gaps:

```text
no frozen corpus manifest / file-hash snapshot
top11-20 item-level candidates were not visible, even when first_hit_rank was 11-20
```

Both gaps are now addressed for the existing P0 main/holdout set.

Frozen corpus:

```text
check: pass / 0 errors
primary files: 409
full files: 4384
artifacts:
  PHASE_B_FROZEN_CORPUS_MANIFEST.md
  PHASE_B_FROZEN_CORPUS_MANIFEST_CHECK.md
  results/phase_b_frozen_corpus_manifest.json
  results/phase_b_frozen_corpus_manifest.csv
```

Top11-20 receipts:

```text
check: pass / 0 errors
receipt rows: 7200
query sets: main + holdout_used
corpora: primary + full
modes: 8
artifacts:
  PHASE_B_TOP11_20_ITEM_RECEIPTS_REPORT.md
  PHASE_B_TOP11_20_ITEM_RECEIPTS_CHECK.md
  results/phase_b_top11_20_item_receipts.csv
  results/phase_b_top11_20_item_receipts_summary.json
```

Interpretation:

```text
This moves P0 from query-level paired outcomes + top10 governance replay toward a more auditable top20 replay.
It does not change the conclusion level.
Phase B remains a sandbox candidate, not C-lite/runtime/core-doc strong conclusion evidence.
```

## External Validation / Answer-Loop Gate Finding

Two next-step specs were added:

```text
PHASE_B_EXTERNAL_VALIDATION_NEXT_STEPS.md
PHASE_B_READ_ONLY_ANSWER_LOOP_PILOT_SPEC.md
```

Validator:

```text
PHASE_B_NEXT_STEP_SPECS_CHECK.md
status: pass / 0 errors
```

These specs separate the next three decisions:

```text
external blind query set
original Yuxi read-only rerun
read-only answer/tool loop pilot before any C-lite discussion
```

Hard boundary:

```text
The specs are future gates, not evidence that those gates have passed.
They do not approve original Yuxi runtime, C-lite, writeback, or action-basis use.
```

## P0 Frozen Rerun V2 Finding

Pro identified a stronger P0 requirement:

```text
one run_id
one frozen corpus/query/script identity
top20 item-level export
top1-10 replay
top11-20 receipts
query metrics
summary
exact consistency validator from top20 rows
```

This has now been implemented.

Result:

```text
run_id: phase_b_frozen_rerun_v2_20260611T142435Z
check: pass / 0 errors
top20 item rows: 14400
query metric rows: 720
summary rows: 32
```

Artifacts:

```text
PHASE_B_FROZEN_RERUN_V2_REPORT.md
PHASE_B_FROZEN_RERUN_V2_CHECK.md
results/phase_b_frozen_rerun_v2_manifest.json
results/phase_b_frozen_rerun_v2_top20_items.csv
results/phase_b_frozen_rerun_v2_query_metrics.csv
results/phase_b_frozen_rerun_v2_summary.csv
tools/build_phase_b_frozen_rerun_v2.py
tools/validate_phase_b_frozen_rerun_v2.py
```

Interpretation:

```text
The prior exact-run-alignment critique is addressed for P0 local proxy evidence.
The remaining blockers are different now: no human relevance judgment, no external blind set, and no original Yuxi read-only runtime rerun.
```

## Blind Relevance Packet Finding

The second Pro-requested lane was started:

```text
blind/internal no-parent-context query set
top5 relevance judgment packet
separate from expected_terms
```

Result:

```text
query_count: 18
top20 item rows: 2880
judgment packet rows: 720
check: pending_judgment / 0 errors
```

Artifacts:

```text
queries_phase_b_blind_relevance.jsonl
PHASE_B_BLIND_RELEVANCE_PILOT_REPORT.md
PHASE_B_BLIND_RELEVANCE_CHECK.md
PHASE_B_BLIND_RELEVANCE_JUDGMENT_INSTRUCTIONS.md
results/phase_b_blind_relevance_top20_items.csv
results/phase_b_blind_relevance_judgment_packet.csv
tools/build_phase_b_blind_relevance_pilot.py
tools/validate_phase_b_blind_relevance_pilot.py
```

Interpretation:

```text
The judgment packet is ready for Pro/external/human grading.
The relevance judgment itself is not yet complete and must not be claimed.
```

## Internal Relevance Judgment Finding

The blind relevance packet was filled with an internal heuristic/model-assisted judge:

```text
judge_id: codex_internal_heuristic_judge_v1
judgment rows: 720
grade_2_relevant: 192
grade_1_borderline: 343
grade_0_not_relevant: 185
check: pass / 0 errors
```

Judged retrieval signal:

```text
primary:
  baseline_file_lexical: hit@5 2/18, MRR@5 0.0324, nDCG@5 0.6078
  clean VAKS-only:       hit@5 10/18, MRR@5 0.3935, nDCG@5 0.9024
  skeleton:              hit@5 11/18, MRR@5 0.5741, nDCG@5 0.9554
  Yuxi proxy:            hit@5 13/18, MRR@5 0.5481, nDCG@5 0.9044

full:
  baseline_file_lexical: hit@5 3/18, MRR@5 0.1667, nDCG@5 0.7537
  clean VAKS-only:       hit@5 11/18, MRR@5 0.3889, nDCG@5 0.8607
  skeleton:              hit@5 13/18, MRR@5 0.6250, nDCG@5 0.9186
  Yuxi proxy:            hit@5 11/18, MRR@5 0.5185, nDCG@5 0.9513
```

Interpretation:

```text
The internal judged relevance signal supports retrieval lift over baseline and clean VAKS-only.
It also shows Yuxi proxy remains competitive on relevance-only metrics.
This strengthens sandbox evidence but cannot replace external human/Pro relevance judgment.
```

## External Relevance Double-Judge Kit Finding

Pro's latest reverse audit lowered the local attribution claim:

```text
VAKS contribution: 中
Yuxi-like contribution: 大
most important remaining blocker:
  same frozen corpus original Yuxi read-only rerun
  external/manual relevance judgment
```

The next P0 is no longer another internal metric table. It is external/manual
judgment over the existing blind relevance top5 packet.

Implemented kit:

```text
template: results/phase_b_blind_relevance_external_judgment_template.csv
rows: 720
requires: Judge A + Judge B + per-row arbitration
check: pending_external_judgment / 0 errors
```

Important finding:

```text
The workflow is now ready for external double-judgment, but the external
judgment itself is not complete. This prevents the internal heuristic
judgment from being silently promoted into stronger evidence.
```

Decision:

```text
Keep Phase B as a sandbox candidate.
Do not use internal judged relevance as external validation.
Do not enter C-lite or claim original Yuxi runtime validation.
Next evidence step is to fill and validate the external judgment file, or run
original Yuxi read-only on a Docker/remote runner.
```

## External Blind Query Set Kit Finding

Pro's minimum-test list also asks for a small external blind query set:

```text
target count: 15-20
author: external human or at least different model family
author restriction: no access to existing Phase B queries/results/reports
allowed source access: VAKS core docs and high-level architecture docs only
```

Implemented kit:

```text
template: queries_phase_b_external_blind_template.jsonl
template rows: 20
filled file expected: queries_phase_b_external_blind.jsonl
check: pending_external_queries / 0 errors
```

Important finding:

```text
The workflow is now ready for external blind query generation, but the
external query set itself is not complete. This prevents agent_blind or fresh
adversarial internal sets from being silently promoted into external blind
evidence.
```

Decision:

```text
Keep the kit as the next external-validation scaffold.
Do not count it as external blind evidence until an external author fills and
the validator accepts `queries_phase_b_external_blind.jsonl`.
Do not enter C-lite or claim original Yuxi runtime validation.
```

## External Kit Revise Finding

Pro's audit marked both external kits as:

```text
external relevance judgment kit: revise
external blind query set kit: revise
```

The relevance kit issue was insufficient blinding:

```text
old judge-facing template leaked mode and original judgment_id
new judge-facing template uses opaque row_id + system_slot
new mapping file is post-judgment only
```

The external blind query issue was missing provenance and premature expected
terms:

```text
old query template asked external authors to write expected_terms
new query template removes expected_terms
new author manifest captures author_type/model_family, allowed docs seen, and
no-access attestations
```

Current status after revision:

```text
external relevance judgment kit: pending_external_judgment / 0 errors
external blind query set kit: pending_external_queries / 0 errors
```

Decision:

```text
The kits have moved from revise-needed to revised-template-ready.
They still do not count as completed external validation until the external
judgments and external queries are actually filled and validated.
```

## Overclaim Wording Tightening Finding

Pro flagged three wording risks and one method-risk footnote.

Tightened:

```text
blind relevance judgment status:
  complete -> complete_internal_only

answer-loop pilot:
  C-lite前夜 test -> pre-C-lite sandbox pilot concept, not a C-lite readiness claim

Frozen Rerun v2:
  replaces patched-together story -> authoritative exact-run local P0 bundle going forward;
  older P0 summaries remain historical artifacts

internal heuristic judge:
  explicitly described as query-profile/bucket-prior diagnostic, not human substitute or gold standard
```

Decision:

```text
These changes reduce accidental promotion of internal/proxy evidence.
They do not add new external evidence and do not change the core verdict:
Phase B remains sandbox candidate only.
```
