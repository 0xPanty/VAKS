# Pro Review Prompt

我把 Codex 最新一轮 `audit shell v1` output-level oracle hardening + alpha bakeoff 打包给你了。请不要只验收数字，也不要默认顺着 Codex 的结论走。

请重点复核：

## A. Output-Level Oracle 是否真的补上了你上次批评的问题

上一轮你的核心批评是：文件拆开了，但判定语义仍然同源。这轮声称改成只看最终 front/back/full artifact。

请检查：

```text
state 是否真的从 rendered artifact 判定
false-lite 是否真的从输出是否打开 full audit 判定
review_due 是否真的看输出中是否显式保留
authority leakage 是否黑盒扫描 rendered text
authority boundary 是否在输出级可见
anchor/jump-back 是否真的解析 pointer 到 raw_sources marker
front face 行数是否来自实际 rendered front
grouping 是否同时测 can_group recall 和 severe over-grouping
```

## B. 最合理 Alpha 是否真的是 Guarded Stack

Codex 的结论是：最合理的不是单项 alpha，而是 guarded stack：

```text
trigger-held deep packet retention
+ sparse provenance mention pointer
+ folded recurrence card
+ versioned fingerprint grouping
+ categorical feedback revision strip
```

请判断：

```text
这个组合是不是最小必要组合？
是否有某个 alpha 可以删掉？
是否有某个 alpha 仍然只是“看起来合理”，但测试没有打穿？
trigger-held deep packet retention 是否确实是主发动机？
categorical feedback revision strip 是否应只是 wording constraint，而不是主 alpha？
```

## C. 这轮有没有新的 Overclaim

请特别找：

```text
是否仍然存在 semantic self-proof
是否存在过度 curated 的 case mix
front reduction 是否仍然高估真实工作流收益
burden units 是否仍然人造
grouping recall 是否过于依赖手写字段
anchor resolve 是否仍只是 marker lookup，不是真实 UI jump-back
```

## D. 是否足够进入 480 Real-Data Paired Pilot

请给明确判断：

```text
1. 直接进入 480
2. 再补一轮 output-level adversarial patch
3. 缩小 alpha 组合后再测
4. 停止 audit shell v1 路线
```

如果不能进 480，请给出最关键的一刀。

## E. 哪些东西仍然不能进主库

请再次列出不能进入主库 truth core / SCHEMA / operation convention 的内容。

当前默认边界：

```text
主库不改
SCHEMA 不动
shell / grouping / dashboard / feedback / tests 不能成为 truth authority
source count / lineage / group count 不能冒充 source independence
provenance 不是 support
support 不是 truth
reviewed knowledge 也不自动 action-ready
```
