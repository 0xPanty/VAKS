---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/nikitavoloboev/knowledge"
repo_key: "nikitavoloboev/knowledge"
checked_commit: "a6b6210430c2668ed1a078a98e3b69f52be37bde"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/nikitavoloboev-knowledge-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: medium
borrow_order: P3
routing_hint:
  - source-semantic-drift
  - agent-workflow
  - spec-to-codex-prompt
fit_layer:
  - capture-provenance
  - maintenance
  - activation
  - risk-inhibition
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - public-vault-structure
avoid:
  - "Do not treat this current repo as an Obsidian knowledge vault."
  - "Do not copy full-permission Codex launch defaults."
  - "Do not allow browser-cookie media extraction without explicit authorization."
dev_context_hint:
  default_layer: risk
  core_only_when: "When designing stale awesome-link detection or spec-to-agent workflow boundaries."
  support_when: "When comparing lightweight task runners and execution prompts."
  risk_when: "When agent tools could auto-run, auto-commit, or read browser cookies."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/nikitavoloboev-knowledge-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - source-drift
  - agent-workflow
---

# Strong Candidate Distillation: nikitavoloboev / knowledge

## Boundary

The current repository is not a normal knowledge vault. This file treats it as
evidence of source semantic drift in the awesome list and extracts only
workflow/tooling ideas that fit VAKS. It does not import the repo's commands,
permissions, or media workflows.

## What This Source Actually Is

At the checked commit, the repo is a Go/CLI workspace with `flow` tasks,
agent-response conventions, a spec prompt generator, deployment helpers, and
experiments. It is not a Markdown knowledge garden comparable to older public
second-brain examples.

For VAKS, the biggest lesson is procedural: a curated source list can drift, so
every entry needs fresh source identity verification before distillation.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `readme.md` | Current repo is titled around Go tooling and flow tasks. | Awesome metadata can become stale. | Do not classify as a vault from list text alone. |
| `.codex/agents.md` | Requires responses to end with `notify:` or `runFlowTask:`. | Agent outputs can carry explicit next-action protocol. | VAKS should not require hidden command tokens in notes. |
| `.claude/agents.md` | Mirrors the agent workflow instructions. | Cross-agent workflow contracts can be standardized. | Contract is local to this repo. |
| `flow.toml` | Task runner for setup, run, spec generation, deploy, and media conversion. | Project commands can be declared as a routable task surface. | Some tasks have privacy/credential risks. |
| `cli/spec/README.md` | Generates Codex-oriented execution prompts from Markdown specs and can launch Codex. | Specs can be the source of an execution prompt. | Full-permission launch is not a VAKS default. |
| `try/dockerlayers/readme.md` | Docker layer explorer with examples and fixture-style reports. | Executable examples/tests can document behavior. | Test output is diagnostic, not truth review. |

## Strong Borrow Points

1. **Source semantic drift must be first-class in intake.**  
   The awesome-list label suggests a knowledge resource, but the current repo is
   a tooling workspace. VAKS should keep a `source_identity_checked_at` /
   `source_drift` note for curated-list imports.

2. **Spec-to-agent prompts are useful as activation artifacts.**  
   The `spec` CLI turns Markdown specs into Codex-oriented prompts. VAKS can
   borrow the idea for context packs: a reviewed project spec can generate an
   execution prompt, but only after action-basis gates.

3. **Agent workflow outputs should be explicit and reviewable.**  
   The `notify:` / `runFlowTask:` convention makes follow-up intent machine
   visible. VAKS can borrow explicit next-action markers, but should keep them
   as candidate/action-planning metadata, not automatic execution.

4. **Task runner manifests help keep commands discoverable.**  
   `flow.toml` makes project commands visible. VAKS can use this as inspiration
   for local helper command registries, with permission and safety flags.

5. **Privacy hazards belong in the distillation.**  
   Media conversion notes reference browser cookie behavior. This should land as
   a risk/inhibition borrow: any future VAKS ingestion helper must require
   explicit authorization before reading private browser state.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Drift check against current HEAD. | Source identity audit. |
| Activation | Spec-to-prompt generation. | Context-pack prompt projection. |
| Decision / Action | `runFlowTask` style explicit follow-up. | Human-approved action marker. |
| Maintenance | Task manifest and tests-as-docs. | Helper registry and diagnostics. |
| Risk / Inhibition | Full permissions, cookies, auto-commit risks. | Deny-by-default policy flags. |

## Local De-Dup / Collision

This collides with agent/runtime sources more than Obsidian vault sources:

- It is closer to workflow/project automation than to Kepano, Obsidian Hub, or
  public vault templates.
- It overlaps with VAKS agent-memory quarantine and action-basis gates.

The unique borrow is the intake-level drift warning plus spec-to-agent prompt
projection.

## Anti-Borrow

- Do not copy "launch Codex with full permissions" as an ordinary workflow.
- Do not permit auto-commit or deploy tasks from note activation alone.
- Do not read Safari/Chrome cookies for media conversion unless explicitly
  authorized and locally allowed.
- Do not treat this repo as evidence for Obsidian note architecture.

## Candidate Tags

```yaml
domain: source_drift_and_agent_workflow
problem: curated_source_list_entry_no_longer_matches_current_repository
pattern:
  - source-identity-drift-check
  - spec-to-agent-prompt
  - explicit-next-action-marker
  - task-runner-manifest
  - privacy-risk-distillation
maturity: active-tooling-workspace
problem_fit: 3
reuse_value: 3
implementation_cost: 3
integration_fit: 3
evidence_strength: 4
reversibility: 5
```

## Fusion Judgment

Borrow moderately as a drift and workflow caution. Do not borrow it as a
knowledge-vault structure.
