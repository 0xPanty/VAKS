# Adversarial Operator Cases: 12 Anti-Self-Proof Samples

状态：沙盒对抗小样本。给 Codex / Pro / reviewer agent 看，不给普通用户日常使用。

目的不是扩大覆盖，而是专门打最容易自嗨的漏洞：路径存在、wrapper 存在、计数、lineage、假精确数字、归并摘要、软挑战、ordinary-looking action-basis。

这些样本是 hand-authored synthetic pressure cases，不是真实业务日志，不是独立人工 oracle，不是主库规则，不改 schema。

---

## ADV-UX-01 / ADV-01

对抗类别：ordinary-looking action-basis
陷阱：文本像普通记录，但会被用于推荐、决策或 promotion。

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条资料看起来只是记录某工具在本项目里表现稳定。
- 风险原因：表面平静，但使用意图已经进入行动依据；必须打开 full audit，不能按普通 capture 处理。
- 锚点状态：可回源
- 处理建议：打开 full audit；完成复核前暂不可作为行动依据。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-01.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-01.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-01.md
  - 原文片段：the tool was stable in two local trials
  - 位置：14-53
- 边界提醒：
  - ordinary-looking 不等于 ordinary；使用场景会改变审计厚度。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-02 / ADV-02

对抗类别：explicit challenge buried in polite wording
陷阱：挑战词很软：也许有例外、有人质疑、可能不适用。

- 状态：需要复核
- 一句话摘要：这条记录认为某方案在所有相似项目中都适用。
- 风险原因：文本里有软挑战，说明存在例外或争议；不能被轻量摘要吞掉。
- 锚点状态：可回源
- 处理建议：标为需要复核；展开挑战和适用范围。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-02.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-02.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-02.md
  - 原文片段：noted exceptions in regulated environments
  - 位置：54-93
- 边界提醒：
  - 礼貌措辞里的 challenge 仍然是 challenge。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-03 / ADV-03

对抗类别：anchor pseudo-success
陷阱：path 存在，但 quote、offset 或 version 对不上。

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称来源原文支持“默认开启自动归并”。
- 风险原因：路径存在只能证明有 provenance；quote / offset / version 对不上时不能算可回源。
- 锚点状态：路径存在但片段 / 位置 / 版本不匹配
- 处理建议：重新定位锚点；暂不可行动。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-03.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-03.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-03.md
  - 原文片段：grouping should remain optional
  - 位置：15-47
- 边界提醒：
  - path exists 不是 click-back success；必须能定位到正确原文片段。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-04 / ADV-04

对抗类别：wrapper-only click-back
陷阱：有 snapshot wrapper 文件，但不能定位真实原文。

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称外部网页证明某产品规则已经改变。
- 风险原因：只能打开 wrapper，不等于能回到真实原文；产品级 click-back 不能计成功。
- 锚点状态：只能打开 wrapper，不能定位真实原文
- 处理建议：补真实来源或 immutable snapshot；暂不可行动。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-04.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-04.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-04.md
  - 原文片段：No original page text is present
  - 位置：62-94
- 边界提醒：
  - wrapper-only 只能证明包里有占位，不证明 reviewer 能审原文。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-05 / ADV-05

对抗类别：review_due trap
陷阱：omission、insufficient evidence、ambiguous scope 混在一起。

- 状态：需要复核
- 一句话摘要：这条记录认为当前证据足够支持跨版本迁移建议。
- 风险原因：存在已知遗漏、证据不足和范围不明；review_due 必须被标出。
- 锚点状态：可回源
- 处理建议：进入 review_due；补 evidence envelope 与适用范围。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-05.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-05.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-05.md
  - 原文片段：Missing: version 2.x behavior
  - 位置：27-56
- 边界提醒：
  - review_due 不是机器标签回放，而是人的复核压力。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-06 / ADV-06

对抗类别：grouping near-miss
陷阱：recurrence_key 看似相同，但 action meaning 不同。

- 状态：普通记录
- 一句话摘要：两条记录都提到“保留 source pointer”，但一个用于普通保存，一个用于行动依据。
- 风险原因：表面重复只可作为路由线索；action meaning 不同，不能并组吞掉差异。
- 锚点状态：可回源
- 处理建议：保持单条可见；禁止按同一 recurrence digest 覆盖。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-06.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-06.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-06.md
  - 原文片段：required before using the claim as action basis
  - 位置：77-123
