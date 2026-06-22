---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from: "raw/repos/2026-06-12-uthvah-sync-embeds-source.md"
source_id: "github:uthvah/sync-embeds@10703d39548a9772573dced19f49ec05f8449500"
snapshot_ref: "raw/repos/_snapshots/2026-06-12-uthvah-sync-embeds-10703d39548a-source.zip"
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
borrow_value: medium
borrow_order: P2
borrow_scope: "Obsidian workbench UX and editable dashboard components"
not_borrow_scope: "truth layer, reviewed knowledge editing, action-basis support, source/evidence authority"
dev_context_hint:
  core: []
  support:
    - "Use as a P2 reference when designing editable Obsidian dashboards or source-card/review-queue workbench surfaces."
  risk:
    - "Direct edit-through can mutate source notes; gate by folder/layer and sandbox first."
    - "Dynamic paths and hidden editor re-parenting are convenience/UX mechanisms, not provenance or review gates."
  cold:
    - "Plugin packaging and community-store installation details."
routing_hint:
  - obsidian-workbench
  - editable-transclusion
  - dashboard-ui
  - project-overlay
possible_project_refs:
  - "outputs/review/project_lens_overlays/2026-06-12-sync-embeds-obsidian-workbench-overlay.md"
point_anchor_refs:
  - source_ref: "raw/repos/2026-06-12-uthvah-sync-embeds-source.md"
    snapshot_ref: "raw/repos/_snapshots/2026-06-12-uthvah-sync-embeds-10703d39548a-source.zip"
    anchors:
      - "README.md:16"
      - "README.md:37-41"
      - "src/main.js:80"
      - "src/main.js:151-235"
      - "src/embed-manager.js:36-57"
      - "src/embed-manager.js:163-208"
      - "src/viewport-controller.js:8-27"
      - "src/viewport-controller.js:82-132"
      - "src/dynamic-paths.js:36-52"
tags:
  - candidate
  - provisional
  - obsidian
  - editable-embed
  - workbench
---

# Candidate Distillation: uthvah/sync-embeds

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

```yaml
record_kind: candidate_distillation
knowledge_status: candidate
processing_tier: medium
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: medium
borrow_order: P2
```

## 一句话判断

`sync-embeds` 对 VAKS 的价值是：它证明 Obsidian dashboard 可以从“只读汇总页”变成“可编辑工作台”，但这个能力必须被夹在 candidate/workbench 层，不能直接碰 reviewed truth 或 action-basis 文件。

## Source

```yaml
derived_from: raw/repos/2026-06-12-uthvah-sync-embeds-source.md
source_id: github:uthvah/sync-embeds@10703d39548a9772573dced19f49ec05f8449500
snapshot_ref: raw/repos/_snapshots/2026-06-12-uthvah-sync-embeds-10703d39548a-source.zip
evidence_granularity: table_or_code_anchor
```

## 它实际解决的问题

Obsidian 原生 embed 更像 preview：可以看见别的 note 或 section，但不能自然地在当前上下文里直接编辑它。这个插件把 embed 包在 `sync` code block 里，然后创建真实 Markdown editor view，把它嵌到当前页中。

对普通用户来说，结果是像 Notion synced block：一个 daily dashboard、project overview 或任务页，可以直接编辑散落在不同文件里的内容。

对 VAKS 来说，问题不是“知识如何变真”，而是：

```text
如何在一个 Obsidian 工作台里编辑源文件/候选文件的局部片段，
同时避免复制内容、上下文跳转和 dashboard 变成静态摘要。
```

## Candidate Points

### 1. Editable transclusion 可作为工作台 UX，但不能作为 truth layer

Source anchors:

- `README.md:16`
- `README.md:37-41`
- `src/embed-manager.js:163-208`

插件的核心不是把内容复制到 dashboard，而是打开真实 editor view 并把它嵌入当前文档。这个设计对 VAKS 有一个实用启发：dashboard 不一定只能显示摘要，也可以显示“可编辑源片段”。

VAKS 可借：

- source card inbox 页面中直接编辑 raw source 的备注区。
- review queue 页面中直接编辑某个 candidate 的开放问题或 routing hint。
- project overview 页面中直接编辑项目 scratch / feedback / candidate notes。

