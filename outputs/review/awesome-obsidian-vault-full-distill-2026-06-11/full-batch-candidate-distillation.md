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
  - outputs/review/2026-06-11-awesome-obsidian-vault-p1-batch-scout.md
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/batch-source-ledger.json
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
  - obsidian-vault-reference-batch
  - source-scouting
  - workbench
  - agent-boundary
  - publishing
  - source-hygiene
possible_project_refs:
  - verified-action-knowledge-system
borrow_value: strong
borrow_order:
  - "P1: skill registry, source catalog, dashboard/workbench, agent-boundary references."
  - "P2: publishing pipeline, docs-as-vault, template, directory/link-health references."
  - "P3: domain-content vaults kept as cold source-shape examples only."
avoid:
  - "Do not copy full vault philosophies into VAKS."
  - "Do not treat stars, curated-list inclusion, install counts, or visual polish as evidence support."
  - "Do not let dashboards, tasks, skills, or publishing outputs become reviewed knowledge or action basis."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "task is specifically about selecting or implementing VAKS workbench/source-catalog/skill-boundary references"
  support_when: "designing Obsidian workbench, source catalog, publishing, skill registry, templates, or link-health surfaces"
  risk_when: "a polished vault/template/registry could be mistaken for truth, review approval, or action readiness"
  cold_references:
    - raw/repos/2026-06-11-obsidian-pkm-vault-awesome-obsidian-vault-source.md
    - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/batch-source-ledger.json
tags:
  - candidate-only
  - full-batch-distillation
  - awesome-obsidian-vault
  - vaks-fit-triage
---

# Full Batch Candidate Distillation: awesome-obsidian-vault

## Boundary

This is a batch-level candidate distillation of the 48 entries in
`obsidian-pkm-vault/awesome-obsidian-vault`.

It is not reviewed knowledge, not a decision, not a formal pattern, and not
action basis. It routes future attention.

## 说人话

这批资料对 VAKS 的价值不是“哪个 vault 漂亮就学哪个”。

真正要借的是机制：

```text
怎么收来源
怎么做目录和工作台
怎么把公开发布和内部权威分开
怎么让 agent/skill 可见但不越权
怎么给大目录做 link health / source status
```

不能借的是：

```text
整套文件夹哲学
插件堆叠
视觉 dashboard 当可信度
任务列表当 review gate
skill registry 当行动许可
```

## Skip Existing

| Entry | Local status | Why skipped |
|---|---|---|
| Kepano Obsidian | already distilled | Existing source/review material already absorbed metadata/view/link activation. |
| Obsidian Tasks | already considered | Existing review material mentions exact repo; task plugin ideas should stay workbench/task layer. |

## P1: Strong VAKS Borrow Candidates

| Entry | VAKS fit layer | Borrow | Do not borrow | Next action |
|---|---|---|---|---|
| Obsidian Hub | source-ingest, workbench, publishing, source-hygiene | Community resource hub, directory MOC generation, plugin/theme/author records, publishable vault surface. | Plugin popularity as trust, community catalog as reviewed support, generated MOC as action readiness. | Heavy review when building source catalog or public vault index. |
| DashboardPlusPlus | workbench, activation, dev-context | One explicit Home dashboard, sectioned navigation, recent/favorite surfaces, lightweight Obsidian entry point. | Dashboard visibility as confidence, Dataview result as review priority, plugin-heavy setup as default. | Use for formal vault HOME/dashboard design only. |
| VoltAgent awesome-agent-skills | agent-boundary, skill-registry, source-hygiene | Curated skill registry, category placement, short descriptions, link-only skill provenance. | Install count/community adoption as truth or action readiness. | Review beside VAKS agent-memory quarantine before skill catalog design. |
| vercel-labs/skills | agent-boundary, skill-registry, tool-safety, source-hygiene | `SKILL.md` metadata, provider abstraction, lock/install flow, quality verification, safer YAML frontmatter parsing. | Automatic skill install, skill output as reviewed knowledge, agent runtime as truth source. | Best next heavy distillation. |

