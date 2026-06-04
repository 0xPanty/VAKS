# Pro Review Prompt

这是 Codex 按你上一轮意见补的极小 hardening patch。请继续独立复核，不要默认接受 Codex 结论。

这轮主要补了五件事：

```text
1. 拆 oracle：cases_input / gold_oracle / renderer / checker / aggregator 分文件和 runner。
2. authority leakage 从 exact phrase 扩到 paraphrase family 黑盒规则。
3. 补 versioning 真对抗样本：除 fingerprint_version 外，grouping 字段全同。
4. headline 改 paired metrics，不再用 synthetic total*12。
5. anchor metric 改成 anchor_problem_visibility，覆盖 missing / stale / drift / moved。
```

请重点判断：

```text
A. 这轮是否真正解决了 same-script self-proof 的主要问题？
B. authority paraphrase family 是否够硬，还是仍太像 lint？
C. versioning hard counterexample 是否足以证明 versioned fingerprint grouping 现在值得进入 480 pilot？
D. paired metrics 是否更可信？
E. anchor_problem_visibility 是否比 missing_anchor_visibility 更合适？
F. 现在是否可以进入 480 real-data paired pilot？
```

如果还不能进入 480，请只给最关键的剩余 blocker。

边界仍然是：

```text
主库不改
SCHEMA 不动
shell / grouping / dashboard / feedback / tests 不能成为 truth authority
source count / lineage / group count 不能冒充 source independence
provenance 不是 support
support 不是 truth
reviewed knowledge 也不自动 action-ready
```
