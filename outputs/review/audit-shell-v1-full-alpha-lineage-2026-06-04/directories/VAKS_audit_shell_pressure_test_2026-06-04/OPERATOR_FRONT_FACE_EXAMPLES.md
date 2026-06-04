# Operator Front-Face Examples

日期：2026-06-04

这些是根据强压测试抽出的前脸示例。它们是 sandbox 设计样例，不是主库记录。

## 1. 普通 source card

路径：`raw/articles/2026-04-04-karpathy-llm-wiki-source.md`

```text
状态：普通资料，轻量处理。
一句话：Karpathy LLM Wiki 来源记录，适合作为背景 source。
风险原因：当前只是 source record，不直接作为 truth 或 action support。
锚点状态：source URL 可回源。
处理建议：轻量保存；如果要用它支撑规则或行动，再打开 full audit。
回源入口：source record / source URL。
```

## 2. 视频 source card

路径：`raw/videos/2026-06-04-bilibili-obsidian-usage-barriers-source.md`

```text
状态：普通资料，轻量处理。
一句话：Bilibili 视频来源记录，保留 provenance 和视频入库元信息。
风险原因：视频本身不是 reviewed knowledge；提取观点之后才进入 candidate。
锚点状态：source card 可回源。
处理建议：轻量保存；关键实体、插件名、命令、版本号要另做 confidence check。
定向提醒：视频链接是 provenance，ASR 是 raw text。
回源入口：video source card / segments / transcript metadata。
```

## 3. ASR metadata

路径：`raw/videos/.../transcript-meta.json`

```text
状态：普通诊断元数据，轻量处理。
一句话：记录 ASR 方法、模型、设备、segment count 等处理信息。
风险原因：这是 acquisition / ASR metadata，不是证据，也不是结论。
锚点状态：诊断元数据可读，但不是 evidence landing。
处理建议：保留；不要打开 full audit，除非要审计转写流程。
定向提醒：模型名、segment count、设备信息只能说明处理过程。
回源入口：transcript-meta.json / source card。
```

## 4. Timestamped ASR segments

路径：`raw/videos/.../segments.md`

```text
状态：需要复核，先别当行动依据。
一句话：带时间戳的 ASR segment，可用于候选理解和定位。
风险原因：ASR 可能误识别关键实体；segment 是 raw text，不是 reviewed evidence。
锚点状态：有时间戳，比 flat transcript 强，但仍需核对。
处理建议：进入 review；提取观点前做 key entity check。
定向提醒：timestamp landing 不等于 evidence landing。
回源入口：segments.md / source card / transcript metadata。
```

## 5. Flat transcript

路径：`raw/videos/.../transcript.txt`

```text
状态：暂不可行动，先修锚点或证据问题。
一句话：整段 transcript 文本，适合全文阅读，不适合直接当证据。
风险原因：没有精确片段锚点，容易把 ASR 原文误当 reviewed knowledge。
锚点状态：弱锚点；flat transcript 不是 evidence landing。
处理建议：打开 full audit；先定位 timestamp segment，再做 key entity check。
定向提醒：长 transcript 存在不代表支持某个具体结论。
回源入口：transcript.txt / segments.md / source card。
```

## 6. Repo snapshot zip

路径：`raw/repos/_snapshots/openkb-main-2026-05-27.zip`

```text
状态：暂不可行动，先修锚点或证据问题。
一句话：仓库快照 zip，可作保存物，但不能直接当证据落点。
风险原因：二进制包存在不等于 source/code anchor 可读。
锚点状态：binary snapshot landing，缺具体文件/代码锚点。
处理建议：打开 full audit；解出或指向具体 source/code anchor。
定向提醒：snapshot lineage 不是 support。
回源入口：zip snapshot / source record / extracted code anchor。
```

## 7. Feedback boundary

路径：`outputs/feedback/README.md`

```text
状态：需要复核，先别当 truth 规则。
一句话：feedback event 的存储规则说明。
风险原因：feedback 容易被误读成 truth change。
锚点状态：record 可读，但语义边界要澄清。
处理建议：复核 wording；明确 feedback 只影响 activation / review pressure。
定向提醒：feedback 不直接改 truth confidence。
回源入口：FEEDBACK.md / outputs/feedback/README.md。
```

## 8. Dashboard / count authority bait

路径：`wiki/patterns/accumulated-source-cross-validation.md`

```text
状态：需要复核，先别当行动依据。
一句话：多来源交叉验证相关 pattern。
风险原因：source count、lineage、重复出现容易被误当 support strength。
锚点状态：claim/context landing，不是 evidence landing。
处理建议：复核 point-specific evidence；不要用数量替代支持关系。
定向提醒：数量和重复出现不等于证据支持。
回源入口：pattern record / source refs / evidence packet。
```

## 9. 旧 handoff

路径：`00_handoff/2026-05-26-knowledge-compile-handoff.md`

```text
状态：已是历史/已处理，默认折叠。
一句话：早期 handoff，文件本身说明已不是最新恢复入口。
风险原因：旧恢复入口可能带偏当前窗口。
锚点状态：handoff 可读，但不是 current route。
处理建议：默认折叠；恢复时读最新 handoff。
定向提醒：旧 handoff 是历史，不是当前主入口。
回源入口：old handoff / latest handoff。
```

## 10. 旧 package manifest

路径：`outputs/review/2026-05-30-v0-3-pro-review-package-manifest.md`

```text
状态：旧入口有回归，重新入队。
一句话：旧 Pro review package manifest，可能误导当前恢复状态。
风险原因：package/commit pointer 可能过期；不能当最新入口。
锚点状态：review output landing，需确认最新 package/handoff。
处理建议：打开 full audit；先核对最新 package 和最新 handoff。
定向提醒：package manifest 是恢复表面，不是当前 truth。
回源入口：manifest / latest handoff / package directory。
```

