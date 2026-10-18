---
type: obsidian_usage_supplement
status: sandbox_usage_note
created_at: 2026-06-06
updated_at: 2026-06-06
scope: Project Overlay / 项目借鉴清单
truth_boundary: 使用层补充；不是主线架构；不是 schema；不是 reviewed knowledge；不是 action basis
---

# Project Overlay 使用层补充

## 一句话

Project Overlay 不是新的主架构对象。

它现在的定位是：

```text
给当前项目看的借鉴清单。
```

人话：

```text
通用知识点保持干净。
项目自己有一张清单，记录当前项目想借哪部分、不能误借哪部分、该去哪里看。
```

## 当前先这么用

在完整 Obsidian 使用手册写完之前，先按这个轻规则使用：

```text
一个项目 = 一张 Project Overlay / 借鉴清单
```

清单里每条只回答四个问题：

```text
1. 指向哪个通用知识点？
2. 当前项目想借哪部分？
3. 当前项目不能误借哪部分？
4. 当前项目里大概该去哪里看？
```

## 最小字段

推荐每条 entry 至少写：

```text
kp_ref
stance
borrow_scope
updated_at
```

可选写：

```text
non_borrow_scope
target_hint
```

这里的 `target_hint` 只是路标，不是证据。

## 借鉴序位

为了让以后打开蒸馏记录时一眼看到“最值得借的东西”，可以在 source
蒸馏、repo 蒸馏、article 蒸馏、Project Overlay 里加一个轻量借鉴序位。

推荐写法：

```yaml
borrow_value: strong | medium | low | avoid
borrow_order:
  - P1: 最强借鉴，优先看
  - P2: 有用但需要改造
  - P3: 可观察 / 可备用
avoid:
  - 明确不要吸收的坑
```

人话：

```text
P1 = 最值得借，放前面
P2 = 有用，但要改造或加边界
P3 = 先观察，以后可能用
avoid = 明确不借，防止误吸收
```

这只是阅读排序和借鉴优先级，不表示：

```text
truth confidence
reviewed knowledge
architecture adopted
promotion status
action basis
```

如果某个 P1 借鉴项未来真的要进入：

```text
主架构
decision
promotion
action basis
```

仍然必须切回对应的 review / v0.2.13 流程。`borrow_order` 只能帮人先看重点，
不能替代证据、复核或落地主张。

## stance 只是临时阅读立场

推荐临时使用：

```text
watch
partial
avoid
defer
```

它们只表示当前项目怎么看这个知识点，不表示：

```text
已采用
已批准
已落地
最终结论
行动依据
```

## 知识点本体不要贴项目标签

不要这样：

```text
通用知识点.md 里写 #Misa #VAKS #已借鉴
```

应该这样：

```text
MISA.md 里引用这个通用知识点
VAKS.md 里也可以引用同一个通用知识点
```

这样同一个知识点可以被多个项目借，但项目判断不会互相污染。

## 当前已有沙盒样例

轻量落地包：

```text
outputs/review/project-overlay-lightweight-landing-test-2026-06-06/
```

核心样例：

```text
project_overlays/MISA.md
project_overlays/VAKS.md
protocol/PROJECT_OVERLAY_ONE_PAGE_PROTOCOL.md
```

Pro 复核结论：

```text
sandbox closeout: 可以
sandbox use: 可以
mainline: 不可以
next gate: real blind non-author pass
```

## 使用反馈也要记录

这份手册还是初版，所以使用过程中遇到的问题要主动留下反馈。

人话：

```text
只要实际用起来有不顺手、看不懂、容易误会、重复劳动、字段漏写、
同步麻烦、索引难找、tag 不准、入口分级拿不准、路径冲突、脚本缺口、
Codex 操作别扭、小 bug、小冲突，都应该记录。
```

推荐先记到：

```text
outputs/feedback/
```

例如：

```text
outputs/feedback/2026-06-06-retrieval-source-intake-operational-feedback.md
```

最小记录内容：

```text
1. 当时在做什么？
2. 哪一步顺手？
3. 哪一步不顺手？
4. 容易误读成什么？
5. 影响什么：usefulness / scope_fit / activation / workflow？
6. 不影响什么：truth / verification_status / source_reliability？
7. 可能怎么优化：手册、skill、script、lint、view、index？
```

记录时要保留边界：

```text
feedback = 使用经验 / workflow 信号 / 未来优化输入
feedback != truth
feedback != reviewed knowledge
feedback != decision
feedback != action basis
```

如果是正反馈：

```text
说明哪里真的帮到了工作流，但不要提升 truth confidence。
```

如果是负反馈：

```text
说明哪里造成摩擦或误读风险；必要时创建 review pressure，
但不要自动改 schema、主线架构或 reviewed knowledge。
```

如果是小 bug：

```text
先记录可复现现象、涉及文件、期望行为、实际行为、临时绕法。
等后续 toolchain / Codex skill / lint 设计时再统一处理。
```

这条规则的目的不是增加负担，而是让 Obsidian 使用手册从真实使用中长出来。

## 不能用它做什么

Project Overlay 不能当：

```text
truth
ADR
reviewed knowledge
action basis
project decision
schema
mainline object model
```

一旦要用某条 entry 支持：

```text
行动
promotion
architecture absorption
decision
risk-sensitive answer
```

就停止使用 overlay，切回 v0.2.13。

## closeout 先按 drain 理解

项目结束时，live overlay 不要一直飘着。

先按这个轻规则处理：

```text
真的有跨项目参考价值 -> scoped candidate experience / follow-up note
真的发现某 scope 下不能借 -> scoped candidate boundary / follow-up note
没结论但留历史 -> archive
重复、低值、误导 -> delete + tombstone
```

这不是 lifecycle 状态机，只是清场规则。

## 未来完整手册再写什么

等整体架构更完整后，再写正式 Obsidian 使用手册，覆盖：

```text
Project Overlay 文件放哪里
怎样从知识点跳到项目清单
怎样 closeout
怎样做新窗口恢复
怎样做 Codex skill
怎样做 blind non-author pass
```

现在这份只是过渡补充，目的是让未来 Codex 不会把 Project Overlay
误读成主线知识系统。
