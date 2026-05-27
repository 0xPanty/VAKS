---
type: summary
status: summary-draft
created: 2026-05-27
updated: 2026-05-27
sources:
  - "[[2026-05-27-obsidian-para-source]]"
topics:
  - PARA
  - Obsidian
  - memory-tier
  - dev-context
  - actionability
verification_status: single-source
evidence_level: secondary
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-03
relations:
  - target: "[[MEMORY_TIER]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-obsidian-para-source]]"
    rationale: "PARA's actionability and archive-first migration suggest activation rules for base memory tiering."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-obsidian-para-source]]"
    rationale: "PARA project/area/resource/archive flows map cleanly to dev context core/support/cold references, while risk remains our added layer."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[para-folder-taxonomy-as-truth-layer]]"
    type: risk_of
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-obsidian-para-source]]"
    rationale: "Directly adopting PARA folders as the truth layer would collapse actionability routing into verification schema."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - summary
  - obsidian
  - para
  - memory-tier
  - dev-context
---

# Obsidian PARA Architecture Review

## AI-readable preamble

This review treats `byarbrough/obsidian-para` as a vault-template source, not as a runtime implementation.

Its useful alpha for our system is actionability-based activation and archive-first lazy reactivation.

It should not replace the verified-action truth layer, review gate, provenance model, or risk layer.

## 它解决什么问题

`obsidian-para` 解决的是个人资料库的行动性组织问题：

```text
What should I work on?
What am I responsible for?
What topic do I keep around?
What can leave the active workspace?
```

它不解决：

```text
Which claim is true?
Which source is reliable?
Which decision is field-tested?
Which relation is reviewed?
```

所以它适合进入本系统的 activation / lifecycle layer，不适合进入 truth layer。

## 核心设计

仓库把 vault 控制成四个顶层类别：

```text
1. Projects
2. Areas
3. Resources
4. Archive
```

这四类不是主题标签，而是行动状态：

```text
Projects:
  有目标和时限的离散工作。

Areas:
  需要长期维持标准的责任域。

Resources:
  持续感兴趣但尚未转成行动的主题。

Archive:
  暂不活跃，但未来可能复用的历史材料。
```

关键操作逻辑：

```text
put information where it is most likely needed next
```

这条规则比“按主题归类”更接近我们需要的 `activation_reason`。

## Source / Code Extraction

仓库结构非常轻：

```text
README.md
1. Projects/README.md
2. Areas/README.md
3. Resources/README.md
4. Archive/README.md
templates/goal_template.md
templates/resource_template.md
.obsidian/templates.json
```

没有插件代码、索引器、Dataview 脚本或自动化运行时。

因此可拔取的是：

```text
folder grammar
lifecycle transition rules
minimal templates
migration method
archive reactivation logic
```

而不是：

```text
runtime API
compiler strategy
query engine
lint implementation
agent protocol
```

## 值得提炼的模式

1. `actionability-based-memory-routing`

资料不应该只按主题存放或召回，而应回答：

```text
Where will this likely be needed next?
```

这直接支持 `scope_key` 和 `activation_reason`。

2. `archive-first-lazy-reactivation`

旧资料不需要先全部精细整理。先入 archive/cold，实际使用时再 reheat。

这能降低资料库迁移和冷启动成本，也能用真实使用行为发现高价值材料。

3. `project-goal-gate`

项目层需要 goal / deadline / next action。没有目标的内容不应自动进入当前开发 Core。

这个点应进入 `DEV_CONTEXT.md` 的 Core 选择规则。

4. `lifecycle-transition-review`

Project 完成后，应扫描其中可复用的材料：

```text
reusable pattern -> warm
ongoing responsibility -> area/support
one-off residue -> cold/archive
```

这能补强 dev context 的 Exit 阶段。

## 对当前项目的适配点

### 适合吸收

```text
memory_tier:
  hot/warm/cold should reflect likely next use, not abstract importance.

DEV_CONTEXT:
  Core should require a project/task goal and stop condition.

Exit flow:
  finished project contexts should be scanned for reusable warm patterns before archiving.

Cold strategy:
  cold is dormant intellectual capital, not junk.
```

### 不适合吸收

```text
top-level PARA folders as vault root
manual moving as primary automation
PARA category as truth status
archive as reliability signal
four-folder limit as verified-action schema limit
```

## 对大框架设计防线的意义

PARA 提供了一个清晰的防线：

```text
行动性路由可以很简单。
可信知识层不能因此变简单到没有证据。
```

也就是说：

```text
PARA-like routing:
  decides what to look at next.

Verified-action schema:
  decides what can be trusted and acted on.
```

如果二者混在一起，资料库会退化成“文件夹整理系统”，失去 verified knowledge / action basis 的主目标。

## 冷热记忆相关 alpha

最有价值的 alpha 是：

```text
lazy reactivation by use
```

不要预先整理所有旧资料，也不要把所有资料手动分层。

更好的规则：

```text
default old material to cold
when a project/query needs it, bring it into a scoped dev context
if it proves reusable, write back as warm
if it becomes current work, mark scoped hot
after the project ends, cool it deliberately
```

这比“全库一次性冷热分类”更符合实际使用，也更适合 agent 调取。

## 融合判断

结论：`adapt`

理由：

```text
吸收 PARA 的 actionability / lifecycle / archive-first migration。
拒绝 PARA folder taxonomy 作为 verified-action truth layer。
用 metadata 和 dev context pack 承载它，不做顶层目录重构。
```

下一步：

```text
把 lazy reactivation、where-needed-next、project goal gate、exit scan 写入 MEMORY_TIER.md / DEV_CONTEXT.md。
```
