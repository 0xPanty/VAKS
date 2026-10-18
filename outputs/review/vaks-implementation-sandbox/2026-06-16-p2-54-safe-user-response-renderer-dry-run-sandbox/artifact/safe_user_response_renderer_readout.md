---
record_kind: sandbox_artifact_readout
slice_id: 2026-06-16-p2-54-safe-user-response-renderer-dry-run-sandbox
status: built_pending_review
---

# Safe User Response Renderer Readout

| Case | Reply ID | Reply | Next Step |
| --- | --- | --- | --- |
| `no_reply` | `keep_reference_no_action` | 当前没有收到新的选择。我会保持 sandbox 作为参考，不执行任何选项，也不会合并、同步、提交、推送或写入正式层。 | `wait_or_report_reference_only` |
| `explicit_A` | `acknowledge_reference_only` | 收到，按 A 处理：只保留 sandbox 作为参考。我不会合并、promotion、sync、commit、push，也不会写入 reviewed knowledge、evidence support 或 action basis。 | `no_action_reference_only` |
| `explicit_B` | `ask_readonly_planning_scope` | 收到 B 的方向。下一步只能先确认单独的只读规划范围；在你明确范围前，我不会启动新 slice，也不会合并、同步、提交、推送或 promotion。 | `ask_for_separate_read_only_scope` |
| `explicit_C` | `ask_mainline_review_scope` | 收到 C 的方向。需要你单独批准主线评审范围和允许路径；在此之前我不会改主线、合并、同步、提交、推送或写入正式层。 | `ask_for_allowed_paths_and_scope` |
| `explicit_D` | `acknowledge_park_or_reject` | 收到 D。我会把 sandbox 链按搁置或拒绝理解，但不会改主线、不会删除既有产物，也不会同步、提交或推送。 | `acknowledge_no_mutation` |
| `ambiguous_reply` | `ask_one_clarification` | 这句话还不能确定是 A、B、C 还是 D。我先停下，不执行任何选项。请只回复一个选项：A、B、C 或 D。 | `ask_one_short_clarification` |
| `multiple_options` | `ask_choose_one` | 你同时提到了多个选项。我先停下，不执行任何选项。请只选择一个：A、B、C 或 D。 | `ask_user_to_choose_one_option` |
| `approval_with_execution_words` | `stop_for_separate_scope` | 这条回复包含执行、合并、同步、提交、推送或写入正式层的语义。我现在停止，不执行。若要越过 sandbox 边界，需要你单独给出明确范围和允许路径。 | `stop_and_ask_for_separate_explicit_scope` |
| `unknown_case_fallback` | `stop_for_unknown_classifier_case` | 分类结果不在已知安全集合内。我现在停止，不执行任何选项。请重新明确选择 A、B、C 或 D，或单独给出明确范围。 | `stop_and_ask_for_clarification` |

The renderer is dry-run only. It drafts safe wording and never executes an
option.
