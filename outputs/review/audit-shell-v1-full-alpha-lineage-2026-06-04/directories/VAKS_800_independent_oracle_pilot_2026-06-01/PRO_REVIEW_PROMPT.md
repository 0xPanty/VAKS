请复核这个 VAKS audit shell v1 800-case pressure-overlay pilot 的 patched package，重点看最新收束和 Chinese reviewer-card candidate convention。

不需要从零重审全部自动包。请先看：

- `NEXT_REVIEW_READING_ORDER.md`
- `README_FOR_PRO.md` 的 `Latest Convergence / Current Candidate Convention`
- `reports/PRO_REVIEW_PASS_WITH_CONCERNS_AND_NEXT_ROUTE.md`
- `reports/OPERATOR_ADJUDICATION_ROUND1_REVIEW_RESULT.md`
- `reports/CLICKBACK_SEMANTIC_LANDING_EVAL.md`
- `review_packet_operator_adjudication_narrow/README_OPERATOR_ADJUDICATION_NARROW.md`

然后再看：

- `reports/AUDIT_SHELL_V1_SANDBOX_CLOSEOUT.md`
- `reports/CHINESE_REVIEWER_CARD_PATCH_SPEC.md`
- `reports/AUDIT_SHELL_V1_REVIEWER_CARD_CANDIDATE_CONVENTION.md`
- `reports/EXTERNAL_ARCHITECTURE_REVIEW_SYNTHESIS.md`
- `reports/EXTERNAL_SOURCE_PRIORITY_AND_FINAL_JUDGMENT.md`
- `reports/RISK_TIERED_REVIEWER_UX_PATCH_SPEC.md`
- `reports/CHINESE_REVIEWER_CARD_USABILITY_PREFLIGHT_PROTOCOL.md`
- `reports/NEGATIVE_CONTROL_AND_VALIDATION_TIMELINE.md`
- `reports/QUALITY_GATES_AND_THRESHOLDS.md`
- `reports/CHINESE_FORBIDDEN_WORDING_LINT.md`
- `review_packet_risk_tiered_24/README_RISK_TIERED_24.md`
- `review_packet_adversarial_12/README_ADVERSARIAL_12.md`

这包不是要你默认接受 Codex 的结论。请自由发挥，尤其欢迎指出更合理的设计收束、反例、overclaim、blind spot，或者是否只需要一个更窄的小补丁。不要为了测试而再鼓励大范围自动评测。

请不要从 `pilot_800_results.json` 或 reduction 数字开始判断。先按 `NEXT_REVIEW_READING_ORDER.md` 看边界文件、核心脚本、click-back manifest 和 human packet 覆盖，再看自动结果。

背景定位：

- 这是 sandbox-only package。
- 没有改主库，没有改 `SCHEMA.md`。
- 自动部分已补丁化：800 cases、四臂、frozen machine oracle、selector/pointer checks、front-density 指标、负控、authority fuzz、stratified blank human packets。
- 当前负控已扩为三类：`leaky_or_unversioned_control`、`authority_leaky_renderer`、`fake_precision_feedback_renderer`。三者都必须 fail；如果任一负控抓不出来，harness 不值得信。
- 当前新增 `quality_gates_v1.json` / `quality_gate_eval_800.json` / `reports/QUALITY_GATES_AND_THRESHOLDS.md`。这里的 go 只表示“允许进入主库候选 operation convention 讨论”，不是直接采用。当前整体状态应仍是 `not_go_yet`，因为 wrong actionability、authority misunderstanding、human timing/open-rate、以及 product click-back semantic landing 等 hard/product gates 还没过。
- 当前新增 `forbidden_wording_zh.json` / `reports/CHINESE_FORBIDDEN_WORDING_LINT.md` / `review_packet_risk_tiered_24/forbidden_wording_lint_zh.json`。请复核中文禁用措辞与安全替代表是否足够防止 truth/readiness 越权。
- 这仍然不是真正完成的 independent human-oracle pilot；human timing、dual review、click-back adjudication 仍为空白。
- 最新收束是：default core = `shell_core` + Chinese AI/reviewer-operator rendering；recurrence / grouping = conditional side arm；authority lint + categorical feedback strip + forbidden-wording lint = background guardrails。
- Chinese reviewer-card 是 AI/reviewer operator 的 view-layer alpha，不是用户日常流程、不是新 truth layer、不是 schema change、不是主库 operation convention。
- 进一步收束后的实现理解是：risk-gated review surface + evidence envelope + source-first drilldown；card 只是第一层 renderer。
- 外部来源优先级已经单独收进 `reports/EXTERNAL_SOURCE_PRIORITY_AND_FINAL_JUDGMENT.md`：优先读 W3C Web Annotation / PROV、GitHub conversation、Sentry issue/grouping、OpenTelemetry sampling、ClaimReview、SciFact、AVeriTeC、AmbiFC、FEVER 等原始规范、官方 docs 和原始论文。英文一手来源优先于中文二手总结。
- 当前新增的 `review_packet_risk_tiered_24/` 只是 24 个中文 operator 小样本预演材料，未填写人审结果，也不要求普通用户查看。
- 当前新增的 `review_packet_adversarial_12/` 是 12 个 synthetic adversarial operator cases，用来专门打 anti-self-proof trap：ordinary-looking action-basis、buried challenge、anchor pseudo-success、wrapper-only click-back、review_due trap、grouping near-miss、serious folded trap、authority paraphrase、fake numeric precision、summary overwrite、source-count trap、lineage trap。它不是普通覆盖扩展，不参与降噪率，也不是产品级 click-back 证明。
- 当前新增 `reports/CODEX_OPERATOR_PREFLIGHT_DRY_RUN_REPORT.md`、`review_packet_risk_tiered_24/CODEX_OPERATOR_PREFLIGHT_DRY_RUN.csv` 和 `review_packet_adversarial_12/CODEX_ADVERSARIAL_OPERATOR_DRY_RUN.csv`。这些只表示 Codex operator dry-run，不是独立人审、不是 timed usability、不是 adoption gate。
- 当前 `data/clickback_snapshot_manifest.json` 已把 24 个 representative full-anchor cases 从旧的 4 live / 20 fallback 修到 24 live / 0 fallback。上一轮窄样本复核指出这只是 transport success，不是 semantic landing。当前新增 `data/clickback_semantic_landing_eval.json`，并用 exact evidence / exact claim / claim-keyword window 修复 selector landing；目前 automated semantic selector success 是 24/24，`body_window` / boilerplate 是 0/24。请重点复核 landing class 分布，尤其 claim_keyword_window 是否只能算较弱的 claim-relevant context landing，而不能等同于 evidence landing。不要把它当作已通过 product gate。
- 最新外部窄样本复核结论是 `pass with concerns`，但当时不同意进入 120-case main packet，也不同意打开 recurrence side packet。本包已修 selector landing proxy 和 ordinary+warning handling 边界；请判断下一步是否应 rerun narrow adjudication，而不是直接开 120-case main packet。
- 最新中文 operator card 已增加最小中文 handling gloss，并把 `raw_sources/...` 这类路径改成“来源 / 记录 / 证据入口 + 句柄”的形式。请复核这是否足够降低工程夹具味。

