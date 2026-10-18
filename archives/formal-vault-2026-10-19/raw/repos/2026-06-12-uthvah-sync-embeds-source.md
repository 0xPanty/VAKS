---
type: source
status: source-captured
title: "uthvah/sync-embeds"
source_id: "github:uthvah/sync-embeds@10703d39548a9772573dced19f49ec05f8449500"
source_uri: "github:uthvah/sync-embeds@10703d39548a9772573dced19f49ec05f8449500"
source_url: "https://github.com/uthvah/sync-embeds"
source_type: repository
owner: uthvah
repo: sync-embeds
author: uthvah
publisher: GitHub
created_at: 2025-09-18T00:55:07Z
updated_at: 2026-06-09T22:26:08Z
pushed_at: 2026-06-05T13:16:04Z
captured_at: 2026-06-12
captured_by: Codex
checked_commit: "10703d39548a9772573dced19f49ec05f8449500"
checked_commit_short: "10703d39548a"
commit_time: 2026-06-05T14:16:04+01:00
commit_subject: "fix: replace unsupported around() property descriptor with Object.defineProperty (#42)"
default_branch: main
license: MIT
repo_visibility: public
source_status: active
github_metadata:
  stars: 95
  forks: 9
  open_issues: 23
  archived: false
manifest:
  id: sync-embeds
  name: "Sync Embeds"
  version: 2.0.2
  min_app_version: "0.15.0"
  is_desktop_only: false
package:
  name: obsidian-sync-embeds
  version: 2.0.0
source_integrity:
  source_hash:
  snapshot_hash: "856F56027033EB53AFFB593C8A08D5807B597EB653AB24588E34A7803036923C"
  ingest_state: new
snapshot_location: "raw/repos/_snapshots/2026-06-12-uthvah-sync-embeds-10703d39548a-source.zip"
adapter_ingest:
  adapter_name: git-clone-and-archive
  adapter_version: git
  capture_method: "git clone --depth 1 + git archive"
  extraction_trace:
    - "GitHub page/API checked"
    - "README, manifest, package, source modules, styles, build config inspected"
    - "npm install --ignore-scripts in temp clone"
    - "production esbuild run in temp clone"
  known_limits:
    - "No Obsidian runtime UI test was performed."
    - "No upstream test suite is present in tracked files."
    - "npm audit reported one moderate dev-dependency issue in esbuild."
raw_location: "raw/repos/_snapshots/2026-06-12-uthvah-sync-embeds-10703d39548a-source.zip"
processing_mode: repo-intake
processing_level: medium
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: raw-only
evidence_granularity: table_or_code_anchor
files_reviewed:
  - README.md
  - manifest.json
  - package.json
  - esbuild.config.mjs
  - src/main.js
  - src/embed-manager.js
  - src/viewport-controller.js
  - src/dynamic-paths.js
  - src/command-interceptor.js
  - src/settings.js
  - styles.css
topics:
  - obsidian
  - synced-embed
  - editable-transclusion
  - workbench-ui
  - dashboard-editing
projects:
  - verified-action-knowledge-system
source_family:
  - obsidian-plugin
  - viewer-workbench-reference
upstream_sources: []
verification_status: source-captured
candidate_relation_suggestions: []
tags:
  - source/repo
  - obsidian/plugin
  - vaks/raw
  - candidate-input
---

# 来源记录：uthvah/sync-embeds

## 为什么收录

用户要求对 `uthvah/sync-embeds` 做“蒸馏”。该仓库是一个 Obsidian 插件：它把普通 `![[...]]` embed 包进 `sync` code block 后，渲染成可编辑、可双向同步的嵌入块。它对 VAKS 的价值不在 truth / review 架构，而在 Obsidian 工作台层：如何从一个 dashboard 或项目页直接编辑源笔记片段，同时减少复制粘贴和上下文切换。

## 来源信息

- 作者：`uthvah`
- 发布方：GitHub
- 原始链接：https://github.com/uthvah/sync-embeds
- 默认分支：`main`
- 检查 commit：`10703d39548a9772573dced19f49ec05f8449500`
- commit 时间：`2026-06-05T14:16:04+01:00`
- commit 标题：`fix: replace unsupported around() property descriptor with Object.defineProperty (#42)`
- GitHub metadata captured：stars 95，forks 9，open issues 23，license MIT，not archived
- Manifest version：`2.0.2`
- Package version：`2.0.0`
- 快照位置：`raw/repos/_snapshots/2026-06-12-uthvah-sync-embeds-10703d39548a-source.zip`
- 快照 SHA256：`856F56027033EB53AFFB593C8A08D5807B597EB653AB24588E34A7803036923C`

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

