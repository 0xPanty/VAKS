---
type: library_review
status: draft
library_name: "Agent-Loop-Skills"
repo_url: "https://github.com/gaasher/Agent-Loop-Skills"
source_url: "raw/repos/2026-06-23-gaasher-Agent-Loop-Skills-source.md"
checked_commit: 25dd18fc93523c212addd46fad540c779b18515a
commit_time: 2026-06-22T06:46:38-04:00
source_status: active
reviewed_at: 2026-06-23
domain:
  - agentic-loops
  - agent-skills
  - evaluator-optimizer
  - autoresearch
  - workflow-ledger
related_projects:
  - verified-action-knowledge-system
current_branch: "VAKS source-intake/operator-loop design and future MISA execution workflows"
extracted_patterns:
  - loop-as-skill
  - five-ingredient-loop-contract
  - verification-gated-keep-revert
  - append-only-run-ledger
  - spawn-or-degrade-roles
  - evidence-contradiction-matrix
fusion_decision: adapt
confidence: medium
evidence_count: 18
cross_validated_with:
  - "VAKS raw/candidate/reviewed/action-basis boundary"
  - "VAKS tests/benchmarks/judges are diagnostics, not approval"
  - "VAKS Source Annotation Sidecar locator-only boundary"
negative_evidence:
  - "No loop was executed during this intake."
  - "README/showcase benchmark claims were not reproduced."
  - "Runtime subagent isolation is not portable to Codex without explicit user-triggered agent setup."
  - "Loop metrics and ledgers do not create truth, review, evidence support, or action basis."
extension_potential: "High as a candidate operational-loop template for VAKS/MISA; low as a truth/review architecture."
relations: []
tags:
  - architecture-review
  - agentic-loops
  - agent-skills
  - evaluator-optimizer
---

# 库分析：Agent-Loop-Skills

## 它解决什么问题

它解决的不是“知识如何变真”，而是：

```text
agent 如何一轮一轮把一个 artifact 变好
并且每轮都有信号、ledger、keep/revert/stop 规则
```

仓库把多个常见 agent 工作流包装成 open-standard Agent Skills：

```text
autoresearch
scientific writing
literature survey
data analysis
optimization
prompt optimization
red-team
power analysis
```

说人话：它把“让 agent 反复改进”从一句口头指令变成一组可安装、可复用、可记录的循环模板。

## 核心设计

核心抽象：

```text
loop = program + artifact slot + feedback signal + run ledger + termination/budget
```

仓库结构：

```text
README.md
docs/
loops/<loop-name>/SKILL.md
loops/<loop-name>/roles/
loops/<loop-name>/schemas/
loops/<loop-name>/tools/
loops/<loop-name>/examples/
showcase/
.claude-plugin/
```

关键运行原则：

