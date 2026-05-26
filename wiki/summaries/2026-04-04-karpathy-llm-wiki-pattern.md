---
type: summary
status: summarized
created: 2026-05-26
updated: 2026-05-26
sources:
  - "[[2026-04-04-karpathy-llm-wiki-source]]"
topics:
  - llm-wiki
  - verified-knowledge-system
  - agentic-vault
verification_status: primary-source
evidence_level: primary
confidence: high
last_verified: 2026-05-26
next_review: 2026-06-26
relations:
  - target: "[[schema-md-as-ai-wiki-contract]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[2026-04-04-karpathy-llm-wiki-source]]"
    rationale: "Karpathy identifies the schema document as the key configuration that makes the LLM a disciplined wiki maintainer."
    created: 2026-05-26
    last_verified: 2026-05-26
  - target: "[[markdown-system-of-record-derived-indexes]]"
    type: supports
    strength: 4
    confidence: high
    evidence:
      - "[[2026-04-04-karpathy-llm-wiki-source]]"
    rationale: "The gist treats markdown wiki files, index, log and Git as the durable operating surface."
    created: 2026-05-26
    last_verified: 2026-05-26
  - target: "[[verified-vault-api-for-agent-brain]]"
    type: refines
    strength: 3
    confidence: medium
    evidence:
      - "[[2026-04-04-karpathy-llm-wiki-source]]"
    rationale: "The gist supports compiled context for agents but stops short of a strict verified context-pack API."
    created: 2026-05-26
    last_verified: 2026-05-26
tags:
  - summary/primary-source
  - llm-wiki
  - verified-vault
---

# 摘要：Karpathy LLM Wiki 模式

## AI-readable preamble

这是 Karpathy LLM Wiki gist 的源头摘要。当前结论：它强力支持“LLM 编译知识库，而不是每次 RAG 重找资料”的方向；但它默认 LLM 拥有 wiki 写权，我们需要加 verified schema、review 队列和 agent 权限分层。

## 一句话结论

Karpathy 的思路不是“更好的 Obsidian 模板”，而是把知识库当成可持续编译的 Markdown codebase：人负责选资料和提问题，LLM 负责整理、交叉引用、维护 index/log 和健康检查。

## 它和普通 RAG 的区别

普通 RAG：

```text
query -> retrieve raw chunks -> temporary synthesis
```

LLM Wiki：

```text
ingest source -> update persistent wiki -> query compiled knowledge -> file back valuable answers
```

核心增量是“知识会复利”。新资料进入后不是只被索引，而是被整理进已有页面、关系和冲突记录里。

## 对我们最有价值的点

1. `raw / wiki / schema` 三层非常稳定。
2. `SCHEMA.md` 是 Agent 纪律的核心，不是装饰文件。
3. `index.md` 和 `log.md` 是 LLM 恢复上下文和导航 wiki 的关键。
4. ingest 不只是写摘要，还要更新相关页面、交叉引用和 log。
5. query 的高价值答案要回写，避免死在聊天里。
6. lint/health check 是长期知识库不腐烂的必要动作。
7. 小中规模时不急着上 RAG，index-first 可以先跑通。
8. Git 是天然的历史、回滚和审查层。

## 和我们当前系统的差异

Karpathy 原文默认：

```text
LLM owns the wiki layer.
```

我们改成：

```text
Codex/user-reviewed write owns verified wiki.
Misa/gbrain read-only or suggest-only.
Review queue is not truth layer.
```

Karpathy 原文页面类型偏通用：

```text
entity / concept / comparison / query / summary
```

我们当前页面类型更偏验证和采纳：

```text
source / summary / claim / pattern / anti-pattern / decision / qa / implementation-note
```

这不是冲突，而是加强：Karpathy 给运行模式，我们加 truth gate。

## 采纳判断

采纳：

- raw 不可变。
- schema 作为 AI 操作契约。
- index-first / progressive context loading。
- ingest/query/lint 三操作。
- valuable answer file-back。
- Git 审计。
- 搜索工具只作为后续增强。

改造：

- `LLM writes wiki entirely` 改为 `Codex reviewed write + Misa suggest-only`。
- `wiki page synthesis` 改为 `claim/pattern/decision with evidence and negative evidence`。
- `contradiction noted in page` 改为 `verification_status: conflicted + evidence_timeline + review`。

暂不做：

- 自动 batch ingest 大量资料。
- scheduled agents 自动维护。
- 让 Misa/gbrain 直接修改正式 wiki。
- 过早上 qmd/vector/Zilliz。

## 对下一步的影响

当前 `SCHEMA.md` 方向是对的。下一步不应该继续盲目看工具，而应该补：

1. `templates/review-candidate.md`
2. `templates/summary-record.md`
3. health check / schema lint
4. context pack 最小格式
5. `index.md` / `log.md` 是否需要从现有 `knowledge-graph-index.md` 和 git history 中分离出来

## 当前缺口

- 还没有正式 `log.md`。
- 还没有 schema lint 脚本。
- 还没有 review candidate 模板。
- 还没有 context pack 生成器。
- 已有节点类型和 Karpathy entity/concept/comparison 模型需要继续映射，而不是混用。
