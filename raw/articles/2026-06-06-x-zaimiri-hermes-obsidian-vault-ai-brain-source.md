---
type: source
status: source-captured
record_kind: source_card
knowledge_status: raw
retrieval_policy: source_identity_only
promotion_gate: none
lifecycle_state: source_registered
review_pressure: none
action_basis_allowed: false
truth_mutation_allowed: false
created: 2026-06-06
project: verified-action-knowledge-system
title: "Hermes Agent + Obsidian Vault = AI Brain"
source_title_raw: "Hermes Agent + Obsidian Vault = AI Brain"
source_id: x-zaimiri-hermes-obsidian-vault-ai-brain-2026-06-06
source_uri: x-post:zaimiri/hermes-obsidian-vault-ai-brain
source_url:
source_type: article
author: zaimiri
author_handle: "@zaimiri"
platform: X
captured_at: 2026-06-06
captured_by: Codex from user-provided pasted text
raw_location: raw/articles/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-source/pasted-text.txt
snapshot_ref_or_source_date: user_pasted_text_2026-06-06
why_saved: candidate intake for VAKS content/source distillation run
variant_locations:
  - raw/articles/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-source/pasted-text-variant-2026-06-06.txt
processing_tier: medium
processing_status: candidate-distilled
review_priority: normal
review_owner: Codex
source_status: active
source_family: x-hermes-obsidian-agent-vault-workflow
source_metadata_quality: partial
source_hygiene_note: "Exact X URL was not provided. Hermes commands and capability claims are recorded as source claims only and were not independently verified in this capture. Later user attachment was preserved as a same-source variant; it includes minor browser UI capture noise and omits the final period, so it does not change the candidate distillation."
key_entity_confidence:
  author_handle: high
  exact_post_url: missing
  hermes_commands: unverified
  filesystem_mcp_setup: unverified
  workflow_claims: medium
routing_labels:
  - source-provenance
  - x-article
  - hermes-agent
  - obsidian-workflow
  - agent-access
  - candidate-only
truth_boundary: "Source provenance and candidate comprehension only; not reviewed knowledge; not action basis."
candidate_relation_suggestions:
  - candidate:markdown_vault_as_agent_receipt_layer
  - candidate:agent_output_zone_before_direct_edits
  - candidate:read_first_system_note_for_agent_context
  - candidate:scoped_filesystem_access_for_vault_tools
  - candidate:skills_as_repeatable_workflow_files
  - candidate:cron_prompt_as_operating_procedure
  - candidate:automated_outputs_need_source_receipts
  - candidate:human_review_before_project_status_or_irreversible_edits
  - candidate:secrets_stay_outside_vault
  - candidate:output_only_warmup_before_write_access
related_prior_sources:
  - raw/articles/2026-06-04-x-hermes-self-improving-agent-source.md
  - raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source.md
  - wiki/summaries/2026-05-obsidian-claude-ai-superbrain-content-factory.md
related_review_output:
  - outputs/review/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-candidate-distillation.md
tags:
  - source
  - x-article
  - hermes
  - obsidian
  - agent-access
  - candidate-only
---

# X Source: Zaimiri Hermes + Obsidian Vault AI Brain Thread

## Boundary

This source card preserves a user-provided X article / thread about connecting
Hermes Agent to an Obsidian vault.

It is not reviewed knowledge. It is not a Hermes installation decision. It does
not prove that Hermes, Filesystem MCP, cron jobs, or any listed command works in
the current environment.

The raw text copy is stored at:

```text
raw/articles/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-source/pasted-text.txt
```

A later user attachment for the same source is preserved at:

```text
raw/articles/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-source/pasted-text-variant-2026-06-06.txt
```

That variant adds only browser UI capture lines at the beginning (`文章`,
`查看新帖子`, `对话`) and omits the final period from the last sentence. It
does not change the candidate distillation.

## What The Source Says

The article describes a local workflow:

```text
Obsidian stores readable Markdown context.
Hermes reads that context.
Hermes runs repeatable skills or scheduled work.
Obsidian stores the output receipts.
```

Its proposed setup includes:

```text
one Obsidian vault
one Hermes config
one bounded filesystem access path
one read-first system note
one initial Hermes skill
one scheduled morning brief
one output zone for early agent writes
```

The article's most useful design idea is not the exact folder names. It is the
write boundary:

```text
agent outputs first go to a visible output folder;
humans review and promote;
direct edits expand only after reliability is proven.
```

## Source-Useful Details

Reusable details worth routing as candidate comprehension:

- Obsidian vault as local Markdown memory layer.
- Hermes as agent runtime that can read files, use tools, run skills, and run
  cron jobs.
- Agent output should remain visible as Markdown receipts.
- Secrets belong outside the vault.
- Filesystem access should be scoped to the vault rather than the whole machine.
- A `06-SYSTEM/CLAUDE.md`-style file can act as a read-first steering note.
- Skills should be specific repeatable workflow files.
- Cron prompts should name the skill, read folders, write path, forbidden
  actions, and review conditions.
- The first week should be output-only into an agent output folder.
- Project status edits, deletions, and sensitive-domain edits need human review.
- Automated outputs should reference the source files they used.

## Do Not Treat As

Do not treat this source as:

```text
reviewed Hermes setup instructions
proof that Hermes commands are current
proof that Filesystem MCP configuration is safe for this machine
permission to grant broad agent write access
permission to schedule unattended vault rewriting
reviewed evidence for architecture absorption
action basis for installing or configuring Hermes
```

## Current Routing

This source has been routed to candidate distillation and a project overlay
sidecar only:

```text
outputs/review/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-candidate-distillation.md
outputs/review/project_overlays/VAKS-zaimiri-hermes-obsidian-agent-2026-06-06.md
```

No `wiki/` node, schema change, template change, scheduled automation, or
Hermes setup action is created by this source card.