```text
bind user's artifact and environment at invocation time
run one focused iteration
measure a real signal
keep only if signal says better
log append-only
stop by threshold / plateau / budget / saturation / human interrupt
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:46-49` | The repo says each loop is generic and binds program, artifact, signal, ledger, termination at invocation time. | Central loop-as-skill thesis. | README thesis is architecture framing, not proof of performance. |
| `README.md:51-55` | It names unsupervised loop failure risk and verification-gated discipline. | Honest autonomy boundary. | Verification gate still depends on signal quality. |
| `README.md:72-77` | Lists five ingredients and spawn-or-degrade. | Good reusable loop contract. | Need host-specific execution checks. |
| `docs/authoring.md:7-18` | Hard constraints: self-contained folder, one SKILL.md, no hardcoded bindings, spawn-or-degrade, ledger. | Good skill authoring hygiene. | Authoring rule is not runtime validation. |
| `docs/skill-authoring-rules.md:28-37` | Formalizes five ingredients. | Strongest borrowable pattern. | Candidate operational contract only. |
| `docs/skill-authoring-rules.md:150-194` | Stdlib tools, user environment execution, no silent heavy deps. | Good environment contract. | User env execution remains operational risk. |
| `docs/skill-authoring-rules.md:203-211` | Eval-driven sandbox and Sonnet-run authoring target. | Good validation culture. | Not proof every loop has passing eval in this snapshot. |
| `docs/compatibility.md:26-43` | Explains why runtime role-file subagent dispatch is Claude-Code-specific and inline elsewhere. | Excellent portability warning. | Codex should not assume real isolated role agents. |
| `.claude-plugin/plugin.json:1-12` | Plugin metadata and skills path. | Install/package shape. | Claude plugin metadata only. |
| `loops/karpathy/SKILL.md:17-22` | Minimal autonomous metric-improvement loop. | Baseline loop form. | Infinite until human interrupt is risky for VAKS. |
| `loops/karpathy/SKILL.md:89-99` | Loop checklist: edit, run, read metric, log, keep/revert. | Attribution and signal gate. | Metric can be gamed if harness editable. |
| `loops/optimize-loop/SKILL.md:16-31` | Correctness gate plus metric minimization. | Best evaluator-optimizer pattern. | Gate strength determines safety. |
| `loops/optimize-loop/SKILL.md:65-81` | Baseline, snapshot, one change, gate, metric, keep/discard, ledger. | Strong general operator loop shape. | Still diagnostic, not review/action authority. |
| `loops/data-analysis/SKILL.md:19-23` | Hypothesis -> verify; no insight without a number. | Useful data-analysis discipline. | Number is not causal proof. |
| `loops/literature-survey/SKILL.md:20-28` | Evidence/contradiction matrix with verbatim snippets. | Strong review-input generator for VAKS. | Matrix is candidate evidence map, not reviewed knowledge. |
| `loops/literature-survey/SKILL.md:129-145` | Never fabricate, map disagreement, measured saturation. | Good anti-smoothing and coverage discipline. | Saturation is local to search protocol. |
| `loops/tournament-autoresearch/SKILL.md:19-25` | Idea tournament and realized-delta judge calibration. | Useful measurable selection calibration. | Judge calibration is not truth confidence. |
| `loops/tournament-autoresearch/SKILL.md:153-169` | Calibration ledger and judge lessons. | Selection-memory pattern. | Hit-rate is a heuristic signal only. |

## 当前支线价值

当前支线：

```text
VAKS source-intake/operator-loop design and future MISA execution workflows
```

它对当前支线：

```text
refines
```

具体价值：

- Gives VAKS a concrete "loop-run" shape for future bounded source-intake and review-input generation.
- Gives MISA a clean pattern for evaluator-optimizer and work-order loops.
- Gives source-intake a practical ledger primitive.
- Gives future red-team/blue-team workflows a find -> fix -> re-verify separation.
- Gives host-portability language that prevents Codex/Claude-specific assumptions from leaking into the design.

风险：

- "Loop until interrupted" conflicts with VAKS's ordinary light capture and user-confirmed write boundaries.
- Metrics, judges, benchmarks, and ledgers can create false authority if mixed with reviewed knowledge.
- A weak gate can be optimized while behavior silently changes.
- In Codex, role-file subagent dispatch should degrade inline unless the user explicitly sets up subagents.
- Showcase success can seduce design into benchmark theater without evidence-aware review.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Strongly compatible with simple loopable ingest/query/lint commands. | adapt |
| Dusk workbench | Ledgers and loop states can feed an operator cockpit. | adapt |
| source ingest | Useful for bounded source-intake loops and capture ledgers. | adapt with guardrails |
| review queue | Literature matrix / claim verification can generate review inputs. | adapt as candidate only |
| schema / reviewed knowledge | No authority model; does not replace VAKS schema. | no |
| memory / dev context | Run ledgers can become Cold Reference / Support for dev context. | adapt |
| feedback | Strong operational feedback discipline, but feedback remains diagnostic. | adapt |
| retrieval / cache | Literature-search skill offers retrieval tooling, but not authority. | watch |
| API / MCP / agent access | Skill packaging and spawn-or-degrade are useful. | adapt |
| viewer / workbench | Ledgers/showcase style can inspire progress views. | adapt later |
| publishing | Showcase ledgers and result charts are good communication artifacts. | watch |
| risk / anti-pattern | Major risk: loop output / metric / judge score mistaken for truth. | keep warning |

