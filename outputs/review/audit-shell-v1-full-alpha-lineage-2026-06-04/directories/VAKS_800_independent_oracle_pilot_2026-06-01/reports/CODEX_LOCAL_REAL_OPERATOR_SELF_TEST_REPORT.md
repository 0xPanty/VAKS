# Codex local real operator self-test

## Verdict

结论：Codex 自己看得懂，能用于后台 operator triage；但这不是真人评审，也不是 product click-back gate。

这次只测一件事：我作为你的资料库管家，面对本地真实行承载样本和 full-anchor 快照时，能不能看懂 shell/operator surface 给出的状态、下一步动作、回源强弱和边界提醒。没有让用户参与，没有打开 120-case main packet，也没有把 recurrence 默认打开。

## Summary

- 样本数：26
- 能看懂状态和下一步动作：26/26
- wrong actionability：0/26
- serious miss：0/26
- authority misunderstanding：0/26
- source / record / evidence 路径可打开：23/26 / 26/26 / 26/26
- quote 文本可找到 / offset 精确：22/26 / 22/26
- landing class 分布：{"evidence_landing": 1, "claim_landing": 1, "claim_relevant_context_landing": 4, "none": 20}

## What This Means

对 Codex 来说，这张 operator surface 有帮助：它把我需要做的事压成了“轻量保存、复核、阻塞不可行动、补锚点、重新入队、行动前 full audit”这些动作，而不是让我从一大坨 raw audit transcript 里猜。

但它的边界也清楚：`claim_relevant_context_landing` 只能算弱回源落点，不能当证据段；`claim_landing` 也只是 claim 落点，不等于 support。真正要当行动依据时，仍然要打开 full audit 或找 evidence landing。

## Sample Readout

| case | layer | state | anchor | landing | actionability | Codex next action |
|---|---|---|---|---|---|---|
| FULLANCHOR-016 | full_anchor_click | ordinary | valid | evidence_landing | light_save_only | 轻量保存；如需作为行动依据再打开 full audit |
| FULLANCHOR-003 | full_anchor_click | for_review | valid | claim_landing | not_actionable_until_review | 进入复核；打开 full audit；复核前不作为行动依据 |
| FULLANCHOR-001 | full_anchor_click | ordinary | valid | claim_relevant_context_landing | light_save_only | 轻量可读，但回源只是 claim 相关上下文；行动前必须打开 full audit |
| FULLANCHOR-002 | full_anchor_click | blocking | valid | claim_relevant_context_landing | not_actionable | 暂不可行动；打开 full audit；优先修锚点或处理阻塞原因 |
| FULLANCHOR-005 | full_anchor_click | ordinary | valid | claim_relevant_context_landing | light_save_only | 轻量可读，但回源只是 claim 相关上下文；行动前必须打开 full audit |
| FULLANCHOR-006 | full_anchor_click | blocking | valid | claim_relevant_context_landing | not_actionable | 暂不可行动；打开 full audit；优先修锚点或处理阻塞原因 |
| SCIFACT-001 | ordinary_stable | ordinary | valid |  | light_save_only | 轻量保存；如需作为行动依据再打开 full audit |
| SCIFACT-002 | ordinary_stable | ordinary | valid |  | light_save_only | 轻量保存；如需作为行动依据再打开 full audit |
| SCIFACT-061 | action_challenge_conflict | blocking | valid |  | not_actionable | 暂不可行动；打开 full audit；优先修锚点或处理阻塞原因 |
| SCIFACT-062 | action_challenge_conflict | blocking | valid |  | not_actionable | 暂不可行动；打开 full audit；优先修锚点或处理阻塞原因 |
| SCIFACT-091 | omission_insufficiency_ambiguity | for_review | valid |  | not_actionable_until_review | 进入复核；打开 full audit；复核前不作为行动依据 |
| SCIFACT-092 | omission_insufficiency_ambiguity | for_review | valid |  | not_actionable_until_review | 进入复核；打开 full audit；复核前不作为行动依据 |
| SCIFACT-116 | anchor_problem | blocking | missing |  | not_actionable | 暂不可行动；打开 full audit；优先修锚点或处理阻塞原因 |
| SCIFACT-117 | anchor_problem | for_review | stale |  | not_actionable_until_review | 进入复核；打开 full audit；复核前不作为行动依据 |
| HOLDOUT-029 | anchor_jumpback_failure | blocking | missing |  | not_actionable | 暂不可行动；打开 full audit；优先修锚点或处理阻塞原因 |
| HOLDOUT-001 | false_lite_trap | blocking | valid |  | not_actionable | 暂不可行动；打开 full audit；优先修锚点或处理阻塞原因 |
| HOLDOUT-017 | review_due_trap | for_review | valid |  | not_actionable_until_review | 进入复核；打开 full audit；复核前不作为行动依据 |
| SCIFACT-131 | resolved_repeated_recurrence | resolved_folded | valid |  | historical_only | 默认折叠；只保留历史入口；回归时再重开 |
| SCIFACT-132 | resolved_repeated_recurrence | resolved_folded | valid |  | historical_only | 默认折叠；只保留历史入口；回归时再重开 |
| SCIFACT-151 | authority_leak_bait | ordinary | valid |  | light_save_only | 轻量保存；把 dashboard/test/count/lint 只当诊断，不当事实依据 |
| SCIFACT-152 | authority_leak_bait | ordinary | valid |  | light_save_only | 轻量保存；把 dashboard/test/count/lint 只当诊断，不当事实依据 |
| HOLDOUT-065 | authority_leakage_paraphrase | ordinary | valid |  | light_save_only | 轻量保存；把 dashboard/test/count/lint 只当诊断，不当事实依据 |
| HOLDOUT-045 | over_grouping_near_miss | ordinary | valid |  | light_save_only | 轻量保存；如需作为行动依据再打开 full audit |
| HOLDOUT-046 | over_grouping_near_miss | ordinary | valid |  | light_save_only | 轻量保存；如需作为行动依据再打开 full audit |
| HOLDOUT-073 | serious_folded_violation | regressed | valid |  | not_actionable | 重新入队；打开 full audit；不要继续按已解决处理 |
| HOLDOUT-074 | serious_folded_violation | blocking | missing |  | not_actionable | 暂不可行动；打开 full audit；优先修锚点或处理阻塞原因 |

## Files

- CSV: `review_packet_local_real_self_test/LOCAL_REAL_OPERATOR_SELF_TEST.csv`
- Summary: `review_packet_local_real_self_test/LOCAL_REAL_OPERATOR_SELF_TEST_SUMMARY.json`

## Boundary

本报告只能说明“Codex/operator agent 能读懂并执行初步路由”。它不能替代真人双评、timing、真实 UI click log，也不能把 `not_go_yet` 改成 go。
