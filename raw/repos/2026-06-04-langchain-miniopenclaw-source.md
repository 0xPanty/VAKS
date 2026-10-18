---
type: source
status: source-captured
title: langchain-miniopenclaw / langchain-OpenClaw
source_id: github-lyxhnu-langchain-miniopenclaw
source_uri: github:lyxhnu/langchain-miniopenclaw
source_url: https://github.com/lyxhnu/langchain-miniopenclaw/tree/main
source_type: repository
platform: github
owner: lyxhnu
repo: langchain-miniopenclaw
default_branch: main
checked_ref: main
checked_commit: 8497d99
checked_commit_note: short SHA observed from GitHub commit page; full clone/API lookup failed because local GitHub TLS handshake failed
commit_time: 2026-03-10
captured_at: 2026-06-04
captured_by: Codex
raw_location: raw/repos/2026-06-04-langchain-miniopenclaw-source.md
processing_mode: repo-review
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public_no_cookies
source_status: public_repo_observed
snapshot_location:
snapshot_status: not_available_local_tls_failure
license_status: no_license_file_observed_in_top_level_listing
verification_status: unverified
topics:
  - local-agent-workbench
  - file-first-memory
  - transparent-agent
  - skills-as-markdown
  - rag
  - dev-context
  - candidate-only
projects:
  - verified-action-knowledge-system
source_family: agent-workbench-reference
upstream_sources:
  - https://github.com/ConardLi/rag-skill
tags:
  - raw-repo
  - github
  - candidate-only
---

# Repository Source: langchain-miniopenclaw / langchain-OpenClaw

## 为什么收录

这个仓库是一个本地运行、文件优先、可审计的 AI Agent 工作台原型。它对 VAKS 的价值不在“直接拿来做核心系统”，而在于它把几个我们一直在讨论的方向用代码串起来了：

- 文件作为长期记忆 / prompt / skill 的可读来源。
- 向量索引只是可重建缓存。
- skill 不是硬编码函数，而是可读的 `SKILL.md`。
- 前端能看到 token、tool start/end、retrieval、raw messages、Memory / Skills / Workspace 文件。
- 会话和工具记录落盘到本地 JSON。

这和 VAKS 的 `Capture -> Understand -> Review -> Connect -> Act and Learn` 不完全同层，但对未来 activation / dev context / agent workbench / viewer 有明显参考价值。

## 来源卡

- 仓库：https://github.com/lyxhnu/langchain-miniopenclaw/tree/main
- README 项目名：langchain-OpenClaw
- 观察分支：main
- 观察 commit：8497d99（GitHub commit page 上的短 SHA）
- 最新观察到的 commit 时间：2026-03-10
- 访问方式：公开 GitHub 页面与 raw 文件，无 cookies
- 本地 clone / API 状态：失败，Windows GitHub TLS handshake / API EOF；本次审阅改用 GitHub web/raw 文件
- 本地快照：未生成
- 许可证：顶层文件列表未观察到 LICENSE，后续若要复用代码必须再确认授权

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | 声称本地运行、文件优先、可审计 Agent 工作台；对话 JSON、长期记忆 Markdown、skill as `SKILL.md`、prompt/tool/memory/retrieval 可见 | 和 VAKS 的文件优先、可审计、可复盘方向高度同频 | README 是项目自述，不是运行验证 |
| `backend/app.py` | FastAPI lifespan 中 refresh skill snapshot、初始化 agent、配置并 rebuild memory index；挂载 chat/sessions/files/tokens/compress/config API | 启动时显式重建可见上下文和索引，适合“缓存可重建”思路 | 没有生产安全、认证、多租户边界 |
| `backend/graph/prompt_builder.py` | system prompt 由 `SKILLS_SNAPSHOT.md`、`workspace/SOUL.md`、`workspace/IDENTITY.md`、`workspace/USER.md`、`workspace/AGENTS.md`、`memory/MEMORY.md` 组装；RAG 模式下 memory 改为检索注入 | prompt 组成可文件化、可审阅、可局部编辑 | prompt 组装不是 truth review，memory 也不是 reviewed knowledge |
| `backend/graph/memory_indexer.py` | `memory/MEMORY.md` 建 LlamaIndex；MD5 digest 判断是否重建；无 embedding key 时索引为空 | 文件是事实源，索引是派生缓存 | 单一 memory 文件不区分 source/raw/candidate/reviewed/feedback |
| `backend/tools/search_knowledge_tool.py` | `knowledge/` 文档建立向量索引；无 embedding 或异常时有 keyword fallback；返回 source、score、text | 检索可作为 activation/context prep，并保留 source 字段 | score 只是检索分，不是 evidence support 或 truth confidence |
| `backend/graph/session_manager.py` | session JSON 持久化；保存 messages、tool_calls、compressed_context；可 archive 压缩历史 | 会话与工具输出可以变成 use ledger / debug ledger 的工程参考 | 压缩摘要是 candidate context，不是事实；tool record 也不是证据支持 |
| `backend/api/files.py` | 只允许编辑 `workspace/`、`memory/`、`skills/`、`knowledge/` 和 `SKILLS_SNAPSHOT.md`；保存 memory 后 rebuild index；保存 skills 后 refresh snapshot | 编辑白名单与写后刷新机制值得借鉴 | 这只是路径白名单，缺少 VAKS 的 promotion / review / action-basis gate |
| `backend/tools/skills_scanner.py` | 扫描 `skills/*/SKILL.md` frontmatter，生成 `SKILLS_SNAPSHOT.md` | skill registry 可以是轻量 Markdown 索引 | skill 可写入会引入 agent memory quarantine / tool-safety 风险 |
| `backend/tools/terminal_tool.py` | 工具可执行终端命令，含很小的 destructive blacklist 与 30s timeout | 调试型 agent workbench 的能力样例 | 黑名单太弱，不能作为 VAKS 未来 agent safety 方案 |
| `frontend/src/components/editor/InspectorPanel.tsx` | Monaco editor 编辑 Memory / Skills / Prompt 文件 | 右侧 inspector/workbench 很适合 VAKS 未来可视化审阅面板 | UI 编辑不是 review；编辑权限需要严格边界 |
| `frontend/src/components/chat/ChatPanel.tsx` / `ChatMessage.tsx` | 聊天区展示工具回放、检索卡、流式输出 | “看见内部状态”的交互模型有参考价值 | 可观测性不是正确性 |

