---
type: architecture_alignment_note
status: candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: light-medium-heavy-source-to-action-flow
truth_boundary: alignment note; not reviewed knowledge; not action basis
write_scope: outputs/review only
---

# v0.2.13 Light / Medium / Heavy Alignment

## 说人话

VAKS 这套东西本来就应该按轻 / 中 / 重来理解。

不要再把它讲成一堆吓人的系统名。最简单就是：

```text
轻 = 能搜到
中 = 能参考
重 = 能拿来做决定
```

## 轻：资料备案和可检索

轻处理解决的是：

```text
这份资料是什么？
以后能不能搜到？
里面大概有什么可能有用的点？
有什么来源自身限制？
```

对应现在的构件：

```text
Source Card
Source Routing Overlay
candidate points
source-bound constraints
```

轻层可以记录：

```text
source identity
URL / file / transcript / anchor
candidate comprehension
candidate points
transferable hints
non-generalizable constraints
source family / de-dup hint
```

轻层不能做：

```text
项目采纳判断
truth confidence
action readiness
architecture decision
candidate pattern promotion
```

一句话：

```text
轻层让资料可见、可搜、可回源，但不让它变成知识或决定。
```

## 中：通用候选知识点和项目开发区

中处理解决的是：

```text
这批资料里有没有可复用的机制？
这个机制对当前项目能不能借？
借到哪里？
为什么适合或不适合？
升级前还差什么 gate？
```

对应现在的构件：

```text
Candidate Pattern Bank
Project Borrowing Ledger / Project Borrowing Workspace
```

中层可以记录：

```text
通用候选点 / candidate pattern
problem addressed
mechanism
applicability
non-goals
risk of overreach
project disposition: watch / prototype / adapt / reject for now
target locus
required gates before promotion
```

中层不能做：

```text
把 candidate pattern 当 reviewed knowledge
把 project borrowing 当 ADR
把 adapt 当 architecture adopted
把 reuse count / source count 当 support strength
```

一句话：

```text
中层是项目开发区 / 借鉴目录，不是正式决策区。
```

## 重：吸收闸门和行动依据

重处理只在少数情况打开：

```text
promotion
significant decision
action basis
risk-sensitive answer
strong relation promotion
explicit "is this enough to act / decide / promote?" question
```

对应现在的构件：

```text
Evidence-Aware Review
Evidence Sufficiency Gate
Action Basis
v0.2.13 non-circular warrant rule
```

重层必须说明：

```text
claim
point-specific anchored evidence
non-circular warrant
scope / assumptions
known challenges / gaps
current residual review status
```

重层要防止：

```text
evidence list pretending to be action basis
source family repetition pretending to be independent support
tool / vendor / diagram / source count / confidence label pretending to be support
candidate borrowing pretending to be architecture decision
```

一句话：

```text
重层不是日常 intake；它只管从“可参考”升级到“可行动”的那一刻。
```

## Correct Flow

健康状态应该是：

```text
很多资料停在轻
少数点进入中
极少数进入重
```

也就是：

```text
raw source / source card
-> optional source routing overlay
-> candidate points / candidate patterns when warranted
-> project borrowing workspace when project fit matters
-> promotion-time review packet with explicit non-circular warrant
```

## What v0.2.13 Is

v0.2.13 不是轻层规则。

v0.2.13 不是中层规则。

v0.2.13 是重层最后一公里规则：

```text
Evidence is not enough; show the non-circular warrant.
```

它只在“要行动 / 要决策 / 要 promotion”时出现。

## What To Do Now

Current practical posture:

```text
keep main architecture minimal rule
keep outputs/review as experiment/history
do not create a new stable project workspace yet
do not rename directories yet
do not create a new schema object
do not create a new template
do not make every source become a pattern
```

Next real validation:

```text
1. 双项目复用验证
2. 不升级验证
3. 真实 promotion/action-basis 验证
```

If those pass, then consider a stable long-term name such as:

```text
project borrowing workspace
project reference workspace
项目开发区台账
项目借鉴目录
```

But that is a later directory / naming decision, not today's architecture change.
