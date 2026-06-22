---
type: source
record_kind: source_card
status: source-captured
title: '如何用一套流程搞定读书笔记 ：2 年读书笔记实践分享'
source_id: bilibili-BV1tNLG6pEJJ
source_uri: bilibili:BV1tNLG6pEJJ
source_url: https://www.bilibili.com/video/BV1tNLG6pEJJ/
source_type: video
platform: bilibili
platform_id: BV1tNLG6pEJJ
author: reminds_AI卡片笔记
publisher: reminds_AI卡片笔记
published_at: '2026-05-16 21:14:14 +08:00'
updated_at:
duration: 558s
captured_at: '2026-06-13 23:23:00 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source.md
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: review_due
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
why_saved: capture video/transcript provenance for candidate VAKS source-intake and learning-loop review; not reviewed knowledge
access_boundary: public
transcript_method: local_asr
transcript_location: raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/transcript.txt
segments_location: raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/segments.md
transcript_metadata_location: raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/transcript-meta.json
ledger_location: raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - video-intake
  - bilibili
  - book-note-workflow
  - reading-highlight-inbox
  - own-language-card
  - atomic-knowledge-card
  - index-card
  - active-recall
  - learning-feedback-loop
  - source-intake-reference
  - vaks-reference
projects:
  - verified-action-knowledge-system
source_family: bilibili-reminds-book-note-workflow
upstream_sources:
  - https://reminds-app.com/doc/content/a1e7ddd9-8494-4ef6-ac85-d19fb7c6b955
  - https://forum.reminds-app.com/t/topic/66
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
  - book-note-workflow
  - source-intake-loop
  - active-recall
  - vaks-distill-candidate
---

# 如何用一套流程搞定读书笔记：2 年读书笔记实践分享

## 为什么收录

这条视频讲的不是 Obsidian 插件，而是一套“读书划线 -> 二次加工 -> 卡片化 -> 索引卡 -> 每日回顾”的个人读书笔记流程。它对 VAKS 的价值在于：它把 capture 之后的人侧理解、筛选、重写、连接和回顾讲得很完整，正好可以用来反推我们的 source intake / candidate comprehension / activation / feedback 边界。

本卡只记录来源和候选理解，不创建 reviewed knowledge。视频里的学习方法、心理学解释、工具能力和效果宣称都需要后续验证。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1tNLG6pEJJ/
- 标题：如何用一套流程搞定读书笔记 ：2 年读书笔记实践分享
- 作者 / UP 主：reminds_AI卡片笔记
- 发布时间：2026-05-16 21:14:14 +08:00
- 视频时长：558s
- 访问边界：public, no cookies

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: review_due
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
```

## 获取与转写

```yaml
subtitle_status: no_public_subtitle_found
transcript_method: local_asr
asr_engine: openai-whisper
asr_model: small
asr_device: cuda / fp16
transcript_quality: medium
media_retention: deleted
scratch_cleanup: temporary audio/playurl deleted after final sync verification
project_visible_artifacts: yes
cookies_used: false
cloud_api_used: false
```

ASR 是 raw/source text，不是 reviewed evidence。专名误识别明显：ASR 中多次出现的 `Remix` / `Remanse` 结合 UP 主身份和公开文档，判断为 `reminds`；书名 `人人/认真/安人觉醒` 判断为《认知觉醒》。这些实体仍按 key-entity confidence 管理。

## 人话摘要

作者先对比两种读书笔记：早期在 Notion 里做长文档，主要复制原文划线，回顾压力大，最后“看过就忘”；现在用卡片笔记法，把一本书拆成一张张知识点卡片，每张尽量用自己的话重写，最后再做一张索引卡把整本书串起来。

完整流程是：在微信读书阅读和划线；用 reminds 同步划线和想法到闪念箱；每天早上花约半小时筛选和二次加工；左边看原始划线，右边写新的笔记卡片；用书名标签管理同一本书的卡片；直接引用原文的内容单独打引用标签；读完一本书后，把卡片拖到白板上分类、移动、整理框架；必要时让 AI 给一个框架角度，但最终自己写索引卡；每天回顾约 16 张卡片，用主动回忆和填空式回顾逼迫自己提取知识，并在回顾时继续迭代卡片。

对 VAKS 最有价值的地方不是某个工具，而是这条链路：`capture 只是入口 -> own-language rewrite 才是候选理解 -> index card 是候选综合 -> active recall/rewrite 是反馈和再激活 -> cross-source spark 是关联候选`。

## 关键实体置信度

```text
confirmed:
  - BVID: BV1tNLG6pEJJ
  - 标题: 如何用一套流程搞定读书笔记 ：2 年读书笔记实践分享
  - 作者 / UP 主: reminds_AI卡片笔记
  - 发布时间: 2026-05-16 21:14:14 +08:00
  - 视频主题: 读书笔记流程、微信读书划线同步、卡片笔记、索引卡、每日回顾
  - reminds 官方文档确认: 可绑定微信读书，将划线同步到闪念

