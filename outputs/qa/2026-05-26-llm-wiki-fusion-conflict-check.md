---
type: qa
question: "llm_wiki 提炼出的模板和设计点会不会和我们的资料库架构冲突？"
asked_at: 2026-05-26
sources:
  - raw/repos/2026-05-26-llm-wiki-source.md
  - wiki/summaries/2026-05-26-llm-wiki-architecture-review.md
related:
  - wiki/decisions/2026-05-26-llm-wiki-fusion-compatibility.md
confidence: high
---

# Q&A：llm_wiki 融合冲突检查

## 结论

不冲突，但不能一次性全吞。

它的高价值设计应该被拆成可验证模块，再按阶段进入我们的资料库架构。

## 当前可放心采用

- `purpose.md`：已经补进根目录，不改变现有结构。
- review 队列思想：进入我们“未验证资料不能直接采纳”的质量门。
- sources / evidence / confidence：和我们已有可信度治理完全一致。

## 当前只能轻量采用

- 四信号关系评分：等 metadata 更干净后做脚本。
- 图谱健康检查：先输出 Markdown 报告，不做可视化。
- 来源生命周期：先 stale/review，不做自动删除。

## 当前暂不采用

- 完整桌面 App。
- Louvain 图谱 UI。
- LanceDB / vector search。
- 复杂 ingest queue。

## 为什么这样不冲突

因为我们把它拆成层：

```text
purpose/schema = 规则层
source/pattern/claim/anti-pattern = 知识层
graph/health = 关系和质量层
API/context pack = 调用层
agent gbrain = 推理层
```

每一层职责不同，所以不会互相抢位置。

## 最大风险

最大风险不是设计冲突，而是过早工程化。

如果现在就做 App、API、图数据库，会把还没验证过的模板固化，后面改起来很痛。

## 当前判断

`llm_wiki` 的设计是可融合的，而且是目前看到的最高工程信号之一。

但我们的融合方式是：吸收机制，暂不吸收完整产品形态。
