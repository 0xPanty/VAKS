---
type: qa
status: active
created: 2026-05-30
updated: 2026-05-30
project: verified-action-knowledge-system
scope:
  - evidence-packet
  - micro-trial
  - v0-3
sources:
  - "outputs/review/2026-05-29-framework-reference-research.md"
  - "FUSION_ARCHITECTURE_V0_2_DRAFT.md"
  - "SCHEMA.md"
verification_status: in-review
evidence_level: excerpt
confidence: medium
last_verified: 2026-05-30
next_review: 2026-06-03
tags:
  - evidence-discipline
  - micro-trial
  - review-queue
---

# Evidence Packet Micro-Trial

Post-Pro note:
This was the first local micro-trial and preserves a draft packet shape. Its main value is the lazy-gate pressure test. The canonical post-Pro packet shape now puts source anchors on `evidence_items`, uses `evidence_support.evidence_role` instead of `relation_to_point`, and uses `knowledge_state` for review output. See `outputs/review/2026-05-30-v0-3-integrated-ten-alpha-trial.md` for the patched canonical trial.

## Purpose

This is a manual micro-trial for v0.3 Evidence and Review Discipline.

It tests whether Evidence Packet improves review clarity without becoming a new truth layer or heavy workflow.

This trial does not validate external papers or repos. It validates the local architecture contract against one local research artifact and the newly written local rules.

## Trial Question

```text
Should Evidence Packet become the lightweight review input for important promotion or action use?
```

## Source Anchors

### A1 Framework Research Boundary

Source:

```text
outputs/review/2026-05-29-framework-reference-research.md:13-17
```

Anchor:

```text
candidate-only: 以下所有判断都是候选输入，不是 reviewed truth。
provenance is not support: 来源、引用、出处只能说明“从哪里来”，不能自动说明“支持这个判断”。
similarity is not relation: 向量相似、检索分数、共同主题都不能直接写成 supports / contradicts / refines。
feedback is not truth: 使用反馈只能影响 activation / usefulness / scope fit，不能直接改 truth confidence。
```

Evidence relation:

```text
supports boundary only
```

### A2 Evidence Packet Alpha

Source:

```text
outputs/review/2026-05-29-framework-reference-research.md:776-806
```

Anchor:

```text
最强 alpha: 把 review input 统一成 Evidence Packet，而不是 source summary。
...
为什么无缝: 它正好落在 Understand -> Review 之间，不改变主架构，也不直接升级 truth。
```

Evidence relation:

```text
supports point P1
```

### A3 Warrant And Challenge Alpha

Source:

```text
outputs/review/2026-05-29-framework-reference-research.md:808-840
```

Anchor:

```text
有来源不等于有证据；有证据不等于证据能支持该判断。
...
它让 Point Collision 不再只有“推翻/接受”，而是给 reviewer 更小的修订动作。
```

Evidence relation:

```text
supports points P2 and P3
```

### A4 Omission And Granularity Alpha

Source:

```text
outputs/review/2026-05-29-framework-reference-research.md:913-942
```

Anchor:

```text
source digest / compiled wiki 最大风险不是写错，而是丢掉关键事实、边界条件、反例和风险。
...
不必一开始就 full read，但必须知道当前证据粒度停在哪一层。
```

Evidence relation:

```text
supports omission_check and evidence_granularity
```

### A5 Local v0.3 Rule

Source:

```text
FUSION_ARCHITECTURE_V0_2_DRAFT.md:3153-3181
SCHEMA.md:750-756
```

Anchor:

```text
A source is not evidence by itself.
A citation is not support by itself.
A retrieved relation is not a reviewed relation.
...
Evidence Packet does not create truth, confidence, reviewed relation, or action readiness by itself.
```

Evidence relation:

```text
local constraint / boundary
```

## Candidate Points

| Point | Type | Evidence granularity | Initial judgment |
|---|---|---|---|
| P1: Evidence Packet should be the lightweight review input for important promotion or action use. | pattern | excerpt_or_passage | standing with scope limit |
| P2: Warrant separation should be required for high-value judgments, not ordinary capture. | pattern | excerpt_or_passage | standing |
| P3: Minimal revision should be a standard Point Collision output. | pattern | excerpt_or_passage | standing with template caution |

## Evidence Packet P1

