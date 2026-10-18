---
type: source
status: source-captured
title: "基于obsidian与GPT5.5的自生长自迭代知识库网络讲解(已开源至github）"
source_id: bilibili-BV1cM7C6BEsM
source_uri: bilibili:BV1cM7C6BEsM
source_url: https://www.bilibili.com/video/BV1cM7C6BEsM/
source_type: video
platform: bilibili
platform_id: BV1cM7C6BEsM
author: "乐创科技"
publisher: "乐创科技"
published_at: "2026-06-05 18:09:43 +08:00"
updated_at:
duration: 1643s
captured_at: "2026-06-07 03:39:17 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-07-bilibili-self-learning-library-source.md
processing_mode: runner
processing_level: medium
processing_tier: medium
review_priority: high
review_owner: Codex
formalization_status: raw-only
access_boundary: public_no_cookies
transcript_method: local_asr
transcript_location: raw/videos/2026-06-07-bilibili-self-learning-library-source/transcript.txt
segments_location: raw/videos/2026-06-07-bilibili-self-learning-library-source/segments.md
transcript_metadata_location: raw/videos/2026-06-07-bilibili-self-learning-library-source/transcript-meta.json
ledger_location: raw/videos/2026-06-07-bilibili-self-learning-library-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - self-learning-library
  - obsidian
  - local-agent
  - ai-memory
  - local-harness
  - selective-rag
  - candidate-only
projects:
  - verified-action-knowledge-system
source_family: self-learning-library
upstream_sources:
  - https://github.com/LLK-LL/Self-Learning-Library
verification_status: source_metadata_confirmed
candidate_relation_suggestions:
  - target: "[[Activation Tier]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The video frames local knowledge as memory retrieved into future agent work, not as truth by default."
  - target: "[[Feedback Ledger]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The main loop records user corrections and repeated mistakes so later work avoids regression."
  - target: "[[Evidence-Aware Review]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The described scoring/conflict/generalization layers resemble review input routing, not automatic truth."
tags:
  - raw-video
  - bilibili
  - self-learning-library
  - local-harness
  - self-growing-knowledge-base
  - ai-memory
  - candidate-only
---

# Bilibili Source Record: Self-Learning Library

## 为什么收录

这个视频是 `LLK-LL/Self-Learning-Library` 的讲解来源。用户要求先看视频讲的逻辑，再看仓库补充，并明确说：

```text
这都是一个知识点，别开两个。
```

所以本卡只作为视频来源证明和 transcript 入口；正式蒸馏在统一知识点文件里完成，不把视频和仓库拆成两个独立候选方向。

## 来源信息

- Platform: Bilibili
- BV: `BV1cM7C6BEsM`
- Title: `基于obsidian与GPT5.5的自生长自迭代知识库网络讲解(已开源至github）`
- Uploader: `乐创科技`
- Published: `2026-06-05 18:09:43 +08:00`
- Duration: `1643s`
- Description: `LLK-LL/Self-Learning-Library`
- Public metadata captured with no cookies.

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

Video source records provide provenance, transcript location, and findability. They do not create reviewed evidence, project borrowing conclusions, or action basis.

## 获取与转写

```yaml
subtitle_status: public subtitle endpoints checked, no public subtitle found
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
compute_type: float16
language: zh
language_probability: 1
segment_count: 709
text_chars: 7158
transcript_quality: medium
media_retention: deleted
scratch_cleanup: media_deleted
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-07-bilibili-self-learning-library-source/transcript.txt
segments_location: raw/videos/2026-06-07-bilibili-self-learning-library-source/segments.md
transcript_metadata_location: raw/videos/2026-06-07-bilibili-self-learning-library-source/transcript-meta.json
ledger_location: raw/videos/2026-06-07-bilibili-self-learning-library-source/acquisition-ledger.json
```

说明：

```text
字幕 / ASR 是 raw source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
视频临时音频已删除，只保留 transcript / segments / metadata / ledger。
```

## 人话摘要

UP 主讲的是一个“自生长知识库”：把本地 Agent 的工作过程、用户纠错、失败经验和反复出现的要求记录下来，再用分层规则和检索流程约束下一次输出。

它的逻辑不是“Obsidian 多建几个文件夹”，而是：

```text
纠错和工作记录
-> 本地记忆
-> 分析/打分
-> 冲突、泛化、受限
-> 输出下一次应该怎样检索和执行
-> 用 harness/workflow 约束 AI 不要乱跑
```

这与 VAKS 的价值点重合：记忆不是直接变真理，而是成为后续任务的候选约束、回归检查和 review input。

## 关键实体置信度

```text
confirmed:
  - Bilibili BV1cM7C6BEsM
  - Uploader: 乐创科技
  - Repository name from video description: LLK-LL/Self-Learning-Library
  - Public audio + local ASR, no cookies, no cloud API

likely:
  - The speaker means "Harness Workflow"; ASR sometimes rendered it as "Harmless".
  - "GPT5.5" appears in the title, but this source card treats it as video title text, not product verification.

unclear:
  - Some tool names in ASR are noisy, such as web model names and local UI names.

needs user visual check:
  - None for the core repository identity; the GitHub repo was checked separately.
```

## 关键时间锚点

- `0036-0064`: 知识库目标是让 AI 有记忆，记录修改过程并迭代总结。
- `0192-0258`: 讨论上下文丢失，提出把记录放到本地电脑形成“本地大脑”。
- `0644-0667`: 本地记忆库记录犯错，让 AI 下次不要再犯同样错误。
- `0680-0912`: 讲输入层、分析/打分层、冲突层、泛化层、受限层、输出层。
- `1015-1085`: 讲 `Project Harness Workflow`，把它理解成约束 AI 的工作流。
- `1210-1230`: 用本地 harness/workflow 约束 AI 幻想和任务执行。
- `1456-1498`: 指向 GitHub 上的 `Self Learning Library` 仓库和 `.md` 工作流文件。

## 可抽取 Candidate Points

- `local-harness-as-ai-memory`
- `correction-to-rule-loop`
- `selective-rag-before-task`
- `evidence-reasoning-output-layering`
- `conflict-limited-generalized-rule-routing`
- `no-regression-guard`
- `workflow-governance-not-content-rule`

## 可借鉴

- 本地 Agent 需要可回钻的记忆层，不应只靠一次聊天上下文。
- 用户纠错、导师意见、失败修复可以形成后续任务的检查项。
- 冲突、受限、泛化要分层，不要把所有记忆揉成一个大 prompt。
- Workflow/harness 是约束机制，不是普通提示词堆砌。

## 不能直接借鉴

- 不要把视频里的“网页端很落后”等观点当事实结论。
- 不要把演示仓库的论文写作内容直接导入 VAKS 主库。
- 不要把 ASR 中的产品名、模型名、版本名当高置信实体。
- 不要把“自学习”理解成自动真值更新或自动晋级 reviewed knowledge。

## VAKS 归位

```text
Capture: public video metadata, transcript, segments, ASR ledger.
Understand: one unified candidate distillation with the repository.
Review: candidate-only; later evidence-aware review only.
Connect: local harness / memory loop / selective retrieval / no-regression guard.
Activation / Context Pack: support layer when designing VAKS harness and memory workbench.
Decision / Action: not action basis.
Use Ledger / Feedback: user corrections can create review pressure, not truth mutation.
```

## 下一步

与 `LLK-LL/Self-Learning-Library` 仓库源卡合并进入一个统一候选蒸馏，不单独开第二个知识点。
