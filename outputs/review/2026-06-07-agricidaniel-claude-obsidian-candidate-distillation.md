---
record_kind: candidate_distillation
type: review-candidate
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
derived_from:
  - raw/repos/2026-06-07-agricidaniel-claude-obsidian-source.md
  - raw/repos/_snapshots/AgriciDaniel-claude-obsidian-cb93ff6d82f9c35a08bf6010e7fac36dfddc827b.zip
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
project: verified-action-knowledge-system
scope: agricidaniel-claude-obsidian-repo-distillation
source_commit: cb93ff6d82f9c35a08bf6010e7fac36dfddc827b
source_checked_at: 2026-06-07
borrow_value: strong
borrow_order:
  - "P1: skill catalog as explicit agent action surface"
  - "P1: hot/index/log recovery spine"
  - "P1: per-file locking plus hook gates for AI writes"
  - "P2: local-first hybrid retrieval with explicit egress consent"
  - "P2: methodology mode router as filing-policy layer"
  - "P2: lint/verifier reports as maintenance diagnostics"
  - "P3: canvas, autoresearch, and thinking-loop UI/workflow layer"
avoid:
  - "Do not auto-promote generated wiki pages into reviewed knowledge."
  - "Do not default to auto-research, web egress, auto-commit, or broad vault writes."
  - "Do not treat hot cache, index, retrieval score, lint report, or dashboard as action basis."
  - "Do not copy one filing methodology as a global VAKS default."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS skill runtime, AI file-write safety, Obsidian workbench, or retrieval/cache pipeline."
  support_when: "Comparing implementation-level AI second-brain / Obsidian tooling references."
  risk_when: "Any proposal uses auto-ingest, auto-research, auto-commit, broad vault writes, or retrieval scores as authority."
  cold_references:
    - raw/repos/2026-06-07-agricidaniel-claude-obsidian-source.md
    - raw/repos/_snapshots/AgriciDaniel-claude-obsidian-cb93ff6d82f9c35a08bf6010e7fac36dfddc827b.zip
routing_hint:
  - source-intake
  - activation-tier
  - dev-context
  - agent-write-safety
  - retrieval-cache
  - obsidian-workbench
possible_project_refs:
  - DEV_CONTEXT.md
  - MEMORY_TIER.md
  - SOURCE_INTAKE.md
  - FEEDBACK.md
  - outputs/review/project_overlays/VAKS/VAKS-agricidaniel-claude-obsidian-2026-06-07.md
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/AgriciDaniel-claude-obsidian-cb93ff6d82f9c35a08bf6010e7fac36dfddc827b.zip
    selector_type: file-lines
    selector_value: README.md:20-27
  - snapshot_ref: raw/repos/_snapshots/AgriciDaniel-claude-obsidian-cb93ff6d82f9c35a08bf6010e7fac36dfddc827b.zip
    selector_type: file-lines
    selector_value: skills/wiki-ingest/SKILL.md:50-82
  - snapshot_ref: raw/repos/_snapshots/AgriciDaniel-claude-obsidian-cb93ff6d82f9c35a08bf6010e7fac36dfddc827b.zip
    selector_type: file-lines
    selector_value: skills/wiki-retrieve/SKILL.md:15-24
tags:
  - candidate
  - provisional
  - repo-distillation
  - claude-obsidian
  - agent-skills
  - obsidian
borrow_tags:
  - P1/skill_catalog_as_action_surface
  - P1/hot_index_log_recovery_spine
  - P1/per_file_locking_for_ai_writes
  - P2/local_first_retrieval_with_egress_gate
  - P2/methodology_router_as_filing_policy
  - P2/lint_verifier_as_diagnostics
  - P3/canvas_autoresearch_thinking_layer
do_not_borrow_tags:
  - avoid/generated_wiki_as_reviewed_truth
  - avoid/auto_research_default
  - avoid/auto_commit_default
  - avoid/broad_vault_write_default
  - avoid/retrieval_score_as_authority
---

# AgriciDaniel Claude Obsidian Candidate Distillation

## Boundary

This is candidate orientation from a public GitHub repository.