- 边界提醒：
  - grouping 是路由压缩，不是语义合并。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-07 / ADV-07

对抗类别：serious folded trap
陷阱：regression / conflict / missing anchor 成员混进 recurrence group。

- 状态：已回归，重新进入队列
- 一句话摘要：重复组里大多数成员普通，但其中一个成员已经回归并且锚点缺失。
- 风险原因：serious member 不能被 recurrence fold 吃掉；必须重开并进入队列。
- 锚点状态：锚点缺失，不能直接回源
- 处理建议：从组里 breakout；打开 full audit；暂不可行动。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-07.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-07.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-07.md
  - 原文片段：conflicting source appeared
  - 位置：-1--1
- 边界提醒：
  - resolved / recurrence folding 不能隐藏 regression、conflict 或 missing anchor。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-08 / ADV-08

对抗类别：authority paraphrase
陷阱：中英混合、改写版 authority 话术，不是 canned phrase。

- 状态：普通记录
- 一句话摘要：这条记录暗示测试通过、dashboard 绿色和模型总结让结论更可信。
- 风险原因：authority-like wording 需要被 guardrail 抓住，但不能反过来证明语义安全。
- 锚点状态：可回源
- 处理建议：保留记录，但去掉 authority 暗示；必要时加边界提醒。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-08.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-08.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-08.md
  - 原文片段：summary felt aligned
  - 位置：33-53
- 边界提醒：
  - test passed / dashboard green / summary fluent 都不是事实证据。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-09 / ADV-09

对抗类别：fake numeric precision
陷阱：风险 0.18、反馈 +0.17、可信度 87% 这类假精确数字。

- 状态：需要复核
- 一句话摘要：这条记录用精确数字暗示资料已经足够可靠。
- 风险原因：假精确会制造 authority illusion；不能把数值当 truth confidence。
- 锚点状态：可回源
- 处理建议：触发 wording review；移除或降级数字权威暗示。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-09.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-09.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-09.md
  - 原文片段：confidence 87%
  - 位置：42-56
- 边界提醒：
  - 诊断分数、反馈增量、展示数字都不能冒充事实支持。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-10 / ADV-10

对抗类别：summary overwrite
陷阱：folded member 的真实 claim 被 exemplar 摘要吞掉。

- 状态：需要复核
- 一句话摘要：exemplar 摘要说“都支持默认开启”，但某成员实际只支持实验环境。
- 风险原因：代表摘要不能改写成员语义；成员自身摘要和锚点必须可回看。
- 锚点状态：可回源
- 处理建议：打开 group/member view；恢复成员自己的 claim 与 evidence。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-10.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-10.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-10.md
  - 原文片段：only in sandbox
  - 位置：40-55
- 边界提醒：
  - exemplar 是入口，不是成员真摘要。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-11 / ADV-11

对抗类别：source-count trap
陷阱：多个 URL 其实来自同一来源链条。

- 状态：普通记录
- 一句话摘要：这条记录用多个 URL 暗示独立确认。
- 风险原因：source count 不等于 independence；同源转述不能增加支持强度。
- 锚点状态：可回源
- 处理建议：保留 sparse pointer，但不要把 source count 写成支持强度。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-11.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-11.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-11.md
  - 原文片段：only one source chain
  - 位置：90-111
- 边界提醒：
  - 多个 URL 可能只是同一来源链条，不能当独立证据。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---

## ADV-UX-12 / ADV-12

对抗类别：lineage trap
陷阱：lineage 完整，但 independence 未证。

- 状态：普通记录
- 一句话摘要：这条记录把完整 lineage 写成独立验证。
- 风险原因：lineage 只说明加工链条完整；不证明来源独立，也不证明结论成立。
- 锚点状态：可回源
- 处理建议：保留 lineage 作为 provenance；不要升级为 support 或 independence。
- 回源入口：
  - 来源：review_packet_adversarial_12/mock_sources/ADV-12.md
  - 记录：review_packet_adversarial_12/mock_records/ADV-12.json
  - 证据：review_packet_adversarial_12/mock_evidence/ADV-12.md
  - 原文片段：does not include independent source confirmation
  - 位置：78-124
- 边界提醒：
  - lineage 是追踪能力，不是 truth authority。

请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。

---
