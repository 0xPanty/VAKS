---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
derived_from:
  - raw/repos/2026-06-07-donghuixin-ai-vibe-writing-skills-source.md
  - raw/repos/_snapshots/donghuixin-AI-Vibe-Writing-Skills-dbfee78dac29c0c347354ffe696cf124b80c1817.zip
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: yes
routing_hint:
  - source-intake
  - review-queue
  - dev-context
  - maintenance-lint
  - agent-workflow-boundary
possible_project_refs:
  - VAKS
point_anchor_refs:
  - source: raw/repos/2026-06-07-donghuixin-ai-vibe-writing-skills-source.md
    snapshot_ref: raw/repos/_snapshots/donghuixin-AI-Vibe-Writing-Skills-dbfee78dac29c0c347354ffe696cf124b80c1817.zip
borrow_value: strong
borrow_order:
  - "P1: Spec/DoD -> draft -> defensive red-team -> review audit -> forced rewrite as a practical candidate-to-review loop."
  - "P2: Hard/soft memory plus reference library as a useful split for activation, preference, and evidence orientation."
  - "P3: Router, compactor, LaTeX self-healing, AI-style detector, and PDF tooling as peripheral workbench ideas."
avoid:
  - "Do not treat AI detection, PPL, prompt output, or workflow pass/fail as truth confidence."
  - "Do not let reference_library or hard_memory write directly into reviewed knowledge."
  - "Do not copy self-healing script execution into VAKS without explicit tool-safety boundaries."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS operator workflows, review queue UI, action-facing review gates, or agent memory/write boundaries."
  support_when: "Comparing candidate review workflows, context compaction, prompt routing, source intake, or reviewer-facing red-team patterns."
  risk_when: "Any proposal tries to use AI detectors, workflow success, or memory entries as evidence support or truth."
  cold_references:
    - raw/repos/2026-06-07-donghuixin-ai-vibe-writing-skills-source.md
    - raw/repos/_snapshots/donghuixin-AI-Vibe-Writing-Skills-dbfee78dac29c0c347354ffe696cf124b80c1817.zip
tags:
  - candidate
  - provisional
  - repo-distillation
  - agent-workflow
  - defensive-review
---

# Candidate Distillation: AI Vibe Writing Skills as a Spec-Driven Review Loop

## Boundary

This note is one combined candidate knowledge point for `donghuixin/AI-Vibe-Writing-Skills`.

It can help route attention, compare ideas, or create a VAKS Project Overlay. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

The Bilibili video originally supplied with the repository was not used as evidence in this distillation because the user said the audio is not reliable enough. This candidate point is derived from the GitHub repository and snapshot only.

## 人话总结

这个库表面上是“AI 写作技能”，但真正有价值的是它把写作变成了一个文件化的可审计流程。

它不是让 AI 直接开写，而是先把任务变成 `document_spec`，再把 spec 变成带 DoD 的大纲，然后读取风格、错题本、硬记忆、软记忆和参考文献，生成草稿。草稿之后还要过防御性预审，提前模拟审稿人怎么攻击；最后再做 Spec Audit、AI 味检测、证据覆盖和 Defensive Audit。如果失败，不是温柔地给几个建议，而是打回重写。

和 VAKS 像的地方在这里：

```text
不要让一次生成直接变成结果。
先有输入契约，再有候选输出，再做风险/证据/边界检查，失败就回流。
```

但它和 VAKS 的关键差别也很清楚：

```text
它管的是写作质量和投稿可用性。
VAKS 管的是知识可信度、行动依据和 truth mutation 边界。
```

所以这份仓库最适合借流程，不适合借权威。

## Source

```yaml
derived_from:
  - raw/repos/2026-06-07-donghuixin-ai-vibe-writing-skills-source.md
checked_commit: dbfee78dac29c0c347354ffe696cf124b80c1817
snapshot_ref: raw/repos/_snapshots/donghuixin-AI-Vibe-Writing-Skills-dbfee78dac29c0c347354ffe696cf124b80c1817.zip
point_anchor_refs:
  - README.md:25
  - README.md:104
  - SKILLS.md:5
  - SKILLS.md:79
  - SKILLS.md:80
  - .traerules:5
  - .ai_context/prompts/8_content_review_agent.md:138
  - .ai_context/prompts/8_content_review_agent.md:144
  - .ai_context/prompts/14_defensive_writing_agent.md:153
```

