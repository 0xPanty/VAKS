---
type: source
record_kind: source_card
status: source-captured
title: "Agents365-ai/drawio-skill"
source_id: github-Agents365-ai-drawio-skill
source_uri: https://github.com/Agents365-ai/drawio-skill
source_url: https://github.com/Agents365-ai/drawio-skill
source_type: repository
author: Agents365-ai
publisher: GitHub
published_at:
updated_at: 2026-06-04T00:53:31+08:00
captured_at: 2026-06-14
captured_by: Codex
version_or_commit: 00ed825c4aec623a5838a16d1ad6b7a2c603dfa6
source_integrity:
  source_hash:
  snapshot_hash: 6BEBAC082480FC6D657B3B9792A94A9ABAEBE098AE93C0FBF51E48B3C1D72A76
  ingest_state: new
adapter_ingest:
  adapter_name: git-clone-and-archive
  adapter_version: git archive
  capture_method: "git clone --depth 1, then git archive HEAD"
  extraction_trace: "local inspection of README, SKILL.md, references, scripts, tests, changelog"
  known_limits:
    - "No draw.io desktop CLI export was executed during this intake."
    - "No Graphviz-backed real autolayout export was executed during this intake."
    - "Standard-library regression tests were executed and passed."
source_status: active
raw_location: raw/repos/_snapshots/2026-06-14-Agents365-ai-drawio-skill-00ed825-source.zip
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
why_saved: "User asked to distill drawio-skill as a potential tool/reference for VAKS/MISA architecture and workflow visualization."
topics:
  - diagram-generation
  - drawio
  - agent-skill
  - codebase-visualization
  - architecture-documentation
projects:
  - verified-action-knowledge-system
source_family:
  - repository
  - agent-skill
upstream_sources: []
verification_status: source_snapshot_captured
candidate_relation_suggestions: []
tags:
  - repo-intake
  - drawio
  - diagram-generation
  - architecture-documentation
---

# 来源记录：Agents365-ai/drawio-skill

## 为什么收录

用户要求蒸馏 `Agents365-ai/drawio-skill`。

本记录只保存来源身份、快照和初步看点。它不代表该 skill 已被采纳，也不代表生成出来的图可以作为证据、review 结论或 action basis。

## 来源信息

