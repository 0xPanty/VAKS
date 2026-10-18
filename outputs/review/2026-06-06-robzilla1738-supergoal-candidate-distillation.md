---
type: repo_candidate_distillation
status: candidate_only
created_at: 2026-06-06
source_record: raw/repos/2026-06-06-robzilla1738-supergoal-source.md
source_url: https://github.com/robzilla1738/supergoal
checked_commit: 86f1b0095ed1f6f9dc99f550a6053c931a4f96f4
commit_time: "2026-06-05 19:53:03 +0000"
truth_boundary: candidate distillation only; not reviewed knowledge; not VAKS main architecture; not action basis
review_priority: low
projects:
  - verified-action-knowledge-system
tags:
  - supergoal
  - agent-workflow
  - codex-skill
  - claude-code-plugin
  - autonomous-build
  - final-audit
  - not-main-architecture
---

# Supergoal Candidate Distillation

## 一句话人话结论

Supergoal 是一个让 Claude Code / Codex CLI “先深度规划，再一次性 dispatch 长任务”的技能/插件。它关心的是 coding agent 如何把一个大任务拆成阶段、写到 `.supergoal/` 文件、用一个 `/goal` 自动执行到底，并在失败时重试/修复/停机交接。

它跟 VAKS 主架构无关：不处理 source provenance、candidate point、evidence support、review queue、reviewed relation、context pack、action basis 或 Obsidian truth layer。

## 它到底是什么

它的运行形状大概是：

```text
/supergoal <task>
-> load memory + detect tools
-> classify greenfield / brownfield
-> recon codebase / environment
-> list risks and dependencies
-> split into adaptive phases
-> write ROADMAP / STATE / THINKING / PROTOCOL / phase specs
-> show plan review and wait for explicit confirmation
-> run pre-flight
-> print one ready-to-paste /goal
-> /goal session executes phases with verify blocks
-> final audit before SUPERGOAL_RUN_COMPLETE
```

所以它不是“知识系统”，而是“执行系统的外壳”。

## 可借鉴但不进主架构的点

1. `one-goal-dispatch-with-file-backed-specs`

候选理解：长任务不要把全部计划塞进一条 prompt，而是把 roadmap、state、protocol、phase specs 写在本地文件里，再用短 `/goal` 作为完成条件。

边界：这只是 coding agent 的执行编排技巧，不是 VAKS 的知识对象或 review 机制。

2. `hard-user-gate-before-unsupervised-run`

候选理解：开始无人值守执行前，必须先给用户计划审查和明确确认机会。

边界：VAKS 已经有“不要自动开始执行/自动化”的操作规则，不需要为此改主线。

3. `complete-working-tree-audit`

候选理解：审计 coding agent 交付物时，不能只看 commit range；未提交、暂存、未跟踪文件都要纳入检查。

边界：这对代码交付检查有用，但不是 VAKS 证据支持或 truth confidence。

4. `three-strike-recovery`

候选理解：长任务失败时可以先 probe/retry，再写 fix spec，再 handoff。

边界：适合执行失败，不适合知识审查。VAKS 的冲突、证据不足、scope mismatch 不能用“重试三次”解决。

5. `memory-writeback-as-phase-boundary`

候选理解：每个阶段结束时写入非显而易见学习，下一次 run 复用。

边界：VAKS 必须保留 agent memory quarantine；自动 memory writeback 只能是候选/反馈/操作记忆，不能改 reviewed truth。

## 不吸收的部分

- 不把 `.supergoal/` 当成 VAKS 的任务/知识目录。
- 不把 `/goal` 协议纳入 VAKS 主线。
- 不引入新的主架构模块。
- 不创建 project borrowing ledger disposition。
- 不把它作为 evidence-aware review、source intake、context pack 或 action basis 的证据。
- 不安装这个技能到本机 Codex/Claude 环境。
- 不运行它的脚本。

## 和 VAKS 的关系

最准确的分类：

```text
auxiliary-tooling-reference
agent-execution-protocol-reference
coding-task-completion-discipline
low-priority candidate note
```

它可能在以后这些问题上有参考价值：

```text
怎么让 coding agent 长任务更少半途而废
怎么把阶段计划写成文件而不是塞进聊天
怎么检查未提交文件也算交付物
怎么在执行失败时停得有证据
```

但对当前 VAKS 主架构：

```text
no source-intake change
no schema change
no review queue change
no evidence packet change
no activation tier change
no retrieval layer change
no Obsidian vault model change
```

## Source / Code Anchors

| Anchor | What exists | Candidate extraction | Boundary |
|---|---|---|---|
| `README.md:3-7` | Project describes itself as deep planning plus autonomous build, working on Claude Code and Codex CLI. | Classify as agent workflow / skill. | Self-description only. |
| `README.md:142-151` | Lists staged workflow from context detection through final audit. | Workflow map. | Not VAKS architecture. |
| `README.md:169-186` | Lists `.supergoal/` artifacts. | File-backed task execution substrate. | Not Obsidian knowledge substrate. |
| `skills/supergoal/SKILL.md:261-335` | Explicit plan review gate before dispatch. | Good caution pattern. | Already covered by VAKS operating rules. |
| `skills/supergoal/SKILL.md:385-429` | Phase loop and final audit before completion. | Strong completion discipline. | Does not replace review/warrant. |
| `skills/supergoal/scripts/repo-state.sh:2-36` | Complete working-tree comparison helper, no mutation. | Useful coding audit helper. | Tooling only. |
| `CHANGELOG.md:7-31` | v0.6.1 focuses on uncommitted-work audit correctness. | Confirms current release emphasis. | Changelog self-report; tests not run. |

## 适配判断

- Direct use: no
- Fork: no
- Design-only: only if later studying coding-agent execution loops
- Main architecture value: none
- Tooling side value: low to medium
- Risk: if over-absorbed, it would smuggle execution-control mechanics into knowledge-governance architecture
- Next action: keep as synced source + low-priority candidate note; no further VAKS work

## 结论

```text
watch_tooling_only / reject_for_main_architecture
```

这条资料已经完成轻入口和候选蒸馏。它可以留档，但不用进入主架构讨论。
