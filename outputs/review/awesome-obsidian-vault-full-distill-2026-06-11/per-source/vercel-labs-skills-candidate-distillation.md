---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/vercel-labs-skills-source.md
  - raw/repos/2026-06-11-obsidian-pkm-vault-awesome-obsidian-vault-source.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - agent_skill_runtime_boundary
possible_project_refs:
  - verified-action-knowledge-system
borrow_value: strong
borrow_order: P1
fit_layer:
  - agent-boundary
  - skill-registry
  - tool-safety
  - source-hygiene
not_fit_layer:
  - reviewed-knowledge
  - action-basis
avoid:
  - "Do not allow automatic skill install, skill output, or agent runtime to mutate reviewed knowledge."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Only when the task explicitly targets this source or its VAKS fit layer."
  support_when: "When designing agent_skill_runtime_boundary or comparing related vault/source patterns."
  risk_when: "When this source polish, popularity, automation, or domain taxonomy could be mistaken for VAKS authority."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/vercel-labs-skills-source.md
tags:
  - candidate-only
  - per-source-distillation
  - awesome-obsidian-vault
  - "dev-design"
---

# Candidate Distillation: skills — Vercel labs

## Boundary

This is a per-original-source candidate distillation. It can guide attention and future review. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## Source

```yaml
source_card: raw/repos/2026-06-11-awesome-obsidian-vault/vercel-labs-skills-source.md
repo_key: "vercel-labs/skills"
vault_url: "https://github.com/vercel-labs/skills"
web_url: "https://www.skills.sh/"
head_or_version: "be0dd25b4a8665894a56f45ef582cc02ca802c39"
readme_status: "ok:README.md"
```

## VAKS Fit

```yaml
borrow_value: strong
borrow_order: P1
routing_hint: agent_skill_runtime_boundary
fit_layer:
  - agent-boundary
  - skill-registry
  - tool-safety
  - source-hygiene
not_fit_layer:
  - reviewed-knowledge
  - action-basis
```

## Strongest Borrow

SKILL metadata, provider abstraction, lock/install flow, safer frontmatter parsing

## What To Avoid

Do not allow automatic skill install, skill output, or agent runtime to mutate reviewed knowledge.

## Candidate Points

1. This source may help VAKS at the layer(s) listed in `fit_layer`, but only as candidate orientation until a later evidence-aware review.
2. Its current metadata/README/tree sample should be treated as source identity and design hints, not independent support.
3. If this source becomes relevant to an implementation task, reopen the original repo/source and inspect exact files before borrowing details.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Boundary |
|---|---|---|
| Capture / Source Ingest | Source identity and structure can inform capture/source-card design when relevant. | Raw source identity is not support. |
| Understand | README/tree shape can suggest candidate points. | Summary is not reviewed knowledge. |
| Review | May become review input if a specific pattern is useful. | Needs source anchors and evidence packet before promotion. |
| Connect | Can be linked as candidate_relation only. | No auto reviewed relation. |
| Act and Learn | Not action-ready. | `action_basis_allowed: false`. |

## Reopen Trigger

Reopen this source when VAKS work touches:

```	ext
agent_skill_runtime_boundary
```

or when the user asks for a deeper review of this exact repo/source.
