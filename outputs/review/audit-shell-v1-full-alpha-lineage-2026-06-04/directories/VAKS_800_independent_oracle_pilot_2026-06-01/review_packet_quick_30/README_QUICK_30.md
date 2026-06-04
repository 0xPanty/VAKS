# Quick 30 Human Pilot

状态：本地单人预演，不是正式 human timing study。

## 怎么做

1. 打开 `quick_main_core_review.md`。
2. 每个 assignment 先读 View A，再读 View B。
3. 在 `quick_main_core_sheet_blank.csv` 里记录粗略秒数、是否会打开 full audit、看到的 state、click-back 结果、哪一版更轻、主观负担和备注。
4. 然后打开 `quick_side_recurrence_review.md`，填写 `quick_side_recurrence_sheet_blank.csv`。
5. 全部做完后再打开 `hidden_variant_map.csv`，看 View A / View B 分别是哪一个 variant。

表格里的 `view_a_source_path` / `view_b_source_path` 如果为空，表示那一侧没有暴露出可解析 pointer；可以把 click-back 记为 `na` 或在备注里写明。

## 范围

- 主预演：20 个 case，`baseline_full` vs `shell_core`。
- 侧预演：10 个 recurrence-heavy case，`shell_core` vs `shell_core_plus_recurrence`。

## 这轮能回答什么

- 人审流程顺不顺。
- `shell_core` 是否真的更轻，同时没有藏住 serious 风险。
- click-back 字段对真人 reviewer 是否足够好理解。
- recurrence grouping 是帮忙，还是制造误解。

## 这轮不能证明什么

- 这不是双人复核。
- 这不是产品级 click-back 验证。
- 这不是 independent human oracle。
- 不能写进主库 operation convention。
