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
  - raw/repos/2026-06-07-juliye2025-evil-read-arxiv-source.md
  - raw/repos/_snapshots/juliye2025-evil-read-arxiv-31bca2e56bfc2439e2d93384a238bd20502c2a77.zip
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
  - paper-scouting
  - review-queue
  - dev-context
  - feedback-ledger
  - source-artifact-extraction
possible_project_refs:
  - VAKS
point_anchor_refs:
  - source: raw/repos/2026-06-07-juliye2025-evil-read-arxiv-source.md
    snapshot_ref: raw/repos/_snapshots/juliye2025-evil-read-arxiv-31bca2e56bfc2439e2d93384a238bd20502c2a77.zip
borrow_value: very_strong
borrow_order:
  - "P1: Research Scout lane: interest config -> arXiv/S2/DBLP search -> candidate ranking -> source queue."
  - "P1: Workbench loop: cache, paper card, image extraction, focus search, feedback, preference update as candidate-only learning."
  - "P1: Freshness + influence split: recent arXiv plus older/high-impact Semantic Scholar plus top-conference DBLP."
  - "P2: Auto-link and favorites as activation aids, not reviewed relations."
  - "P3: Direct vault note writing, graph updates, shell bridges, and old PubMed/arXiv hunter require hardening before reuse."
avoid:
  - "Do not treat recommendation score, citation count, LLM semantic rank, or user likes as truth confidence."
  - "Do not let LLM summaries or title/abstract analysis become reviewed knowledge."
  - "Do not let automatic domain/keyword updates mutate VAKS main config without a candidate patch and review gate."
  - "Do not write source candidates directly into reviewed notes or reviewed relations."
  - "Do not import shell exec bridges without command-injection and path-safety hardening."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS paper-scouting, source discovery queues, future research intake workbench, or candidate-only feedback learning."
  support_when: "Comparing source search, candidate ranking, image/source artifact extraction, or paper-workbench UI."
  risk_when: "Any proposal tries to make automatic source finding equal automatic learning, promotion, truth, or action readiness."
  cold_references:
    - raw/repos/2026-06-07-juliye2025-evil-read-arxiv-source.md
    - raw/repos/_snapshots/juliye2025-evil-read-arxiv-31bca2e56bfc2439e2d93384a238bd20502c2a77.zip
tags:
  - candidate
  - provisional
  - repo-distillation
  - paper-scouting
  - source-intake
  - feedback-learning
---

# Candidate Distillation: evil-read-arxiv as a Research Scout and Paper Intake Workbench

## Boundary

This is one combined candidate knowledge point for `juliye2025/evil-read-arxiv`.

It can route attention, compare ideas, or support a VAKS Project Overlay. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 人话总结

这个库最强的地方不是“会搜 arXiv”，而是它把“找论文”做成了一个完整的研究摄入流水线：

```text
研究兴趣配置
-> 搜新论文 / 搜高影响论文 / 搜顶会论文
-> 去重、过滤、评分、排序
-> 生成每日推荐或年度顶会推荐
-> 对重点论文提图、做轻分析、生成笔记
-> 前端里刷论文、收藏、反馈
-> 反馈再反过来调整未来的搜索关键词和权重
```

它和 VAKS 很像的地方是：它不是等用户手动塞资料，而是主动把外部资料池变成候选队列，再用本地文件和反馈让系统越来越贴近用户兴趣。

但最关键的边界也必须说清楚：

```text
evil-read-arxiv 可以帮我们找资料。
它不能替我们判断资料是真的、够证据、可行动。
```

所以它对 VAKS 是 P1 级借鉴，但借的是 `Research Scout / Source Discovery`，不是自动真理层。

## Source

```yaml
derived_from:
  - raw/repos/2026-06-07-juliye2025-evil-read-arxiv-source.md
checked_commit: 31bca2e56bfc2439e2d93384a238bd20502c2a77
snapshot_ref: raw/repos/_snapshots/juliye2025-evil-read-arxiv-31bca2e56bfc2439e2d93384a238bd20502c2a77.zip
key_anchors:
  - README.md:24
  - README.md:56
  - README.md:63
  - README.md:351
  - README.md:426
  - start-my-day/scripts/search_arxiv.py:937
  - conf-papers/scripts/search_conf_papers.py:621
  - web/src/app/api/papers/route.ts:174
  - web/src/app/api/preferences/update/route.ts:12
```

## Candidate Points

### 1. 研究兴趣配置是“找资料的种子”，不是知识 schema

