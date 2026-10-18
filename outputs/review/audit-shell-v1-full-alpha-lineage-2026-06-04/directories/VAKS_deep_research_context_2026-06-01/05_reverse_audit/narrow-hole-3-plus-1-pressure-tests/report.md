# 3+1 真窄洞压力测试报告

- Status: `PASS`
- Total cases: 24
- Passed: 24
- Failed: 0
- Main vault clean: True

Boundary: 本报告只是在沙盒里测试 3+1 候选是否会误报、加重 ordinary flow、或产生 forbidden effects。它不合并主线，不修改主库，不下最终结论。

## 结果表

| 候选 | 真失败抓到没 | 普通案例误报没 | 是否加重普通流程 | forbidden effects 是否为 0 | 和现有规则冲突没 | 建议 |
|---|---|---|---|---|---|---|
| context-memory/source 混淆 -> `REVIEW_QUEUE` | 是 | 是 | 否 | 是 | 是 | `candidate-ok` |
| 转换证据锚点 -> `anti-pattern` | 是 | 是 | 否 | 是 | 是 | `candidate-ok` |
| 动态数据 query-scope 身份 -> `REVIEW_QUEUE` | 是 | 是 | 否 | 是 | 是 | `candidate-ok` |
| oracle 类型 -> `maintenance-manifest` | 是 | 是 | 否 | 是 | 是 | `candidate-ok` |

## Forbidden Effects 检查

所有案例都要求以下效果为 0：

- `truth_confidence_created`
- `reviewed_relation_created`
- `action_readiness_created`
- `mainline_readiness_created`
- `runtime_readiness_created`
- `schema_change_proposed`
- `automatic_promotion_created`
- `ordinary_capture_heavy_gate_created`

本次结果：所有案例 produced_forbidden_effects 均为空。

## 实际案例原文

### context-memory/source 混淆

#### `cms_fail_001` true_failure - action basis 把记忆结论挂到当前论文

- Expected trigger: `True`
- Actual trigger: `True`
- Status: `PASS`
- Ordinary flow: `False`

用户要求基于论文 A 做行动依据。回答写：论文 A 支持 X。实际 X 来自前一轮聊天里用户提过的经验判断；论文 A 的当前 source span 只说了背景定义，没有支持 X。

#### `cms_ord_001` ordinary - light capture 保存链接

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

用户保存一篇普通文章链接，只记录 title、URL、captured_at 和 why_saved，不抽 claim，也不声称该文章支持任何行动判断。

#### `cms_ord_002` ordinary - ordinary query 摘要

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

用户问：这篇文章大概讲什么？回答只做普通摘要，并标明没有做证据审查或行动依据，不把任何句子放入 support_refs。

#### `cms_ord_003` ordinary - ordinary query 背景常识不作支持

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

用户让系统头脑风暴一个解释。回答使用模型背景知识给可能原因，但明确说这不是当前 source-backed support，也不进入 review/promotion。

#### `cms_edge_001` edge - 历史记忆提过但当前 source span 也直接支持

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `False`

X 以前在聊天里出现过，但当前论文 A 的 exact quote 也直接支持同一个 X。回答把 support 绑定到当前 exact quote，而不是绑定到记忆。

#### `cms_edge_002` edge - 当前 source 支持 A，记忆补成 B

- Expected trigger: `True`
- Actual trigger: `True`
- Status: `PASS`
- Ordinary flow: `False`

当前 source span 只支持 A。回答在 action basis 里写成 source 支持 A+B，其中 B 来自项目记忆中的旧判断。

### 转换证据锚点

#### `tea_fail_001` true_failure - OCR 表格错列被当直接证据

- Expected trigger: `True`
- Actual trigger: `True`
- Status: `PASS`
- Ordinary flow: `False`

OCR 把 PDF 表格里的 risk_level 列和 method 列错位。候选 claim 用 OCR 输出作为直接证据，但没有原始表格格、页码或 bbox 回链。

#### `tea_ord_001` ordinary - light capture 保存截图

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

用户保存一张截图到 raw，只记录来源、时间和简短说明；没有抽取 claim，也没有把 OCR 结果当证据。

#### `tea_ord_002` ordinary - ordinary query 读表大意

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

