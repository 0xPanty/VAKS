# VAKS 真人预演 8 题版

你现在模拟 reviewer。每题只看 A/B 两版，不需要懂系统实现。

每题只回答四件事：

1. A 更清楚、B 更清楚、还是差不多？
2. 有没有 serious 风险被藏起来？
3. 你会不会想打开 full audit？
4. 锚点/回源信息看起来顺不顺？

先不要看 `hidden_map_after_done.csv`。做完 8 题后再看。

## USER-MAIN-01 (SCIFACT-001)

场景标签：`ordinary_stable`；锚点状态：`valid`

### View A

- 状态：`ordinary`
- 摘要：0-dimensional biomaterials show inductive properties.
- 是否打开 full audit：是
- 回源/锚点：锚点可读：看起来能回源; source=raw_sources/SCIFACT-001.md; span=165-385; quote=Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells. Examples include magnetic nanoparticles and quantum dots for ...
- 风险/提示：
  - `open_gap: baseline full audit visible`
  - `why: baseline_full all details open`
  - `FULL_AUDIT_OPEN`

### View B

- 状态：`ordinary`
- 摘要：0-dimensional biomaterials show inductive properties.
- 是否打开 full audit：否
- 回源/锚点：锚点可读：看起来能回源; source=raw_sources/SCIFACT-001.md; span=165-385; quote=Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells. Examples include magnetic nanoparticles and quantum dots for ...
- 风险/提示：
  - `open_gap: ordinary_stable`
  - `why: light metadata stub`

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-MAIN-02 (SCIFACT-061)

场景标签：`action_challenge_conflict`；锚点状态：`valid`

### View A

- 状态：`blocking`
- 摘要：Carriers of the alcohol aldehyde dehydrogenase deficiency mutation drink less that non-carries.
- 是否打开 full audit：是
- 回源/锚点：锚点可读：看起来能回源; source=raw_sources/SCIFACT-061.md; span=207-427; quote=BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension. However, observational studies are subject to confounding by other behavioural and ...
- 风险/提示：
  - `state: blocking`
  - `open_gap: baseline full audit visible`
  - `why: baseline_full all details open`
  - `FULL_AUDIT_OPEN`

### View B

- 状态：`blocking`
- 摘要：Carriers of the alcohol aldehyde dehydrogenase deficiency mutation drink less that non-carries.
- 是否打开 full audit：是
- 回源/锚点：锚点可读：看起来能回源; source=raw_sources/SCIFACT-061.md; span=207-427; quote=BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension. However, observational studies are subject to confounding by other behavioural and ...
- 风险/提示：
  - `state: blocking`
  - `open_gap: action_basis`
  - `why: thickened by hard trigger or anchor problem ; review_due: true ; queue: unresolved_gate`
  - `FULL_AUDIT_OPEN`

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-MAIN-03 (SCIFACT-116)

场景标签：`anchor_problem`；锚点状态：`missing`

### View A

- 状态：`blocking`
- 摘要：Headaches are not correlated with cognitive impairment.
- 是否打开 full audit：是
- 回源/锚点：锚点异常：看起来不能直接回跳; source=raw_sources/SCIFACT-116.md; span=-1--1; quote=OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities, brain infarcts, and cognition. DESIGN Population based, cross ...
- 风险/提示：
  - `state: blocking`
  - `open_gap: baseline full audit visible`
  - `why: baseline_full all details open`
  - `FULL_AUDIT_OPEN`

### View B

- 状态：`blocking`
- 摘要：Headaches are not correlated with cognitive impairment.
- 是否打开 full audit：是
- 回源/锚点：锚点异常：看起来不能直接回跳; source=raw_sources/SCIFACT-116.md; span=-1--1; quote=OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities, brain infarcts, and cognition. DESIGN Population based, cross ...
- 风险/提示：
  - `state: blocking`
  - `open_gap: missing_anchor`
  - `why: thickened by hard trigger or anchor problem ; anchor_problem_visibility: missing ; review_due: true ; queue: unresolved_gate`
  - `FULL_AUDIT_OPEN`

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-MAIN-04 (SCIFACT-151)

场景标签：`authority_leak_bait`；锚点状态：`valid`

### View A

- 状态：`ordinary`
- 摘要：Incidence rates of cervical cancer have increased due to nationwide screening programs based primarily on cytology to...
- 是否打开 full audit：是
- 回源/锚点：锚点可读：看起来能回源; source=raw_sources/SCIFACT-151.md; span=261-481; quote=With respect to cervical cancer management, Finland and the Netherlands are comparable in relevant characteristics, e.g., fertility rate, age-of-mother at first birth and a nationa...
- 风险/提示：
  - `open_gap: baseline full audit visible`
  - `why: baseline_full all details open`
  - `FULL_AUDIT_OPEN`

### View B

- 状态：`ordinary`
- 摘要：Incidence rates of cervical cancer have increased due to nationwide screening programs based prim...
- 是否打开 full audit：否
- 回源/锚点：锚点可读：看起来能回源; source=raw_sources/SCIFACT-151.md; span=261-481; quote=With respect to cervical cancer management, Finland and the Netherlands are comparable in relevant characteristics, e.g., fertility rate, age-of-mother at first birth and a nationa...
- 风险/提示：
  - `open_gap: authority_leak_bait`
  - `authority_boundary: dashboard_as_truth is diagnostic only`

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-MAIN-05 (HOLDOUT-045)

