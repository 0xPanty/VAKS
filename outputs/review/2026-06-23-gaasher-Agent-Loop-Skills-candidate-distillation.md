---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/repos/2026-06-23-gaasher-Agent-Loop-Skills-source.md
derived_from:
  - raw/repos/2026-06-23-gaasher-Agent-Loop-Skills-source.md
  - raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
  - wiki/summaries/2026-06-23-gaasher-Agent-Loop-Skills-architecture-review.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - agentic-loop-design
  - source-intake-loop
  - operator-workflow
  - misa-agent-execution
  - evaluator-optimizer
possible_project_refs:
  - verified-action-knowledge-system
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-loop-five-ingredients.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-verification-gated-keep-revert.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-spawn-or-degrade-boundary.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-literature-evidence-matrix.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-tournament-judge-calibration.md
point_anchor_refs:
  - "README.md:46-54"
  - "README.md:72-77"
  - "docs/skill-authoring-rules.md:28-37"
  - "docs/skill-authoring-rules.md:174-179"
  - "docs/compatibility.md:26-43"
  - "loops/optimize-loop/SKILL.md:16-21"
  - "loops/literature-survey/SKILL.md:20-28"
  - "loops/tournament-autoresearch/SKILL.md:19-25"
borrow_value: strong
borrow_order: P1
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "An approved task is specifically designing a bounded agent loop, source-intake loop, MISA operator loop, or evaluator-optimizer workflow."
  support_when: "Agent workflow design, loop runner design, research/source-intake automation, MISA execution scaffolding, or task verification ledgers."
  risk_when: "A loop output, benchmark, judge score, retrieval result, or GitHub popularity signal is being treated as evidence support, reviewed knowledge, or action basis."
  cold_references:
    - raw/repos/2026-06-23-gaasher-Agent-Loop-Skills-source.md
    - raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
avoid:
  - "Do not borrow infinite/autonomous looping as VAKS ordinary intake behavior."
  - "Do not treat tests, metrics, judges, or ledgers as truth/review/action authority."
  - "Do not assume Codex has Claude-Code-style runtime role-file subagent isolation."
  - "Do not use GitHub stars, README demos, or showcase results as proof of quality."
tags:
  - candidate
  - provisional
  - agentic-loops
  - agent-skills
  - evaluator-optimizer
---

# 候选蒸馏：Agent-Loop-Skills

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话结论

这个仓库值得入库，而且是强借鉴：

```text
Agent-Loop-Skills = 把 agent loop 做成可安装 skill 的模式库
核心不是“更聪明的 prompt”
而是“artifact + signal + ledger + stop”的可审计迭代结构
```

对 VAKS/MISA 最有价值的不是直接跑它的 loop，而是吸收它的工程形状：

```text
每个循环必须绑定：
1. 要改进的 artifact
2. 可检查的反馈信号
3. 每轮只做一个可归因改变
4. append-only ledger
5. 明确 stop / budget / human interrupt
6. 失败则 revert / discard / refute
```

## Source

```yaml
derived_from:
  - raw/repos/2026-06-23-gaasher-Agent-Loop-Skills-source.md
  - raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-loop-five-ingredients.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-verification-gated-keep-revert.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-spawn-or-degrade-boundary.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-literature-evidence-matrix.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-tournament-judge-calibration.md
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
    selector_type: file_line
    selector_value: README.md:46-54
  - snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
    selector_type: file_line
    selector_value: docs/skill-authoring-rules.md:28-37
  - snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
    selector_type: file_line
    selector_value: loops/optimize-loop/SKILL.md:16-21
```

## Candidate Points

### Candidate Point 1: Loop Is A Skill, Not Just A Prompt

The repo reframes a skill as a reusable loop program:

```text
SKILL.md program
-> user-bound artifact
-> real signal
-> append-only ledger
-> stop condition
```

This is better than "write a prompt that tells the agent to improve things" because it forces every loop to answer:

```text
What is being changed?
Who/what scores it?
What gets kept?
What gets discarded?
How do we know what happened?
When do we stop?
```

For VAKS, this maps cleanly to source-intake and review workflow design, but only as candidate operational scaffolding.

### Candidate Point 2: Verification-Gated Keep/Revert Is The Core Discipline

The strongest pattern across the repo is:

```text
propose one change
run in user's environment
measure the bound signal
keep only if better and still valid
otherwise revert / discard / refute
log the result
```

Examples:

```text
karpathy: scalar metric improves -> keep
optimize-loop: correctness gate passes AND metric improves -> keep
data-analysis: independently re-derived number supports the hypothesis -> record finding
literature-survey: new matrix-changing sources continue appearing -> keep expanding
red-team: new distinct failure class appears -> continue
```

VAKS should borrow the shape, not the authority:

```text
signal = diagnostic / feedback
ledger = trace
review = later authority gate
```

### Candidate Point 3: Run Ledger Is The Missing Operational Memory Primitive

VAKS already has provenance, candidate, review, context pack, and feedback boundaries. Agent-Loop-Skills adds a practical runtime primitive:

```text
ledger.tsv:
  iteration
  change/hypothesis/query
  signal
  status
  description
```

This is useful for:

```text
source intake loops
operator cockpit loops
MISA work-order loops
red-team / blue-team loops
optimization loops
research survey loops
```

But the boundary must stay visible:

```text
ledger proves what the loop did
ledger does not prove the conclusion is true
```

### Candidate Point 4: Spawn-Or-Degrade Is A Good Portability Contract

The repo is honest that skill loading is broad, but runtime role-file subagent dispatch is host-specific.

