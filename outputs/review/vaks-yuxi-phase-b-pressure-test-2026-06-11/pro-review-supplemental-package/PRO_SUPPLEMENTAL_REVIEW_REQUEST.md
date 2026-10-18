---
record_kind: pro_supplemental_review_request
status: draft
project_id: VAKS
created_at: 2026-06-11
truth_boundary: review_request_not_decision
action_basis_allowed: false
---

# VAKS + Yuxi-like Phase B P0/P1 Supplemental Review Request

请你做一次反向审计，不要顺着我们的结论走。

背景：你之前指出 Phase B 证据“部分成立”，主要问题是样本小、holdout 被迭代污染、缺 query-level trace / receipt / relevance judgment、`yuxi_native_profile` 不是原版 Yuxi、promotion gate 只证明负向阻断。我们按这个方向补了 P0/P1 证据包。

补充说明：这次还加入了一组 `agent_blind` 查询，由一个不继承本线程上下文的子 agent 独立生成。它被要求只读核心文档，不读取已有 Phase B queries/results/reports。它仍然不是外部人类盲测，也不是 original Yuxi runtime 测试。

二次补充：按你最新反馈，我们又补了 P0 级别的可复跑/可审计材料：frozen corpus manifest + file-hash snapshot，以及 P0 main/holdout 的 top11-20 item-level receipts。也就是说，top20 first-hit-rank 不再只停留在 query-level，11-20 名候选现在也能逐条看见；但这仍然只是本地 proxy harness 的可审计增强，不是 original Yuxi runtime 验证。

三次补充：你指出这些 hardening artifacts 仍像后补材料，不一定和 earlier P0 metrics 属于同一次 frozen run。我们新增了 `Frozen Rerun v2`：同一个 run_id 下，一次性产出 corpus manifest、query manifest、script hashes、top20 item-level export、top1-10 replay、top11-20 receipts、query metrics、summary，并用 validator 从 top20 item rows 精确回推 query metrics 和 summary。它解决的是本地 P0 proxy 证据的 exact-run alignment；它仍然没有补 human relevance judgment，也没有运行 original Yuxi runtime。

四次补充：我们新增了 18 条 internal no-parent-context blind relevance queries，并产出 top5 judgment packet。随后用 `codex_internal_heuristic_judge_v1` 填了 720 行 0/1/2 judged relevance，得到 judged hit@5 / MRR@5 / nDCG@5。这个 judgment 和 `expected_terms` 分离，但它仍然是内部启发式/模型辅助判分，不是外部人类或 Pro judgment。请你重点审这个判分是否可接受，或者是否应该由你/外部人重判。

五次补充：根据你最新结论，我们没有把 internal judgment 当成最终证据，而是新增并修订了 external/manual relevance judgment kit：`results/phase_b_blind_relevance_external_judgment_template.csv`。新版 judge-facing template 隐藏了 `mode`、`run_id`、原始 `judgment_id` 等系统身份字段，只暴露 opaque `row_id` 和 `system_slot`；真实 mode 映射单独放在 `results/phase_b_blind_relevance_external_judgment_mapping.csv`，仅用于判分后统计。它要求 Judge A、Judge B 独立判分，并由 arbiter 对每一行给出 `arbitrated_relevance`。当前状态是 `pending_external_judgment / 0 errors`，也就是说匿名模板和校验链就绪，但外部/人工双判尚未完成。

六次补充：按你给的最小补测顺序，我们又新增并修订了 external blind query set kit：`queries_phase_b_external_blind_template.jsonl`。新版模板要求外部人类或不同模型家族生成 15-20 条新 query，且不得读取现有 Phase B queries/results/reports；同时新增 `results/phase_b_external_blind_query_author_manifest_template.json`，用于记录 author_type、author_id_or_model_family、allowed_docs_seen 和 no-access attestations。外部作者不再填写 `expected_terms`；后续 scoring hints 必须由内部在 query 文本冻结后另行补。当前状态是 `pending_external_queries / 0 errors`，也就是说外部出题模板、作者声明模板和校验链就绪，但真正外部 blind query set 尚未完成。

请重点判断：