```yaml
evidence_packet:
  point: "Evidence Packet should be the lightweight review input for important promotion or action use."
  point_type: pattern
  source_anchors:
    - url_or_path: outputs/review/2026-05-29-framework-reference-research.md
      exact_quote: "把 review input 统一成 Evidence Packet，而不是 source summary。"
      prefix: "### 3.1 Evidence Packet"
      suffix: "它正好落在 Understand -> Review 之间，不改变主架构，也不直接升级 truth。"
      captured_at: 2026-05-30
    - url_or_path: FUSION_ARCHITECTURE_V0_2_DRAFT.md
      exact_quote: "Before important knowledge is promoted or used for action, the system should build an Evidence Packet."
      prefix: "The system adopts a lightweight evidence discipline:"
      suffix: "This is not a formal logic system."
      captured_at: 2026-05-30
  evidence_items:
    - source_anchor: A2
      evidence_granularity: excerpt_or_passage
      relation_to_point: supports
      rationale: "The research explicitly proposes Evidence Packet as the strongest alpha and locates it between Understand and Review."
    - source_anchor: A5
      evidence_granularity: excerpt_or_passage
      relation_to_point: limits_scope
      rationale: "The local v0.3 rule narrows the trigger to important promotion or action use and denies truth authority."
  grounds: "The research identifies a gap between source summary and review input; local v0.3 writes this as a bounded review rule."
  warrant: "Review quality improves when the reviewer sees a point, concrete evidence span, relation to point, scope, risk, and minimal revision in one packet."
  qualifier: "Use for promotion, decision, strong reviewed relation, action basis, explicit challenge, stale/contested point, high-impact source review, or reviewer request."
  strongest_rebuttal: "This could make ordinary capture too heavy if required everywhere."
  challenge_kind: scope_limit
  risk_flags:
    - review_burden
    - template_bloat
  omission_check:
    missing_risks: "Could still miss external source-specific limitations because this trial uses local excerpts only."
    missing_scope_limits: "Does not test paper/code/table anchors."
    possible_omissions: "No original FEVER/AVeriTeC/ClaimVer source was re-read in this trial."
    needs_full_source_read: false
  review_question: "Is the lazy trigger narrow enough to prevent ordinary capture paperwork?"
  minimal_revision_needed: refine_scope
```

Review result:

```yaml
review_result:
  knowledge_state: limited
  strongest_challenge: "Could become paperwork if attached to ordinary capture."
  scope_limit: "Important promotion or action use only."
  minimal_revision_needed: refine_scope
  review_due_when:
    - micro_trial_finds_burden
    - ordinary_capture_gets_slow
    - template_users_skip_fields
```

## Evidence Packet P2

```yaml
evidence_packet:
  point: "Warrant separation should be required for high-value judgments, not ordinary capture."
  point_type: pattern
  source_anchors:
    - url_or_path: outputs/review/2026-05-29-framework-reference-research.md
      exact_quote: "有来源不等于有证据；有证据不等于证据能支持该判断。"
      prefix: "### 3.2 Warrant Is Separate From Provenance"
      suffix: "只在 architecture decision、high-impact pattern、reviewed claim 中启用，不强制普通 capture 填写。"
      captured_at: 2026-05-30
    - url_or_path: SCHEMA.md
      exact_quote: "grounds records the evidence basis; warrant records why the evidence supports or weakens the point."
      prefix: "Rules:"
      suffix: "challenge_kind explains what kind of challenge exists; it does not automatically reject the point."
      captured_at: 2026-05-30
  evidence_items:
    - source_anchor: A3
      evidence_granularity: excerpt_or_passage
      relation_to_point: supports
      rationale: "The research directly identifies the source/evidence/warrant split."
    - source_anchor: A5
      evidence_granularity: excerpt_or_passage
      relation_to_point: supports
      rationale: "The schema now records grounds and warrant as review input, not truth."
  grounds: "The reviewed material already guards provenance/support; warrant makes the bridge explicit."
  warrant: "Separating warrant prevents URL/citation/source presence from being mistaken for support."
  qualifier: "High-value judgments only."
  strongest_rebuttal: "If required too often, reviewers may fill warrant with vague prose."
  challenge_kind: source_hygiene
  risk_flags:
    - vague_warrant
    - reviewer_fatigue
  omission_check:
    missing_risks: "Could need examples of good/bad warrant."
    missing_scope_limits: "No claim/pattern/decision template examples yet."
    possible_omissions: "No external Toulmin source was re-opened."
    needs_full_source_read: false
  review_question: "Do templates need examples to prevent vague warrants?"
  minimal_revision_needed: keep
```

Review result:

```yaml
review_result:
  knowledge_state: standing
  strongest_challenge: "Risk of vague warrants."
  scope_limit: "Only high-value review surfaces."
  minimal_revision_needed: keep
  review_due_when:
    - reviewers_fill_warrant_vaguely
    - micro_trial_cannot_distinguish_ground_from_warrant
```