## 人话摘要

这个库像一个“小型本地 Agent IDE”：后端用 FastAPI + LangChain 创建 agent，前端用 Next.js + Monaco 做三栏界面。左边是会话，中间是聊天和工具回放，右边可以看和改 Memory / Skills / Workspace 文件。系统 prompt 不是藏在代码里，而是由一组 Markdown 文件实时拼装。长期记忆保存在 `memory/MEMORY.md`，需要 RAG 时再用 LlamaIndex 建索引检索；知识库在 `knowledge/` 下，也可以做向量 + 关键词回退检索。

对 VAKS 来说，最有用的是它把“文件可读、索引可重建、prompt 可解释、工具过程可见、UI 可检查”做成了一个工作台形态。这非常适合未来 activation / dev context / context-pack workbench 的设计参考。

但它不解决 VAKS 的核心问题：它没有区分 source provenance、raw text、candidate comprehension、candidate points、reviewed knowledge、action basis、feedback ledger。它的 memory 文件、RAG 命中、tool output、会话摘要都只能算 candidate/context/activation，不能成为 truth。

## 候选价值判断

```text
Direct use: no
Fork: no, at least not before license and runtime verification
Design-only: yes
Adapt: yes, for workbench / inspector / prompt-component / file-first memory patterns
Reject: no
```

## VAKS 归位

```text
Capture:
  作为 GitHub repository source record 收录，保留 URL、观察 ref、代码锚点。

Understand:
  候选理解是“本地透明 Agent 工作台”，不是普通 RAG 库。

Review:
  当前不进入 reviewed knowledge；只作为 architecture review 的候选来源。

Connect:
  可连接到 CoMe、Karpathy LLM Wiki、RAGLab、Obsidian local KB、agent memory quarantine。

Activation / Context Pack:
  对未来 dev context / agent workbench / file inspector / prompt visibility 方向有较强激活价值。

Decision / Action:
  不作为 action basis；不直接引入代码或运行时。

Use Ledger / Feedback:
  后续如果我们测试 workbench 原型，可以把“可见 prompt / skill / memory / tool chain”作为 usefulness 反馈项。
```

## Candidate Points

- 文件优先的 agent memory/workbench 设计可以降低黑盒感：真正可长期保存和审阅的是 Markdown / JSON 文件，索引只是可重建缓存。
- Prompt、skills、memory、workspace profile 拆成可见文件，能让 agent 行为更容易复盘和局部修改。
- 前端 inspector + chat/tool/retrieval stream 是 VAKS 未来 context-pack workbench 的强候选界面模式。
- 检索分数、retrieval cards、tool outputs、compressed conversation summary 都只能是 activation / candidate context，不能替代 evidence-aware review。
- 允许 agent 或用户编辑 Memory / Skills / Workspace 文件时，必须加 agent memory quarantine、review_due、写入权限和 action gate。

## 风险和不确定

- 本次没有 clone 成功，也没有运行测试；代码审阅基于 GitHub 页面和 raw 文件。
- 仓库看起来是教学/面试型原型，成熟度有限。
- 顶层未观察到 license，代码复用前必须确认授权。
- 终端工具只靠简单 blacklist，安全边界不足。
- 前端/后端默认本地开发，无 auth、多租户、权限模型。
- memory 单文件 + vector index 没有 VAKS 所需的 truth/candidate/action 分层。
- RAG 模式下检索内容作为 assistant context 注入，容易在产品语义上被误读成“已确认记忆”。

## 下一步建议

- 作为“本地透明 Agent Workbench”候选来源保留。
- 后续 Direction Review 可把它和 CoMe、RAGLab、Obsidian local KB、Karpathy wiki 一起看。
- 不建议现在 fork 或集成。
- 如果要进一步验证，需要在新窗口解决 GitHub clone/TLS 或手动下载 snapshot，再跑最小本地启动检查。
