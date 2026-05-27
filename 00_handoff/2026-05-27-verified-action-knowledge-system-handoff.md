# 2026-05-27 handoff：Verified Action Knowledge System 主架构确认

## 工作目录

```text
C:\Users\Administrator\Documents\资料库
```

## 当前主结论

主架构已选定：

```text
Verified Action Knowledge System
```

不是普通 Obsidian 笔记库，不是单纯 Karpathy LLM Wiki，也不是直接 fork `atomicstrata/llm-wiki-compiler`。

最终目标是：

```text
raw source
-> ingest / compiler
-> review candidate
-> verified knowledge graph
-> decision / action basis
-> context pack / API / viewer
-> human / agent action
-> feedback timeline
-> updated confidence / gaps / next review
```

一句话：

```text
把资料变成可信知识，再变成行动依据，行动后还能反馈修正。
```

## 主架构与参考库关系

这套系统是融合设计，但不是拼盘。

各参考来源的位置：

```text
主架构:
  Verified Action Knowledge System

底层操作范式:
  Karpathy LLM Wiki

工程实现参考:
  atomicstrata/llm-wiki-compiler

模块级实现参考:
  VectifyAI/OpenKB

可信知识启发:
  gbrain

操作/维护启发:
  obsidian-second-brain

视图/workbench:
  Obsidian Bases / Base Hub

检索后端:
  QMD / nano-NotebookLM / Zilliz / hybrid retrieval

agent 接口:
  context pack / MCP / Misa read-only
```

裁决原则：

```text
能服务主架构: 吸收
不能服务: 不进
会污染主线: 拒绝
只是以后可能用: watch
```

## 是否包含 Karpathy LLM Wiki

包含，而且作为基础范式。

Karpathy 的核心能力：

```text
raw/
wiki/
index.md
log.md
ingest
query
lint
LLM 维护 wiki
Obsidian 做 IDE
```

本系统都纳入，但增加：

```text
summary
claim
pattern
anti-pattern
decision
review queue
verification_status
evidence_level
relations
context pack
agent access tiers
action feedback
```

## 是否包含 llm-wiki-compiler

包含其工程能力，但不采用它的 generic schema 作为 truth layer。

`llm-wiki-compiler` 已纳入实现目标的能力：

```text
ingest
incremental compile
source hash/state
concept extraction
review queue
candidate approve/reject
claim-level provenance
static lint
query
context pack
MCP
viewer
watch
export
project next action
```

## 是否包含 OpenKB

包含其模块级设计，但不采用它的 generic concept wiki 作为 truth layer。

OpenKB 已纳入实现参考的能力：

```text
PageIndex long-document tree source adapter
wiki foundation / generator surface separation
query / chat over compiled wiki
Skill Factory
skill validate / eval / history / rollback
path-scoped agent write tools
ghost wikilink whitelist / strip
hash registry and remove cleanup
URL source ingest normalization
skill trigger/body alignment eval
skill iteration workspace / rollback
```

不能直接照搬：

```text
summary / concept / exploration
```

作为核心 truth schema。

OpenKB 的正确位置：

```text
source adapter
candidate compiler
context pack / query surface
output adapter / skill generator
lint rule pack
agent access tier reference
```

我们改造方向：

```text
concept wiki compiler
-> verified action knowledge compiler
```

不能直接照搬：

```text
concept/entity/comparison/overview
```

作为核心 truth schema。

我们的核心节点必须是：

```text
source
summary
claim
pattern
anti-pattern
decision
qa
implementation-note
```

## 防止四不像的主裁决框架

后续任何新库、新功能、新插件、新 agent 思路进入前，必须回答：

```text
1. 它属于哪一层？
2. 它解决哪一个真实痛点？
3. 它增强可信知识、行动依据，还是只是看起来高级？
4. 它是否能以模块形式接入？
5. 它失败时能否回退到 Markdown 主记录？
6. 它是否会绕过 review gate？
7. 它是否会把候选召回误当 truth？
8. 不做它，系统是否仍能跑通？
```

答不清楚：

```text
不进核心，只能进 watch / candidate。
```

## 当前核心分层

