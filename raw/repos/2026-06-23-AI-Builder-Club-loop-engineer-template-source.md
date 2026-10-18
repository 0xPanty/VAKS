---
type: source
record_kind: source_card
status: source-captured
title: "AI-Builder-Club/loop-engineer-template"
source_id: github-AI-Builder-Club-loop-engineer-template
source_uri: https://github.com/AI-Builder-Club/loop-engineer-template
source_url: https://github.com/AI-Builder-Club/loop-engineer-template
source_type: repository
author: AI-Builder-Club
publisher: GitHub
published_at: 2026-06-14T13:47:44Z
updated_at: 2026-06-22T18:48:54Z
captured_at: 2026-06-23T02:54:55+08:00
captured_by: Codex
version_or_commit: a2267355209713a2184eaeef3b276ec680219d2b
source_integrity:
  source_hash: a2267355209713a2184eaeef3b276ec680219d2b
  snapshot_hash: E3173F420D3203CD48A7AADEAD8182868490A6F83B95403F706FA6DDB2AE8A93
  ingest_state: new
adapter_ingest:
  adapter_name: git-clone-and-archive
  adapter_version: git archive
  capture_method: "git clone --depth 1, GitHub API metadata, then git archive HEAD"
  extraction_trace: "local inspection of README, ARCHITECTURE.md, CLAUDE.md, LOG.md, folder schemas, Claude skills, dev-local template, and ship-change workflow"
  known_limits:
    - "No loop was executed during this intake."
    - "No Claude Code skill execution or workflow execution was performed."
    - "No external video or AI Builder Club course content was consumed; only this public repository and GitHub API metadata were inspected."
    - "GitHub stars, forks, language, and issue counts are volatile metadata captured at intake time only."
    - "README and template claims were not independently validated beyond repository/source inspection."
source_status: active
raw_location: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
processing_tier: medium
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
review_priority: normal
review_owner: Codex
formalization_status: raw-only
why_saved: "User asked to also distill AI-Builder-Club/loop-engineer-template after distilling Agent-Loop-Skills, to cover current Loop Engineer style agent workflows in the VAKS knowledge base."
topics:
  - agentic-loops
  - loop-engineer
  - file-based-agent-memory
  - codebase-harness
  - verify-before-pr
  - claude-code-skills
projects:
  - verified-action-knowledge-system
source_family:
  - repository
  - agent-template
  - loop-engineering
upstream_sources: []
verification_status: source_snapshot_captured
candidate_relation_suggestions: []
tags:
  - repo-intake
  - loop-engineer
  - agentic-loops
  - candidate-only
---

# 来源记录：AI-Builder-Club/loop-engineer-template

## 为什么收录

用户在完成 `gaasher/Agent-Loop-Skills` 蒸馏后，继续要求蒸馏 `AI-Builder-Club/loop-engineer-template`。

本记录只保存来源身份、源码快照和初步看点。它不代表 VAKS 已经采纳该模板，也不代表其中的 README 叙述、Claude Code skill 设计、GitHub 热度或课程入口可以作为 evidence support、reviewed knowledge 或 action basis。

## 来源信息

- 作者/组织：AI-Builder-Club
- 发布方：GitHub
- 原始链接：https://github.com/AI-Builder-Club/loop-engineer-template
- 版本 / commit：`a2267355209713a2184eaeef3b276ec680219d2b`
- commit 时间：`2026-06-18T23:59:11+10:00`
- commit subject：`README: use custom clickable video thumbnail`
- GitHub created_at：`2026-06-14T13:47:44Z`
- GitHub pushed_at：`2026-06-18T13:59:12Z`
- license：none declared in GitHub API metadata
- source_status：active
- 采集方式：`git clone --depth 1` + GitHub API metadata + `git archive HEAD`
- 本地快照：`raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip`
- 快照 SHA256：`E3173F420D3203CD48A7AADEAD8182868490A6F83B95403F706FA6DDB2AE8A93`
- GitHub metadata snapshot：stars `186`, forks `36`, open issues `0`, language `JavaScript`, default branch `main` at intake time only.

## Intake Boundary

