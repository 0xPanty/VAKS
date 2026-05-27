---
type: decision
status: active
created: 2026-05-27
updated: 2026-05-27
decision: "Adopt Karpathy-simple outside, verified-action strict inside as the primary UX and implementation principle."
decision_scope:
  - ux
  - implementation-blueprint
  - architecture-principles
  - open-source-positioning
related_projects:
  - verified-action-knowledge-system
based_on:
  - "[[ARCHITECTURE_PRINCIPLES]]"
  - "[[SCHEMA]]"
  - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
  - "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
patterns:
  - "[[review-gated-compile-queue]]"
  - "[[context-pack-evidence-envelope]]"
  - "[[progressive-vault-context-loader]]"
  - "[[two-output-rule-answer-plus-knowledge-writeback]]"
anti_patterns:
  - "[[direct-compile-to-truth-layer-without-review]]"
  - "[[copying-full-second-brain-runtime-before-schema-stabilizes]]"
  - "[[auto-compiled-concept-wiki-as-verified-truth-layer]]"
outcome: adopted
verification_status: active
evidence_level: synthetic
evidence_strength: high
confidence: high
negative_evidence:
  - "If strict metadata and full architecture layers are exposed in the default user path, the system will be harder to use than Karpathy-style LLM Wiki."
  - "If first implementation tries to include every reference-library capability, it risks becoming a heavy, incoherent product stack."
replaces:
superseded_by:
migration_path:
  - "Put this principle at the top of IMPLEMENTATION_BLUEPRINT.md."
  - "Define a simple default command surface before defining optional strict fields."
  - "Make one end-to-end source-to-context-pack path work before adding runtime modules."
rollback_path:
  - "If UX becomes too complex, reduce the default surface back to raw/wiki/index/log plus manual review."
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: decision
gaps:
  - "IMPLEMENTATION_BLUEPRINT.md is not written yet."
  - "No runnable CLI/API has implemented this UX principle yet."
evidence_timeline:
  - date: 2026-05-27
    source: "subagent architecture review"
    observation: "Independent gpt-5.5 xhigh review judged the architecture conditionally stronger than individual libraries only if the default UX stays Karpathy-simple."
    effect: supports
    confidence: high
relations:
  - target: "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
    rationale: "The quality bar needs a UX constraint so capability does not become default complexity."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
    type: constrains
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
    rationale: "Included LLM Wiki stack capabilities must be hidden behind simple capture/query/lint/context operations."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[copying-full-second-brain-runtime-before-schema-stabilizes]]"
    type: risk_of
    strength: 4
    confidence: high
    evidence:
      - "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
    rationale: "Trying to implement all runtime capabilities first would leak complexity and recreate this anti-pattern."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - decision
  - ux
  - implementation-blueprint
  - open-source
---

# Karpathy-simple outside, verified-action strict inside

## AI-readable preamble

This is now a primary design decision.

The system should feel as easy as Karpathy-style LLM Wiki in normal use, while preserving stricter verified/action contracts behind review, lint, context packs, and decision records.

The architecture is conditionally stronger than individual reference libraries only if complexity stays hidden from the default user path.

## Decision

Adopt this principle:

```text
Karpathy-simple outside.
Verified-action strict inside.
```

In user-facing terms:

```text
add source
process this
what do I know about X
lint/check vault
make context pack
review recent actions
```

In backend terms:

```text
raw source
-> candidate
-> lint/review
-> verified claim / pattern / decision
-> context pack
-> action
-> feedback
```

## Why

An independent subagent review judged the architecture as **conditionally strong**:

```text
It can be stronger than any single reference library in capability.
It will not be better in UX unless the default surface stays simple.
```

The risk is not insufficient ambition. The risk is leaking architecture complexity into everyday use.

## What This Means

Default capture must stay light.

Strict schema should appear only when a node is promoted into:

```text
claim
pattern
anti-pattern
decision
implementation-note
context pack
```

Reference-library capabilities should be behind replaceable modules:

```text
llm-wiki-compiler mechanics
OpenKB long-doc / Skill Factory
obsidian-second-brain hygiene
gbrain epistemic discipline
retrieval engines
viewer/API/MCP
```

None of these should make the default user path harder than Karpathy's raw/wiki/index/log loop.

## First Blueprint Rule

The first implementation must prove one narrow end-to-end path:

```text
one source
-> one candidate
-> lint/review
-> one verified node
-> one context pack
```

Do not build the full runtime stack first.

## Blueprint Principles

1. First prove one end-to-end source-to-context-pack loop.
2. Keep default UX Karpathy-simple: capture, query, lint, context.
3. Candidate is never truth.
4. Split schema into required baseline fields and strict promotion fields.
5. Modules must obey contracts and be removable; Markdown remains runnable without them.