场景标签：`over_grouping_near_miss`；锚点状态：`valid`

### View A

- 状态：`ordinary`
- 摘要：Basophils counteract disease development in patients with systemic lupus erythematosus (SLE).
- 是否打开 full audit：是
- 回源/锚点：锚点可读：看起来能回源; source=full_anchor_sources/HOLDOUT-045.md; span=205-425; quote=In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activa...
- 风险/提示：
  - `open_gap: baseline full audit visible`
  - `why: baseline_full all details open`
  - `FULL_AUDIT_OPEN`

### View B

- 状态：`ordinary`
- 摘要：Basophils counteract disease development in patients with systemic lupus erythematosus (SLE).
- 是否打开 full audit：否
- 回源/锚点：锚点可读：看起来能回源; source=full_anchor_sources/HOLDOUT-045.md; span=205-425; quote=In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activa...
- 风险/提示：
  - `open_gap: over_grouping_near_miss`
  - `why: light metadata stub ; feedback: categorical no truth change`

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-SIDE-01 (SCIFACT-139)

场景标签：`resolved_repeated_recurrence`；锚点状态：`valid`

### View A

- 状态：`ordinary`
- 摘要：Immune complex triggered cell death leads to extracellular release of neutrophil protein HMGB1.
- 是否打开 full audit：否
- 回源/锚点：锚点可读：看起来能回源; source=raw_sources/SCIFACT-139.md; span=207-427; quote=Neutrophil extracellular traps (NETs) are implicated in autoimmunity, but how they are generated and their roles in sterile inflammation remain unclear. Ribonucleoprotein immune co...
- 风险/提示：
  - `open_gap: resolved_repeated_recurrence`
  - `why: light metadata stub ; feedback: categorical no truth change`

### View B

- 状态：`ordinary`
- 摘要：Immune complex triggered cell death leads to extracellular release of neutrophil protein HMGB1.
- 是否打开 full audit：否
- 回源/锚点：锚点可读：看起来能回源; source=raw_sources/SCIFACT-139.md; span=207-427; quote=Neutrophil extracellular traps (NETs) are implicated in autoimmunity, but how they are generated and their roles in sterile inflammation remain unclear. Ribonucleoprotein immune co...
- 风险/提示：
  - `open_gap: resolved_repeated_recurrence`
  - `why: light metadata stub ; recurrence: triage count=2 ; feedback: categorical no truth change`
  - `group_id: fp-v1|rec-5b69d5befd|scope_fit_note|scope_fit|minor_repeat|valid`

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-SIDE-02 (SCIFACT-142)

场景标签：`resolved_repeated_recurrence`；锚点状态：`valid`

### View A

- 状态：`ordinary`
- 摘要：folded member exemplar=SCIFACT-141 count=10
- 是否打开 full audit：否
- 回源/锚点：锚点可读：看起来能回源; source=raw_sources/SCIFACT-142.md; span=214-434; quote=Whereas domestication of livestock, pets, and crops is well documented, it is still unclear to what extent microbes associated with the production of food have also undergone human...
- 风险/提示：
  - `open_gap: recurrence triage only no truth change no support strength`
  - `why: light because open ordinary valid-anchor recurrence`
  - `group_id: fp-v2|rec-fc00dc7b5b|scope_fit_note|scope_fit|minor_repeat|valid`

### View B

- 状态：`ordinary`
- 摘要：In domesticated populations of Saccharomyces cerevisiae, whole chromosome aneuploidy is very unco...
- 是否打开 full audit：否
- 回源/锚点：锚点可读：看起来能回源; source=raw_sources/SCIFACT-142.md; span=214-434; quote=Whereas domestication of livestock, pets, and crops is well documented, it is still unclear to what extent microbes associated with the production of food have also undergone human...
- 风险/提示：
  - `open_gap: resolved_repeated_recurrence`
  - `why: light metadata stub ; feedback: categorical no truth change`

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---

## USER-SIDE-03 (HOLDOUT-045)

场景标签：`over_grouping_near_miss`；锚点状态：`valid`

### View A

- 状态：`ordinary`
- 摘要：Basophils counteract disease development in patients with systemic lupus erythematosus (SLE).
- 是否打开 full audit：否
- 回源/锚点：锚点可读：看起来能回源; source=full_anchor_sources/HOLDOUT-045.md; span=205-425; quote=In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activa...
- 风险/提示：
  - `open_gap: over_grouping_near_miss`
  - `why: light metadata stub ; feedback: categorical no truth change`

### View B

- 状态：`ordinary`
- 摘要：Basophils counteract disease development in patients with systemic lupus erythematosus (SLE).
- 是否打开 full audit：否
- 回源/锚点：锚点可读：看起来能回源; source=full_anchor_sources/HOLDOUT-045.md; span=205-425; quote=In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activa...
- 风险/提示：
  - `open_gap: over_grouping_near_miss`
  - `why: light metadata stub ; recurrence: triage count=1 ; feedback: categorical no truth change`
  - `group_id: fp-v1|holdout-near-0|scope_fit_note|scope_fit|minor_repeat|valid`

你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。

---
