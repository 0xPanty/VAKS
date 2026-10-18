---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://www.linkingyourthinking.com/ideaverse-for-obsidian/onboarding-ideaverse"
repo_key: "linkingyourthinking/ideaverse"
checked_commit: "not_applicable_live_web_source"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/linkingyourthinking-ideaverse-anchor-manifest.json
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
  - onboarding-vault
  - guided-map
  - link-hygiene
fit_layer:
  - candidate-comprehension
  - activation
  - publishing
  - risk-inhibition
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - source-snapshot-authority
avoid:
  - "Do not import proprietary or paid Ideaverse vault content."
  - "Do not ask users to trust community plugins by default."
  - "Do not treat a live marketing/onboarding page as stable architecture evidence."
dev_context_hint:
  default_layer: cold-reference
  core_only_when: "When designing guided onboarding, home maps, and link-practice prompts."
  support_when: "When comparing sample vault onboarding flows."
  risk_when: "When plugin trust, incomplete downloads, or live-web drift affect source confidence."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/linkingyourthinking-ideaverse-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - sample-vault
  - onboarding
---

# Strong Candidate Distillation: Linking Your Thinking / Ideaverse

## Boundary

This is a live-web/onboarding source, not a GitHub repository. A public download
was attempted, but the local zip-like file was incomplete and could not be
opened as a valid archive. This file therefore extracts only observed onboarding
and lesson design from public web pages.

It does not import Ideaverse vault content, paid material, plugin settings, or
proprietary templates.

## What This Source Actually Is

The observed source is an onboarding page for Ideaverse Lite/Pro/Zero-style
Obsidian sample vaults, plus the first lesson page. It instructs users to open
the downloaded folder as a separate Obsidian vault, not to drag it into an
existing vault, to follow Home/Map entry points, and to inspect how notes are
linked.

The first lesson emphasizes uplinks, indexes/maps, paragraph-level links, and
not over-linking.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| Onboarding page | Lite download links, installation steps, open as new vault warning, plugin trust step, Home Basic / Ideaverse Map entry points. | Sample vault onboarding should isolate the demo vault and provide clear first-map navigation. | Do not trust plugins by default in VAKS. |
| Windows install section | Warns not to drag into existing vault; says ignore `_MACOSX`; references expected file/folder counts. | Installation docs should prevent accidental merge into a real vault. | Page has count/name inconsistencies. |
| Lesson 1 overview | Asks user to inspect links, uplinks, indexes/maps, linked paragraphs, and to add useful links without overdoing it. | Guided link literacy and anti-overlinking prompt. | Link practice is not evidence review. |
| Partial zip download | Local file begins like a zip but lacks end-of-central-directory record. | Snapshot completeness must be verified before treating downloads as source. | Incomplete archive cannot anchor vault internals. |

## Strong Borrow Points

1. **Sample vaults should be opened as separate vaults.**  
   The onboarding explicitly warns against dragging the sample into an existing
   vault. VAKS should use this boundary for any formal sample-vault tests:
   isolate, inspect, then delete temp copies after verification.

2. **First-run navigation needs a Home/Map surface.**  
   Home Basic and Ideaverse Map are onboarding anchors. VAKS can borrow the idea
   for future candidate workbenches: one obvious recovery map, not many hidden
   starts.

3. **Teach links as practice, not as automatic structure.**  
   The first lesson asks users to inspect uplinks, indexes/maps, and paragraph
   links, then add only useful links. This aligns with VAKS: links are
   activation and comprehension aids, not reviewed relations.

4. **Plugin trust should be explicit.**  
   The page asks users to trust and enable plugins. VAKS should invert the
   default: do not enable unknown plugins in the formal vault unless explicitly
   authorized and scoped.

5. **Download/source completeness must be checked.**  
   The attempted public download produced an incomplete zip-like file. VAKS
   source intake should record incomplete archives as limited evidence rather
   than silently proceeding.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Live web pages and attempted archive. | Source limit note. |
| Candidate Comprehension | Guided first lesson. | Onboarding checklist. |
| Activation | Home/Map entry surfaces and uplinks. | Recovery map and navigation hints. |
| Risk / Inhibition | Plugin trust and incomplete archive. | Explicit trust/snapshot gate. |
| Reviewed Knowledge | No direct fit. | Keep separate. |

## Local De-Dup / Collision

This overlaps with Obsidian templates, digital gardens, and public vault
examples:

- CyanVoxel and Dusk show vault/template structures.
- Kepano shows property/view-first activation.
- Ideaverse contributes guided onboarding and link-practice pedagogy, not a
  source-verified structure in this run.

The unique borrow is the separate-vault onboarding and "link, but do not
overlink" practice loop.

## Anti-Borrow

- Do not import proprietary vault files or paid templates.
- Do not enable community plugins in the formal VAKS vault by default.
- Do not treat a failed/incomplete zip as a source snapshot.
- Do not treat link density as knowledge quality.
- Do not rely on live marketing pages as stable architecture authority.

## Candidate Tags

```yaml
domain: sample_vault_onboarding
problem: teaching_users_to_enter_and_navigate_a_linked_vault_safely
pattern:
  - separate-sample-vault-install
  - home-map-onboarding
  - uplink-and-index-literacy
  - anti-overlinking-guidance
  - plugin-trust-explicitness
  - archive-completeness-check
maturity: public-onboarding-source
problem_fit: 3
reuse_value: 3
implementation_cost: 2
integration_fit: 3
evidence_strength: 2
reversibility: 5
```

## Fusion Judgment

Borrow moderately for onboarding and link-literacy design. Do not borrow vault
internals because no complete source snapshot was available in this run.
