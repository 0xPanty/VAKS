---
type: decision
status: active
created: 2026-05-27
updated: 2026-05-27
decision: "Use Karpathy-style LLM Wiki as the main operating spine, with verified-action strictness as the inner kernel and other libraries as modular extensions."
decision_scope:
  - architecture-spine
  - ux
  - implementation-blueprint
  - open-source-positioning
related_projects:
  - verified-action-knowledge-system
based_on:
  - "[[2026-04-04-karpathy-llm-wiki-pattern]]"
  - "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
  - "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
  - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
patterns:
  - "[[review-gated-compile-queue]]"
  - "[[context-pack-evidence-envelope]]"
  - "[[wiki-foundation-generator-surface-separation]]"
  - "[[knowledge-to-agent-skill-factory]]"
anti_patterns:
  - "[[copying-full-second-brain-runtime-before-schema-stabilizes]]"
  - "[[generic-concept-schema-as-truth-layer]]"
  - "[[auto-compiled-concept-wiki-as-verified-truth-layer]]"
outcome: adopted
verification_status: active
evidence_level: synthetic
evidence_strength: high
confidence: high
negative_evidence:
  - "Using OpenKB, gbrain, or obsidian-second-brain as the main skeleton would make the default open-source entry heavier."
  - "Using every reference design as equal architecture would produce a confusing hybrid."
replaces:
superseded_by:
migration_path:
  - "Expose raw/wiki/index/log style as the default vault shape."
  - "Keep verified-action schema behind review and promotion."
  - "Treat llm-wiki-compiler, OpenKB, obsidian-second-brain, gbrain, and retrieval tools as replaceable modules."
  - "Write IMPLEMENTATION_BLUEPRINT.md around one simple spine and optional modules."
rollback_path:
  - "If Karpathy spine proves too weak, keep raw/wiki compatibility while adding a minimal CLI wrapper rather than replacing the user-facing model."
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: decision
gaps:
  - "IMPLEMENTATION_BLUEPRINT.md still needs to turn this into concrete stages."
  - "No runnable CLI command surface exists yet."
evidence_timeline:
  - date: 2026-05-27
    source: "architecture discussion and subagent review"
    observation: "The strongest route is a single Karpathy-simple skeleton with strict verified/action internals and modular references."
    effect: supports
    confidence: high
relations:
  - target: "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
    type: implements
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-karpathy-spine-modular-extensions]]"
    rationale: "The spine decision turns the UX principle into an architecture selection."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
    type: constrains
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-karpathy-spine-modular-extensions]]"
    rationale: "LLM Wiki stack capabilities are included only as long as they preserve the Karpathy-simple operating spine."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[2026-05-27-openkb-as-module-reference]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-karpathy-spine-modular-extensions]]"
    rationale: "OpenKB remains a module reference rather than the main skeleton."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - decision
  - architecture-spine
  - karpathy-simple
  - modular-extensions
---

# Karpathy Spine, Modular Extensions

## AI-readable preamble

The architecture spine is now selected.

Default user experience and open-source entry should follow Karpathy-style LLM Wiki: raw, wiki, index, log, ingest, query, lint. Verified-action strictness lives behind review and promotion. Other libraries provide modular extensions, not competing skeletons.

This prevents the system from becoming a pile of good ideas with no single center.

## Decision

Use this structure:

```text
Main spine:
  Karpathy-style LLM Wiki
  raw / wiki / index / log / ingest / query / lint

Inner kernel:
  Verified Action Knowledge System
  review gate / evidence / relations / decision / context pack / feedback

Modular extensions:
  llm-wiki-compiler
  OpenKB
  obsidian-second-brain
  gbrain
  retrieval tools
  viewer/API/MCP
```

## In Plain Words

Pick one body.

Use Karpathy as the body because it is simple and understandable.

Use our verified-action layer as the organs because it makes knowledge trustworthy and actionable.

Use the other libraries as tools and limbs because each is strong at a specific job.

## What Each Reference Contributes

```text
Karpathy:
  main skeleton and default UX

llm-wiki-compiler:
  review queue, provenance, lint, context pack, MCP/viewer mechanics

OpenKB:
  long-doc ingest, Skill Factory, path-scoped writes, hash registry

obsidian-second-brain:
  AI-readable preamble, propagation discipline, context loading, health check

gbrain:
  fact/take/hypothesis/bet/decision, holder, evidence timeline, gaps
```

## What This Forbids

Do not make every reference an equal root architecture.

Do not expose verified metadata in the default capture path.

Do not let OpenKB concept schema, gbrain runtime, or obsidian-second-brain background automation replace the spine.

Do not start implementation by building all modules.

## Blueprint Implication

`IMPLEMENTATION_BLUEPRINT.md` must start with:

```text
1. Karpathy-simple operating spine.
2. One source-to-context-pack verified loop.
3. Optional modules only after the loop works.
```

The first runnable version should be easy to explain in one sentence:

```text
Add raw material, compile reviewed knowledge, ask with evidence, export context for action.
```
