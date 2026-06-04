# Risk-Tiered Reviewer UX Preflight: 24 Chinese Operator Samples

状态：沙盒小样本预演材料。给 AI / reviewer operator 使用，不是普通用户日常流程，不是正式 human timing，不是 independent human oracle，不是主库规则。

使用者是 Codex / Pro / reviewer agent。每条记录只看中文 operator 前脸，判断它为什么轻量或加厚、下一步怎么处理、能不能回源、有没有 authority 误读。

普通用户不需要读这些卡片；用户只应在风险影响回答或行动时看到一句人话提醒。

全局边界：本卡用于分流与回源，不替代原始证据；重复数不表示支持强度；lineage 不证明独立性；test/dashboard/lint 不证明事实成立。

---

## RISK-UX-01 / SCIFACT-001

样本类型：普通稳定记录

- 状态：普通记录
- 一句话摘要：这条记录声称：0-dimensional biomaterials show inductive properties.
- 中文导读：先轻量保存；只有进入行动依据或出现硬触发时才打开 full audit。
- 风险原因：普通稳定记录，无硬触发；保持轻量即可。
- 锚点状态：可回源
- 处理建议：轻量保存；如需行动依据，请打开完整审计包
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/SCIFACT-001.md）
  - 记录入口：打开记录（句柄：records/SCIFACT-001.json）
  - 证据入口：打开证据（句柄：evidence/SCIFACT-001.md）
  - 原文片段：Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells. Examples include magnetic nanoparticles and quantum dots for stem cell labeling and in vivo tracking;
  - 位置：165-385
  - 语义落点：未显示

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-02 / AVERITEC-001

样本类型：普通稳定记录

- 状态：普通记录
- 一句话摘要：这条记录声称：Hunter Biden had no experience in Ukraine or in the energy sector when he joined the board of Burisma.
- 中文导读：先轻量保存；只有进入行动依据或出现硬触发时才打开 full audit。
- 风险原因：普通稳定记录，无硬触发；保持轻量即可。
- 锚点状态：可回源
- 处理建议：轻量保存；如需行动依据，请打开完整审计包
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/AVERITEC-001.md）
  - 记录入口：打开记录（句柄：records/AVERITEC-001.json）
  - 证据入口：打开证据（句柄：evidence/AVERITEC-001.md）
  - 原文片段：No No
  - 位置：217-222
  - 语义落点：未显示

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-03 / AMBIFC-001

样本类型：普通稳定记录

- 状态：普通记录
- 一句话摘要：这条记录声称：a irrational number can be a real number.
- 中文导读：先轻量保存；只有进入行动依据或出现硬触发时才打开 full audit。
- 风险原因：普通稳定记录，无硬触发；保持轻量即可。
- 锚点状态：可回源
- 处理建议：轻量保存；如需行动依据，请打开完整审计包
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/AMBIFC-001.md）
  - 记录入口：打开记录（句柄：records/AMBIFC-001.json）
  - 证据入口：打开证据（句柄：evidence/AMBIFC-001.md）
  - 原文片段：* Since c is even, dividing c by 2 yields an integer. Let y be this integer (c = 2y). * Squaring both sides of c = 2y yields c2 = (2y)2, or c2 = 4y2. * Substituting 4y2 for c2 in the first equation (c2 = 2b2) gives us 4y
  - 位置：150-370
  - 语义落点：未显示

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-04 / SCIFACT-061

样本类型：行动依据 / 明确挑战 / 冲突

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称：Carriers of the alcohol aldehyde dehydrogenase deficiency mutation drink less that non-carries.
- 中文导读：先判断为不可行动并打开 full audit；英文 claim 只作原文内容，不替代复核。
- 风险原因：涉及行动依据，必须打开 full audit。
- 锚点状态：可回源
- 处理建议：打开 full audit；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/SCIFACT-061.md）
  - 记录入口：打开记录（句柄：records/SCIFACT-061.json）
  - 证据入口：打开证据（句柄：evidence/SCIFACT-061.md）
  - 原文片段：BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension. However, observational studies are subject to confounding by other behavioural and sociodemographic factors, while clinical
  - 位置：207-427
  - 语义落点：未显示

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-05 / AVERITEC-061

