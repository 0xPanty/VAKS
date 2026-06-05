---
type: candidate_patch_pressure_test
status: candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
version_under_test: v0.2.13 revised candidate
patch_under_test: v0-2-13-make-action-support-visible
test_method: manual_adversarial_pressure_test
source_basis:
  - outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-revised-candidate-patch.md
  - outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-revised-test.md
  - outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
  - outputs/review/candidate_pattern_bank/source-structure-first-rag.md
  - outputs/review/project_borrowing_ledgers/VAKS.md
  - outputs/review/2026-06-05-v0-2-12-intake-trial-scsc-tools.md
truth_boundary: pressure test output only, not reviewed knowledge
write_scope: outputs/review only
---

# v0.2.13 Revised Pressure Test Suite

## 说人话结论

这轮不是再做漂亮的概念测试，而是故意找茬。

我用三类压力压 v0.2.13 revised：

```text
1. 触发边界：它会不会把普通 intake / routing 拖重？
2. 支持质量：它会不会被空 warrant、循环 warrant、scope jump、伪独立支持骗过？
3. 真实候选材料：它会不会把 active pattern、ledger adapt、tool catalogue 误读成主线依据？
```

结论：

```text
No blocking design failure found.
Keep as v0.2.13 revised candidate.
Do not promote to mainline yet.
Do not create candidate pattern file.
```

我现在挑不出“规则方向本身”的硬伤。剩下的不是概念 bug，而是验证边界：

```text
还需要拿真实 action-basis 写作场景跑一次，看它是否真的省误判且不烦人。
```

## Rule Under Test

Current revised candidate rule:

```text
For action_basis and significant promotion/decision use, when an answer or claim
will be relied on for action or risk-sensitive judgment, make the support visible:
state the action-facing claim, the point-specific anchored evidence, the non-circular
warrant connecting that evidence to the claim, the relevant scope/assumptions,
the known challenges or gaps, and the current residual review status.
Diagrams, notation, source counts, tool counts, vendor pages, and confidence labels
do not increase support, independence, or action readiness.
```

Short form:

```text
Evidence is not enough; show the non-circular warrant.
```

## Acceptance Bar

The rule can stay candidate only if it passes all of these:

| Dimension | Must Do |
| --- | --- |
| Trigger precision | Trigger only for action / promotion / decision / risk-sensitive use |
| Ordinary-work restraint | Not burden ordinary intake, source routing, search, or summaries |
| Warrant quality | Catch blank, circular, non-explanatory, and scope-jumping warrants |
| Evidence anchoring | Reject bare URLs, background citations, and vague source lists as support |
| Source-family restraint | Not count same-family repetition as independent support |
| Non-support exclusion | Reject tool/vendor/diagram/source-count/confidence-label support smuggling |
| Candidate boundary | Not turn active pattern, ledger disposition, or test PASS into reviewed truth |
| Promotion discipline | Not create pattern or mainline patch from this test alone |

## Summary Matrix

| ID | Test Class | Scenario | Expected | Result |
| --- | --- | --- | --- | --- |
| A1 | Trigger | Ordinary SCSC Tools source routing | No trigger | PASS |
| A2 | Trigger | "Is this enough?" for reading context only | No trigger | PASS |
| A3 | Trigger | "Is this enough?" for action decision | Trigger | PASS |
| A4 | Trigger | Draft relation mention, not promotion/action | No trigger | PASS |
| A5 | Trigger | Action-critical relation judgment | Trigger | PASS |
| B1 | Warrant | Blank warrant | Block/degrade | PASS |
| B2 | Warrant | Circular warrant | Block/degrade | PASS |
| B3 | Warrant | Scope jump | Block/degrade | PASS |
| B4 | Warrant | Evidence mismatch | Block/degrade | PASS |
| B5 | Warrant | Good scoped warrant | Candidate review can proceed | PASS |
| C1 | Evidence | Bare URL as support | Block/degrade | PASS |
| C2 | Evidence | Background citation as support | Block/degrade | PASS |
| C3 | Evidence | Same source family counted as independent | Block independence claim | PASS |
| C4 | Evidence | Tool/vendor/diagram as support | Exclude as non-support | PASS |
| C5 | Evidence | Active candidate pattern as reviewed truth | Block promotion | PASS |
| D1 | Real material | `retrieval-is-activation-not-truth` as action-facing rule candidate | Proceed candidate-only; no mainline | PASS |
| D2 | Real material | `source-structure-first-rag` used to change templates now | Block; required gates missing | PASS |
| D3 | Real material | VAKS ledger `adapt` treated as ADR/action basis | Block | PASS |
| D4 | Real material | SCSC Tools used for assurance-tool adoption | Block | PASS |
| D5 | Real material | SCSC Tools ordinary intake | No trigger | PASS |
| E1 | Regression | Claims ordinary intake is proven unaffected | Block overclaim | PASS |
| E2 | Regression | Creates candidate pattern from v0.2.13 | Block | PASS |
| E3 | Regression | Promotes sentence to mainline without real example | Block | PASS |

