---
type: source
status: source-captured
title: evil-read-arxiv
source_id: github-juliye2025-evil-read-arxiv
source_uri: github:juliye2025/evil-read-arxiv@31bca2e56bfc2439e2d93384a238bd20502c2a77
source_url: https://github.com/juliye2025/evil-read-arxiv
source_type: repository
owner: juliye2025
repo: evil-read-arxiv
checked_commit: 31bca2e56bfc2439e2d93384a238bd20502c2a77
commit_time: 2026-06-01T20:30:17+08:00
commit_subject: "Merge pull request #27 from YannickYang/main"
captured_at: 2026-06-07 05:14:45 +08:00
captured_by: Codex
version_or_commit: 31bca2e56bfc2439e2d93384a238bd20502c2a77
source_status: active
raw_location: raw/repos/2026-06-07-juliye2025-evil-read-arxiv-source.md
snapshot_ref: raw/repos/_snapshots/juliye2025-evil-read-arxiv-31bca2e56bfc2439e2d93384a238bd20502c2a77.zip
snapshot_sha256: 791F09A89E567D34FED4436E61375ACF94A5F82E633498FDE11F50FDA7CC8471
processing_mode: repo-intake
processing_level: heavy
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: high
review_owner: Codex
formalization_status: raw-only
topics:
  - arxiv-paper-scouting
  - academic-source-intake
  - semantic-scholar
  - dblp-conference-scouting
  - obsidian-paper-workbench
  - feedback-preference-learning
projects:
  - verified-action-knowledge-system
source_family: academic-paper-scouting-workbench
upstream_sources:
  - arXiv API
  - Semantic Scholar API
  - DBLP API
  - PubMed
verification_status: source-code-inspected
candidate_relation_suggestions:
  - target: "[[2026-06-07-juliye2025-evil-read-arxiv-candidate-distillation]]"
    relation_type: derived_from
    relation_state: candidate
    why_suggested: "The repository provides a paper-source discovery, scoring, workbench, and feedback loop that can be compared with VAKS source intake and future research scouting."
tags:
  - raw-repo
  - github
  - candidate-only
---

# 来源记录：evil-read-arxiv

## 为什么收录

用户明确要求对 `juliye2025/evil-read-arxiv` 做强蒸馏，并判断它可能是资料库未来自动学习、自动找资料的路径。

本记录只固定来源、commit、快照和代码锚点。它不代表采纳结论、真值判断、review verdict、action basis 或主线架构变更。

## 来源信息

- 作者 / owner: `juliye2025`
- 仓库：`evil-read-arxiv`
- 原始链接：<https://github.com/juliye2025/evil-read-arxiv>
- 检查 commit：`31bca2e56bfc2439e2d93384a238bd20502c2a77`
- commit time：`2026-06-01T20:30:17+08:00`
- commit subject：`Merge pull request #27 from YannickYang/main`
- source_status: active
- snapshot: `raw/repos/_snapshots/juliye2025-evil-read-arxiv-31bca2e56bfc2439e2d93384a238bd20502c2a77.zip`
- snapshot SHA256: `791F09A89E567D34FED4436E61375ACF94A5F82E633498FDE11F50FDA7CC8471`
- license: not found in inspected file list

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

Source records provide provenance and findability. They do not carry adoption verdicts, truth confidence, reviewed relation strength, project decision, or action basis.

## Source / Code Anchor Matrix

