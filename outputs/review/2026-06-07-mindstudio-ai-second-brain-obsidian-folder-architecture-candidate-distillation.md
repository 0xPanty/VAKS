---
record_kind: candidate_distillation
type: review-candidate
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
derived_from:
  - raw/articles/2026-06-07-mindstudio-ai-second-brain-obsidian-vault-folder-architecture-source.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
project: verified-action-knowledge-system
scope: mindstudio-ai-second-brain-obsidian-folder-architecture-distillation
source_checked_at: 2026-06-07
borrow_value: medium
borrow_order:
  - "P1: raw -> processed -> wiki as a plain source-state spine"
  - "P1: agents.md as inspectable behavior spec"
  - "P1: index.md and log.md as pointer and operation trace"
  - "P2: journal and CRM as optional use-context modules"
  - "P2: question-driven wiki growth as candidate synthesis"
  - "P3: Web Clipper and hourly automation as later tool-layer references"
avoid:
  - "Do not treat the article's folder count as schema."
  - "Do not borrow generated wiki pages as reviewed knowledge."
  - "Do not default to hourly Codex automation."
  - "Do not default to auto commit/push."
  - "Do not put journal/CRM into VAKS core before privacy and scope boundaries exist."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS source-state, project-local behavior manuals, or Obsidian workbench UX."
  support_when: "Discussing AI second-brain folder structures and simple Obsidian implementation choices."
  risk_when: "Any proposal treats generated wiki, journal/CRM, automation, or index/log as truth/action authority."
  cold_references:
    - raw/articles/2026-06-07-mindstudio-ai-second-brain-obsidian-vault-folder-architecture-source.md
routing_hint:
  - source-intake
  - project-local-manual
  - activation-index
  - operation-log
  - optional-use-context-modules
possible_project_refs:
  - SOURCE_INTAKE.md
  - DEV_CONTEXT.md
  - MEMORY_TIER.md
  - FEEDBACK.md
  - outputs/review/project_overlays/VAKS/VAKS-mindstudio-ai-second-brain-obsidian-folder-architecture-2026-06-07.md
point_anchor_refs:
  - source_ref: raw/articles/2026-06-07-mindstudio-ai-second-brain-obsidian-vault-folder-architecture-source.md
    selector_type: web-lines
    selector_value: turn0view0:45-49
  - source_ref: raw/articles/2026-06-07-mindstudio-ai-second-brain-obsidian-vault-folder-architecture-source.md
    selector_type: web-lines
    selector_value: turn0view0:76-84
  - source_ref: raw/articles/2026-06-07-mindstudio-ai-second-brain-obsidian-vault-folder-architecture-source.md
    selector_type: web-lines
    selector_value: turn0view0:107-141
tags:
  - candidate
  - provisional
  - article-distillation
  - mindstudio
  - obsidian
borrow_tags:
  - P1/raw_processed_wiki_state_spine
  - P1/agents_md_as_behavior_spec
  - P1/index_log_as_navigation_and_trace
  - P2/journal_crm_as_optional_use_context
  - P2/question_generated_wiki_as_candidate_synthesis
  - P3/web_clipper_hourly_automation_as_tool_reference
do_not_borrow_tags:
  - avoid/folder_count_as_schema
  - avoid/generated_wiki_as_reviewed_truth
  - avoid/hourly_automation_default
  - avoid/auto_commit_push_default
  - avoid/journal_crm_as_core_without_privacy_boundary
---

# MindStudio AI Second Brain Folder Architecture Candidate Distillation

## Boundary

This is candidate orientation from a public MindStudio article.

It is not reviewed knowledge, not a VAKS architecture decision, not a formal pattern, and not action basis.

It does not enable Obsidian Web Clipper, scheduled Codex automation, journal/CRM modules, GitHub sync, or agent vault write access.

## Plain-Language Takeaway

说人话：

```text
这篇文章的价值是把 AI Obsidian vault 讲得很简单：

资料先丢 raw；
处理完移到 processed；
AI 生成 wiki；
journal/CRM 是使用场景；
agents.md 管 agent 行为；
index.md 帮 agent 找东西；
log.md 记 agent 做了什么。
```