```text
1. raw source layer
   原始资料、repo snapshot、文章、论文、会话、项目材料。

2. ingest / compiler layer
   source adapters、hash/state、LLM compile、summary/claim/pattern extraction。

3. review candidate layer
   AI/Misa/Codex 只能生成候选；候选通过 lint/review 后才能入库。

4. verified knowledge graph layer
   source / summary / claim / pattern / anti-pattern / decision。

5. relation / health layer
   relations、edge strength、graph health、schema/provenance/relation lint。

6. retrieval layer
   BM25/vector/GraphRAG/Zilliz/QMD 只做候选召回，不做 truth。

7. context pack / API layer
   给 agent 返回带证据、置信度、反例、gaps、actionability 的包。

8. agent access layer
   read-only / suggest-only / reviewed-write / owner-final。

9. decision / action basis layer
   行动建议、前提、风险、回退、成功指标。

10. feedback timeline layer
   行动结果、用户修正、field test 反向更新 confidence / gaps / next_review。

11. viewer / Obsidian workbench layer
   Bases、viewer、dashboard、review workbench，只做视图和操作台。
```

## 当前已落地的重要文件

核心契约与决策：

- `purpose.md`
- `ARCHITECTURE_PRINCIPLES.md`
- `SCHEMA.md`
- `wiki/decisions/2026-05-26-architecture-layering-v0-1.md`
- `wiki/decisions/2026-05-27-implementation-includes-llm-wiki-stack.md`
- `wiki/decisions/2026-05-27-quality-bar-extensible-verified-action-knowledge-system.md`
- `wiki/decisions/2026-05-27-codex-mediated-ingest-and-review-gate.md`
- `wiki/decisions/2026-05-27-karpathy-simple-verified-strict-ux-principle.md`
- `wiki/decisions/2026-05-27-karpathy-spine-modular-extensions.md`
- `wiki/decisions/2026-05-27-traceability-first-graduated-verification.md`
- `wiki/indexes/knowledge-graph-index.md`

Karpathy / llm-wiki-compiler：

- `raw/articles/2026-04-04-karpathy-llm-wiki-source.md`
- `wiki/summaries/2026-04-04-karpathy-llm-wiki-pattern.md`
- `raw/repos/2026-05-26-llm-wiki-compiler-source.md`
- `wiki/summaries/2026-05-26-llm-wiki-compiler-architecture-review.md`
- `wiki/projects/2026-05-27-llm-wiki-compiler-implementation-extraction.md`
- `raw/repos/2026-05-27-openkb-source.md`
- `wiki/summaries/2026-05-27-openkb-architecture-review.md`
- `wiki/decisions/2026-05-27-openkb-as-module-reference.md`

llm-wiki-compiler 实现级模式：

- `wiki/patterns/incremental-source-state-compiler.md`
- `wiki/patterns/self-contained-review-candidate-record.md`
- `wiki/patterns/agent-context-pack-budget-guardrails.md`
- `wiki/patterns/agent-tool-access-tiering.md`
- `wiki/patterns/source-adapter-ingest-contract.md`
- `wiki/patterns/project-state-next-action-contract.md`
- `wiki/patterns/exportable-knowledge-artifact-surface.md`
- `wiki/anti-patterns/generic-concept-schema-as-truth-layer.md`
- `wiki/patterns/wiki-foundation-generator-surface-separation.md`
- `wiki/patterns/long-document-tree-index-source-adapter.md`
- `wiki/patterns/knowledge-to-agent-skill-factory.md`
- `wiki/patterns/path-scoped-agent-output-writes.md`
- `wiki/patterns/ghost-wikilink-whitelist-before-write.md`
- `wiki/patterns/source-hash-registry-and-idempotent-ingest.md`
- `wiki/patterns/url-source-ingest-normalization.md`
- `wiki/patterns/removal-cleanup-with-registry-commit-point.md`
- `wiki/patterns/artifact-trigger-and-body-alignment-eval.md`
- `wiki/patterns/skill-artifact-iteration-workspace-rollback.md`
- `wiki/anti-patterns/auto-compiled-concept-wiki-as-verified-truth-layer.md`

已确认高优先级模式：

- `wiki/patterns/review-gated-compile-queue.md`
- `wiki/patterns/claim-level-provenance-source-ranges.md`
- `wiki/patterns/context-pack-evidence-envelope.md`
- `wiki/patterns/static-wiki-health-lint-before-auto-rewrite.md`
- `wiki/anti-patterns/direct-compile-to-truth-layer-without-review.md`

