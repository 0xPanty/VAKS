---
type: library_review
status: candidate
library_name: evil-read-arxiv
repo_url: https://github.com/juliye2025/evil-read-arxiv
source_url: https://github.com/juliye2025/evil-read-arxiv
checked_commit: 31bca2e56bfc2439e2d93384a238bd20502c2a77
commit_time: 2026-06-01T20:30:17+08:00
source_status: active
reviewed_at: 2026-06-07
domain: academic-paper-scouting-workbench
related_projects:
  - verified-action-knowledge-system
current_branch: source-intake-research-scouting
extracted_patterns:
  - research-scout-config
  - recent-plus-influential-source-discovery
  - conference-paper-scouting
  - heuristic-candidate-ranking
  - paper-triage-workbench
  - feedback-driven-search-preference
  - source-artifact-figure-extraction
fusion_decision: adapt
confidence: medium
evidence_count: 42
cross_validated_with:
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
  - REVIEW_QUEUE.md
  - FEEDBACK.md
  - MEMORY_TIER.md
negative_evidence:
  - scoring and citation counts are heuristic only
  - title/abstract LLM analysis is not full-paper review
  - auto-updating config must be quarantined
  - shell exec bridges need hardening
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

# 库分析：evil-read-arxiv

## 它解决什么问题

`evil-read-arxiv` 解决的是研究者持续找论文、筛论文、看论文、沉淀笔记的问题。

它不是一个严格的知识库系统，而是一个论文摄入工作台：

```text
外部论文源
-> 候选发现
-> 低成本过滤
-> 启发式排序
-> UI / 笔记 / 图像 / 轻分析
-> 用户反馈
-> 搜索偏好调整
```

对 VAKS 来说，它的价值不是 reviewed knowledge，而是未来自动找资料的候选入口。

## 核心设计

它可以压成八层：

