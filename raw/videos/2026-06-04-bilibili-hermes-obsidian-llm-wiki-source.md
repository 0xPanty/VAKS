---
type: source
status: source-captured
title: "Hermes + Obsidian + LLM Wiki 构建 AI 知识库"
source_title_raw: "Hermes+Obsidian+LLM wkii，构建AI知识库"
source_id: bilibili-BV16hZFB5ERM
source_uri: bilibili:BV16hZFB5ERM
source_url: https://www.bilibili.com/video/BV16hZFB5ERM/
source_type: video
platform: bilibili
platform_id: BV16hZFB5ERM
author: "轻霜铺满城"
publisher: "轻霜铺满城"
published_at: "2026-04-26 19:49:15 +08:00"
updated_at:
duration: 846s
captured_at: "2026-06-04 23:16:42 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source.md
processing_mode: runner-plus-manual-distillation
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public_no_cookies
transcript_method: local_asr
transcript_location: raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - hermes
  - obsidian
  - llm-wiki
  - karpathy-wiki
  - applescript
  - local-knowledge-base
  - wikilinks
  - graph-view
  - agent-workbench
  - activation
  - context-preparation
  - candidate-only
  - video-intake
projects:
  - verified-action-knowledge-system
source_family: bilibili-hermes-obsidian-llm-wiki
upstream_sources:
  - https://hermes-agent.lzw.me/docs/en/user-guide/skills/bundled/research/research-llm-wiki
verification_status: unverified-video-summary
candidate_relation_suggestions:
  - candidate:intent_phrase_gate_for_agent_kb_operations
  - candidate:llm_wiki_as_candidate_compile_not_truth
  - candidate:obsidian_graph_as_navigation_not_reviewed_relation
  - candidate:hermes_as_automation_engine_not_knowledge_authority
  - candidate:applescript_ui_automation_requires_permission_gate
  - candidate:wiki_folder_as_workbench_surface
  - candidate:persistent_wiki_vs_query_time_rag_boundary
  - candidate:source_citation_post_validation_required
tags:
  - raw-video
  - bilibili
  - candidate-only
---

# 视频资料：Hermes + Obsidian + LLM Wiki 构建 AI 知识库

## 为什么收录

这条视频是一个 Hermes + LLM Wiki + Obsidian 的个人知识库工作流演示。它不是 verified knowledge，也不是可直接采纳的 VAKS 架构证据；它的价值在于展示了普通用户怎样把“AI 自动整理文档”和“Obsidian 本地 Markdown 双链浏览”串成一个可用工作台。

对 VAKS 来说，本条最值得保留的是三个点：一是把工具角色分清，Hermes 是自动化执行入口，LLM Wiki 是候选编译和本地 wiki 生成，Obsidian 是浏览和图谱工作台；二是用明确触发词区分“写入知识库”和“结合知识库回答”；三是提醒我们，Obsidian GraphView / wikilinks 适合 activation 和导航，但不能变成 reviewed relation 或 truth support。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV16hZFB5ERM/
- 标题：Hermes+Obsidian+LLM wkii，构建AI知识库
- 作者 / UP 主：轻霜铺满城
- 发布时间：2026-04-26 19:49:15 +08:00
- 视频时长：846 秒
- 收录时间：2026-06-04 23:16:42 +08:00
- 访问边界：public_no_cookies
- 播放 / 收藏 / 点赞等统计：已记录在 `source-metadata.json`，只作来源元数据，不作为价值或可信度证据。

## 获取与转写

```yaml
subtitle_status: public subtitle endpoints checked, empty
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
compute_type: float16
language: zh
segment_count: 93
text_chars: 5151
duration_seconds: 845.392125
elapsed_seconds: 112.75
transcript_quality: medium
media_retention: deleted
cloud_api_used: false
cookies_used: false
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source/acquisition-ledger.json
```

说明：