样本类型：行动依据 / 明确挑战 / 冲突

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称：Democrats recited the US Pledge of Allegiance tonight and took out "under God".
- 中文导读：先判断为不可行动并打开 full audit；英文 claim 只作原文内容，不替代复核。
- 风险原因：涉及行动依据，必须打开 full audit。
- 锚点状态：可回源
- 处理建议：打开 full audit；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/AVERITEC-061.md）
  - 记录入口：打开记录（句柄：records/AVERITEC-061.json）
  - 证据入口：打开证据（句柄：evidence/AVERITEC-061.md）
  - 原文片段：The Pledge of Allegiance to the Flag: "I pledge allegiance to the Flag of the United States of America, and to the Republic for which it stands, one Nation under God, indivisible, with liberty and justice for all," shoul
  - 位置：194-414
  - 语义落点：未显示

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-06 / AMBIFC-061

样本类型：行动依据 / 明确挑战 / 冲突

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称：in finding dory, dory finds her parents.
- 中文导读：先判断为不可行动并打开 full audit；英文 claim 只作原文内容，不替代复核。
- 风险原因：涉及行动依据，必须打开 full audit。
- 锚点状态：可回源
- 处理建议：打开 full audit；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/AMBIFC-061.md）
  - 记录入口：打开记录（句柄：records/AMBIFC-061.json）
  - 证据入口：打开证据（句柄：evidence/AMBIFC-061.md）
  - 原文片段：In the United States and Canada, Finding Dory opened on June 17, 2016, alongside Central Intelligence, with projections having the film grossing $110–120 million in its opening weekend, with some estimates going as high
  - 位置：149-369
  - 语义落点：未显示

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-07 / SCIFACT-116

样本类型：锚点问题

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称：Headaches are not correlated with cognitive impairment.
- 中文导读：先判断为暂不可行动；本轮重点是识别锚点缺失并要求补锚点。
- 风险原因：锚点缺失，不能直接回源，需要先处理回源问题。
- 锚点状态：锚点缺失，不能直接回源
- 处理建议：补锚点；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/SCIFACT-116.md）
  - 记录入口：打开记录（句柄：records/SCIFACT-116.json）
  - 证据入口：打开证据（句柄：evidence/SCIFACT-116.md）
  - 原文片段：OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities, brain infarcts, and cognition. DESIGN Population based, cross sectional study. SETTING Epidemiology of
  - 位置：-1--1
  - 语义落点：未显示
- 定向边界提醒：
  - 有 provenance 不等于有可用 support；锚点异常时不能作为行动依据。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-08 / AVERITEC-116

样本类型：锚点问题

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称：The murder of Oscar Grant, by a police officer in the United States, was never prosecuted by the DA.
- 中文导读：先判断为暂不可行动；本轮重点是识别锚点缺失并要求补锚点。
- 风险原因：锚点缺失，不能直接回源，需要先处理回源问题。
- 锚点状态：锚点缺失，不能直接回源
- 处理建议：补锚点；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/AVERITEC-116.md）
  - 记录入口：打开记录（句柄：records/AVERITEC-116.json）
  - 证据入口：打开证据（句柄：evidence/AVERITEC-116.md）
  - 原文片段：Oscar Grant, 22, was shot once while on the platform after a BART officer drew his gun during what officials called a volatile and chaotic scene. A gravely wounded Grant was taken to Highland Hospital, where he died Yes
  - 位置：-1--1
  - 语义落点：未显示
- 定向边界提醒：
  - 有 provenance 不等于有可用 support；锚点异常时不能作为行动依据。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-09 / AMBIFC-116

样本类型：锚点问题

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称：avatar is the last airbender a disney movie.
- 中文导读：先判断为暂不可行动；本轮重点是识别锚点缺失并要求补锚点。
- 风险原因：锚点缺失，不能直接回源，需要先处理回源问题。
- 锚点状态：锚点缺失，不能直接回源
- 处理建议：补锚点；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/AMBIFC-116.md）
  - 记录入口：打开记录（句柄：records/AMBIFC-116.json）
  - 证据入口：打开证据（句柄：evidence/AMBIFC-116.md）
  - 原文片段：Rob Keyes of Screen Rant called the series "one of the greatest cartoons ever made". Mike Noyes of Inside Pulse recommended it to viewers who enjoy "great" adventure. Gord Lacey of TVShowsonDVD.com called the series "one
  - 位置：-1--1
  - 语义落点：未显示