## A. Trigger Boundary Tests

### A1: Ordinary SCSC Tools Source Routing

Input:

```text
SCSC Tools source arrives.
Need only lightweight source record, candidate comprehension, and source routing overlay.
No action, promotion, decision, or risk-sensitive answer is being made.
```

Expected:

```text
trigger_make_support_visible: no
reason: ordinary source routing
```

Observed:

```text
The rule does not trigger.
Existing v0.2.12 SCSC Tools trial remains sufficient.
```

Result: PASS.

### A2: "Is This Enough?" For Reading Context Only

Input:

```text
Reviewer asks: Is this enough context to keep reading the source?
```

Expected:

```text
trigger_make_support_visible: no
reason: not action/promotion/decision/risk-sensitive
```

Result: PASS.

### A3: "Is This Enough?" For Action Decision

Input:

```text
Reviewer asks: Is this enough evidence to use this claim in an action basis?
```

Expected:

```text
trigger_make_support_visible: yes
reason: enough means enough for action-basis use
```

Result: PASS.

### A4: Draft Relation Mention

Input:

```text
A candidate note says retrieval and activation are related.
No relation promotion and no action use.
```

Expected:

```text
trigger_make_support_visible: no
```

Result: PASS.

### A5: Action-Critical Relation Judgment

Input:

```text
VAKS wants to rely on "retrieval result supports claim" as an action-critical relation.
```

Expected:

```text
trigger_make_support_visible: yes
likely_result: block unless reviewed support exists
```

Result: PASS.

## B. Warrant Quality Tests

### B1: Blank Warrant

Input:

```yaml
action_facing_claim: Promote v0.2.13 revised to mainline now.
point_specific_anchored_evidence:
  - Pro review said direction is valid.
non_circular_warrant:
```

Expected:

```text
status: insufficient
reason: missing_or_non_explanatory_warrant
```

Result: PASS.

### B2: Circular Warrant

Input:

```yaml
action_facing_claim: Promote v0.2.13 revised to mainline now.
point_specific_anchored_evidence:
  - Pro review said direction is valid.
non_circular_warrant: It should be promoted because the evidence supports promoting it.
```

Expected:

```text
status: insufficient
reason: circular_warrant
```

Result: PASS.

### B3: Scope Jump

Input:

```yaml
action_facing_claim: Every source intake should use the action-support rule.
point_specific_anchored_evidence:
  - GSN/CAE material says action-facing claims should show argument/evidence/context.
non_circular_warrant: Since GSN uses structured arguments, every VAKS intake should use structured arguments.
```

Expected:

```text
status: insufficient
reason: scope_jump
```

Result: PASS.

### B4: Evidence Mismatch

Input:

```yaml
action_facing_claim: VAKS should implement a diagram editor.
point_specific_anchored_evidence:
  - GSN/CAE material supports making action support visible.
non_circular_warrant: Since diagrams can communicate arguments, VAKS should implement diagram editing.
```

Expected:

```text
status: insufficient
reason: evidence_mismatch
```

Result: PASS.

### B5: Good Scoped Warrant

Input:

