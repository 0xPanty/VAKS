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
scope: x-article-hermes-obsidian-agent-vault-distillation
proposed_node_type: candidate-distillation
proposed_title: "Zaimiri Hermes Obsidian Vault AI Brain X Article Candidate Distillation"
proposed_by: Codex
sources:
  - raw/articles/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-source.md
  - raw/articles/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-source/pasted-text.txt
related_prior_distillation:
  - raw/articles/2026-06-04-x-hermes-self-improving-agent-source.md
  - raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source.md
  - wiki/summaries/2026-05-obsidian-claude-ai-superbrain-content-factory.md
  - wiki/patterns/path-scoped-agent-output-writes.md
  - wiki/patterns/agent-tool-access-tiering.md
  - wiki/patterns/claude-md-index-md-navigation-layer.md
evidence_level: user-provided-x-article
verification_status: unverified
candidate_reliability_note: medium for workflow boundary themes; low for exact commands and tool capability claims
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
  - markdown_vault_as_agent_receipt_layer
  - agent_output_zone_before_direct_edits
  - read_first_system_note_for_agent_context
  - scoped_filesystem_access_for_vault_tools
  - skills_as_repeatable_workflow_files
  - cron_prompt_as_operating_procedure
  - automated_outputs_need_source_receipts
  - human_review_before_project_status_or_irreversible_edits
  - secrets_stay_outside_vault
  - output_only_warmup_before_write_access
related_project_overlay:
  - outputs/review/project_overlays/VAKS/VAKS-zaimiri-hermes-obsidian-agent-2026-06-06.md
reviewer:
review_result:
---

# Zaimiri Hermes Obsidian Vault AI Brain Candidate Distillation

## Boundary

This is a candidate distillation of a user-provided X article about using Hermes
Agent with an Obsidian vault.

It does not modify:

