---
type: review-candidate
status: pending-review
record_kind: candidate_distillation
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
retrieval_policy: orientation_only
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
created: 2026-06-06
project: verified-action-knowledge-system
scope: x-article-claude-obsidian-90-days-distillation
proposed_node_type: candidate-distillation
proposed_title: "CyrilXBT Claude Obsidian 90-Day Retrospective Candidate Distillation"
proposed_by: Codex
sources:
  - raw/articles/2026-06-06-x-cyrilxbt-claude-obsidian-90-days-source.md
  - raw/articles/2026-06-06-x-cyrilxbt-claude-obsidian-90-days-source/pasted-text.txt
related_prior_distillation:
  - outputs/review/2026-06-06-x-hamza-obsidian-second-brain-candidate-distillation.md
  - outputs/review/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-candidate-distillation.md
  - raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source.md
  - wiki/summaries/2026-05-obsidian-claude-ai-superbrain-content-factory.md
  - wiki/patterns/claude-md-index-md-navigation-layer.md
  - wiki/patterns/operational-session-capture-loop.md
evidence_level: user-provided-x-article-self-report
verification_status: unverified
candidate_reliability_note: medium for workflow failure modes; low for quantitative claims
truth_boundary: "candidate comprehension only; not reviewed knowledge; not architecture decision; not action basis"
write_scope: outputs/review only
routing_labels:
  source_kind: practitioner_x_article
  processing_lane: medium_candidate_distillation
  truth_lane: candidate_only
  project_overlay_route: confirmed_sidecar_exists
  candidate_pattern_bank: no_new_entry
  v0_2_13_trigger: no
candidate_point_labels:
  - forgotten_notes_resurface_in_context
  - specific_steering_file_compounds_output_quality
  - vault_quality_limits_agent_synthesis
  - automation_output_must_be_read_or_it_is_noise
  - five_core_workflows_before_expansion
  - connection_finder_as_activation_not_truth
  - decision_support_metrics_need_review
  - weekly_steering_update_calibrates_context
  - automated_briefs_are_operational_receipts
  - broad_vault_read_access_requires_boundary
related_project_overlay:
  - outputs/review/project_overlays/VAKS/VAKS-cyrilxbt-claude-obsidian-90-days-2026-06-06.md
reviewer:
review_result:
---

# CyrilXBT Claude Obsidian 90-Day Retrospective Candidate Distillation

## Boundary

This is a candidate distillation of a user-provided X article about using Claude
with an Obsidian vault for 90 days.

It does not modify:

```text
wiki/
SCHEMA.md
REVIEW_QUEUE.md
templates/
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

It does not connect Claude Desktop, configure Filesystem MCP, create scheduled
workflows, or grant any vault access.

## Plain-Language Takeaway

The useful part of this source is not "connect Claude to everything."

The useful part is:

```text
agent-attached vaults become useful when forgotten context resurfaces;
the steering file determines output quality;
bad notes create bad synthesis;
scheduled outputs become noise if humans do not read them;
longitudinal receipts can reveal patterns, but only after review.
```

For VAKS, this reinforces the existing architecture:

```text
Activation can surface forgotten context.
Steering files route context but are not truth.
Vault health affects output quality.
Automation output is candidate / receipt.
Review and action basis remain separate.
```

## Source Comprehension

### What The Article Is Really About

The article is a retrospective on three months of agent-attached note use. Its
main arc is:

```text
Day 1:
  Claude can read the vault, which creates a powerful but unsettling broad-access moment.

Week 1:
  Forgotten notes return in context.

Week 2:
  Morning brief becomes the first useful recurring workflow.

Week 3:
  CLAUDE.md changes from "config file" to living steering document.

Month 1:
  Manual status tracking, related-note search, blank-page starts, meeting note formatting, context re-explanation, and weekly review compilation shrink.

Month 2:
  Automations become invisible, then over-automation creates unread output noise.

Month 3:
  Accumulated reviews, daily notes, and decision logs begin surfacing self-patterns.