likely:
  - ASR 中 "Remix" / "Remanse" 指 reminds。
  - ASR 中 "闪音箱" 指 闪念箱。
  - ASR 中 "索因卡" 指 索引卡。
  - ASR 中 "认/任/安人觉醒" 指《认知觉醒》。
  - ASR 中 "卡拼笔记写作法" 指《卡片笔记写作法》。
  - ASR 中 "为什么学生不喜欢上学" 为书名《为什么学生不喜欢上学》。

unclear:
  - reminds 中具体同步设置、回顾设置、AI 挖空/填空算法和提示词。
  - 视频画面里的具体 UI 文案和标签路径。
  - 作者提到的学习效果和心理学解释尚未独立验证。

needs user visual check:
  - 如果要复刻产品流程或 UI，需要检查视频画面，不能只靠 ASR。
```

## 时间轴 / 分段

- 00:00-00:44：说明要分享 2 年多读书笔记实践；对比旧长文档和新卡片笔记；新方法是一张卡片一个知识点，最后用一张卡片串联整本书。
- 01:22-01:47：旧 Notion 长文档主要摘录原文划线，不是自己的思考；回顾压力大，最后看过就忘。
- 01:47-02:12：引用卡片笔记写作法的思路：长期学习要写下来，真正理解要转成自己的语言。
- 02:14-03:08：阅读和同步：微信读书里划线/写想法，绑定 reminds 后同步到闪念箱，按章节聚合成闪念卡片；划线时先宽进，整理时再筛选。
- 03:10-04:02：每天早上约半小时整理笔记；左侧看同步来的划线，右侧新建空白卡；用自己的话重写，暂时写不出来时先手动敲作者原话，回顾时再加工。
- 04:02-04:25：用书名标签管理笔记；原文摘录与自己转述分开，用引用标签区分。
- 04:25-05:31：读完一本书后建立索引卡；把笔记拖到白板分类、移动、思考框架；卡住时让 AI 给一个框架角度，最后自己写卡片把全书串起来。
- 05:31-06:31：每天回顾并迭代笔记；长文档难回顾，卡片每天 16 张约 15-30 分钟；回顾时继续改写、总结、压缩语言。
- 06:31-07:17：AI 挖空/填空式回顾带来主动回忆；看过不等于记得，吃力提取反而帮助记牢。
- 07:17-07:52：回顾过程中会发生跨书联想，例如把《认知觉醒》里的思考力和《为什么学生不喜欢上学》里的事实性知识联系起来。
- 07:52-09:17：作者强调每天拆小做，2 年多积累几千张卡片、百万字；学习像长期扎根，短期慢，长期会有突破。

## 反漏提取检查

```text
pain point:
  - 原文划线和长文档会制造“我已经学了”的错觉，但没有自己的思考、难回顾、难调用。

workflow:
  - 微信读书阅读/划线 -> reminds 闪念箱同步 -> 每天早上筛选 -> own-language card -> 书名/引用标签 -> 白板聚类 -> 索引卡 -> 每日主动回忆 -> 回顾中迭代。

