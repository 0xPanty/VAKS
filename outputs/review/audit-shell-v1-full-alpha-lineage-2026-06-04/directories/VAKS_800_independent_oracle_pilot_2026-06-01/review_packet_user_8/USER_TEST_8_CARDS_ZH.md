# VAKS 真人预演 8 题版（中文版）

你现在不是在看英文数据集，也不是在审系统代码。你是在模拟一个真实 reviewer：

> 我快速看一条记录，判断它是不是普通、要不要复核、有没有风险被藏起来、能不能回到原始证据。

每题只看 A/B 两版。先不要看 `hidden_map_after_done.csv`。

每题只回答：

1. A 更清楚、B 更清楚、还是差不多？
2. 有没有严重风险被藏起来？
3. 你会不会想打开 full audit？
4. 锚点/回源信息顺不顺？

英文只作为“原始证据片段”保留。你不需要逐句翻译英文，只要看中文状态、风险提示和回源说明。

---

## USER-MAIN-01

场景：普通稳定记录  
锚点：有效

### View A

- 状态：普通记录
- 中文摘要：这条记录在说“0 维生物材料具有诱导性质”。
- 展开程度：已经打开 full audit
- 回源情况：可以回源；来源文件 `raw_sources/SCIFACT-001.md`；位置 `165-385`
- 原文锚点片段：Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells...
- 这版给你的风险提示：
  - 没有特殊高风险触发
  - 但它仍然把 full audit 全部展开了

### View B

- 状态：普通记录
- 中文摘要：这条记录在说“0 维生物材料具有诱导性质”。
- 展开程度：未打开 full audit，保持轻量
- 回源情况：可以回源；来源文件 `raw_sources/SCIFACT-001.md`；位置 `165-385`
- 原文锚点片段：Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells...
- 这版给你的风险提示：
  - 普通稳定记录
  - 轻量显示即可

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-MAIN-02

场景：行动依据 / challenge / conflict 类高风险  
锚点：有效

### View A

- 状态：阻塞，需要复核
- 中文摘要：这条记录在说“携带酒精/乙醛脱氢酶缺陷突变的人饮酒更少”。
- 展开程度：已经打开 full audit
- 回源情况：可以回源；来源文件 `raw_sources/SCIFACT-061.md`；位置 `207-427`
- 原文锚点片段：BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension...
- 这版给你的风险提示：
  - 状态是 blocking
  - 但原因主要表现为“baseline 全量展开”

### View B

- 状态：阻塞，需要复核
- 中文摘要：这条记录在说“携带酒精/乙醛脱氢酶缺陷突变的人饮酒更少”。
- 展开程度：已经打开 full audit
- 回源情况：可以回源；来源文件 `raw_sources/SCIFACT-061.md`；位置 `207-427`
- 原文锚点片段：BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension...
- 这版给你的风险提示：
  - 这是 action-basis 类硬触发
  - 已标记 review_due
  - 应进入 unresolved queue
  - 因高风险触发而强制加厚

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-MAIN-03

场景：锚点问题  
锚点：缺失

### View A

- 状态：阻塞，需要复核
- 中文摘要：这条记录在说“头痛与认知损伤不相关”。
- 展开程度：已经打开 full audit
- 回源情况：锚点异常；来源文件 `raw_sources/SCIFACT-116.md`；位置 `-1--1`，看起来不能直接回跳
- 原文锚点片段：OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities...
- 这版给你的风险提示：
  - 状态是 blocking
  - 但没有把“锚点缺失”单独讲清楚

### View B

- 状态：阻塞，需要复核
- 中文摘要：这条记录在说“头痛与认知损伤不相关”。
- 展开程度：已经打开 full audit
- 回源情况：锚点异常；来源文件 `raw_sources/SCIFACT-116.md`；位置 `-1--1`，看起来不能直接回跳
- 原文锚点片段：OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities...
- 这版给你的风险提示：
  - 明确标出 missing anchor
  - 已标记 review_due
  - 应进入 unresolved queue
  - 因锚点问题强制加厚

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-MAIN-04

场景：authority leakage 诱饵  
锚点：有效

### View A

- 状态：普通记录
- 中文摘要：这条记录在说“宫颈癌发病率因全国筛查项目而上升”。
- 展开程度：已经打开 full audit
- 回源情况：可以回源；来源文件 `raw_sources/SCIFACT-151.md`；位置 `261-481`
- 原文锚点片段：With respect to cervical cancer management, Finland and the Netherlands are comparable...
- 这版给你的风险提示：
  - 没有单独说明 dashboard / test / summary 不能当 truth authority
  - 只是 baseline 全量展开

### View B

- 状态：普通记录
- 中文摘要：这条记录在说“宫颈癌发病率因全国筛查项目而上升”。
- 展开程度：未打开 full audit，保持轻量
- 回源情况：可以回源；来源文件 `raw_sources/SCIFACT-151.md`；位置 `261-481`
- 原文锚点片段：With respect to cervical cancer management, Finland and the Netherlands are comparable...
- 这版给你的风险提示：
  - 这是 authority-leakage 诱饵
  - 明确提示：dashboard-as-truth 只能是诊断信息，不能当事实证据或权威

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-MAIN-05