对 VAKS 来说，能借的是“文件夹和文件各司其职”的直觉。

不能借的是：

```text
生成的 wiki = 真知识
小时级自动处理 = 默认
自动 commit/push = 默认
journal/CRM = 核心层
7 folders = schema
```

## 借鉴标签

```yaml
P1:
  - raw_processed_wiki_state_spine
  - agents_md_as_behavior_spec
  - index_log_as_navigation_and_trace
P2:
  - journal_crm_as_optional_use_context
  - question_generated_wiki_as_candidate_synthesis
P3:
  - web_clipper_hourly_automation_as_tool_reference
avoid:
  - folder_count_as_schema
  - generated_wiki_as_reviewed_truth
  - hourly_automation_default
  - auto_commit_push_default
  - journal_crm_as_core_without_privacy_boundary
```

## Source Comprehension

### What The Article Is Really About

The article argues that an AI-friendly Obsidian vault can stay simple if its folders and root files encode workflow state:

```text
/raw
  unprocessed source intake

/raw/processed
  already-ingested source trail

/wiki
  AI-generated knowledge pages and cross-links

/journal
  dated personal reflection grounded in wiki/journal/CRM context

/crm
  named markdown contact records

agents.md
  behavior spec for the agent

index.md
  pointer/catalog layer

log.md
  operation trace
```

The strongest mechanism is:

```text
capture stays easy;
processing state is visible;
agent behavior is editable;
navigation and operation traces are first-class files;
generated synthesis grows but remains traceable to sources.
```

### What The Article Is Not

It is not:

```text
a verified architecture benchmark
a security review
a privacy model
a VAKS schema proposal
a reason to schedule Codex automation by default
a reason to auto-commit or auto-push VAKS changes
```

The article is useful as a design explanation and candidate pattern source.

## Candidate Points

### 1. raw_processed_wiki_state_spine

Candidate point:

```text
Separating unprocessed raw sources, processed source trail, and generated wiki
pages gives an AI vault visible workflow state without a database.
```

Source anchor:

```text
web lines 54-90
```

VAKS fit:

```text
This reinforces VAKS source-state separation, but VAKS should map it to:
raw/source card -> candidate distillation -> review -> reviewed/action basis.
```

Boundary:

```text
`/raw/processed` is a practical state marker. It does not prove source quality or
review status.
```

Route:

```text
candidate point
possible future support for source intake state UX
```

### 2. processed_as_dedupe_and_audit_trail

Candidate point:

```text
Moving or marking processed sources prevents repeated ingestion and preserves a
path back to the original input when generated wiki pages look wrong.
```

Source anchor:

```text
web lines 80-84
```

VAKS fit:

```text
Strong fit for intake ledger, manifest, and source hash checks.
```

Boundary:

```text
Processed means handled, not reviewed, trusted, or action-ready.
```

Route:

```text
candidate point
possible route: processed-state-not-authority
```

### 3. generated_wiki_is_candidate_synthesis

Candidate point:

```text
AI-generated wiki pages can make source material reusable by extracting
concepts, entities, tools, and questions into linked notes.
```

Source anchor:

```text
web lines 85-90
```

VAKS fit:

```text
Useful for Understand / Candidate Comprehension.
```

Boundary:

```text
In VAKS, generated wiki pages cannot be treated as reviewed knowledge. They are
candidate synthesis until review.
```

Route:

```text
candidate point
risk route: generated-wiki-as-reviewed-truth
```

### 4. journal_and_crm_are_use_context_modules

Candidate point:

```text
Journal and CRM folders can make personal responses more grounded by giving the
agent dated reflection and contact context.
```

Source anchor:

```text
web lines 91-106
```

VAKS fit:

```text
Useful as optional project/user context modules, especially for future workbench
or personal-use layer.
```

Boundary:

```text
Journal and CRM data are sensitive use-context records. They should not enter
VAKS core truth or default retrieval without scope and privacy rules.
```