- 定向边界提醒：
  - 有 provenance 不等于有可用 support；锚点异常时不能作为行动依据。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-10 / SCIFACT-091

样本类型：已知遗漏 / 证据不足 / 范围不明

- 状态：需要复核
- 一句话摘要：这条记录声称：Discrimination between the initiator and elongation tRNAs depends on the translation initiation factor IF3.
- 中文导读：先判断为需要复核；重点看缺口、挑战、范围和证据充分性。
- 风险原因：存在已知遗漏或证据缺口，不能直接行动。；适用范围或证据充分性不清，需要复核。
- 锚点状态：可回源
- 处理建议：打开 full audit；完成复核前不要作为行动依据
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/SCIFACT-091.md）
  - 记录入口：打开记录（句柄：records/SCIFACT-091.json）
  - 证据入口：打开证据（句柄：evidence/SCIFACT-091.md）
  - 原文片段：In bacterial translational initiation, three initiation factors (IFs 1-3) enable the selection of initiator tRNA and the start codon in the P site of the 30S ribosomal subunit. Here, we report 11 single-particle cryo-ele
  - 位置：219-439
  - 语义落点：未显示

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-11 / AVERITEC-091

样本类型：已知遗漏 / 证据不足 / 范围不明

- 状态：需要复核
- 一句话摘要：这条记录声称：Social Security beneficiaries count on the post office to get their checks
- 中文导读：先判断为需要复核；重点看缺口、挑战、范围和证据充分性。
- 风险原因：存在已知遗漏或证据缺口，不能直接行动。；适用范围或证据充分性不清，需要复核。
- 锚点状态：可回源
- 处理建议：打开 full audit；完成复核前不要作为行动依据
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/AVERITEC-091.md）
  - 记录入口：打开记录（句柄：records/AVERITEC-091.json）
  - 证据入口：打开证据（句柄：evidence/AVERITEC-091.md）
  - 原文片段：Social Security is paid via paper cheques and direct deposits. 557,840 63,668,789
  - 位置：189-270
  - 语义落点：未显示

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-12 / AMBIFC-091

样本类型：已知遗漏 / 证据不足 / 范围不明

- 状态：需要复核
- 一句话摘要：这条记录声称：there is a series 9 of vampire diaries
- 中文导读：先判断为需要复核；重点看缺口、挑战、范围和证据充分性。
- 风险原因：存在已知遗漏或证据缺口，不能直接行动。；适用范围或证据充分性不清，需要复核。
- 锚点状态：可回源
- 处理建议：打开 full audit；完成复核前不要作为行动依据
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/AMBIFC-091.md）
  - 记录入口：打开记录（句柄：records/AMBIFC-091.json）
  - 证据入口：打开证据（句柄：evidence/AMBIFC-091.md）
  - 原文片段：The series is set in the fictional town of Mystic Falls, Virginia, a town charged with supernatural history since its settlement of migrants from New England in the late 18th century. It follows the life of Elena Gilbert
  - 位置：147-367
  - 语义落点：未显示

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-13 / FULLANCHOR-001

样本类型：完整锚点回源

- 状态：普通记录
- 一句话摘要：这条记录声称：Hunter Biden had no experience in Ukraine or in the energy sector when he joined the board of Burisma.
- 中文导读：先轻量保存；只有进入行动依据或出现硬触发时才打开 full audit。
- 风险原因：普通稳定记录，无硬触发；保持轻量即可。
- 锚点状态：可回源
- 处理建议：轻量保存；如需行动依据，请打开完整审计包
- 回源入口：
  - 来源入口：打开来源（句柄：real_source_snapshots/FULLANCHOR-001.txt）
  - 记录入口：打开记录（句柄：records/FULLANCHOR-001.json）
  - 证据入口：打开证据（句柄：evidence/FULLANCHOR-001.md）
  - 原文片段：Pam Bondi, former Florida attorney general turned impeachment lawyer "A corrupt Ukrainian oligarch put Hunter on the board of his gas company, even though he had no experience in Ukraine — or in the energy sector.
  - 位置：8770-8983
  - 语义落点：claim 相关上下文落点，弱；需要人审确认是否是证据段
