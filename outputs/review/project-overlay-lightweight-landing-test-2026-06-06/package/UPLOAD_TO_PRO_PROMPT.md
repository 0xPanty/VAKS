# Upload Prompt For Pro

请复核这个新包：

```text
project-overlay-lightweight-landing-test-2026-06-06.zip
```

背景：

上一轮七候选压力测试证明 project-scoped sidecar overlay 对 Codex/agent
维护项目有帮助，但把 Project Lens 对象模型、字段、snapshot、closeout
lifecycle、retrieval precedence 等推进主线会变重。

你建议收束成：

```text
keep sandbox only
mainline minimal wording only
do not mainline the object model
do not change schema / review queue / templates
```

本包按这个建议做了一版轻量落地：

- 一个项目一张 borrowing list / Project Overlay。
- live entry 只保留 `kp_ref`、`stance`、`borrow_scope`、`updated_at`。
- `target_hint` 只作路径/符号/命令导航，不写 health/support。
- live stance 只用 `watch / partial / avoid / defer`。
- outcome 与 live stance 分离。
- snapshot 降级成 scoped `candidate experience note` / `candidate boundary note`。
- closeout 只作为 drain note，不做 lifecycle state machine。
- retrieval 只保留一条 plain default read order，不做 priority/authority mechanism。
- 不改 `ARCHITECTURE_PRINCIPLES.md`、`FUSION_ARCHITECTURE_V0_2_DRAFT.md`、
  `SCHEMA.md`、`REVIEW_QUEUE.md`、`templates/`。

请重点调研/复核：

1. 这版是否已经足够轻，还是仍然像一个对象系统？
2. 哪些字段/词还会让人误读成 truth、ADR、action basis 或 project approval？
3. `candidate experience note` / `candidate boundary note` 是否足够弱？是否还会像 best practice / universal ban？
4. `watch / partial / avoid / defer` 是否合适？`avoid` 是否仍有 universal-ban 风险？
5. 默认读序是否应该继续保留，还是进一步压成更口语的操作建议？
6. `closeout drain` 是否应保留为硬规则？
7. 下一步是不是应该做真正 blind non-author pass，而不是继续改主线？

请尽量最大可能保留已经证明有用的功能：

```text
kp_ref
optional target_hint
stance/outcome separation
closeout drain
archive/tombstone hygiene
action-facing return to v0.2.13
cross-project isolation
```

但请继续帮我们压掉不必要的制度感。