- 作者：Agents365-ai
- 发布方：GitHub
- 原始链接：https://github.com/Agents365-ai/drawio-skill
- 版本 / commit：`00ed825c4aec623a5838a16d1ad6b7a2c603dfa6`
- commit 时间：`2026-06-04T00:53:31+08:00`
- commit subject：`docs: add "when to use / when not to use" routing guidance (#33)`
- license：MIT
- source_status：active
- 采集方式：`git clone --depth 1` + `git archive HEAD`
- 本地快照：`raw/repos/_snapshots/2026-06-14-Agents365-ai-drawio-skill-00ed825-source.zip`
- 快照 SHA256：`6BEBAC082480FC6D657B3B9792A94A9ABAEBE098AE93C0FBF51E48B3C1D72A76`

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
| Project framing | `README.md:17`, `README.md:26`, `README.md:28`, `README.md:29`, `README.md:30` | Confirms skill scope: natural language to draw.io XML, codebase visualization, shape search, self-check, feedback loop. |
| Skill metadata | `skills/drawio-skill/SKILL.md:3`, `skills/drawio-skill/SKILL.md:4`, `skills/drawio-skill/SKILL.md:7`, `skills/drawio-skill/SKILL.md:22` | Confirms version, supported use cases, dependencies, and when not to use. |
| Resource routing | `skills/drawio-skill/SKILL.md:31`, `skills/drawio-skill/SKILL.md:39`, `skills/drawio-skill/SKILL.md:45`, `skills/drawio-skill/SKILL.md:48` | Confirms modular references/scripts and on-demand loading pattern. |
| Workflow | `skills/drawio-skill/SKILL.md:76`, `skills/drawio-skill/SKILL.md:96`, `skills/drawio-skill/SKILL.md:98`, `skills/drawio-skill/SKILL.md:100` | Confirms dependency check, generation, validation/export, self-check loop. |
| Self-check / review | `skills/drawio-skill/SKILL.md:113`, `skills/drawio-skill/SKILL.md:128`, `skills/drawio-skill/SKILL.md:133` | Confirms visual review and iteration safety valve. |
| Auto-layout docs | `skills/drawio-skill/references/autolayout.md:1`, `skills/drawio-skill/references/autolayout.md:5`, `skills/drawio-skill/references/autolayout.md:81` | Confirms Graphviz-backed layout and importers. |
| Shape search docs | `skills/drawio-skill/references/shapes.md:1`, `skills/drawio-skill/references/shapes.md:48` | Confirms official shape search and AI/LLM brand logo support. |
| Auto-layout code | `skills/drawio-skill/scripts/autolayout.py:51`, `skills/drawio-skill/scripts/autolayout.py:108`, `skills/drawio-skill/scripts/autolayout.py:141`, `skills/drawio-skill/scripts/autolayout.py:179`, `skills/drawio-skill/scripts/autolayout.py:314` | Confirms palette loading, dot generation, Graphviz layout, draw.io XML emission. |
| Structural validation | `skills/drawio-skill/scripts/validate.py:24`, `skills/drawio-skill/scripts/validate.py:48`, `skills/drawio-skill/scripts/validate.py:99` | Confirms deterministic lint checks. |
| Shape index | `skills/drawio-skill/scripts/shapesearch.py:27`, `skills/drawio-skill/scripts/shapesearch.py:50`, `skills/drawio-skill/scripts/shapesearch.py:87` | Confirms local official shape index search. |
| AI icons | `skills/drawio-skill/scripts/aiicons.py:33`, `skills/drawio-skill/scripts/aiicons.py:64`, `skills/drawio-skill/scripts/aiicons.py:77`, `skills/drawio-skill/scripts/aiicons.py:116` | Confirms brand logo lookup and variant selection. |
| Code importers | `skills/drawio-skill/scripts/pyimports.py:27`, `skills/drawio-skill/scripts/jsimports.py:48`, `skills/drawio-skill/scripts/goimports.py:42`, `skills/drawio-skill/scripts/rustimports.py:47`, `skills/drawio-skill/scripts/pyclasses.py:59` | Confirms multi-language codebase graph extraction. |
| Tests | `tests/test_scripts.py:1`, `tests/test_scripts.py:44`, `tests/test_scripts.py:76`, `tests/test_scripts.py:127`, `tests/test_scripts.py:197` | Confirms dependency-free test coverage for scripts. |

## 初步看点

- It is a mature diagram-production skill rather than a knowledge architecture.
- The most useful mechanics are: diagram-type presets, codebase import graph extraction, Graphviz autolayout, deterministic `.drawio` validation, shape/icon search, browser fallback, and review loop.
- It may help VAKS explain architecture, review workflow, context-pack flow, and product workbench state more clearly.
- It may help MISA/agent work by visualizing code/module graphs during architecture debugging.

## 明显疑点

- Generated diagrams are explanation artifacts, not evidence support.
- The self-check / visual validation is diagnostic only; it cannot create review approval.
- draw.io desktop CLI and optional Graphviz are operational dependencies, not knowledge-system components.
- AI/LLM brand icons may be CDN-referenced unless embedded, which matters for offline/archival diagrams.

## 可抽取 Candidate Points

1. Diagram generation should live in an output/workbench layer, not truth/review layer.
2. Deterministic `.drawio` lint before visual review is a useful pattern for generated artifacts.
3. Codebase-to-diagram extraction can help MISA/VAKS architecture debugging, but diagrams remain derived views.
4. Shape search reduces hallucinated vendor icon/style strings; this is an output-quality pattern.
5. Style presets and user approval before saving style can inspire product/workbench personalization boundaries.

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- VAKS starts a diagram/export/publishing product surface.
- MISA uses generated diagrams in action-facing architecture decisions.
- A future workflow tries to treat generated diagrams as evidence or reviewed knowledge.

## 本地验证

Executed:

```text
python -m unittest discover -s tests -v
```

Result:

```text
Ran 21 tests in 1.597s
OK
```

Not executed:

- draw.io desktop CLI export.
- Graphviz real layout run.
- vision self-check.

## 下一步

- Use candidate distillation for product/documentation planning.
- Use project overlay only when building VAKS visual documentation or MISA code-structure visualization.
- Do not use diagrams as action basis without independent source/review anchors.