此 source card 只提供来源身份、快照和源码锚点。它不能作为 VAKS 的采用结论、reviewed pattern、插件安装建议、truth support 或 action basis。

## Source / Code Anchor Matrix

| Anchor | What exists | Why it matters | Boundary |
|---|---|---|---|
| `README.md:16` | 项目定义：将 Obsidian transclusion 变成 live editable synced block。 | 说明它解决的是编辑体验，不是知识校验。 | README 是项目自述，不是独立验证。 |
| `README.md:26-31` | 列出双向同步、快捷键、section/header embed、动态 pattern、header 管理。 | 给出可蒸馏功能范围。 | 功能声明未在真实 Obsidian vault 中复测。 |
| `README.md:37-41` | 解释实现思路：隐藏真实 editor pane 并 re-parent 到当前文档；section embed 用 viewport 限制。 | 核心设计锚点。 | 依赖 Obsidian/CodeMirror DOM 行为，可能随版本漂移。 |
| `README.md:64-118` | `sync` code block 语法、section embed、动态变量、局部显示选项。 | 可借为 VAKS 工作台语法参考。 | 动态路径不等于稳定 provenance anchor。 |
| `README.md:124-140` | Daily dashboard 和 project overview 示例。 | 与 VAKS dashboard / project overview 相邻。 | 示例不是 VAKS 架构结论。 |
| `manifest.json:2-9` | 插件 id/name/version/minAppVersion/isDesktopOnly。 | 插件身份和版本锚点。 | `isDesktopOnly: false` 未经移动端实测。 |
| `package.json:2-20` | 包名、version、build script、依赖 `monkey-around`。 | 暴露版本不一致和 monkey-patching 风险。 | package version 与 manifest version 不一致，需维护检查。 |
| `src/main.js:80` | 注册 `sync` markdown code block processor。 | 入口机制：普通 Markdown 块变工作台组件。 | 只适合作 UI layer，不应绕过 VAKS 文件边界。 |
| `src/main.js:151-235` | monkey patch `executeCommand`、`getActiveViewOfType`、`activeLeaf`。 | 让嵌入 editor 获得热键/active view 体验。 | 高耦合工作台 hack；不能当稳定核心边界。 |
| `src/main.js:245-253` | focus tracking 将当前焦点绑定到 embed。 | 嵌入编辑器行为路由的基础。 | focus 状态不是 authority 状态。 |
| `src/embed-manager.js:36-57` | 解析 `sync` block 中的 embed 行并逐个处理。 | 小语法层，容易理解。 | 只解析 `![[...]]` 行，能力范围有限。 |
| `src/embed-manager.js:63-82` | 从 alias 中提取 `{height,maxHeight,title,...}` option。 | 局部配置设计。 | 字符串解析简单，复杂 alias 边界需测试。 |
| `src/embed-manager.js:103-124` | 解析 note path/section，查找文件，阻止递归 embed。 | 关键 source selection 逻辑。 | 递归保护只覆盖同一 note 直接递归。 |
| `src/embed-manager.js:141-146` | 使用 `IntersectionObserver` lazy load embed。 | 多 embed dashboard 性能手段。 | 性能声明需要真实 vault 压测。 |
| `src/embed-manager.js:163-208` | 创建 `WorkspaceLeaf`，`openFile(... mode: source)`，保存 view/editor。 | “真实 editor 实例”设计的源码锚点。 | 直接打开源文件 editor，写入会修改源文件。 |
| `src/embed-manager.js:239-246` | section 时隐藏 properties；whole note 可折叠 properties。 | workbench 视图清洁度处理。 | 这是显示/体验层，不是 schema 层。 |
| `src/viewport-controller.js:8-27` | section viewport 初始化，挂上边界保护、header 拦截、内容约束。 | section-bounded editing 的核心。 | DOM/事件层保护，不是强安全隔离。 |
| `src/viewport-controller.js:46-62` | 根据 section 行号生成 CSS，隐藏 section 外行。 | 通过视口限制暴露范围。 | 隐藏不等于不可修改，需要事件约束配合。 |
| `src/viewport-controller.js:82-132` | Backspace/Delete 边界保护。 | 防止删除隐藏边界换行。 | 只覆盖部分键盘行为，不能作为安全模型。 |
| `src/viewport-controller.js:143-230` | header 输入/粘贴拦截，防止破坏标题层级。 | 值得借鉴的“局部编辑约束”。 | 规则是 Markdown header 专用。 |
| `src/viewport-controller.js:353-374` | 查找 section 起止行和 header level。 | section anchor 的实现方式。 | 依赖 heading 文本精确匹配。 |
| `src/dynamic-paths.js:36-52` | 按 date offset、date、time、title 顺序解析动态路径。 | Daily/project dashboard 的路径模板。 | 动态路径不适合作证据锚点。 |
| `src/dynamic-paths.js:67-181` | date/time/title pattern 解析和基础格式校验。 | 可借为轻量模板解析参考。 | 不是完整模板引擎。 |
| `src/command-interceptor.js:10-34` | 热键 command handler 映射。 | 嵌入编辑体验完整化。 | 与 Obsidian command id 耦合。 |
| `src/command-interceptor.js:366-390` | section embed 中 header level 限制。 | 局部编辑约束的另一锚点。 | 不能替代 VAKS review gate。 |
| `styles.css:2-28` | sync container/embed 基础布局。 | 工作台 UI 组件外壳。 | 样式层，不是知识结构。 |
| `styles.css:284-288` | focus highlight。 | 当前编辑焦点可见性。 | 只改善 UX。 |

