# Adversarial Operator Cases 12

状态：sandbox-only adversarial add-on。给 Codex / Pro / reviewer agent 使用，不给普通用户日常阅读。

## 这包测什么

这不是普通覆盖扩展，而是专门测试最容易自证或误信的地方：

- ordinary-looking action-basis
- explicit challenge buried in polite wording
- anchor pseudo-success
- wrapper-only click-back
- review_due trap
- grouping near-miss
- serious folded trap
- authority paraphrase
- fake numeric precision
- summary overwrite
- source-count trap
- lineage trap

## 怎么用

1. 打开 `ADVERSARIAL_OPERATOR_CARDS_ZH.md`。
2. 每条只判断：陷阱是否识别、下一步是否正确、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。
3. 填 `ADVERSARIAL_REVIEW_SHEET_BLANK.csv`。
4. 做完后再看 `hidden_gold_after_done.csv`。

## 边界

- hand-authored synthetic pressure cases，不是真实业务日志。
- 不参与 ordinary reduction、front-line budget、或 product-grade click-back 成功率。
- `mock_sources/` 里的文件只用于演示 path / wrapper / quote / action-context 陷阱。
- 产品级 click-back 仍只能由真实来源或 immutable snapshot 证明。
- 这包不改 `SCHEMA.md`，不进入主库 operation convention。
