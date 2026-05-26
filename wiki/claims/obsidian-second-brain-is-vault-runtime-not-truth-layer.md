---
type: claim
status: accepted
created: 2026-05-26
claim: obsidian-second-brain is best treated as an agentic vault runtime reference, not as the verified truth layer for this资料库.
source:
  - [[2026-05-26-obsidian-second-brain-source]]
supports:
  - [[2026-05-26-obsidian-second-brain-skill-analysis]]
evidence_level: primary-source
verification_status: source-reviewed
confidence: high
tags:
  - claim
  - architecture-boundary
  - obsidian
---

# Claim: obsidian-second-brain Is Vault Runtime, Not Truth Layer

## Claim

`obsidian-second-brain` should not replace our verified knowledge architecture.

It should be used as a reference for how AI operates, writes, propagates, loads context, and checks health inside a vault.

## Evidence

The repo's strongest files are command/rule/runtime files:

- `SKILL.md`
- `references/ai-first-rules.md`
- `references/write-rules.md`
- `references/vault-schema.md`
- `commands/obsidian-ingest.md`
- `commands/obsidian-reconcile.md`
- `commands/obsidian-synthesize.md`
- `commands/obsidian-world.md`
- `hooks/validate-ai-first.sh`
- `scripts/vault_health.py`

These define how an AI should write and maintain a vault.

They do not fully define our required verified knowledge flow:

```text
source -> claim -> pattern -> anti-pattern -> decision
```

Nor do they fully implement our required trust fields:

```text
source_quality
evidence_level
negative_evidence
cross_source_count
verification_status
adoption_status
```

## Adoption Boundary

Use it to design:

- AI-first note shape
- propagation rules
- context loader
- health checker
- write-time validator

Do not use it to define:

- final claim schema
- final decision gate
- automatic truth resolution
- first-phase runtime automation

