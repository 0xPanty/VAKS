---
type: implementation_extraction
status: recorded
created: 2026-05-26
source_repo: https://github.com/nashsu/llm_wiki
source_commit: ff84ee9ec131c4ae8ee4f5b14069276a19634c18
local_snapshot: C:/Users/Administrator/AppData/Local/Temp/llm_wiki_zip/llm_wiki-main
local_snapshot_status: temporary
related_summary:
  - wiki/summaries/2026-05-26-llm-wiki-architecture-review.md
related_decision:
  - wiki/decisions/2026-05-26-llm-wiki-fusion-compatibility.md
confidence: high
---

# 实现级提取：llm_wiki 代码里值得防错的设计

## 结论

`llm_wiki` 不只提供架构概念，它的源码里有一批防错设计。以后自己写资料库自动化时，不能只记“要做 ingest / graph / API”，还要保留这些实现不变量。

## 已读核心文件

- `src/lib/templates.ts`
- `src/lib/ingest.ts`
- `src/lib/ingest-cache.ts`
- `src/lib/ingest-queue.ts`
- `src/lib/graph-relevance.ts`
- `src/lib/wiki-graph.ts`
- `src/lib/graph-insights.ts`
- `src/lib/search.ts`
- `src-tauri/src/commands/search.rs`
- `src-tauri/src/api_server.rs`
- `src/lib/source-lifecycle.ts`
- `src/lib/project-file-sync.ts`
- `src-tauri/src/commands/file_sync.rs`
- `src/lib/project-identity.ts`
- `src/lib/wiki-page-delete.ts`
- `src-tauri/src/commands/vectorstore.rs`

UI 组件没有作为核心吸收对象。

## 可复用实现不变量

### 1. 模板层：purpose 和 schema 要分开

来源：`src/lib/templates.ts`

不变量：

- `purpose.md` 管“为什么做、研究范围、关键问题、当前 thesis”。
- `schema.md` 管“页面类型、命名、frontmatter、索引、日志、链接规则”。
- 不同场景用不同模板，但底层结构保持一致。

对本资料库的启发：

- 我们需要 `purpose.md`，但 schema 要扩展为 verified knowledge 字段。

### 2. Ingest 不能让 LLM 直接乱写文件

来源：`src/lib/ingest.ts`

不变量：

- ingest 分两步：先分析资料，再生成 wiki 文件。
- LLM 生成文件必须用受控 FILE block。
- 写入前必须检查路径，只允许写入 `wiki/`。
- 要防 `..`、绝对路径、Windows 保留名、控制字符、空路径。
- FILE block parser 要处理 CRLF、大小写/空格变体、代码块里的 `---END FILE---`、未闭合块警告。

对本资料库的启发：

- 未来写 source compiler 时，LLM 输出必须先进入 parse + validate，不能直接写盘。

### 3. 自动写入要有 project lock

来源：`src/lib/ingest.ts`

不变量：

- ingest 期间会读旧 index，再写新 index。
- 同一项目必须串行，避免两个 LLM 同时基于旧 index 写回，把彼此覆盖。

对本资料库的启发：

- 即使一开始只是脚本，也要避免并发编译同一个 vault。

### 4. Cache 命中必须检查产物仍存在

来源：`src/lib/ingest-cache.ts`

不变量：

- 用 SHA256 判断 source 内容是否变化。
- 但 cache hit 只有在上次写出的文件仍存在时才有效。
- 如果产物缺失，应重新 ingest，不能相信缓存。

对本资料库的启发：

- 未来 `raw -> wiki` 编译缓存要记录 input hash + output paths + schema version。

### 5. Queue 要能恢复、取消、重试和清理

来源：`src/lib/ingest-queue.ts`

不变量：

- task 状态包括 pending / processing / done / failed。
- 队列持久化到 `.llm-wiki/ingest-queue.json`。
- processing 被中断后要恢复成 pending。
- cancel processing 时要 abort LLM call，并清理已经写出的文件。
- 每个任务绑定稳定 project id，而不是只绑定路径。
- 切换项目时要有 stale-context guard，避免旧任务写到新项目。

对本资料库的启发：

- 早期可以不用 queue，但一旦有自动 ingest，就必须有这些边界。

### 6. Project identity 不应依赖路径

来源：`src/lib/project-identity.ts`

不变量：

- 项目有稳定 UUID。
- 全局 registry 记录 UUID -> 当前路径。
- 文件夹移动后，任务仍能找到项目。

对本资料库的启发：