`config.example.yaml` 用 `research_domains` 保存领域、关键词、arXiv 分类和 priority。这个配置被 `start-my-day/scripts/search_arxiv.py` 读取后，直接变成搜索范围、匹配关键词、分类加分和排除规则。

VAKS 借鉴点：

```text
未来可以有一个 Research Scout Config：
- 当前关注主题
- 必搜来源类型
- 关键词和排除词
- 时间窗口
- 新论文 / 高影响论文 / 顶会论文比例
- 每日候选上限
```

但这个 config 只能产生 source candidate。它不是概念体系，不是 reviewed schema，不应该直接写入 `wiki/concepts`、`wiki/patterns` 或 reviewed relations。

### 2. 它的 source discovery 是多入口，不是单一搜索框

仓库里至少有四条找资料路径：

```text
daily arXiv:
  最近 N 天内按分类 / focus keyword 搜索新论文

Semantic Scholar hot papers:
  搜过去一年高影响论文，用 influentialCitationCount / citationCount 辅助排序

conf-papers:
  DBLP 拉指定年份顶会论文，再用 S2 补摘要、引用和 arXiv ID

paper_hunter:
  旧式 arXiv / PubMed hunter，直接写入 vault
```

VAKS 最该借前面三条：

```text
newness lane:
  找最新候选，避免资料库老化

influence lane:
  找已经被引用/关注的候选，避免只看新东西

venue lane:
  找顶会/会议候选，避免只靠关键词碰运气
```

`paper_hunter.py` 这种直接写 vault 的路径要谨慎。它适合作为早期思路，但对 VAKS 太容易越过 source card 和 review queue。

### 3. 评分系统有用，但只能当候选排序

`start-my-day` 的推荐分数由四个维度构成：

```text
relevance: 关键词、摘要、分类匹配
recency: 30 / 90 / 180 天窗口
popularity: 引用数或新论文潜在热度
quality: 摘要里的创新词、方法词、实验词、量化结果词
```

`conf-papers` 去掉新近性，改成：

```text
relevance 40%
popularity 40%
quality 20%
```

这个设计的价值是排序成本低、可解释、能快速缩小候选集。

VAKS 必须加的边界：

```text
recommendation_score != support
recommendation_score != truth_confidence
recommendation_score != review_status
recommendation_score != action_basis
```

更适合的字段名不是 `quality_score`，而是：

```yaml
candidate_priority:
  relevance_signal:
  freshness_signal:
  influence_signal:
  extraction_quality_signal:
  why_ranked:
```

### 4. 它有一个非常实用的“近期新源 + 旧高影响源”组合

普通每日搜索不是只搜最近论文。它先搜最近 N 天 arXiv，再补过去一年 Semantic Scholar 高影响论文，最后合并去重。

这对 VAKS 很值得借：

```text
每天只看新论文，会被噪声牵着走。
只看高引用论文，会错过新变化。
两条腿走路，才适合资料库持续更新。
```

VAKS 未来自动找资料可以默认拆成：

```yaml
fresh_candidates:
  source: arXiv / blog / repo / release
  window: recent
  purpose: catch emerging signals

anchor_candidates:
  source: S2 / citations / known repos / standards
  window: older_or_influential
  purpose: provide grounding and comparison
```

### 5. 顶会模块的两阶段过滤很适合节省 API 和注意力

`conf-papers` 先用 DBLP 把会议论文全拉下来，再只按标题做轻量关键词过滤。通过过滤后，才调用 Semantic Scholar 补摘要、引用、arXiv ID。

这个结构很聪明：

```text
先用便宜信号扩大覆盖。
再对候选做昂贵补充。
最后才排序。
```

VAKS 可以把它泛化成：

```text
wide crawl
-> cheap lexical / metadata filter
-> enrichment only for survivors
-> candidate card
-> human or model-assisted triage
-> later review
```

注意：轻量标题过滤会漏掉标题不显式命中关键词但内容相关的论文，所以它适合做 scout，不适合做 completeness audit。

### 6. 笔记生成和图谱更新是“输出模板”，不是知识校准

`paper-analyze/scripts/generate_note.py` 生成的是双语论文笔记模板：核心信息、研究问题、方法、实验、局限、相关论文、综合评价等。

`paper-analyze/scripts/update_graph.py` 会往 `PaperGraph/graph_data.json` 添加节点和 related 边。

VAKS 借鉴点：

```text
把候选论文的 intake 输出做成稳定模板，能降低阅读启动成本。
```

VAKS 不该直接借：

```text
自动 related edge。
自动 quality_score。
自动 analyzed status。
```

原因很简单：VAKS 的 reviewed relation 必须来自证据和 review，不是来自“这两篇论文看起来相关”。

