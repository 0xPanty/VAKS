---
type: source
record_kind: source_record
status: source-captured
title: "zhizhuodemao/ai-reverse-toolkit"
source_id: "github:zhizhuodemao/ai-reverse-toolkit@02799de7420ea78c57bf7af8cc0f2d38fef017bd"
source_uri: "https://github.com/zhizhuodemao/ai-reverse-toolkit"
source_url: "https://github.com/zhizhuodemao/ai-reverse-toolkit"
source_type: repository
author: "zhizhuodemao"
publisher: GitHub
published_at: "2026-02-05T09:15:52Z"
updated_at: "2026-06-10T11:31:33Z"
pushed_at: "2026-03-14T10:29:38Z"
captured_at: "2026-06-11"
captured_by: Codex
version_or_commit: "02799de7420ea78c57bf7af8cc0f2d38fef017bd"
checked_commit: "02799de7420ea78c57bf7af8cc0f2d38fef017bd"
checked_commit_time: "2026-03-14T10:29:28Z"
checked_commit_subject: "Add anti-debug reference and missing env-patch references"
language: Python
license: MIT
github_stars_at_capture: 317
github_forks_at_capture: 53
github_open_issues_at_capture: 1
source_integrity:
  source_hash_kind: git_commit
  source_hash: "02799de7420ea78c57bf7af8cc0f2d38fef017bd"
  snapshot_path: "raw/repos/_snapshots/2026-06-11-zhizhuodemao-ai-reverse-toolkit-02799de-source.zip"
  snapshot_sha256: "97A142AA23591129AD4E64152671BCC9AA2D1D2CDDC0AD18EE91DF9CA8EC677E"
  ingest_state: new
adapter_ingest:
  adapter_name: "github-api + public source archive"
  adapter_version: "manual-codex-2026-06-11"
  capture_method: "public GitHub API metadata, git ls-remote, GitHub archive snapshot, local source inspection"
  extraction_trace:
    - "README.md"
    - "CLAUDE.md"
    - "rules/js-reverse.md"
    - "skills/find-crypto-entry/SKILL.md"
    - "skills/env-patch/SKILL.md"
    - "skills/ast-deobfuscate/SKILL.md"
    - "skills/skill-creator/SKILL.md"
    - "skills/env-patch/references/*.md"
  known_limits:
    - "Repository was not executed."
    - "No reverse-engineering operation was performed."
    - "Operational bypass instructions were not adopted into VAKS."
    - "GitHub metadata is a capture-time snapshot and can drift."
source_status: active_public_repo_as_of_capture
raw_location: "raw/repos/_snapshots/2026-06-11-zhizhuodemao-ai-reverse-toolkit-02799de-source.zip"
processing_mode: explicit_distill
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
formalization_status: raw-only
review_priority: medium
review_owner: Codex
topics:
  - ai-assisted-workflow
  - skill-based-agent-process
  - reverse-engineering-methodology
  - progressive-disclosure
  - diagnostic-loop
  - evidence-log
  - eval-driven-skill-improvement
projects:
  - verified-action-knowledge-system
source_family: repo-ai-workflow-toolkit
verification_status: unverified
candidate_outputs:
  - "outputs/review/2026-06-11-zhizhuodemao-ai-reverse-toolkit-candidate-distillation.md"
  - "outputs/review/2026-06-11-ai-reverse-toolkit-general-workflow-patterns.md"
  - "wiki/summaries/2026-06-11-zhizhuodemao-ai-reverse-toolkit-architecture-review.md"
  - "outputs/review/project_lens_overlays/2026-06-11-ai-reverse-toolkit-agent-workflow.md"
tags:
  - source/repo
  - status/raw
  - ai/skill-workflow
  - workflow/diagnostic-loop
  - workflow/evidence-log
  - vaks/process-inspiration
  - boundary/not-action-basis
---

# zhizhuodemao/ai-reverse-toolkit Source Record

## Capture Reason

The user explicitly requested distillation and asked whether `ai-reverse-toolkit`
has borrowable ideas for VAKS while preserving general reusable knowledge.

This source is captured as a repo/workflow reference. It is not reviewed
knowledge, not an action basis, and not authorization to perform security
bypass work.

## Source Identity

- Repository: `zhizhuodemao/ai-reverse-toolkit`
- URL: <https://github.com/zhizhuodemao/ai-reverse-toolkit>
- Checked commit: `02799de7420ea78c57bf7af8cc0f2d38fef017bd`
- Checked commit time: `2026-03-14T10:29:28Z`
- License: MIT
- Snapshot: `raw/repos/_snapshots/2026-06-11-zhizhuodemao-ai-reverse-toolkit-02799de-source.zip`
- Snapshot SHA256: `97A142AA23591129AD4E64152671BCC9AA2D1D2CDDC0AD18EE91DF9CA8EC677E`

## What The Source Is

The repository is a prompt/skill/rule toolkit for AI-assisted reverse
engineering. Its README presents the core idea as encoding reverse-engineering
experience into AI-executable instructions: tools provide hands, skills provide
the decision process.

Source anchors:

| Anchor | What exists | Extraction |
|---|---|---|
| `README.md:11-13` | Defines the core idea | Encode tacit expert workflow into AI-executable instructions. |
| `README.md:15-24` | Repository structure | `skills/`, `rules/`, and project guidance are separated. |
| `README.md:57-60` | Skill table | Each skill has input/output and a bounded task. |
| `CLAUDE.md` | Project conventions | Repo is a prompt/knowledge repository, not a runnable app. |
| `rules/js-reverse.md` | Six-phase manual | Request analysis, entry location, code analysis, deobfuscation, algorithm restoration, validation. |
| `skills/find-crypto-entry/SKILL.md:17-23` | Strategy selection | Choose static search or dynamic breakpoint based on signal. |
| `skills/find-crypto-entry/SKILL.md:49-72` | Anti-patterns and completion standard | Stop at entry location; do not overrun into algorithm restoration. |
| `skills/env-patch/SKILL.md:16-34` | Engine/strategy separation and rules | Stable engine, mutable strategy file, load order, format validation. |
| `skills/env-patch/SKILL.md:116-184` | Diagnostic loop | Read report, route errors/undefined/hang, reference files on demand. |
| `skills/ast-deobfuscate/SKILL.md:56-67` | Flexible plan and MCP role | Enter planning, skip irrelevant steps, use MCP for probes not bulk work. |
| `skills/ast-deobfuscate/SKILL.md:527-563` | Safety and reversibility | Sandbox, intermediate files, preserve uncertain code. |
| `skills/skill-creator/SKILL.md:47-111` | Skill design principles | Capture intent, progressive disclosure, avoid surprise. |
| `skills/skill-creator/SKILL.md:141-232` | Evaluation loop | Test prompts, baseline, assertions, grading, aggregation. |

## Boundary

```text
source record = provenance only
candidate distillation = design extraction
general workflow pattern = reusable candidate method
project overlay = VAKS-side borrowing hint
promotion = later evidence-aware review only
```

Do not use this source to justify cracking, authorization bypass, private-code
extraction, or action-facing security work inside VAKS.
