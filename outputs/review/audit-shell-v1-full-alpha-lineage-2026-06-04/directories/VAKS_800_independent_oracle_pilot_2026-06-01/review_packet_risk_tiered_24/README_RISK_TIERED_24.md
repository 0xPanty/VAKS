# Risk-Tiered Reviewer UX Preflight 24

状态：沙盒小样本预演材料。给 AI / reviewer operator 使用，不是普通用户日常流程，不是正式 human timing，不是 independent human oracle，不是主库 operation convention。

普通用户不需要读这些卡片。用户只应在风险影响回答或行动时看到一句人话提醒。

## 怎么用

1. 打开 `RISK_TIERED_REVIEWER_CARDS_ZH.md`。
2. 每条只看中文 operator 前脸，判断状态、升级原因、处理建议和回源入口。
3. 把答案填到 `RISK_TIERED_REVIEWER_SHEET_BLANK.csv`。
4. 做完后再看 `hidden_gold_after_done.csv`。

## 这轮看什么

- time-to-triage：多久能判断下一步。
- serious miss rate：有没有漏掉严重项。
- wrong-actionability rate：有没有把不可行动项当可行动。
- click-back success：source / record / evidence 能不能跳回。
- authority misunderstanding：有没有把 count、test、dashboard、lineage、feedback、shell summary 当证据。
- forbidden wording：中文 operator 文案不能出现 `forbidden_wording_zh.json` 中的 truth/readiness 越权措辞。

## 这轮不看什么

- 不看 line reduction。
- 不比较 recurrence side arm。
- 不生成人审结论。
- 不证明 product-grade click-back。
- 不证明 semantic firewall。
