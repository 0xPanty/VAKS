请你作为独立架构审查者，复核 VAKS / 资料库 的 Project Lens 是否应该进入真实主架构。

背景：

1. v0.2.13 最小主线规则已经落地：真正用于 action_basis / significant promotion / decision / risk-sensitive use 时，不能只列 evidence list，必须说明 non-circular warrant。
2. Project Lens 是新候选设计：项目侧联 sidecar overlay，用来记录当前项目如何临时看待通用知识点。
3. Project Lens 不是 schema、template、ADR、reviewed knowledge、truth layer、action basis，也不是正式开发区目录。
4. 我们已经做了两类测试：
   - candidate sidecar 高强度测试；
   - 完整主架构副本实插入测试。

请重点阅读：

```text
03_FULL_MAINLINE_COPY_INSERTION_TEST/FULL_MAINLINE_COPY_INSERTION_TEST_REPORT.md
03_FULL_MAINLINE_COPY_INSERTION_TEST/with-project-lens/FUSION_ARCHITECTURE_V0_2_DRAFT.md
03_FULL_MAINLINE_COPY_INSERTION_TEST/with-project-lens/ARCHITECTURE_PRINCIPLES.md
01_CURRENT_LANDED_MAINLINE/FUSION_ARCHITECTURE_V0_2_DRAFT.md
01_CURRENT_LANDED_MAINLINE/ARCHITECTURE_PRINCIPLES.md
04_HIGH_INTENSITY_SIDECAR_TEST/HIGH_INTENSITY_GAUNTLET.md
02_PROJECT_LENS_CANDIDATE/project_lens_overlays/VAKS.md
```

请回答：

1. Verdict: accept_to_mainline_minimal / revise_wording / keep_sandboxed / reject_for_now。
2. 如果 accept_to_mainline_minimal：应该放进哪些文件、哪些位置、用什么最小 wording？
3. 如果 revise_wording：请给出可直接 patch 的替代 wording。
4. 是否存在 authority leakage：Project Lens 会不会被误读成 reviewed truth、ADR、decision、action basis、schema/template？
5. 是否与 v0.2.13 的 late-stage action-facing review requirement 冲突，还是互补？
6. 是否应该保留 `kp_ref`、structured `target_hint`、`conceptual` target status、`outcome_ref`，还是这些只能留在 sidecar 实现层？
7. 是否有任何 blocker 会阻止 scoped commit？
8. 请明确哪些东西仍然不能并入主线：schema、template、formal folders、graph-lite、pipeline、governance、automation 等。

请用中文回答，优先说人话，但保留足够的架构判断依据。