## Candidate Points

### 1. `document_spec` 是任务级 source of truth，不是让 AI 猜用户要什么

仓库把大型写作任务前置成 `document_spec.md`：主题、目标、受众、核心论点、证据要求、约束、要缩窄的 claim 都先写出来。README 的 workflow contract 和 workflow coordinator 都强调，先有 spec，再有 outline 和 draft。

VAKS 借鉴点：

```text
对高影响回答、action basis、review package、架构吸收，不要直接让 agent 生成。
先写一个轻量 task contract / intent backbrief：
- 本次问题是什么
- scope_in / scope_out 是什么
- 要用哪些证据
- 哪些 claim 不能越界
- 成功标准是什么
```

这和 VAKS 已有的 intent confirmation、Evidence Packet、Context Pack Trace 很贴近，可以作为 operator workflow 的可读表层。

### 2. DoD 把“好不好”变成可检查的输出约束

仓库的大纲不是普通 outline，而是带 `definition_of_done` 和 `defensive_dod` 的结构。写作 agent 必须逐条落实 DoD，review agent 再逐条审计。

VAKS 借鉴点：

```text
普通 candidate point 不需要 DoD。
但重要输出可以有一个最小 DoD：
- 是否保留 raw source anchor
- 是否标明 candidate/reviewed/action boundary
- 是否列出 known gaps / counterevidence
- 是否区分 support、background citation、orientation
- 是否有 scope/applicability 限制
```

这不是新 schema，而是 review / action-facing workflow 的检查面。

### 3. Hard memory / soft memory / reference library 的三分法有用，但权威太松

仓库区分：

```text
hard_memory: 术语、单位、关键事实
soft_memory: 偏好、语气、表达习惯
reference_library: 参考文献与证据
error_log: 负面约束和错题本
```

这和 VAKS 的 Activation Tier、Feedback Ledger、Source Intake 有相似直觉：不要把事实、偏好、纠错、参考来源混成一个记忆池。

VAKS 可借：

```text
继续强化“记忆不是 truth”：
- exact facts / terms 可以变成 candidate facts 或 reviewed terms
- preferences 只能影响表达和 activation
- corrections 创建 review_pressure 或 feedback-event
- source/reference entries 是 provenance / evidence candidates，不是 support 本身
```

VAKS 不能借：

```text
不能让 agent 把 PDF 摘要直接写进 hard memory 后就当作事实使用。
```

### 4. 防御性写作是一个可迁移的 red-team review pattern

防御性写作 agent 的四段式很强：

```text
Attack -> Validity Threat -> Boundary Reframing -> Evidence Anchor
```

然后每个攻击点走三策：

```text
上策：这不是缺陷，这是特点
中策：缺点本身是工程边界分析
下策：rebuttal / 补证据 / 降级 claim
```

放到 VAKS，最值得借的是这个“先模拟反对意见，再校准 claim”的结构，而不是学术写作本身。

VAKS 可改造成：

```text
Candidate Point Red-Team:
- challenge: 这个点可能被哪里攻击
- validity threat: 是证据不足、范围不明、时间过期、定义偷换，还是行动风险
- boundary reframing: 它真正成立的范围是什么
- evidence anchor: 需要回到哪个 raw source span
- claim calibration: 是否降级、缩窄或进入 review_due
```

这和 VAKS 的 Evidence-Aware Review、Known Omission Check、Temporal Applicability Check、Evidence Sufficiency Gate 非常同频。

### 5. Review failure 必须回流，而不是“建议你改改”

仓库的 content-review-agent 写得很硬：如果 spec audit、defensive audit、AI score、证据覆盖失败，就作为严重违规打回写作 agent 强制重写。

VAKS 借鉴点：

