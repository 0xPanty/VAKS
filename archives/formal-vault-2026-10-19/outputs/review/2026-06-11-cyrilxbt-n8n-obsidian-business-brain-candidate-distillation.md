---
record_kind: candidate_distillation
status: draft
provisional: true
title: "CyrilXBT N8N + Obsidian Business Brain：业务自动化脑的候选蒸馏"
created_at: 2026-06-11
created_by: Codex
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: project_sidecar_created
review_pressure: none
derived_from:
  - raw/articles/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-source.md
  - raw/articles/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-source/pasted-text.txt
  - outputs/review/project_lens_overlays/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-overlay.md
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
  - obsidian-workbench
  - automation-surface
  - source-intake
  - decision-review
  - briefing-workflow
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - raw/articles/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-source/pasted-text.txt#The Architecture
  - raw/articles/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-source/pasted-text.txt#The Eight Core Workflows
  - raw/articles/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-source/pasted-text.txt#Connecting the Workflows Into a System
borrow_value: medium
borrow_order:
  - "P1: workflow cadence and shared context file as a future Obsidian workbench reference"
  - "P2: decision logger/reviewer and pattern detector prompts, adapted behind VAKS evidence gates"
  - "P3: N8N implementation details only after official-doc/runtime verification"
avoid:
  - "Do not let N8N or Claude write reviewed knowledge, decisions, truth confidence, or action basis directly."
  - "Do not auto-update a core CLAUDE.md/context file from generated summaries without review."
  - "Do not treat repeated generated summaries as independent evidence."
  - "Do not copy unverified API/model/tool details into implementation docs."
  - "Do not ingest private email, CRM, support, or finance data without explicit authorization and privacy boundaries."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "the active task is building or evaluating Obsidian automation, N8N workflows, daily/weekly review surfaces, or a VAKS operator cockpit"
  support_when: "designing source intake cadence, decision review prompts, context brief generation, or project workbench rhythms"
  risk_when: "someone proposes direct LLM-to-vault writes, auto context-file mutation, full-vault prompting, or generated-output-as-evidence"
  cold_references:
    - raw/articles/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-source.md
    - raw/articles/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-source/pasted-text.txt
tags:
  - candidate
  - provisional
  - source-distillation
  - obsidian
  - n8n
  - automation
  - candidate-only
---

# 候选蒸馏：N8N + Obsidian Business Brain

## 说人话

这篇帖子的核心不是“它证明了什么”，而是给了一个很清楚的使用节奏：

```text
业务里每天产生的东西
-> 自动进 inbox
-> LLM 帮你整理成结构化笔记
-> Obsidian 存长期记忆
-> 每天/每周/每月回看、提醒、提炼模式
```

对 VAKS 有用，但不能照搬。

最该借的是“工作流节奏”和“共享上下文文件”；最该避开的是“让自动化直接把 AI 输出写成永久可信知识”。

## Candidate Point 1: 三层业务脑可以映射到 VAKS，但权威边界不同

原文三层：

```text
Obsidian = permanent memory
N8N = automation nervous system
Claude API = intelligence layer
```

VAKS 可以吸收成：

```text
Markdown / Obsidian = durable surface
automation = capture / routing / notification
LLM = candidate comprehension / briefing / review input
review gate = separate authority layer
```

关键差异：

```text
原文容易把 AI synthesis 写成 business memory。
VAKS 必须把 AI synthesis 先放 candidate / output / overlay。
```

也就是说，自动化可以“帮忙搬运和整理”，但不能直接“裁决真值”。

## Candidate Point 2: `CLAUDE.md` 类中心上下文文件值得借，但只能当 context surface

原文要求每个工作流都读取 Business `CLAUDE.md`，里面放公司身份、战略优先级、项目、theses、竞争格局、已知模式、风险和输出规则。

VAKS 可以借这个形状：

```text
active project context
current priorities
known risks
open decisions
review warnings
output routing rules
```

但在 VAKS 里它不应该成为 truth source。

更安全的形状是：

```text
DEV_CONTEXT / context pack / project cockpit
  reads reviewed + candidate + overlay by authority bucket
  exposes risk and missing anchors
  suggests updates as candidate patch
  requires human / review gate before changing durable core
```

## Candidate Point 3: 八个工作流是很好的 operator cockpit 菜单

原文八个工作流可以压缩成四类：

| Workflow family | 原文例子 | VAKS 候选借法 |
|---|---|---|
| Daily activation | Morning Business Brief | daily context briefing / hot items / review_due reminders |
| Intake processing | Meeting, customer, market, financial intel | source intake processors with raw snapshots and candidate outputs |
| Decision hygiene | Decision logger + reviewer | decision assumption / expected outcome / review_date loop |
| Synthesis cadence | Weekly review + monthly pattern detector | weekly closeout and candidate pattern pressure, not automatic truth |

