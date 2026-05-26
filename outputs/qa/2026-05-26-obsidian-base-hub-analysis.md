---
type: output
status: completed
created: 2026-05-26
topic: Obsidian Base Hub analysis
sources:
  - raw/repos/2026-05-26-obsidian-base-hub-source.md
related_patterns:
  - obsidian-bases-linked-workbench-views
related_decisions:
  - wiki/decisions/2026-05-26-obsidian-bases-properties-primary-view-layer.md
confidence: medium
---

# 问答记录：Obsidian Base Hub 值不值得借鉴？

## 问题

`rafafields/Obsidian-Base-Hub` 是否有可借鉴之处？

## 大白话结论

它不是我们的核心架构参考，而是一个很实用的 Obsidian Bases 视图样板。

它最有价值的地方是告诉我们：

```text
schema 稳定以后，可以用 .base 把状态、复查、关联对象做成工作台。
```

它不能帮我们判断资料可信不可信，也不能替代 source / claim / pattern / decision。它只负责让人更容易看见和操作这些节点。

## 它补了我们什么

补的是“人怎么管理这些结构化笔记”的 UI/视图层。

我们现在有架构逻辑：

```text
raw -> wiki -> claim/pattern/anti-pattern -> decision
```

但日常使用时还会遇到：

- 哪些 source 还没摘要？
- 哪些 claim 只有单来源？
- 哪些 pattern 还在 watch？
- 哪些 decision 过期要复查？
- 哪些资料和某个项目/主题相关？

Base Hub 的模式可以把这些做成 Obsidian 里的表格/卡片。

## 可以借鉴什么

1. 根页面嵌入局部视图  
比如未来某个 architecture decision 页面，可以嵌入相关 source、supporting claims、contradicting claims、open risks。

2. `+ New` 作为结构化入口  
在 Bases 视图里创建新条目，可以自动进入正确文件夹和字段流。

3. link property 连接对象  
它用 projects/areas 把 task、meeting、people 连接起来。我们可以用 topic/project/source/claim 关系做类似工作台。

4. 状态分组视图  
它按 status/priority 分任务。我们可以按 verification_status/adoption_status/confidence 分 claim/pattern/decision。

## 不该照搬什么

- 不照搬它的目录结构。
- 不照搬 task/project/meeting/person 这套领域模型。
- 不照搬每个 project 复制一份 `.base` 的做法。
- 不照搬它的字段命名，因为里面有 `projects/proyectos`、`role/rol`、`scheduled/agendado` 混用。

## 是否过度设计

现在就做完整 Bases 工作台，会有点早。

但把它记录为“SCHEMA.md 稳定后的视图层模板”，不是过度设计。

正确顺序：

```text
先定 SCHEMA.md
再定模板
再建少量全局 .base 视图
最后才考虑更复杂的面板
```

## 最终判断

`Obsidian-Base-Hub` 是锦上添花型参考，属于 view/workbench layer。

它的价值是让我们的 verified knowledge system 更好用，不是让它更可信。可信度仍然来自 schema、source、claim、evidence、timeline 和 verification gate。

