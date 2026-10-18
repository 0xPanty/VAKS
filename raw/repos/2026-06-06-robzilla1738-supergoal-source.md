---
type: source
status: source-captured
title: "Supergoal"
source_id: 2026-06-06-robzilla1738-supergoal-source
source_uri: https://github.com/robzilla1738/supergoal
source_url: https://github.com/robzilla1738/supergoal
source_type: repository
author: robzilla1738 / repository contributors
publisher: GitHub
published_at:
updated_at: 2026-06-05
captured_at: 2026-06-06
captured_by: Codex
version_or_commit: 86f1b0095ed1f6f9dc99f550a6053c931a4f96f4
commit_time: "2026-06-05 19:53:03 +0000"
commit_subject: "fix: make repo-state.sh executable so its test suite passes on a clean checkout"
source_status: active
license: MIT
stars_at_capture: 90
forks_at_capture: 7
open_issues_at_capture: 0
snapshot_location: raw/repos/_snapshots/robzilla1738-supergoal-86f1b0095ed1f6f9dc99f550a6053c931a4f96f4.zip
snapshot_sha256: A310F3819DF81BBAA9A503966B19B255FF753F7B0BC946A760F38321D89B9544
processing_mode: immediate
processing_level: medium
review_priority: low
review_owner: Codex
formalization_status: candidate-generated
verification_status: primary-source-captured
confidence: high for captured repository contents at checked commit; medium for future upstream state after capture
projects:
  - verified-action-knowledge-system
source_family:
  - agent-workflow-orchestration
  - codex-claude-skill
  - autonomous-execution-protocol
  - planning-tool
topics:
  - supergoal
  - codex-skill
  - claude-code-plugin
  - goal-command
  - phase-spec
  - final-audit
  - memory-writeback
  - repo-state
truth_boundary: source provenance and candidate comprehension only; not VAKS main architecture; not reviewed knowledge; not action basis
candidate_relation_suggestions: []
tags:
  - supergoal
  - agent-workflow
  - autonomous-build
  - planning-protocol
  - candidate-only
  - not-main-architecture
---

# Supergoal Source Record

## 为什么收录

用户给出仓库链接，要求判断它是什么，并明确说明“跟我们主架构无关”。本记录只保留来源、版本、文件锚点和候选理解，后续如研究 Codex / Claude Code 的长任务执行协议时可回看。

说人话：

```text
Supergoal 不是知识库架构，也不是检索 / 证据 / review 系统。
它是一个给 Claude Code / Codex CLI 用的长任务规划和执行编排技能。
```

它的核心做法是：先让 `/supergoal` 做深度规划、内存读取、工具探测、阶段拆分、风险检查和计划确认；然后打印一条 ready-to-paste 的 `/goal` 命令，让用户粘贴一次，后续执行循环按 `.supergoal/` 里的阶段文件跑完，并做失败恢复和最终审计。

## 来源信息

- Repository: `robzilla1738/supergoal`
- URL: https://github.com/robzilla1738/supergoal
- Checked commit: `86f1b0095ed1f6f9dc99f550a6053c931a4f96f4`
- Commit time: `2026-06-05 19:53:03 +0000`
- Commit subject: `fix: make repo-state.sh executable so its test suite passes on a clean checkout`
- GitHub description at capture: plan and autonomously build a software task end-to-end; one ready-to-paste `/goal`; adaptive phase count; memory preload/writeback; 3-strike recovery; works on Claude Code and Codex.
- GitHub metadata at capture: 90 stars, 7 forks, 0 open issues, public repository, language Shell.
- License: MIT
- README version marker: `v0.6.1`
- Snapshot: `raw/repos/_snapshots/robzilla1738-supergoal-86f1b0095ed1f6f9dc99f550a6053c931a4f96f4.zip`
- Snapshot SHA256: `A310F3819DF81BBAA9A503966B19B255FF753F7B0BC946A760F38321D89B9544`
- Inspected mode: source/docs/scripts read; no plugin installed; no script executed.

## 文件 / 代码锚点

