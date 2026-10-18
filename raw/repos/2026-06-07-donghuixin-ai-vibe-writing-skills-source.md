---
type: source
status: source-captured
title: AI Vibe Writing Skills
source_id: github-donghuixin-ai-vibe-writing-skills
source_uri: github:donghuixin/AI-Vibe-Writing-Skills@dbfee78dac29c0c347354ffe696cf124b80c1817
source_url: https://github.com/donghuixin/AI-Vibe-Writing-Skills
source_type: repository
owner: donghuixin
repo: AI-Vibe-Writing-Skills
checked_commit: dbfee78dac29c0c347354ffe696cf124b80c1817
commit_time: 2026-06-02T20:49:52+08:00
commit_subject: "docs: add defensive writing module"
captured_at: 2026-06-07 05:03:45 +08:00
captured_by: Codex
version_or_commit: dbfee78dac29c0c347354ffe696cf124b80c1817
source_status: active
raw_location: raw/repos/2026-06-07-donghuixin-ai-vibe-writing-skills-source.md
snapshot_ref: raw/repos/_snapshots/donghuixin-AI-Vibe-Writing-Skills-dbfee78dac29c0c347354ffe696cf124b80c1817.zip
snapshot_sha256: 2FDD9E6D966080512999DDC8DC5D6559FEF39BAC2030738AF090D74F0F58B6A6
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
  - spec-driven-writing
  - agent-workflow
  - defensive-review
  - memory-boundary
  - evidence-ingestion
projects:
  - verified-action-knowledge-system
source_family: AI-writing-local-context-system
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions:
  - target: "[[2026-06-07-donghuixin-ai-vibe-writing-skills-candidate-distillation]]"
    relation_type: derived_from
    relation_state: candidate
    why_suggested: "The repository provides a file-based agent writing workflow that can be compared with VAKS source intake, review, memory, and action-boundary mechanisms."
tags:
  - raw-repo
  - github
  - candidate-only
---

# 来源记录：AI Vibe Writing Skills

## 为什么收录

用户明确要求对 `donghuixin/AI-Vibe-Writing-Skills` 做强蒸馏，并指出它的逻辑似乎与 VAKS 相似。

本次只使用仓库作为证据来源。原先提供的 Bilibili 视频未作为蒸馏证据，因为用户确认视频声音听不清，要求直接蒸馏仓库逻辑。

## 来源信息

- 作者 / owner: `donghuixin`
- 仓库：`AI-Vibe-Writing-Skills`
- 原始链接：<https://github.com/donghuixin/AI-Vibe-Writing-Skills>
- 检查 commit：`dbfee78dac29c0c347354ffe696cf124b80c1817`
- commit time：`2026-06-02T20:49:52+08:00`
- commit subject：`docs: add defensive writing module`
- source_status: active
- snapshot: `raw/repos/_snapshots/donghuixin-AI-Vibe-Writing-Skills-dbfee78dac29c0c347354ffe696cf124b80c1817.zip`
- snapshot SHA256: `2FDD9E6D966080512999DDC8DC5D6559FEF39BAC2030738AF090D74F0F58B6A6`
- license: MIT

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
| `README.md:25` | Project positioning as local AI writing context system | Establishes top-level intent | Public README claim only |
| `README.md:104` | Workflow contract: spec, outline, recall, draft, defend, review, iterate | Shows the whole process loop | Not proof of runtime correctness |
| `README.md:165` | Agent system table | Identifies module boundaries | Documentation, not execution proof |
| `README.md:184` | Defensive writing section | Main review/red-team idea | Candidate design reference |
| `README.md:320` | PDF and evidence ingestion | Source/reference intake lane | Candidate analogy to VAKS intake |
| `README.md:360` | Local AI style check | Lint/diagnostic surface | Not truth or reviewer authority |
| `SKILLS.md:5` | System-level writing process | Internal operating summary | Candidate workflow evidence |
| `SKILLS.md:79` | Spec audit must be rigid and can return `failed_specs` | Strongest review-loop signal | Candidate design reference |
| `SKILLS.md:80` | Defensive writing strategy ladder | Shows upper/middle/lower escalation | Candidate review-gate analogy |
| `.traerules:5` | System-level workflow instructions | Workspace-level execution contract | Agent instruction, not verified behavior |
| `.traerules:58` | Multi-agent writing loop | Orchestration sequence | Candidate workflow evidence |
| `.ai_context/prompts/6_outline_manager_agent.md:6` | Outline must include DoD | Output contract mechanism | Candidate adaptation target |
| `.ai_context/prompts/7_content_writer_agent.md:14` | Writer must strictly implement DoD | Draft constrained by spec | Candidate adaptation target |
| `.ai_context/prompts/8_content_review_agent.md:138` | Spec Audit checks `document_spec.md` and DoD | Review-as-gate pattern | Candidate adaptation target |
| `.ai_context/prompts/8_content_review_agent.md:144` | Failures force rewrite rather than mild suggestions | Closed-loop correction pressure | Candidate adaptation target |
| `.ai_context/prompts/9_workflow_coordinator.md:4` | Coordinator sequence | Orchestration reference | Candidate workflow evidence |
| `.ai_context/prompts/10_pdf_reader_agent.md:1` | PDF reader extracts structured evidence | Ingest mechanism | Candidate analogy, not VAKS-grade provenance |
| `.ai_context/prompts/11_context_compactor_agent.md:8` | Compact context into skeleton/snapshot/specs | Context budget mechanism | Candidate dev-context analogy |
| `.ai_context/prompts/12_router_agent.md:28` | Prompt slices selected by task context | Dynamic loading mechanism | Candidate context-routing analogy |
| `.ai_context/prompts/13_latex_self_healing_agent.md:5` | Script/execute/verify self-healing loop | Tool loop reference | High safety caution |
| `.ai_context/prompts/14_defensive_writing_agent.md:4` | Defensive writing definition | Red-team review concept | Candidate review-gate analogy |
| `.ai_context/prompts/14_defensive_writing_agent.md:153` | Attack -> Validity Threat -> Boundary Reframing -> Evidence Anchor | Strongest reusable review frame | Candidate adaptation target |
| `.ai_context/reference_learning.md:17` | Reference library / hard memory / soft memory storage | Memory split | Candidate analogy, weaker than VAKS truth boundary |
| `Local_AI_Style_Check/paper_ai_detector.py:33` | LaTeX cleaning before detection | Diagnostic implementation detail | Lint only |
| `Local_AI_Style_Check/paper_ai_detector.py:76` | PPL scoring | AI-style diagnostic | Not evidence support |

