---
type: library_review
status: candidate
library_name: AI Vibe Writing Skills
repo_url: https://github.com/donghuixin/AI-Vibe-Writing-Skills
source_url: https://github.com/donghuixin/AI-Vibe-Writing-Skills
checked_commit: dbfee78dac29c0c347354ffe696cf124b80c1817
commit_time: 2026-06-02T20:49:52+08:00
source_status: active
reviewed_at: 2026-06-07
domain: agent-writing-workflow
related_projects:
  - verified-action-knowledge-system
current_branch: source-intake-review-dev-context
extracted_patterns:
  - spec-driven-agent-workflow
  - defensive-red-team-review
  - hard-soft-memory-boundary
  - failed-review-forced-rewrite
  - prompt-slice-router
fusion_decision: adapt
confidence: medium
evidence_count: 26
cross_validated_with:
  - SOURCE_INTAKE.md
  - REVIEW_QUEUE.md
  - DEV_CONTEXT.md
  - FEEDBACK.md
negative_evidence:
  - prompt conventions are not runtime verification
  - AI detector/PPL must stay diagnostic only
extension_potential: high
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
action_basis_allowed: false
truth_mutation_allowed: false
relations: []
---

# 库分析：AI Vibe Writing Skills

## 它解决什么问题

这个仓库解决的是 AI 写作从“一次性聊天生成”变成“可配置、可复核、可迭代的本地写作工程”的问题。

它的对象不是普通知识库，而是写作工作流：

```text
写作需求
-> 文档规范
-> 大纲与 DoD
-> 风格/错题本/硬记忆/软记忆/参考文献召回
-> 内容生成
-> 防御性预审
-> 检阅审计
-> 失败回写和重写
```

## 核心设计

它的核心设计可以压成五层：

1. **Workspace contract**：`.traerules` 定义工作区级别的 agent 行为。
2. **Context files**：`.ai_context` 保存 spec、style、error log、memory、reference library、templates。
3. **Modular prompts**：每个 agent 有独立 prompt：writer、reviewer、router、compactor、defensive writing、PDF reader 等。
4. **Automation workflows**：`.agents/workflows` 把模块串成完整流程。
5. **Diagnostic tooling**：PDF parsing、MinerU 示例、AI-style check、LaTeX self-healing 作为辅助工具。