### 7. 图片提取是 P1 级 source artifact 增强器

`extract-paper-images` 的逻辑非常值得吃：

```text
优先从 arXiv e-print 源码包提取真实图片
-> 如果源码图片少，再从 PDF 直接提取
-> 如果源码里有 PDF figure，再转成图片
-> 生成 index
```

它还在 tar 解压时过滤绝对路径、`..` 和符号链接，避免路径穿越。

VAKS 借鉴点：

```text
重要论文 source card 可以保留 visual artifacts：
- figure list
- source package extraction ledger
- image hash
- extraction method
- figure-to-section anchor when possible
```

这对论文理解很有价值，尤其是系统架构图、实验图、流程图。但图片仍然只是 source artifact，不是 reviewed claim。

### 8. 现有笔记扫描和自动链接像 VAKS 的 Activation，但比 VAKS 松

`scan_existing_notes.py` 扫描已有 Markdown 笔记，提取 frontmatter title、文件名和标题关键词，构建 keyword -> note path 索引。

`link_keywords.py` 会跳过 frontmatter、代码块、已有 wikilink、图片、普通链接和标题行，再把正文关键词替换成 wikilink。它还会跳过匹配到多个笔记的关键词，避免泛词乱连。

VAKS 借鉴点：

```text
source candidate 进入资料库时，可以自动提示可能相关的旧 notes。
```

VAKS 边界：

```text
auto link == activation hint
auto link != reviewed relation
auto link != evidence support
auto link != concept merge
```

### 9. Web workbench 是它从脚本升级成系统的关键

Web 端把 Python 搜索脚本接进 Next.js：

```text
/api/papers:
  搜索、缓存、AI 摘要、focus 搜索、自动新增研究域候选

/api/papers/filter:
  对已有缓存结果做 LLM 语义重排

/api/papers/[id]/analyze:
  对单篇论文做四段轻分析

/api/papers/[id]/images:
  提取并缓存图片

/api/feedback:
  like / neutral / dislike

/api/preferences/update:
  反馈积累后让 LLM 生成偏好更新
```

UI 上，`PaperCard` 把论文变成可以翻、可以看图、可以深挖、可以反馈的卡片。这比“生成一个长列表”强很多，因为它把 source triage 变成了人能每天使用的界面。

VAKS 最值得借：

```text
研究候选不是直接进知识库，而是先进入 triage workbench。
用户刷过、点过、收藏过、讨厌过，才变成下一轮搜索配置的候选信号。
```

### 10. 反馈学习很强，也最危险

仓库的反馈链路：

```text
用户对论文 like / neutral / dislike
-> feedback.json
-> 满 10 条后触发 preference update
-> LLM 读反馈、当前 config、当前 preference weights
-> 生成 keyword_weights / domain_weights / category_weights / priority_changes / added_keywords
-> 写回 preferences.json 和 config.yaml
```

这对 VAKS 是 P1，但要换一种权力结构：

```text
反馈可以改变检索偏好。
反馈可以改变候选排序。
反馈可以触发 review_due。
反馈不能改变 truth confidence。
反馈不能自动推广知识点。
反馈不能自动创建 reviewed relation。
```

VAKS 应改成：

```yaml
feedback_scouting_patch:
  proposed_by: model
  based_on: feedback_event_ids
  suggested_keyword_additions: []
  suggested_exclusions: []
  suggested_domain_priority_changes: []
  human_review_required: true
  applied_to_truth_layer: false
```

### 11. Focus search 是很好的“临时研究意图”入口

Web 的 focus 搜索会把用户今天关心的方向翻译成英文关键词，再传给 Python 脚本 `--focus`。脚本会把 focus 匹配作为主导评分，已有兴趣域只做参考加分。

这对 VAKS 很贴：

```text
长期兴趣是 warm context。
今天的问题是 hot intent。
搜索应该先满足 hot intent，再参考长期兴趣。
```

VAKS 可以用：

```yaml
research_scout_run:
  durable_interests:
  session_focus:
  focus_window:
  focus_overrides_default: true
  fallback_to_durable_interests: true
```

### 12. 它的轻分析只基于标题/摘要，不能当论文吃透

Web 的 summary 和 analyze prompts 都主要基于标题和摘要。`analyze` 返回四个字段：contribution、innovation、method、results。

这适合 UI 预览，不适合 VAKS heavy intake。

VAKS 对应规则：

```text
title/abstract analysis = skim summary
full text / figures / methods / experiments = medium or heavy intake
reviewed claim = evidence-aware review only
```

## Proposed VAKS Adaptation

### 最小可借架构