1. P0 query-level replay 是否真正解决了“只有汇总表、不可复算”的问题？
2. P0 的指标口径是否诚实？尤其是 top20 paired query outcomes 与 top10 replay/governance checks 的拆分是否合理？
3. frozen corpus manifest / file-hash snapshot 是否足以把“可复算”往“可重跑”推进一步？
4. top11-20 item-level receipts 是否真正补上了之前 11-20 名不可逐条审计的洞？
5. Frozen Rerun v2 是否真正解决了“manifest / replay / receipts / metrics / summary 不是同一次 frozen run”的问题？
6. Frozen Rerun v2 的 validator 是否足够严格，能从 top20 item-level bundle 回推 query metrics 和 summary？
7. clean VAKS-only lexical + authority-bucket control 是否足以隔离 VAKS 边界贡献？
8. P1 fresh adversarial set 是否能增强结论？它不是外部盲测，这个限制应该如何影响判断？
9. P1 promotion gate positive/negative calibration 是否足以回应“只会全拦”的批评？
10. `agent_blind` 查询集是否真正增强了泛化证据？它不是外部人类盲测，这个限制应如何表述？
11. 当前证据是否支持更精确的归因：hybrid Yuxi-like retrieval base 提供 raw retrieval lift，VAKS authority/warning/receipt 提供主要 governance lift，VAKS adapter alignment 额外贡献部分 retrieval lift？
12. 当前证据是否仍然不支持 C-lite、runtime adoption、writeback adoption、mainline strong conclusion？
13. internal blind relevance queries 和 `codex_internal_heuristic_judge_v1` 判分是否有审计价值？它能否缓解 expected_terms proxy 的问题，还是必须由外部人/Pro 重判？
14. revised external/manual relevance judgment kit 的匿名 `row_id/system_slot` + mapping 设计是否足够 blind？是否适合让你或外部人直接填？
15. revised external blind query set kit 的两步流程是否合理：外部作者只写 query + author manifest，内部后补 expected_terms/scoring hints？
16. `PHASE_B_EXTERNAL_VALIDATION_NEXT_STEPS.md` 和 `PHASE_B_READ_ONLY_ANSWER_LOOP_PILOT_SPEC.md` 的下一步门禁是否合理？
17. 如果你认为还有 overclaim，请指出具体文件、具体句子或具体指标。
18. 如果你认为下一步还要补测，请按 P0/P1/P2 优先级列最小必要清单。

请不要默认接受我们的说法。你可以直接给：

```text
overall verdict: 成立 / 部分成立 / 不成立
can keep Phase B as sandbox candidate: yes/no
can enter C-lite: yes/no
can claim original Yuxi runtime validated: yes/no
can commit core docs with strong conclusion: yes/no
most important remaining blocker:
```

包内最重要文件：