```text
在重要 promotion / action basis / review package 中，review failure 不应该只是末尾备注。
它应该改变状态：
- candidate remains candidate
- review_pressure: review_due / blocked
- action_basis_allowed: false
- next_step: revise evidence / narrow claim / collect source / split point
```

这和当前 VAKS 的 candidate_not_action_basis、promotion_gate、review_pressure 是一致的。

### 6. Router 和 Context Compactor 是 dev-context 的轻量工程表层

仓库用 router-agent 选择 prompt slice，用 context-compactor 把长对话压缩成 core argument skeleton、style snapshot、resolved specs。

VAKS 可借：

```text
Context Pack 不一定一开始就是大系统。
可以先有 operator-readable compact pack：
- current question
- source anchors used
- candidate points
- known risks / review_due
- resolved decisions
- open gaps
```

这强化 VAKS 的 `DEV_CONTEXT.md`：Core / Support / Risk / Cold References 不是越多越好，而是要按当前任务动态加载。

### 7. PDF/reference ingestion 与 VAKS source intake 很像，但需要更严格边界

仓库的 PDF reader / reference learning 会抽取摘要、方法、结果、局限、术语、data_points、quotes、style_notes，并规划写入 reference library、hard memory、soft memory。

VAKS 可借：

```text
资料 ingestion 时的 extraction target 很完整：
- facts
- data
- terms
- style
- quotes
- data_points
- quality gaps
```

VAKS 必须加强：

```text
- quote / data point 必须有 source anchor
- summary 不等于 evidence
- hard memory 不能直接接受未审核事实
- PDF parser / MinerU output 是 transformed evidence，需要原始锚点
```

### 8. AI-style detector 只能是 maintenance lint

本地检测脚本会清洗 LaTeX、扫描 AI buzzwords、计算 PPL。这对投稿前自查有用，但对 VAKS 来说风险很高。

VAKS 只能借：

```text
maintenance lint / style hygiene / diagnostic warning
```

不能借：

```text
把 detector score 当 truth、reviewer status、source reliability、evidence support、或 action readiness。
```

这和 VAKS 已有的“test / benchmark / fixture / LLM judge 只是 lint / diagnostic input”完全一致。

## Anti-Omission Extraction

### Pain Point

AI 写作容易出现三个问题：

- 写得快，但不遵守用户真实约束。
- 记忆和参考资料分散，下一次又忘。
- 投稿或审核前才发现 claim、证据、风格、格式、AI 味和审稿攻击面有问题。

### Workflow

```text
user request
-> document_spec
-> outline with DoD / defensive DoD
-> memory + reference recall
-> draft
-> defensive red-team review
-> content review / spec audit / evidence audit / AI-style lint
-> pass -> final draft
-> fail -> rewrite / revise / narrow claim / update memory
```

### Tools / Plugins

- `.traerules` as workspace-level instruction.
- `.agents/workflows` as executable workflow prompts.
- `.ai_context/prompts` as modular agents.
- `hard_memory.json`, `soft_memory.json`, `reference_library.json` as local memory stores.
- `paper_ai_detector.py` as local diagnostic script.
- MinerU / `magic-pdf` examples for PDF parsing.
- Optional GPTZero / external AI detection adapters.

### Information Structure

The repository uses a project-local context folder:

```text
.ai_context/
  custom_specs.md
  document_spec_template.md
  outline_template.md
  style_profile.md
  error_log.md
  memory/
  prompts/
  scripts/
.agents/workflows/
```

This is close to VAKS' file-first philosophy: durable instructions live in files, not hidden chat memory.

### Judgment Mechanism

Judgment is based on:

- spec / DoD compliance,
- evidence coverage,
- defensive audit,
- AI-style lint,
- flow appraisal,
- user correction and memory update.

The strongest mechanism is `failed_specs` and forced rewrite. The weakest mechanism is AI detector / PPL scoring if overtrusted.

### User Experience

Good:

- The operator can point an agent at the repo and get repeatable behavior.
- The user does not have to restate every writing preference each time.
- Review happens before final output, not only after publication.

Bad:

- It can become prompt bureaucracy if every small task requires full spec, memory, red-team, detector, and review.
- Direct memory updates can blur source, preference, and fact authority.

