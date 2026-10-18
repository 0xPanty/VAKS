---
type: pro_review_prompt
status: ready-to-upload
created_at: 2026-06-05
project: verified-action-knowledge-system
truth_boundary: prompt only
---

# Prompt to Pro

请复核这个 VAKS / 资料库 的候选流程试点包。

## 背景

我们持续 intake 外部视频、论文、开源库。之前每条资料卡里经常写：

```text
适合 VAKS / 资料库：
不适合 VAKS / 资料库：
```

现在我们担心这种写法会把外部资料里的知识点过早绑定到 VAKS 项目。未来如果有其他项目，也可能复用同样的候选方法；而一个点不适合 VAKS，不代表不适合别的项目。

所以我们试了一个三层结构：

```text
Source Card
  记录资料本身。

Candidate Pattern Bank
  把明显可能跨项目复用的机制抽成候选方法。

Project Borrowing Ledger
  每个具体项目单独记录：借不借、借到哪里、为什么、要过什么 gate。
```

人话版：

```text
资料分开存；
方法单独抽；
项目自己记借不借。
```

## 当前试点

我们已经在 `outputs/review` 里做了一个 candidate-only 试点：

```text
source_cards/
candidate_pattern_bank/
project_borrowing_ledgers/
```

并拿 4 个本地已蒸馏材料测试：

```text
1. RAG 翻车短视频
2. RAGLab 视觉工作台视频
3. miniopenclaw repo
4. RF-Mem paper
```

请重点看：

```text
pilot/2026-06-05-cross-project-borrowing-pilot-implementation.md
pilot/2026-06-05-cross-project-borrowing-4-item-pilot-test.md
candidate_pattern_bank/INDEX.md
project_borrowing_ledgers/VAKS.md
source_cards/2026-06-04-external-intake-source-routing-ledger.md
```

## 请重点回答

### 1. 总体判断

这套三层结构是否合理？

```text
Source Card
-> Candidate Pattern Bank
-> Project Borrowing Ledger
```

它是否比“每条资料卡都写适合 VAKS / 不适合 VAKS”更干净？

### 2. Source Card 是否需要写项目路由

我们现在犹豫：

```text
source card / source routing 里要不要写“可能路由到哪个项目”？
```

请判断哪种更好：

方案 A：

```text
Source Card 只写可迁移候选点和不可泛化点。
不写具体项目。
项目借不借全部写到 Project Borrowing Ledger。
```

方案 B：

```text
Source Card 可以写轻量 project_routes_optional。
例如：possible route to VAKS borrowing ledger。
但不能写项目 verdict。
```

方案 C：

```text
Source Card 完全不写项目路由。
另用 Source Routing Ledger 做中间 overlay。
```

请给推荐，并说明原因。

### 3. 这套试点是否太重

现在有：

```text
source routing overlay
10 个 candidate patterns
1 个 VAKS borrowing ledger
1 个 4-item pilot test
```

这是否太重？

哪些应该保留？

哪些应该合并、parked 或删除？

### 4. Candidate Pattern Bank 是否有污染风险

请检查它是否可能变成：

- 漂亮名词目录；
- AI 总结真理库；
- 隐形 architecture decision；
- 重复 source card；
- 被来源数量误导的“假支持系统”。

请给具体防污染建议。

### 5. VAKS Borrowing Ledger 是否合适

请检查：

```text
watch / prototype / adapt / reject / superseded
```

这些 disposition 是否合适？

`reviewed_at / reviewer / review_note` 是否应该作为正交元数据，而不是状态？

VAKS ledger 是否有长成 ADR 或 action basis 的风险？

### 6. 主线合并建议

如果你认为这个试点有价值，请明确区分：

可以合并到主线规则的内容：

```text
例如：以后 source card 少写“适合 VAKS / 不适合 VAKS”，改写“可迁移候选点 / 不可泛化点 / 项目路由建议”。
```

必须继续留在 `outputs/review` 观察的内容：

```text
例如：具体 candidate patterns、VAKS ledger 的 watch/adapt 状态。
```

绝对不应该合并的内容：

```text
例如：把 Pattern Bank 当 reviewed knowledge；把 Borrowing Ledger 当 architecture decision。
```

### 7. 建议的最小下一步

请给一个最小下一步，不要大改主架构。

例如：

```text
只改 video/repo source template 的一小段？
只保留 source routing overlay？
只用 VAKS.md 作为项目账本继续观察？
继续跑 10 条新资料再评估？
```

## 边界

请严格保持：

```text
Source Card != truth
Candidate Pattern != reviewed knowledge
Project Borrowing Ledger != ADR / architecture decision
retrieval / rerank / GraphRAG / dashboard / feedback != truth confidence
source count / project count / reuse count != evidence support
```

VAKS 只允许后续 evidence-aware review / project decision 之后，才进入 reviewed knowledge、reviewed relation、main architecture 或 action basis。