请重点看：

1. 最新收束是否合理：
   - default core 是否应收为 `shell_core` + Chinese reviewer-card rendering。
   - Chinese reviewer-card 是否确实是下一步必补的 human-facing clarity alpha，而不是翻译润色。
   - recurrence / grouping 是否继续只能作为条件侧臂。
   - authority lint / categorical feedback / forbidden-wording lint 是否只能作为后台 guardrail。
2. 如需 spot-check，检查这轮 patch 是否补上了上一轮 Pro 点名的自动缺口：
   - human packet 是否覆盖 resolved / can_group / bad anchor / authority bait / anchor jumpback failure / over-grouping near miss / serious folded violation。
   - grouping checker 是否已经能正确计入 folded members。
   - resolved folding 是否应改用 default unresolved-first surface metric，而不是 opened resolved record 的 95% line reduction。
   - click-back snapshot subset 已补到 24 live / 0 fallback；semantic selector success 已从 7/24 修到 24/24。请复核 keyword-window selector 是否合理、是否仍可能误落到非证据上下文，以及 landing class 是否足够明确。
3. `shell_core` 是否仍是唯一默认核心候选。
4. `shell_core_plus_recurrence` 是否只能作为条件臂，而不是默认 core。
5. negative control 是否足够证明 harness 会抓错。
6. frozen gold 是否只能称为流程冻结的 machine oracle，而不能称为独立人工 oracle。
7. authority fuzz 100% 是否仍只能叫 lint pass，不能叫 semantic safety proof。
8. 下一步是否应是 Chinese reviewer-card patch + 12-24 中文小样本可用性预演 + 小 render-integrity lint，而不是继续扩大自动测试。
8a. 在 latest pass-with-concerns 之后，selector landing proxy 已修；下一步是否应 rerun `review_packet_operator_adjudication_narrow/` 的真人双评 adjudication，而不是直接开 120-case main packet。
9. 12-case adversarial add-on 是否覆盖了最容易造成自嗨的反例；是否还缺更狠的 anti-self-proof trap。
10. 三类负控是否足够，尤其是否还需要更强的 authority paraphrase 或 fake precision 负控。
11. go / no-go gate 是否合理，尤其哪些 gate 必须保持 hard、哪些只能算 supporting、哪些现在必须标为 not measured。
12. `reports/QUALITY_GATES_AND_THRESHOLDS.md` 里的阈值解释是否成立：line/char reduction 只能算 supporting，click-back / wrong actionability / authority misunderstanding 才是 hard risk gates。
13. 禁止进入 operation convention 的 anti-pattern 是否完整：LLM summary、dashboard/test/eval、source count、lineage、group count、feedback、fake numeric precision、pointer existence、lint pass、test/report pass 都不能越权成 truth / readiness。
14. `forbidden_wording_zh.json` 是否应加入更多中文/中英混合 forbidden wording，或现有 regex 是否太宽/太窄。

边界请继续坚持：

- shell 不是 truth core。
- grouping/count 不是 support strength。
- provenance/lineage/source count 不是 independence proof。
- feedback 不改 truth。
- test/dashboard/report pass 不得成为 truth authority。
- authority lint 只能是 lint，不能是 semantic safety proof。
- recurrence fold 不能吃掉 serious member。
- 不建议改 `SCHEMA.md`，除非你认为有极强必要性并单独说明。

请最后给一个工程判断：

- pass / pass with concerns / fail
- 是否先做 Chinese reviewer-card 小补丁和有限中文可用性预演
- 是否已经可以进入人工 timing / dual-review / click-back，还是应等 reviewer-card clarity 先补完
- 默认核心应包含什么，尤其是否包含 Chinese reviewer-card rendering
- recurrence bundle 应继续、收窄、还是砍掉
- 哪些指标或文案绝对不能进主库 operation convention
