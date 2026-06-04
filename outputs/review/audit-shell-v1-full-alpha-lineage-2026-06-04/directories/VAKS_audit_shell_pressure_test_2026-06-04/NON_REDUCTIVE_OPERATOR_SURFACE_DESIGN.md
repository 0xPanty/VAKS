# Audit Shell v1 Non-Reductive Operator Surface Design

日期：2026-06-04

状态：sandbox 设计底板，不是主库正式规则，不改 `SCHEMA.md`。

## 一句话

不要把 audit shell v1 先砍成保守小清单。强压结果说明它的价值就在完整分流：

```text
ordinary
for_review
blocking
resolved_folded
regressed
```

它应该被设计成 Codex / Pro / reviewer 的后台操作台，而不是用户前台 card，也不是 truth layer。

## 设计目标

让 operator 一眼知道：

- 这条资料能不能轻量收。
- 要不要复核。
- 有没有缺锚点 / 弱落点。
- 能不能作为答案或行动依据。
- 是不是旧入口、旧 package、旧 handoff。
- feedback / dashboard / test / lint / count / lineage 有没有被误当 authority。
- source / record / evidence drilldown 从哪里回去。

## 不降性能原则

这版设计必须保留：

| 能力 | 为什么不能砍 |
|---|---|
| `ordinary` | 保证普通入库不变成 paperwork。 |
| `for_review` | 承接 draft、derived、stale、weak landing、feedback bait 等中间风险。 |
| `blocking` | 缺锚点、flat transcript、binary snapshot、action-basis 风险必须挡住。 |
| `resolved_folded` | 旧 handoff、旧 decision、完成的 review 输出不能占默认注意力。 |
| `regressed` | 旧 package manifest、回归问题、过期入口要重新入队。 |
| landing class | 防止 claim/context/source/transcript 被误当 evidence landing。 |
| source-first drilldown | operator 必须能回到 source / record / evidence。 |
| targeted boundary reminder | 只在相关风险出现时提醒，不给每条 ordinary 灌全局免责声明。 |

## 后台状态机

```text
record enters operator surface
-> check hard trigger
-> if no hard trigger: ordinary front face
-> if action/answer/promotion use appears: open full audit
-> if review risk: for_review
-> if anchor/action/conflict hard risk: blocking
-> if old/resolved: resolved_folded
-> if old resolved item becomes misleading/stale/conflicted: regressed
```

## 中文前脸 slots

每条记录前脸不需要固定六行，但必须覆盖这些 slot：

| Slot | 作用 |
|---|---|
| 状态 | 人话状态，不直接把 raw label 扔给 operator。 |
| 一句话摘要 | 这条记录自己是什么。 |
| 风险原因 | 为什么轻量、复核、阻塞、折叠或重开。 |
| 锚点状态 | 可回源、缺失、弱、过期、移位、二进制不可直看。 |
| 处理建议 | 轻量保存、复核、打开 full audit、补锚点、折叠、重开。 |
| 定向边界提醒 | 只在 feedback / ASR / dashboard / count / lineage / weak landing 等风险出现时显示。 |
| 回源入口 | source / record / evidence / transcript segment / package / handoff。 |

## 推荐中文状态文案

| Machine state | 中文前脸 |
|---|---|
| `ordinary` | 普通资料，轻量处理 |
| `for_review` | 需要复核，先别当行动依据 |
| `blocking` | 暂不可行动，先修锚点或证据问题 |
| `resolved_folded` | 已是历史/已处理，默认折叠 |
| `regressed` | 旧问题/旧入口有回归，重新入队 |

## 强触发

这些情况必须加厚或阻塞：

- 用作行动依据。
- 用作主库规则 / schema / operation convention 依据。
- 缺 source URL / source URI / source anchor。
- flat transcript 被拿来当证据。
- zip snapshot / package zip 被拿来当证据。
- `next_review` 已过期且要用作当前规则。
- draft / candidate pattern 要被当 adopted rule。
- feedback 被当 truth change。
- dashboard / test / lint / count / lineage 被当 authority。
- 旧 handoff 或旧 package manifest 被当当前入口。
- derived QA / summary 被当 reviewed truth。

## 轻量路径

这些不要乱加厚：

- 普通 source card。
- video source card，前提是不直接用作证据。
- ASR / acquisition metadata JSON。
- template。
- concept explanation。
- current handoff pointer，前提是不改路线。
- completed review output，前提只是历史查看。

重点：轻量不是相信，轻量只是暂时不进入 full audit。

## 视频 / ASR 设计规则

强压结果支持这个拆分：

```text
video source card = ordinary provenance
ASR/acquisition json = ordinary diagnostic metadata
segments.md = for_review
transcript.txt = blocking before evidence/action use
```

这条很重要，不能砍。

视频记录前脸要明确：

```text
视频链接是 provenance。
字幕 / ASR 是 raw source text。
摘要是 candidate comprehension。
提取观点是 candidate point。
promotion 需要后续 evidence-aware review。
```

## Landing Class

推荐先保留这些 operator landing class：

| Landing | 人话解释 |
|---|---|
| `source_record_landing` | 只落到来源记录。能追溯，不等于证据支持。 |
| `claim_landing` | 落到 claim 文本。不是 evidence landing。 |
| `claim_relevant_context_landing` | 只落到相关上下文，比 claim landing 还弱。 |
| `evidence_landing` | 落到具体可支持/挑战的证据位置。 |
| `transcript_segment_landing` | 落到时间段 ASR 文本，需要 key entity check。 |
| `transcript_landing` | 长 transcript / flat text，不能直接行动。 |
| `diagnostic_landing` | 元数据、lint、test、dashboard、manifest，只能辅助。 |
| `handoff_landing` | 恢复入口，不是 schema 或 truth。 |
| `template_landing` | 模板，不是 record facts。 |
| `binary_snapshot_landing` | 有文件，但没有可读证据落点。 |

## 前脸提醒策略

不要每条 ordinary 都写全局免责声明。

只在命中风险时写定向提醒：

- ASR：`ASR 是 raw text，关键实体需复核。`
- feedback：`feedback 只影响 activation / review pressure，不改 truth。`
- dashboard/test/lint：`这是诊断，不是 readiness 或 truth。`
- count/lineage：`数量和重复出现不等于支持强度。`
- weak landing：`这是 claim/context/source landing，不是 evidence landing。`
- old handoff/package：`先确认最新入口。`

## 下一步设计问题

下一步不是问“要不要保留 shell”，而是问：

- operator 前脸怎么压到最短但不丢关键风险？
- 哪些 landing class 必须显示，哪些可以折叠？
- `for_review` 数量很大时怎么分组，但不默认打开 recurrence/grouping？
- Codex 和 Pro/reviewer 看到的前脸是否应该略有区别？
- 怎么记录 click-back 成功/失败，而不把 click-back 当 truth？

## 当前建议

```text
保留完整 shell_core。
不要先降性能。
不要先做正式主库规则。
先用这个设计底板讨论 operator surface。
```

