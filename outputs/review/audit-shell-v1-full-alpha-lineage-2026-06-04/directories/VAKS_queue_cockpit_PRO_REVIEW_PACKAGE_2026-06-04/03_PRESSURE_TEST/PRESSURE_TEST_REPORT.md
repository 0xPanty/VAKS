# VAKS Audit Shell v1 多维强压测试报告

日期：2026-06-04

Sandbox：`C:\Users\Administrator\Documents\VAKS_audit_shell_pressure_test_2026-06-04`

主库：`C:\Users\Administrator\Documents\资料库`，本轮只读。

注意：测试开始时主库已有 dirty 状态；测试过程中又出现了一组未跟踪视频入库文件。本轮没有改主库，没有 commit，只读取这些真实材料并把结果写入 sandbox。

## 这轮测试想证明什么

这轮不是把方案先裁小，也不是急着写草案。

这轮就是把 audit shell v1 保持完整能力，然后上强度：

```text
ordinary
for_review
blocking
resolved_folded
regressed
source / record / evidence drilldown
landing class
feedback boundary
dashboard/test/lint/count/lineage boundary
ASR/video boundary
old handoff / package stale handling
```

一句话：先看它在真实脏流量里扛不扛得住，再讨论怎么设计。

## 样本规模

这次扫了主库 282 个真实文件，覆盖：

- `raw/articles`
- `raw/videos`
- `raw/repos`
- `raw/papers`
- `wiki/claims`
- `wiki/patterns`
- `wiki/anti-patterns`
- `wiki/concepts`
- `wiki/decisions`
- `wiki/summaries`
- `wiki/projects`
- `outputs/review`
- `outputs/feedback`
- `outputs/qa`
- `00_handoff`
- `templates`

里面有普通 source、视频 ASR、segments、repo zip snapshot、package zip、旧 handoff、旧 package manifest、dashboard/lint/test/count 诱饵、feedback 诱饵、模板、派生 QA 和 summary。

## 总结果

| 项目 | 数量 |
|---|---:|
| 总样本 | 282 |
| `ordinary` | 113 |
| `for_review` | 139 |
| `blocking` | 11 |
| `regressed` | 2 |
| `resolved_folded` | 17 |
| 直接打开 full audit | 152 |
| false-lite | 0 |
| over-heavy | 0 |

解释成人话：

```text
该轻的没有被拖重。
该拦的没有漏放。
该复核的没有直接当可行动结论。
```

## 压力维度命中

| 风险维度 | 数量 |
|---|---:|
| source record 不能当 truth | 74 |
| count / lineage / repeated mention 不能当 support | 68 |
| draft / candidate pattern | 58 |
| derived summary / QA 不能当 truth | 42 |
| dashboard / test / lint authority bait | 40 |
| video source boundary | 29 |
| review_due / stale next_review | 25 |
| review output 不能当 authority | 20 |
| feedback truth bait | 18 |
| ASR / acquisition metadata diagnostic | 16 |
| template not record | 14 |
| old handoff stale | 10 |
| binary snapshot no visible evidence | 7 |
| action / schema claim | 6 |

## 最重要发现

### 1. 这个 shell 没有把普通入库压垮

113 条保持 `ordinary`。模板、概念、普通 source card、视频采集元数据、当前 handoff 指针，没有被强行 full audit。

这点很关键。说明它可以保留完整状态机，而不是每条资料都变成大审查。

### 2. ASR / 视频边界扛住了

这轮很适合打视频压力，因为主库里已经有多个视频 source。

结果是：

```text
video source card = ordinary provenance
ASR / acquisition json = ordinary diagnostic metadata
segments.md = for_review
transcript.txt = blocking
```

这很好。它没有把视频 URL、ASR、summary、segments、reviewed knowledge 混成一个东西。

### 3. 弱锚点和 zip 快照被挡住了

repo snapshot zip、package zip、flat transcript 都没有被当成 evidence landing。

这说明 shell 的“可回源”和“证据落点”区分有实际价值。

### 4. feedback 没有改 truth

feedback 相关内容被识别为 activation / review pressure，不是 truth confidence change。

这对主库很重要，因为用户纠偏、对话反馈、系统评估很容易被误写成事实变更。

### 5. dashboard / test / lint / count / lineage 没有变 authority

这轮有 40 条 dashboard/test/lint 权威诱饵，68 条 count/lineage/repeated mention 支持强度诱饵。

shell 的处理是对的：这些可以帮 operator 路由，但不能证明 support、readiness、confidence 或 truth。

### 6. 旧 handoff / 旧 package 能被处理

旧 handoff 被 `resolved_folded`，旧 package manifest 被 `regressed`。

这对 VAKS 很有用，因为恢复入口一旦错了，后面整个窗口都会跑偏。

## 先前疑似失败怎么处理

第一轮自动判定把 16 条视频 JSON 元数据也算成 false-lite 风险，这个判定太粗。

修正后规则是：

```text
ASR / acquisition metadata json = ordinary diagnostic
segments.md = for_review
transcript.txt = blocking before evidence/action use
```

修正后：

```text
false-lite = 0
over-heavy = 0
```

这不是美化结果，而是把“诊断元数据”和“拿来当证据的 ASR 文本”分开。这个区分本身就是下一步设计必须保留的能力。

## 结论

强压结果是：**扛住了，而且价值比上一轮 46 条模拟更明确。**

不是说可以立刻正式 adoption；但可以很明确地说：

```text
不要先降性能。
不要先裁成很小的保守版。
完整 shell_core 分流能力应该保留。
下一步应该讨论怎么设计得顺手，而不是先砍功能。
```

我的判断：

```text
方向：强正向
价值：高
压力表现：过关
普通入库：没有被拖垮
风险拦截：明显有效
下一步：基于强压结果讨论设计，而不是先写收窄草案
```