- 定向边界提醒：
  - 当前只是 claim 相关上下文落点，不等于证据段落落点；行动前需要 full audit。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-14 / FULLANCHOR-002

样本类型：完整锚点回源

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称：Donald Trump delivered the largest tax cuts in American history.
- 中文导读：先判断为不可行动并打开 full audit；英文 claim 只作原文内容，不替代复核。
- 风险原因：涉及行动依据，必须打开 full audit。
- 锚点状态：可回源
- 处理建议：打开 full audit；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：real_source_snapshots/FULLANCHOR-002.txt）
  - 记录入口：打开记录（句柄：records/FULLANCHOR-002.json）
  - 证据入口：打开证据（句柄：evidence/FULLANCHOR-002.md）
  - 原文片段：Several bills since 1980 were larger than the 2017 tax bill , measured not only by contemporary dollars but also by inflation-adjusted dollars and as a percentage of gross domestic product, which is a measure of the size of the overall economy.
  - 位置：8357-8601
  - 语义落点：claim 相关上下文落点，弱；需要人审确认是否是证据段
- 定向边界提醒：
  - 当前只是 claim 相关上下文落点，不等于证据段落落点；行动前需要 full audit。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-15 / SCIFACT-131

样本类型：已解决 / 重复形态

- 状态：已解决，默认折叠，可回看
- 一句话摘要：这条记录声称：Hypocretin neurones induce panicprone state in rats.
- 中文导读：先判断为默认折叠且可回看；若出现新冲突或回归必须重开。
- 风险原因：已解决项可折叠，但必须可回看；回归时必须重开。
- 锚点状态：可回源
- 处理建议：默认折叠，可回看；如回归则重新进入队列
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/SCIFACT-131.md）
  - 记录入口：打开记录（句柄：records/SCIFACT-131.json）
  - 证据入口：打开证据（句柄：evidence/SCIFACT-131.md）
  - 原文片段：Panic disorder is a severe anxiety disorder with recurrent, debilitating panic attacks. In individuals with panic disorder there is evidence of decreased central gamma-aminobutyric acid (GABA) activity as well as marked
  - 位置：164-384
  - 语义落点：未显示
- 定向边界提醒：
  - 重复数 / group count 只代表路由压缩，不代表支持更强。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-16 / AVERITEC-131

样本类型：已解决 / 重复形态

- 状态：已解决，默认折叠，可回看
- 一句话摘要：这条记录声称：Amazon CEO Jeff Bezos has offered free one-day Prime shipping for all mail-in ballots.
- 中文导读：先判断为默认折叠且可回看；若出现新冲突或回归必须重开。
- 风险原因：已解决项可折叠，但必须可回看；回归时必须重开。
- 锚点状态：可回源
- 处理建议：默认折叠，可回看；如回归则重新进入队列
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/AVERITEC-131.md）
  - 记录入口：打开记录（句柄：records/AVERITEC-131.json）
  - 证据入口：打开证据（句柄：evidence/AVERITEC-131.md）
  - 原文片段：No
  - 位置：201-203
  - 语义落点：未显示
- 定向边界提醒：
  - 重复数 / group count 只代表路由压缩，不代表支持更强。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-17 / SCIFACT-151

样本类型：authority 误读诱饵

- 状态：普通记录
- 一句话摘要：这条记录声称：Incidence rates of cervical cancer have increased due to nationwide screening programs based primarily on cytology to detect uterine cervical cancer.
- 中文导读：先当普通路由样本处理，但要特别防止把 count、lineage、test 或 dashboard 误读成证据。
- 风险原因：包含容易被误读成 authority 的表述，需要边界提醒。
- 锚点状态：可回源
- 处理建议：轻量保存；保留边界提醒；不要把诊断、计数或 lint 当证据；作为行动依据时再打开 full audit
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/SCIFACT-151.md）
  - 记录入口：打开记录（句柄：records/SCIFACT-151.json）
  - 证据入口：打开证据（句柄：evidence/SCIFACT-151.md）
  - 原文片段：With respect to cervical cancer management, Finland and the Netherlands are comparable in relevant characteristics, e.g., fertility rate, age-of-mother at first birth and a national screening programme for several years.
  - 位置：261-481
  - 语义落点：未显示