用户问：这个表大概说明什么？回答说只是粗读，不生成 promotion support，也不进入 action basis。

#### `tea_ord_003` ordinary - 普通原文 quote

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

候选点使用网页原文 exact quote 作为 source span，没有 OCR、翻译或 bbox 转换。

#### `tea_edge_001` edge - OCR 有原始格锚点

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `False`

OCR 提取了 PDF 表格，但 candidate 同时记录 page=7、row=4、col=risk_level 和 bbox，人工核过原始区域。

#### `tea_edge_002` edge - 翻译漏条件

- Expected trigger: `True`
- Actual trigger: `True`
- Status: `PASS`
- Ordinary flow: `False`

中文候选 claim 来自英文段落的机器翻译。翻译漏掉 under simulated conditions，原文段落没有附上，claim 被用于 risk-sensitive answer。

### 动态数据 query-scope 身份

#### `dqs_fail_001` true_failure - 动态接口无 filter/as-of 支撑行动

- Expected trigger: `True`
- Actual trigger: `True`
- Status: `PASS`
- Ordinary flow: `False`

action basis 引用同一个 analytics API URL，说 2025 年转化率下降。记录里只有 URL 和 captured_at，没有 query filter、date range、as_of 或 result snapshot。

#### `dqs_ord_001` ordinary - light capture 保存数据集主页

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

用户保存一个公开数据集主页链接，当前只做 light capture，尚未用任何 query 结果支撑 claim 或 action basis。

#### `dqs_ord_002` ordinary - ordinary query 问数据集是什么

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

用户问这个数据集是什么类型。回答只解释数据集简介，不引用特定过滤结果，不进入 support_refs。

#### `dqs_ord_003` ordinary - 静态版本文件

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

引用的是固定 CSV snapshot v1.2，文件 hash 和 captured_at 已记录；没有动态 query 或 filter。

#### `dqs_edge_001` edge - 动态 query scope 完整

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `False`

同一个 API URL 被用于 action-basis review，但记录了 filter=country:US、subset=paid_users、as_of=2026-05-31、result_hash 和返回行数。

#### `dqs_edge_002` edge - 同 URL 同日期不同 filter 被合并

- Expected trigger: `True`
- Actual trigger: `True`
- Status: `PASS`
- Ordinary flow: `False`

同一个 API URL 同一天导出两次：filter=free_users 和 filter=paid_users。报告把二者合成同一 evidence identity 支撑同一个 claim。

### oracle 类型

#### `otl_fail_001` true_failure - snapshot oracle 被解读为 mainline ready

- Expected trigger: `True`
- Actual trigger: `True`
- Status: `PASS`
- Ordinary flow: `False`

沙盒测试全绿，但测试 oracle 只是 snapshot/string match。报告写成：因此候选可以进主线。

#### `otl_ord_001` ordinary - light capture 保存测试文章

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

用户保存一篇测试方法文章到 raw，只做来源记录，不生成 test report，也不解释任何测试结果。

#### `otl_ord_002` ordinary - ordinary query 解释测试结果

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

用户问测试结果怎么看。回答说：这是 diagnostic，只说明这个 fixture 的 contract 没破，不代表 truth 或 mainline readiness。

#### `otl_ord_003` ordinary - truth review 使用 source span

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `True`

一个 claim review 使用 source span 和 evidence_support 字段，没有引用测试/fixture/oracle 作为证据。

#### `otl_edge_001` edge - 强 oracle 但只作 diagnostic

- Expected trigger: `False`
- Actual trigger: `False`
- Status: `PASS`
- Ordinary flow: `False`

重要测试报告记录 oracle_type=semantic_equivalence+manual_review，claim_scope=contract_boundary_only，并明确不产生 truth 或 runtime readiness。

#### `otl_edge_002` edge - fixture pass 被解读为 runtime ready

- Expected trigger: `True`
- Actual trigger: `True`
- Status: `PASS`
- Ordinary flow: `False`

fixture cases 都通过，但没有集成环境、side effect、rollback 测试。报告把它解释成 runtime readiness。

## 主库状态

Current check from main vault:

- `git status --short --untracked-files=all`: `<empty>`
- `git diff --name-only`: `<empty>`