Borrowable pattern:

```text
if host supports isolated subagents:
  spawn role agents
else:
  run roles inline, serially, with same output contract
```

For Codex/VAKS, this is important because we should not design a workflow that assumes Claude-Code-only isolation. A VAKS loop should declare:

```text
real_parallel_roles_available: yes/no
fallback_mode: inline
authority_boundary_unchanged: true
```

### Candidate Point 5: Evidence Matrix Loop Is Especially Relevant To VAKS

`literature-survey` has a close cousin to VAKS review thinking:

```text
sources x claims matrix
supports / contradicts / qualifies
verbatim snippet per cell
saturation measured by new matrix-changing sources
coverage note naming thin spots
```

This is not enough to be reviewed knowledge, but it is a very good candidate-layer review-input generator.

Potential VAKS mapping:

```text
source intake research question
-> candidate evidence/contradiction matrix
-> source annotations / evidence packet candidates
-> later evidence-aware review
```

### Candidate Point 6: Tournament Judge Calibration Is Useful But Risky

`tournament-autoresearch` adds a strong idea:

```text
judge predicts which idea will help
real run measures realized delta
judge logs predicted-vs-realized
judge updates working rubric
```

This is good for agent self-improvement under a measurable metric. But for VAKS:

```text
judge calibration can improve selection heuristics
judge calibration cannot create truth confidence
judge hit-rate cannot become evidence support
```

## What We Should Borrow

Borrow P1:

```text
loop-as-skill shape
five mandatory ingredients
append-only run ledger
one-change-per-iteration attribution
explicit stop/budget/patience
verification-gated keep/revert/refute
spawn-or-degrade host boundary
best-iteration reporting
```

Borrow P2:

```text
literature evidence/contradiction matrix as review-input generator
data-analysis "no finding without number" discipline
optimize-loop correctness-gate + metric design
red-team loop-until-dry as find-only phase before separate fix/re-verify
tournament judge calibration for measurable execution tasks
```

Borrow P3 / watch:

```text
plugin marketplace packaging
host-specific subagent adapters
showcase ledgers as communication examples
generic loop authoring checklist
```

Do not borrow:

```text
infinite loop as default VAKS behavior
agent autonomy without user-approved boundary
judge score as evidence
metric improvement as truth
GitHub popularity as source quality
README demo as reproduced proof
subagent isolation assumptions outside Claude Code
```

## Does It Help VAKS?

Yes, strongly, but it helps a different layer than VAKS truth.

| Area | Help Level | Why |
|---|---:|---|
| Agent/operator loop design | 9/10 | Gives a clean, reusable loop contract. |
| Source intake automation | 8/10 | Ledgers, stop rules, and signal gates fit intake loops well. |
| Review-input generation | 7/10 | Literature matrix and data verification are strong candidate generators. |
| Truth/review/action authority | 2/10 | It does not solve evidence-aware review or action basis. |
| MISA execution loop | 8/10 | Good work-order/evaluator-optimizer pattern. |
| VAKS ordinary capture UX | 4/10 | Too heavy if applied to everyday notes. |

## 跟我们比哪个厉害？

说人话：

```text
它比 VAKS 更会“跑循环”。
VAKS 比它更会“管权威”。
```

Agent-Loop-Skills 强在：

```text
可执行循环
每轮可归因
信号门
ledger
host portability
skill packaging
```

VAKS 强在：

```text
raw / candidate / reviewed / action basis 分层
source annotation 和 evidence packet 边界
reviewed relation / action support
feedback 不改 truth
retrieval 不等于 authority
```

综合评分：

```text
作为 agent loop 模式库：8.5/10
作为 VAKS 核心知识架构：3/10
作为 VAKS/MISA 可借鉴运行层：8/10
```

最优融合：

```text
VAKS 保持权威边界。
Agent-Loop-Skills 的 loop contract 作为候选运行层 / operator loop 模板。
```

## Open Questions

- Should VAKS define a `loop-run` artifact template for source-intake/operator loops?
- Should source-intake loops require a ledger with `change/signal/decision/status` columns?
- Should every agent loop include `action_basis_allowed: false` until an Evidence Packet checks results?
- Should MISA work-order loops borrow the optimize-loop pattern: gate first, metric second, keep best?
- Should a future VAKS query/research loop use `literature-survey` style matrix before evidence-aware review?

## Routing Hint

Route this source to:

```text
agentic-loop-design
operator cockpit
source intake loop design
MISA execution/work-order loops
evaluator-optimizer workflows
research survey / evidence matrix
red-team / blue-team workflow
```

Do not route it to:

```text
reviewed truth
action basis
evidence support
default ordinary capture
automatic promotion
background automation
```

## Forbidden

```text
project_borrow_scope as adoption decision
decision outcome
formal pattern
action basis
truth confidence
loop-output-as-evidence
judge-score-as-review
GitHub-metadata-as-quality-proof
```

## Local Verification

Executed:

```text
git clone --depth 1
git rev-parse HEAD
git log -1
git archive HEAD
Get-FileHash SHA256
local source inspection
```

Not executed:

```text
no loops installed
no loop run reproduced
no showcase benchmark rerun
no host compatibility test
```

## Final Judgment

```text
borrow_value: strong
borrow_order: P1
best_use: bounded agent/operator loop scaffolding
not_best_use: truth/review/action authority
```

说人话：

```text
这东西该收。
但别把它当“可信知识系统”，它是“把 agent 做事变成可审计循环”的工程模板。
我们应该把它放在 VAKS/MISA 的运行层候选库里，别让 loop 热度冲进 truth 层。
```