```yaml
action_facing_claim: v0.2.13 revised should remain candidate-only and be tested on one real action-basis example.
point_specific_anchored_evidence:
  - Pro review verdict was revise_candidate, not reject.
  - Pro review requested one real VAKS action-basis example.
  - Revised patch says no mainline promotion without real trial.
non_circular_warrant: These anchors directly address the same lifecycle question: what to do next with the v0.2.13 rule. They support continued candidate testing because they accept the direction while withholding mainline promotion until a real example shows practical value.
scope_assumptions:
  - applies only to v0.2.13 revised candidate.
known_challenges_or_gaps:
  - no real action-basis example yet.
current_residual_review_status: candidate-only, next step real example trial.
```

Expected:

```text
status: candidate_review_can_proceed
mainline_ready: no
```

Result: PASS.

## C. Evidence Integrity Tests

### C1: Bare URL As Support

Input:

```yaml
action_facing_claim: GSN supports VAKS v0.2.13.
point_specific_anchored_evidence:
  - https://scsc.uk/gsn-standard
non_circular_warrant: The URL exists.
```

Expected:

```text
status: insufficient
reason: bare_url_is_provenance_not_support
```

Result: PASS.

### C2: Background Citation As Support

Input:

```yaml
action_facing_claim: VAKS should create a candidate pattern now.
point_specific_anchored_evidence:
  - GSN/CAE are generally about claims, arguments, and evidence.
non_circular_warrant: Since this family exists, the pattern is justified.
```

Expected:

```text
status: insufficient
reason: background_citation_not_point_specific_support
```

Result: PASS.

### C3: Source-Family Repetition As Independence

Input:

```yaml
action_facing_claim: The same mechanism has three independent supports.
point_specific_anchored_evidence:
  - SCSC GSN overview
  - SCSC GSN nutshell
  - SCSC GSN pattern catalogue
non_circular_warrant: Three pages means independent support.
```

Expected:

```text
status: insufficient_for_independence_claim
reason: same_source_family_repetition
```

Result: PASS.

### C4: Tool / Vendor / Diagram As Support

Input:

```yaml
action_facing_claim: VAKS should implement assurance-case tooling.
point_specific_anchored_evidence:
  - SCSC Tools lists several tools.
  - Vendor pages describe diagram editors and evidence repositories.
non_circular_warrant: Many tools and mature diagrams show VAKS should implement this.
```

Expected:

```text
status: insufficient
reason:
  - tool_count_not_support
  - vendor_claim_not_conformance_validation
  - diagram_clarity_not_action_readiness
```

Result: PASS.

### C5: Active Candidate Pattern As Reviewed Truth

Input:

```yaml
action_facing_claim: `retrieval-is-activation-not-truth` is active, so it is reviewed VAKS truth.
point_specific_anchored_evidence:
  - candidate pattern file status: active
non_circular_warrant: Active means accepted.
```

Expected:

```text
status: insufficient
reason: active_candidate_pattern_not_reviewed_truth
```

Result: PASS.

## D. Real Material Trials

### D1: `retrieval-is-activation-not-truth` As Action-Facing Rule Candidate

Input claim:

```text
VAKS should continue treating retrieval as activation/context preparation, not truth or action basis.
```

Anchored evidence:

```text
- `retrieval-is-activation-not-truth.md` one-line pattern says retrieval/vector/rerank/GraphRAG/community summary/agentic retrieval bring material forward but are not truth confidence, reviewed relation, or action basis.
- VAKS project borrowing ledger marks this pattern `adapt` and says it already matches the core boundary, but still needs wording review before template patch.
- v0.2.13 revised patch preserves retrieval/context pack as activation/context preparation.
```

Non-circular warrant:

```text
The evidence directly supports the scoped claim because all three anchors address the same boundary: retrieval can activate context but cannot create support, reviewed relation, or action readiness. The ledger's `adapt` disposition supports project fit only; it does not by itself promote the rule to mainline.
```

Challenges/gaps:

```text
- Existing candidate pattern is active but not reviewed knowledge.
- Ledger disposition is not ADR/action basis.
- Any template wording still needs review.
```

Expected:

```text
status: candidate_action_basis_packet_coherent
allowed_next_step: wording review or real action-basis note
blocked_next_step: automatic mainline promotion
```

Result: PASS.

This is the strongest positive trial. The rule helps because it forces the difference between:

```text
retrieval boundary has project fit
```

and:

```text
retrieval boundary is reviewed architecture text
```