### Automation Boundary

Safe automation:

- route prompt slices,
- compile compact context,
- run lint,
- produce review report,
- propose memory updates.

Risky automation:

- write facts directly into hard memory,
- execute self-healing scripts without safety,
- use detector scores as proof,
- treat a passed workflow as evidence support.

### Fit For VAKS

Strong fit:

- candidate-to-review workflow,
- review failure state transition,
- red-team attack surface,
- claim calibration,
- task contract / DoD,
- file-backed agent operating instructions.

Medium fit:

- router / compactor,
- hard/soft memory split,
- PDF extraction schema,
- style/error lint.

Low / risky fit:

- PPL detector,
- external AI detector APIs,
- auto memory writes,
- self-healing tool loops.

### Challenge To VAKS

This repository challenges VAKS in a useful way:

```text
VAKS has strong epistemic boundaries, but can become too abstract for operators.
AI Vibe Writing Skills shows how much value a simple file-based workflow can create
when every role has a visible prompt, every output has a DoD, and failures route back.
```

So the lesson is not “add more schema”.

The lesson is:

```text
Put the strictness into readable operator surfaces.
```

## VAKS 层级归位

```text
Capture / Provenance:
  - PDF/reference ingestion target list is useful, but VAKS needs stronger source anchors.

Candidate Comprehension:
  - Spec/outline/draft resembles candidate shaping before review.

Knowledge Calibration / Point Collision:
  - Defensive red-team can become candidate attack-surface calibration.

Review / Consolidation:
  - Spec Audit + Defensive Audit + failed_specs -> forced rewrite is the strongest match.

Association / Reviewed Relations:
  - No direct borrowing. The repo does not provide reviewed relation semantics.

Activation / Dev Context:
  - Router and context compactor are strong support references.

Context Pack:
  - Compact_Context can inspire a simple operator-readable context pack.

Decision / Action:
  - No direct action basis. Borrow only after VAKS review gates.

Use Ledger / Feedback:
  - Error log and user correction are useful analogies, but feedback must not mutate truth.
```

## Borrow Order

### P1: 最强借鉴

- `spec_as_task_contract`: before high-impact generation, write a small, user-checkable task contract.
- `dod_as_output_gate`: important outputs should have minimal DoD and machine-filterable boundary fields.
- `defensive_red_team_gate`: review attacker / counterevidence / scope-risk before finalizing important claims.
- `review_failure_forces_rewrite`: failed review changes state and routes work back, instead of appending weak advice.

### P2: 有用但要改造

- `hard_soft_memory_split`: preserve fact / preference / reference / correction separation.
- `reference_ingestion_targets`: extract facts, data, terms, quotes, style, quality gaps, but add VAKS source anchors.
- `router_compactor`: use task-specific loading and compact context, but keep authority buckets separate.

### P3: 可观察 / 备用

- LaTeX self-healing loop for future product/tooling lane.
- Local AI-style lint as maintenance manifest inspiration.
- External detector API list as optional diagnostic adapter catalog.

## Avoid

- Do not make AI-style score, PPL, GPTZero, or any detector an authority layer.
- Do not let hard memory receive unreviewed facts as truth.
- Do not make workflow success a substitute for evidence support.
- Do not copy full prompt-agent stack as VAKS core.
- Do not allow self-healing script generation without explicit safety and execution boundary.
- Do not turn defensive reframing into rhetorical excuse; if evidence is weak, claim must narrow.

## Open Questions

- Should VAKS introduce a small `task_contract` template for high-impact answer/action/review windows?
- Can `Attack -> Validity Threat -> Boundary Reframing -> Evidence Anchor` be used as an optional Evidence Packet review aid?
- Should `failed_specs` become a field in review packages, or stay as operator report language?
- How can VAKS keep this operator-surface simplicity without adding another formal lane?

## Routing Hint

```text
source-intake:
  heavy source, candidate-only

review-queue:
  only if a P1 item is proposed for mainline adoption

dev-context:
  support_with_required_risk for operator workflow / review UI / context-pack work

maintenance-lint:
  detector and style-check parts only
```

## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
```