VAKS 不可借：

- 从 dashboard 直接编辑 reviewed claims、decisions、patterns。
- 把可编辑视图当成 review gate。
- 把“能在一个页面编辑”误读成“可以降低证据/权限要求”。

Candidate judgment:

```text
adapt as workbench UX, not as knowledge architecture
```

### 2. Section-bounded editing 是好模式，但 DOM/CSS 隐藏不是安全边界

Source anchors:

- `README.md:30`
- `src/viewport-controller.js:8-27`
- `src/viewport-controller.js:46-62`
- `src/viewport-controller.js:82-132`
- `src/viewport-controller.js:143-230`
- `src/viewport-controller.js:353-374`

插件的 section embed 能定位到某个 heading，并尝试只显示/允许编辑该 heading 下的区域。它还加了 Backspace/Delete 边界保护、header 输入拦截、paste header 调整。

VAKS 可借：

- 在工作台中只暴露某个候选点、某个 source-card section、某个 feedback block。
- 对局部编辑加“不要越界破坏结构”的轻约束。
- 用 heading/section 作为轻量 UI anchor。

VAKS 必须补：

- 文件层权限：哪些目录可编辑，哪些只读。
- 字段层权限：哪些 section 可以改，哪些必须走 review。
- 写入日志：每次 dashboard edit-through 都应能追溯到文件、section、时间、操作者。
- 回滚/冲突策略：尤其是正式 vault、多窗口、多设备同步时。

Candidate judgment:

```text
borrow the local-editing constraint idea; do not rely on it as enforcement
```

### 3. Dynamic path templates 适合 activation，不适合 provenance

Source anchors:

- `README.md:86-118`
- `src/dynamic-paths.js:36-52`
- `src/dynamic-paths.js:67-181`

插件支持 `{{date}}`、date offset、`{{time}}`、`{{title}}` 等变量，让 dashboard 自动指向当天、上周、当前项目标题对应的 note。

VAKS 可借：

- daily review workbench 自动指向当天 source inbox。
- project page 自动拉取同名 project notes 或 task blocks。
- active context page 自动显示当前项目的 scratch/support/risk notes。

VAKS 不可借：

- 动态路径作为 source provenance。
- 动态路径作为 evidence anchor。
- 动态路径作为 reviewed relation 的稳定目标。

候选边界：

```text
dynamic path = activation convenience
stable source path/hash/commit = provenance anchor
reviewed relation = later evidence-aware review only
```

### 4. Command interception 改善编辑手感，但应隔离在插件/工作台层

Source anchors:

- `src/main.js:151-235`
- `src/command-interceptor.js:10-34`
- `src/command-interceptor.js:366-390`

插件 monkey-patch 了 Obsidian commands 和 workspace active view，使焦点在 embed 内时，常见热键能作用在 embed editor 上。这个设计对用户体验很好：不用为了粗体、checkbox、list、header 来回跳源文件。

VAKS 可借：

- 如果未来有正式 Obsidian 工作台插件，可以让候选卡片/源卡片局部编辑更顺手。
- 给 active project dashboard 提供“像真 editor 一样”的交互，而不是只读预览。

VAKS 不可借：

- 在核心知识层依赖 monkey patch。
- 把 active focus 当成 active project / active authority。
- 默认把热键写入范围放开到 reviewed 文件。

Candidate risk:

```text
workspace monkey patch is brittle and should be optional/sandboxed
```

### 5. Multiple embeds + lazy loading 可做轻量 dashboard，但需要候选/权限过滤

Source anchors:

- `README.md:124-140`
- `src/embed-manager.js:36-57`
- `src/embed-manager.js:141-146`
- `styles.css:2-28`

插件允许一个 `sync` block 里放多个 embeds，并用 lazy load 降低一次性加载压力。对 VAKS 来说，这像一个很轻的工作台：一个页面挂多个文件片段。

可借例子：

```text
Daily VAKS Inbox:
  - 今天的 raw sources
  - review_due candidates
  - project scratch notes
  - feedback events needing triage

Project Overview:
  - project source card section
  - current candidate distillation section
  - risk notes
  - next action scratch
```

