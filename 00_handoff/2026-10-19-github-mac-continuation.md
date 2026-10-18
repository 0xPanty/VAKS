# GitHub / Mac 开发接续记录 — 2026-10-19

## 本次目标与边界

用户要求把 VAKS 的全部项目内容、设计细节和开发进度上传自己的 GitHub，以便在 Mac 延续开发。本次是项目迁移与完整性整理，不是保险产品部署，也不把候选方案、sandbox 或历史测试结果晋升为主线能力。

迁移前：分支 `master`，HEAD `10e7be9ac4630730473f3c6c30622b31dabab998`，57 个提交，没有远程仓库，有大量尚未提交的修改与新增研究/实验。保留既有提交历史和工作树的 VAKS 修改。目标为私有 `0xPanty/VAKS`。

首次上手请读 [START_HERE_MAC.md](../START_HERE_MAC.md)。最终 GitHub 提交及附件上传结果以迁移报告与实际远程状态为准；此 handoff 不以“创建了说明文件”代替上传确认。

## 现在到底有哪些东西

| 部分 | 恢复入口 | 应怎样理解 |
|---|---|---|
| 架构主线 | `README.md`、`FUSION_ARCHITECTURE_V0_2_DRAFT.md`、`SCHEMA.md` | Capture → Understand → Review → Connect → Act and Learn；轻入口、关键用途懒闸门 |
| 主线工具与最近主线交接 | `00_handoff/2026-06-22-vaks-guard-closeout-and-bases-park-handoff.md`、`tools/vaks_guard.py` | Guard 已落地为只读检查器；大部分 sandbox 未自动并入主线 |
| Source Capture | `docs/source-capture-store-v1.md`、`tools/store_source_capture.py`、`tools/verify_source_capture_store.py`、`tools/rebuild_source_snapshot_index.py` | 本地捕获、内容存储、校验、派生索引已有代码；不等于生产知识服务 |
| Fragment Candidate | `docs/fragment-candidate-v1.md`、`tools/validate_fragment_candidate.py` | 保留实现及候选契约，不能把 fragment 当已审知识 |
| 检索设计 | `outputs/review/vaks-retrieval-layer-design-2026-06-11/retrieval-layer-north-star.md`、同目录 `progress.md` | 候选研究与设计 |
| 本地只读查询实验 | `outputs/review/source-intake-generic-readonly-loop-2026-06-14/GENERIC_READONLY_LOOP_REPORT.md` | 工具与实验结果，不是完整产品服务 |
| r0.5 真实只读查询证据 | `outputs/review/source-intake-real-readonly-evidence-loop-r0-5-2026-06-23/r0_5_summary.json`、同目录 `LIMITS.md` | 3 次受限查询；本地词项检索与确定性 plans，未验证真实 IAM / LLM |
| R1.5 | `outputs/review/vaks-supervised-trial-adapter-preflight-r1-5-r47-2026-06-25/summary.json` | 历史通过只支持单账户低风险有监督试用建议；真实 IAM、模型质量、生产延迟未证明 |
| R1.6 最新完整结果 | `outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json`、`CONTRACT.md`、`LIMITS.md` | 历史试验结果；不写正式 vault，不是生产验收 |
| R1.6 当前代码 | `tools/vaks_disposable_vault_trial_r1_6.py` | RUN_ID 已到 r218，但 `r218-2026-08-23` 只有测试残留，没有 summary / 完成收据；不能继承 r217 的通过结论 |
| 保险团队助手 | `outputs/review/2026-09-26-vaks-insurance-team-plan-candidate.md` | “保有據”暂名，draft-2 / candidate；先本人和小团队，未批准广泛商业化 |
| Pro 评审 | `outputs/review/2026-09-27-baoyouju-vaks-pro-review-response.md` | 完整外部评审意见存档，Conditional Go 有范围限制；未自动采纳 |

研究来源、来源锚点、source annotations、Project Overlay、模板、schemas、tests、实验完整结果及历史评审 ZIP 均是有价值的恢复材料。目录名出现 production / ready / pass 不能脱离该目录的 LIMITS、契约和日期作能力结论。

## 正式 vault 的补齐办法

正式 vault 为 `H:\Obsidian\资料库`，工程为当前 Git 仓库。保险方案三份原始路径此前缺失，但 Pro 包内存在字节相同副本；本次将原路径补齐，便于 Mac 继续维护与跳转。

完整比对见 `docs/migration/2026-10-19-vault-comparison.json`。相同内容不复制；当前仓库已有但不同的文件不覆盖，而把正式 vault 版本保存为迁移参考快照。已在当前 Git 工作树明确删除的旧路径不自动恢复到原位置，必要时保存为历史参考。所有复制遵循 SHA256 检查。

这些副本仍是既有材料的存档，不创造新的知识审核结论。原始来源状态、候选状态、历史决议和当前设计解释分别保留。

## Mac 接下来做什么

1. 克隆后对照迁移清单；需要完整第三方快照时恢复私有 Release 附件。
2. 在 Mac 创建 Python 环境，跑接续入口里的基础自检，记录真实 Mac 结果；先处理路径与 Python 依赖，不直接跑 r218 或视频同步。
3. 决定本轮实际开发切口。若推进保险团队助手，优先评估“会谈后核对单＋有出处的回复草稿”的单一业务闭环；这是 Pro 的候选建议，仍需用户定范围与公司资料授权。
4. 若继续 VAKS 内核，先核实 r218 的未完成状态和既有 TODO；不要把各实验线统一称为已完成，也不为迁移继续扩大架构。

当前不能宣称有多租户 SaaS、生产 IAM、经过验证的保险产品推荐、端到端延迟保证，或已获公司内部资料使用许可。

## 本次验证范围

- Python 3.12.14 / Windows，Source Capture implementation manifest `--check`：6 个组件通过。
- Guard self-test：7 类检查通过，manifest 160 个 case hash。
- `selftest_source_capture.py`：99 项通过。
- `selftest_source_capture_store.py`：62 项通过。
- 完整源文件及大附件 hash、Git 对象/路径与同步后远程提交在迁移记录中另行记录。
- 尚未真实执行 macOS 验证；上述结果不代表所有 sandbox、生产运行或保险业务验收通过。

不要修改历史评审包中的 manifest 或源码摘录来“对齐”今天的文件：它们记录的是当时快照。
