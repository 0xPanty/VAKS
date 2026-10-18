---
type: source_refresh_distillation
status: candidate_only
created_at: 2026-06-06
source_record: raw/repos/2026-05-26-llm-wiki-source.md
source_url: https://github.com/nashsu/llm_wiki
checked_commit: 21bab39766a387cc161b3d4a56eb8be099dffca7
checked_version: 0.4.20
snapshot_location: raw/repos/_snapshots/nashsu-llm-wiki-21bab39766a387cc161b3d4a56eb8be099dffca7.zip
snapshot_sha256: 05F8984B5713F5B8B8295749946C664FB7D00BB6B72E828EFABD9C463EF78E82
truth_boundary: refresh and candidate distillation only; not reviewed knowledge; not architecture decision; not action basis
projects:
  - verified-action-knowledge-system
related_existing_records:
  - wiki/summaries/2026-05-26-llm-wiki-architecture-review.md
  - outputs/qa/2026-05-26-llm-wiki-value-analysis.md
  - outputs/qa/2026-05-26-llm-wiki-implementation-extraction.md
  - wiki/decisions/2026-05-26-llm-wiki-fusion-compatibility.md
tags:
  - llm-wiki
  - source-refresh
  - karpathy-pattern
  - candidate-only
---

# nashsu/llm_wiki Short Refresh

## 一句话结论

这条短帖对 VAKS **有帮助，但不是新方向**。

它强化了我们已经吸收过的判断：

```text
llm_wiki = 自动知识编译机 / 工程发动机 / 操作台参考
VAKS = verified knowledge graph / review gate / action-basis 纪律
```

所以处理方式不是“引入 llm_wiki 替代 VAKS”，而是继续把它当工程参考。

## 这次短帖说了什么

短帖把 `nashsu/llm_wiki` 概括为 Karpathy LLM Wiki 模式的桌面产品：

```text
不是每次查询都从头 RAG。
而是把 sources 增量编译成持久 wiki。
wiki 保持更新，查询时读已经编译好的知识库。
```

它强调的功能包括：

- `Raw Sources -> Wiki -> Schema`
- Obsidian-compatible wikilink
- two-step ingest
- multimodal image extraction
- four-signal knowledge graph
- Louvain community detection
- Deep Research
- local HTTP API
- MCP / Agent Skill

## 当前源头刷新

这次重新核了 GitHub 和源码 snapshot：

```text
repo: nashsu/llm_wiki
checked_commit: 21bab39766a387cc161b3d4a56eb8be099dffca7
commit_time: 2026-06-05T09:48:49Z
package_version: 0.4.20
snapshot_sha256: 05F8984B5713F5B8B8295749946C664FB7D00BB6B72E828EFABD9C463EF78E82
```

确认源头仍然支持短帖里的主要说法：

- README 明确说它是 cross-platform desktop application。
- README 明确保留 Karpathy 的三层、三操作、index/log、wikilink、frontmatter、Obsidian compatibility。
- `package.json` 显示版本 `0.4.20`。
- `src/lib/graph-relevance.ts` 仍有四信号关系模型。
- `src/lib/wiki-graph.ts` 使用 `graphology-communities-louvain`。
- `src-tauri/src/api_server.rs` 仍绑定 `19828` 并提供项目、文件、搜索、图谱、rescan 等 API。
- `mcp-server/` 提供 MCP 工具：projects、files、search、graph、rescan。

## 对 VAKS 的帮助

### 1. two-step ingest 可以继续借

对 VAKS 有价值的是：

```text
先分析资料
再生成候选 wiki / candidate point
```

这和 VAKS 的边界兼容：

```text
source -> candidate comprehension -> review
```

不能借成：

```text
source -> generated wiki -> truth
```

### 2. local API / MCP 是中期参考

`llm_wiki` 的 API/MCP 证明了一个方向：

```text
本地知识库可以被 agent 调用
但默认应返回可核查路径和查询结果
```

VAKS 未来如果做 API，不应只返回普通搜索结果，而应返回：

```text
context pack
verification_status
evidence_level
confidence
risk / gaps / review_due
source anchors
```

### 3. 图谱和 Louvain 只能做 activation / diagnostics

四信号图谱和 Louvain 有用，但用途是：

```text
发现邻域
找孤岛
找桥接点
找可能的社区
提示 missing point / review_due
```

不能变成：

```text
graph rank = trust
community = reviewed taxonomy
high score = evidence support
```

### 4. Deep Research 只能进候选层

Deep Research 的价值是扩展搜索和补资料。

对 VAKS 来说，它只能产生：

```text
raw source
candidate point
missing evidence
review question
```

不能直接产生：

```text
reviewed claim
reviewed relation
action-ready conclusion
```

### 5. 多模态图片提取值得作为 source support

PDF / 网页图片的 factual caption 对 VAKS 有用，尤其是论文图、架构图、截图。

边界是：

```text
image caption = extraction aid
not evidence support by itself
not final interpretation
```

## 采纳判断

```text
already_processed
refresh_confirms_existing_distillation
no_new_mainline_architecture_change
watch_for_engineering_reference
```

当前最佳用法：

- 继续保留 `llm_wiki` 作为实现级参考。
- 不把完整桌面 app 纳入 VAKS 主线。
- 不把 Deep Research / graph / vector search 当 truth engine。
- 如果未来做 VAKS API，优先做 evidence-aware context pack resolver，而不是普通 wiki search API。

## 和现有记录的关系

这条短帖没有替代旧蒸馏。

旧记录仍是主判断：

- `wiki/summaries/2026-05-26-llm-wiki-architecture-review.md`
- `outputs/qa/2026-05-26-llm-wiki-value-analysis.md`
- `outputs/qa/2026-05-26-llm-wiki-implementation-extraction.md`
- `wiki/decisions/2026-05-26-llm-wiki-fusion-compatibility.md`

本文件只是把 2026-06-06 的短帖触发和当前 repo 状态补上。