```text
Bilibili URL = source provenance。
ASR = raw source text，不是 reviewed evidence。
本摘要 = candidate comprehension，不是 truth。
抽取出的观点 = candidate points，不是 reviewed knowledge。
Hermes / LLM Wiki / Obsidian / GraphView / retrieval / context pack 都只能先归入 activation 或 context preparation。
promotion / action basis 只能后续 evidence-aware review。
```

## 人话摘要

视频讲的是一条个人知识库自动化链路：用户把文档交给 Hermes，Hermes 通过 AppleScript 操作 LLM Wiki，把文档导入本地知识库；LLM Wiki 把文档整理成结构化 wiki 页面和双向链接；这些 Markdown wiki 页面再作为一个文件夹放进 Obsidian，用 Obsidian 的双链、全文搜索和 GraphView 浏览。

视频反复强调两个触发词边界：当用户明确说“写入知识库 / 导入知识库 / 把文件放进知识库”时，Hermes 才执行导入；当用户说“结合知识库 / 查一下知识库 / 根据知识库回答”时，Hermes 才检索。日常普通对话不碰知识库，以免污染。

它的核心不是“让知识变真”，而是“让文档从一次性 RAG 变成可积累的本地 wiki 工作台”。这对 VAKS 有启发，但只能落在 Capture、Understand、Activation、Dev Context、Context Pack 或 agent workbench，不进入 truth core。

## 关键实体置信度

```text
confirmed:
  - Bilibili BV: BV16hZFB5ERM。
  - 标题、UP 主、发布时间、时长：来自 Bilibili public view metadata。
  - Hermes、Obsidian、AppleScript、GraphView：标题 / ASR / 视频语境中反复出现。
  - 本次获取没有使用 cookies，没有使用云 API。
  - Hermes 官方文档中存在 bundled research skill: llm-wiki，可用于确认“llm-wiki”不是纯 ASR 幻听。

likely:
  - 视频标题中的 "LLM wkii" 应为 LLM Wiki。
  - ASR 中的 "LLM Vicky / LM Viki / Viki / Vicky" 应为 LLM Wiki。
  - ASR 中的 "Rab / RIK" 应为 RAG。
  - ASR 中的 "MacDom" 应为 Markdown。
  - ASR 中的 "Cloud" 应为 Claude。

unclear:
  - 视频口播中的 GitHub 路径听起来像 "NashU / LM_Vicky"，未核验，不能写成确认 repo。
  - "3500 stars"、"GPL V3"、具体 Releases 下载路径、各模型提供商支持范围，未独立核验。
  - "Vinimax" 可能是 Minimax，但 ASR 不足以确认。

needs user visual check:
  - 如果之后要精确复刻界面、repo、下载步骤、按钮名或版本，需要检查 04:25-05:10 左右的安装画面和 09:55-10:35 左右的界面截图。
```

## 时间轴 / 分段

- 00:00-00:43：提出工作流目标：用 Hermes 串联 LLM Wiki 和 Obsidian，自动整理文档并形成结构化知识网络。
- 00:43-01:34：介绍 Obsidian：本地 Markdown vault、双向链接、GraphView。
- 01:34-03:12：介绍 LLM Wiki：和传统 RAG 的区别是增量构建持久化 wiki，而不是每次查询都从零检索拼接。
- 03:12-05:41：说明 LLM Wiki 的导入、提问、预览和 wiki 文件夹，生成的 Markdown 页面可放进 Obsidian。
- 05:41-06:47：说明 Hermes 的角色：通过 AppleScript 控制 LLM Wiki GUI，需要 macOS 辅助访问权限。
- 06:47-07:20：明确知识库操作边界：只有显式说写入或查询时才操作知识库。
- 07:20-09:30：串联完整流程：Hermes 接指令，LLM Wiki 导入并生成页面，Obsidian 打开 wiki 文件夹浏览。
- 09:30-11:42：展示界面和 Obsidian 双链 / GraphView：中心节点、孤岛节点、全文搜索。
- 11:42-13:15：总结三条规则：写入知识库、结合知识库、Obsidian 随时浏览。
- 13:15-14:05：总结三者分工：Hermes = 自动化执行引擎，LLM Wiki = 本地知识库和增量 wiki 构建，Obsidian = 展示与可视化层。

