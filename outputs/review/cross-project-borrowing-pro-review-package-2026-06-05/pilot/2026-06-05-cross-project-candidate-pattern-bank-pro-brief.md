---
type: review_brief
status: candidate-proposal
title: Cross-Project Candidate Pattern Bank and Project Borrowing Ledger
created_at: 2026-06-05
created_by: Codex
project: verified-action-knowledge-system
scope: external-reference-distillation
formalization_status: candidate-only
review_target: Pro / frontier design research
truth_boundary: not reviewed knowledge, not architecture decision, not action basis
---

# Cross-Project Candidate Pattern Bank / Project Borrowing Ledger

## 背景

当前 VAKS / 资料库正在持续 intake 外部视频、论文、仓库和设计材料。现有做法是：每条外部资料里都会写“对资料库有什么可借鉴 / 不能借鉴”。这在早期是合理的，因为当前唯一明确使用者就是 VAKS。

但长期看，这种写法有一个问题：外部资料被过早绑定到“资料库项目”。同一个知识点或设计模式，未来可能也适用于其他项目；反过来，一个点“不适合 VAKS”，并不代表它不适合别的项目。

因此需要考虑把“外部知识点”和“项目借鉴判断”拆开。

## 核心想法

把现有外部资料蒸馏拆成三层：

```text
1. Source Card
   记录这条视频 / repo / paper 原本说了什么。

2. Candidate Pattern Bank
   从一个或多个来源中抽出可迁移的候选知识点 / 候选设计模式。

3. Project Borrowing Ledger
   某个具体项目单独记录：借了哪些候选点，没借哪些，借到哪里，为什么。
```

一句话：

```text
source 负责出处；
candidate pattern 负责通用抽象；
project ledger 负责项目化吸收。
```

## 为什么这样更科学

### 1. 防止项目语境污染知识点

知识点本身应保持独立。例如：

```text
file-first-agent-workbench
```

它本身不是“适合资料库”或“不适合资料库”，而是一个候选模式。不同项目可以有不同判断：

```text
VAKS:
  只借鉴为 activation / dev context / workbench，不进入 truth。

AI 写作助手:
  可能可以直接作为素材库和创作记忆层。

企业合规系统:
  可能因为权限、审计和敏感信息风险而暂不借。
```

所以“适合 / 不适合”应写在项目 ledger 里，而不是写死在知识点卡里。

### 2. 让外部资料变成可复用资产

如果每条资料都只写“对 VAKS 有什么用”，未来其他项目复用时还要重新读一遍原资料。更好的方式是把可迁移点先沉淀成通用候选模式，再让项目按需引用。

### 3. 更符合 VAKS 的候选边界

外部资料只能产生 candidate points / candidate patterns。项目是否采用，需要另走 project fit / review / decision。

这能继续保护现有边界：

```text
source provenance != support
candidate pattern != reviewed knowledge
project borrowing != architecture decision
project feedback != truth confidence
```

### 4. 更方便做 Direction Review

后续不再只问“某个视频对 VAKS 有没有用”，而是问：

- 哪些候选模式在多个来源中反复出现？
- 哪些模式跨项目可迁移？
- 哪些模式只适合特定项目？
- 哪些模式有强污染风险？
- 哪些模式值得进入某个项目的 review / prototype / decision？

## 建议的文件分区

这是候选结构，不是已采纳目录。

```text
raw/
  videos/
  repos/
  papers/
    # source cards stay here

wiki/candidate-patterns/
  file-first-agent-workbench.md
  source-structure-first-rag.md
  retrieval-is-activation.md
  prompt-components-as-files.md
  skills-as-markdown.md

wiki/projects/vaks/
  borrowing-ledger.md
  rejected-borrowings.md
  direction-review-rag.md

wiki/projects/<future-project>/
  borrowing-ledger.md
  rejected-borrowings.md
  project-fit-review.md
```

## Candidate Pattern 卡片形状

示例：

```yaml
type: candidate_pattern
status: candidate
pattern_id: file-first-agent-workbench
title: File-first Agent Workbench
source_refs:
  - raw/repos/2026-06-04-langchain-miniopenclaw-source.md
  - raw/videos/...
abstraction_level: reusable_pattern
pattern_family:
  - agent-workbench
  - local-memory
  - context-pack
borrowable_parts:
  - Markdown / file as visible long-term source
  - index as rebuildable cache
  - prompt / skill / memory inspector
risks:
  - agent memory contamination
  - retrieval-as-truth confusion
  - permission and tool-safety risk
do_not_generalize:
  - file-first does not mean every project should be local-file-only
  - memory visibility does not make memory reviewed truth
review_state: candidate
promotion_state: none
```

正文应回答：

- 这个模式是什么？
- 它从哪些来源抽象出来？
- 哪些部分可迁移？
- 哪些部分不能泛化？
- 适用前提是什么？
- 主要风险是什么？
- 哪些项目已经引用过它？
- 目前仍然缺什么证据或验证？

## Project Borrowing Ledger 形状

示例：

