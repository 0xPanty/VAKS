---
type: pattern
status: candidate
source:
  - [[2026-05-26-obsidian-second-brain-source]]
related:
  - [[graph-insights-health-check]]
confidence: high
adoption_layer: health
tags:
  - health-check
  - maintenance
  - validation
---

# Vault Health Check As Maintenance Contract

## Pattern

A knowledge vault needs routine health checks, not only search.

`obsidian-second-brain` ships a `vault_health.py` that detects duplicate notes, orphans, stale tasks, missing frontmatter, empty folders, broken links, and template leftovers. Its command layer extends this idea to contradictions, concept gaps, and stale claims.

## Why It Matters

Our资料库的健康问题会更偏 verified knowledge：

- claim without source
- pattern without evidence
- anti-pattern without failure condition
- decision without alternatives
- source without status
- stale source on fast-moving topic
- output not linked back to concepts
- claim contradicted but not marked

这些问题不靠肉眼能长期维护。

## Our Adaptation

After `SCHEMA.md`, create a local health checker that reports:

```text
critical:
  - accepted decision without evidence
  - verified claim without source
  - conflicting accepted claims

warning:
  - single-source pattern marked adopted
  - missing negative evidence
  - stale next_review
  - source_status missing

info:
  - orphan source
  - low-relation node
  - output not backlinked
```

## Risk

Health check should report before auto-fixing.

Automatic mutation should wait until schema, tests, and diff review are stable.

