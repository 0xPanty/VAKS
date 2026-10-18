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
  - source-scouting
  - reference-review
  - obsidian-workbench
  - agent-boundary
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - raw/repos/2026-06-11-obsidian-pkm-vault-awesome-obsidian-vault-source.md
borrow_value: strong
borrow_order:
  - "P1: VAKS architecture/workbench/agent-boundary candidates, inspect first."
  - "P2: useful examples for publishing, templates, docs-as-vault, and dashboard surfaces."
  - "P3: content-heavy vaults, keep as cold source-structure references only."
avoid:
  - "Do not borrow domain content, folder taxonomies, popularity, or static-site polish as VAKS architecture."
  - "Do not treat awesome-list inclusion, stars, or websites as evidence support."
  - "Do not let templates override raw/wiki/review/action-basis boundaries."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "task is specifically about selecting Obsidian/vault references for VAKS intake or workbench design"
  support_when: "reviewing source intake, workbench, activation, publishing, dashboard, or agent-boundary examples"
  risk_when: "a source looks polished but lacks evidence, Obsidian compatibility, or VAKS layer fit"
  cold_references:
    - raw/repos/2026-06-11-obsidian-pkm-vault-awesome-obsidian-vault-source.md
tags:
  - candidate-only
  - source-scouting
  - obsidian-vaults
  - vaks-fit-triage
  - skip-processed
---

# Candidate Triage: awesome-obsidian-vault

## Boundary

This note is a candidate routing layer for a list of vaults.

It is not reviewed knowledge, not an architecture decision, not a quality proof, and not action basis.

## 说人话

这个列表不是“都要吸收”。它是一个候选池。

对 VAKS 来说，先问三件事：

```text
1. 它帮 VAKS 哪一层？
2. 它不能借到哪一层？
3. 本地有没有已经蒸馏过或已经被主架构覆盖？
```

以后蒸馏这里面的库，标签不能只写 `obsidian / digital-garden / pkm`。必须写 VAKS 层：

```text
source-ingest
candidate-review
activation
dev-context
context-pack
workbench
publishing
agent-boundary
retrieval-cache
source-hygiene
risk
```

## Already Distilled / Skip For Now

Strict exact-source check found these already in local artifacts:

| Entry | Reason to skip |
|---|---|
| Kepano Obsidian | Existing source and architecture review under `raw/repos/` and `wiki/summaries/`. Already absorbed as metadata/view/link activation support, not truth. |
| Obsidian Tasks | Existing review material mentions the exact repo. Treat as already considered for task/workbench surfaces unless the user asks for a fresh current-version review. |

Known mainline-covered patterns from prior work also reduce priority:

| Pattern | Current status |
|---|---|
| PARA-style folder routing | Already rejected as truth architecture; only actionability routing is useful. |
| Dusk-style dashboard | Already absorbed as workbench/dev-context surface, not truth. |
| Kagantic-style hierarchical index | Already absorbed as Markdown-first context routing. |
| generic retrieval-is-activation | Already mainline boundary. |

## P1: Inspect First

These are most likely to produce VAKS-relevant borrow points.

| Entry | VAKS fit | Borrow only as | Do not borrow as |
|---|---|---|---|
| Obsidian Hub | Community documentation vault, taxonomy, plugin/reference discoverability | source catalog, docs-as-vault, public workbench reference | truth authority, schema, plugin adoption proof |
| KaaS - jimbrig | Knowledge-as-a-service style personal/system knowledge repo | knowledge architecture comparison, documentation/workbench patterns | runtime authority, action basis |
| Knowledge - nikitavoloboev | Downgraded after P1 scout: current GitHub repo no longer looks like the listed knowledge vault | source freshness / stale catalog warning | VAKS architecture, until a fresh vault/source anchor is found |
| DashboardPlusPlus - TfTHacker | Obsidian dashboard/workbench surface | home/dashboard/navigation surface for formal vault | confidence/readiness indicator |
| Awesome Agent Skills - VoltAgent | Skill registry and agent-workflow examples | agent-boundary, skill catalog, workflow-as-files | agent write authority or reviewed memory |
| skills - Vercel labs | File-based skill ecosystem and website | visible skill registry, prompt/skill packaging, tool-safety comparison | automatic agent action or truth mutation |