```text
wiki/
SCHEMA.md
REVIEW_QUEUE.md
templates/
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

It does not install Hermes, configure MCP, create cron jobs, or grant any agent
write permissions.

## Plain-Language Takeaway

The useful part of this source is:

```text
agent memory should stay visible;
agent write access should start narrow;
agent output should leave receipts;
humans promote useful drafts;
automation needs explicit operating rules.
```

For VAKS, this reinforces the existing split:

```text
Obsidian / Markdown / files = readable workbench and source of operation trace.
Hermes / skills / cron = possible agent runtime and workflow executor.
Agent output = candidate or receipt, not reviewed truth.
Review / promotion / action basis = later gated path.
```

## Source Comprehension

### What The Article Is Really About

The article proposes an agent-attached vault:

```text
local Markdown vault
bounded filesystem access
read-first system note
repeatable skills
scheduled prompts
visible output receipts
human review before promotion or irreversible edits
```

Its core mechanism is not "Obsidian has folders" or "Hermes has commands." The
core mechanism is controlled agency:

```text
give the agent enough context to help;
give it a safe place to write;
make every output inspectable;
expand authority slowly.
```

### What The Article Is Not

It is not:

```text
a primary Hermes documentation source
a security review of MCP filesystem access
a verified command reference
a VAKS architecture decision
a source of reviewed evidence for action basis
```

It is a useful practitioner workflow sample.

## Candidate Points

### 1. markdown_vault_as_agent_receipt_layer

Candidate point:

```text
A Markdown vault can function as an agent-readable memory layer and a
human-readable receipt layer when agent outputs are written back as files with
visible paths.
```

Source anchor:

```text
raw/articles/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-source.md
raw/articles/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-source/pasted-text.txt
article theme: Obsidian stores context; Hermes does work; Obsidian keeps receipts
```

VAKS fit:

```text
Supports file-first-agent-workbench and visible operation trace.
```

Boundary:

```text
Receipt visibility is not evidence support or review. It only makes later review
possible.
```

Route:

```text
candidate point
candidate pattern route: file-first-agent-workbench
```

### 2. agent_output_zone_before_direct_edits

Candidate point:

```text
An agent should first write into a dedicated output zone before it is allowed to
edit project folders or permanent notes.
```

Source anchor:

```text
pasted text sections: Create a vault structure Hermes can understand; 05-HERMES-OUTPUTS; first week output-only
```

VAKS fit:

```text
Directly reinforces path-scoped-agent-output-writes.
```

Boundary:

```text
The exact folder name `05-HERMES-OUTPUTS` is not VAKS schema. The reusable idea
is write-narrow before write-wide.
```

Route:

```text
candidate point
candidate pattern route: path-scoped-agent-output-writes
candidate pattern route: agent-tool-access-tiering
```

### 3. read_first_system_note_for_agent_context

Candidate point:

```text
A short read-first system note can give an agent stable vault rules, priorities,
active projects, writing preferences, and review boundaries.
```

Source anchor:

```text
pasted text section: Add the system note Hermes should read first
```

VAKS fit:

```text
Reinforces CLAUDE.md + index.md Navigation Layer, handoff-first recovery, and
project-local AGENTS.md routing.
```

Boundary:

```text
A stale steering note can mislead the agent. It should route context, not act as
truth authority.
```

Route:

```text
candidate point
candidate pattern route: claude-md-index-md-navigation-layer
possible support for project-state-next-action-contract
```

### 4. scoped_filesystem_access_for_vault_tools

Candidate point:

```text
Filesystem access for an agent should be scoped to the vault or another explicit
workspace path rather than the whole machine.
```

Source anchor:

```text
pasted text section: Connect the vault through Filesystem MCP
```

VAKS fit:

```text
Reinforces agent access tiering and path-scoped write boundaries.
```

Boundary:

```text
This article does not validate the MCP server implementation, path traversal
behavior, permission model, or current Hermes command syntax.
```

Route:

```text
candidate point
candidate pattern route: agent-tool-access-tiering
candidate pattern route: path-scoped-agent-output-writes
```

### 5. skills_as_repeatable_workflow_files

Candidate point:

```text
Agent skills are useful when they make repeatable workflows explicit as visible
files with process steps, quality bars, and write targets.
```

Source anchor:

```text
pasted text section: Create your first Hermes skill
```

VAKS fit:

```text
Reinforces skills-and-prompts-as-visible-files and future procedural memory
quarantine.
```

Boundary:

```text
A skill file is a workflow draft or operating instruction. It is not reviewed
knowledge, and an agent should not approve its own skill changes.
```

Route:

```text
candidate point
candidate pattern route: skills-and-prompts-as-visible-files
candidate pattern route: memory-granularity-and-quarantine
```

### 6. cron_prompt_as_operating_procedure

Candidate point:

```text
Scheduled agent prompts should read like small operating procedures: name the
skill, folders to read, output path, forbidden actions, and review conditions.
```

Source anchor:

```text
pasted text section: Schedule the workflows
```

VAKS fit:

```text
Supports future automation safety and operational-session-capture-loop.
```

Boundary:

```text
This does not authorize scheduled synthesis in VAKS now. Scheduled work remains
off unless explicitly requested and bounded.
```

Route:

```text
candidate point
candidate pattern route: operational-session-capture-loop
possible future route: automation prompt contract
```

### 7. automated_outputs_need_source_receipts

Candidate point:

```text
Automated vault outputs should reference the source files they used, so humans
can inspect where the output came from.
```

Source anchor:

```text
pasted text sections: vault-morning-brief quality bar; safety rules
```

VAKS fit:

```text
Strong fit with VAKS provenance and candidate comprehension boundaries.
```

Boundary:

```text
Referencing a path is provenance, not evidence support. Specific point support
still needs later review.
```

Route:

```text
candidate point
candidate pattern route: file-first-agent-workbench
candidate pattern route: retrieval-is-activation-not-truth
```

### 8. human_review_before_project_status_or_irreversible_edits

Candidate point:

```text
Project status changes, deletions, sensitive-domain edits, and irreversible
actions should require human review even if the agent can draft or organize
notes.
```

Source anchor:

```text
pasted text sections: Human review rule; safety setup
```

VAKS fit:

```text
Reinforces lazy gates, agent memory quarantine, and action-basis separation.
```

Boundary:

```text
Human review here is process control. It still does not by itself create truth
confidence or evidence support.
```

Route:

```text
candidate point
candidate pattern route: agent-tool-access-tiering
candidate pattern route: path-scoped-agent-output-writes
```

### 9. secrets_stay_outside_vault

Candidate point:

```text
Secrets and API keys should not be stored in the knowledge vault; they belong in
runtime config or environment files with separate handling.
```

Source anchor:

```text
pasted text sections: Install Hermes; safety setup
```

VAKS fit:

```text
Supports future agent-runtime safety boundaries.
```

Boundary:

```text
This is a safety convention, not a knowledge point about Hermes capability.
```

Route:

```text
candidate point
possible route: future agent access safety checklist
```

### 10. output_only_warmup_before_write_access

Candidate point:

```text
A new vault automation should run output-only for a trial period before being
allowed to move files, edit project truth, or update permanent notes.
```

Source anchor:

```text
pasted text sections: first week output-only; add workflows slowly
```

VAKS fit:

```text
Supports staged authority and review-first automation.
```

Boundary:

```text
The "seven days" number is a practitioner suggestion, not a validated threshold.
The reusable mechanism is trial-before-authority.
```

Route:

```text
candidate point
candidate pattern route: path-scoped-agent-output-writes
candidate pattern route: agent-tool-access-tiering
```

## Candidate Pattern Bank Decision

Do not create a new Candidate Pattern Bank entry from this one article.

Reason:

```text
Most useful ideas already route to existing local patterns:
file-first-agent-workbench
skills-and-prompts-as-visible-files
memory-granularity-and-quarantine
path-scoped-agent-output-writes
agent-tool-access-tiering
claude-md-index-md-navigation-layer
operational-session-capture-loop
retrieval-is-activation-not-truth
```

Possible future pattern only if more sources repeat it:

```text
cron-prompt-as-operating-procedure
```

But for now it stays a candidate point, not a bank entry.

## Candidate Routing Hints (Not Project Overlay)

The project-scoped borrowing list is written as a separate candidate sidecar:

```text
outputs/review/project_overlays/VAKS/VAKS-zaimiri-hermes-obsidian-agent-2026-06-06.md
```

It is not a schema, not a formal Project Lens object, and not an action basis.

## Candidate Routing Hints

Candidate routing hints:

```text
1. Agent output should first land in a visible output zone.
2. Filesystem access should be path-scoped.
3. Agent workflows should be visible as files.
4. A read-first steering note can reduce repeated orientation work.
5. Scheduled prompts need explicit operating boundaries.
6. Agent outputs should cite source paths used.
7. Humans review project status edits, deletions, sensitive edits, and promotion.
```

## Candidate Boundary Notes

Candidate boundaries:

```text
1. Hermes as a required VAKS runtime.
2. The exact VAULT folder structure as VAKS schema.
3. `05-HERMES-OUTPUTS` as a mandated folder name.
4. Unverified Hermes commands as current installation instructions.
5. Cron jobs as default VAKS automation.
6. Source-path receipts as evidence support.
7. Agent-generated briefs as reviewed project truth.
8. Prompt-only permission boundaries without path enforcement.
```

## Relation To Prior Local Materials

This article aligns with prior local materials:

```text
raw/articles/2026-06-04-x-hermes-self-improving-agent-source.md
  supports Hermes-like skills and procedural memory, while keeping runtime output out of truth.

raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source.md
  supports explicit agent operation boundaries and Obsidian as activation/workbench.

wiki/summaries/2026-05-obsidian-claude-ai-superbrain-content-factory.md
  supports visible skills, CLAUDE.md-style operating notes, and human judgment gates.

wiki/patterns/path-scoped-agent-output-writes.md
  already holds the stronger local pattern for write-narrow agent access.
```

This article is lower authority than implementation reviews and primary-source
repo reviews. Its value is workflow pressure and boundary language.

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

If a future window wants to install Hermes, grant filesystem access, schedule
cron jobs, or adopt an agent write policy, then v0.2.13 must run:

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

If more Hermes / Obsidian / agent-vault sources arrive, cluster them around:

```text
agent output zone before direct edits
scoped filesystem access
read-first system note
visible skills
cron prompt operating procedure
source receipts vs evidence support
```

Then decide whether any one of those has enough repeated mechanism value to
become a Candidate Pattern Bank entry or reviewed architecture note.

