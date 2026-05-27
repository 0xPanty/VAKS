---
type: qa
status: archived
created: 2026-05-27
updated: 2026-05-27
question: "连续对话能不能反推检索权重和需求关键词？应该用 SQL 还是别的方式记录？"
answer_summary: "可行，但应把它当成低置信度 routing feedback。v0.1 用 Markdown 做知识主资料、JSONL append-only 做事件真相、SQLite 做可重建索引缓存。隐式反馈只调 usefulness、scope fit、activation ranking、route/keyword boost，不改 truth confidence。"
sources:
  - "https://www.microsoft.com/en-us/research/publication/unbiased-learning-rank-biased-feedback/"
  - "https://www.microsoft.com/en-us/research/publication/exploring-session-context-using-distributed-representations-of-queries-and-reformulations/"
  - "https://openai.github.io/openai-agents-js/guides/tracing/"
  - "https://platform.openai.com/docs/guides/trace-grading"
  - "https://docs.langchain.com/langsmith/attach-user-feedback"
  - "https://learn.microsoft.com/en-us/azure/databricks/generative-ai/tutorials/ai-cookbook/quality-overview"
  - "https://arxiv.org/abs/2307.14117"
  - "https://arxiv.org/abs/2407.00072"
  - "https://arxiv.org/abs/2405.14431"
related_patterns:
  - "[[conversation-derived-feedback-routing]]"
  - "[[accumulated-source-cross-validation]]"
related_decisions:
  - "[[2026-05-27-traceability-first-graduated-verification]]"
verification_status: single-source
evidence_level: synthetic
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
relations:
  - target: "[[conversation-derived-feedback-routing]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-conversation-derived-feedback-routing-research]]"
    rationale: "External IR/RAG/dialogue feedback work supports treating user continuation as a biased routing signal rather than a truth signal."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - qa
  - feedback
  - implicit-feedback
  - query-routing
---

# Conversation-Derived Feedback Routing Research

## TL;DR

这个想法逻辑成立，而且有成熟近亲。

但第一版要收得很小：

```text
自然对话反推 feedback
= 低置信度 route / keyword / scope 信号
!= 自动学习事实
!= 自动训练排序模型
!= 自动修改 truth node
```

最合适的落地方式：

```text
Markdown = 人能读的知识主资料
JSONL = append-only 事件真相
SQLite = 可删除、可重建的索引缓存
```

## 外部近亲

### Implicit feedback / click feedback

搜索系统早就用用户行为当反馈，比如 click、dwell time、后续查询。

可借鉴点：

```text
用户行为可以帮助排序
但行为信号有偏差
不能把行为等同满意
```

对我们的含义：

```text
继续追问不能直接当“答案好”
只能当“这条路线可能值得继续展开”
```

### Session-based search / query reformulation

最贴近我们的不是 CTR，而是 query reformulation。

用户连续追问，本质是在改写需求：

```text
反馈怎么做
-> 自然语言反馈会不会更好
-> 能不能从继续聊天反推关键词
```

这说明系统应该记录：

```text
parent query
follow-up query
reformulation type
new inferred keywords
activated route
```

### RAG feedback / trace feedback

OpenAI trace grading、LangSmith feedback、RAG quality tuning 都在强调一件事：

```text
要记录一次运行中发生了什么
再把反馈绑定到具体步骤
```

对我们的含义：

```text
feedback 不应该只绑到最终答案
也应该能绑到 point、relation、route、keyword、context pack
```

### Dialogue implicit feedback

对话系统研究也验证了：用户后续话术可以成为反馈。

但重要警告是：

```text
长对话不一定代表满意
用户反馈内容比简单正负更重要
隐式反馈在复杂问题上很噪
```

所以我们应该记录 `signal_type` 和 `reason`，而不是只记一个赞/踩。

## v0.1 设计

只在真的用了 context activation 的重要问答里记录 `query-run`。

下一轮用户话术分类：

```text
explicit_positive
same_line_followup
narrower_followup
correction
wrong_scope
missing
topic_shift
```

事件写入：

```text
outputs/feedback/query-runs/YYYY-MM-DD.jsonl
outputs/feedback/events/YYYY-MM-DD.jsonl
```

未来 SQLite 派生：

```text
query_runs
candidate_exposures
feedback_signals
activation_adjustments
```

SQLite 只能是缓存。删掉后必须能从 JSONL 重建。

## 权重规则

使用白盒公式，不做隐藏学习：

```text
effective_delta =
  signal_strength
  * signal_confidence
  * recency_decay
  * exposure_weight
```

关键限制：

```text
same_line_followup 默认只在 session 内生效
每个 target 每个 session 最多 +/-1
长期 usefulness / scope_fit 调整限制在 -2 到 +2
旧隐式反馈随时间衰减
显式纠错优先级高于隐式继续
```

## 风险

最大风险不是技术实现，而是误读用户行为。

坏结果：

```text
用户继续追问只是因为没答好
系统却误判为路线正确
然后下次更强地召回同一路线
```

防法：

```text
继续追问只做弱信号
显式纠错权重大于隐式继续
missing 不惩罚所有已召回点
wrong_scope 先降 route/scope，不全局否定 point
contradiction 永远不能被反馈权重隐藏
```

## 结论

这条 alpha 值得落地。

它的准确表达是：

```text
conversation-derived feedback routing
```

大白话：

```text
系统看你怎么继续聊，反推哪些知识线路对你有用。
但它只调路线，不改事实。
```

第一版不需要复杂 SQL。先用 JSONL 记录真实事件，再从事件生成可重建 SQLite 索引。