Codex-mediated intake 决策：

- `wiki/decisions/2026-05-27-codex-mediated-ingest-and-review-gate.md`

当前规则：

```text
普通自动捕获 -> raw/inbox 或对应 raw source 目录 -> daily/weekly 候选整理
用户点名提炼 -> raw source -> Codex 立即生成候选 -> review 后晋级 wiki
```

关键边界：

```text
自动系统只负责 capture 和 review candidate。
Codex 是默认入库把关者。
用户是最终采纳者。
daily brief / weekly synthesis 不能直接成为 verified truth 或 decision。
```

UX / 开源定位关键决策：

- `wiki/decisions/2026-05-27-karpathy-simple-verified-strict-ux-principle.md`
- `wiki/decisions/2026-05-27-karpathy-spine-modular-extensions.md`

独立 gpt-5.5 xhigh subagent 评审结论：

```text
Verdict: 有条件强。

功能能力上限可以强于单个参考库。
但体验不天然强于 Karpathy。
只有默认体验保持 Karpathy-simple，严格 verified/action 层藏在后台，才可能同时赢体验和能力。
```

必须写入 `IMPLEMENTATION_BLUEPRINT.md` 最前面的原则：

```text
1. 第一版只证明一条 source -> candidate -> lint/review -> verified node -> context pack 的端到端闭环。
2. 默认体验必须 Karpathy-simple：快速捕获、快速查询、可读 index/log。
3. Candidate 永远不是 truth。
4. Schema 分必填底线字段和晋级增强字段；严格字段不要污染普通 capture。
5. API/MCP/viewer/Skill Factory/vector/PageIndex 都必须可关闭，Markdown 主记录仍可跑通。
```

2026-05-27 新增验证纠偏：

```text
Traceability first.
Verification only when it matters.
```

含义：

```text
raw/source:
  只要求来源可追溯，不要求填满 evidence/confidence/relations。

candidate:
  要能审：source refs、source ranges、extracted point、uncertainty。

claim / pattern / anti-pattern:
  再补 evidence、confidence、negative evidence、gaps、关键 relations。

decision / context pack / implementation-note:
  才需要 risk、preconditions、rollback、success metric、feedback path。
```

这个纠偏避免验证系统阻碍 capture。严格验证仍然存在，但只卡晋级和行动依据，不卡普通收集。

配套新增模式：

```text
wiki/patterns/accumulated-source-cross-validation.md
REVIEW_QUEUE.md
FEEDBACK.md
templates/review-candidate.md
templates/feedback-event.md
outputs/qa/2026-05-27-alpha-point-collision-research.md
wiki/projects/2026-05-27-alpha-point-collision-validation-v0-1.md
```

含义：

```text
每条 source 先进来并保留 provenance。
后续相似内容越来越多时，再通过 supports / contradicts / refines / replaces 形成交叉验证。
库越厚，越能发现重复观点、冲突观点、同源搬运和稳定模式。
重复出现只是晋级信号，不自动等于 truth。
```

Alpha v0.1 已收束为：

```text
provenance-first
-> candidate point
-> point collision signal
-> point cluster
-> reviewed promotion
```

核心对象：

```text
source trace
candidate point
collision signal
point cluster
```

硬边界：

```text
不能因为相似就自动 cross-checked。
不能把同源复制算独立支持。
不能把 AI summary 算独立来源。
不能自动涨 confidence。
不能自动晋级 claim / pattern / decision。
```

反馈校准规则已新增：

```text
FEEDBACK.md
templates/feedback-event.md
```

核心边界：

```text
truth confidence:
  观点真不真，只能通过 review/promotion 改。

usefulness:
  这条知识对某类问题有没有帮助，可以由反馈调排序。

scope fit:
  这条知识适不适合当前项目/版本/场景，可以由反馈收窄。
```

用户反馈不能直接改 truth，不能隐藏反证，不能自动晋级。反馈只校准 activation path，并生成 review work。

当前最终路线已确认：