## 视频里直接说了什么

- Obsidian 是本地 Markdown 双链笔记工具，数据在本地，vault 本质上是一个文件夹。
- LLM Wiki 与传统 RAG 的差别在于，它让 AI 增量构建持久化 wiki，而不是每次提问都从原文档临时检索拼接。
- LLM Wiki 会提取关键实体、概念、关系，生成或更新 wiki 页面，页面之间形成引用和关联。
- 视频称 LLM Wiki 会标注矛盾、知识空白和来源；这些说法在本卡中仍只按视频说法记录，未作为已验证能力。
- LLM Wiki 的 wiki 文件夹是 Markdown 页面，可以直接放进 Obsidian 作为 vault 浏览。
- Hermes 在这套流程中是自动化执行引擎，通过 AppleScript 控制 LLM Wiki 的图形界面。
- macOS 上需要开启辅助访问权限，终端或相关应用才能控制其他应用界面。
- Hermes 只有在用户明确说“写入知识库 / 导入知识库 / 把文件放进知识库”时才导入。
- Hermes 只有在用户明确说“结合知识库 / 查一下知识库 / 根据知识库回答”时才检索。
- 日常普通对话不主动读写知识库，避免无关内容污染知识库。

## 我的理解 / 推断

这条视频的实际结构可以写成：

```text
显式用户意图
-> Hermes 自动化
-> AppleScript 操作 LLM Wiki
-> LLM Wiki 导入文档并生成候选 wiki 页面
-> wiki 文件夹作为 Markdown vault
-> Obsidian 浏览 / 搜索 / 双链 / GraphView
-> 需要回答时再显式触发知识库检索
```

这不是 VAKS 的 truth 机制。它更像一个候选理解和 activation workbench：LLM Wiki 把材料整理成可浏览页面，Obsidian 提供导航和图谱，Hermes 负责把用户指令转成自动化动作。它解决的是“我懒得手动整理知识库 / 不想每次从零搜索”的体验问题，不解决“这条知识是否有证据、是否可行动、是否已审查”的问题。

## 反漏提取检查

```text
pain point:
  手动搭知识库、导入文档、整理链接和每次重新检索都很烦；用户希望 AI 自动把文档变成可积累的本地 wiki，并能在 Obsidian 里浏览。

workflow:
  用户发出写入指令 -> Hermes 识别显式意图 -> AppleScript 控制 LLM Wiki 导入文件 -> LLM Wiki 读取文档、提取实体/概念/关系、生成或更新 wiki 页面 -> wiki 文件夹进入 Obsidian vault -> 用户用双链、搜索、GraphView 浏览 -> 用户发出结合知识库指令 -> Hermes/LLM Wiki 检索并整合回答。

tools / plugins:
  Hermes、AppleScript、LLM Wiki、Obsidian、Markdown、wikilinks、GraphView、OpenAI/Claude/其他 OpenAI-compatible API。具体 repo、版本、star、license 未核验。

information structure:
  视频强调本地 wiki 文件夹、Markdown 页面、双向链接、GraphView 中的中心节点和孤岛节点。它没有 claim / evidence / review queue / decision / use ledger 结构。

judgment mechanism:
  视频的判断机制主要是“AI 是否把文档整理成结构化页面、是否标注来源、是否方便浏览、是否避免日常对话污染”。它没有 evidence-aware review、truth confidence、scope/risk check 或 action readiness。

user experience:
  优点是操作词非常清楚，用户只要说写入或结合知识库；Obsidian 作为浏览层也很直观。缺点是 AppleScript 控 GUI 脆弱，macOS 权限敏感，LLM Wiki 生成页面容易被误认为已审查知识。

automation boundary:
  自动化负责打开应用、导入文件、输入问题、读取预览、生成 wiki 页面。人工仍必须确认导入意图、确认路径/文件、检查 AI 理解、决定是否把候选内容升级 review。普通聊天不能自动触发知识库读写。

risk:
  1. AI 生成的 wiki 页面被误当 truth。
  2. Obsidian GraphView 关系被误当 reviewed relation。
  3. LLM Wiki 说“标注来源”容易被误读为 evidence support，仍需逐点核验。
  4. AppleScript GUI 自动化可能误点、误导入、误读窗口内容。
  5. 一旦写入权限太宽，日常对话和临时输出会污染知识库。

fit for us:
  可借鉴到 VAKS 的 agent access、intent confirmation、Dev Context、Activation、Context Pack 和 workbench 体验。尤其是“写入知识库”和“结合知识库”的触发词，可以作为轻量懒闸门。

challenge to us:
  它提醒我们普通用户很在乎简单体验：一句话导入、一句话检索、Obsidian 直接看。如果 VAKS 入口太重，用户会更喜欢这种简单 workflow。我们的 strict review 应保留在 promotion / action basis，而不是压到普通 capture / query 前台。
```