```text
PHASE_B_P0_P1_SUPPLEMENTAL_PRESSURE_REPORT.md
PHASE_B_P0_QUERY_LEVEL_REPLAY_REPORT.md
PHASE_B_P0_QUERY_LEVEL_REPLAY_CHECK.md
PHASE_B_METRIC_DICTIONARY.md
PHASE_B_FROZEN_CORPUS_MANIFEST.md
PHASE_B_FROZEN_CORPUS_MANIFEST_CHECK.md
PHASE_B_TOP11_20_ITEM_RECEIPTS_REPORT.md
PHASE_B_TOP11_20_ITEM_RECEIPTS_CHECK.md
PHASE_B_FROZEN_RERUN_V2_REPORT.md
PHASE_B_FROZEN_RERUN_V2_CHECK.md
PHASE_B_BLIND_RELEVANCE_PILOT_REPORT.md
PHASE_B_BLIND_RELEVANCE_CHECK.md
PHASE_B_BLIND_RELEVANCE_JUDGMENT_INSTRUCTIONS.md
PHASE_B_INTERNAL_RELEVANCE_JUDGMENT_REPORT.md
PHASE_B_EXTERNAL_RELEVANCE_JUDGMENT_KIT.md
PHASE_B_EXTERNAL_RELEVANCE_JUDGMENT_KIT_CHECK.md
PHASE_B_P1_ADVERSARIAL_AUDIT_REPORT.md
PHASE_B_P1_ADVERSARIAL_AUDIT_CHECK.md
PHASE_B_P1_PROMOTION_GATE_CALIBRATION_REPORT.md
PHASE_B_P1_PROMOTION_GATE_CALIBRATION_CHECK.md
PHASE_B_AGENT_BLIND_AUDIT_REPORT.md
PHASE_B_AGENT_BLIND_AUDIT_CHECK.md
PHASE_B_ORIGINAL_YUXI_RUNTIME_FEASIBILITY.md
PHASE_B_EXTERNAL_VALIDATION_NEXT_STEPS.md
PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT.md
PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT_CHECK.md
PHASE_B_READ_ONLY_ANSWER_LOOP_PILOT_SPEC.md
PHASE_B_NEXT_STEP_SPECS_CHECK.md
results/phase_b_p0_summary.csv
results/phase_b_p0_query_level_metrics.csv
results/phase_b_p0_query_level_replay.csv
results/phase_b_frozen_corpus_manifest.json
results/phase_b_frozen_corpus_manifest.csv
results/phase_b_top11_20_item_receipts.csv
results/phase_b_top11_20_item_receipts_summary.json
results/phase_b_frozen_rerun_v2_manifest.json
results/phase_b_frozen_rerun_v2_top20_items.csv
results/phase_b_frozen_rerun_v2_top1_10_replay.csv
results/phase_b_frozen_rerun_v2_top11_20_receipts.csv
results/phase_b_frozen_rerun_v2_query_metrics.csv
results/phase_b_frozen_rerun_v2_summary.csv
results/phase_b_blind_relevance_top20_items.csv
results/phase_b_blind_relevance_judgment_packet.csv
results/phase_b_blind_relevance_judgments.csv
results/phase_b_blind_relevance_judged_summary.csv
results/phase_b_blind_relevance_external_judgment_template.csv
results/phase_b_blind_relevance_external_judgment_mapping.csv
results/phase_b_external_relevance_judgment_kit.json
results/phase_b_external_relevance_judgment_kit_check.json
results/phase_b_external_blind_query_author_manifest_template.json
results/phase_b_external_blind_query_set_kit.json
results/phase_b_external_blind_query_set_kit_check.json
results/phase_b_p1_adversarial_combined_summary.csv
results/phase_b_p1_adversarial_audit.json
results/phase_b_p1_promotion_gate_calibration_summary.json
results/phase_b_agent_blind_combined_summary.csv
results/phase_b_agent_blind_audit.json
queries_phase_b_adversarial.jsonl
queries_phase_b_agent_blind.jsonl
queries_phase_b_blind_relevance.jsonl
queries_phase_b_external_blind_template.jsonl
tools/build_phase_b_p0_query_replay.py
tools/validate_phase_b_p0_query_replay.py
tools/build_phase_b_frozen_corpus_manifest.py
tools/validate_phase_b_frozen_corpus_manifest.py
tools/build_phase_b_top11_20_receipts.py
tools/validate_phase_b_top11_20_receipts.py
tools/build_phase_b_frozen_rerun_v2.py
tools/validate_phase_b_frozen_rerun_v2.py
tools/build_phase_b_blind_relevance_pilot.py
tools/validate_phase_b_blind_relevance_pilot.py
tools/build_phase_b_internal_relevance_judgments.py
tools/build_phase_b_external_relevance_judgment_kit.py
tools/validate_phase_b_external_relevance_judgment_kit.py
tools/build_phase_b_external_blind_query_set_kit.py
tools/validate_phase_b_external_blind_query_set_kit.py
tools/build_phase_b_p1_adversarial_audit.py
tools/validate_phase_b_p1_adversarial_audit.py
tools/build_phase_b_p1_promotion_gate_calibration.py
tools/validate_phase_b_p1_promotion_gate_calibration.py
tools/build_phase_b_agent_blind_audit.py
tools/validate_phase_b_agent_blind_audit.py
tools/validate_phase_b_next_step_specs.py
```

当前我们自己的保守结论：

```text
keep_phase_b_as_sandbox_candidate: yes
enter_c_lite: no
runtime_adoption: no
writeback_adoption: no
mainline_strong_conclusion: no
original_yuxi_runtime_validated: false
```
