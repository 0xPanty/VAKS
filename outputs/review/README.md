# Review Queue

这里保存外部 agent 或 Misa/gbrain 产生的候选建议。

本目录不是 truth layer。这里的内容不能直接当作正式 claim、pattern、anti-pattern 或 decision。

## 当前规则

- Misa/gbrain 默认只读正式资料库。
- 候选建议可以进入本目录，等待 Codex/用户复核。
- 复核必须检查来源、证据等级、验证状态、反例、关系边、风险和回退路径。
- 通过复核后，候选内容才能迁移到 `wiki/claims/`、`wiki/patterns/`、`wiki/anti-patterns/` 或 `wiki/decisions/`。

## 候选建议应包含

```yaml
type: review-candidate
status: pending-review
created:
proposed_node_type:
proposed_title:
proposed_by:
sources:
evidence_level:
verification_status:
confidence:
relations: []
reviewer:
review_result:
```

正文应写清：

- 候选结论是什么
- 为什么值得进入资料库
- 支持证据
- 反例或不确定性
- 建议迁移到哪个正式节点类型
- 需要 Codex/用户复核的问题