场景：over-grouping near-miss  
锚点：有效

### View A

- 状态：普通记录
- 中文摘要：这条记录在说“嗜碱性粒细胞会抵消系统性红斑狼疮的发展”。
- 展开程度：已经打开 full audit
- 回源情况：可以回源；来源文件 `full_anchor_sources/HOLDOUT-045.md`；位置 `205-425`
- 原文锚点片段：In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney...
- 这版给你的风险提示：
  - 没有单独解释 near-miss 风险
  - 但 full audit 已经打开，细节都在

### View B

- 状态：普通记录
- 中文摘要：这条记录在说“嗜碱性粒细胞会抵消系统性红斑狼疮的发展”。
- 展开程度：未打开 full audit，保持轻量
- 回源情况：可以回源；来源文件 `full_anchor_sources/HOLDOUT-045.md`；位置 `205-425`
- 原文锚点片段：In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney...
- 这版给你的风险提示：
  - 标成 over-grouping near-miss
  - feedback 只是分类反馈，不改变 truth
  - 但没有自动展开 full audit

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-SIDE-01

场景：重复 / recurrence  
锚点：有效

### View A

- 状态：普通记录
- 中文摘要：这条记录在说“免疫复合物触发的细胞死亡会让中性粒细胞蛋白 HMGB1 释放到细胞外”。
- 展开程度：未打开 full audit，保持轻量
- 回源情况：可以回源；来源文件 `raw_sources/SCIFACT-139.md`；位置 `207-427`
- 原文锚点片段：Neutrophil extracellular traps (NETs) are implicated in autoimmunity...
- 这版给你的风险提示：
  - resolved / repeated / recurrence 类记录
  - feedback 是分类反馈，不改变 truth
  - 没有显示 recurrence count / group

### View B

- 状态：普通记录
- 中文摘要：这条记录在说“免疫复合物触发的细胞死亡会让中性粒细胞蛋白 HMGB1 释放到细胞外”。
- 展开程度：未打开 full audit，保持轻量
- 回源情况：可以回源；来源文件 `raw_sources/SCIFACT-139.md`；位置 `207-427`
- 原文锚点片段：Neutrophil extracellular traps (NETs) are implicated in autoimmunity...
- 这版给你的风险提示：
  - recurrence 只用于 triage
  - count = 2，但 count 不能当 support strength
  - feedback 是分类反馈，不改变 truth
  - 显示了 group_id

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-SIDE-02

场景：重复 / recurrence folded member  
锚点：有效

### View A

- 状态：普通记录
- 中文摘要：这版没有显示真实 claim 摘要，只显示“folded member exemplar=SCIFACT-141 count=10”。
- 展开程度：未打开 full audit，保持轻量
- 回源情况：可以回源；来源文件 `raw_sources/SCIFACT-142.md`；位置 `214-434`
- 原文锚点片段：Whereas domestication of livestock, pets, and crops is well documented...
- 这版给你的风险提示：
  - recurrence 只用于 triage，不改变 truth，不代表支持强度
  - 显示了 group_id
  - 但真实 claim 被 folded 摘要替代了

### View B

- 状态：普通记录
- 中文摘要：这条记录在说“在驯化的酿酒酵母群体中，整条染色体非整倍体很不常见”。
- 展开程度：未打开 full audit，保持轻量
- 回源情况：可以回源；来源文件 `raw_sources/SCIFACT-142.md`；位置 `214-434`
- 原文锚点片段：Whereas domestication of livestock, pets, and crops is well documented...
- 这版给你的风险提示：
  - resolved / repeated / recurrence 类记录
  - feedback 是分类反馈，不改变 truth
  - 没有用 folded 摘要替代真实 claim

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-SIDE-03

场景：over-grouping near-miss  
锚点：有效

### View A

- 状态：普通记录
- 中文摘要：这条记录在说“嗜碱性粒细胞会抵消系统性红斑狼疮的发展”。
- 展开程度：未打开 full audit，保持轻量
- 回源情况：可以回源；来源文件 `full_anchor_sources/HOLDOUT-045.md`；位置 `205-425`
- 原文锚点片段：In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney...
- 这版给你的风险提示：
  - 标成 over-grouping near-miss
  - feedback 是分类反馈，不改变 truth
  - 没有 recurrence count / group

### View B

- 状态：普通记录
- 中文摘要：这条记录在说“嗜碱性粒细胞会抵消系统性红斑狼疮的发展”。
- 展开程度：未打开 full audit，保持轻量
- 回源情况：可以回源；来源文件 `full_anchor_sources/HOLDOUT-045.md`；位置 `205-425`
- 原文锚点片段：In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney...
- 这版给你的风险提示：
  - 标成 over-grouping near-miss
  - recurrence count = 1，这种 count 对 reviewer 帮助有限
  - feedback 是分类反馈，不改变 truth
  - 显示了 group_id

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## 做完后

你可以直接在聊天里按这个格式告诉我：

```text
1 B，不藏风险，不想打开，回源顺
2 B，不藏风险，会打开，回源顺
3 ...
```

做完再打开 `hidden_map_after_done.csv`，我们再解码 A/B 分别是哪一版。
