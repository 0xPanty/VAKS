---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/mayfrost/guides/tree/master"
repo_key: "mayfrost/guides"
checked_commit: "bd8efbcdc4315f659953766249990d761fefc223"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/mayfrost-guides-anchor-manifest.json
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
  - operational-runbook
  - risk-ladder
  - staleness-warning
fit_layer:
  - candidate-comprehension
  - action-risk
  - maintenance
  - source-hygiene
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not use the security or system commands as live advice without current verification."
  - "Do not copy ideology-heavy or stale operating-system recommendations into VAKS."
  - "Do not treat difficulty order as evidence sufficiency."
dev_context_hint:
  default_layer: risk
  core_only_when: "When designing risk ladders, operational runbook templates, or action-gating warnings."
  support_when: "When comparing long-form command-heavy guides and TOC-driven operational docs."
  risk_when: "When old commands, security advice, or destructive system operations might be used as action basis."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/mayfrost-guides-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - runbook
  - risk-ladder
---

# Strong Candidate Distillation: mayfrost / guides

## Boundary

This file extracts operational-document and risk-ladder lessons. It does not
endorse the guide content, security advice, distro recommendations, or commands
as current or safe action basis.

## What This Source Actually Is

`mayfrost/guides` is a small collection of command-heavy guides covering system
installation, security, networking, bootloaders, cross-compiling, distros, X,
audio/video, and communication. The README explicitly says the docs are under
rewrite and links may change.

The repo is useful to VAKS as a cautionary example of long-lived operational
guides: they need TOCs, difficulty/risk ladders, placeholders, and stale-advice
warnings.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | FDL notice and explicit rewrite-in-progress warning. | Staleness/change warning belongs near source identity. | Warning does not validate content. |
| `CHECKLIST.md` | Security checklist grouped by difficulty levels 1-55. | Risk/difficulty ladder can organize progressive hardening. | Advice is not action basis. |
| `SECURITY.md` | Routes security material to checklist. | Thin router document avoids duplication. | Router is not review. |
| `CROSS-COMPILING.md` | TOC, hardware assumptions, commands, placeholders, options. | Operational runbook with prerequisites and variable placeholders. | Commands require current validation. |
| Root guide set | Small file set by operational domain. | Domain-per-guide keeps scope clear. | Domain boundaries can be ideological/stale. |

## Strong Borrow Points

1. **Put staleness and rewrite warnings at the source boundary.**  
   The README's rewrite warning is valuable because it prevents readers from
   assuming stable links or current advice.

2. **Risk ladders can organize hardening without forcing all steps.**  
   `CHECKLIST.md` orders security actions by difficulty. VAKS can borrow the
   risk-ladder shape for action gating, but each action still needs current
   evidence and environment fit.

3. **Operational runbooks should name assumptions and placeholders.**  
   `CROSS-COMPILING.md` identifies target architecture/device assumptions and
   uses placeholders like device paths and toolchain directories. VAKS action
   packs should do the same before any command execution.

4. **Thin router files reduce duplicate guidance.**  
   `SECURITY.md` points to the checklist rather than re-declaring everything.
   VAKS can use index/router docs for activation while preserving one source of
   candidate instructions.

5. **Command-heavy notes require inhibition gates.**  
   The guide includes destructive disk and bootloader commands. VAKS should
   treat such notes as high-risk and require explicit confirmation plus current
   verification.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Candidate Comprehension | Operational guide structure. | Candidate runbook template. |
| Action / Decision | Difficulty ladder and prerequisites. | Gate only, not action basis. |
| Risk / Inhibition | Destructive commands and stale advice. | Require confirmation and verification. |
| Maintenance | Rewrite warning and link drift. | Staleness lint. |
| Activation | Router docs and TOCs. | Navigation support. |

## Local De-Dup / Collision

This overlaps with security/tooling guides in other vaults, but its unique
value is a risk ladder for operational hardening. Compared with `OSSU`, it is
not a curriculum with selection criteria; compared with `CS-Notes`, it is less
of a second brain and more of a command runbook corpus.

## Anti-Borrow

- Do not execute or recommend commands without current verification.
- Do not import ideological security recommendations.
- Do not use the difficulty ladder as proof that an action is safe.
- Do not treat old distro/package links as current.

## Candidate Tags

```yaml
domain: operational_guides
problem: organizing_command_heavy_system_guides_with_risk_and_staleness
pattern:
  - rewrite-warning-at-source-boundary
  - security-difficulty-ladder
  - assumption-rich-runbook
  - placeholder-variable-commands
  - destructive-action-inhibition
maturity: small-stale-guide-corpus
problem_fit: 3
reuse_value: 3
implementation_cost: 2
integration_fit: 3
evidence_strength: 3
reversibility: 4
```

## Fusion Judgment

Borrow as a risk/runbook reference, not as technical advice. The VAKS-safe
lesson is how to mark assumptions, difficulty, staleness, and destructive
operations before action.
