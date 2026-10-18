---
type: candidate_blackbox_analysis
status: draft
title: "cBrain 1.3.2 离线包黑盒设计拆解"
created_at: "2026-06-11"
created_by: Codex
processing_level: medium
processing_tier: medium
knowledge_status: candidate
overlay_state: retrieval_layer_workspace
source_url: https://cbrain.site/download
package_name: cBrain-1.3.2.zip
package_size_bytes: 159649337
package_sha256: D13D97F842F3394FF17D0B94CC53174B01C290AE2460986E2A246125FE42CAB8
analysis_scope:
  - public download response metadata
  - zip directory listing
  - public default-data files
  - public cBrain documentation nodes
excluded_scope:
  - app.asar code inspection
  - decompilation
  - license bypass
  - cracking
  - runtime execution
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: blackbox_candidate_not_action_basis
action_basis_allowed: false
truth_mutation_allowed: false
projects:
  - verified-action-knowledge-system
topics:
  - retrieval-workbench
  - local-first-data-layout
  - graph-plus-markdown
  - exportable-context-pack
  - migration-strategy
borrow_value: strong
borrow_order: P1_for_data_shape_and_workbench_P2_for_retrieval_engine
tags:
  - candidate-only
  - blackbox-analysis
  - retrieval-layer-design
  - cbrain
---

# cBrain 离线包黑盒设计拆解

## 边界

这不是破解，也不是反编译。

本记录只看公开下载包的目录结构、公开默认数据、公开说明节点。没有运行程序，没有打开 `resources/app.asar` 里的代码，没有绕授权。

## 包元信息

公开下载地址返回：

```yaml
url: https://cbrain.site/download
content_disposition: attachment; filename=cBrain-1.3.2.zip
content_type: application/zip
content_length: 159649337
last_modified_gmt: 2026-05-07 13:36:08
zip_sha256: D13D97F842F3394FF17D0B94CC53174B01C290AE2460986E2A246125FE42CAB8
```

zip 目录统计：

```yaml
entry_count: 4257
uncompressed_bytes: 418562332
top_level: cBrain-1.3.2
notable_entries:
  - cBrain导图笔记.exe
  - LICENSE.electron.txt
  - LICENSES.chromium.html
  - resources/app.asar
  - default-data/graph.json
  - default-data/notes/*.md
  - default-data/canvas/*.json
  - default-data/books.json
  - default-data/objective.json
  - default-data/task.json
  - default-data/time.json
```

从 `LICENSE.electron.txt`、`LICENSES.chromium.html`、`resources/app.asar`
这些文件名可以判断：它至少使用了 Electron/Chromium 打包形态。这里不进一步检查私有代码。

## 公开默认数据形态

`default-data` 暴露出来的产品数据模型大致是：

```text
graph.json        = 节点和连接的图结构
notes/*.md        = 每个节点对应的 Markdown 正文
books.json        = 图书对象，可挂节点
canvas/*.json     = 白板/画布对象，包含 state 和 elements
drawings.json     = 画板对象索引，可挂节点
music.json        = 音乐对象，可挂节点
objective.json    = 目标对象，可挂节点
task.json         = 任务对象，可挂节点或目标
time.json         = 时间记录对象，挂任务
images/           = 资源文件
```

实测默认数据规模：

```yaml
graph_nodes: 4177
graph_links: 18312
markdown_note_files: 4177
markdown_note_bytes: 5225487
books: 649
objectives: 154
tasks: 199
time_records: 670
drawings: 12
music_items: 45
canvas_json_files: 29
```

节点字段稳定出现：

```text
fileName / othername / createTime / kq / topic / updateTime / id / nodeType / status / linkInfo
```

连接字段稳定出现：

```text
nodeId1 / nodeId2 / createTime / columnId / interaction / linkType / updateTime / status
```

这说明它不是把所有东西塞进一篇笔记，而是把系统拆成：

```text
node identity
-> graph links
-> markdown note body
-> domain object records
-> visual canvas/resource records
```

## 公开说明里的产品逻辑

公开节点说明还显示出几个重要倾向：

