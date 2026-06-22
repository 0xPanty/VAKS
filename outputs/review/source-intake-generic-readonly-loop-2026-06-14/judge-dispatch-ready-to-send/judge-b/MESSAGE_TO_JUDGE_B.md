# 发给 Judge B 的消息

请只扮演 Judge B，做 excerpt-based semantic support judgment。

附件：

- `semantic-support-judge-b.zip`
- `semantic-support-judge-b.zip.sha256`

请只解压并填写 zip 里的：

```text
results/semantic_support_judgment_template.csv
```

规则：

- 只填 `judge_b_*` 列。
- 不要修改 `row_id`、`query`、`answer_use_claim`、`anchor_ref`、`anchor_source_hash`、`frozen_snapshot_ref`、`anchor_excerpt`。
- 只依据可见的 `query`、`answer_use_claim`、`anchor_excerpt` 判断。
- 如果 excerpt 不足或被截断，请给 0 或 1，并在 notes 说明。
- `relevance`: 0 = 不相关，1 = 部分相关，2 = 直接相关。
- `sufficiency`: 0 = 不支持该 claim，1 = 弱支持/部分支持，2 = 足以支持这个 read-only answer/use claim。

不要使用或索要 case_id、expected outcome、author-side self-check、row-to-case mapping、Judge A 结果、arbitration 文件或完整 Pro review package。

完成后只回传填写后的 CSV，文件名用 `returned_judge_b.csv`。