```text
主骨架:
  Karpathy-style LLM Wiki
  raw / wiki / index / log / ingest / query / lint

内部严格层:
  Verified Action Knowledge System
  review gate / evidence / relations / decision / context pack / feedback

模块枝叶:
  llm-wiki-compiler = review queue / provenance / lint / context pack / MCP / viewer
  OpenKB = long-doc / Skill Factory / scoped writes / hash registry
  obsidian-second-brain = preamble / propagation / progressive context / health check
  gbrain = fact/take/hypothesis/bet/decision / holder / timeline / gaps
  retrieval/viewer/API = replaceable runtime modules
```

一句话：

```text
骨架选 Karpathy，内核用 verified-action，枝叶按需吸收其他库强项。
```

本轮新增 cyrilXBT / automated vault 系列：

- `raw/articles/2026-05-27-automated-obsidian-daily-brief-source.md`
- `wiki/summaries/2026-05-27-automated-vault-feedback-loop-review.md`
- `wiki/patterns/frictionless-capture-to-review-inbox.md`
- `wiki/patterns/daily-brief-as-knowledge-return-loop.md`
- `wiki/patterns/weekly-synthesis-thesis-and-gap-review.md`
- `wiki/anti-patterns/automated-brief-as-truth-without-review.md`
- `raw/articles/2026-05-27-jarvis-obsidian-claude-code-source.md`
- `wiki/summaries/2026-05-27-jarvis-content-vault-review.md`
- `wiki/patterns/published-performance-feedback-loop.md`

判断：

```text
automated vault / daily brief:
  有用点是知识返还和候选整理。
  只能进入 raw/review/feedback，不能自动成为 truth。

JARVIS inside Obsidian:
  是内容创作者工作流，不是 verified knowledge architecture。
  只吸收 published performance feedback loop。
  其它内容归并到已有 skills-as-action-modules 和 source-to-publish-content-pipeline。
```

本轮新增关系图结论：

- `wiki/patterns/project-crosslink-graph-view.md`

判断：

```text
可以展示项目之间的联系图。
但它属于 viewer / Obsidian workbench layer。
图必须从 reviewed relations 生成。
不能让 Obsidian 双链、tag、vector 相似度或漂亮大网图替代可信关系边。
```

Review 目录：

- `outputs/review/README.md`

## 当前 architecture quality bar

目标不是“更安全的 LLM Wiki”，而是：

```text
参考库能力全覆盖
+ verified truth layer
+ action basis layer
+ extensible module contracts
+ review / lint / evidence gates
+ feedback from real actions
```

判断是否真的比参考库好，看：

```text
1. 同一份 raw source，能否产出比普通 wiki 更可验证的 claim？
2. 同一批参考库，能否提炼出 pattern、anti-pattern 和 decision？
3. Agent 拿到 context pack 后，是否知道哪些能行动、哪些不能？
4. 决策出错后，系统是否能记录反馈并降低置信度？
5. 新检索、新 UI、新 API、新 agent 能否作为插件接入，而不改 truth layer？
6. 用户能否从资料入库一路走到行动建议，而不是停在“我知道一些笔记”？
```

## 当前不要做什么

## 本轮新增 alpha：conversation-derived feedback routing

本轮核心发现：

```text
用户的连续对话本身可以成为反馈。
但它只能校准 retrieval / activation route，不能改 truth。
```

用户提出的关键洞察：

```text
如果继续沿着同一条线聊，说明这条线路可能有用。
如果追问更具体，说明需要生成更细的需求关键词和子通道。
如果说跑偏、不是这个意思、漏了某点，说明要修正 route / scope / missing signal。
如果没有继续追问，不能自动脑补为满意或不满意。
```

最终收敛设计：

```text
conversation-derived feedback
= 低置信度 route / keyword / scope 信号
!= truth signal
!= 自动训练模型
!= 自动修改 verified node
```

落地存储规则：

```text
Markdown:
  人能读的知识主资料。

JSONL:
  append-only 记录 query-run / feedback-event，是事件真相。

SQLite:
  未来可选，只做可删除、可重建的索引缓存。
```

信号规则：

```text
明确说有用:
  强正反馈，可持久化为 usefulness / route boost。

继续沿同线追问:
  弱正反馈，默认只在当前 session 内加权。

追问更具体:
  生成或增强 route / keyword / channel。

说跑偏 / 不是这个意思:
  降 route / scope fit，不降 truth confidence。

说漏了:
  生成 missing-point / missing-route candidate。

换题:
  关闭上一条 route，不写持久反馈。

没有继续追问:
  neutral / unknown，不更新权重。
```