1. **Interest Config Layer**：`config.yaml` / `research_interests.yaml` 定义领域、关键词、arXiv 分类、排除词、priority、语言、vault path。
2. **Source Discovery Layer**：arXiv 搜最近论文，S2 搜过去一年高影响论文，DBLP 搜顶会论文，PubMed 作为旧 hunter 补充。
3. **Enrichment Layer**：S2 补摘要、引用、外部 ID、arXiv ID、作者机构。
4. **Heuristic Ranking Layer**：相关性、新近性、热门度、摘要质量词，做候选排序。
5. **Output / Note Layer**：每日推荐、顶会推荐、论文分析模板、PaperGraph JSON。
6. **Artifact Layer**：arXiv 源码包和 PDF 图像抽取，生成图片目录和索引。
7. **Workbench Layer**：Next.js 前端卡片、焦点搜索、语义重排、深挖、图片、收藏、设置。
8. **Feedback Learning Layer**：like / neutral / dislike 累积后，让 LLM 建议关键词、权重和优先级变化。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:24` | Daily recommendations search recent arXiv and S2 hot papers | Two-speed discovery: fresh + influential | Documentation |
| `README.md:56` | Top-conference recommendation via DBLP + S2 | Conference/venue-based discovery path | Documentation |
| `README.md:63` | Web app with AI summary, deep analysis, focus search, feedback, favorites | Workbench, not just script | Documentation |
| `README.md:351` | Relevance/recency/popularity/quality scoring | Candidate priority model | Heuristic |
| `README.md:426` | Load config -> scan notes -> search -> merge -> score -> note -> analyze -> link | Full loop | Documentation |
| `config.example.yaml:24` | Domain keywords, arXiv categories, priority | Search config as user intent | Candidate config |
| `start-my-day/scripts/search_arxiv.py:168` | Date-range arXiv search | Recent source discovery | API-dependent |
| `start-my-day/scripts/search_arxiv.py:229` | Focus keyword arXiv search | Session intent search | Keyword-dependent |
| `start-my-day/scripts/search_arxiv.py:301` | S2 hot paper search | Influence-oriented discovery | Citation is not truth |
| `start-my-day/scripts/search_arxiv.py:432` | Build S2 queries from configured domain keywords | Query fan-out from config | Heuristic |
| `start-my-day/scripts/search_arxiv.py:619` | Relevance scoring with focus override | Today's intent beats long-term domain | Good for hot context |
| `start-my-day/scripts/search_arxiv.py:732` | Quality from abstract indicators | Weak quality proxy | Do not treat as review |
| `start-my-day/scripts/search_arxiv.py:830` | Filter, score, append matched domain/keywords | Candidate ranking output | Candidate only |
| `start-my-day/scripts/search_arxiv.py:1124` | Merge, dedupe by arXiv ID / normalized title | Basic source hygiene | Not canonical identity |
| `start-my-day/scripts/scan_existing_notes.py:154` | Keyword-to-note index | Existing-note activation | Not reviewed relation |
| `start-my-day/scripts/link_keywords.py:118` | Safe-ish wikilink insertion | Association surface | Lexical only |
| `paper-analyze/scripts/generate_note.py:29` | Bilingual comprehensive note template | Structured note scaffold | Placeholder, not analysis |
| `paper-analyze/scripts/update_graph.py:74` | Adds paper node and related edges | Lightweight graph | Not reviewed relation |
| `extract-paper-images/scripts/extract_images.py:33` | Download arXiv source package | Source artifact acquisition | Needs ledger if adopted |
| `extract-paper-images/scripts/extract_images.py:58` | Filters unsafe tar members before extract | Useful tool-safety practice | Partial protection |
| `extract-paper-images/scripts/extract_images.py:119` | PDF image fallback with size filters | Artifact fallback | Visual only |
| `conf-papers/scripts/search_conf_papers.py:63` | Venue map for CVPR/ICCV/ECCV/ICLR/AAAI/NeurIPS/ICML/MICCAI/ACL/EMNLP | Venue-configured scouting | Extensible |
| `conf-papers/scripts/search_conf_papers.py:114` | DBLP conference search | Broad venue pull | API-dependent |
| `conf-papers/scripts/search_conf_papers.py:311` | Title keyword lightweight filter | Cheap first gate | Can miss relevant papers |
| `conf-papers/scripts/search_conf_papers.py:384` | S2 enrichment with title similarity threshold | Metadata/citation enrichment | Match heuristic |
| `conf-papers/scripts/search_conf_papers.py:540` | Conference scoring | Rank after enrichment | Heuristic |
| `conf-papers/scripts/search_conf_papers.py:621` | Main DBLP -> filter -> S2 -> score pipeline | Full conference route | Candidate only |
| `paper-search/scripts/paper_hunter.py:71` | Saves paper and PDF directly to vault | Legacy direct-ingest path | Risky for VAKS |
| `web/src/lib/python-bridge.ts:64` | `searchPapers` calls Python with CLI args | Web/Python bridge | `exec` hardening needed |
| `web/src/lib/data.ts:42` | JSON feedback/preference/cache stores | Local workbench memory | Not knowledge truth |
| `web/src/app/api/papers/route.ts:17` | Batch AI summaries | Skim layer | Title/abstract summary |
| `web/src/app/api/papers/route.ts:85` | Maybe add research domain from focus search | Self-updating scout config | Must become patch candidate |
| `web/src/app/api/papers/route.ts:174` | GET route orchestrates cache/search/summarize/feedback | Main workbench pipeline | Candidate discovery |
| `web/src/app/api/papers/filter/route.ts:7` | LLM semantic re-rank | Focused triage | LLM score only |
| `web/src/app/api/preferences/update/route.ts:12` | LLM analyzes feedback and writes preference/config changes | Learning loop | Quarantine required |
| `web/src/app/api/papers/[id]/analyze/route.ts:7` | On-demand four-field analysis | Quick paper preview | Not full intake |
| `web/src/app/api/papers/[id]/images/route.ts:18` | Runs image extraction from web route | Artifact-on-demand | Shell exec risk |

## 当前支线价值

当前支线：

```text
source-intake / research-scouting / feedback-ledger / dev-context
```

它对当前支线：

```text
refines strongly
```

具体价值：

- 给 VAKS 一个可落地的未来 `Research Scout` 参考：不是一条搜索命令，而是持续候选发现。
- 给 source intake 一个候选队列前置层：先找资料，再决定哪些进入 source card / distillation。
- 给 feedback ledger 一个实用闭环：用户反馈影响未来候选排序，但不影响真理。
- 给 dev-context 一个 UI 直觉：把候选资料做成卡片和过滤器，而不是让模型一次性读一堆列表。
- 给 paper intake 一个 artifact idea：提取 arXiv 源码图和 PDF 图，帮助理解论文结构。

风险：

- 它的 score 很容易被误读成质量或可信度。
- 它的 LLM analysis 主要基于标题/摘要。
- 它的 auto-update config 太激进。
- 它的 web shell bridge 需要安全重写。
- 它的 graph update 不符合 VAKS reviewed relation 边界。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Capture / Provenance | arXiv/S2/DBLP/PubMed discovery and metadata capture | adapt as candidate source discovery |
| Candidate Comprehension | LLM summaries and four-field analysis | adapt only as skim orientation |
| Knowledge Calibration | none in VAKS sense; score is not calibration | reject direct use |
| Review / Consolidation | no evidence-aware review; templates are placeholders | require VAKS review gate |
| Association / Relations | keyword wikilinks and graph related edges | adapt as activation hints |
| Activation / Dev Context | existing-note scan, focus search, paper cards | adapt |
| Context Pack | cache and UI presentation, but no coverage map | watch |
| Decision / Action | no action basis discipline | reject direct use |
| Use Ledger / Feedback | explicit feedback and preference update loop | adapt with quarantine |
| Cooling / Reactivation | no stale/review_due logic | add if adopted |
| Risk / Inhibition | some retries and tar safety, but weak shell boundaries | adapt only after hardening |

## Worth Extracting

### `research-scout-lane`

External sources should first enter a candidate queue:

```text
source discovery run
-> source candidate
-> source card
-> candidate distillation
-> review queue
```

This is the single most important borrowing.

### `fresh-plus-anchor-search`

Use fresh results for novelty and high-impact/venue results for grounding:

```text
fresh lane:
  new arXiv / recent repos / recent articles

