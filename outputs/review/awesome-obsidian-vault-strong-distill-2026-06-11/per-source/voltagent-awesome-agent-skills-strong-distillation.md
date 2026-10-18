---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/VoltAgent/awesome-agent-skills"
repo_key: "VoltAgent/awesome-agent-skills"
checked_commit: "0e6e58985eb75a2cf7b2cbf4bc518f1bd4ef1210"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/voltagent-awesome-agent-skills-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/voltagent-awesome-agent-skills-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/voltagent-awesome-agent-skills-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
borrow_order: P1
routing_hint:
  - agent_skill_registry
  - source_hygiene
fit_layer:
  - agent-boundary
  - skill-registry
  - source-ingest
  - source-hygiene
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-skill-install
avoid:
  - "Do not treat a curated-list entry, popularity, badge, or skill count as review evidence."
  - "Do not let external skill descriptions become VAKS reviewed claims."
  - "Do not import third-party skills into an active agent runtime without a separate safety gate."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing a VAKS agent-skill registry, external-source registry, or quarantine rule for future agent/MCP memory writes."
  support_when: "When comparing candidate registry governance, taxonomy, quality-bar language, and source-hygiene warnings."
  risk_when: "When a list entry, official/team label, sponsor placement, or community adoption could be mistaken for safety or truth."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/voltagent-awesome-agent-skills-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/voltagent-awesome-agent-skills-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - agent-skills
---

# Strong Candidate Distillation: VoltAgent / awesome-agent-skills

## Boundary

This is a strong candidate distillation, not reviewed knowledge. It may guide
future VAKS design, but it cannot create reviewed relations, truth confidence,
architecture adoption, or action basis.

## What This Source Actually Is

This repo is a curated registry of agent skills. The repository itself contains
a large `README.md` registry and a short `CONTRIBUTING.md`; it does not contain
the skills themselves. Its strongest value for VAKS is governance shape:
how to list external agent capabilities without claiming ownership,
endorsement, safety, or execution readiness.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Large categorized registry of official/team and community skills, plus a table of agent-specific skill paths. | Shows how a cross-agent registry can preserve source identity, category, short function, and target environment in one surface. | Registry entry is provenance/routing only. |
| `README.md` security notice | The registry warns that listed skills may include unsafe content and are not audited. | VAKS should make warning language first-class for candidate external capabilities. | Warning is not a review result. |
| `README.md` quality standards | Criteria cover metadata quality, specific descriptions, and scoped tool declarations. | Useful for future VAKS source-card lint and agent-skill intake gates. | Criteria are intake heuristics, not truth confidence. |
| `CONTRIBUTING.md` entry format | Entries use `author/skill-name`, link, and short description. | Borrow a compact source identity format for candidate registries. | Link existence does not mean usable source. |
| `CONTRIBUTING.md` requirements | Requires public repo, docs, author/org prefix, short description, and real usage. | VAKS can require minimum provenance before listing external tools/sources in a workbench. | Real usage is still weak evidence, not safety. |

## Strong Borrow Points

1. **Registry is a routing layer, not an authority layer.**  
   This matches VAKS: external source lists can help activation and discovery,
   but must stay outside reviewed knowledge. The registry pattern should map to
   `source-ingest`, `activation`, and `agent-boundary`, never `wiki/claims`.

2. **Every entry should preserve author/source identity.**  
   The `author/skill-name` style is worth adapting into VAKS source cards and
   future agent-tool registries because it keeps provenance visible at scan
   time.

3. **Quality-bar text should become an intake lint, not promotion logic.**  
   VAKS can borrow checks like public source, docs present, short description,
   scoped tool needs, and specific trigger language. These checks decide whether
   a source is worth opening, not whether it is true.

4. **Security disclaimer belongs directly in the registry surface.**  
   The source keeps a warning near the registry rather than burying it in docs.
   VAKS should use the same move for agent-skill and MCP registries: visible
   risk labels beside candidate capability entries.

5. **Cross-agent path table is a useful compatibility map.**  
   The path table for different agent environments is a good model for VAKS
   adapter notes, but only as operational context. It should not be hardcoded
   into core architecture.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Source Ingest | Minimum entry fields: owner/name, source URL, short function, category, docs presence. | Adapt as source-card lint. |
| Candidate Comprehension | Short skill descriptions help triage. | Keep as candidate summary only. |
| Review Queue | Quality criteria can route weak entries to missing-evidence or risk. | Use as review pressure, not review result. |
| Association / Activation | Category registry can light up relevant candidate sources. | Candidate relation only. |
| Agent Gateway / Tool Boundary | Explicit security warning and scoped-tool idea. | Strongly borrow for future agent/MCP memory quarantine. |
| Action / Use Ledger | No direct action value. | Must pass separate execution/safety gate. |

## Local De-Dup / Collision

The earlier shallow file already labeled this as `agent_skill_registry`. This
strong file replaces that shallow conclusion with evidence anchors and a clearer
boundary:

- `borrow_value: strong` stays valid.
- The borrow is not "use the listed skills"; it is "borrow the registry
  governance pattern."
- The source strengthens existing VAKS boundaries around agent memory
  quarantine and candidate-only external capability records.

## Anti-Borrow

- Do not import the registry's full taxonomy as VAKS ontology.
- Do not treat "official", "community-adopted", or "most contributed" as a
  trust score.
- Do not install or run listed skills as part of source review.
- Do not make sponsor/product placement part of any ranking logic.

## Candidate Tags

```yaml
domain: agent-skill-registry
problem: external-capability-discovery-without-authority-confusion
pattern:
  - link-only-registry
  - visible-security-disclaimer
  - short-entry-format
  - quality-bar-before-listing
maturity: emerging
problem_fit: 5
reuse_value: 4
implementation_cost: 2
integration_fit: 4
evidence_strength: 3
reversibility: 5
```

## Fusion Judgment

Adapt the registry governance, not the content. For VAKS, this source is best
used as a P1 reference for future external tool/source catalogs and agent-skill
quarantine rules.