## 初步看点

- The repository is organized as a file-backed agent operating contract: `.traerules`, `.agents/workflows`, `.ai_context/prompts`, `custom_specs`, templates, hard/soft memory, error log, and reference library.
- The most important architectural idea is not writing style imitation, but a workflow loop: spec -> outline with DoD -> memory/evidence recall -> draft -> defensive red-team -> review audit -> forced rewrite -> memory update.
- The repository treats reviewer risk as something to surface before final output, using attack surfaces, contribution boundary, evidence anchors, and claim narrowing.
- It has a lightweight memory split: hard memory for exact facts/terms, soft memory for preference/style, reference library for evidence.
- Its weakest fit for VAKS is authority control: the repository is designed for writing usefulness, not reviewed truth; PPL and AI detectors are diagnostics, not validation.

## 明显疑点

- The workflow is mostly prompt/file convention rather than a tested runtime system.
- Reference ingestion can write to hard/soft memory directly; VAKS should not copy that authority model.
- AI detector / PPL language can easily be overread as proof; VAKS should keep this in maintenance-lint only.
- LaTeX self-healing generates and runs scripts; VAKS should only borrow this under explicit tool-safety and approval boundaries.
- The repo does not yet show a strong provenance/evidence packet model equivalent to VAKS source anchors, review gates, and truth mutation controls.

## 可抽取 Candidate Points

- `spec_as_task_contract`: a user-approved spec can act as a local task contract before generation.
- `dod_as_output_gate`: section-level DoD can become a reviewable output contract.
- `hard_soft_memory_split`: exact facts and style preferences should not be stored or recalled as one undifferentiated memory.
- `defensive_red_team_gate`: action-facing or review-facing outputs benefit from an attack-surface pass before finalization.
- `review_failure_forces_rewrite`: if spec/evidence/defensive audit fails, the system should route back to generation or revision rather than merely attaching advice.
- `prompt_router_as_context_discipline`: prompt slices and compact context can reduce full-context overloading.
- `diagnostic_not_authority`: AI-style scoring and detector APIs are useful lint, not truth or review authority.

## 当前处理等级

```text
heavy
```

升级到 reviewed / action-facing use 的条件：

- Convert candidate points into VAKS Evidence Packets.
- Verify exact source spans and compare with existing VAKS reviewed boundaries.
- Run support/challenge review before any mainline schema, decision, or pattern change.

## 下一步

- See candidate distillation: `outputs/review/2026-06-07-donghuixin-ai-vibe-writing-skills-candidate-distillation.md`
- See architecture review: `wiki/summaries/2026-06-07-donghuixin-ai-vibe-writing-skills-architecture-review.md`
- See VAKS project overlay: `outputs/review/project_overlays/VAKS/VAKS-ai-vibe-writing-skills-2026-06-07.md`