tools / platforms:
  - 微信读书, reminds, Notion, AI 辅助框架生成, AI 挖空/填空回顾。

information structure:
  - 原始划线是 inbox/source-like material；重写卡片是 candidate comprehension；书名标签是来源/主题聚类；引用标签区分 verbatim quote；索引卡是 synthesis/context card。

judgment mechanism:
  - 能否用自己的话写清楚，用于检验理解；每日回顾和填空错误暴露“看过不等于记得”；跨书联想暴露关联生成。

user experience:
  - 阅读时低摩擦先捕获；整理时每天固定小块时间；白板移动卡片帮助看结构；回顾时通过主动回忆逼迫知识提取。

automation boundary:
  - 自动同步、AI 框架、AI 挖空都只能辅助 capture/comprehension/activation；不能自动变成 truth、reviewed relation 或 action basis。

risk:
  - 工具闭源/平台绑定；ASR 专名不稳；AI 框架可能过度塑形；引用和转述如果不保留 source anchor，会污染证据边界；记得熟不代表内容可靠。

fit for us:
  - 很适合作为 VAKS 的 reading/source intake 参考，尤其是候选点原子化、原文/转述分离、索引卡、回顾反馈、跨源关联候选。

challenge to us:
  - VAKS 已经有 Capture/Review/Activation/Feedback，但日常读书资料的“人侧加工流程”还可以更明确：什么时候宽进，什么时候筛选，什么时候转成 candidate point，什么时候只做 recall/activation。
```

## 可抽取 Candidate Points

- Candidate Point 1: `highlight/inbox` 不是知识，只是 source-like raw capture；VAKS 应保留原始划线和来源锚点。
- Candidate Point 2: `own-language rewrite` 适合作为 candidate comprehension，但不能替代 evidence support。
- Candidate Point 3: `one card one knowledge point` 可映射到 VAKS candidate point 的原子化要求。
- Candidate Point 4: `quote tag` 和 `paraphrase card` 的分离值得吸收：原文引用、用户转述、模型总结必须分层。
- Candidate Point 5: `book index card` 可作为候选 context pack / synthesis card，而不是 reviewed relation。
- Candidate Point 6: `AI-generated framework` 只能作为候选视角，不能自动创建正式分类、关系或决策。
- Candidate Point 7: `daily active recall / cloze review` 属于 Activation + Use Ledger / Feedback，不改变 truth confidence。
- Candidate Point 8: `review-time rewrite` 是反馈闭环：忘记、写不顺、填错、发现歧义，都可以产生 review_due 或 candidate revision。
- Candidate Point 9: `cross-book spark` 是 Association candidate，必须经过 evidence-aware review 才能成为 reviewed relation。

## VAKS 归位

```text
Capture / Provenance:
  微信读书划线、闪念箱同步、原文摘录、source card、transcript、ledger。

Candidate Comprehension:
  用自己的话重写成卡片；一张卡片一个知识点；暂时写不出时保留原文并标记未加工。

Knowledge Calibration / Point Collision:
  回顾时发现自己写不清、填不出、跨书观点冲突或互补，进入 review_due / collision candidate。

Review / Consolidation:
  只有带 source anchor、evidence item、warrant、scope/risk 的点才可进入 evidence-aware review。

Association / Reviewed Relations:
  白板聚类和索引卡是候选关联；跨书联想是候选关系，不是 reviewed relation。

Activation / Dev Context:
  每日回顾、16 张卡片、主动回忆，是人侧 activation/reactivation queue。

Context Pack:
  一本书的索引卡像一个轻量 context pack，但它只能做理解入口，不能当证据包。

Decision / Action:
  这条视频不产生行动依据；若方法要落到 VAKS 流程，需要另行 review。

Use Ledger / Feedback:
  填错、忘记、改写、压缩、补充、跨源联想，都可成为反馈事件或 review pressure。

Cooling / Reactivation:
  间隔回顾/每日回顾给 VAKS 的 reactivation 设计提供人侧参考。
```