It is not reviewed knowledge, not a VAKS architecture decision, not a formal pattern, and not action basis.

It does not install the plugin, connect Claude to Obsidian, enable web egress, run hooks, start auto-research, or grant any vault access.

## Plain-Language Takeaway

说人话：

```text
这个 repo 对我们最有用的不是“又一个 Obsidian AI 笔记库”。

它有用在于：
把 AI 怎么读资料、写笔记、查旧内容、维护索引、避免多 agent 写乱文件，
做成了一组实际文件、skills、hooks、scripts 和 tests。
```

对 VAKS 来说，它是一个实现级参考，不是主架构替代品。

VAKS 已经有：

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

这个 repo 补的是工具层细节：

```text
怎么把 skill 暴露给 agent；
怎么让 session 从 hot cache 恢复；
怎么让 AI 写文件更不容易写炸；
怎么把检索当缓存而不是当真理；
怎么把 PARA / LYT / Zettelkasten 放到路由层，而不是绑死系统。
```

## 借鉴标签

```yaml
P1:
  - skill_catalog_as_action_surface
  - hot_index_log_recovery_spine
  - per_file_locking_for_ai_writes
P2:
  - local_first_retrieval_with_egress_gate
  - methodology_router_as_filing_policy
  - lint_verifier_as_diagnostics
P3:
  - canvas_autoresearch_thinking_layer
avoid:
  - generated_wiki_as_reviewed_truth
  - auto_research_default
  - auto_commit_default
  - broad_vault_write_default
  - retrieval_score_as_authority
```

## Source Comprehension

### What The Repo Is Really About

The repository implements a Claude Code + Obsidian wiki system:

```text
source files / URLs / sessions
-> agent skills
-> generated wiki pages
-> index / hot cache / log
-> query / lint / retrieval / save / canvas / autoresearch
```

The operational spine is:

```text
.raw/ = source documents
wiki/ = generated wiki
wiki/index.md = master catalog
wiki/hot.md = recent context cache
wiki/log.md = append-only operation log
skills/ = agent action modules
scripts/ = transport, lock, retrieval, route helpers
hooks/ = session/load/save/commit automation
tests/ = hermetic checks for lock/retrieval/mode/cache behavior
```

### What It Is Not

It is not:

```text
a verified truth system
a VAKS-compatible reviewed knowledge schema
a safe default for broad Obsidian writes
a proof that auto-research should be turned on
a reason to make hot cache / retrieval score / lint output action basis
```

Its own `wiki/` layer is agent-generated knowledge. In VAKS terms, that maps closer to raw/candidate/context than to reviewed/action-ready knowledge.

## Candidate Points

### 1. skill_catalog_as_action_surface

Candidate point:

```text
Agent skills can be treated as explicit action surfaces: each skill has trigger
words, scope, workflow expectations, and fallbacks.
```

Source anchors:

```text
AGENTS.md:29-38
README.md:173-193
skills/wiki/SKILL.md:105-124
```

VAKS fit:

```text
Strong fit for future VAKS skill runtime and intake helper design.
```

Boundary:

```text
Trigger words are routing signals, not permission. VAKS still requires explicit
intake words before writing files or syncing Obsidian.
```

Route:

```text
candidate point
possible future pattern: skill-catalog-as-action-surface
```

### 2. hot_index_log_recovery_spine

Candidate point:

```text
A small hot/index/log spine can restore recent context, keep a master catalog,
and preserve operation chronology without crawling the whole vault.
```

Source anchors:

```text
README.md:287-315
README.md:569-570
WIKI.md:143-185
hooks/hooks.json:3-17
```

VAKS fit:

```text
Strong fit for Activation Tier, handoff recovery, and dev-context startup.
```

Boundary:

```text
hot.md is activation state. index.md is navigation. log.md is operation history.
None of them is reviewed knowledge or action basis.
```

Route:

```text
candidate point
possible route: activation-cache-not-truth
```

### 3. raw_generated_split_needs_review_gate

Candidate point:

```text
The repo separates `.raw/` sources from generated `wiki/` pages, but VAKS needs
an additional candidate/reviewed/action-basis split before using generated pages.
```

Source anchors:

