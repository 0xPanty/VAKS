---
type: landed_rule_operational_test
status: passed
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: v0.2.13-action-support-visibility-after-main-architecture-landing
truth_boundary: operational test report; not reviewed knowledge; not release tag; not schema; not template
write_scope: outputs/review only
---

# v0.2.13 Landed Rule Operational Test

## 说人话结论

这次测的是已经落进主架构的规则，不是继续测候选想法。

被测规则：

```text
Evidence is not enough; show the non-circular warrant.
```

落地位置：

```text
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
```

测试结果：

```text
pass
```

更具体：

```text
轻层没有被拖重。
中层没有被误当决策。
重层能要求 claim / evidence / warrant / scope / gap / residual status。
工具页、source count、routing hint、candidate pattern、ledger adapt 都不能偷渡成 support 或 action readiness。
```

## Preflight: Landing Check

### Main architecture contains the landed rule

Observed anchors:

```text
FUSION_ARCHITECTURE_V0_2_DRAFT.md
  - Action Support Visibility
  - non-circular warrant
  - diagrams / notation / source counts / tool counts / vendor pages / confidence labels do not increase support

ARCHITECTURE_PRINCIPLES.md
  - evidence list is not action basis by itself
  - action-facing use must show a non-circular warrant
  - ordinary capture and ordinary query stay light
```

Result:

```text
pass
```

### Obsidian copy matches repo copy

Checked:

```text
H:\Obsidian\资料库\FUSION_ARCHITECTURE_V0_2_DRAFT.md
H:\Obsidian\资料库\ARCHITECTURE_PRINCIPLES.md
```

Result:

```text
pass
```

The file hashes matched the repo copies at test time.

### Forbidden surfaces not modified by this test

Checked:

```text
SCHEMA.md
REVIEW_QUEUE.md
templates/
```

Result:

```text
pass
```

No diff was present on those surfaces for this test.

## Test 1: Light Source Intake Should Stay Light

Input:

```text
SCSC Tools page lists GSN / assurance-case tools.
```

Question:

```text
Should this create a VAKS pattern, tool recommendation, adoption decision, or action basis?
```

Landed-rule expectation:

```text
No.
This is ordinary source intake / tool-directory triage.
v0.2.13 should not trigger.
```

Observed anchors:

```text
outputs/review/2026-06-05-v0-2-12-intake-trial-scsc-tools.md
  - no new pattern from one source: pass
  - SCSC listing does not validate GSN conformance
  - tool directory as discovery, not endorsement
  - new_pattern_created: no
  - Should this create a pattern? no
  - Keep this as outputs/review candidate-only
```

Result:

```text
pass
```

Why this matters:

```text
落地规则没有把普通资料 intake 变成 assurance-case 审查。
```

## Test 2: Source Routing Overlay Must Not Become Support

Input:

```text
Source Routing Overlay row maps a source to possible candidate pattern routes.
```

Question:

```text
Can the route itself count as evidence support or project decision?
```

Landed-rule expectation:

```text
No.
Routing hint is not support.
Pattern route is not action readiness.
```

Observed anchors:

```text
outputs/review/source_cards/2026-06-04-external-intake-source-routing-ledger.md
  - truth_boundary: routing hints only; candidate-only
  - source_family_id prevents same-family repetition from becoming independent support
  - pattern route is only route suggestion, not support

outputs/review/source_cards/INDEX.md
  - routing index only; not source replacement; not reviewed knowledge
```

Result:

```text
pass
```

Why this matters:

```text
开发区前面的薄 routing 层没有变成半决策层。
```

## Test 3: Medium Candidate Pattern / Borrowing Entry Must Stay Pre-Decision

Input:

```text
Candidate pattern: retrieval-is-activation-not-truth
Project borrowing ledger: VAKS disposition = adapt
```

Question:

```text
Does active candidate pattern + VAKS adapt mean mainline promotion or template change is allowed now?
```

Landed-rule expectation:

```text
No.
Candidate pattern is reusable candidate knowledge.
Borrowing entry is project fit / development workspace.
Neither is action basis.
```

Observed anchors:

```text
outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
  - truth_boundary: candidate pattern only; not reviewed knowledge
  - retrieval / vector / rerank / GraphRAG / agentic retrieval are not truth confidence, reviewed relation, or action basis

outputs/review/project_borrowing_ledgers/VAKS.md
  - truth_boundary: project fit ledger only; not reviewed knowledge; not ADR; not action basis
  - watch / prototype / adapt / reject are only project borrowing postures
  - real architecture / reviewed relation / action basis must go through later review / decision
```

Result:

```text
pass
```