## Build / Runtime Check

```yaml
temp_clone: "C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\vaks-sync-embeds-intake"
node: "v24.11.0"
npm: "11.6.1"
install_command: "npm install --ignore-scripts"
build_command: "$env:NODE_ENV='production'; node esbuild.config.mjs"
build_result: succeeded
test_suite: none_found_in_tracked_files
npm_audit:
  moderate: 1
  package: esbuild
  advisory: GHSA-67mh-4wv8-2f99
  note: "dev dependency / build tooling risk; not runtime truth judgment"
scratch_side_effects:
  - "node_modules created"
  - "package-lock.json created"
  - "main.js rewritten by build in temp clone"
```

## 初步看点

- 它用很薄的 `sync` code block 语法，把多个 source notes / sections 挂到一个 dashboard 里。
- 它不是复制内容，而是把真实 editor view 放进当前页面，因此编辑会回写原始 note。
- 它在 section embed 上做了 header hierarchy 和 cursor/boundary 保护，适合蒸馏成“局部可编辑视图”的候选模式。
- 它的动态路径对 daily note / project overview 很实用，但不能作为稳定 source anchor。

## 明显疑点

- package version `2.0.0` 与 manifest version `2.0.2` 不一致。
- tracked files 没有 test/spec。
- 构建依赖 `esbuild@0.17.3`，npm audit 报一个 moderate advisory。
- `executeCommand`、`activeLeaf`、`getActiveViewOfType` monkey patch 体验上强，但对 Obsidian 内部 API / DOM 变化敏感。
- 真实 Obsidian vault、移动端、多人同步、冲突写入、VAKS formal vault 中的权限边界均未测试。

## 可抽取 Candidate Points

1. Editable transclusion can reduce duplicate dashboard text if write permissions are path- and layer-scoped.
2. Section-bounded editing is useful for workbench snippets, but DOM/CSS hiding is not a security boundary.
3. Dynamic note path templates are activation conveniences, not evidence anchors.
4. Command interception can preserve editing ergonomics, but monkey patching workspace state should stay optional and sandboxed.
5. Dashboard edit-through should never target reviewed knowledge by default.

## 当前处理等级

```text
medium candidate-only repo intake
```

升级到 heavy 的条件：

- 用户要在正式 `H:\Obsidian\资料库` 里真实安装/测试该插件。
- VAKS 开始设计 Obsidian dashboard / Bases / editable project workbench。
- 需要决定是否允许 dashboard 直接编辑 raw/candidate/reviewed 文件。
- 需要比较多个 Obsidian synced-block / editable-embed 方案。

## 下一步

- 读取对应 candidate distillation。
- 若后续进入 Obsidian 工作台实现，先在 disposable vault 做插件 sandbox，不要直接装进正式 vault。
- 若要吸收为 VAKS 设计，先限定为 candidate/project overlay，不提升到 reviewed pattern。