边界：

```text
dashboard grouping is not retrieval authority
dashboard visibility is not evidence support
dashboard editability is not promotion
```

## Open Questions

1. 在正式 `H:\Obsidian\资料库` 里，哪些目录永远不允许 edit-through？
2. 如果要借这个模式，是否只允许写 `outputs/review`、`raw/*` 的备注区、`outputs/feedback`，而不允许写 `wiki/claims` / `wiki/decisions`？
3. Obsidian 的 Bases 是否已经足够覆盖查看/筛选需求，sync-embeds 是否只应该补“局部编辑”？
4. 多设备同步时，嵌入 editor 对同一文件的并发编辑会不会扩大冲突？
5. 动态路径在中文/特殊字符标题、重名文件、移动端上是否稳定？

## Routing Hint

```yaml
route_to:
  - obsidian-workbench
  - editable-dashboard
  - source-card-ui
  - review-queue-ui
  - active-project-dashboard
do_not_route_to:
  - reviewed-knowledge
  - evidence-support
  - action-basis
  - source-truth
```

## VAKS Fit

| VAKS Layer | Fit | Note |
|---|---:|---|
| Capture / Provenance | Medium | Can make source cards easier to edit from an inbox page. |
| Candidate Comprehension | Medium | Useful for editing candidate snippets from dashboards. |
| Review / Consolidation | Low-medium | Can display review items, but cannot perform review. |
| Association / Reviewed Relations | Low | No relation or evidence logic. |
| Activation / Dev Context | Medium | Dynamic dashboard/page embeds can activate current project context. |
| Context Pack | Low | Can show context, but not assemble evidence envelopes. |
| Decision / Action | Avoid | Not action basis. |
| Feedback | Medium | Could edit feedback/event notes from a workbench. |
| Viewer / Workbench | Medium-high | Best-fit layer. |
| Risk / Inhibition | Medium | Edit-through is useful but dangerous without write boundaries. |

## Borrow Value

```yaml
borrow_value: medium
borrow_order: P2
why_not_strong:
  - "It is a useful UI/workbench plugin, not a VAKS architecture primitive."
  - "No real Obsidian vault runtime test was performed."
  - "It relies on DOM/editor/workspace patching that must stay sandboxed."
  - "No tracked test suite was found."
why_not_low:
  - "The editable-transclusion idea maps cleanly to VAKS source/review dashboard pain."
  - "Section-bounded editing is a concrete UI pattern worth remembering."
```

## Avoid

- Do not install directly into the formal vault without a disposable-vault test.
- Do not expose reviewed knowledge files to direct dashboard editing.
- Do not treat CSS-hidden section boundaries as security.
- Do not use `{{date}}` / `{{title}}` dynamic links as source anchors.
- Do not rely on monkey-patched Obsidian active view as a VAKS authority signal.
- Do not treat the README claim of broad user trust as independent quality evidence.
- Do not ignore package/manifest version mismatch before any real use.

## Minimal Future Test

If this becomes implementation-relevant:

```text
1. Create disposable vault under H:\Obsidian\资料库\_tmp-sync-embeds-test-<date>.
2. Install plugin manually or via community store.
3. Create fake raw/source, candidate, reviewed, and feedback notes.
4. Test sync embed against writable raw/candidate only.
5. Confirm reviewed notes are not exposed to editable embeds.
6. Test section heading boundaries, dynamic paths, and rollback.
7. Delete disposable vault and verify deletion.
```

## Direct Judgment

```yaml
direct_use: no, not in formal vault without sandbox
fork: no
design_only: yes
adapt: yes, for Obsidian workbench UX
reject: no, but reject truth/action use
current_branch_value: "P2 support for Obsidian dashboard / workbench design"
whole_architecture_value: "medium for viewer/workbench and activation surfaces; low for truth/review"
risk: "edit-through mutation, DOM/editor brittleness, dynamic-anchor confusion, dependency hygiene"
next_action: "keep candidate-only; use overlay if future VAKS Obsidian workbench design resumes"
```

## Forbidden

```text
project_borrow_scope in this file as adoption conclusion
decision outcome
formal pattern
action basis
truth confidence
reviewed relation
```