必须守住的边界：

```text
feedback can adjust:
  usefulness
  scope fit
  activation ranking
  route / keyword boost

feedback cannot adjust:
  truth confidence
  verification_status
  source reliability
  decision outcome
```

这条设计和 point collision 互补：

```text
point collision:
  让知识本身越积累越能交叉验证。

conversation-derived feedback routing:
  让查询路径越使用越懂用户真实需求。
```

外部调研结论：

```text
外部有关键零件：
  implicit feedback
  query reformulation / session search
  learning-to-rank bias warnings
  trace feedback
  RAG feedback

但没有看到完整等于本系统的闭环。
本系统的 alpha 是把这些零件收束到 verified-action knowledge system：
  反馈只调路线，不改真理。
```

不要再回到旧问题：

```text
不要只做 Obsidian 模板。
不要只做 SCHEMA，不做运行能力。
不要直接 fork 某个库作为主架构。
不要为了实现某个库的功能硬加模块。
不要让 concept schema 替代 verified node flow。
不要让 retrieval / vector / graph score 替代 truth layer。
不要让 agent 直接写 formal wiki。
不要在 schema/review/lint 未稳定前上 full auto rewrite。
```

## 当前下一步建议

`IMPLEMENTATION_BLUEPRINT.md`、`REVIEW_QUEUE.md`、`FEEDBACK.md` 已创建。下一步不要继续加重验证，而是跑第一个 10-source point collision + conversation-derived feedback trial：

```text
1. 选择 10 条真实 source。
   从每条 source 抽 2-8 个 candidate point。

2. 生成 collision signal。
   supports / contradicts / refines / replaces / duplicates / near_miss。

3. Review collision signal。
   只把 reviewed signal 用作晋级信号。

4. CONTEXT_PACK.md
   answer/decision/implementation/Misa memory pack 的 JSON contract。

5. LINT_RULES.md
   traceability/provenance/promotion/actionability/agent-access lint。

6. AGENT_ACCESS.md
   Misa/gbrain/Codex/user 的权限层与工具边界。

7. query-run / feedback-event 试跑
   用一次真实追问或纠偏，生成 conversation-derived feedback event。
```

建议顺序：

```text
10-source point collision trial
-> one query-run + feedback-event trial
-> CONTEXT_PACK.md
-> LINT_RULES.md
-> AGENT_ACCESS.md
```

## 下一窗口恢复读法

先读本文件：

```text
00_handoff/2026-05-27-verified-action-knowledge-system-handoff.md
```

然后读：

```text
purpose.md
ARCHITECTURE_PRINCIPLES.md
SCHEMA.md
wiki/decisions/2026-05-27-quality-bar-extensible-verified-action-knowledge-system.md
wiki/decisions/2026-05-27-implementation-includes-llm-wiki-stack.md
wiki/decisions/2026-05-27-codex-mediated-ingest-and-review-gate.md
wiki/decisions/2026-05-27-karpathy-simple-verified-strict-ux-principle.md
wiki/decisions/2026-05-27-karpathy-spine-modular-extensions.md
wiki/decisions/2026-05-27-traceability-first-graduated-verification.md
wiki/decisions/2026-05-26-architecture-layering-v0-1.md
IMPLEMENTATION_BLUEPRINT.md
REVIEW_QUEUE.md
FEEDBACK.md
wiki/projects/2026-05-27-llm-wiki-compiler-implementation-extraction.md
wiki/projects/2026-05-27-alpha-point-collision-validation-v0-1.md
wiki/summaries/2026-05-27-openkb-architecture-review.md
wiki/summaries/2026-05-27-automated-vault-feedback-loop-review.md
wiki/summaries/2026-05-27-jarvis-content-vault-review.md
wiki/patterns/accumulated-source-cross-validation.md
wiki/patterns/conversation-derived-feedback-routing.md
wiki/patterns/published-performance-feedback-loop.md
wiki/patterns/project-crosslink-graph-view.md
outputs/qa/2026-05-27-alpha-point-collision-research.md
outputs/qa/2026-05-27-conversation-derived-feedback-routing-research.md
wiki/indexes/knowledge-graph-index.md
```

如果要继续实现蓝图，优先创建：

```text
10-source point collision trial + one query-run / feedback-event trial
```

`ARCHITECTURE_PRINCIPLES.md` 已创建，并已明确：