这不是一个强 runtime，而是一个“文件即操作契约”的 agent skill repo。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:25` | Project describes itself as local AI writing context system | File-backed context system, not web app | README claim |
| `README.md:104` | Workflow contract | Spec -> outline -> recall -> draft -> defend -> review -> iterate | Design-level evidence |
| `README.md:165` | Agent system table | Clear agent/module roles | Documentation |
| `README.md:184` | Defensive writing | Reviewer attack pre-review | Candidate review pattern |
| `README.md:320` | PDF and evidence ingestion | Structured reference intake | Needs VAKS-grade anchors |
| `README.md:360` | Local AI style check | Diagnostic lint tool | Not authority |
| `SKILLS.md:5` | Mandatory system process | Internal process summary | Design-level evidence |
| `SKILLS.md:79` | Spec audit rigidity | Failure is not vague advice | Strong workflow signal |
| `SKILLS.md:80` | Defensive writing strategy order | Upper/middle/lower strategy ladder | Strong workflow signal |
| `.traerules:5` | Workflow instructions | Workspace contract | Prompt convention |
| `.traerules:58` | Multi-agent loop | Orchestration order | Prompt convention |
| `.ai_context/custom_specs.md:1` | User settings template | Context budget, evidence, review, defensive settings | Config skeleton |
| `.ai_context/document_spec_template.md:1` | Document spec as source of truth | Task contract pattern | Writing-specific |
| `.ai_context/outline_template.md:1` | Outline JSON/YAML with DoD | Checkable output contract | Adaptable |
| `.ai_context/prompts/6_outline_manager_agent.md:6` | Outline must generate DoD | Gate before writing | Prompt convention |
| `.ai_context/prompts/7_content_writer_agent.md:14` | Writer must implement every DoD | Constrained candidate generation | Prompt convention |
| `.ai_context/prompts/8_content_review_agent.md:5` | Spec and DoD are audit standard | Review checks against source contract | Candidate review pattern |
| `.ai_context/prompts/8_content_review_agent.md:138` | Spec Audit task | Machine-readable failed specs | Candidate review pattern |
| `.ai_context/prompts/8_content_review_agent.md:144` | Failures force rewrite | Closed-loop correction | Strongest reusable loop |
| `.ai_context/prompts/9_workflow_coordinator.md:4` | Coordinator workflow | End-to-end orchestration | Prompt convention |
| `.ai_context/prompts/10_pdf_reader_agent.md:1` | PDF reader role | Evidence/reference extraction | Needs stronger provenance |
| `.ai_context/prompts/11_context_compactor_agent.md:8` | Compact context | Context budget / continuity | Strong dev-context fit |
| `.ai_context/prompts/12_router_agent.md:28` | Prompt slice routing | Dynamic context loading | Strong dev-context fit |
| `.ai_context/prompts/13_latex_self_healing_agent.md:5` | Script -> execute -> verify | Tool loop | Safety caution |
| `.ai_context/prompts/14_defensive_writing_agent.md:4` | Defensive writing definition | Contribution boundary / limitation disclosure / misunderstanding prevention | Strong review analogy |
| `.ai_context/prompts/14_defensive_writing_agent.md:153` | Attack -> Validity Threat -> Boundary Reframing -> Evidence Anchor | Reusable review frame | Candidate only |
| `.ai_context/reference_learning.md:17` | Reference/hard/soft memory split | Memory lane separation | Needs truth-boundary hardening |
| `Local_AI_Style_Check/paper_ai_detector.py:33` | LaTeX cleanup | Diagnostic implementation | Lint only |
| `Local_AI_Style_Check/paper_ai_detector.py:76` | PPL calculation | Style/AI trace heuristic | Not evidence |

## 当前支线价值

当前支线：

```text
source-intake / review-queue / dev-context / operator workflow
```

它对当前支线：

```text
refines
```

具体价值：

- 给 Source Intake 的 heavy path 一个更清楚的 operator surface：先 spec，再 DoD，再 candidate，再 review，再 rewrite。
- 给 REVIEW_QUEUE 一个“attack-surface / evidence-anchor / claim-calibration”的可读辅助框架。
- 给 DEV_CONTEXT 一个 router / compactor 的低成本实现直觉：按任务加载，不全量加载。
- 给 maintenance lint 一个边界提醒：AI-style detector 只能做 diagnostic input。

风险：

- 仓库写作场景中的 `hard_memory` 比 VAKS truth boundary 松，不能直接复制。
- Review 主要是规范、风格、证据覆盖检查，不等于 VAKS evidence-aware review。
- Prompt convention 不是 verified runtime；不能因为文件写了流程就认为流程已真实执行。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | File-first, local context, visible prompts and memory files | adapt |
| Dusk workbench | Workflow commands and context folders act like task workbench | adapt |
| source ingest | PDF/reference intake target list is useful | adapt with stronger anchors |
| review queue | Spec Audit + Defensive Audit + failed_specs -> rewrite is strong | adapt |
| schema / reviewed knowledge | No direct reviewed schema; memory is too loose | reject direct use |
| memory / dev context | hard/soft/reference/error split helps activation and preference boundaries | adapt |
| feedback | error_log turns user correction into future constraint | adapt with truth quarantine |
| retrieval / cache | minimal; no strong search runtime | watch |
| API / MCP / agent access | optional detector adapter/MCP idea only | watch |
| viewer / workbench | no significant UI except MinerU GUI | low |
| publishing | strong for academic writing workflow, not VAKS publishing layer yet | watch |
| risk / anti-pattern | AI detector as authority; hard_memory as unreviewed fact store; self-healing scripts | avoid |

## 值得提炼的模式

### `spec-driven-agent-workflow`

Before generation, create a task-local spec that fixes scope, claims, evidence requirements, and negative constraints.

VAKS adaptation:

```text
Use for significant action, architecture absorption, review package, or risk-sensitive answer.
Do not use for ordinary query.
```

### `dod-as-reviewable-output-contract`

DoD makes an output auditable without turning every task into full formal verification.

VAKS adaptation:

```text
Use a small DoD for important candidate/review/action outputs:
- source anchor present
- boundary field present
- action_basis_allowed false unless review passed
- known gaps / challenge surfaced
```

### `defensive-red-team-before-finalization`

The defensive writing agent is a useful pattern beyond writing: simulate the skeptical reviewer before finalizing a strong claim.

VAKS adaptation:

```text
Attack -> Validity Threat -> Boundary Reframing -> Evidence Anchor
```

This can become an optional review aid inside Evidence Packet / Known Omission Check, not a new truth layer.

### `failed-review-forced-rewrite`

If audit fails, state transition matters. The item should go back for revision, not accumulate polite suggestions.

VAKS adaptation:

```text
candidate remains candidate
review_pressure: review_due / blocked
action_basis_allowed: false
next_step: revise / narrow / split / collect evidence
```

### `prompt-router-and-context-compactor`

The repo's router and compactor are a practical reminder that context loading should be scoped.

VAKS adaptation:

```text
Index tells where to start.
Dashboard tells what is live.
Briefing tells what deserves full reading.
Dev context pack decides what is loaded.
Review gate decides what is true.
```

## 标签与量化

- domain: agent-writing-workflow
- problem: AI generation needs durable task contract, memory, review, and rewrite loop
- pattern: spec-driven candidate-to-review workflow
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 4
- evidence_strength: 3
- reversibility: 5

## 交叉验证

- 相似设计来源：Karpathy LLM Wiki file-first workflow, VAKS Source Intake, REVIEW_QUEUE, DEV_CONTEXT, maintenance-manifest boundaries.
- 用户历史项目里的相似问题/影子：VAKS 反复强调 source/candidate/review/action boundary 和 operator-readable handoff.
- 支持证据：README workflow contract, SKILLS process, `.traerules`, prompt files, memory/reference templates.
- 反例或失败边界：prompt conventions are not runtime proof; detector scoring is easy to overclaim.
- 最小验证方式：create one VAKS operator review checklist using task_contract + DoD + red-team + failed_specs for a real candidate package, without schema changes.

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Spec before writing reduces drift | VAKS intent confirmation and action-facing gates | refines | Should high-impact VAKS tasks get a small task_contract surface? |
| DoD makes review concrete | VAKS Evidence Packet / maintenance manifest | refines | Should DoD be a template block or just review package language? |
| Defensive red-team catches reviewer attacks early | Evidence-Aware Review, Known Omission Check | refines | Can attack-surface framing become optional Evidence Packet aid? |
| Hard/soft memory split prevents mixed recall | Activation Tier and Feedback truth quarantine | supports/refines | How to keep hard memory from implying reviewed facts? |
| AI detector detects style issues | Maintenance lint boundary | risk_of | How to prevent detector score from becoming authority? |
| Self-healing scripts close tool loops | Agent tool safety quarantine | risk_of | What approval/sandbox boundary is required before VAKS borrows tool-loop automation? |

边界：

- 相似不是支持。
- 冲突不是自动推翻。
- 重复出现不是自动真理。
- 校准输出是 review input，不是 reviewed relation。

## Support / Challenge Review

- What supports it:
  - Repository files consistently express the same workflow across README, SKILLS, `.traerules`, workflows, and prompt files.
  - The content review and defensive writing prompts include explicit failure and claim-calibration rules.
  - Memory/reference templates show actual file-level separation.

- What challenges it:
  - The repository is mostly prompt conventions, not a validated runtime.
  - Memory writeback is looser than VAKS truth mutation boundaries.
  - AI detector heuristics are fragile and can be overread.
  - Self-healing tool loops may be unsafe outside a controlled code workspace.

- Challenge severity: major for direct adoption; minor for design-only adaptation.
- Scope limits:
  - Strongest value is workflow / operator surface.
  - Weakest value is truth/evidence authority.
- Known risks:
  - Overdesigning VAKS with a new formal lane.
  - Treating writing review as evidence review.
  - Letting style lint pollute truth boundary.
- Review again when:
  - A concrete VAKS operator workflow needs a task contract / DoD / red-team pass.
  - Agent writeback or tool-loop automation is reopened.
- Action readiness: not_ready

## 对当前项目的适配点

VAKS should borrow:

```text
1. Task contract for significant work.
2. DoD for important output review.
3. Defensive red-team framing for candidate point pressure tests.
4. Failed audit -> state transition / rewrite loop.
5. Router / compactor as dev-context operator ergonomics.
```

VAKS should not borrow:

```text
1. Hard memory as unreviewed fact authority.
2. AI detector as evidence.
3. Workflow pass as truth.
4. Self-healing execution loop without explicit safety.
5. Full prompt-agent stack as core architecture.
```

## 可拓展性

- 是否适合作为插件/适配层：yes, as an operator workflow / review assistant.
- 是否会绑定核心结构：should not; keep sidecar and optional.
- 未来替换成本：low if implemented as templates and review package blocks.
- 可迁移路径：
  - Add candidate-only task_contract block in review packages.
  - Add optional attack-surface table to Evidence Packet trial.
  - Add failed_specs/state transition in review outputs.
  - Keep detectors in maintenance manifest only.

## 复杂度和风险

Complexity is manageable if borrowed as operator templates. It becomes risky if VAKS tries to import all agents, workflow commands, detectors, memory stores, and self-healing tools at once.

Primary risk:

```text
把“写作质量闭环”误读成“知识可信闭环”。
```

They are adjacent, not identical.

## 不可行点 / 避坑

- Do not use PPL / AI detector score as trust.
- Do not let user correction immediately mutate reviewed knowledge.
- Do not use defensive reframing to rationalize unsupported claims.
- Do not create a mandatory spec for every ordinary source capture.
- Do not run self-healing scripts in VAKS without explicit authorization and path sandbox.
- Do not convert this into a new top-level architecture lane.

## 融合判断

- 结论：adapt
- 理由：The repo strongly validates VAKS' file-first, candidate-to-review, and failure-backflow instincts, but its authority model is weaker than VAKS and must stay candidate/operator-layer.
- 验证方式：one small VAKS review-package pilot using task contract + DoD + red-team table + failed_specs state transition, with no schema change.

## 直接判断

- Direct use: no
- Fork: no
- Design-only: yes
- Reject: no
- Current branch value: strong for Source Intake / Review Queue / Dev Context operator surfaces
- Whole architecture value: strong as candidate workflow reference, weak as truth authority
- Risk: overclaiming detector/workflow/memory authority
- Next action: keep as VAKS Project Overlay P1/P2 support; promote nothing until a concrete review pilot passes

## 后续行动

- If VAKS later reopens review package ergonomics, test a small `task_contract` and `failed_specs` block.
- If Evidence Packet needs a human-readable challenge table, test the defensive-writing four-part frame.
- If dev-context work resumes, compare router/compactor with `DEV_CONTEXT.md` Core / Support / Risk / Cold References.
- If agent tool loops resume, use this as a cautionary reference for self-healing automation boundaries.