```text
skills/wiki/SKILL.md:29-54
skills/wiki-ingest/SKILL.md:163-178
WIKI.md:423-486
```

VAKS fit:

```text
Useful as a comparison point: it shows what VAKS should keep and what VAKS must
harden.
```

Boundary:

```text
Generated wiki pages are not reviewed truth. In VAKS, they must route through
candidate distillation and review before promotion.
```

Route:

```text
candidate point
risk route: generated-wiki-as-truth
```

### 4. per_file_locking_for_ai_writes

Candidate point:

```text
AI file writes need per-file locks, path validation, stale-lock recovery, and
hook gates before multi-agent or high-rate write workflows are safe enough to consider.
```

Source anchors:

```text
skills/wiki-ingest/SKILL.md:50-82
hooks/hooks.json:33-50
tests/test_concurrent_write.sh:2-13
tests/test_wiki_lock.sh:129-143
```

VAKS fit:

```text
Very strong for future VAKS automation safety, especially if multiple agents or
helpers ever write the same vault/repo.
```

Boundary:

```text
Locking is a safety primitive, not permission to auto-write. It also does not
replace review, git discipline, or explicit user intent.
```

Route:

```text
candidate point
possible future pattern: per-file-locking-for-ai-writes
```

### 5. retrieval_cache_with_egress_gate

Candidate point:

```text
Retrieval can be a derived cache with tiers: simple hot/index lookup, BM25,
optional contextual prefix, and rerank, with explicit egress gates for off-machine calls.
```

Source anchors:

```text
skills/wiki-query/SKILL.md:49-73
skills/wiki-retrieve/SKILL.md:15-24
skills/wiki-retrieve/SKILL.md:128-178
PRIVACY.md:25-33
scripts/bm25-index.py:2-42
scripts/retrieve.py:128-185
```

VAKS fit:

```text
Strong for activation and context-pack preparation.
```

Boundary:

```text
Retrieval rank, contextual prefix, rerank score, and explain traces are routing
signals only. VAKS action-facing answers still need reviewed support or raw
source anchors.
```

Route:

```text
candidate point
possible route: retrieval-is-activation-not-truth
```

### 6. methodology_router_as_filing_policy

Candidate point:

```text
Filing style can be routed by a mode helper, so PARA / LYT / Zettelkasten /
generic affect where pages go without redefining the whole knowledge system.
```

Source anchors:

```text
README.md:255-272
scripts/wiki-mode.py:2-18
scripts/wiki-mode.py:146-184
skills/wiki-mode/SKILL.md:205-214
```

VAKS fit:

```text
Useful for keeping VAKS from hardcoding one Obsidian methodology as a global
default.
```

Boundary:

```text
Filing mode is UX/workflow policy. It does not change source authority, evidence
support, or review status.
```

Route:

```text
candidate point
possible future pattern: filing-policy-router
```

### 7. lint_verifier_as_diagnostic_not_truth

Candidate point:

```text
Lint and verifier agents are useful as maintenance diagnostics and fresh-review
passes, especially when they ask before auto-fixing and cite file locations.
```

Source anchors:

```text
skills/wiki-lint/SKILL.md:12-18
skills/wiki-lint/SKILL.md:214-230
CLAUDE.md:77-79
agents/verifier.md
```

VAKS fit:

```text
Strong fit with maintenance manifest, review_due pressure, and non-author pass.
```

Boundary:

```text
Diagnostics can create review pressure. They cannot mutate truth, promote
knowledge, or become evidence support.
```

Route:

```text
candidate point
possible route: maintenance-lint-not-truth
```

### 8. autoresearch_program_is_high_risk_without_vaks_boundary

Candidate point:

```text
A configurable autoresearch loop can make research repeatable, but it is high
write-rate, high egress, and easy to over-trust unless outputs stay candidate-only.
```

Source anchors:

```text
skills/autoresearch/SKILL.md:49-64
skills/autoresearch/SKILL.md:74-90
skills/autoresearch/SKILL.md:154-164
skills/autoresearch/references/program.md:9-36
skills/autoresearch/references/program.md:71-72
```

VAKS fit:

```text
Useful as warning and later tool-layer inspiration.
```

Boundary:

```text
VAKS should not default to autonomous research or direct write into reviewed
knowledge. Research outputs start as raw/candidate.
```

Route:

```text
candidate point
risk route: auto-research-default
```

### 9. canvas_as_visual_workbench_not_evidence

Candidate point:

```text
Canvas can be a visual reference/workbench layer for images, PDFs, notes, and
relationship sketches.
```

Source anchors:

```text
skills/canvas/SKILL.md:7-16
skills/canvas/SKILL.md:50-86
wiki/meta/dashboard.base:16-72
```

VAKS fit:

```text
Useful for future workbench/viewer design.
```

Boundary:

```text
Canvas layout, dashboard grouping, and visual adjacency are not evidence
support or reviewed relations.
```

Route:

```text
candidate point
possible future UI/workbench reference
```

### 10. thinking_loop_and_verifier_are_calibration_tools

Candidate point:

```text
A thinking loop and separate verifier can reduce solo-agent bias when the task is
novel, irreversible, or architecture-sensitive.
```

Source anchors:

```text
skills/think/SKILL.md:17-29
skills/think/SKILL.md:73-99
skills/think/SKILL.md:185-200
CLAUDE.md:77-79
```

VAKS fit:

```text
Useful for architecture review windows, non-author passes, and closeout GROW
sections.
```

Boundary:

```text
Better thinking process improves calibration. It does not create evidence
support or truth confidence by itself.
```

Route:

```text
candidate point
possible route: reviewer-pass-as-process-evidence
```

## Candidate Pattern Bank Decision

Do not create a new reviewed pattern from this repo now.

Reason:

```text
The repo is high-value, but the first landing should stay as source card,
candidate distillation, architecture review, and VAKS overlay.
```

Possible future pattern routes if repeated by other implementation sources:

```text
skill-catalog-as-action-surface
hot-index-log-recovery-spine
per-file-locking-for-ai-writes
filing-policy-router
retrieval-cache-with-explicit-egress
lint-report-as-review-pressure
```

## Relation To Existing Local Material

This repo refines several already-seen clusters:

```text
Kepano Obsidian:
  view/workbench/substrate reference; this repo explicitly says it aligns with
  kepano/obsidian-skills for Obsidian primitives.

CyrilXBT / Claude + Obsidian 90-day retrospective:
  practitioner workflow/failure-mode source; this repo is implementation-level
  counterpart with skills/hooks/scripts.

langchain-miniopenclaw:
  local agent workbench / file-first memory reference; this repo is more
  Obsidian-specific and has stronger AI write-safety surfaces.

VAKS source intake control flow:
  confirms the need to keep raw/candidate/overlay/reviewed/action-basis separate.
```

## Candidate Routing Hints

Use this source when designing:

```text
1. VAKS skill trigger and helper layout.
2. Obsidian write helper safety.
3. Hot/warm/cold activation and handoff recovery.
4. Repo/source intake manifests and duplicate skipping.
5. Retrieval/cache layers with egress gates.
6. Project workbench / dashboard / canvas views.
7. Maintenance lint and non-author review flows.
```

Do not use it when answering:

```text
1. Is a claim true?
2. Should VAKS adopt auto-research?
3. Is broad agent vault write access safe?
4. Can retrieval scores support action?
5. Should one Obsidian filing mode become the default for all workspaces?
```

## v0.2.13 Trigger Check

Does this source currently trigger v0.2.13?

```text
action_basis: no
significant promotion: no
significant decision: no
architecture absorption: no
risk-sensitive answer relied on for action: no
explicit "is this enough to act" question: no
```

Result:

```text
v0.2.13 not triggered
```

If a future window uses this repo to justify installing a plugin, enabling web egress, allowing auto-commit, allowing broad vault writes, or changing VAKS reviewed/action-basis behavior, v0.2.13 must run first.

## Suggested Next Step

Keep this as candidate-only implementation reference.

Reopen it when the active task is:

```text
VAKS skill runtime
Obsidian helper safety
agent write locks
retrieval/cache implementation
workbench/dashboard/canvas design
maintenance lint / verifier design
```