```

The strongest mechanism is not the specific tool stack. It is a feedback loop:

```text
vault context
-> agent-generated operational output
-> human reading / correction
-> steering file update
-> better next output
```

### What The Article Is Not

It is not:

```text
a controlled productivity study
a verified decision-quality measurement
a security review of broad filesystem access
a primary Claude Desktop / MCP documentation source
a VAKS architecture decision
a source of reviewed evidence for action basis
```

It is a useful practitioner retrospective and failure-mode source.

## Candidate Points

### 1. forgotten_notes_resurface_in_context

Candidate point:

```text
An agent connected to a readable vault can surface forgotten notes at the moment
of use, which is different from manual keyword search.
```

Source anchor:

```text
raw/articles/2026-06-06-x-cyrilxbt-claude-obsidian-90-days-source.md
raw/articles/2026-06-06-x-cyrilxbt-claude-obsidian-90-days-source/pasted-text.txt
article sections: Week 1; notes the author forgot existed resurfaced in real time
```

VAKS fit:

```text
Supports Activation Tier, context pack preparation, and retrieval-as-activation.
```

Boundary:

```text
Surfacing a note is not evidence support. The retrieved note still needs review
if it is used for a claim, decision, or action basis.
```

Route:

```text
candidate point
candidate pattern route: retrieval-is-activation-not-truth
```

### 2. specific_steering_file_compounds_output_quality

Candidate point:

```text
A specific, frequently updated steering file can improve agent output quality
across recurring workflows because it gives stable project, priority, voice,
and boundary context.
```

Source anchor:

```text
pasted text sections: Week 3; What I Would Do Differently Starting Today
```

VAKS fit:

```text
Reinforces AGENTS.md, handoff files, and CLAUDE.md + index.md Navigation Layer.
```

Boundary:

```text
The steering file routes context. It does not become truth, reviewed evidence,
or permission to act.
```

Route:

```text
candidate point
candidate pattern route: claude-md-index-md-navigation-layer
possible support for project-state-next-action-contract
```

### 3. vault_quality_limits_agent_synthesis

Candidate point:

```text
Agent synthesis quality is limited by vault quality; inconsistent, copied, or
underprocessed notes produce weaker synthesis.
```

Source anchor:

```text
pasted text section: Month 1: What Surprised Me; vault quality problem surfaced immediately
```

VAKS fit:

```text
Supports maintenance manifests, source intake boundaries, and candidate
comprehension before review.
```

Boundary:

```text
Vault cleanup improves usability but does not by itself create reviewed truth.
```

Route:

```text
candidate point
possible future route: vault health as output-quality diagnostic
```

### 4. automation_output_must_be_read_or_it_is_noise

Candidate point:

```text
Automated outputs that exceed the user's ability to read and act on them become
automated noise rather than productivity gains.
```

Source anchor:

```text
pasted text section: Month 2: The Failure That Taught Me the Most
```

VAKS fit:

```text
Highly relevant to VAKS automation restraint and lazy strictness.
```

Boundary:

```text
This argues against automatic scheduled synthesis as a default. It does not
prove that all automation is bad.
```

Route:

```text
candidate point
possible future pattern if repeated: automation-output-readability-budget
```

### 5. five_core_workflows_before_expansion

Candidate point:

```text
A small set of recurring workflows may produce more usable value than many
scheduled workflows because it keeps review load within human capacity.
```

Source anchor:

```text
pasted text sections: Month 2 failure; What I Would Do Differently
```

VAKS fit:

```text
Supports simple-first tooling and staged workflow adoption.
```

Boundary:

```text
The five named workflows are this author's experience, not a universal optimal
set or VAKS required workflow list.
```

Route:

```text
candidate point
candidate pattern route: simple-first-retrieval-baseline
possible support for skills-and-prompts-as-visible-files
```

### 6. connection_finder_as_activation_not_truth

Candidate point:

```text
Agent-suggested connections can reveal useful associations between notes, but
they should be treated as activation suggestions until reviewed.
```

Source anchor:

```text
pasted text sections: Month 1 connections; What I Would Do Differently; Trust the connection finder
```

VAKS fit:

```text
Directly supports Association Neighborhood Activation without turning suggested
links into reviewed relations.
```

Boundary:

```text
Non-obvious connections can be insightful and still unsupported. They require
review before becoming strong relations or action basis.
```

Route:

```text
candidate point
candidate pattern route: retrieval-is-activation-not-truth
candidate pattern route: graph-and-ontology-as-candidate-context
```

### 7. decision_support_metrics_need_review

Candidate point:

```text
Decision-support prompts can use past notes and decision logs to prepare better
context, but reported outcome metrics need review before they guide policy.
```

Source anchor:

```text
pasted text section: Month 3; fast decisions had a 40% higher revision or reversal rate
```

VAKS fit:

```text
Supports decision outcome calibration and Use Ledger ideas, with a strong
evidence boundary.
```

Boundary:

```text
The 40% figure is a self-reported metric from the source. It cannot be used as
action evidence without source data, definitions, and review.
```

Route:

```text
candidate point
possible support for FEEDBACK.md / decision outcome calibration
```

### 8. weekly_steering_update_calibrates_context

Candidate point:

```text
Regularly updating active priorities and project state keeps recurring agent
outputs aligned with the current week.
```

Source anchor:

```text
pasted text section: Review and update CLAUDE.md every Monday
```

VAKS fit:

```text
Supports handoff freshness, Activation Tier, and project-state next-action
contracts.
```

Boundary:

```text
Freshness improves scope fit. It does not increase truth confidence.
```

Route:

```text
candidate point
candidate pattern route: claude-md-index-md-navigation-layer
possible support for project-state-next-action-contract
```

### 9. automated_briefs_are_operational_receipts

Candidate point:

```text
Morning briefs, project health reports, weekly reviews, and decision logs can
serve as operational receipts that help humans inspect work patterns over time.
```

Source anchor:

```text
pasted text sections: Week 2; Month 2; Month 3
```

VAKS fit:

```text
Supports operational-session-capture-loop and feedback-ledger-style learning.
```

Boundary:

```text
Operational receipts are not reviewed knowledge. They may create review
pressure or activation hints, not truth mutation.
```

Route:

```text
candidate point
candidate pattern route: operational-session-capture-loop
candidate pattern route: memory-granularity-and-quarantine
```

### 10. broad_vault_read_access_requires_boundary

Candidate point:

```text
Giving an agent access to every note in a vault can be powerful but should be
treated as an access-boundary decision, not a casual productivity setting.
```

Source anchor:

```text
pasted text section: Day 1; author felt unsettled when Claude could read every note
```

VAKS fit:

```text
Reinforces agent tool access tiering, path-scoped writes, and sensitive-note
boundaries.
```

Boundary:

```text
This article describes broad read access. It does not justify broad write
access, sensitive data access, or unattended automation.
```

Route:

```text
candidate point
candidate pattern route: agent-tool-access-tiering
candidate pattern route: path-scoped-agent-output-writes
```

## Candidate Pattern Bank Decision

Do not create a new Candidate Pattern Bank entry from this one article.

Reason:

```text
Most useful ideas already route to existing patterns:
retrieval-is-activation-not-truth
file-first-agent-workbench
skills-and-prompts-as-visible-files
memory-granularity-and-quarantine
simple-first-retrieval-baseline
graph-and-ontology-as-candidate-context
agent-tool-access-tiering
path-scoped-agent-output-writes
claude-md-index-md-navigation-layer
operational-session-capture-loop
```

Possible future patterns only if more sources repeat them:

```text
automation-output-readability-budget
vault-quality-limits-agent-synthesis
```

For now they stay candidate points.

## Candidate Routing Hints (Not Project Overlay)

The project-scoped borrowing list is written as a separate candidate sidecar:

```text
outputs/review/project_overlays/VAKS/VAKS-cyrilxbt-claude-obsidian-90-days-2026-06-06.md
```

It is not a schema, not a formal Project Lens object, and not an action basis.

## Candidate Routing Hints

Candidate routing hints:

```text
1. Forgotten material resurfacing is a core activation value.
2. A specific steering file is worth more than a generic instruction file.
3. Vault quality affects agent synthesis quality.
4. Generated outputs need a human attention budget.
5. Core recurring workflows should stay few until proven useful.
6. Connection suggestions are activation candidates, not reviewed relations.
7. Longitudinal operational receipts can reveal patterns for review.
```

## Candidate Boundary Notes

Candidate boundaries:

```text
1. Broad vault read access as a default.
2. Broad write access from a productivity story.
3. Self-reported hours saved as evidence.
4. Self-reported decision metrics as policy evidence.
5. Five workflows as mandatory VAKS workflow design.
6. Morning briefs as action-ready documents.
7. Connection finder output as reviewed relations.
8. CLAUDE.md as truth authority.
```

## Relation To The Previous Two X Articles

This article is the third piece in the current Obsidian / agent-vault cluster:

```text
Hamza Obsidian article:
  focuses on note surfacing, simple capture, own-words processing, and links as activation.

