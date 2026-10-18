---
type: user_notes
status: ready
created_at: 2026-06-12
scope: plain-language handoff
---

# Notes For User

人话版：

```text
这轮不是证明 Yuxi，也不是开 C-lite。
这轮是把 VAKS 自己的 Source Intake 边界打硬。
```

已经做成的硬结果：

```text
枚举锁死了
旧字段漂移清掉了
当前 lint 语料是 219 个 collected files，其中 166 个 validated intake surfaces，53 个 skipped
当前结构层是 0 hard error，但语义层还有 122 个 warning 债
warning 主要是 source why_saved 占位迁移债，以及 4 个缺正文收录理由的 raw source
已把 confirmed overlay 占位、raw source 顶层 confidence/relations 升级 hard error；soft source metadata 已从 11 个文件顶层下沉到 legacy_raw_metadata
已收紧 enum：pack_allowed 用 none；长期 overlay_state 不含 suggested；intake record_kind 不含 graph_neighbor；promotion_gate 不含 review_passed
已把 warning 分层：118 个可延期迁移债，4 个高风险人工复核，当前 0 个 hard-error 类残留
raw source 的 why_saved 占位现在必须正文有真实收录理由才算可延期债；当前有 4 个被单独拉到高风险人工复核
已把 legacy Project Lens 17 个文件移到 _legacy_project_lens，不再算 canonical current lint，下游消费默认禁止，并留 tombstone
33 个故意失败案例全部被挡
legacy_raw_metadata 现在是 audit/tombstone 子树，检索、图谱、pack、support checker 默认必须忽略
SOURCE_INTAKE 顶部成熟度已从 active/high 降为 sandbox_contract_candidate/medium
core docs 只能吸收边界原则，不能吸收 P0 passed / validator complete / runtime ready 这类结论
现在不能再笼统说 pass_with_warnings，准确说法是“结构层通过，语义债未清，P0 未通过”
迁移策略是不激进清零 warning：保守红区清理 + 中间模式安全隔离，剩余 why_saved 不自动编
最终 warning 策略已单独成文：安全迁移债继续显性保留，真红区升级 hard error，legacy Project Lens 不进 canonical P0 scope
复核包里会包含这 219 个 canonical current lint 文件和 17 个 legacy compatibility 文件，Pro 解压后可以重跑检查
复核包里现在有单独 current lint corpus manifest
复核包里现在也包含 PACKAGE_CHECK.json；解压后没有嵌套 zip 时，package validator 会跳过 zip-entry 检查而不是直接失败
复核包已准备给 Pro 查
```

需要 Pro 重点看的不是“理念对不对”，而是：

```text
validator 还有没有漏洞
frontmatter 机械归一的 placeholder warning 应该留 warning 还是升级 error
raw source 里的 confidence/relations 旧字段是否必须清理或降级
freshness/relevance/source_quality/cross_source_count 下沉到 legacy_raw_metadata 是否合适
legacy project_lens_overlay 是 warning 兼容保留，还是应该迁移/排除
duplicate YAML key 检测是否足够
SOURCE_INTAKE 顶部 maturity 字段是否还需要更保守
core docs 是否只能吸收原则性 contract wording，而不能吸收验证结论
source-card authority cleanup 和 red-zone cleanup 的转换是否可接受
enum v2.6 的四个收口是否正确
warning v2.7 的分类和动作是否正确
legacy Project Lens v2.9 直接排除并归档方式是否正确
why_saved placeholder / author unknown / legacy kp_ref 这三类字段的最终分级是否正确
剩余 122 个 warning 是否可以作为 migration/manual-review debt 保留
这是否足以说 Source Intake P0 passed，还是只能说 sandbox hardening v2 更强
结构层 pass 和语义层 pass 是否应该继续分开写
下一步是否需要更多真实 query-run / context-pack receipts
静态 validator 之外，是否必须补 read-only answer/use-loop trace
迁移策略是否应该继续保持 conservative_plus_safe_middle，而不是激进清零 warning
最终 warning 策略是否够清楚：哪些能留 migration debt，哪些必须 hard error，legacy lens 是否应继续排除
```