## 值得提炼的模式

### Pattern 1: Five-Ingredient Loop Contract

```text
program
artifact slot
feedback signal
run ledger
termination / budget
```

This is the cleanest general pattern. VAKS can reuse it for any future loop-run artifact.

### Pattern 2: Verification-Gated Keep/Revert

```text
one change
same gate
same metric
keep only if valid and better
otherwise restore
append ledger row
```

For VAKS/MISA, the key is to preserve the difference:

```text
valid_for_loop != reviewed knowledge
metric_better != action_basis
```

### Pattern 3: Ledger As Runtime Provenance

The append-only ledger is operational provenance:

```text
what was tried
what signal was measured
what decision was made
what artifact won
```

VAKS already has source provenance; this adds loop-run provenance.

### Pattern 4: Evidence Matrix Before Review

The literature survey loop can generate:

```text
claim/source matrix
stance per source
verbatim snippet
contested flag
coverage note
```

This is close to VAKS Evidence Packet preparation, but still candidate.

### Pattern 5: Spawn-Or-Degrade Roles

For multi-role workflows:

```text
spawn if isolated subagents are supported
degrade inline otherwise
keep same schema/contract
```

This prevents tool-specific architecture.

### Pattern 6: Self-Calibrating Judge For Measurable Domains

Judge calibration is useful when the domain has realized outcomes:

```text
prediction -> run -> realized delta -> hit/miss -> rubric update
```

For VAKS, use only as selection heuristic feedback, never as truth confidence.

## 标签与量化

- domain: agentic loops / agent skills / evaluator optimizer
- problem: agents need repeatable, signal-gated improvement loops rather than one-shot prompting
- pattern: loop-as-skill
- maturity: experimental / emerging
- complexity: medium
- problem_fit: 5/5 for operator-loop design, 2/5 for truth architecture
- reuse_value: 5/5 for VAKS/MISA runtime workflows
- implementation_cost: 2/5 to borrow pattern, 4/5 to run/maintain loops
- integration_fit: 4/5 as sidecar/operational layer
- evidence_strength: 3/5 for design extraction, 1/5 for performance claims not reproduced
- reversibility: 5/5 if kept as candidate sidecar

## 交叉验证

- 相似设计来源：Karpathy autoresearch, evaluator-optimizer loops, red-team harnesses, scientific agent skills.
- 用户历史项目里的相似问题/影子：VAKS source-intake pipelines, MISA/Hermes work-order loop, VAKS Guard read-only lazy gate, source annotation and evidence packet boundaries.
- 支持证据：Repo includes 20 loop folders, docs, role prompts, schemas, stdlib tools, examples, showcase ledgers, plugin metadata.
- 反例或失败边界：No local execution; weak gates can be gamed; infinite loops conflict with ordinary intake; subagent isolation host-dependent.
- 最小验证方式：Create a tiny VAKS sandbox loop-run spec and require ledger + authority labels + no action_basis before review.

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Loop should be a first-class artifact with program/artifact/signal/ledger/stop. | VAKS already separates source/candidate/review/action but lacks a formal loop-run artifact. | missing_evidence / candidate_relation | Should VAKS add a lightweight `loop-run` template under outputs/review or keep it informal? |
| Metric-gated keep/revert makes agent work auditable. | Tests/benchmarks/judges are diagnostics, not approval. | refines | How do we label loop signals so they never become support? |
| Literature matrix can prepare review inputs. | Evidence Packet requires point/source anchor/warrant/scope/risk. | candidate_relation | Can matrix cells become source_annotation or evidence_packet candidates? |
| Spawn-or-degrade prevents host lock-in. | VAKS should not globalize tool-specific workflows. | supports as design boundary | Should every multi-role VAKS workflow declare host fallback mode? |
| Infinite loop can improve measurable ML tasks. | Ordinary VAKS capture must stay light and user-scoped. | scope_mismatch | Which VAKS loops are allowed to run until interrupt, if any? |

