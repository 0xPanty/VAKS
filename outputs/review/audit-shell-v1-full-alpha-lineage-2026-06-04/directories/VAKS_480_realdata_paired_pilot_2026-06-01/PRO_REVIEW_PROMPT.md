请复核这个 VAKS audit shell v1 480 paired pilot 包。

我希望你不要只看 headline 数字，请重点判断：

1. 这个 480 是否够资格叫 real-data paired pilot，还是只能叫 real-row + pressure-overlay pilot？
2. `shell_core` 是否可以被视为当前最合理的强正向 alpha？
3. `shell_core_plus_recurrence` 是否应该保留为可选 recurrence bundle，还是证据仍不足？
4. unversioned recurrence control 的失败，是否足以说明 versioned fingerprint 是 grouping 的必要安全件？
5. burden 指标是否仍有自证嫌疑，尤其是 line/char/review_proxy 与真实 reviewer burden 的距离？
6. anchor 现在从 source path/marker 扩到 record/evidence pointer resolution，这是否够进入主框架沙盒测试？还缺什么 selector/UI click-back？
7. authority fuzz 只命中 9/16，是否说明 authority lint 只能作为 lint/convention，不能作为 guardrail proof？
8. 最合理的主框架沙盒落点是什么：core shell、core+recurrence、还是只记录为候选不落？

请自由指出：

- overclaim
- blind spot
- 哪些指标不能进主库
- 哪些设计可以进入 sandbox operation convention 草案
- 是否需要补一轮小 patch，还是可以进入主框架沙盒压力测试

边界提醒：

- shell 不是 truth core。
- grouping 不是 support strength。
- provenance/lineage/source count 不是 independence proof。
- feedback 不改 truth confidence。
- test/dashboard/report pass 不得成为 truth authority。
- 不要建议改 `SCHEMA.md`，除非你认为有非常强的必要性并单独说明。

