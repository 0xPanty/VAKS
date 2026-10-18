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
  - raw/repos/2026-06-11-obsidian-pkm-vault-awesome-obsidian-vault-source.md
  - outputs/review/2026-06-11-awesome-obsidian-vault-candidate-triage.md
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
  - p1-scout
  - obsidian-workbench
  - agent-boundary
  - source-hygiene
possible_project_refs:
  - verified-action-knowledge-system
borrow_value: strong
borrow_order:
  - "P1: Obsidian Hub, DashboardPlusPlus, vercel-labs/skills, VoltAgent/awesome-agent-skills"
  - "P2: KaaS as publish/export pipeline and vault-to-site workflow"
  - "Downgrade: nikitavoloboev/knowledge current repo no longer looks like the listed knowledge vault"
avoid:
  - "Do not treat current GitHub stars, awesome-list inclusion, or install counts as evidence support."
  - "Do not import plugin-heavy dashboards, skill registries, or publish workflows into VAKS truth core."
  - "Do not trust stale awesome-list labels when current repo contents differ."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "task is specifically about P1 Obsidian/vault references from awesome-obsidian-vault"
  support_when: "designing workbench, dashboard, source catalog, publishing, or skill registry boundaries"
  risk_when: "a source offers polished UI or agent skills that could be mistaken for reviewed knowledge or action authority"
  cold_references:
    - raw/repos/2026-06-11-obsidian-pkm-vault-awesome-obsidian-vault-source.md
tags:
  - candidate-only
  - p1-scout
  - obsidian-vaults
  - workbench
  - agent-boundary
  - source-hygiene
---

# P1 Batch Scout: awesome-obsidian-vault

## Boundary

This is a scout-level candidate distillation.

It fixes current HEAD / README / selected source anchors for six P1 candidates. It is not a full architecture review for each repository.

Do not promote any point from this file without a separate source card, source/code anchor pass, and VAKS review gate.

## Source Anchors Checked

| Repo | HEAD / branch | Selected anchors inspected | Current scout result |
|---|---|---|---|
| `obsidian-community/obsidian-hub` | `b11036f9a4db77917a4f07804541cceffc96cc66` / `main` | `README.md`, `.github/scripts/templates/directory_moc.md.jinja`, `.github/scripts/plugins.py` | P1 workbench/source-catalog candidate |
| `jimbrig/KaaS` | `028fcf40521403c1b8a9fa6b28c3b9b2cd8cebbc` / `main` | `README.md`, `.github/workflows/convert-links.yml`, `.github/workflows/mkdocs.yml`, `.obsidian/` tree | P2 publish/export pipeline candidate |
| `nikitavoloboev/knowledge` | `a6b6210430c2668ed1a078a98e3b69f52be37bde` / `main` | `readme.md`, root tree | downgrade: current repo appears to be Go tooling, not the listed vault |
| `TfTHacker/DashboardPlusPlus` | `e202bb286cd92d7986407293c0a4a33789fef2bd` / `master` | `README.md`, `Dashboard++.md`, `.obsidian/plugins/` tree | P1 dashboard/workbench candidate |
| `VoltAgent/awesome-agent-skills` | `0e6e58985eb75a2cf7b2cbf4bc518f1bd4ef1210` / `main` | `README.md`, `CONTRIBUTING.md` | P1 skill registry / curation candidate |
| `vercel-labs/skills` | `c243b178746ae8fdd1a9a4af12324afb18e714a3` / `main` | `README.md`, `skills/find-skills/SKILL.md`, `src/frontmatter.ts`, `src/install.ts`, `src/providers/registry.ts` | P1 skill package manager / safety candidate |

## Candidate Points

### 1. Obsidian Hub: public source catalog as a vault

Best VAKS borrow:

```text
community-maintained resource hub
directory MOC generation
plugin/theme/author records generated from source data
publishable Obsidian vault as reference surface
```

VAKS layer fit:

```yaml
fit_layer:
  - source-ingest
  - workbench
  - publishing
  - source-hygiene
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - plugin-adoption-proof
borrow_value: strong
borrow_order: P1
```

Why it matters:

```text
VAKS has strong authority boundaries but still needs usable source catalogs and human-readable workbench surfaces.
Obsidian Hub shows a concrete pattern: source records can feed directory/MOC pages without becoming truth.
```

Do not borrow:

```text
plugin popularity as trust
community catalog as reviewed support
generated MOCs as action readiness
```

### 2. KaaS: vault-to-publish pipeline

Best VAKS borrow:

```text
Obsidian vault -> exported markdown -> MkDocs / GitHub Pages publish path
workflow-visible conversion stage
separate source vault and public site build
```

VAKS layer fit:

```yaml
fit_layer:
  - publishing
  - products
  - source-hygiene
not_fit_layer:
  - truth-core
  - review-queue
  - action-basis
borrow_value: medium
borrow_order: P2
```

Why it matters:

```text
VAKS already separates `wiki/` and `products/`.
KaaS is useful as a publish/export workflow reference, not as a verified-action architecture.
```

Risk:

```text
The workflow uses force-push style publishing and broad file copying.
For VAKS, any publish pipeline must preserve source/provenance and never rewrite reviewed records silently.
```

### 3. nikitavoloboev/knowledge: stale catalog warning

Scout correction:

```text
The awesome list labels this as Knowledge, but the current repo HEAD appears to be Go tooling / CLI code.
The root `readme.md` starts with `# Go`, and the file tree is dominated by `cli/`, `go.mod`, and Go source files.
```

VAKS layer fit:

```yaml
fit_layer:
  - source-hygiene
  - catalog-freshness
not_fit_layer:
  - knowledge-architecture
  - workbench
  - reviewed-knowledge
borrow_value: avoid
borrow_order: downgraded
```

Borrow the warning, not the source:

```text
curated lists drift
repo names and websites can outlive the original vault shape
freshness checks must happen before distillation
```

### 4. DashboardPlusPlus: homepage as workbench

Best VAKS borrow:

```text
one explicit Home/Dashboard note
sectioned navigation by life/work/project areas
Dataview-powered recent/favorite surfaces
CSS class and snippets for readable dashboard layout
```

VAKS layer fit:

```yaml
fit_layer:
  - workbench
  - activation
  - dev-context
not_fit_layer:
  - truth-core
  - review-approval
  - evidence-support
borrow_value: strong
borrow_order: P1
```

Why it matters:

```text
VAKS formal vault needs a usable entry surface.
Dashboard++ is a small, inspectable example of a dashboard note that helps humans navigate without changing knowledge authority.
```

Do not borrow:

```text
plugin-heavy setup as default
dashboard visibility as confidence
recent/favorite Dataview results as review priority without explicit review_pressure
```

### 5. VoltAgent awesome-agent-skills: skill registry curation

Best VAKS borrow:

```text
curated skill registry
short descriptions
category placement
submission quality bar
link-only registry with skills living in their own repos
```

VAKS layer fit:

```yaml
fit_layer:
  - agent-boundary
  - skill-registry
  - workbench
  - source-hygiene
not_fit_layer:
  - agent-write-authority
  - reviewed-memory
  - action-basis
borrow_value: strong
borrow_order: P1
```

Why it matters:

```text
VAKS will eventually need visible skills/workflows, but skills must stay operational.
VoltAgent's useful pattern is registry curation and skill provenance, not automatic trust.
```

Do not borrow:

```text
install count as truth
community adoption as action readiness
external skill as permission to write reviewed knowledge
```

### 6. vercel-labs/skills: package-managed skills with safety details

Best VAKS borrow:

```text
SKILL.md metadata and discovery flow
project-level skill lock/install flow
provider registry abstraction
frontmatter parsing that avoids JS eval
quality verification before recommending skills
```

VAKS layer fit:

```yaml
fit_layer:
  - agent-boundary
  - skill-registry
  - tool-safety
  - source-hygiene
not_fit_layer:
  - truth-core
  - reviewed-relation
  - action-basis
borrow_value: strong
borrow_order: P1
```

Why it matters:

```text
This is the strongest P1 scout hit for VAKS agent access.
It gives concrete implementation anchors for visible skill packages, provider matching, and safer frontmatter parsing.
```

Do not borrow:

```text
automatic skill install without user intent
skill output as reviewed knowledge
skill popularity as evidence support
agent runtime as VAKS source of truth
```

## Updated Priority After Scout

```text
P1 keep:
  Obsidian Hub
  DashboardPlusPlus
  VoltAgent awesome-agent-skills
  vercel-labs/skills

P2 keep:
  KaaS

Downgrade / skip until fresh source is found:
  nikitavoloboev/knowledge
```

## Next Heavy Distillation Order

If continuing this list, the best next heavy reviews are:

```text
1. vercel-labs/skills
2. Obsidian Hub
3. DashboardPlusPlus
4. VoltAgent/awesome-agent-skills
5. KaaS only if publishing/product-output is the active question
```

Reason:

```text
VAKS currently needs stronger retrieval/workbench/agent-boundary surfaces, not more general content-vault examples.
```