```text
本地版数据存用户本地，不上传服务器。
在线版和离线版数据不互通。
换设备靠复制本地文件夹和软件。
导出支持 Markdown / PDF / HTML / Excel / 全部笔记文件夹。
给 AI 的导出支持 json / markdown，且有标准版、全量版、仅导图、仅文字等模式。
迁移不追求一次性搬完，而是用到哪里迁移哪里。
搜索包含节点搜索、笔记搜索、子树搜索、历史记录、随机回顾等入口。
```

说人话：它不是单纯做“搜索”，而是把知识管理设计成一套
**本地数据包 + 图导航 + Markdown 正文 + 多对象挂载 + 导出给人/AI** 的工作台。

## 对 VAKS 检索层的借鉴

### 1. 借数据形态，不借私有实现

VAKS 可以借这个形态：

```text
stable anchor id
human-readable title / alias
markdown body path
relation cache
domain object links
activation / coverage signal
export modes
```

不要借：

```text
私有 app 代码
封闭数据库作为真值
UI 连接数当可靠性
本地结果当已审证据
```

### 2. Graph + Markdown 比纯向量库更适合我们

VAKS 需要的是：

```text
Markdown/YAML 仍然做人类可审计源
graph/cache/index 只做可重建检索层
```

cBrain 的公开数据正好提醒我们：

```text
图结构负责找路
Markdown 负责正文
对象表负责工作流
导出负责迁移和 AI 协作
```

这比“所有东西进一个向量库”更接近 VAKS。

### 3. 检索结果应该是工作台卡片

从 cBrain 的节点逻辑看，一个结果不该只是文件名或相似度分数，而应该是：

```text
node_id / anchor_id
title / alias
body_path
graph_neighbors
domain_links
coverage_hint
allowed_use
open / export / build pack / review
```

VAKS 可以改成：

```text
result hit
-> anchor card
-> show layer/status/use limit
-> show supporting/challenging/risk/stale nearby context
-> build context pack only when allowed
```

### 4. AI 导出模式很值得借

cBrain 公开说明里提到导出当前导图数据给 AI，并区分标准版、全量版、仅导图、仅文字。

VAKS 可以转译为：

```text
context_pack_standard
context_pack_full_audit
structure_only
text_only
evidence_packet
risk_and_gap_only
```

关键区别：

```text
cBrain 导出是帮助 AI 理解知识。
VAKS 导出还必须携带 authority / allowed_use / support_status。
```

### 5. 迁移策略很实用

cBrain 的迁移观点是：不要追求一次性完整搬家，重要内容先迁移，用到哪里迁移哪里。

VAKS 可以借成：

```text
lazy migration
query-triggered intake
source-first retention
candidate-only staging
promotion later
```

这和我们现在的 VAKS intake 边界一致。

## 对我们定制检索层的新增设计假设

可以把 VAKS 检索层拆成这几块：

```text
1. durable_markdown_store
   source cards / candidate distillations / reviewed notes / decisions

2. anchor_manifest
   stable ids, titles, aliases, headings, source paths, hashes

3. relation_activation_cache
   derived links, topic neighborhoods, project overlays, stale/conflict hints

4. domain_object_links
   tasks, decisions, feedback events, context packs, use ledger records

5. retrieval_index
   BM25 / sparse / vector / rerank, all rebuildable from durable store

6. export_pack_modes
   standard / audit / structure-only / text-only / evidence / risk-gap
```

核心原则不变：

```text
data shape can help retrieval
retrieval output can help activation
activation cannot mutate truth
local/offline does not mean reviewed
graph link does not mean evidence support
```

## 融合判断

```yaml
fusion_decision: adapt-for-data-shape-and-workbench
borrow_value: strong
borrow_order: P1_for_data_shape_and_workbench_P2_for_retrieval_engine
mainline_change_now: no
pilot_needed: yes
best_layer:
  - retrieval workbench
  - anchor manifest
  - rebuildable relation cache
  - context pack export modes
  - lazy migration workflow
avoid_layer:
  - reviewed truth
  - evidence support
  - action basis
  - private implementation
```