## Support / Challenge Review

- What supports it:
  - Source code/docs show a consistent loop contract across README, authoring rules, and multiple loop SKILL files.
  - Multiple loops implement explicit gate + ledger + stop patterns.
  - Compatibility docs clearly expose host-specific subagent limits.
- What challenges it:
  - No loops were executed in this intake.
  - Showcase results are source claims, not reproduced evidence.
  - Some loops intentionally run forever, which conflicts with VAKS ordinary intake defaults.
  - A loop can optimize a weak metric or overfit a judge.
- Challenge severity: minor for design borrowing; major for direct operational adoption.
- Scope limits:
  - Use as candidate operational-loop template.
  - Do not use as reviewed knowledge, action basis, or autonomous background automation.
- Known risks:
  - loop-output-as-truth
  - metric-gaming
  - weak-gate-overtrust
  - host-isolation-assumption
  - hype/popularity-as-proof
  - infinite-loop-scope-creep
- Review again when:
  - VAKS designs a real loop-run template.
  - MISA uses evaluator-optimizer loops in production.
  - A loop output is proposed as action-facing support.
- Action readiness: not_ready

## 对当前项目的适配点

Potential VAKS uses:

```text
source-intake loop-run ledger
literature survey candidate matrix
claim-verify candidate precheck
red-team find-only loop for guardrails
operator cockpit progress surface
loop authoring checklist for local skills
```

Potential MISA uses:

```text
work-order evaluator-optimizer
benchmark-gated code improvement
prompt optimization against local oracle
red-team / blue-team cycles
selection judge calibration where real metrics exist
```

Required VAKS label on any loop-run artifact:

```yaml
record_kind: loop_run
knowledge_status: candidate
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: loop_signal_not_support
truth_mutation_allowed: false
action_basis_allowed: false
```

## 可拓展性

- 是否适合作为插件/适配层：yes, as external skill collection or design source.
- 是否会绑定核心结构：no, if kept as operational sidecar.
- 未来替换成本：low; the five-ingredient contract is portable.
- 可迁移路径：
  1. Keep source as candidate.
  2. Extract a small `loop-run` template only after user confirmation.
  3. Add authority labels and evidence/action warnings.
  4. Pilot on one bounded source-intake or MISA task.
  5. Promote only after evidence-aware review.

## 复杂度和风险

The pattern is simple, but the temptation is dangerous:

```text
agent loop looks productive
ledger fills up
metric moves
user feels progress
```

But for VAKS:

```text
activity != support
metric != truth
judge != reviewer
ledger != evidence packet
```

This must stay visible in any borrowed design.

## 不可行点 / 避坑

- Do not make agent loops the default for ordinary capture.
- Do not run background loops without explicit user scope.
- Do not let loop ledgers enter reviewed/action buckets.
- Do not treat self-calibrating judges as human review.
- Do not assume Claude Code runtime role dispatch works in Codex.
- Do not count "new sources found" as evidence sufficiency.
- Do not use showcase metrics as proof without rerun.

## 融合判断

- 结论：adapt
- 理由：Excellent operational-loop design source; weak/no authority model.
- 验证方式：Pilot a bounded VAKS source-intake loop-run artifact with ledger, stop rule, and `action_basis_allowed: false` receipts.

## 直接判断

- Direct use: no for VAKS core; maybe for isolated experimental tasks.
- Fork: no.
- Design-only: yes, strong.
- Reject: no.
- Current branch value: high for loop-run/operator workflow design.
- Whole architecture value: operational sidecar, candidate review-input generator.
- Risk: loop signal mistaken for truth/action support.
- Next action: keep candidate-only; consider a future lightweight `loop-run` template after user confirmation.

## 后续行动

- Add to future VAKS/MISA operator-loop design references.
- If the user later wants implementation, start with one tiny bounded loop, not a general loop framework.
- Any loop-run output must point back to raw source anchors or stable artifacts before it can feed review.
