---
type: qa
created: 2026-05-26
question: obsidian-second-brain 源码里哪些实现不变量未来落地时值得参考？
source:
  - [[2026-05-26-obsidian-second-brain-source]]
confidence: high
tags:
  - qa
  - implementation-notes
  - source-extraction
---

# obsidian-second-brain Implementation Extraction

## Purpose

This file records implementation-level takeaways so future coding does not rely on memory or re-reading the whole repo.

## Module Map

| File | What It Teaches | Borrowable Invariant |
|---|---|---|
| `references/ai-first-rules.md` | AI-readable note contract | Every durable knowledge node needs type/date/status/source/confidence and a short context preamble |
| `references/vault-schema.md` | raw/wiki/index/log and bi-temporal facts | raw is immutable, wiki is derived, index is front door, log is audit trail |
| `references/write-rules.md` | propagation and search-before-write | no note should be created without checking related nodes and indexes |
| `commands/obsidian-ingest.md` | ingest should update existing knowledge | source intake should produce candidate updates, not only new notes |
| `commands/obsidian-reconcile.md` | contradiction workflow | conflict is either resolved with evidence or marked open |
| `commands/obsidian-synthesize.md` | pattern creation from repeated evidence | repeated concepts across sources can promote to synthesis candidates |
| `commands/obsidian-health.md` | health report orchestration | scripts can detect mechanical issues; agent/human interprets semantic issues |
| `commands/obsidian-challenge.md` | red-team with vault history | future QA can cite prior decisions/failures against current plans |
| `commands/obsidian-emerge.md` | unnamed pattern detection | repeated themes should become explicit candidate patterns |
| `commands/obsidian-world.md` | progressive context loading | recovery/context pack should be level-based, not full-vault loading |
| `commands/research-deep.md` | vault-first gap research | search should start from current vault baseline, then fill gaps |
| `hooks/validate-ai-first.sh` | write-time validation | schema checks can be non-blocking first, then stricter later |
| `hooks/load_vault_context.py` | session-start context injection | avoid repeated discovery; inject minimal operating manual once |
| `scripts/vault_health.py` | mechanical health checks | duplicate/orphan/broken-link/frontmatter checks are easy first wins |
| `scripts/bootstrap_vault.py` | preset generation | useful later for creating starter vaults, not needed for core schema |

## Reusable Implementation Rules

1. Markdown/YAML remains system-of-record.

Indexes, dashboards, search caches, and generated graphs must be rebuildable from Markdown records.

2. Source ingestion produces an update plan.

Do not let the first version auto-rewrite accepted knowledge. It should emit:

```text
new nodes
candidate rewrites
candidate contradictions
candidate synthesis
required index/log updates
```

3. Validation starts as warning-only.

Like `validate-ai-first.sh`, the first health/validator layer should report schema problems without deleting or reverting user files.

4. Context loading must be deterministic.

Define a fixed read order so new windows recover the same way:

```text
purpose -> SCHEMA -> handoff -> index -> active decisions -> task-specific sources
```

5. Reconciliation needs a human gate.

Clear mechanical stale fields may be updated later, but semantic truth changes require candidate records and user review.

## Do Not Copy Directly

- The full slash-command runtime.
- Claude-specific hook wiring.
- Background `PostCompact` update behavior.
- Scheduled autonomous rewrite cycles.
- External API research pipeline as a core dependency.
- Preset folder structures.
- Kanban/task/person CRM domain model.

## Future Coding Note

When implementation begins, re-create the logic in our schema vocabulary:

```text
source
summary
claim
pattern
anti-pattern
decision
relation
health issue
context pack
```

Do not preserve the repo's personal productivity vocabulary unless it maps cleanly.