anchor lane:
  S2 cited papers / standards / top venues / canonical repos
```

### `cheap-filter-before-expensive-enrichment`

The conference module avoids calling S2 on every DBLP paper. It filters first, enriches second.

VAKS can reuse this for papers, repos, articles, videos:

```text
wide search
-> cheap metadata filter
-> enrichment
-> candidate card
```

### `triage-workbench`

The web UI makes paper reading a daily triage loop:

```text
see candidate
inspect title/summary/images
deep dive if needed
like / neutral / dislike
move on
```

This is more ergonomic than dumping a Markdown list.

### `feedback-as-search-learning`

Feedback should improve future search, not truth:

```text
positive feedback -> more like this in scouting
negative feedback -> less like this / review search scope
explicit correction -> review_due
```

### `source-artifact-figures`

Figures are not just decoration. For papers, architecture diagrams and result figures are often the fastest comprehension entry.

VAKS adoption should record:

```yaml
artifact_kind: figure
source_package: arxiv_eprint
extraction_method:
artifact_path:
artifact_hash:
claim_support_allowed: false
```

## What Not To Absorb

1. Do not absorb recommendation score as truth confidence.
2. Do not absorb citation count as evidence support.
3. Do not absorb LLM summaries as reviewed comprehension.
4. Do not absorb automatic keyword/domain updates as mainline config mutation.
5. Do not absorb graph edges as reviewed relations.
6. Do not absorb direct Obsidian writes without source card boundary.
7. Do not absorb shell `exec` route patterns without parameterized execution and sandboxing.

## Fusion Fit

### Current branch fit

```yaml
fit: high
priority: P1
best_target: source-intake / research-scouting / feedback-ledger
not_target: reviewed truth layer / action basis / final knowledge graph
```

### Proposed landing shape

```yaml
candidate_pattern:
  name: research-scout-candidate-queue
  state: candidate_only
  source_types:
    - paper
    - repository
    - article
    - video
  outputs:
    - source_candidate_record
    - source_card_suggestion
    - candidate_priority_signal
    - feedback_scouting_patch
  forbidden_outputs:
    - reviewed_knowledge
    - truth_confidence
    - reviewed_relation
    - action_basis
```

## Short Verdict

值得 P1。

主要可借鉴的是：把“自动找资料”设计成候选源发现和人工/模型协作 triage 的循环，而不是让资料库自动相信、自动提升、自动行动。

一句话：

```text
evil-read-arxiv 是资料库的“侦察兵”参考，不是资料库的大脑真理层。
```
