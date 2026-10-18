---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "fmhy/edit"
source_url: "https://github.com/fmhy/edit"
checked_commit: "bff3e076091b2632e5bc8afee86d1d624c71f6a7"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/fmhy-edit-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/fmhy-edit-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/fmhy-edit-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
borrow_order: P2
routing_hint:
  - community_directory_review
fit_layer:
  - source-scouting
  - feedback
  - vault-health
  - publishing
  - risk
not_fit_layer:
  - reviewed-knowledge
  - evidence-support
  - action-basis
avoid:
  - "Do not import high-risk directory content into VAKS knowledge."
  - "Do not treat community stars, approvals, backups, or link presence as evidence support."
  - "Do not route VAKS truth changes through external feedback/webhook systems."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing contribution intake, duplicate checks, feedback routing, removal ledgers, or directory-specific lint."
  support_when: "When comparing issue templates, contribution bans, single-page search surfaces, recently removed generation, and VitePress publication."
  risk_when: "When community directory signals could be confused with reviewed knowledge or action readiness."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/fmhy-edit-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - feedback
  - directory-governance
---

# Strong Candidate Distillation: fmhy / edit

## What This Source Actually Is

This is the editing/build repository for a very large public link directory. It
uses VitePress, a Nitro/Cloudflare API, contribution templates, feedback intake,
markdown lint, single-page generation, removed-entry generation, and strict
community contribution rules. The content itself is high-risk and not reusable
as VAKS knowledge.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `.github/README.md` | Project overview, backups, contribution reminders, duplicate search. | Directory governance needs public intake instructions. | Link directory is not evidence. |
| `.github/CONTRIBUTING.md` | Submission bans, duplicate checks, reporting, testing, editing workflows. | Intake should say what not to submit. | Community fit is not truth. |
| `wiki.yml` issue template | Structured issue type/context. | Feedback should be typed and scoped. | Issue is not review. |
| `feedback.post.ts` and `Feedback.ts` | Validated feedback, page/heading/type, rate limit, webhook delivery. | Feedback intake needs schema and abuse control. | Feedback does not mutate truth. |
| `generate-single-page.js` | Aggregates directory pages for whole-site search. | Single-page search surfaces help dedup. | Generated page is projection. |
| `generate-removed.js` | Uses git history to list removed entries. | Removal ledgers can preserve negative/removed context. | Removed entry is not global ban. |
| `lint-markdown.js` | Domain-specific markdown lint. | Directory conventions can be machine-checked. | Lint is not evidence review. |
| `docs/.vitepress/config.mts` | VitePress, RSS, PWA, meta, markdown transforms, build hooks. | Publication/runtime surfaces should be explicit. | Build output is not canonical. |

## Strong Borrow Points

1. **Contribution intake should include negative rules.**  
   The contribution guide is valuable because it explicitly lists what should
   not be submitted and when discussion is required before a PR.

2. **Duplicate search needs a single-page projection.**  
   The generated single-page Markdown surface is a practical way to support
   `Ctrl+F` duplicate checks without making it canonical.

3. **Removal ledgers are useful review input.**  
   The recently removed generator preserves deleted links with commit context.
   VAKS can adapt this for source retirement and known-bad candidate history.

4. **Feedback needs schema, scope, and rate limits.**  
   Page, heading, type, message validation, and rate limiting are useful for
   VAKS feedback events. Routing to external chat is only process input.

5. **Domain-specific lint is worth borrowing.**  
   The markdown lint checks conventions that generic formatters miss. VAKS can
   use this pattern for source cards, candidate files, and maintenance manifests.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Source Scouting | Directory contribution and duplicate checks. | Adapt cautiously. |
| Feedback | Typed, scoped, rate-limited feedback. | Strong adaptation. |
| Vault Health | Domain markdown lint and removal ledgers. | Strong diagnostic pattern. |
| Publishing | VitePress build and generated surfaces. | Projection only. |
| Reviewed Knowledge | None directly. | Reject. |

## Local De-Dup / Collision

This overlaps with Interneto as a directory source. FMHY is stronger for
community governance, duplicate checks, feedback routing, and removal history;
Interneto is stronger for agent-facing architecture and typed catalog workbench.

## Fusion Judgment

Borrow as P2 for contribution guardrails, duplicate search, removal ledger,
feedback schema, and domain-specific lint. Reject directory content and
community popularity signals as evidence support.
