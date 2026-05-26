---
type: summary
status: active
created: 2026-05-27
updated: 2026-05-27
tags:
  - openkb
  - llm-wiki
  - pageindex
  - skill-factory
  - architecture-review
sources:
  - "[[2026-05-27-openkb-source]]"
verification_status: primary-source
evidence_level: primary
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
relations:
  - target: "[[2026-05-27-openkb-as-module-reference]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-openkb-architecture-review]]"
    rationale: "OpenKB should be treated as a module reference for ingest, long-doc retrieval, generator surfaces, and skill output."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[auto-compiled-concept-wiki-as-verified-truth-layer]]"
    type: risk_of
    strength: 4
    confidence: high
    evidence:
      - "[[2026-05-27-openkb-architecture-review]]"
    rationale: "OpenKB's direct concept-page update model is useful for generic wiki compilation but risky as verified truth."
    created: 2026-05-27
    last_verified: 2026-05-27
---

# OpenKB 架构提炼

## 一句话结论

OpenKB 是 Karpathy LLM Wiki 的 Python/PageIndex/Skill Factory 版本：它适合作为实现模块参考，不适合作为本资料库的主 truth schema。

更准确地说：

```text
OpenKB = raw/wiki compiler + long-doc adapter + query/chat + skill generator
本系统 = verified truth layer + action basis + review gate + extensible runtime
```

两者不冲突，但层级不能反过来。

## 它完整实现了什么

OpenKB 的核心链路是：

```text
raw document
-> local ingest
-> short doc full-text conversion or long PDF PageIndex
-> wiki/sources
-> wiki/summaries
-> wiki/concepts
-> index.md / log.md
-> query / chat / Skill Factory / lint
```

它的目录结构接近 Karpathy 思路：

```text
raw/
wiki/
  index.md
  log.md
  AGENTS.md
  sources/
  summaries/
  concepts/
  explorations/
  reports/
output/
  skills/
.openkb/
  config.yaml
  hashes.json
  pageindex state
```

## 最强的地方

### 1. 长文档处理比普通 LLM Wiki 强

短文档走 full-text conversion，长 PDF 走 PageIndex tree，再把页面内容保存成可切片 JSON。

这比“把整个 PDF 塞给 LLM”或“只做向量 chunk”更适合 agent：

```text
summary tells agent where to look
agent fetches tight page ranges
source windows remain inspectable
no vector DB required for v0
```

对我们来说，它应该进入 `source adapter` 设计。

### 2. Wiki foundation 和 generator surface 分得清楚

OpenKB 明确把 wiki foundation 和 query/chat/skill generator 分开。

这和我们的架构原则一致：

```text
verified knowledge graph = substrate
context pack / API / skill / report = surfaces
```

这个分层可以直接进入 `IMPLEMENTATION_BLUEPRINT.md`。

### 3. Skill Factory 很有价值

OpenKB 不只回答问题，还能把 wiki 编译成可分发 Anthropic Skill。

这个点比普通 context pack 更进一步：

```text
context pack = one次任务上下文
skill = 可安装、可复用、可触发的 agent 能力包
```

我们可以吸收成 `output adapter`：

```text
verified nodes -> skill candidate -> validate/eval -> approved skill
```

### 4. Agent 工具权限边界做得对

OpenKB query agent 主要读 wiki；chat 写工具限制在 `wiki/explorations/**` 和 `output/**`。Skill agent 只能写目标 skill 目录。

这验证了我们的 agent access tier：

```text
read wiki
write only candidate/output
no direct formal truth rewrite
```

### 5. Ghost wikilink 防线很实用

OpenKB 在 LLM 写 concept/summary 前构造 known target whitelist，并在写入前 strip unresolved wikilinks。

这可以直接转成我们的 lint/write validator：

```text
LLM may propose links
program validates targets
unknown target becomes plain text or review issue
```

## 不适合直接采用的地方

### 1. Generic concept schema 不够

OpenKB 的核心 wiki 类型是：

```text
summary
concept
exploration
```

这对普通知识库够用，但对我们不够。我们需要：

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

原因很简单：我们不只是要知道“某个概念是什么”，还要知道“哪个 claim 可验证、哪个 pattern 可采用、哪个 decision 可行动”。

### 2. Direct compile 会绕过 review gate

OpenKB `add` 会直接更新 summaries/concepts/index/log。

这适合个人 wiki 自动维护，但本资料库不能让它直接写 formal truth layer。正确改造是：

```text
OpenKB-style compile
-> candidate summary / candidate claim / candidate pattern
-> lint
-> review queue
-> approve into verified wiki
```

### 3. Contradiction flag 不等于 verified conflict handling

README 提到 contradictions are flagged，但源码层的核心强项主要是 structural lint + semantic lint prompt。它没有把冲突证据、negative evidence、holder、valid_from/valid_until、decision rollback 做成主 schema。

所以它能帮我们发现问题，但不能替代我们的 verification model。

### 4. Watch auto-compile 不适合作为 v0.1 默认

`openkb watch` 对普通 LLM Wiki 很方便，但对 verified system 风险偏高。

在本资料库中它只能进入：

```text
raw source watcher -> candidate queue
```

不能进入：

```text
raw source watcher -> formal wiki rewrite
```

## 对我们当前架构的价值排序

| OpenKB 设计 | 价值 | 是否吸收 | 所属层 |
|---|---:|---|---|
| PageIndex long-doc tree adapter | 很高 | 吸收为候选模块 | source adapter / retrieval |
| wiki foundation + generator surfaces | 很高 | 吸收为原则 | architecture / output adapter |
| Skill Factory | 很高 | 中期吸收 | output adapter / agent access |
| path-scoped agent tools | 高 | 吸收 | agent access |
| ghost wikilink whitelist | 高 | 吸收 | lint / write validator |
| hash registry / idempotent ingest | 中高 | 吸收 | ingest state |
| URL source ingest normalization | 中 | 吸收为候选模块 | source adapter |
| remove cleanup with commit point | 中高 | 吸收为候选模块 | lifecycle |
| skill trigger/body alignment eval | 高 | 吸收为质量门 | output adapter / eval |
| skill iteration workspace / rollback | 中高 | 吸收为候选模块 | output lifecycle |
| generic concept pages | 中 | 只做兼容输入 | compile candidate |
| watch auto-compile | 中低 | 暂缓 | automation |
| direct concept rewrite | 风险高 | 不进 core | anti-pattern |

## 和 llm-wiki-compiler 的区别

`llm-wiki-compiler` 更像完整 wiki compiler + review queue + context pack + MCP/viewer。

OpenKB 更像：

```text
LLM wiki compiler
+ PageIndex long document handling
+ query/chat agent
+ skill factory
+ output marketplace
```

它对我们的新增启发主要不是 review queue，而是：

```text
long-doc adapter
generator output layer
skill validation / eval / rollback
agent read/write path discipline
source hash registry
retryable remove lifecycle
URL acquisition normalization
```

## 融合判断

OpenKB 应该作为模块参考进入我们的架构，但不能作为主架构。

推荐融合方式：

```text
OpenKB ingest ideas
-> our source adapter contract

OpenKB concept compiler
-> our candidate compiler

OpenKB query/chat
-> our context pack/API layer

OpenKB Skill Factory
-> our output adapter / skill pack generator

OpenKB lint
-> our lint rule pack

OpenKB hash/remove/workspace ideas
-> our implementation lifecycle rules
```

最终裁决权仍属于：

```text
SCHEMA.md
ARCHITECTURE_PRINCIPLES.md
review queue
decision records
```