Why this matters:

```text
中层能参考，但不会自动变成正式决策。
```

## Test 4: Heavy Action-Facing Claim With Good Warrant

Input:

```text
Claim: Keep the v0.2.13 minimal mainline action-support visibility wording for now.
```

Evidence:

```text
Pro review accepted the direction but asked for narrowing.
Main architecture landing is only minimal wording.
Pressure tests caught circular warrant, source-family fake independence, and tool/vendor/diagram shortcuts.
No-upgrade and dual-project tests showed light / medium layers do not get forced into heavy flow.
```

Warrant:

```text
These anchors all address the same promotion boundary:
whether the minimal action-support visibility wording should remain after landing.
They support keeping the small rule because it strengthens the existing action-basis gate
without adding schema/template/directory/system expansion.
They do not support expanding beyond the minimal rule.
```

Expected judgment:

```text
keep minimal rule
block expansion
```

Observed anchor:

```text
outputs/review/2026-06-05-v0-2-13-real-promotion-validation.md
  - minimal_mainline_wording: keep_for_now
  - expansion_to_schema: blocked
  - expansion_to_template: blocked
  - stable_project_workspace_migration: blocked
  - ordinary_intake_change: blocked
```

Result:

```text
pass
```

Why this matters:

```text
重层不是只会拦，也能放行一个范围很窄、warrant 清楚的主架构小规则。
```

## Test 5: Tool Catalogue Shortcut Must Fail

Input:

```text
Claim: VAKS should adopt or build assurance-case tooling because SCSC lists many tools.
```

Bad evidence:

```text
SCSC tool list
many tool names
vendor feature descriptions
GSN / assurance-case diagrams and notation
```

Bad warrant:

```text
Many tools exist, so this is mature enough for VAKS to adopt.
```

Landed-rule expectation:

```text
fail
```

Failure reason:

```text
tool count is not support
vendor claim is not support
catalogue membership is not conformance validation
diagram / notation is not action readiness
```

Result:

```text
pass
```

The claim is correctly blocked.

## Test 6: Circular Warrant Must Fail

Input:

```text
Claim: VAKS should update source intake templates now to require source-structure preservation fields.
```

Bad evidence:

```text
candidate pattern is active
VAKS project borrowing ledger says adapt
```

Bad warrant:

```text
It is active and adapt, so templates should change now.
```

Landed-rule expectation:

```text
fail
```

Failure reason:

```text
candidate pattern is not reviewed knowledge
ledger adapt is not architecture decision
required gates before template change are missing
ordinary capture burden risk remains unresolved
```

Observed anchor:

```text
outputs/review/2026-06-05-v0-2-13-revised-nonmeta-action-basis-trials.md
  - Trial 2 blocked template change now
```

Result:

```text
pass
```

The premature template change is correctly blocked.

## Test 7: Ordinary Intake Contamination Check

Input:

```text
New reference arrives.
Agent wants to process it.
```

Question:

```text
Does v0.2.13 require every source card, routing row, or candidate point to carry a full warrant packet?
```

Landed-rule expectation:

```text
No.
Default is light.
v0.2.13 only triggers for action_basis / significant promotion / significant decision / risk-sensitive action use.
```

Observed anchor:

```text
outputs/review/2026-06-05-v0-2-13-usage-guide.md
  - 轻 = 能搜到
  - 中 = 能参考
  - 重 = 能拿来做决定
  - ordinary intake does not trigger v0.2.13
```

Result:

```text
pass
```

Why this matters:

```text
这条规则没有把日常资料处理拖成重模板。
```

## Final Verdict

```yaml
landed_rule_presence: pass
obsidian_sync: pass
forbidden_surface_check: pass
light_intake_not_heavy: pass
routing_hint_not_support: pass
candidate_pattern_not_decision: pass
good_heavy_warrant_allows_minimal_rule: pass
tool_catalogue_shortcut_blocked: pass
circular_warrant_blocked: pass
ordinary_intake_contamination_blocked: pass
overall: pass
```

## What The Test Proves

It proves:

```text
The landed v0.2.13 rule works as a final action-basis guardrail.
It can keep a narrowly justified mainline rule.
It blocks common fake-support shortcuts.
It does not force light or medium layers into heavy review.
```

It does not prove:

```text
long-run usability over months
stable workspace migration readiness
schema/template readiness
full assurance-case system value
```

## Operational Status After Test

```yaml
minimal_mainline_rule: keep
usage_guide: keep
outputs_review_validations: keep
schema_change: no
template_change: no
stable_directory_migration: no
candidate_pattern_from_assurance_case_cluster: no
commit_push: no
```
