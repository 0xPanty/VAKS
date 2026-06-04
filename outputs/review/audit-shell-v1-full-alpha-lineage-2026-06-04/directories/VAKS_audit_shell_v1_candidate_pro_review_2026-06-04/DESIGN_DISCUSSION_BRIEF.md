# Design Discussion Brief

日期：2026-06-04

## 当前立场

强压测试已经说明：

```text
audit shell v1 方向成立。
完整 shell_core 有价值。
不要先降性能。
不要先砍成保守小清单。
```

但它也不应该直接变成正式主库规则。下一步应该讨论设计，而不是继续纠结“有没有价值”。

## 下一步讨论要解决的问题

### 1. 前脸多短才够

目标不是越详细越好，而是 operator 一眼能做动作：

```text
轻量保存
复核
阻塞
折叠
重开
```

设计问题：哪些 slot 必须第一屏显示？哪些 drilldown 可以折叠？

### 2. landing class 怎么说人话

必须让 operator 明白：

```text
source landing 不是 evidence landing
claim landing 不是 evidence landing
context landing 更不是 evidence landing
transcript landing 只是 raw text
diagnostic landing 只是诊断
```

设计问题：中文 wording 怎么短又不误导？

### 3. `for_review` 量大怎么处理

强压里 139 条 `for_review`。这是合理的，因为主库有很多 candidate/draft/derived/stale 材料。

设计问题：如何不默认打开 recurrence/grouping，也能让 review queue 不吓人？

候选办法：

```text
按风险原因分组显示，但不把 group count 当 support。
默认只显示 unresolved first。
resolved_folded 默认收起。
```

### 4. 视频 / ASR 怎么专门呈现

强压证明视频链路必须拆开：

```text
source card
metadata json
segments
transcript
candidate points
reviewed knowledge
```

设计问题：视频前脸是否需要专门的 ASR boundary slot？

### 5. click-back 怎么测

下一阶段如果要继续上证据，不是再扫更多文件，而是测：

```text
operator 能不能点回 source / record / evidence
点回是不是落到正确位置
弱 landing 有没有被误当 evidence
```

但 click-back 成功也只是操作可用性，不是 truth。

## 推荐下一步动作

先做一个 sandbox operator surface prototype，不写主库：

```text
输入：PRESSURE_TEST_RESULTS.csv
输出：30 条中文 operator front-face prototype
覆盖：ordinary / for_review / blocking / resolved_folded / regressed
目标：看前脸是否短、清楚、能行动
```

如果 prototype 看着顺，再讨论是否写入主库候选 operation convention。

## 不做什么

暂时不做：

- 不改 `SCHEMA.md`。
- 不正式 adoption。
- 不打开 recurrence/grouping 默认。
- 不把 audit shell 变成用户前台 card。
- 不把测试结果当 truth authority。

