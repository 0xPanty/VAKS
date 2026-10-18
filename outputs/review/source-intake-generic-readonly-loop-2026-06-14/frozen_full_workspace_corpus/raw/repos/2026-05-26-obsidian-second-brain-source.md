---
type: source
record_kind: source_card
source_kind: github_repo
repo: eugeniughelbur/obsidian-second-brain
url: https://github.com/eugeniughelbur/obsidian-second-brain
commit: 23a0ed29afe63314c8fe0f8ff8a7d3ba5192b52c
retrieved: 2026-05-26
remote_head_verified: 2026-05-26
snapshot: raw/repos/_snapshots/obsidian-second-brain-23a0ed29afe63314c8fe0f8ff8a7d3ba5192b52c.zip
source_status: captured
evidence_level: primary-source
source_integrity:
  capture_confidence: high
verification_status: source-reviewed
tags:
  - repo
  - obsidian
  - second-brain
  - ai-first-vault
  - workflow-runtime
knowledge_status: raw
processing_tier: light
source_id: eugeniughelbur/obsidian-second-brain
source_url: https://github.com/eugeniughelbur/obsidian-second-brain
captured_at: 2026-05-26
title: eugeniughelbur/obsidian-second-brain
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---
# eugeniughelbur/obsidian-second-brain Source Record

## Repository Fact

`obsidian-second-brain` is not an Obsidian plugin. It is a Claude Code / cross-CLI skill package that operates on an Obsidian vault from outside Obsidian.

It positions itself as an evolution of Karpathy's LLM Wiki pattern: new sources should rewrite existing pages, contradictions should be reconciled, and the vault should be maintained by commands, hooks, and scheduled agents.

## Local Review

- Local clone: `C:\Users\Administrator\AppData\Local\Temp\obsidian_second_brain_probe\obsidian-second-brain`
- Local commit: `23a0ed29afe63314c8fe0f8ff8a7d3ba5192b52c`
- Remote HEAD checked on 2026-05-26 and matched local commit.

## Files Read

- `README.md`
- `architecture.md`
- `SKILL.md`
- `references/ai-first-rules.md`
- `references/vault-schema.md`
- `references/write-rules.md`
- `commands/obsidian-ingest.md`
- `commands/obsidian-reconcile.md`
- `commands/obsidian-synthesize.md`
- `commands/obsidian-health.md`
- `commands/obsidian-challenge.md`
- `commands/obsidian-emerge.md`
- `commands/obsidian-world.md`
- `commands/research-deep.md`
- `hooks/validate-ai-first.sh`
- `hooks/load_vault_context.py`
- `scripts/vault_health.py`
- `scripts/bootstrap_vault.py`

## Key Modules

- AI-first rules: note format contract for future AI retrieval.
- Vault schema: raw/wiki/index/log plus bi-temporal timelines.
- Write rules: propagation, search-before-create, section injection, soft archive.
- Commands: ingest, reconcile, synthesize, challenge, emerge, world, health, research.
- Hooks: session context loading and write-time validation.
- Health script: duplicate, orphan, broken link, stale task, missing frontmatter, template leftover checks.
- Bootstrap script: generates vault presets and operating files.

## Initial Classification

This repo is best classified as an agentic vault workflow/runtime reference.

It is useful for:

- operation rules
- vault writing discipline
- context bootstrapping
- propagation rules
- maintenance checks
- AI-first note shape

It is not sufficient as:

- verified truth layer
- source-quality model
- evidence gate
- negative-evidence system
- final schema for this资料库

