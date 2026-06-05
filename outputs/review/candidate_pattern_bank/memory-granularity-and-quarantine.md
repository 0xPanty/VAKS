---
type: candidate_pattern
status: active
pattern_id: memory-granularity-and-quarantine
created_at: 2026-06-05
truth_boundary: candidate pattern only; not reviewed knowledge
source_family_ids:
  - sf-memory-retrieval
  - sf-agent-workbench
project_fit_refs:
  - outputs/review/project_borrowing_ledgers/VAKS.md
---

# Memory Granularity and Quarantine

## One-Line Pattern

记忆应有不同粒度、生命周期和写入边界；agent 或 AI 生成的记忆先进入 candidate / quarantine，不直接改 reviewed truth。

## Problem Addressed

长期记忆系统容易污染：一句话、一个会话摘要、一个工具输出、一个用户反馈，可能被过度固化，后续不断激活错误上下文。

## Mechanism

- 区分 episode / summary / concept / preference / decision / feedback。
- 记录来源和生成活动。
- agent 写入只能产生 candidate 或 feedback-event。
- 负反馈触发 review_due，不直接改 truth。
- 过期、冷却、supersession 与 usefulness 分开。

## Applicability

- 个性化记忆。
- agent workspace。
- VAKS memory tier / feedback ledger / future agent memory path。

## Non-Goals and Trade-Offs

- 不把所有 memory 都 formal review。
- 不把 feedback 变成 truth mutation。
- 不要求普通使用都有重审查。

## Derived From Sources

- `raw/repos/2026-06-04-come-context-memory-source.md`
- `raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source.md`
- `raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source.md`
- `raw/repos/2026-06-04-langchain-miniopenclaw-source.md`

## Aliases or Near-Duplicates

- agent memory quarantine
- multi-granularity memory
- cooling / expiry memory
- feedback not truth

## Risk of Overreach

- 把 quarantine 做成永久垃圾堆。
- 过度分层导致 memory 不可用。
- 让 agent self-review 自己的写入。

## Project Fit Refs

- VAKS: `watch`; important for future agent access.
