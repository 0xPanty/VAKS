---
type: output
status: completed
created: 2026-05-26
topic: gbrain second brain architecture analysis
sources:
  - raw/repos/2026-05-26-gbrain-source.md
related_patterns:
  - markdown-system-of-record-derived-indexes
  - compiled-truth-plus-append-only-timeline
  - epistemology-takes-facts-layer
  - schema-packs-as-living-contract
  - think-gather-synthesize-gap-analysis
related_decisions:
  - wiki/decisions/2026-05-26-architecture-layering-v0-1.md
confidence: high
---

# 问答记录：gbrain 对我们有什么可取之处？

## 问题

`garrytan/gbrain` 这个之前很火的 agent 第二大脑是否有可以借鉴的思路？它和截图里的 8 层 RAG 说法，对我们当前资料库架构有什么启发？

## 大白话结论

gbrain 最有价值的地方不是“它会向量搜索”，而是它把第二大脑做成了一个知识引擎：

```text
资料不是直接喂给 AI
  -> 先变成可追溯的事实、观点、关系、当前结论和历史证据
  -> 再由检索和图谱找证据
  -> 最后合成带引用和缺口的回答
```

它补全了我们当前骨架里最薄的两块：

1. `epistemology layer`：谁说了什么、什么时候说、这是事实还是观点、置信度多少。
2. `synthesis / dream cycle layer`：周期性把热事实沉淀为冷判断，找 pattern、找矛盾、更新当前结论。

## 和截图 8 层的对应

| 截图层 | gbrain 体现 | 对我们的启发 |
|---|---|---|
| Chunking | markdown chunker v3、code chunker v4、tree-sitter、CJK fallback、chunker_version | 未来索引必须记录 chunker version；代码/文章/会议不能同一种切法 |
| Embedding | 多 embedding column / provider / cache safety | embedding namespace 是硬规则，不能混模型 |
| Indexing | HNSW / pgvector / atomic swap rebuild | 中后期再做，当前只记录不实现 |
| Query understanding | regex intent、recency/salience/detail/modality、可选 LLM expansion | 检索要先理解问题类型，不是盲 top-k |
| Reranking | fail-open reranker、audit failure | reranker 只能增强，不能让搜索不可用 |
| Epistemology | facts / takes / bet / hunch、holder、confidence、weight、time | 这是我们应立即吸收进 schema 的核心 |
| Entity linking | typed edges、frontmatter link rules、graph signals | 我们需要 supports / contradicts / refines / replaces 等 verified relation |
| Synthesis | think answer+citation+gaps、dream cycle consolidate/patterns | 未来 context pack 应返回 answer + citations + gaps + negative evidence |

## 可取之处

### 1. Brain / memory / session 分层

gbrain 明确区分：

- brain：世界知识和长期知识库。
- memory：agent 操作偏好、用户习惯。
- session：当前任务上下文。

这和我们之前的 `Verified Vault / Agent gbrain / Session` 分层完全同频。对我们来说，资料库不应该塞 agent 的临时偏好，也不应该把当前聊天当永久真相。

### 2. Markdown 是主记录，索引都是派生物

gbrain 很强调 system of record：Markdown brain repo 是 canonical，DB / graph / vector / cache 都可重建。

这支持我们的底层路线：Obsidian/Bases/API/RAG 都只是视图或派生层，truth 在 Markdown source / claim / decision 文件里。

### 3. Compiled truth + timeline

gbrain 的思路是页面顶部保存当前综合结论，timeline 保存证据变化。

这正好解决我们之后融合多个库时的问题：最终 decision 要能更新，但旧证据不能消失。

### 4. Takes / facts 是工程化 epistemology

gbrain 不只存相似文本，而是存：

- fact
- take
- bet
- hunch
- holder
- confidence
- source
- since / until

这比普通 claim 模板更细。我们应该把它压缩进自己的 `SCHEMA.md`，但不用照搬它的数据库表。

### 5. Schema packs 给 `SCHEMA.md` 提供未来形态

gbrain 用 schema pack 定义 page type、link type、filing rule、extractable、routing。我们当前不需要 runtime pack，但 `SCHEMA.md` 应该按这种“活契约”来设计。

### 6. Think pipeline 是未来 context pack 的样子

gbrain `think` 不是只 search，而是 gather pages/takes/graph evidence，再 synthesize answer、citations、gaps。

这给了我们未来 API 的输出形态：

```text
context-pack =
  answer draft
  + supporting claims
  + contradicting claims
  + source citations
  + confidence
  + gaps / unknowns
```

## 不该照搬的地方

- 不直接 fork gbrain。
- 不现在做 MCP / OAuth / minions / scheduler / company brain。
- 不现在做完整 HNSW/reranker/graph search 系统。
- 不让 LLM 自动写入大量 facts/takes 后直接信任。
- 不用 gbrain 默认 page schema 替代我们的 source/claim/pattern/anti-pattern/decision schema。

## 对当前主线的影响

gbrain 把我们下一步优先级压得更清楚：

1. 先写 `SCHEMA.md`。
2. claim 要有 epistemic status：fact/take/hypothesis/bet/decision。
3. 每个 decision 要有 compiled truth + evidence timeline。
4. 关系类型要能表达 supports / contradicts / refines / replaces / derived_from / risk_of。
5. 健康检查要查 unsupported claim、conflicted claim、stale decision、missing evidence。
6. 搜索和 API 放中期，不是当前第一步。

## 最终判断

gbrain 是目前最值得吸收的架构参考之一，但它是“压缩吸收”的对象，不是“直接采用”的对象。

一句话：

```text
它证明我们不是在做普通 RAG；
我们要做的是带证据、立场、时间和采纳门槛的 verified knowledge engine。
```