这对 VAKS 的“Obsidian use surface / cockpit”很有启发：不是再造一个大系统，而是把已有 Capture -> Understand -> Review -> Connect -> Act and Learn 用更好操作的日常节奏呈现出来。

## Candidate Point 4: 决策记录模板很贴近 VAKS

原文 decision note 要求写：

```text
decision
context
alternatives
key assumption
expected outcome
review criteria
risk
review date
```

这和 VAKS 的 decision outcome calibration 很吻合。

可借用：

```text
重大行动前，把 assumption 和 expected outcome 写出来。
到 review date 时，检查实际结果是否支持当初假设。
结果只校准 future recommendation，不直接改 truth。
```

不要借用：

```text
让 Claude 自动决定 review date 并写成正式 decision。
让 Monday reviewer 直接修改旧 decision 的 status。
```

## Candidate Point 5: Pattern detector 的“三个独立输入”是防噪音启发，不是真值规则

原文要求 pattern 至少来自三个不同 intelligence inputs，而不是同一主题重复出现。

这是好启发：

```text
如果 customer notes、meeting notes、financial review 都指向同一结构问题，
那它可以进入 synthesis_needed / review_due。
```

但 VAKS 不能把它变成：

```text
出现三次 = 真的
三个 AI brief 都提到 = 独立证据
```

安全借法：

```text
three independent source classes -> review pressure
review pressure -> candidate synthesis
candidate synthesis -> evidence-aware review if important
```

## Candidate Point 6: 输出互相引用会复利，也会复利式污染

原文说：

```text
weekly review reads daily briefs
monthly pattern detector reads weekly reviews
morning brief references competitive intelligence
```

这会让系统越来越懂业务，但也会带来一个 VAKS 风险：

```text
AI summary A
-> AI summary B reads A
-> AI summary C reads B
-> 原始 source anchor 被越抛越远
```

所以对 VAKS 来说，复利链条必须带：

```text
raw source / snapshot refs
candidate vs reviewed badges
warning codes
missing anchor markers
source-family independence check
```

否则“越来越聪明”可能只是“越来越自信地复述旧摘要”。

## VAKS Mapping

| VAKS layer | Fit | Borrow |
|---|---:|---|
| Capture / Provenance | Medium | Inbox watcher and retained source snapshot idea. |
| Candidate Comprehension | High | Meeting/customer/market/finance processors as candidate outputs. |
| Knowledge Calibration | Medium | Pattern and decision review prompts can create review pressure. |
| Review / Consolidation | Low by default | Original source lacks review gate; VAKS must add one. |
| Association / Connect | Medium | Outputs can reference each other if authority buckets are visible. |
| Activation / Dev Context | High | Morning brief / CLAUDE.md context file maps to activation surface. |
| Context Pack | Medium | Briefings can become context-pack candidates, not support. |
| Decision / Action | Risky | Needs intent confirmation, evidence packet, and action basis gate. |
| Feedback | Medium | Weekly/monthly reviews can route usefulness and stale assumptions. |

## Borrow Gradient

```yaml
borrow_value: medium
borrow_order:
  - P1: shared context file + daily/weekly/monthly workflow cadence
  - P2: decision review and pattern detector prompt shapes
  - P3: N8N/Telegram/Brave/API mechanics after verification
```

## Do Not Borrow

- Do not let N8N/Claude write reviewed knowledge directly.
- Do not auto-update `CLAUDE.md` or any core context file from generated summaries.
- Do not treat generated briefings as independent evidence.
- Do not ingest private business systems without explicit permission and scoped retention rules.
- Do not use “all files in vault” as a prompt strategy without retrieval budget, authority buckets, and source anchors.
- Do not copy API/model configuration from the post without official-doc verification.

## Open Questions

- What is the canonical source URL and publication date for this post?
- Is N8N the right automation surface for VAKS, or should a thinner script/CLI/Obsidian plugin surface come first?
- Which first workflow is most valuable for VAKS: daily brief, weekly closeout, decision reviewer, or intake processor?
- How should a future context file expose reviewed vs candidate vs overlay material mechanically?
- Can workflow outputs preserve source anchors cheaply enough to avoid summary-compounding?

## Current Judgment

```yaml
direct_use: no
fork_or_run: no
design_only: yes
implementation_next: only_if_user_requests_obsidian_or_n8n_workbench_prototype
mainline_change_now: no
reviewed_knowledge_created: false
action_basis_allowed: false
truth_mutation_allowed: false
```
