# Pro 证据底稿的迁移补充

记录日期：2026-10-19。此文件只记录迁移恢复，不是重新研究、重跑测试或采纳 Pro 结论。

## 恢复结果与限制

- 原会话：[评审保有據VAKS方案](https://chatgpt.com/c/6ab7f4bb-3938-83ec-aa52-cc67d92efbc5)。主报告已完整保存在 [评审原文](../../outputs/review/2026-09-27-baoyouju-vaks-pro-review-response.md)。
- 原报告生成的附件名：`baoyouju_review_evidence_2026-09-27.md`，报告中的地址为 `sandbox:/mnt/data/baoyouju_review_evidence_2026-09-27.md`。该地址不是 Mac 文件路径，也不是可通用下载的 GitHub 链接。
- 本次成功打开原附件预览，确认标题为“保有據 × VAKS：评审证据定位与成本计算底稿”。读取到整段预览文本 76,144 个 JavaScript 字符、UTF-8 91,003 字节；计数包含预览标题和界面渲染文字，**不是原 Markdown 文件的字节数或哈希**。
- 主报告和预览的两个下载入口均未取得可确认的本地文件；因此没有宣称已恢复原附件或其原始字节。下面保存预览中第 3–5 节的内容转写及全部 21 条链接，便于 Mac 直接查阅；第 1–2 节未在此重复转写。附件原件仍是一个明确的迁移限制。
- 预览第 1–2 节是评审包完整性说明及 E01–E13 的包内证据定位；对应评审包、原文及代码摘录已在 Git 中。原件与本文件的转写不能混为一份经哈希确认的材料。

## 包内定位索引（按预览保留标题）

1. E01 — 快照范围与任务书
2. E02 — 产品 draft-2：职责、发布、风险与候选业务
3. E03 — 来源保存与完整性校验：包内代码原路径行号
4. E04 — 只读 Guard：不授予事实、审阅或执行权
5. E05 — 检索：知识状态过滤、本地词项、正文前 20000 字符
6. E06 — R1.5/R1.6 限定范围与性能预算
7. E07 — 已有时间和适用性设计，不应误判为概念缺失
8. E08 — Agent 权限与 Context Pack 是文档契约
9. E09 — 实施蓝图：分层、排序、降级、未来运行时
10. E10 — 来源存储契约与派生快照索引
11. E11 — 轻量查询及证据/行动边界
12. E12 — 最新融合文档与历史实验的适用边界
13. E13 — 历史 handoff：只读、沙箱、当时真实记录状态

## 第 3 节：可复算成本情景（预览转写，表格排版整理）

全部用量和人工时间为假设，不是实测。价格读取日期为 2026-09-27，单位为美元。公开列价只供预算比较，不代表已确认采购资格、区域、企业批准或业务效果；本次迁移没有刷新价格。

| 参数 | 值 |
|---|---|
| 每次生成输入 | 8000 token |
| 每次生成总计费输出（含推理） | 1500 token |
| 预留计费用量增加 | 10%（假设，非测得失败率） |
| Gemini 2.5 Flash 每百万输入/输出 | USD 0.30 / 2.50 |
| Gemini 2.5 Pro 每百万输入/输出 | USD 1.25 / 10.00 |
| Jev 输入每百万 | USD 0.042；输出免费 |
| Jev 候选比较用量 | 每任务 20×700 = 14000 输入 token（假设） |
| 换算 | USD 1 = HKD 7.8，仅计算假设 |

单次生成成本 = (输入 token × 输入单价 + 总计费输出 token × 输出单价) / 1000000 × 1.1。双遍为两次相同预算调用，不假定第二遍可以证明事实正确。

| 月任务数 | Flash 单遍 USD | Pro 单遍 USD | Flash 双遍 USD | Pro 双遍 USD | Jev 另增 USD |
|---|---|---|---|---|---|
| 100 | 0.6765 | 2.7500 | 1.3530 | 5.5000 | 0.0588 |
| 500 | 3.3825 | 13.7500 | 6.7650 | 27.5000 | 0.2940 |
| 4000 | 27.0600 | 110.0000 | 54.1200 | 220.0000 | 2.3520 |

音频敏感性：单声道 30 分钟×100 次/月=3000 分钟；Google STT V2 标准 USD 0.016/分钟 => USD 48/月；低优先级动态批次 USD 0.003/分钟 => USD 9/月。后者不是同等延迟服务。不含存储、传输、重试、转录校对和后续生成。

小团队 500 任务/月：维护 6–12 小时/月、支持 2–4 小时/月、时间价值 HKD 250/小时；基础设施预算 USD 20–100/月（预算占位，非供应商报价）；加单遍生成费用，月固定及后台用量约 HKD 2182.38–4887.25。未计建设、初次整理、公司审批、专业审查或音频。每任务净节约约 1.05–2.35 分钟才抵消这一组假设开销。人工任务时间应按原流程与新流程配对计算，不能把已计入新流程的人工审阅再次作为新增成本扣除。

延迟敏感性（非实测、非 SLA、非 p95）：认证/检索/核对 0.2–1.5 秒 + 模型初始等待 1–5 秒 + 1500 输出 token÷20–80 token/秒，约 20–82 秒；额外排队、推理等待、限流、重试另计。Jev 假设 20 项、并发 5、每波 0.2–0.8 秒，则仅重排增加约 0.8–3.2 秒。

## 第 4 节：外部来源记录（链接取自原预览）

所有页面研究时点为 2026-09-27。日期未标注者不推定发布日期。以下说明为原评审的记录，本次迁移未重新打开核验各网站。

| 来源 | 原评审记录的用途或限制 |
|---|---|
| [PCPD，Agentic AI 个人资料指引（PDF）](https://www.pcpd.org.hk/english/resources_centre/publications/files/pcpd_use_of_agentic_ai.pdf) | 实际读取及截图；指引不是公司授权或销售合规批准 |
| [TypeSafe，模型与价格](https://docs.typesafe.ai/models) | 读取时 jev-1.13.0；别名和价格可能变化 |
| [TypeSafe，Jev 1.13 已知限制](https://docs.typesafe.ai/model-jaggedness/jev-1.13) | 数字、日期、复杂否定、上下文干扰和对抗内容风险 |
| [TypeSafe，API quickstart](https://docs.typesafe.ai/introduction/quickstart) | 云 API 请求形态；未调用 |
| [TypeSafe，重排示例](https://docs.typesafe.ai/cookbooks/rerank_typesafe) | 厂商小样本示例，不是香港保险实测 |
| [TypeSafe，法律文件入口](https://docs.typesafe.ai/legal) | ZDR 为企业条件，不能等同默认不保存 |
| [TypeSafe，DPA](https://typesafe.ai/legal/data-processing) | 合同条件仍须正式采购审查 |
| [Microsoft，Copilot 架构](https://learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-architecture) | 用户权限边界；不是 VAKS 验证 |
| [AWS，知识库同步](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-data-source-sync-ingest.html) | 变更需同步/重建派生索引；不是即时撤权保证 |
| [AWS，检索与生成](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-retrieval.html) | Retrieve 与 RetrieveAndGenerate 分离 |
| [Google Cloud，RAG 参考架构](https://docs.cloud.google.com/architecture/gen-ai-rag-vertex-ai-vector-search) | 摄入与 serving 分层；参考架构而非项目认可 |
| [Google Cloud，生成模型价格](https://cloud.google.com/vertex-ai/generative-ai/pricing) | 标准 Gemini 2.5 价格；原评审记录页面已重定向至 Agent Platform 价格 |
| [Google Cloud，Speech-to-Text 价格](https://cloud.google.com/speech-to-text/pricing) | 单声道与多声道计费、标准与动态批次区别 |
| [腾讯云，WorkBuddy 产品/团队页](https://www.tencentcloud.com/act/pro/workbuddy) | 团队 RAG、共享 Skills、管理及价格是厂商公开声明，未实测 |
| [腾讯云，WorkBuddy 桌面产品文档](https://www-sg.tencentcloud.com/document/product/1300/81046) | 区分桌面、团队和企业采购范围 |
| [x.ai，Grok Bot overview](https://docs.x.ai/grok-bot/overview) | 与普通 Grok 聊天/社交机器人区分 |
| [x.ai，Grok Bot Skills/Routines](https://docs.x.ai/grok-bot/skills-routines-and-automations) | 共享工作流能力；未实测 |
| [x.ai，Grok Bot 安全与私隐](https://docs.x.ai/grok-bot/approvals-security-and-privacy) | 共享云电脑、存储及管理员约束；原评审记录页面标示 SpaceXAI |
| [Meta，Muse 安全架构](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse) | 原评审记录 2026-09-08；作为 MUSE 候选身份，原讨论未给链接仍有歧义 |
| [HKU CLIC，保险中介操守说明](https://www.clic.org.hk/en/topics/insurance/how_can_I_get_an_insurance_policy/insurance_intermediaries/q3) | 二级法律解说，不能代替现行 IA 守则全文 |
| [IPD 商标查询入口](https://esearch.ipd.gov.hk/) | 仅确认入口，未完成注册库检索或名称清查 |

## 第 5 节：未完成核验（按预览保留）

IA 现行守则全文的直接读取未成功；知识产权署版权/AI 例外的现行官方适用资料未取得充分核验；未以旧资料断言 PDPO 第 33 条在研究时点的生效状态；未取得公司内部资料许可、云模型采购批准、真实客户处理授权；未确认 Jev 的公开自托管服务、默认精确保留时长或本团队合同；未实测竞品，未取得原讨论 MUSE 确切链接，未完成商标注册库检索。上述不足不被普通网页、厂商营销、历史测试或第三方概述替代。

MUSE 的身份仍应按用户实际使用的产品核对；本次没有据域名或旧助手结论宣布原评审身份正确或错误。该不确定性保留至后续产品评审。
