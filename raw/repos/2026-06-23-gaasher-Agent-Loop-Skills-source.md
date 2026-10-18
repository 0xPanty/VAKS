---
type: source
record_kind: source_card
status: source-captured
title: "gaasher/Agent-Loop-Skills"
source_id: github-gaasher-Agent-Loop-Skills
source_uri: https://github.com/gaasher/Agent-Loop-Skills
source_url: https://github.com/gaasher/Agent-Loop-Skills
source_type: repository
author: gaasher
publisher: GitHub
published_at: 2026-06-15T02:01:33Z
updated_at: 2026-06-22T18:40:18Z
captured_at: 2026-06-23T02:45:52+08:00
captured_by: Codex
version_or_commit: 25dd18fc93523c212addd46fad540c779b18515a
source_integrity:
  source_hash: 25dd18fc93523c212addd46fad540c779b18515a
  snapshot_hash: 06C8E6B6A8951922EA97A505F3178E3F3A79F7EE49F373B17A3E5EADA9014029
  ingest_state: new
adapter_ingest:
  adapter_name: git-clone-and-archive
  adapter_version: git archive
  capture_method: "git clone --depth 1, GitHub API metadata, then git archive HEAD"
  extraction_trace: "local inspection of README, docs, loop SKILL.md files, roles/schemas/tools/examples/showcase layout"
  known_limits:
    - "No loop was executed during this intake."
    - "No external Agent Skills host compatibility test was performed."
    - "GitHub stars, forks, and issue counts are volatile metadata captured at intake time only."
    - "README claims and linked external narratives were not independently validated beyond repository/source inspection."
source_status: active
raw_location: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
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
why_saved: "User asked to distill gaasher/Agent-Loop-Skills because loop-style agent workflows are currently popular and VAKS lacks this knowledge point."
topics:
  - agentic-loops
  - agent-skills
  - verification-gated-iteration
  - run-ledger
  - subagents
  - autoresearch
  - evaluator-optimizer
projects:
  - verified-action-knowledge-system
source_family:
  - repository
  - agent-skill
  - agentic-loop-library
upstream_sources: []
verification_status: source_snapshot_captured
candidate_relation_suggestions: []
tags:
  - repo-intake
  - agent-skills
  - agentic-loops
  - candidate-only
---

# 来源记录：gaasher/Agent-Loop-Skills

## 为什么收录

用户要求蒸馏 `gaasher/Agent-Loop-Skills`，原因是最近 loop / agentic loop 很火，而资料库还缺这类知识点。

本记录只保存来源身份、源码快照和初步看点。它不代表该仓库已经被 VAKS 采纳，也不代表其中的 benchmark、README demo、GitHub 热度或 skill 设计可以作为 evidence support、reviewed knowledge 或 action basis。

## 来源信息

- 作者：gaasher
- 发布方：GitHub
- 原始链接：https://github.com/gaasher/Agent-Loop-Skills
- 版本 / commit：`25dd18fc93523c212addd46fad540c779b18515a`
- commit 时间：`2026-06-22T06:46:38-04:00`
- commit subject：`Beautify (#32)`
- GitHub created_at：`2026-06-15T02:01:33Z`
- GitHub pushed_at：`2026-06-22T10:46:40Z`
- license：MIT
- source_status：active
- 采集方式：`git clone --depth 1` + `git archive HEAD`
- 本地快照：`raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip`
- 快照 SHA256：`06C8E6B6A8951922EA97A505F3178E3F3A79F7EE49F373B17A3E5EADA9014029`
- GitHub metadata snapshot：stars `10`, forks `1`, open issues `1`, default branch `main` at intake time only.

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
| Project framing | `README.md:5-9`, `README.md:32-49`, `README.md:51-55`, `README.md:72-77` | Confirms the central idea: package reusable loops as skills; bind task/artifact/signal/budget at invocation time; verify each iteration. |
| Demo / showcase claims | `README.md:20-26`, `README.md:109-143`, `showcase/tournament-autoresearch/results.tsv` | Confirms the repo includes archived run outputs, but these remain source claims/showcase records unless independently reproduced. |
| Loop inventory | `README.md:147-201`, `loops/*/SKILL.md` | Confirms 20 loop folders, each centered on a domain-specific iteration pattern. |
| Packaging | `.claude-plugin/plugin.json:1-12`, `.claude-plugin/marketplace.json`, `pyproject.toml` | Confirms plugin name, skills root, MIT license, Python tooling, and install shape. |
| Authoring rules | `docs/authoring.md:7-22`, `docs/skill-authoring-rules.md:28-37`, `docs/skill-authoring-rules.md:39-53` | Confirms loop folders are self-contained and every loop needs program, artifact slot, feedback signal, ledger, termination/budget. |
| Runtime boundaries | `docs/skill-authoring-rules.md:150-194`, `docs/skill-authoring-rules.md:203-211` | Confirms stdlib-only helpers, user environment execution, consented deps, and sandbox eval expectations. |
| Subagent portability | `docs/compatibility.md:1-24`, `docs/compatibility.md:26-43`, `docs/compatibility.md:45-56` | Confirms skills install broadly, but runtime role-file subagent dispatch is Claude-Code-specific; other hosts degrade inline. |
| Minimal autoresearch loop | `loops/karpathy/SKILL.md:17-22`, `loops/karpathy/SKILL.md:89-99`, `loops/karpathy/SKILL.md:120-132`, `loops/karpathy/SKILL.md:142-148` | Confirms keep/revert based on one scalar metric and append-only results ledger. |
| Tournament loop | `loops/tournament-autoresearch/SKILL.md:19-25`, `loops/tournament-autoresearch/SKILL.md:92-102`, `loops/tournament-autoresearch/SKILL.md:125-131`, `loops/tournament-autoresearch/SKILL.md:153-169` | Confirms competing proposers, Judge selection, realized-delta calibration, and rubric refinement. |
| Optimization loop | `loops/optimize-loop/SKILL.md:16-31`, `loops/optimize-loop/SKILL.md:65-81`, `loops/optimize-loop/SKILL.md:98-125`, `loops/optimize-loop/SKILL.md:127-140` | Confirms hard correctness gate plus metric minimization and best-iteration reporting. |
| Literature survey loop | `loops/literature-survey/SKILL.md:20-28`, `loops/literature-survey/SKILL.md:83-94`, `loops/literature-survey/SKILL.md:129-145` | Confirms evidence/contradiction matrix, verbatim snippets, measured saturation, and coverage note. |
| Data analysis loop | `loops/data-analysis/SKILL.md:19-23`, `loops/data-analysis/SKILL.md:57-63`, `loops/data-analysis/SKILL.md:78-87`, `loops/data-analysis/SKILL.md:107-117` | Confirms no finding without computed number and independent re-derivation gate. |
| Red team loop | `loops/red-team/SKILL.md:17-21`, `loops/red-team/tools/harness.py:4-10`, `loops/red-team/SKILL.md:129-135` | Confirms adversarial loop-until-dry and explicit separation between find and fix/re-verify phases. |