Route:

```text
candidate point
possible future project/workbench overlay only
```

### 5. agents_md_as_behavior_spec

Candidate point:

```text
A project-local markdown instruction file can act like an inspectable behavior
spec for agent operations.
```

Source anchor:

```text
web lines 107-137
```

VAKS fit:

```text
Directly reinforces VAKS AGENTS.md, handoffs, local manuals, and skill files.
```

Boundary:

```text
Instruction files govern behavior, but they are not evidence, reviewed truth, or
permission to act outside the user's explicit request.
```

Route:

```text
candidate point
possible route: project-local-manual-as-agent-api
```

### 6. index_log_as_navigation_and_trace

Candidate point:

```text
An index gives the agent a pointer layer; a log gives both human and agent an
operation history.
```

Source anchor:

```text
web lines 138-141
```

VAKS fit:

```text
Strong fit for Activation Tier, handoff recovery, source intake ledgers, and
operation receipts.
```

Boundary:

```text
Index and log are navigation and trace. They are not support, truth, confidence,
or reviewed relation.
```

Route:

```text
candidate point
possible route: pointer-index-and-operation-log
```

### 7. continuous_retrieval_automation_is_a_later_gate

Candidate point:

```text
Continuous or scheduled processing can reduce manual retrieval burden, but it
also raises cost, duplication, privacy, and false-authority risk.
```

Source anchor:

```text
web lines 144-149
web lines 182-190
```

VAKS fit:

```text
Useful as a pressure point for future automation, not as a default.
```

Boundary:

```text
VAKS ordinary capture stays explicit. Scheduled automation requires separate
approval, clear source scope, write boundaries, and review/promotion gates.
```

Route:

```text
candidate point
risk route: hourly-automation-default
```

### 8. versioning_is_safety_not_approval

Candidate point:

```text
Git backup can make agent edits recoverable and portable across machines or
agents.
```

Source anchor:

```text
web lines 176-179
```

VAKS fit:

```text
Supports repo discipline, sync/hash, and rollback thinking.
```

Boundary:

```text
Commit/push is safety and recovery, not review approval or truth promotion.
VAKS should not auto-commit or auto-push by default.
```

Route:

```text
candidate point
risk route: auto-commit-push-default
```

## Candidate Pattern Bank Decision

Do not create a new reviewed pattern from this one article.

Possible future candidate pattern names if repeated by stronger sources:

```text
raw-processed-wiki-state-spine
project-local-manual-as-agent-api
pointer-index-and-operation-log
processed-state-not-authority
question-generated-candidate-note
```

For now, keep them candidate-only and project overlay scoped.

## Relation To Current VAKS Cluster

This article is a simplified companion to the implementation-level sources already being processed:

```text
AgriciDaniel/claude-obsidian:
  concrete repo with skills, hooks, retrieval, locks, tests.

MindStudio article:
  plain-language product/workflow explanation of a similar vault shape.

VAKS:
  stricter authority system that keeps raw/candidate/reviewed/action-basis separate.
```

The useful fusion is:

```text
Borrow the simplicity of the file map.
Keep the VAKS authority boundaries.
Reject automatic authority from generated wiki or automation.
```

## Open Questions

- Should VAKS eventually name a "processed" state, or keep using source cards + manifests + ledger?
- Should VAKS have a formal `log.md` equivalent, or continue using handoffs/ledgers/feedback events?
- Where would journal/CRM belong if this becomes a personal-use layer: project overlay, user context, or separate private vault?
- What exact gate would be required before scheduled intake is allowed?

## Routing Hint

Useful for:

```text
source intake UX
plain-language VAKS explanation
Obsidian vault folder design
project-local agent manuals
operation logs and index files
optional personal use-context modules
```

Not useful as:

```text
reviewed source of truth
schema authority
automation approval
privacy model
GitHub sync policy
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

If a future window uses this article to justify scheduled automation, auto commit/push, broad vault write access, journal/CRM in core, or generated wiki as reviewed knowledge, v0.2.13 must run first.