P1 distillation route:

```text
source card
-> candidate distillation
-> architecture review when code/templates exist
-> project overlay only if the VAKS-specific borrow scope is concrete
```

## P2: Useful With Narrow Scope

These should be distilled only if a current VAKS question needs that layer.

| Entry | VAKS fit | Likely layer |
|---|---|---|
| Obsidian Icewind | Polished published vault and navigation | workbench / publishing / UX |
| Blue Book - lyz-code | Docs-as-vault and long-lived personal docs | source structure / publishing / cold reference |
| Intersect - rknightuk | Published personal docs/site | workbench / publishing |
| Topobon - uroybd | Digital garden example | publishing / navigation |
| Interneto - David7ce | Web-directory scale curation | source catalog / source hygiene / link maintenance |
| Free Media Heck Yeah | Large curated directory | link health, source status, warning labels |
| Obsidian Digital Garden | publishing pipeline | products / publishing |
| Digital Garden Docs | documentation for publishing | publishing workflow |
| Obsidian Vault Template - CyanVoxel | template conventions | capture/workbench template comparison |
| Obsidian Templates - groepl / ykerus | reusable template examples | capture template comparison |
| System Design 101 | technical docs vault | docs-as-vault structure, not VAKS architecture |

## P3: Cold References Only

These are mostly domain-content or curriculum libraries. They can still teach source structure, but they should not be heavy-distilled unless a specific question needs them.

| Group | Entries | Default treatment |
|---|---|---|
| Cooking / recipe vaults | Based.cooking, Grimgrains, recetas-cocina, recipes, Chowdown, DevCookbook, HowToCook, Cookbook, Giallozafferano | cold reference for content schema / static site structure only |
| Computer-science content vaults | JavaScript Info, CS Notes, OSSU, learning-notes, computing notes, mayfrost guides | P3 unless testing docs-as-vault scale or source update hygiene |
| API/product documentation | dotnet API Docs, SQL Docs, Data Engineering Wiki | P3; useful for docs source freshness, not VAKS architecture |
| Personal/static sites | XXIIVV/oscean, Hundred Rabbits, kokorobot | P3 for navigation/creative wiki patterns |
| Special domains | Wikiterra, recipe datasets, Anki/shared decks, Kiwix/Wikimedia resources | cold references only |

## VAKS Tagging Rule For Next Distillations

Use these tags first, then add ordinary topic tags:

```yaml
vaks_layer:
  - source-ingest
  - candidate-review
  - activation
  - dev-context
  - context-pack
  - workbench
  - publishing
  - agent-boundary
  - retrieval-cache
  - source-hygiene
  - risk
borrow_value: strong | medium | low | avoid
borrow_order: P1 | P2 | P3
fit_layer:
not_fit_layer:
evidence_strength:
review_route:
dev_context_hint:
```

Plain-language rule:

```text
Borrow mechanisms, not vibes.
Borrow layer-specific patterns, not whole vault philosophies.
Borrow warning labels as eagerly as positive ideas.
```

## Avoid List

- Do not turn a digital garden into VAKS truth architecture.
- Do not treat public navigation polish as evidence discipline.
- Do not treat task/dashboard plugins as review approval.
- Do not copy content-domain folders into VAKS.
- Do not make every template a schema field.
- Do not make a broad curated directory the source of truth.
- Do not treat link popularity, stars, or awesome-list curation as support.

## Next Candidate Batch

Recommended first batch:

```text
1. Obsidian Hub
2. DashboardPlusPlus
3. VoltAgent/awesome-agent-skills
4. vercel-labs/skills
5. KaaS
```

Reason:

```text
They map directly to VAKS workbench, source catalog, publishing pipeline, and agent-boundary questions. `nikitavoloboev/knowledge` was downgraded after scout because the current GitHub repo appears to have drifted away from the listed vault shape.
```

Do not process cooking/content libraries before these unless the user asks for content-schema or static-site source structure specifically.