## 可抽取 Candidate Points

- `intent_phrase_gate_for_agent_kb_operations`：把“写入知识库 / 导入知识库”和“结合知识库 / 查知识库”区分为两类显式意图，可作为 agent 操作知识库的轻量懒闸门候选。
- `agent_write_requires_scope_confirmation`：导入/写入知识库前应确认文件、路径、目标层级和写入边界，尤其当自动化能控制 GUI 时。
- `llm_wiki_pages_are_candidate_comprehension`：LLM Wiki 生成的 wiki 页面应视为 candidate comprehension，不是 reviewed knowledge。
- `obsidian_graph_is_navigation_not_truth`：Obsidian GraphView 和 wikilinks 是导航/activation，不是 reviewed relation，也不是证据支持。
- `source_citation_needs_post_validation`：LLM Wiki 或回答中出现“来源标注”只说明有 provenance 或引用线索，不自动等于 specific point support。
- `persistent_wiki_vs_query_time_rag_boundary`：持久化 wiki 能减少重复整理，但这只是 context preparation，不应变成 truth confidence。
- `applescript_automation_as_agent_workbench_risk`：AppleScript/GUI 自动化可以提升体验，也增加误操作、权限和可审计性风险。
- `human_observation_slot`：LLM Wiki 右侧预览区允许人边看边确认 AI 理解，可转化为 VAKS 中的人工检查槽，而不是自动通过。

## 可借鉴

- 借鉴“显式触发词”作为轻量操作闸门：写入、导入、结合、查一下、根据知识库回答。
- 借鉴三层分工：automation engine、candidate wiki compiler、Obsidian view/workbench。
- 借鉴 wiki 文件夹作为本地 Markdown workbench，便于 Obsidian、VS Code 或其他工具打开。
- 借鉴 GraphView 识别中心节点和孤岛节点，用作 coverage / activation 线索。
- 借鉴“日常普通对话不触碰知识库”的污染防线。
- 借鉴导入后让用户看预览区，作为人工抽查和理解校准。

## 不能直接借鉴

- 不能把 LLM Wiki 的页面生成当成 VAKS promotion。
- 不能把 Obsidian 双链或 GraphView 连线当成 reviewed relation。
- 不能把“标注来源”当成 evidence support，除非后续逐点验证 source span 是否支持具体 point。
- 不能默认 agent 有写入正式 vault 的权限。
- 不能把 AppleScript GUI 自动化当成可靠、可审计的知识操作主路径。
- 不能因为视频宣称“越用越准确”就把持久化 wiki 视为 truth growth。
- 不能把未核验的 repo、star、license、模型支持、产品功能写成确定事实。