| Anchor | What exists | Why inspected | Boundary |
|---|---|---|---|
| `README.md:24` | `start-my-day` daily paper recommendation feature list | Top-level workflow intent | README claim |
| `README.md:56` | `conf-papers` top-conference search feature list | Confirms DBLP + S2 conference scouting path | README claim |
| `README.md:63` | Web app feature list | Confirms workbench, summaries, feedback, favorites | README claim |
| `README.md:351` | Four-dimensional scoring mechanism | Identifies scoring semantics | Heuristic, not evidence quality |
| `README.md:426` | End-to-end working principle diagram | Confirms source discovery -> score -> note -> analyze loop | Public documentation |
| `config.example.yaml:6` | Language, vault path, papers dir, S2 key fields | Configuration surface | User-specific config, not schema for VAKS |
| `config.example.yaml:24` | Research domains with keywords, categories, priority | Query generation source | Candidate scouting config only |
| `config.example.yaml:206` | Excluded keywords and common-word filters | Negative filters | Filtering, not review |
| `start-my-day/SKILL.md:54` | Daily paper workflow overview | Skill-level operator sequence | Claude Code skill contract |
| `start-my-day/SKILL.md:190` | Daily recommendation note generation rules | Shows vault output shape | Obsidian workflow reference |
| `start-my-day/SKILL.md:329` | Top 3 papers get images and deep analysis | Escalation path from recommendation to detail | Not evidence-aware review |
| `start-my-day/SKILL.md:413` | Scan existing notes then auto-link keywords | Existing-note activation idea | Lexical link, not reviewed relation |
| `start-my-day/scripts/search_arxiv.py:40` | arXiv/Semantic Scholar constants and weights | Search and scoring primitives | Runtime code inspected, not executed |
| `start-my-day/scripts/search_arxiv.py:108` | Load research YAML and fallback config | Config ingestion | Fallback defaults are not project rules |
| `start-my-day/scripts/search_arxiv.py:168` | arXiv date-range search | Recent-source discovery | API result, not completeness guarantee |
| `start-my-day/scripts/search_arxiv.py:229` | arXiv keyword focus search | User-focus discovery path | Keyword search only |
| `start-my-day/scripts/search_arxiv.py:301` | Semantic Scholar hot-paper search | Older / influential paper discovery | Citation count is not truth |
| `start-my-day/scripts/search_arxiv.py:432` | S2 hot papers from categories / user queries | Broader query fan-out | Query heuristic |
| `start-my-day/scripts/search_arxiv.py:515` | arXiv XML parser | Source metadata extraction | Parses API metadata only |
| `start-my-day/scripts/search_arxiv.py:619` | Relevance scoring | Interest matching | Heuristic signal |
| `start-my-day/scripts/search_arxiv.py:732` | Quality score from abstract words | Quality-like signal | Weak proxy, not review |
| `start-my-day/scripts/search_arxiv.py:830` | Filter and score papers | Candidate ranking | Ranking only |
| `start-my-day/scripts/search_arxiv.py:937` | CLI main, focus mode, normal mode, merge, dedupe, output JSON | Full daily scouting runtime | Inspected only |
| `start-my-day/scripts/scan_existing_notes.py:93` | Scan existing Markdown notes | Local prior-context index | Activation input |
| `start-my-day/scripts/scan_existing_notes.py:154` | Build keyword-to-note index | Association surface | Not reviewed relation |
| `start-my-day/scripts/link_keywords.py:19` | Markdown line parser skips frontmatter/code/links | Safer wikilink insertion | Formatting helper |
| `start-my-day/scripts/link_keywords.py:118` | Keyword linking logic with single-note guard | Auto-association mechanism | Lexical only |
| `paper-analyze/SKILL.md:78` | Get PDF/source/metadata for a paper | Per-paper source expansion | Skill instruction, not executed |
| `paper-analyze/SKILL.md:237` | Generate comprehensive paper note and graph update | Downstream note path | Template workflow |
| `paper-analyze/scripts/generate_note.py:29` | Bilingual paper-note templates | Structured note skeleton | Placeholder content |
| `paper-analyze/scripts/update_graph.py:28` | JSON paper graph node/edge update | Simple graph persistence | Not VAKS reviewed relation |
| `extract-paper-images/scripts/extract_images.py:33` | Download and safely extract arXiv source tarball | Source artifact enhancement | Source artifact only |
| `extract-paper-images/scripts/extract_images.py:119` | PDF image extraction fallback | Image fallback path | Visual extraction, not paper understanding |
| `extract-paper-images/scripts/extract_images.py:221` | End-to-end image extraction CLI | Image cache/index output | Inspected only |
| `conf-papers/SKILL.md:10` | DBLP + S2 top-conference workflow | Conference scouting lane | Skill contract |
| `conf-papers/SKILL.md:317` | Rules, error handling, differences from daily search | Operational boundary | Not VAKS rule |
| `conf-papers/scripts/search_conf_papers.py:44` | Reuses daily scoring, defines venues and weights | Conference scorer construction | Heuristic |
| `conf-papers/scripts/search_conf_papers.py:114` | DBLP conference search | Venue-source discovery | API result, not exhaustive guarantee |
| `conf-papers/scripts/search_conf_papers.py:311` | Lightweight title keyword filter | API-cost control gate | May miss useful papers |
| `conf-papers/scripts/search_conf_papers.py:384` | S2 enrichment with title similarity check | Adds abstract/citations/arXiv ID | Match threshold heuristic |
| `conf-papers/scripts/search_conf_papers.py:540` | Three-dimensional scoring | Conference ranking | Heuristic |
| `conf-papers/scripts/search_conf_papers.py:621` | Main conf-papers runtime | Full conference scouting pipeline | Inspected only |
| `paper-search/scripts/paper_hunter.py:23` | Legacy hunter reads config and writes paper notes | Direct source-to-vault path | Too loose for VAKS truth layer |
| `web/src/lib/python-bridge.ts:64` | Next.js calls Python search script | Web-to-Python bridge | Uses shell exec, needs hardening before adoption |
| `web/src/lib/data.ts:16` | Data dirs, cache dirs, config path | Local persistence model | App-local state |
| `web/src/lib/data.ts:42` | Feedback, preferences, paper cache, analysis cache, images | Workbench memory surface | Not reviewed knowledge |
| `web/src/lib/anthropic.ts:41` | API key / base URL resolution | LLM provider setup | Secret handling surface |
| `web/src/app/api/papers/route.ts:17` | AI summaries | Title/abstract summary layer | Not full-paper review |
| `web/src/app/api/papers/route.ts:85` | Auto-add research domain from focus search | Self-updating search config | Needs review gate |
| `web/src/app/api/papers/route.ts:174` | Papers GET route: cache, search, summarize, merge feedback | Main web source-discovery route | Candidate workbench |
| `web/src/app/api/papers/filter/route.ts:7` | LLM semantic re-ranking of cached papers | Human-focus narrowing | LLM score not authority |
| `web/src/app/api/preferences/update/route.ts:12` | Feedback-driven preference update | Preference learning loop | Must stay quarantined |
| `web/src/app/api/papers/[id]/analyze/route.ts:7` | On-demand four-field paper analysis | Lightweight analysis route | Based on title/abstract fallback |
| `web/src/app/api/papers/[id]/images/route.ts:18` | On-demand image extraction route | Visual workbench support | Uses shell exec |
| `web/src/app/api/feedback/route.ts:5` | Like/neutral/dislike feedback API | Explicit use feedback capture | Usefulness signal only |
| `web/src/lib/i18n.ts:180` | Summary/analyze/filter/domain/translate prompts | Prompt layer for AI workbench | Prompt output only |
| `web/src/components/PapersContext.tsx:53` | Shared paper/search/filter state | UI workflow state | Interface behavior |
| `web/src/app/papers/page.tsx:153` | Feedback advances paper and triggers preference update | Reading workflow loop | Feedback not truth |
| `web/src/components/PaperCard.tsx:20` | Paper card loads images, deep dive, feedback | Main paper inspection surface | UI only |
| `web/src/app/api/settings/route.ts:6` | Settings read/write with masked API key | User-config workbench | Needs privacy discipline |

## Retained Artifacts

```yaml
source_card: raw/repos/2026-06-07-juliye2025-evil-read-arxiv-source.md
snapshot_ref: raw/repos/_snapshots/juliye2025-evil-read-arxiv-31bca2e56bfc2439e2d93384a238bd20502c2a77.zip
snapshot_sha256: 791F09A89E567D34FED4436E61375ACF94A5F82E633498FDE11F50FDA7CC8471
candidate_distillation: outputs/review/2026-06-07-juliye2025-evil-read-arxiv-candidate-distillation.md
architecture_review: wiki/summaries/2026-06-07-juliye2025-evil-read-arxiv-architecture-review.md
project_overlay: outputs/review/project_overlays/VAKS/VAKS-evil-read-arxiv-2026-06-07.md
```

## Non-Claims

- This record does not verify that arXiv, S2, DBLP, or PubMed returned complete or current results.
- This record does not execute the app or scripts.
- This record does not validate generated paper summaries.
- This record does not treat recommendation score, citation count, LLM summary, feedback count, or graph edge as evidence support.
- This record does not approve automatic VAKS learning, automatic truth mutation, or automatic promotion.
