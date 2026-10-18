---
type: candidate_pattern
status: active
pattern_id: skills-and-prompts-as-visible-files
created_at: 2026-06-05
truth_boundary: candidate pattern only; not reviewed knowledge
source_family_ids:
  - sf-agent-workbench
project_fit_refs:
  - outputs/review/project_borrowing_ledgers/VAKS.md
---

# Skills and Prompts as Visible Files

## One-Line Pattern

把 agent 的技能说明、prompt 组件、角色设定、workspace profile 做成可读文件，而不是只藏在代码或模型上下文里。

## Problem Addressed

Agent 为什么这样做、用什么规则、读了哪些技能，经常不可见。不可见会让行为难复盘，也让错误难定位。

## Mechanism

- `SKILL.md` / frontmatter 作为 skill registry。
- prompt components 拆成文件。
- workspace identity/user/agents 作为可审阅文本。
- 保存 snapshot / hash / refresh ledger。

## Applicability

- agent workbench。
- local AI development environment。
- VAKS future tool/agent access surface。

## Non-Goals and Trade-Offs

- 可见 prompt 不等于正确 prompt。
- skill 可编辑需要权限和 quarantine。
- 不应让 agent 直接批准自己的 skill changes。

## Derived From Sources

- `raw/repos/2026-06-04-langchain-miniopenclaw-source.md`
- `raw/videos/2026-06-04-bilibili-openclaw-karpathy-knowledge-base-source.md`
- `raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source.md`

## Aliases or Near-Duplicates

- prompt component files
- skills as markdown
- visible agent rules
- skill registry snapshot

## Risk of Overreach

- prompt/skill 文件被当成项目真理。
- prompt injection 通过 skill 文件长期固化。
- 工具能力被过早开放。

## Project Fit Refs

- VAKS: `watch`; only after tool-safety review.