## P2: Useful With Narrow Scope

| Entry | VAKS fit layer | Borrow | Do not borrow | Routing |
|---|---|---|---|---|
| KaaS | publishing, products, source-hygiene | Vault-to-export-to-MkDocs/GitHub Pages pipeline; visible conversion stage. | Force-push publish pipeline, broad copying, public site as source of truth. | Product/output publishing only. |
| Obsidian Vault Template - CyanVoxel | capture-template, workbench, onboarding | Opinionated starter vault and template conventions. | Template folders as VAKS schema. | Compare when designing ordinary note-intake templates. |
| Obsidian Templates - groepl | capture-template, source-ingest | Reusable template collection as capture prompts. | Every template as mandatory metadata. | P2 template comparison. |
| Obsidian Templates - ykerus | capture-template, source-ingest | Lightweight template variants and capture affordances. | Template collection as reviewed knowledge model. | P2 template comparison. |
| Obsidian Digital Garden - ThatOtherAndrew | publishing, products | Public garden publishing path and navigation surface. | Published note as reviewed claim. | Use for products layer, not truth core. |
| Digital Garden Docs - oleeskild | publishing, documentation | Documentation for digital-garden publishing workflow. | Plugin workflow as VAKS architecture. | Use when implementing publishing docs. |
| Digital Gardeners - MaggieAppleton | publishing, explanation, design-language | Digital garden framing and public knowledge presentation. | Garden philosophy as evidence discipline. | Use for product/expression language. |
| Topobon | publishing, navigation, workbench | Polished digital garden navigation and public browsing. | Visual polish as evidence or quality. | P2 UX reference. |
| Obsidian Icewind | workbench, publishing, navigation | Polished published vault structure. | Public site elegance as VAKS review quality. | P2 UX/navigation reference. |
| Blue Book - lyz-code | docs-as-vault, publishing, source-structure | Long-lived documentation wiki with stable navigation. | Docs structure as VAKS truth workflow. | P2 docs-scale reference. |
| Intersect - rknightuk | personal-docs, publishing, navigation | Personal site/vault publishing shape. | Personal categories as VAKS taxonomy. | P2 navigation reference. |
| Interneto | source-catalog, source-hygiene, link-health | Large web directory, category navigation, link maintenance pressure. | Directory inclusion as support or trust. | P2 source catalog / link-health reference. |
| Free Media Heck Yeah | source-catalog, source-status, risk | Huge curated directory, mirror/link survival, warning labels. | Piracy/domain content; popularity as trust. | P2 link-health/risk-label reference only. |
| Documentation - Rico Sta. Cruz / cheatsheets | docs-as-vault, dense-reference, source-structure | Dense cheat-sheet structure and quick lookup style. | Cheat-sheet brevity as sufficient evidence. | P2 context-pack compression reference. |
| System Design 101 | docs-as-vault, education-structure | System-design content organization and diagrams. | Technical claims as reviewed VAKS evidence. | P2 docs source structure only. |
| Data Engineering Wiki | docs-as-vault, domain-wiki, source-catalog | Domain knowledge wiki organization and index style. | Domain wiki as VAKS evidence authority. | P2 docs-scale/source-catalog reference. |
| Gatekeeperwiki Game | workbench, domain-wiki, navigation | Game wiki navigation and domain page structure. | Game taxonomy as general knowledge schema. | P2/P3, only if testing non-technical domain vaults. |

## P3: Cold Source-Shape References

These entries are not useless. They are just not VAKS architecture drivers.
Keep them as cold references unless a future task needs their exact domain shape.

