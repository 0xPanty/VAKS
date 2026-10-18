---
type: candidate_pattern
status: active
pattern_id: file-first-agent-workbench
created_at: 2026-06-05
truth_boundary: candidate pattern only; not reviewed knowledge
source_family_ids:
  - sf-agent-workbench
  - sf-obsidian-workflow
project_fit_refs:
  - outputs/review/project_borrowing_ledgers/VAKS.md
---

# File-First Agent Workbench

## One-Line Pattern

把 agent 的长期材料、prompt、skills、workspace profile、会话记录、上下文包尽量落成可读文件；索引和向量库只是可重建缓存。

## Problem Addressed

Agent 工作流容易黑盒：记忆藏在向量库里，prompt 藏在代码里，skill 藏在工具注册里，用户不知道 agent 为什么这样回答或执行。

## Mechanism

- Markdown / JSON 作为可读 source of operation trace。
- prompt components 拆成可审阅文件。
- skills 以 `SKILL.md` / frontmatter 形式可见。
- inspector 展示 memory / skills / workspace / tool trace。
- index 可从文件重建。

## Applicability

- 本地 AI 工作台。
- agent development environment。
- VAKS future dev context / context-pack viewer。
- 需要人类审阅 agent 行为的系统。

## Non-Goals and Trade-Offs

- file-first 不等于 file is truth。
- 本地文件不天然安全。
- inspector 可见性不等于 evidence review。
- 过多文件可能增加维护负担。

## Derived From Sources

- `raw/repos/2026-06-04-langchain-miniopenclaw-source.md`
- `raw/videos/2026-06-04-bilibili-openclaw-karpathy-knowledge-base-source.md`
- `raw/videos/2026-06-04-bilibili-karpathy-llm-wiki-not-recommend-source.md`
- `raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source.md`
- `raw/videos/2026-06-04-bilibili-claude-code-obsidian-local-knowledge-base-source.md`

## Aliases or Near-Duplicates

- local agent workbench
- files as durable context
- Obsidian as AI IDE
- index-as-cache

## Risk of Overreach

- 把 memory file 当 reviewed knowledge。
- 让 agent 直接写 skill / memory / source。
- 因为可见就误以为可靠。
- 复用代码前忽略 license / safety / runtime verification。

## Project Fit Refs

- VAKS: `watch`; useful for future workbench, not truth layer.