- 定向边界提醒：
  - dashboard、test、LLM summary 或 lint 只能作诊断，不能当事实证据。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-18 / AVERITEC-151

样本类型：authority 误读诱饵

- 状态：普通记录
- 一句话摘要：这条记录声称：The U.S. Health and Human Services Secretary Alex Azar's visit to Taiwan in August 2020 is a breach of international rules.
- 中文导读：先当普通路由样本处理，但要特别防止把 count、lineage、test 或 dashboard 误读成证据。
- 风险原因：包含容易被误读成 authority 的表述，需要边界提醒。
- 锚点状态：可回源
- 处理建议：轻量保存；保留边界提醒；不要把诊断、计数或 lint 当证据；作为行动依据时再打开 full audit
- 回源入口：
  - 来源入口：打开来源（句柄：raw_sources/AVERITEC-151.md）
  - 记录入口：打开记录（句柄：records/AVERITEC-151.json）
  - 证据入口：打开证据（句柄：evidence/AVERITEC-151.md）
  - 原文片段：There is no “international rule” banning high-ranking U.S. officials from visiting Taiwan. While countries have been careful to engage in diplomacy with Taiwan, this restraint has been assumed to be out of courtesy for C
  - 位置：238-458
  - 语义落点：未显示
- 定向边界提醒：
  - dashboard、test、LLM summary 或 lint 只能作诊断，不能当事实证据。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-19 / HOLDOUT-045

样本类型：过度归并近失误

- 状态：普通记录
- 一句话摘要：这条记录声称：Basophils counteract disease development in patients with systemic lupus erythematosus (SLE).
- 中文导读：先当普通路由样本处理，但要特别防止把 count、lineage、test 或 dashboard 误读成证据。
- 风险原因：存在过度归并近失误，只能作为路由提示，不能当支持强度。
- 锚点状态：可回源
- 处理建议：轻量保存；仅保留归并边界提醒；不要把 group count 当支持强度；作为行动依据时再打开 full audit
- 回源入口：
  - 来源入口：打开来源（句柄：full_anchor_sources/HOLDOUT-045.md）
  - 记录入口：打开记录（句柄：records/HOLDOUT-045.json）
  - 证据入口：打开证据（句柄：evidence/HOLDOUT-045.md）
  - 原文片段：In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activation of basophils by autoreactive IgE ca
  - 位置：205-425
  - 语义落点：未显示
- 定向边界提醒：
  - 重复数 / group count 只代表路由压缩，不代表支持更强。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-20 / HOLDOUT-046

样本类型：过度归并近失误

- 状态：普通记录
- 一句话摘要：这条记录声称：Birth-weight is positively associated with breast cancer.
- 中文导读：先当普通路由样本处理，但要特别防止把 count、lineage、test 或 dashboard 误读成证据。
- 风险原因：存在过度归并近失误，只能作为路由提示，不能当支持强度。
- 锚点状态：可回源
- 处理建议：轻量保存；仅保留归并边界提醒；不要把 group count 当支持强度；作为行动依据时再打开 full audit
- 回源入口：
  - 来源入口：打开来源（句柄：full_anchor_sources/HOLDOUT-046.md）
  - 记录入口：打开记录（句柄：records/HOLDOUT-046.json）
  - 证据入口：打开证据（句柄：evidence/HOLDOUT-046.md）
  - 原文片段：BACKGROUND Birth size, perhaps a proxy for prenatal environment, might be a correlate of subsequent breast cancer risk, but findings from epidemiological studies have been inconsistent. We re-analysed individual particip
  - 位置：169-389
  - 语义落点：未显示
- 定向边界提醒：
  - 重复数 / group count 只代表路由压缩，不代表支持更强。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-21 / HOLDOUT-029

