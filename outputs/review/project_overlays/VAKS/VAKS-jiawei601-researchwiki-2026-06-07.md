---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
target_ref: outputs/review/2026-06-07-jiawei601-researchwiki-candidate-distillation.md
target_selector: "ResearchWiki as paper intake and research synthesis spine"
target_hint: "paper-intake / Zotero-source-candidate / topic-method-claim-gap / synthesis-lint"
project_borrow_scope:
  - "Borrow specified Zotero collection -> import plan / manifest -> user confirmation -> single-paper intake."
  - "Borrow paper card not endpoint: every paper should route into topic, method, claim, gap, synthesis, index, and log."
  - "Borrow evidence and uncertainty markers for paper claim/gap extraction."
  - "Borrow memory/agents/templates as explicit operating rule layer, not truth layer."
  - "Borrow tag taxonomy, term aliases, and lint as duplicate/evidence hygiene."
  - "Borrow batch synthesis cadence after several related papers."
project_non_borrow_scope:
  - "For VAKS, do not borrow ResearchWiki wiki/claims as reviewed support or action basis."
  - "For VAKS, do not borrow memory/ as truth memory."
  - "For VAKS, do not borrow Obsidian graph links, tags, aliases, or lint pass as evidence support."
  - "For VAKS, do not allow Zotero import to scan the whole library/storage or mutate attachments."
  - "For VAKS, do not treat AI-inferred gaps as real gaps before evidence-aware review."
project_reopen_trigger:
  - "Reopen when VAKS designs Zotero or paper-source candidate intake."
  - "Reopen when VAKS builds academic research scout / paper triage lanes."
  - "Reopen when VAKS implements paper claim/gap extraction or Evidence Packet prefill."
  - "Reopen when VAKS designs synthesis cadence for batches of related sources."
confirmation_basis: "User explicitly identified jiawei601/ResearchWiki and requested distillation into the VAKS vault."
last_checked_at: 2026-06-07
expires_at:
borrow_value: strong
borrow_order:
  - "P1: Zotero scoped import plan + manifest + single-paper gate"
  - "P1: paper card is not endpoint"
  - "P1: topic/method/claim/gap as candidate cross-paper nodes"
  - "P1: evidence/uncertainty marking for claim and gap extraction"
  - "P1: tag/alias/lint hygiene"
  - "P2: batch synthesis after 3-5 related papers"
  - "P2: operator-friendly memory/agents/templates"
  - "P3: Obsidian graph and Quickstart polish"
avoid:
  - "memory as truth"
  - "wiki/claims as reviewed VAKS support"
  - "graph links as relation authority"
  - "full Zotero scan"
  - "AI-inferred gap as reviewed gap"
---

# Project Overlay: VAKS -> ResearchWiki

## Boundary

This is a VAKS-scoped borrowing sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern. It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-07-jiawei601-researchwiki-candidate-distillation.md
source_ref: raw/repos/2026-06-07-jiawei601-researchwiki-source.md
snapshot_ref: raw/repos/_snapshots/jiawei601-ResearchWiki-3f0705087fdd242514f1179bc53518b87a97f02c.zip
target_hint: paper-intake / Zotero-source-candidate / topic-method-claim-gap / synthesis-lint
```

## Project Borrow Scope

For VAKS, borrow ResearchWiki as a paper-intake and research-synthesis reference:

1. `zotero_import_gate`: read only a user-specified collection, produce import plan and manifest, then wait for user confirmation.
2. `single_paper_intake`: confirmed paper enters PDF read / paper-card flow one at a time.
3. `paper_card_not_endpoint`: paper card must route into topic, method, claim, gap, index, log, and later synthesis.
4. `claim_gap_prefill`: paper intake may pre-fill claim/gap candidates with evidence anchors and AI-inference labels.
5. `batch_synthesis`: after several related papers, run synthesis, gap analysis, review outline, and lint.
6. `rule_layer`: use memory/agents/templates as explicit local operating instructions.
7. `hygiene_lint`: tag taxonomy, term aliases, duplicate-page checks, missing claim source checks, and missing gap-evidence checks.

Best one-line borrowing:

```text
ResearchWiki 教我们把论文从“单篇摘要”推进到“候选结构图”，但不要跳过 VAKS 的 review gate。
```

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

- `wiki/claims` as reviewed support, reviewed relation, truth confidence, or action basis.
- `memory/` as truth memory.
- `paper card created` as knowledge promotion.
- `synthesis page created` as review pass.
- `lint pass` as evidence support.
- `graph link` as reviewed relation.
- full Zotero library/storage scan.
- direct Zotero item/PDF mutation.
- AI-inferred gap as real/reviewed gap.

Plain-language warning:

```text
这个库很适合教我们怎么吃论文。
它不能替我们判定论文里的主张已经通过 VAKS 复核。
```

## Reopen Trigger

Reopen this overlay when VAKS is working on:

- Zotero connector / collection import.
- paper source candidate queue.
- PDF/paper medium or heavy intake.
- academic research scout.
- claim/gap Evidence Packet prefill.
- literature map / related work generation.
- alias/tag/duplicate lint for candidate points.

## Confirmation

```yaml
confirmation_basis: "User explicitly identified jiawei601/ResearchWiki and requested distillation into the VAKS vault."
last_checked_at: 2026-06-07
expires_at:
```

## Borrow Gradient

```yaml
borrow_value: strong
P1:
  - Zotero scoped import plan and manifest
  - user confirmation before paper intake
  - paper card is not endpoint
  - topic/method/claim/gap candidate graph
  - evidence and uncertainty marking
  - tag/alias/lint hygiene
P2:
  - batch synthesis after related papers accumulate
  - review-outline / research-positioning surfaces
  - memory/agents/templates as operator UX
P3:
  - exact folder layout
  - Obsidian graph view
  - README/Quickstart wording
avoid:
  - memory as truth
  - claim page as reviewed support
  - graph/link count as relation quality
  - full Zotero scan
  - automatic promotion from paper card
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