### D2: `source-structure-first-rag` Used To Change Templates Now

Input claim:

```text
VAKS should update source intake templates now to require structure-preserving fields.
```

Anchored evidence:

```text
- `source-structure-first-rag.md` says preserving source structure before chunking has value.
- VAKS ledger marks it `adapt` for future source intake, context-pack preparation, retrieval workbench.
```

Non-circular warrant being tested:

```text
The pattern is active and marked adapt, so templates should change now.
```

Expected:

```text
status: insufficient
reason:
  - candidate_pattern_not_template_authority
  - ledger_adapt_not_action_basis
  - required_gates_missing
  - ordinary_capture_burden_risk
```

Result: PASS.

The revised rule blocks the action and preserves the boundary.

### D3: VAKS Ledger `adapt` Treated As ADR / Action Basis

Input claim:

```text
Because the VAKS ledger says `adapt`, the architecture decision has been made.
```

Expected:

```text
status: blocked
reason: project_borrowing_ledger_not_ADR_not_action_basis_not_truth_confidence
```

Result: PASS.

### D4: SCSC Tools Used For Assurance-Tool Adoption

Input claim:

```text
VAKS should adopt an assurance-case tool or build equivalent tooling because SCSC lists many tools.
```

Anchored evidence:

```text
- SCSC Tools page lists tools.
- v0.2.12 SCSC Tools trial records that the page is not endorsement, recommendation, or conformance validation.
```

Expected:

```text
status: blocked
reason:
  - tool_catalogue_discovery_only
  - no adoption evidence
  - no conformance validation
  - no VAKS fit review
```

Result: PASS.

### D5: SCSC Tools Ordinary Intake

Input:

```text
Create/keep source routing overlay for SCSC Tools.
No action decision.
```

Expected:

```text
trigger_make_support_visible: no
```

Result: PASS.

This confirms the rule does not drag a finished v0.2.12 intake trial into an action-basis envelope.

## E. Regression / Overclaim Tests

### E1: "Ordinary Intake Is Proven Unaffected"

Input claim:

```text
The tests prove ordinary intake will not be burdened.
```

Expected:

```text
status: overclaim
corrected_claim: The design intends not to burden ordinary intake, and pressure tests found no forced trigger. Real use is still unproven.
```

Result: PASS.

### E2: Create Candidate Pattern From v0.2.13

Input claim:

```text
Create `structured-action-basis-envelope` in candidate_pattern_bank now.
```

Expected:

```text
status: blocked
reason: Pro review says no pattern file now; this is a terminal rule, not a standalone pattern yet.
```

Result: PASS.

### E3: Promote To Mainline Without Real Example

Input claim:

```text
Add the revised rule to mainline docs now.
```

Expected:

```text
status: blocked
reason: no real VAKS action-basis trial yet; second-pass wording review still needed.
```

Result: PASS.

## Fault Hunt

I tried to break the rule in these ways:

```text
make it trigger too early
make it accept a circular warrant
make it accept a scope jump
make it accept source-family repetition as independent support
make it accept tool/vendor/diagram material as support
make it treat candidate pattern status as reviewed truth
make it treat ledger adapt as ADR
make it overclaim ordinary-intake non-burden
make it create a pattern prematurely
make it promote to mainline prematurely
```

None found a blocking design failure after the Pro revisions.

## Remaining Weaknesses

These are real, but they are not current blockers:

1. Warrant quality still requires reviewer judgment. A future lightweight reviewer checklist may help if repeated use is inconsistent.
2. The rule has not yet been used on a freshly arising, high-stakes VAKS action-basis note.
3. The rule does not automate evidence support checking; it only makes the support claim inspectable.
4. A sloppy operator could still fill the fields badly. The rule catches obvious bad forms, not all bad reasoning.

## Stress Verdict

Current verdict:

```text
v0.2.13 revised candidate survives pressure testing.
```

Disposition:

```text
keep_candidate: yes
revise_again_now: no
create_candidate_pattern: no
promote_to_mainline: no
next_required_work: one real fresh action-basis trial
```

Plain-language confidence:

```text
I am convinced this is the right candidate shape for now.
I do not see a reason to reject it or reshape it again before a real fresh trial.
I still would not promote it to mainline without that real trial.
```