```text
主架构: Verified Action Knowledge System
参考库位置: Karpathy / llm-wiki-compiler / gbrain / obsidian-second-brain / retrieval tools
每层职责
什么能进核心
什么只能进外围
什么绝不允许
如何吸收新库
如何防止四不像
```

## 当前状态

- `SCHEMA.md v0.1` 已创建。
- `ARCHITECTURE_PRINCIPLES.md v0.1` 已创建。
- `IMPLEMENTATION_BLUEPRINT.md v0.1` 已创建。
- `REVIEW_QUEUE.md v0.1` 已创建。
- `FEEDBACK.md v0.1` 已创建。
- `wiki/patterns/conversation-derived-feedback-routing.md` 已创建，定义从连续对话反推低置信度 route / keyword / scope 信号。
- `outputs/qa/2026-05-27-conversation-derived-feedback-routing-research.md` 已创建，记录外部 implicit feedback / session search / RAG feedback 调研结论。
- `templates/review-candidate.md` 已创建。
- `templates/feedback-event.md` 已创建。
- `templates/query-run.md` 已创建。
- `outputs/feedback/README.md` 已创建，定义 feedback JSONL 事件日志目录。
- `wiki/projects/2026-05-27-memory-tier-and-publishing-pipeline-draft.md` 已创建，作为下一窗口方向草案：冷热分层和 5 步发布工作流一起考虑、分开落地。
- 已新增 traceability-first / graduated verification 决策：raw/source 先保来源可追溯，严格验证只在晋级和行动依据阶段触发。
- 已新增 alpha point collision 研究记录和 v0.1 落地规格。
- 主架构已定为 `Verified Action Knowledge System`。
- `llm-wiki-compiler` 已完成高层和源码级第一轮提取。
- OpenKB 已完成 README 和源码级第一轮提取，定位为模块级实现参考。
- Karpathy LLM Wiki 已作为基础范式纳入。
- 当前系统是融合设计，各取所长，但主裁决框架已明确。
- 还没有创建 `CONTEXT_PACK.md` / `LINT_RULES.md` / `AGENT_ACCESS.md` 等后续实现规格文件。
- 还没有创建 `MEMORY_TIER.md` / `PUBLISHING_PIPELINE.md` / `templates/publish-draft.md`；当前只有方向草案。
- 还没有真正实现脚本、API、MCP、viewer；当前是架构与知识系统设计阶段。

## 明确未落地清单

下个窗口不要忘记：下面这些只是设计方向或规格，尚未跑通。

```text
1. 反馈逻辑已设计，但执行层未落地
   已有:
     FEEDBACK.md
     templates/feedback-event.md
     templates/query-run.md
     outputs/feedback/README.md
     wiki/patterns/conversation-derived-feedback-routing.md

   未做:
     真实 query-run JSONL
     真实 feedback-event JSONL
     问题 -> 追问/纠偏 -> 第二次召回改善 的试跑
     JSONL 聚合权重规则脚本
     SQLite rebuildable cache

2. 5 步发布工作流未落地
   已有:
     source-to-publish-content-pipeline pattern
     published-performance-feedback-loop pattern
     products/ 目录
     memory-tier + publishing-pipeline draft direction

   未做:
     PUBLISHING_PIPELINE.md
     templates/publish-draft.md
     capture -> triage -> theme -> draft -> publish -> feedback 的正式字段
     发布后评论/指标 -> feedback-event / missing-point 的试跑

3. 冷热分层未正式落地
   已有:
     wiki/projects/2026-05-27-memory-tier-and-publishing-pipeline-draft.md

   未做:
     MEMORY_TIER.md
     memory_tier / activation_status / last_activated 字段接入 SCHEMA.md
     hot / warm / cold dashboard 或查询规则

4. point collision 还没有真实试跑
   已有:
     REVIEW_QUEUE.md
     wiki/projects/2026-05-27-alpha-point-collision-validation-v0-1.md

   未做:
     10-source trial
     candidate point 抽取
     collision signal 生成
     reviewed cluster 晋级样例
```

最建议的下一步顺序：

```text
MEMORY_TIER.md
-> PUBLISHING_PIPELINE.md
-> templates/publish-draft.md
-> one query-run + feedback-event trial
-> 10-source point collision trial
```