```text
Research Scout Config
-> Scout Run
-> Candidate Source Queue
-> Candidate Source Card
-> Triage Workbench
-> Feedback Ledger
-> Search Config Patch Candidate
-> Human review / apply to scouting only
```

### 对应 VAKS 内部边界

| evil-read-arxiv object | VAKS adaptation | Must not become |
|---|---|---|
| `research_domains` config | scout config / source discovery config | concept schema |
| arXiv / S2 / DBLP result | source candidate | reviewed source support |
| recommendation score | candidate priority signal | truth confidence |
| LLM summary | skim orientation | reviewed comprehension |
| generated note | candidate note scaffold | reviewed knowledge |
| graph edge | possible association hint | reviewed relation |
| feedback rating | usefulness signal | evidence or truth update |
| auto domain update | config patch candidate | automatic mainline mutation |
| image extraction | source artifact | claim support by itself |
| favorites folder | human interest signal | review verdict |

## P1 / P2 / P3

### P1: 必借

1. `Research Scout lane`
   - interest config,
   - focus query,
   - recent source search,
   - high-impact source search,
   - conference source search,
   - candidate ranking,
   - source queue.

2. `候选 workbench`
   - paper cards,
   - images,
   - one-click source link,
   - feedback,
   - favorites,
   - cached runs.

3. `fresh + anchor 双通道`
   - 新论文找趋势，
   - 高影响论文找锚点，
   - 顶会论文找高密度候选。

4. `feedback as scouting pressure`
   - 反馈改检索和排序，
   - 不改真理。

5. `source artifact extraction`
   - 特别是 arXiv source figure extraction。

### P2: 可借，但要改

1. 自动关键词链接：改成 activation hint。
2. LLM semantic filter：改成 candidate re-ranking，并记录 prompt/output。
3. 自动新增研究方向：改成 config patch candidate。
4. 论文图谱：改成 possible association / activation graph，不生成 reviewed relation。
5. `paper-analyze` 模板：保留结构，增加 source anchor、known gaps、claim/evidence separation。

### P3: 只当参考

1. `paper_hunter.py` 的直接写 vault。
2. `generate_note.py` 的 analyzed status 和 quality_score。
3. shell exec bridge 的实现方式。
4. Web app 当前的 API key / data 文件管理方式。

## Avoid / Negative Knowledge

### 1. 自动找资料不等于自动学习

VAKS 未来可以自动找资料，但自动找来的东西只能是候选。

```text
auto scout -> source candidate
source candidate -> source card
source card -> candidate distillation
candidate distillation -> review queue
review queue -> reviewed knowledge only after gate
```

### 2. 引用数不是证据强度

Semantic Scholar 的引用数适合“可能值得看”，不适合“这个 claim 更可信”。

### 3. 摘要里的创新词不是质量

`state-of-the-art`、`novel`、`framework`、`benchmark` 等词只能做弱信号。很多摘要会营销自己，很多重要论文反而写得朴素。

### 4. LLM 偏好更新不能直接改主配置

仓库会把 LLM 生成的 added_keywords 和 priority_changes 写回配置。VAKS 应改成待审 patch。

### 5. Shell bridge 要安全重写

Web API 用 `exec` 拼命令调用 Python 脚本。`focus`、`arxivId` 等用户输入如果没有严格参数化，未来接入 VAKS 前必须做 command injection、路径、超时和资源隔离检查。

### 6. 直接写 Obsidian 笔记要过 source card

旧 `paper_hunter.py` 会直接保存论文笔记和 PDF。VAKS 不应复制这种直写方式。必须先有 raw source card / artifact ledger。

## One-Line Decision Candidate

```text
值得 P1：把它作为 VAKS 未来 Research Scout / 自动找资料候选队列的参考架构；不值得把它当自动知识入库或自动真理系统。
```

## Review Queue Suggestions

```yaml
review_due:
  - candidate_id: research-scout-lane
    question: "Should VAKS add a candidate-only Research Scout lane for arXiv/S2/DBLP/repo/article discovery?"
    required_checks:
      - source card boundary
      - candidate queue storage
      - feedback ledger quarantine
      - search config patch review
      - no truth mutation
  - candidate_id: paper-artifact-extraction
    question: "Should VAKS use arXiv source package figure extraction for medium/heavy paper intake?"
    required_checks:
      - artifact hash
      - source package ledger
      - figure source path
      - no claim support without review
  - candidate_id: triage-workbench
    question: "Should VAKS build a small source triage workbench before reviewed intake?"
    required_checks:
      - candidate labels
      - user feedback as usefulness only
      - promotion gate visibility
```
