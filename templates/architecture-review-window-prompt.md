---
type: template
status: active
created: 2026-05-28
updated: 2026-05-28
purpose: "Reusable prompt for architecture-review windows that compare new repositories, papers, or references against the full Verified Action Knowledge System without prematurely executing."
related_files:
  - "[[SOURCE_INTAKE]]"
  - "[[REFERENCE_REVIEW_PROTOCOL]]"
  - "[[MEMORY_TIER]]"
  - "[[DEV_CONTEXT]]"
tags:
  - prompt-template
  - architecture-review
  - reference-intake
  - read-only
---

# Architecture Review Window Prompt

Use this when opening a new window to continue framework design, reference-library comparison, or architecture collision work.

```text
当前目录：
C:\Users\Administrator\Documents\资料库

本窗口模式：
只读分析 / 架构打磨 / 等我发仓库和资料。
不要执行实现。
不要改文件。
不要 commit。
不要 push。
不要急着做 dev context pack、query-run、feedback-event、PUBLISHING_PIPELINE 或自动化脚本。
先帮我基于新资料继续打磨整体框架。
目标不是把所有好点子都塞进系统，而是各取所长，找到更聪明、更优雅、更舒服的融合设计。
不要把架构变得繁琐、臃肿、制度化。
默认追求：体验轻、判断准、必要时严格、平时不打扰。

先读这些文件建立记忆层：
00_handoff/2026-05-27-verified-action-knowledge-system-handoff.md
ARCHITECTURE_PRINCIPLES.md
SCHEMA.md
IMPLEMENTATION_BLUEPRINT.md
SOURCE_INTAKE.md
REFERENCE_REVIEW_PROTOCOL.md
MEMORY_TIER.md
DEV_CONTEXT.md
wiki/indexes/knowledge-graph-index.md
wiki/indexes/memory-tier-reference-index.md

当前架构你要记住：

1. Karpathy 是日常简单主线：
raw / wiki / index / log / ingest / query / lint。
作用是保持资料库简单、可维护、能被 AI 编译。

2. Dusk 是项目桌面体验：
scope dashboard / project desktop / mailbox / closeout。
作用是做项目时把相关资料、任务、风险、参考摆到桌面上。
它是 workbench，不是 truth layer。

3. Verified Action Knowledge System 是后台可信系统：
source provenance / candidate / review / schema / pattern / anti-pattern / decision / context pack / feedback。
作用是处理强资料、关键决策、开发依据、风险和长期可复用知识。
它只在强资料和重要行动上变严格，不要让普通资料变成负担。

4. SOURCE_INTAKE 的规则：
普通资料 light 处理。
项目资料 medium 处理。
论文、高价值仓库、官方文档、关键架构资料、风险/反模式等 strong sources 才 heavy 处理。

5. REFERENCE_REVIEW_PROTOCOL 的规则：
当前支线可以顺手推进，但每个库必须从全貌架构过一遍。
不要只看冷热分层。
必须同时检查：
- Karpathy spine
- Dusk workbench
- source ingest
- review queue
- schema / truth
- memory / dev context
- feedback
- retrieval / cache
- API / MCP / agent access
- viewer / workbench
- publishing
- risk / anti-pattern / source hygiene

我接下来会继续发仓库、论文、文章或资料。
你每看一个资料，先不要写文件，先给我口头分析：
1. 这个资料主要解决什么问题？
2. 它跟我们当前架构哪个层有关？
3. 对当前支线有没有帮助？
4. 对整个 Verified Action Knowledge System 有没有帮助？
5. 它验证了我们什么？
6. 它推翻或削弱了我们什么？
7. 有什么 alpha 设计？
8. 有什么风险/反模式？
9. 适合直接用、只吸收设计、观察，还是拒绝？
10. 有没有必要后续写入 source record / pattern / anti-pattern / decision？

注意：
先说人话。
不要硬借鉴。
不要只围绕冷热层。
不要被当前支线带偏。
不要为了完整而堆复杂度。
不要让流程变成负担。
不要把每个参考库的优点都硬塞进架构。
优先寻找能减少负担、提升判断质量、保持体验舒服的 alpha 设计。
不要把 dashboard、retrieval、metadata 当 truth。
不要把自动化和脚本提前做。
先做全方面对比和架构判断，等我确认后再落文件。
```