| Entry | Cold borrow | Avoid |
|---|---|---|
| Based.cooking | Recipe content model: ingredients, steps, simple static structure. | Cooking taxonomy as VAKS schema. |
| Grimgrains | Illustrated recipe/site style and narrative browsing. | Aesthetic layout as evidence quality. |
| Recetas de Cocina | Multilingual recipe vault and static publishing. | Recipe collection as knowledge architecture. |
| Recetas Cocina dataset | Dataset packaging for domain content. | Dataset existence as source reliability. |
| Recipes as JSON | Structured recipe records and machine-readable content. | JSON domain schema as VAKS schema. |
| Chowdown | Recipe static site generator pattern. | Static site generator as VAKS core. |
| DevCookbook | Developer recipe/cookbook structure. | Cookbook metaphor as review process. |
| HowToCook | Chinese recipe knowledge base, large domain content. | Procedure notes as action basis without review. |
| Cookbook - douglaslassance | Small recipe vault source shape. | Domain folders as general taxonomy. |
| Giallozafferano | Web-only recipe site for source capture. | Website polish as vault quality. |
| Computing notes - noodleslove | Personal learning notes source shape. | Personal note style as VAKS architecture. |
| JavaScript Info | Tutorial/docs source structure and versioned learning content. | Tutorial claims as VAKS reviewed evidence. |
| CS Notes - xy-241 | Curriculum-style CS notes and topic hierarchy. | Course hierarchy as universal vault taxonomy. |
| Computer Guides - mayfrost | Guide collection and archival reference structure. | Guide list as evidence support. |
| OSSU Computer Science | Curriculum graph and prerequisite structure. | Curriculum order as VAKS activation order. |
| Learning Notes - keyvanakbary | Personal learning record and publish path. | Personal learning notes as review queue model. |
| Wikiterra Vault | Domain wiki/vault structure for cosmology. | Domain-specific ontology as VAKS ontology. |
| dotnet API Docs | Large API docs source/versioning. | API docs repository as Obsidian workflow model. |
| SQL Docs | Large product docs, versioned content. | Microsoft docs structure as VAKS truth layer. |
| Alexia Chen notes | Personal digital notes. | Personal categories as architecture. |
| Devine Lu Linvega / oscean | Creative wiki/personal system and navigation. | Creative taxonomy as verified knowledge structure. |
| Hundred Rabbits project site | Project/site wiki, creative archive. | Project aesthetic as review discipline. |
| Rekka Bellum / kokorobot | Personal site navigation and archive style. | Personal site structure as VAKS schema. |
| Ideaverse - LYT | Ideaverse onboarding and personal PKM method. | LYT method as VAKS truth model. |

## Downgraded / Freshness Warning

| Entry | Finding | VAKS lesson |
|---|---|---|
| Knowledge - nikitavoloboev | Current GitHub HEAD appears to be Go tooling/CLI, not the listed knowledge vault shape. | Curated lists drift. Always check current repo contents before distillation. |

## Layer Summary

```yaml
source-ingest:
  P1: Obsidian Hub
  P2: Interneto, FMHY, template collections
workbench:
  P1: DashboardPlusPlus, Obsidian Hub
  P2: Icewind, Topobon, Intersect
agent-boundary:
  P1: vercel-labs/skills, VoltAgent awesome-agent-skills
publishing:
  P2: KaaS, Obsidian Digital Garden, Digital Garden Docs, Blue Book
source-hygiene:
  P1: Obsidian Hub
  P2: Interneto, FMHY
  warning: nikitavoloboev/knowledge drift
context-pack:
  P2: cheatsheets, docs-as-vault references
risk:
  all dashboards/skills/catalogs must stay outside truth and action basis
```

## Candidate Borrow Rules For Future Reviews

1. For `vercel-labs/skills`, inspect code and docs deeply before borrowing any skill runtime idea.
2. For `Obsidian Hub`, inspect generation scripts and data files, not just the publish site.
3. For `DashboardPlusPlus`, borrow the dashboard note shape, not its plugin bundle.
4. For large directories, borrow link-health and warning labels, not content.
5. For domain vaults, borrow source-shape only when the current task needs that domain pattern.

## Completion State

All 48 entries have now been routed:

```text
2 exact skips
4 P1 strong candidates
17 P2 narrow-scope candidates
24 P3 cold references
1 downgraded freshness warning
```

This completes batch-level candidate distillation for the awesome list.
