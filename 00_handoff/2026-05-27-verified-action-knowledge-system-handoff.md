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

不急着继续盲看新库。优先把已确认架构收束为可实现规格：

```text
1. IMPLEMENTATION_BLUEPRINT.md
   从 Markdown-only 到 compiler/API/viewer 的阶段路线。

2. REVIEW_QUEUE.md
   candidate 文件结构、approve/reject/archive 流程。

3. CONTEXT_PACK.md
   answer/decision/implementation/Misa memory pack 的 JSON contract。

4. LINT_RULES.md
   schema/provenance/relation/decision/actionability/agent-access lint。

5. AGENT_ACCESS.md
   Misa/gbrain/Codex/user 的权限层与工具边界。
```

建议顺序：

```text
IMPLEMENTATION_BLUEPRINT.md
-> REVIEW_QUEUE.md
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
wiki/decisions/2026-05-26-architecture-layering-v0-1.md
wiki/projects/2026-05-27-llm-wiki-compiler-implementation-extraction.md
wiki/summaries/2026-05-27-openkb-architecture-review.md
wiki/summaries/2026-05-27-automated-vault-feedback-loop-review.md
wiki/summaries/2026-05-27-jarvis-content-vault-review.md
wiki/patterns/published-performance-feedback-loop.md
wiki/patterns/project-crosslink-graph-view.md
wiki/indexes/knowledge-graph-index.md
```

如果要继续实现蓝图，优先创建：

```text
IMPLEMENTATION_BLUEPRINT.md
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
- 主架构已定为 `Verified Action Knowledge System`。
- `llm-wiki-compiler` 已完成高层和源码级第一轮提取。
- OpenKB 已完成 README 和源码级第一轮提取，定位为模块级实现参考。
- Karpathy LLM Wiki 已作为基础范式纳入。
- 当前系统是融合设计，各取所长，但主裁决框架已明确。
- 还没有创建 `IMPLEMENTATION_BLUEPRINT.md` / `CONTEXT_PACK.md` 等最终实现规格文件。
- 还没有真正实现脚本、API、MCP、viewer；当前是架构与知识系统设计阶段。