- 如果以后做 App/API，不要把绝对路径当长期身份。

### 7. 删除 source 要保护共享知识页

来源：`src/lib/source-lifecycle.ts`、`src/lib/wiki-page-delete.ts`

不变量：

- 删除 raw source 后，只删除完全依赖该 source 的 wiki 页面。
- 如果页面还有其他 sources，只移除被删 source，不删页面。
- 删除 wiki 页时要清理 index、body wikilinks、frontmatter `related`、embedding、source media。

对本资料库的启发：

- 我们未来的 `sources[]` 不是摆设，它决定删除和可信度回溯。

### 8. Graph score 是关系信号，不是真值信号

来源：`src/lib/graph-relevance.ts`、`src/lib/wiki-graph.ts`、`src/lib/graph-insights.ts`

不变量：

- direct link、source overlap、common neighbor、type affinity 可以合成关系分。
- 低连接孤岛、低内聚社区、桥接节点可以做 health check。
- Louvain 社区检测只有在节点规模足够时才值得上。

对本资料库的启发：

- 我们可以借四信号做 relation score。
- 但必须叠加 source quality / evidence level，否则垃圾来源会被图谱放大。

### 9. Search 要先做确定性，再选配向量

来源：`src/lib/search.ts`、`src-tauri/src/commands/search.rs`

不变量：

- 先做关键词搜索、标题加权、短语加权、CJK bigram。
- 可选向量搜索，不开启也能工作。
- 关键词结果和向量结果用 RRF 合并。
- 搜索要有文件数量上限、结果上限、Unicode-safe snippet。

对本资料库的启发：

- 早期不要上 Zilliz / LanceDB。
- 先做本地 deterministic search + index，再考虑向量。

### 10. Local API 必须默认收紧

来源：`src-tauri/src/api_server.rs`

不变量：

- 只绑定 `127.0.0.1`。
- health 可无认证，其他端点要 token。
- 有 body limit、file content limit、rate limit、in-flight limit。
- `safe_join` 防路径穿越。
- 只暴露 `purpose.md`、`schema.md`、`wiki/`、`raw/sources/`，不暴露内部 `.llm-wiki`。
- chat API 没准备好时明确返回 501，不假装支持。

对本资料库的启发：

- 未来 context pack API 必须只读优先，返回验证字段，不能暴露内部状态。

### 11. 文件监听要区分用户改动和应用写入

来源：`src/lib/project-file-sync.ts`、`src-tauri/src/commands/file_sync.rs`

不变量：

- watcher 用 snapshot + queue，不直接看到变动就立刻信任。
- 应用自己写入的路径短时间忽略，避免触发自己。
- raw source watch 有 include/exclude 扩展名、目录、glob、文件大小上限。
- Linux 有周期 rescan，防 watcher 漏事件。

对本资料库的启发：

- 自动监听属于后期；一旦做，就要 snapshot 化，不能靠简单 file event。

### 12. Vector store 是增强层，不是核心层

来源：`src-tauri/src/commands/vectorstore.rs`

不变量：

- chunk-level index 比 page-level 更细。
- page id 要验证，防 filter injection。
- upsert 是先删同 page 旧 chunks，再加新 chunks。
- 空 chunks upsert 是 no-op，不清空旧索引。
- legacy table 有迁移/清理路径。

对本资料库的启发：

- 向量层以后如果做，必须可重建、可删除、可迁移，不作为唯一真值。

## 未来自己实现时的最小顺序

不要从 App 开始。建议顺序：

1. 固化 Markdown schema：source / claim / pattern / anti-pattern / decision。
2. 写 deterministic checker：frontmatter、sources、links、index 是否一致。
3. 写 health report：孤岛、低证据高引用、冲突 claim、stale source。
4. 写 source compiler：LLM 输出先 parse + validate，再写 wiki。
5. 加 cache：input hash + output paths + schema version。
6. 加 review queue：冲突、低置信、重复、缺页先让人判断。
7. 加 relation score：四信号 + source quality gate。
8. 最后再考虑 local API / context pack。

## 不应照搬

- 完整 Tauri App。
- UI 三栏布局。
- 复杂 Deep Research。
- LanceDB/vector 默认开启。
- Louvain 图谱 UI。
- 多 provider 设置页。

这些是产品层，不是当前资料库的核心层。

## 对当前资料库的新增要求

以后每次深读参考库，如果未来可能复刻其机制，都要补一份实现级提取记录。否则只靠架构总结，后续写代码容易丢掉关键边界。