| Anchor | What exists | Extraction | Boundary |
|---|---|---|---|
| `README.md:3-7` | README frames Supergoal as deep planning followed by autonomous build, and says it works on Claude Code and Codex CLI. | This is an agent-workflow skill, not a knowledge-system source. | README claim is product self-description, not independent validation. |
| `README.md:142-151` | Stages include memory/tool detection, greenfield/brownfield intake, recon, risks, adaptive phase count, `.supergoal/` specs, pre-flight, `/goal` handoff, and final audit. | Useful as a compact map of the workflow. | It is a host interaction protocol, not VAKS review architecture. |
| `README.md:153-162` | Failure recovery uses first retry, second fix spec, third handoff. | Interesting operational loop for long-running coding tasks. | Do not import as VAKS truth/review state machine. |
| `README.md:163-167` | Each phase may write non-obvious learnings to memory. | Related to agent memory writeback ergonomics. | VAKS memory quarantine still applies; agent memory cannot mutate reviewed truth. |
| `README.md:169-186` | A run produces `.supergoal/ROADMAP.md`, `STATE.md`, `THINKING.md`, `PROTOCOL.md`, context files, applied memories, tools, and phase specs. | Concrete artifact layout for autonomous build orchestration. | These are task-control artifacts, not source intake or evidence packets. |
| `README.md:220-226` | Version marker is `v0.6.1`; license is MIT. | Captured source metadata. | Version and license may drift after capture. |
| `skills/supergoal/SKILL.md:29-42` | Skill summary explains staged context loading, recon, phase spec creation, plan review, and single `/goal` dispatch. | Main implementation contract lives in the skill file. | The contract is written for agent execution, not VAKS governance. |
| `skills/supergoal/SKILL.md:261-335` | Plan review is a hard gate; user must explicitly choose start before `/goal` dispatch. | Good human-gate pattern for unsupervised agent runs. | Already consistent with VAKS process caution; no mainline change needed. |
| `skills/supergoal/SKILL.md:339-377` | Pre-flight runs before printing `/goal`; if red, it loops back to plan review or asks for bypass. | Useful coding-task safety detail. | Applies to software build baselines, not source truth. |
| `skills/supergoal/SKILL.md:385-429` | Execution loop requires verify blocks, cleanliness checks, final audit, audit fixes, and only then `SUPERGOAL_RUN_COMPLETE`. | Strong completion discipline for build agents. | Cannot serve as evidence review or action readiness for VAKS knowledge. |
| `skills/supergoal/scripts/repo-state.sh:2-36` | Helper compares complete working tree against a baseline, including untracked work, and says it never mutates repo/index. | Narrow but practical audit helper. | Tooling detail only; not architecture-level import. |
| `skills/supergoal/references/repo-state-comparison.md:22-63` | Documents complete working-tree vs baseline strategy and helper commands. | Good explanation of why commit-range diff misses uncommitted work. | Relevant to coding-agent audits, not VAKS truth support. |
| `CHANGELOG.md:7-31` | v0.6.1 fixes audit/cleanliness comparison to include complete working tree and adds `repo-state.sh`, reference doc, and tests. | Confirms latest change focus. | Changelog is project self-report; tests not executed here. |

## 人话总结

Supergoal 是一个“长任务自动执行协议包”：

```text
用户说一个大任务
-> /supergoal 先做规划、侦察、拆阶段、写 .supergoal 文件
-> 用户确认一次
-> 它打印一条 /goal
-> 用户粘贴一次
-> agent 按阶段跑，失败就重试 / 写修复 spec / 到三次就停
-> 最后重新审计 ROADMAP、命令、交付物和工作区差异
```

它最像：

```text
Claude Code / Codex 的任务编排技能
长任务 planner + executor handoff template
agent completion audit protocol
```

它不像：

```text
知识库架构
Obsidian vault 模型
source intake 系统
证据支持检查
review queue
retrieval / context pack / action basis
```

## 当前处理结果

- Source card written: `raw/repos/2026-06-06-robzilla1738-supergoal-source.md`
- Source snapshot retained: `raw/repos/_snapshots/robzilla1738-supergoal-86f1b0095ed1f6f9dc99f550a6053c931a4f96f4.zip`
- Candidate distillation: `outputs/review/2026-06-06-robzilla1738-supergoal-candidate-distillation.md`
- Main architecture status: no mainline relevance found; no project overlay or borrowing ledger created.