```yaml
processing_tier: medium
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

Source records provide provenance and findability. They must not carry adopt/reject verdicts, truth scores, project borrowing conclusions, or action basis.

## Inspected Repository Areas

| Area | Anchor | Why inspected |
|---|---|---|
| Project framing | `README.md:3-6`, `README.md:8-26`, `README.md:32-54`, `README.md:56-77` | Confirms the repo frames a loop engineer as an agent that wakes on triggers, works, verifies, logs, and compounds through shared file memory plus a codebase harness. |
| Knowledge substrate | `ARCHITECTURE.md:16-25`, `ARCHITECTURE.md:27-37`, `ARCHITECTURE.md:54-66`, `ARCHITECTURE.md:68-83` | Confirms the minimal two-kind model, domain-as-loop README, append-only timeline, global log, deterministic metrics collectors, and DRY/MECE rules. |
| Deferral boundary | `ARCHITECTURE.md:87-99`, `ARCHITECTURE.md:103-126` | Confirms it explicitly defers trigger fields, recursive threads, entity kinds, derived indexes, reconcile daemons, and autonomy guardrails until real need exists. |
| Agent operating context | `CLAUDE.md:1-6`, `CLAUDE.md:42-64`, `CLAUDE.md:66-79` | Confirms `CLAUDE.md` is designed as tight recurring context, with domain README state and worktree discipline for code work. |
| Folder schemas | `signals/README.md:1-36`, `docs/README.md:1-30`, `domains/README.md:1-47`, `LOG.md:1-29` | Confirms each folder README acts as schema, with signal frequency, docs as durable knowledge, domain run-log, and strict LOG entry grammar. |
| New loop skill | `.claude/skills/new-loop/SKILL.md:6-17`, `.claude/skills/new-loop/SKILL.md:19-31`, `.claude/skills/new-loop/SKILL.md:33-79` | Confirms new domains are scaffolded through a skill, must perform one real test run, and must record to both domain Timeline and LOG.md. |
| Codebase harness | `.claude/skills/setup-codebase-harness/SKILL.md:13-24`, `.claude/skills/setup-codebase-harness/SKILL.md:35-51`, `.claude/skills/setup-codebase-harness/SKILL.md:55-72`, `.claude/skills/setup-codebase-harness/SKILL.md:85-90` | Confirms the harness pattern: legible, executable, verifiable, with map-not-manual docs, mechanical lints, reproducible dev stack, e2e, and PR verification. |
| Dev launcher | `.claude/skills/dev-local-setup/SKILL.md:13-21`, `.claude/skills/dev-local-setup/SKILL.md:23-47`, `.claude/skills/dev-local-setup/assets/dev-local.template.sh:1-18`, `.claude/skills/dev-local-setup/assets/dev-local.template.sh:49-72`, `.claude/skills/dev-local-setup/assets/dev-local.template.sh:92-138` | Confirms one-command tmux dev stack scaffold, preflight, idempotent windows, status/log/restart/attach commands, and a no-secrets boundary. |
| E2E gate | `.claude/skills/e2e-setup/SKILL.md:12-16`, `.claude/skills/e2e-setup/SKILL.md:23-49`, `.claude/skills/e2e-setup/SKILL.md:50-64` | Confirms system-level testing through real flows, video/trace proof, layered assertions, stable selectors, fresh data, and failure triage. |
| PR verification | `.claude/skills/pr/SKILL.md:11-24`, `.claude/skills/pr/SKILL.md:26-65`, `.claude/skills/pr/SKILL.md:67-89` | Confirms verify-before-PR: feature proof by fresh read-only verifier, then objective regression checks, then PR body with proof. |
| Ship workflow | `.claude/workflows/ship-change.js:1-14`, `.claude/workflows/ship-change.js:48-77`, `.claude/workflows/ship-change.js:118-137`, `.claude/workflows/ship-change.js:150-199`, `.claude/workflows/ship-change.js:216-253`, `.claude/workflows/ship-change.js:255-309` | Confirms an end-to-end worktree -> implement -> simplify -> review -> verify -> PR workflow, with degraded Codex review and `/pr` delegation when present. |

## 初步看点

- This is not mainly a library of loop algorithms. It is a template for making agent loops operational in a repo.
- Its strongest idea is a small shared-memory substrate:

```text
signals/ = repeated observations and feedback
docs/ = durable analysis and decisions
domains/ = loop state, cadence, backlog, metrics links, timeline
LOG.md = global short activity feed
```

- It separates artifact ownership by kind from loop ownership by domain field. This is highly relevant to VAKS because it avoids putting every object under a workstream folder and instead keeps cross-cutting artifacts linkable.
- It adds a concrete code-shipping harness:

```text
map-not-manual docs
mechanical lints
one-command dev stack
real e2e gate
fresh verifier sub-agent
PR proof
worktree isolation
```

## 明显疑点

- The repository is a template and public teaching artifact. It does not prove the template works in the user's environment.
- It assumes Claude Code skills/workflows. Codex can borrow concepts, but not assume Claude runtime semantics.
- The two-kind `signal/doc` substrate is intentionally minimal, but VAKS already has stricter raw/candidate/reviewed/action-basis boundaries. Do not collapse VAKS layers into this simplified model.
- Append-only timelines and LOG entries prove that something was recorded, not that the recorded conclusion is true.
- GitHub popularity and current "loop engineer" hype are discovery signals only, not quality proof.

## 可抽取 Candidate Points

- Minimal loop knowledge substrate: kinds by artifact type, domains as loop state, no premature task/entity/index layers.
- Append-only per-artifact Timeline plus short global LOG as operational memory.
- Domain README as live charter, backlog, evidence links, metrics, and run-log.
- Codebase harness as legible/executable/verifiable preparation for autonomous code work.
- Verify-before-PR with independent app-driving verifier and objective regression checks.

## Not Promoted

This source is not promoted to:

```text
wiki/claims
wiki/patterns
wiki/decisions
reviewed knowledge
Evidence Packet
action basis
```