## 风险和不确定

- ASR 对专名有明显误听：LLM Wiki 被听成 Vicky/Viki，RAG 被听成 Rab/RIK，Markdown 被听成 MacDom。
- 视频里的 repo 地址、stars、license、provider 支持未核验。
- Hermes 通过 AppleScript 操作 GUI 的具体脚本、错误处理、权限模型和审计日志没有在视频中完整展示。
- LLM Wiki 声称能标注矛盾、知识空白、来源，但本卡没有验证其实现质量。
- Obsidian 图谱很容易给用户“关系已经成立”的错觉，需要 VAKS 明确边界。
- 本条视频有教程/演示性质，不能作为架构采纳证据。

## VAKS 归位

```text
Capture:
  Bilibili URL、public metadata、ASR transcript、timestamp segments、ledger 进入 raw/videos。

Understand:
  本卡的人话摘要、时间轴、工作流和 candidate points 是 candidate comprehension。

Review:
  不产生 reviewed claim。若后续采用 intent phrase gate 或 LLM Wiki/Obsidian workbench，需要 evidence-aware review。

Connect:
  可连接到 agent access、Source Intake、DEV_CONTEXT、Activation Tier、context-pack preparation、Obsidian workbench。

Activation / Context Pack:
  本条最相关层。LLM Wiki、GraphView、wikilinks、retrieval 和 persistent wiki 都只能先作为 activation/context preparation。

Decision / Action:
  不形成行动依据。不改主架构，不改 schema。

Use Ledger / Feedback:
  可启发 agent 操作 ledger：何时写入、何时查询、谁触发、读写了什么路径、是否需要 review_due。
```

## 处理等级

```text
light:
  只保存来源卡、一句话摘要、为什么收录。

medium:
  加完整转写、时间轴、关键实体置信度、candidate points、可借鉴 / 不可借鉴。

heavy:
  只有当视频里的想法会影响架构、决策、行动或 strong relation 时，才进入 REVIEW_QUEUE / outputs/review。
```

当前等级：medium。

升级到 heavy 的条件：

- 准备把“写入知识库 / 结合知识库”正式写成 VAKS agent intent gate。
- 准备采用 Hermes + LLM Wiki + Obsidian 作为 VAKS 的实际 workbench 或 dev-context 入口。
- 后续多个外部样本都指向“persistent wiki / Obsidian workbench / explicit intent gate”是必需方向。
- 需要评估 AppleScript 或 GUI 自动化是否能用于正式写入流程。

## 价值判断

价值：中高，但只作为候选 UX / workbench / agent-access 参考。

它比一般 Obsidian 入门视频更有价值，因为它把三件事讲清了：工具分工、显式 intent gate、日常聊天不污染知识库。它也比泛泛 RAG 视频更贴近 VAKS，因为它强调 persistent wiki 和本地 Markdown workbench。

但它不是强证据资料。它没有验证 LLM Wiki 的抽取质量，没有证明来源标注可作为 evidence support，也没有处理 reviewed relation、truth confidence、temporal applicability、risk 或 action basis。因此当前只保留为 candidate source，不改架构。

## 下一步

本条先进入外部资料候选积累。后续可以和已收录的 Hermes + Obsidian YouTube 视频、Claude Code + Obsidian 本地知识库视频、OpenClaw / Karpathy LLM Wiki 资料一起做 Direction Review，重点比较：

- `context primer / master context` 与 `DEV_CONTEXT.md` 的关系。
- `LLM Wiki persistent pages` 与 VAKS `candidate comprehension / review queue` 的关系。
- `Obsidian GraphView / wikilinks` 与 VAKS `activation / reviewed relation` 的边界。
- `Hermes write/query trigger phrases` 是否值得吸收入 agent access lazy gate。