样本类型：回源跳转失败风险

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称：Articles published in open access format are less likely to be cited than traditional journals.
- 中文导读：先判断为暂不可行动；本轮重点是识别锚点缺失并要求补锚点。
- 风险原因：锚点缺失，不能直接回源，需要先处理回源问题。；回源跳转可能失败，需要确认 source-first drilldown。
- 锚点状态：锚点缺失，不能直接回源
- 处理建议：补锚点；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：full_anchor_sources/HOLDOUT-029.md）
  - 记录入口：打开记录（句柄：records/HOLDOUT-029.json）
  - 证据入口：打开证据（句柄：evidence/HOLDOUT-029.md）
  - 原文片段：PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized a
  - 位置：-1--1
  - 语义落点：未显示
- 定向边界提醒：
  - 有 provenance 不等于有可用 support；锚点异常时不能作为行动依据。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-22 / HOLDOUT-030

样本类型：回源跳转失败风险

- 状态：需要复核
- 一句话摘要：这条记录声称：Articles published in open access format are more likely to be cited than traditional journals.
- 中文导读：先判断为需要重新定位来源；不要因为有路径就算回源成功。
- 风险原因：锚点可能过期，需要复核来源版本，需要先处理回源问题。；回源跳转可能失败，需要确认 source-first drilldown。
- 锚点状态：锚点可能过期，需要复核来源版本
- 处理建议：重新定位来源；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：full_anchor_sources/HOLDOUT-030.md）
  - 记录入口：打开记录（句柄：records/HOLDOUT-030.json）
  - 证据入口：打开证据（句柄：evidence/HOLDOUT-030.md）
  - 原文片段：PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized a
  - 位置：-1--1
  - 语义落点：未显示
- 定向边界提醒：
  - 有 provenance 不等于有可用 support；锚点异常时不能作为行动依据。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-23 / HOLDOUT-073

样本类型：严重项折叠 / 回归陷阱

- 状态：已回归，重新进入队列
- 一句话摘要：这条记录声称：Cold exposure reduces BAT recruitment.
- 中文导读：先判断为回归重开；不能被 resolved 或 recurrence 折叠吞掉。
- 风险原因：已回归，必须重新进入队列。；严重项不能被折叠，必须保持可见。
- 锚点状态：可回源
- 处理建议：打开 full audit；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：full_anchor_sources/HOLDOUT-073.md）
  - 记录入口：打开记录（句柄：records/HOLDOUT-073.json）
  - 证据入口：打开证据（句柄：evidence/HOLDOUT-073.md）
  - 原文片段：Molecular mechanisms underlying the cold-associated high cardiovascular risk remain unknown. Here, we show that the cold-triggered food-intake-independent lipolysis significantly increased plasma levels of small low-dens
  - 位置：150-370
  - 语义落点：未显示

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---

## RISK-UX-24 / HOLDOUT-074

样本类型：严重项折叠 / 回归陷阱

- 状态：阻塞，暂不可作为行动依据
- 一句话摘要：这条记录声称：Combination nicotine replacement therapies with varenicline or bupropion lead to significantly higher long-term abstinence rates at 52 weeks than varenicline monotherapy.
- 中文导读：先判断为暂不可行动；本轮重点是识别锚点缺失并要求补锚点。
- 风险原因：锚点缺失，不能直接回源，需要先处理回源问题。；严重项不能被折叠，必须保持可见。
- 锚点状态：锚点缺失，不能直接回源
- 处理建议：补锚点；暂不可行动
- 回源入口：
  - 来源入口：打开来源（句柄：full_anchor_sources/HOLDOUT-074.md）
  - 记录入口：打开记录（句柄：records/HOLDOUT-074.json）
  - 证据入口：打开证据（句柄：evidence/HOLDOUT-074.md）
  - 原文片段：IMPORTANCE Combining pharmacotherapies for tobacco-dependence treatment may increase smoking abstinence. OBJECTIVE To determine efficacy and safety of varenicline and bupropion sustained-release (SR; combination therapy)
  - 位置：-1--1
  - 语义落点：未显示
- 定向边界提醒：
  - 有 provenance 不等于有可用 support；锚点异常时不能作为行动依据。

请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。

---
