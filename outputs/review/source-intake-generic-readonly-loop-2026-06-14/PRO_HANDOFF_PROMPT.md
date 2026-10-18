# Prompt To Send Pro

请反向审计这份 VAKS Source Intake Generic Read-Only Loop 包。

重点不是看它有没有写得好看，而是判断它是否真正回应了上一轮 blocker，尤其是最新 Pro 指出的两件事：残余 fallback 是否彻底退场、judge-only packet 是否真正盲化。

1. pack role assignment 是否已经不再按 case_id 手工决定 support，而是按通用规则处理 live top-k；
2. candidate / project_overlay 是否都被通用规则降为 review_input，而不是 final support；
3. 新增的 sandbox QueryPolicy / authority-bucket receipt 是否真的在 retrieval 前生成，并进入 query-run/context-pack artifacts；
4. QueryPolicy 是否明确记录 allowed buckets、allowed roles、support-candidate buckets、implemented local lexical channel，以及未实现 dense/vector/sparse/graph/RRF/rerank；
5. `results/receipt_effect_*` 是否 demonstrate restricted allowed buckets 会产生 non-zero pre-ranking exclusions；
6. receipt-effect paired same-query cases 是否在不改 scorer/corpus 的情况下产生 top-k 变化；
7. 主 harness 新增的默认 restricted review/action case 是否也出现 non-zero exclusion；
8. source_annotation bucket 是否已有 retention/exclusion 的 receipt-effect 运行证据；
9. reviewed bucket 是否已有真实 reviewed 文档的 retention/exclusion receipt-effect 运行证据；
10. raw source card 是否只有在 read-only support mode 且 raw/stable anchor 可解析时才进入 support；
11. packaged scripts / outputs 里是否已经没有上一轮 legacy fallback 机制：旧的已知 anchor 常量、forced-hit helper、known-anchor resolution label、forced-anchor marker、高分注入模式；
12. full collected Markdown corpus snapshot + replay 是否足以支撑“本包可复跑”，但不被过度解释成 full production reproducibility；
13. 三条 non-FlexNote allow smoke case（W3C Web Annotation、W3C PROV、RAG attribution faithfulness）是否真的缓解了单一 FlexNote anchor family 的问题，但没有被过度解释成语义支持已完成；
14. low-cue allow queries 是否没有直接点名 support heading，却仍能通过 section-content overlap 解析到 support；
15. cue-depleted paraphrase pressure suite 是否诚实暴露了自然问法鲁棒性边界，而不是把每条自然 query 都调到 pass；
16. decoy queries 是否没有误放 support，尤其是 action-mode 和 implementation/runtime decoy；
17. 默认主 harness 是否已经真正排除 `_runtime_test_fixtures`，且 clean corpus rerun 不再只是补救性旁证；
18. judge-only semantic support packet 是否是 ready_not_judged，而不是误写成 semantic support 已完成；
19. author-side scripted semantic support self-check 是否只应算作者侧自检，而不能算 independent manual review、external blind relevance 或 Pro judgment；
20. 还有没有 P0 / runtime adoption / live LLM-tool / vector-graph retrieval / semantic groundedness 的 overclaim。

请直接给：

- overall verdict
- can keep as sandbox runtime evidence: yes/no
- does it improve over v2: yes/no
- does it prove Source Intake P0 passed: yes/no
- does it prove generic production runtime validated: yes/no
- does it prove external/blind semantic support completed: yes/no
- fallback removal status
- judge-only packet readiness
- clean corpus rerun status
- query policy / authority bucket receipt status
- receipt-effect nonzero bucket exclusion status
- default restricted policy case status
- source_annotation bucket receipt-effect status
- reviewed bucket receipt-effect status
- most important remaining blocker
- minimum next tests
- overclaims or unsafe wording

边界：这包自称不是 P0 passed，不是 live LLM/tool runtime，不是 vector/graph retrieval，不是 runtime adoption ready。新增 QueryPolicy 是 sandbox receipt contract + receipt-effect test，不是完整 Pro retrieval plane。这里的 live local lexical retrieval 只等于 local Markdown lexical retrieval；dense/vector/sparse/graph/RRF/rerank 仍未实现。semantic support 仍未完成独立/外部 judge；judge-only packet 只是准备给双判使用。请不要按这些强结论审；请审它是否足够支撑“generic read-only pack/use sandbox evidence + QueryPolicy receipt first step + nonzero bucket exclusion evidence”。