Zaimiri Hermes + Obsidian article:
  focuses on agent output zones, visible receipts, skills, cron prompts, and scoped filesystem access.

CyrilXBT Claude + Obsidian article:
  focuses on 90-day operational use, steering-file quality, over-automation noise, vault quality, and longitudinal receipts.
```

Together they point to the same VAKS-safe reading:

```text
files and links help activation;
agent outputs need quarantine;
human review stays the gate;
automation must fit human attention;
metrics and decisions need later evidence-aware review.
```

## v0.2.13 Trigger Check

Does this source currently trigger v0.2.13?

```text
action_basis: no
significant promotion: no
significant decision: no
architecture absorption: no
risk-sensitive answer relied on for action: no
explicit "is this enough to act" question: no
```

Result:

```text
v0.2.13 not triggered
```

If a future window wants to use this source to justify Claude/MCP access,
scheduled workflows, decision support policy, or action-basis behavior, then
v0.2.13 must run:

```text
claim
anchored evidence
non-circular warrant
scope / assumptions
known challenges / gaps
residual risk
```

## Suggested Next Step

Keep this as candidate-only.

If more longitudinal agent-vault sources arrive, cluster them around:

```text
automation-output-readability-budget
vault-quality-limits-agent-synthesis
steering-file-freshness
connection-finder-as-activation
operational-receipts-for-pattern-review
broad-read-access-boundary
```

Then decide whether any one has enough repeated mechanism value to become a
Candidate Pattern Bank entry or reviewed architecture note.