## Evidence Packet P3

```yaml
evidence_packet:
  point: "Minimal revision should be a standard Point Collision output."
  point_type: pattern
  source_anchors:
    - url_or_path: outputs/review/2026-05-29-framework-reference-research.md
      exact_quote: "collision 后只问最小必要动作：keep / refine_scope / mark_contested / mark_stale / supersede / reject。"
      prefix: "最小优雅吸收方向："
      suffix: "Source anchor: 对网页/论文/代码采用 url/path + exact quote..."
      captured_at: 2026-05-30
    - url_or_path: outputs/review/2026-05-29-framework-reference-research.md
      exact_quote: "它让 Point Collision 不再只有“推翻/接受”，而是给 reviewer 更小的修订动作。"
      prefix: "### 3.4 Minimal Revision Needed"
      suffix: "### 3.5 Source Anchor Mini-Profile"
      captured_at: 2026-05-30
  evidence_items:
    - source_anchor: A3
      evidence_granularity: excerpt_or_passage
      relation_to_point: supports
      rationale: "The research states the benefit and enum directly."
  grounds: "Point Collision needs a next-action vocabulary that is smaller than automatic conflict resolution."
  warrant: "Reviewers can preserve contested knowledge better when the output is a minimal revision suggestion."
  qualifier: "It remains review routing metadata and does not edit reviewed knowledge automatically."
  strongest_rebuttal: "The enum might be too small for some decision superseding cases."
  challenge_kind: scope_limit
  risk_flags:
    - enum_too_small
  omission_check:
    missing_risks: "Does not test every collision type."
    missing_scope_limits: "Decision superseding may need richer audit fields."
    possible_omissions: "No multi-source conflict trial yet."
    needs_full_source_read: false
  review_question: "Is the enum enough for first micro-trial?"
  minimal_revision_needed: keep
```

Review result:

```yaml
review_result:
  knowledge_state: standing
  strongest_challenge: "May need richer fields for decision superseding."
  scope_limit: "Use as a review suggestion; detailed superseding still uses decision_superseding."
  minimal_revision_needed: keep
  review_due_when:
    - collision_trial_needs_extra_action
    - decision_superseding_cannot_be_expressed
```

## Context Pack Trace

```yaml
context_pack_trace:
  used_sources:
    - outputs/review/2026-05-29-framework-reference-research.md
    - FUSION_ARCHITECTURE_V0_2_DRAFT.md
    - SCHEMA.md
  ignored_sources:
    - external FEVER / AVeriTeC / ClaimVer repos
    - external Toulmin / argumentation primary texts
  ignored_reason: "This trial validates local review contract behavior, not external source truth or implementation."
  activation_role: core
  unresolved_contradictions:
    - "No direct external source-code or primary-paper recheck was performed."
  risk_flags:
    - source_depth_limited
    - architecture_self_reference
```

## Logic Test Matrix

| Test | Expected | Result |
|---|---|---|
| URL-only citation is not support. | block promotion support | pass |
| Evidence Packet does not create truth. | review input only | pass |
| Warrant explains support path. | provenance/support split visible | pass |
| Challenge is not only contradiction. | scope_limit / source_hygiene available | pass |
| Minimal revision avoids auto conflict resolution. | refine_scope / keep instead of auto edit | pass |
| Omission check catches source-depth limitation. | missing external primary-source check visible | pass |
| Context trace exposes ignored sources. | external repos/papers explicitly ignored | pass |

## Trial Finding

Evidence Packet is useful enough to keep.

It improved review clarity in three ways:

```text
1. It forced the point and evidence span to stay together.
2. It forced warrant / scope / challenge to be explicit.
3. It made source-depth limitations visible through omission_check and context_pack_trace.
```

It also exposed the main weakness:

```text
This trial used local excerpts and local schema rules.
It did not verify the external primary sources or repo implementations behind the research report.
```

That weakness does not invalidate the local contract test. It means the next trial should use one external primary source or one repo source record if the goal is source-level validation.

## Decision

```yaml
decision:
  keep_evidence_packet: true
  keep_as_truth_layer: false
  keep_as_review_queue_input: true
  next_revision: refine_scope
  next_trial:
    - use one external primary source
    - create one candidate point
    - test source_anchor + evidence_granularity + omission_check
```

## Stop Point

Do not add automation yet.

Next useful step:

```text
Run a second micro-trial on one external primary source or repo record, not on the local research summary.
```
