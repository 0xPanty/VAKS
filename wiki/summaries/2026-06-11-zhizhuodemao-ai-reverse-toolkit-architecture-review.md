---
type: architecture_review
record_kind: architecture_review
status: candidate
title: "zhizhuodemao/ai-reverse-toolkit architecture review"
source_ref: "raw/repos/2026-06-11-zhizhuodemao-ai-reverse-toolkit-source.md"
source_id: "github:zhizhuodemao/ai-reverse-toolkit@02799de7420ea78c57bf7af8cc0f2d38fef017bd"
source_uri: "https://github.com/zhizhuodemao/ai-reverse-toolkit"
created_at: "2026-06-11"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
truth_status: not_reviewed
action_basis_allowed: false
truth_mutation_allowed: false
retrieval_policy:
  policy_kind: candidate_review_summary
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: architecture_review_not_adoption
project_fit:
  verified_action_knowledge_system: strong_workflow_design_fit
  truth_layer: reject
  review_layer: process_inspiration_only
  activation_layer: strong_fit
  retrieval_layer: diagnostic_workflow_fit
assessment:
  domain: ai-assisted-expert-workflow
  maturity: emerging
  complexity: medium
  problem_fit_vaks_workflow: 4
  problem_fit_vaks_truth: 1
  reuse_value: 4
  implementation_cost: 2
  integration_fit: 4
  evidence_strength: 3
  reversibility: 5
tags:
  - architecture-review
  - candidate
  - ai/skill-workflow
  - vaks/process-inspiration
  - vaks/retrieval-diagnostics
  - risk/security-bypass-excluded
---

# ai-reverse-toolkit Architecture Review

## One-Line Judgment

`ai-reverse-toolkit` is worth preserving as a strong candidate reference for
VAKS workflow/skill design. It should not be adopted as a security-reversal
tool inside VAKS.

## Problem It Solves

The repository tries to make AI behave like a structured reverse-engineering
analyst by encoding expert workflow into skills, rules, references, scripts,
and evaluation loops.

The reusable problem is broader:

```text
How do we turn tacit expert procedure into AI-executable, evidence-aware,
bounded workflows?
```

## Architecture Shape

```text
user intent
-> skill trigger
-> bounded task scope
-> strategy selection
-> tool operation
-> diagnostic report
-> reference lookup
-> intermediate artifacts
-> completion standard
-> validation/eval loop
```

For VAKS this maps to:

```text
user question
-> query intent router
-> authority/scope boundary
-> allowed retrieval tools
-> retrieval diagnostics
-> source/candidate/review anchors
-> context pack or review input
-> evidence/action gate only when needed
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:11-13` | The repo frames itself as encoding expert experience into AI instructions | Expert workflow can be made explicit and executable | General design only |
| `README.md:15-24` | Skills, rules, and guidance are separated | Progressive disclosure across skill body and references | Borrow strongly |
| `README.md:57-60` | Skill table lists input and output per skill | Bounded skill contracts | Borrow strongly |
| `CLAUDE.md` | Prompt/knowledge repo, no build/test app | This is a workflow knowledge artifact, not a runtime dependency | Do not import as platform |
| `rules/js-reverse.md` | Six-stage technical manual | Background manuals complement task skills | Borrow structure only |
| `skills/find-crypto-entry/SKILL.md:17-23` | Strategy selection based on signal | Use signal-based route selection | Borrow for query intent |
| `skills/find-crypto-entry/SKILL.md:49-72` | Anti-patterns and completion standard | Stop at stage boundary | Borrow strongly |
| `skills/env-patch/SKILL.md:16-34` | Engine/strategy split, immutable source, load-order rules, format check | Separate tool engine from policy/strategy | Borrow pattern only |
| `skills/env-patch/SKILL.md:116-184` | Diagnostic loop and references | Failure classes route next actions | Borrow for retrieval diagnostics |
| `skills/ast-deobfuscate/SKILL.md:56-67` | Plan mode, skip irrelevant steps, MCP as probe | Do not force one full pipeline on every task | Borrow strongly |
| `skills/ast-deobfuscate/SKILL.md:527-563` | Safety, intermediate files, preserve uncertainty | Reversibility and uncertainty preservation | Borrow strongly |
| `skills/skill-creator/SKILL.md:47-111` | Capture intent, progressive disclosure, no-surprise principle | Good skills need trigger and safety boundaries | Borrow strongly |
| `skills/skill-creator/SKILL.md:141-232` | Test prompts, baseline, assertions, grading | Skill quality can be measured | Borrow for VAKS skill evals |

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Turns lightweight workflows into explicit instructions | adapt |
| Dusk workbench | Useful for visible workflow steps and diagnostics | adapt |
| source ingest | Strong trigger/scope/completion design for intake skills | adapt |
| review queue | Diagnostic classes map to review reasons | adapt |
| schema / reviewed knowledge | No direct schema authority | reject |
| memory / dev context | Skill outputs can become dev-context hints, not truth | adapt |
| feedback | Skill evaluation loop maps to feedback ledger | adapt |
| retrieval / cache | Diagnostic loop maps to retrieval failure classes | adapt |
| API / MCP / agent access | Tool/skill separation is useful for future agent tools | adapt carefully |
| viewer / workbench | Eval viewer idea suggests workflow result review surface | watch |
| publishing | No direct value | no-clear-value |
| risk / anti-pattern | Security bypass tactics are a boundary risk | avoid |