```yaml
type: project_borrowing_ledger
project: VAKS
status: candidate-ledger
entries:
  - pattern_ref: wiki/candidate-patterns/file-first-agent-workbench.md
    borrowing_status: watch
    use_as:
      - activation
      - dev_context
      - workbench
    target_surfaces:
      - MEMORY_TIER.md
      - future context-pack viewer
    borrowed_parts:
      - file-first memory surface
      - inspector
      - rebuildable index cache
    not_borrowing:
      - memory directly as truth
      - terminal tool with simple blacklist
      - unreviewed skill writes
    reason:
      - VAKS needs visible context, but reviewed knowledge must stay protected.
    required_gate_before_adoption:
      - evidence-aware review
      - tool-safety review
      - prototype validation
    decision_ref:
```

关键点：

```text
Borrowing Ledger 是项目适配记录，不是 reviewed truth。
它可以推动 review / prototype / decision，但不能绕过 review。
```

## 对当前 video / repo intake 的影响

以后单条资料卡应少写：

```text
适合资料库：
不适合资料库：
```

改成：

```text
可迁移候选点：
不可泛化点：
风险：
可能关联的 candidate patterns：
建议写入哪些 project borrowing ledger：
```

如果当前项目就是 VAKS，可以在 source card 里只写一句轻量 routing：

```text
VAKS routing: possible fit for activation / workbench; record in VAKS borrowing ledger if later reviewed.
```

不要在每条 source card 里展开完整 VAKS 架构判断。

## 防污染规则

1. Source card 不写成 adoption decision。
2. Candidate pattern 不写成 universal truth。
3. Project borrowing ledger 不写成 architecture decision。
4. Direction Review 只输出设计压力和候选优先级，不输出 truth confidence。
5. 只有经过项目自己的 review / decision，才允许进入主架构或 action basis。
6. 一个项目采用某模式，不代表其他项目自动采用。
7. 一个项目反馈“好用”，只改善 usefulness / scope fit，不改变原始资料 truth。

## 给 Pro 的调研 brief

请调研：在前沿知识管理、软件架构、AI agent memory、RAG / GraphRAG、research workspace、design system、ADR / engineering knowledge base 中，是否已有类似的三层或多层设计：

```text
source record
-> reusable candidate pattern / reusable insight
-> project-specific adoption / borrowing / fit ledger
```

重点不是找名字完全一样的系统，而是找有没有类似分层思想。

### 请回答的问题

1. 有没有系统明确区分：
   - 原始来源 / source note
   - 可复用模式 / insight / pattern / principle
   - 具体项目采用记录 / decision / fit assessment

2. 这些系统如何避免：
   - 把来源材料直接变成通用真理
   - 把通用模式直接变成项目决策
   - 把某项目的采用经验污染其他项目
   - 把检索、评分、dashboard、使用反馈误当 truth

3. 有哪些类似做法值得参考？
   - architecture decision records / ADR
   - design pattern libraries
   - engineering knowledge bases
   - research knowledge graph / literature review systems
   - agent memory systems
   - RAG / GraphRAG workbench
   - design-system token / component adoption logs
   - open-source project review / dependency adoption records

4. 有哪些反例或失败模式？
   - pattern library 变成没人用的抽象目录
   - adoption ledger 变成重复劳动
   - source note、pattern、decision 三者边界混乱
   - 项目适配记录过重，阻碍日常 intake
   - AI 自动总结把候选点写得像已验证事实

5. 对 VAKS 的建议是什么？
   - 是否应该引入 Candidate Pattern Bank？
   - 是否应该引入 Project Borrowing Ledger？
   - 目录放在 `wiki/candidate-patterns/` 和 `wiki/projects/<project>/` 是否合理？
   - source card 是否应该减少“适合资料库 / 不适合资料库”，改成“可迁移候选点 / 不可泛化点 / project ledger routing”？
   - 第一版最小实现应该多轻？

### Pro 输出格式建议

请按下面格式输出：

```text
1. Verdict
   - 是否有类似前沿设计？
   - 我们的三层结构是否方向合理？

2. Comparable Systems / Practices
   - 系统 / 实践名称
   - 它怎么分层
   - 和我们方案相似处
   - 和我们方案不同处
   - 可借鉴点
   - 不应借鉴点

3. Failure Modes
   - 可能乱套的位置
   - 如何防污染
   - 哪些字段或 gate 必须有

4. Recommended Minimal VAKS Implementation
   - 只建议最小目录和最小字段
   - 不要把它做成新主架构
   - 不要增加 heavy workflow

5. Suggested Patch Scope
   - 哪些现有文档需要改
   - 哪些不该改
   - 哪些只放 outputs/review 继续观察
```

### Pro 调研边界

- 不要把“类似系统存在”当作采用证据。
- 不要把流行度、star 数、论文引用数、dashboard 指标当 truth confidence。
- 不要建议自动 promotion。
- 不要把 Candidate Pattern Bank 变成 reviewed knowledge layer。
- 不要把 Project Borrowing Ledger 变成 action basis。
- 如果建议采用，只能建议为 candidate workflow / lightweight project-development surface。

## 当前建议

在 Pro 调研之前，先不要改主架构。

可以先把这件事视为一个候选方向：

```text
candidate direction:
  Separate external reusable candidate patterns from project-specific borrowing decisions.

expected benefit:
  Cross-project reuse without polluting source notes or VAKS-specific project decisions.

expected risk:
  More bookkeeping if overbuilt; candidate pattern bank may become abstract clutter.

minimum viable next step:
  Let Pro compare frontier practices and recommend a lightweight first version.
```