## 初步看点

- The repo's strongest idea is not a single algorithm. It is a reusable loop contract:

```text
program / skill
-> artifact slot
-> real feedback signal
-> append-only run ledger
-> explicit stop or human interrupt
```

- It turns skills from "task instructions" into "iteration programs" that bind to the user's artifact and environment at runtime.
- It repeatedly insists on external signals: tests, metrics, result hashes, computed numbers, source snippets, calibrated judges, or dry-round counts.
- It has a useful portability honesty: skill loading is broad, but runtime subagent isolation is not universal.
- It is especially relevant for future VAKS/MISA operator loops, source-intake loops, research survey loops, red-team/find-fix loops, and evaluator-optimizer patterns.

## 明显疑点

- README demo numbers and showcase ledgers were not reproduced locally.
- "Loop until interrupted" is dangerous for VAKS ordinary intake; VAKS needs bounded, auditable, user-confirmed workflows by default.
- A feedback signal is not evidence support. Tests, metrics, judges, and dry-round counts are diagnostics unless routed through review/evidence gates.
- GitHub popularity and current "loop" hype are discovery signals only, not proof of quality.
- Off Claude Code, multi-role loops run inline rather than with real isolated parallel subagents; this matters for Codex use.

## 可抽取 Candidate Points

1. Treat a loop as a first-class skill artifact with five mandatory ingredients: program, artifact, signal, ledger, stop.
2. Every agent loop should have a real feedback signal and a keep/revert or keep/refute rule.
3. Run ledgers are crucial: they make iteration inspectable and prevent "agent worked a lot" from becoming a false success signal.
4. Spawn-or-degrade is a good portability pattern: use real subagents where supported, but preserve a correct inline fallback.
5. "No claim without a number / snippet / gate" is a useful discipline for data, literature, optimization, and red-team loops.
6. VAKS should borrow loop structure as candidate operational scaffolding, not as truth/review/action authority.

## Source Annotation Sidecars

```yaml
source_annotation_refs:
  - annotation_id: als-loop-five-ingredients
    path: outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-loop-five-ingredients.md
    anchor_status: exact_verified
  - annotation_id: als-verification-gated-keep-revert
    path: outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-verification-gated-keep-revert.md
    anchor_status: exact_verified
  - annotation_id: als-spawn-or-degrade-boundary
    path: outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-spawn-or-degrade-boundary.md
    anchor_status: exact_verified
  - annotation_id: als-literature-evidence-matrix
    path: outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-literature-evidence-matrix.md
    anchor_status: exact_verified
  - annotation_id: als-tournament-judge-calibration
    path: outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-tournament-judge-calibration.md
    anchor_status: exact_verified
```

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- VAKS starts designing reusable operator/source-intake loops.
- MISA needs agent execution loops with ledgers and gates.
- A future workflow tries to use loop output as action basis.
- We need to compare this repo against other loop/skill frameworks with reproduced sandbox runs.

## 本地验证

Executed:

```text
git clone --depth 1 https://github.com/gaasher/Agent-Loop-Skills.git
git rev-parse HEAD
git log -1 --format='%H%n%aI%n%cI%n%s'
git archive --format=zip --output raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip HEAD
Get-FileHash -Algorithm SHA256 raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
```

Not executed:

- Any installed Agent Skill.
- Any showcase loop run.
- Any external host compatibility test.
- Any benchmark or model-training run.

## 下一步

- Use candidate distillation for VAKS/MISA operator-loop design.
- Use project overlay only for project-level borrow/non-borrow boundaries.
- Do not promote loop outcomes, README claims, or GitHub metadata without later evidence-aware review.