## 值得提炼的模式

### Expert Workflow As Skill

专家经验 should not stay as prose only. It should be encoded as:

```text
trigger
scope
decision points
anti-patterns
references
outputs
completion criteria
```

### Diagnostic Loop

Failures should be classified before action:

```text
missing input
wrong scope
stale cache
authority collision
missing evidence
tool unavailable
known limitation
```

### Completion Standard

Each workflow should say where it stops:

```text
find source != distill source
distill source != review claim
build context != approve action
record feedback != mutate truth
```

### Skill Evaluation

VAKS can evaluate workflows with:

```text
baseline vs skill
old skill vs new skill
human feedback
objective assertions where possible
failure case retention
```

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Complex expert workflows should be skill-encoded | VAKS already separates process layers and gates | candidate_relation | Which workflows should become first-class VAKS skills first? |
| Diagnostic loops are better than one-shot automation | VAKS lazy gates and maintenance lint already prefer scoped checks | candidate_relation | What retrieval failure taxonomy should VAKS use? |
| Skill outputs need evaluation against baselines | VAKS feedback ledger and maintenance manifests are not truth | missing_evidence | What minimal eval fixture can test a VAKS retrieval/context skill? |
| Security-specific reverse tactics should not become VAKS workflow defaults | VAKS boundaries reject unauthorized or action-leaking use | scope_mismatch | How should VAKS document black-box analysis without enabling bypass work? |

## Support / Challenge Review

- What supports it:
  - The repository has concrete skill files with trigger/scope/outputs.
  - The structure separates skills, rules, scripts, references, and eval logic.
  - The skill-creator flow explicitly includes baseline and feedback loops.
- What challenges it:
  - Domain is security reverse engineering, not knowledge governance.
  - Some references are operationally sensitive and should not be imported.
  - Repo maturity is low to medium: small, recent, no runtime validation here.
- Challenge severity: major for security-specific tactics, minor for workflow pattern.
- Scope limits:
  - Use as workflow-design inspiration only.
  - Do not use as an action guide for bypassing protections.
- Action readiness: not_ready.

## 对当前项目的适配点

Directly useful for VAKS:

```text
source intake skill design
retrieval query-run diagnostic taxonomy
context pack builder completion standard
evidence sufficiency gate workflow
black-box product analysis workflow
skill eval and baseline harness
```

Not useful for VAKS:

```text
signature bypass
anti-debug evasion
private implementation extraction
platform-specific reverse operations
```

## 融合判断

- Conclusion: adapt.
- Direct use: no.
- Fork: no.
- Design-only: yes.
- Current branch value: strong for VAKS workflow and black-box analysis design.
- Whole architecture value: strong as a model for AI-executable process skills.
- Risk: importing security-bypass posture or letting workflow outputs become truth.
- Next action: use it as a seed for a VAKS `blackbox-product-analysis` or `retrieval-query-run` skill, with explicit boundaries.
