# Quick Side Recurrence Review: shell_core vs shell_core_plus_recurrence

先不要看 `hidden_variant_map.csv`，做完这一轮再看。
每个 assignment 先读 View A，再读 View B。用对应的 blank sheet 记录粗略耗时、是否会打开 full audit、有没有漏 serious 风险、click-back 是否顺、哪一版更轻、主观负担。

## QUICK-SIDE-001 / SCIFACT-139

Layer: `resolved_repeated_recurrence` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-139
state: ordinary
summary: Immune complex triggered cell death leads to extracellular release of neutrophil protein HMGB1.
anchor_health: valid source=raw_sources/SCIFACT-139.md
open_gap: resolved_repeated_recurrence
why: light metadata stub ; feedback: categorical no truth change
pointer_triad: source_path=raw_sources/SCIFACT-139.md source_hash=0c50b035b28c39918a7ea94fe0747bfa5e7aece0cc5c949cc90c709f733397dc source_version=dataset-v1 selector=text_quote+char_offset start=207 end=427 record_path=records/SCIFACT-139.json evidence_path=evidence/SCIFACT-139.md evidence_marker=EVIDENCE_SCIFACT-139_ANCHOR quote="Neutrophil extracellular traps (NETs) are implicated in autoimmunity, but how they are generated and their roles in sterile inflammation remain unclear. Ribonucleoprotein immune complexes (RNP ICs), inducers of NETosis, "
```

### View B

```text
case: SCIFACT-139
state: ordinary
summary: Immune complex triggered cell death leads to extracellular release of neutrophil protein HMGB1.
anchor_health: valid source=raw_sources/SCIFACT-139.md
open_gap: resolved_repeated_recurrence
why: light metadata stub ; recurrence: triage count=2 ; feedback: categorical no truth change
pointer_triad: source_path=raw_sources/SCIFACT-139.md source_hash=0c50b035b28c39918a7ea94fe0747bfa5e7aece0cc5c949cc90c709f733397dc source_version=dataset-v1 selector=text_quote+char_offset start=207 end=427 record_path=records/SCIFACT-139.json evidence_path=evidence/SCIFACT-139.md evidence_marker=EVIDENCE_SCIFACT-139_ANCHOR quote="Neutrophil extracellular traps (NETs) are implicated in autoimmunity, but how they are generated and their roles in sterile inflammation remain unclear. Ribonucleoprotein immune complexes (RNP ICs), inducers of NETosis, "
group_id: fp-v1|rec-5b69d5befd|scope_fit_note|scope_fit|minor_repeat|valid
```

## QUICK-SIDE-002 / SCIFACT-140

Layer: `resolved_repeated_recurrence` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-140
state: ordinary
summary: folded member exemplar=SCIFACT-139 count=2
anchor_health: valid source=raw_sources/SCIFACT-140.md
open_gap: recurrence triage only no truth change no support strength
why: light because open ordinary valid-anchor recurrence
pointer_triad: source_path=raw_sources/SCIFACT-140.md source_hash=1dc93e60f51115cbcee5fd2537bc47ef26be798a184c6539fb591282943e17b2 source_version=dataset-v1 selector=text_quote+char_offset start=211 end=431 record_path=records/SCIFACT-140.json evidence_path=evidence/SCIFACT-140.md evidence_marker=EVIDENCE_SCIFACT-140_ANCHOR quote="Mice lacking junctional adhesion molecule A (JAM-A, encoded by F11r) exhibit enhanced intestinal epithelial permeability, bacterial translocation, and elevated colonic lymphocyte numbers, yet do not develop colitis. To i"
group_id: fp-v1|rec-5b69d5befd|scope_fit_note|scope_fit|minor_repeat|valid
```

### View B

```text
case: SCIFACT-140
state: ordinary
summary: Immune responses result in the development of inflammatory Th17 cells and anti-inflammatory iTregs.
anchor_health: valid source=raw_sources/SCIFACT-140.md
open_gap: resolved_repeated_recurrence
why: light metadata stub ; feedback: categorical no truth change
pointer_triad: source_path=raw_sources/SCIFACT-140.md source_hash=1dc93e60f51115cbcee5fd2537bc47ef26be798a184c6539fb591282943e17b2 source_version=dataset-v1 selector=text_quote+char_offset start=211 end=431 record_path=records/SCIFACT-140.json evidence_path=evidence/SCIFACT-140.md evidence_marker=EVIDENCE_SCIFACT-140_ANCHOR quote="Mice lacking junctional adhesion molecule A (JAM-A, encoded by F11r) exhibit enhanced intestinal epithelial permeability, bacterial translocation, and elevated colonic lymphocyte numbers, yet do not develop colitis. To i"
```

## QUICK-SIDE-003 / SCIFACT-141

Layer: `resolved_repeated_recurrence` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-141
state: ordinary
summary: In adult tissue, most T cells are memory T cells.
anchor_health: valid source=raw_sources/SCIFACT-141.md
open_gap: resolved_repeated_recurrence
why: light metadata stub ; feedback: categorical no truth change
pointer_triad: source_path=raw_sources/SCIFACT-141.md source_hash=0a57a44d3f2742adb2ac87d607710208d517b5aa1ae6df0109c00a0d15581935 source_version=dataset-v1 selector=text_quote+char_offset start=161 end=381 record_path=records/SCIFACT-141.json evidence_path=evidence/SCIFACT-141.md evidence_marker=EVIDENCE_SCIFACT-141_ANCHOR quote="It is unclear how the immune response in early life becomes appropriately stimulated to provide protection while also avoiding excessive activation as a result of diverse new antigens. T cells are integral to adaptive im"
```

### View B

```text
case: SCIFACT-141
state: ordinary
summary: In adult tissue, most T cells are memory T cells.
anchor_health: valid source=raw_sources/SCIFACT-141.md
open_gap: resolved_repeated_recurrence
why: light metadata stub ; recurrence: triage count=10 ; feedback: categorical no truth change
pointer_triad: source_path=raw_sources/SCIFACT-141.md source_hash=0a57a44d3f2742adb2ac87d607710208d517b5aa1ae6df0109c00a0d15581935 source_version=dataset-v1 selector=text_quote+char_offset start=161 end=381 record_path=records/SCIFACT-141.json evidence_path=evidence/SCIFACT-141.md evidence_marker=EVIDENCE_SCIFACT-141_ANCHOR quote="It is unclear how the immune response in early life becomes appropriately stimulated to provide protection while also avoiding excessive activation as a result of diverse new antigens. T cells are integral to adaptive im"
group_id: fp-v2|rec-fc00dc7b5b|scope_fit_note|scope_fit|minor_repeat|valid
```

## QUICK-SIDE-004 / SCIFACT-142

Layer: `resolved_repeated_recurrence` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-142
state: ordinary
summary: folded member exemplar=SCIFACT-141 count=10
anchor_health: valid source=raw_sources/SCIFACT-142.md
open_gap: recurrence triage only no truth change no support strength
why: light because open ordinary valid-anchor recurrence
pointer_triad: source_path=raw_sources/SCIFACT-142.md source_hash=519875bf7ca924c9f783252366d332efb892dbbab2ed1e3fcbc3db47e2c30be3 source_version=dataset-v1 selector=text_quote+char_offset start=214 end=434 record_path=records/SCIFACT-142.json evidence_path=evidence/SCIFACT-142.md evidence_marker=EVIDENCE_SCIFACT-142_ANCHOR quote="Whereas domestication of livestock, pets, and crops is well documented, it is still unclear to what extent microbes associated with the production of food have also undergone human selection and where the plethora of ind"
group_id: fp-v2|rec-fc00dc7b5b|scope_fit_note|scope_fit|minor_repeat|valid
```

### View B

```text
case: SCIFACT-142
state: ordinary
summary: In domesticated populations of Saccharomyces cerevisiae, whole chromosome aneuploidy is very unco...
anchor_health: valid source=raw_sources/SCIFACT-142.md
open_gap: resolved_repeated_recurrence
why: light metadata stub ; feedback: categorical no truth change
pointer_triad: source_path=raw_sources/SCIFACT-142.md source_hash=519875bf7ca924c9f783252366d332efb892dbbab2ed1e3fcbc3db47e2c30be3 source_version=dataset-v1 selector=text_quote+char_offset start=214 end=434 record_path=records/SCIFACT-142.json evidence_path=evidence/SCIFACT-142.md evidence_marker=EVIDENCE_SCIFACT-142_ANCHOR quote="Whereas domestication of livestock, pets, and crops is well documented, it is still unclear to what extent microbes associated with the production of food have also undergone human selection and where the plethora of ind"
```

## QUICK-SIDE-005 / SCIFACT-143

Layer: `resolved_repeated_recurrence` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-143
state: ordinary
summary: In mice, P. chabaudi parasites are able to proliferate faster early in infection when inoculated ...
anchor_health: valid source=raw_sources/SCIFACT-143.md
open_gap: resolved_repeated_recurrence
why: light metadata stub ; feedback: categorical no truth change
pointer_triad: source_path=raw_sources/SCIFACT-143.md source_hash=f4cc6a329d16e2612a7f45843979cb89e56db426e5ae018a84965f6c57cdcfb2 source_version=dataset-v1 selector=text_quote+char_offset start=263 end=483 record_path=records/SCIFACT-143.json evidence_path=evidence/SCIFACT-143.md evidence_marker=EVIDENCE_SCIFACT-143_ANCHOR quote="Immune clearance and resource limitation (via red blood cell depletion) shape the peaks and troughs of malaria parasitemia, which in turn affect disease severity and transmission. Quantitatively partitioning the relative"
```

### View B

```text
case: SCIFACT-143
state: ordinary
summary: folded member exemplar=SCIFACT-141 count=10
anchor_health: valid source=raw_sources/SCIFACT-143.md
open_gap: recurrence triage only no truth change no support strength
why: light because open ordinary valid-anchor recurrence
pointer_triad: source_path=raw_sources/SCIFACT-143.md source_hash=f4cc6a329d16e2612a7f45843979cb89e56db426e5ae018a84965f6c57cdcfb2 source_version=dataset-v1 selector=text_quote+char_offset start=263 end=483 record_path=records/SCIFACT-143.json evidence_path=evidence/SCIFACT-143.md evidence_marker=EVIDENCE_SCIFACT-143_ANCHOR quote="Immune clearance and resource limitation (via red blood cell depletion) shape the peaks and troughs of malaria parasitemia, which in turn affect disease severity and transmission. Quantitatively partitioning the relative"
group_id: fp-v2|rec-fc00dc7b5b|scope_fit_note|scope_fit|minor_repeat|valid
```

## QUICK-SIDE-006 / HOLDOUT-045

Layer: `over_grouping_near_miss` | Anchor status: `valid` | Pool: `adversarial_holdout`

### View A

```text
case: HOLDOUT-045
state: ordinary
summary: Basophils counteract disease development in patients with systemic lupus erythematosus (SLE).
anchor_health: valid source=full_anchor_sources/HOLDOUT-045.md
open_gap: over_grouping_near_miss
why: light metadata stub ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-045.md source_hash=06e1a5c81f074719e5c0567377c7820f074aab9f18de58c00a539d76c8f72f07 source_version=holdout-v1 selector=text_quote+char_offset start=205 end=425 record_path=records/HOLDOUT-045.json evidence_path=evidence/HOLDOUT-045.md evidence_marker=EVIDENCE_HOLDOUT-045_ANCHOR quote="In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activation of basophils by autoreactive IgE ca"
```

### View B

```text
case: HOLDOUT-045
state: ordinary
summary: Basophils counteract disease development in patients with systemic lupus erythematosus (SLE).
anchor_health: valid source=full_anchor_sources/HOLDOUT-045.md
open_gap: over_grouping_near_miss
why: light metadata stub ; recurrence: triage count=1 ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-045.md source_hash=06e1a5c81f074719e5c0567377c7820f074aab9f18de58c00a539d76c8f72f07 source_version=holdout-v1 selector=text_quote+char_offset start=205 end=425 record_path=records/HOLDOUT-045.json evidence_path=evidence/HOLDOUT-045.md evidence_marker=EVIDENCE_HOLDOUT-045_ANCHOR quote="In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activation of basophils by autoreactive IgE ca"
group_id: fp-v1|holdout-near-0|scope_fit_note|scope_fit|minor_repeat|valid
```

## QUICK-SIDE-007 / HOLDOUT-046

Layer: `over_grouping_near_miss` | Anchor status: `valid` | Pool: `adversarial_holdout`

### View A

```text
case: HOLDOUT-046
state: ordinary
summary: Birth-weight is positively associated with breast cancer.
anchor_health: valid source=full_anchor_sources/HOLDOUT-046.md
open_gap: over_grouping_near_miss
why: light metadata stub ; recurrence: triage count=1 ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-046.md source_hash=6ce0d4eb16740b6d4ddc9de96bb4aaf61955719f6f509c7e703341d15d4acd3c source_version=holdout-v1 selector=text_quote+char_offset start=169 end=389 record_path=records/HOLDOUT-046.json evidence_path=evidence/HOLDOUT-046.md evidence_marker=EVIDENCE_HOLDOUT-046_ANCHOR quote="BACKGROUND Birth size, perhaps a proxy for prenatal environment, might be a correlate of subsequent breast cancer risk, but findings from epidemiological studies have been inconsistent. We re-analysed individual particip"
group_id: fp-v1|holdout-near-0|action_basis_note|scope_fit|minor_repeat|valid
```

### View B

```text
case: HOLDOUT-046
state: ordinary
summary: Birth-weight is positively associated with breast cancer.
anchor_health: valid source=full_anchor_sources/HOLDOUT-046.md
open_gap: over_grouping_near_miss
why: light metadata stub ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-046.md source_hash=6ce0d4eb16740b6d4ddc9de96bb4aaf61955719f6f509c7e703341d15d4acd3c source_version=holdout-v1 selector=text_quote+char_offset start=169 end=389 record_path=records/HOLDOUT-046.json evidence_path=evidence/HOLDOUT-046.md evidence_marker=EVIDENCE_HOLDOUT-046_ANCHOR quote="BACKGROUND Birth size, perhaps a proxy for prenatal environment, might be a correlate of subsequent breast cancer risk, but findings from epidemiological studies have been inconsistent. We re-analysed individual particip"
```

## QUICK-SIDE-008 / HOLDOUT-047

Layer: `over_grouping_near_miss` | Anchor status: `valid` | Pool: `adversarial_holdout`

### View A

```text
case: HOLDOUT-047
state: ordinary
summary: Birth-weight is positively associated with breast cancer.
anchor_health: valid source=full_anchor_sources/HOLDOUT-047.md
open_gap: over_grouping_near_miss
why: light metadata stub ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-047.md source_hash=a7a6bb38d63efaf7f35b3864bf03af21265dbaed2c2026d17c30d6da1a0265da source_version=holdout-v1 selector=text_quote+char_offset start=169 end=389 record_path=records/HOLDOUT-047.json evidence_path=evidence/HOLDOUT-047.md evidence_marker=EVIDENCE_HOLDOUT-047_ANCHOR quote="Breast cancer may originate in utero. We reviewed the available evidence on the association between birthweight and the risk of breast cancer. To date, 26 research papers addressing this issue have been published. The ma"
```

### View B

```text
case: HOLDOUT-047
state: ordinary
summary: Birth-weight is positively associated with breast cancer.
anchor_health: valid source=full_anchor_sources/HOLDOUT-047.md
open_gap: over_grouping_near_miss
why: light metadata stub ; recurrence: triage count=1 ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-047.md source_hash=a7a6bb38d63efaf7f35b3864bf03af21265dbaed2c2026d17c30d6da1a0265da source_version=holdout-v1 selector=text_quote+char_offset start=169 end=389 record_path=records/HOLDOUT-047.json evidence_path=evidence/HOLDOUT-047.md evidence_marker=EVIDENCE_HOLDOUT-047_ANCHOR quote="Breast cancer may originate in utero. We reviewed the available evidence on the association between birthweight and the risk of breast cancer. To date, 26 research papers addressing this issue have been published. The ma"
group_id: fp-v1|holdout-near-0|scope_fit_note|scope_fit|conflict_neighbor|valid
```

## QUICK-SIDE-009 / HOLDOUT-073

Layer: `serious_folded_violation` | Anchor status: `valid` | Pool: `adversarial_holdout`

### View A

```text
case: HOLDOUT-073
state: regressed
summary: Cold exposure reduces BAT recruitment.
anchor_health: valid source=full_anchor_sources/HOLDOUT-073.md
open_gap: regression
why: thickened by hard trigger or anchor problem ; review_due: true ; queue: unresolved_gate ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-073.md source_hash=59ac41c10e6c838a3da5c9a2dfd3ea439519014fbbc6dedb4bec64fff37f5c9a source_version=holdout-v1 selector=text_quote+char_offset start=150 end=370 record_path=records/HOLDOUT-073.json evidence_path=evidence/HOLDOUT-073.md evidence_marker=EVIDENCE_HOLDOUT-073_ANCHOR quote="Molecular mechanisms underlying the cold-associated high cardiovascular risk remain unknown. Here, we show that the cold-triggered food-intake-independent lipolysis significantly increased plasma levels of small low-dens"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: regression
source_anchor: status=valid path=full_anchor_sources/HOLDOUT-073.md hash=59ac41c10e6c838a3da5c9a2dfd3ea439519014fbbc6dedb4bec64fff37f5c9a start=150 end=370 quote="Molecular mechanisms underlying the cold-associated high cardiovascular risk remain unknown. Here, we show that the cold-triggered food-intake-independent lipolysis significantly increased plasma levels of small low-dens"
evidence_excerpt: Molecular mechanisms underlying the cold-associated high cardiovascular risk remain unknown. Here, we show that the cold-triggered food-intake-independent lipolysis significantly increased plasma levels of small low-density lipoprotein (LDL) remnants, leading to accelerated development of atherosclerotic lesions in mice. In two genetic mouse knockout models (apolipoprotein E(-/-) [ApoE(-/-)] and LDL receptor(-/-) [Ldlr(-/-)] mice), persistent cold exposure stimulated atherosclerotic plaque growth by increasing lipid deposition. Furthermore, marked increase of inflammatory cells and plaque-associated microvessels were detected in the cold-acclimated ApoE(-/-) and Ldlr(-/-) mice, leading to...
```

### View B

```text
case: HOLDOUT-073
state: regressed
summary: Cold exposure reduces BAT recruitment.
anchor_health: valid source=full_anchor_sources/HOLDOUT-073.md
open_gap: regression
why: thickened by hard trigger or anchor problem ; review_due: true ; queue: unresolved_gate ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-073.md source_hash=59ac41c10e6c838a3da5c9a2dfd3ea439519014fbbc6dedb4bec64fff37f5c9a source_version=holdout-v1 selector=text_quote+char_offset start=150 end=370 record_path=records/HOLDOUT-073.json evidence_path=evidence/HOLDOUT-073.md evidence_marker=EVIDENCE_HOLDOUT-073_ANCHOR quote="Molecular mechanisms underlying the cold-associated high cardiovascular risk remain unknown. Here, we show that the cold-triggered food-intake-independent lipolysis significantly increased plasma levels of small low-dens"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: regression
source_anchor: status=valid path=full_anchor_sources/HOLDOUT-073.md hash=59ac41c10e6c838a3da5c9a2dfd3ea439519014fbbc6dedb4bec64fff37f5c9a start=150 end=370 quote="Molecular mechanisms underlying the cold-associated high cardiovascular risk remain unknown. Here, we show that the cold-triggered food-intake-independent lipolysis significantly increased plasma levels of small low-dens"
evidence_excerpt: Molecular mechanisms underlying the cold-associated high cardiovascular risk remain unknown. Here, we show that the cold-triggered food-intake-independent lipolysis significantly increased plasma levels of small low-density lipoprotein (LDL) remnants, leading to accelerated development of atherosclerotic lesions in mice. In two genetic mouse knockout models (apolipoprotein E(-/-) [ApoE(-/-)] and LDL receptor(-/-) [Ldlr(-/-)] mice), persistent cold exposure stimulated atherosclerotic plaque growth by increasing lipid deposition. Furthermore, marked increase of inflammatory cells and plaque-associated microvessels were detected in the cold-acclimated ApoE(-/-) and Ldlr(-/-) mice, leading to...
```

## QUICK-SIDE-010 / HOLDOUT-074

Layer: `serious_folded_violation` | Anchor status: `missing` | Pool: `adversarial_holdout`

### View A

```text
case: HOLDOUT-074
state: blocking
summary: Combination nicotine replacement therapies with varenicline or bupropion lead to significantly hi...
anchor_health: missing source=full_anchor_sources/HOLDOUT-074.md
open_gap: missing_anchor
why: thickened by hard trigger or anchor problem ; anchor_problem_visibility: missing ; review_due: true ; queue: unresolved_gate ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-074.md source_hash= source_version=holdout-v1 selector=text_quote+char_offset start=-1 end=-1 record_path=records/HOLDOUT-074.json evidence_path=evidence/HOLDOUT-074.md evidence_marker=EVIDENCE_HOLDOUT-074_ANCHOR quote="IMPORTANCE Combining pharmacotherapies for tobacco-dependence treatment may increase smoking abstinence. OBJECTIVE To determine efficacy and safety of varenicline and bupropion sustained-release (SR; combination therapy)"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: missing_anchor
source_anchor: status=missing path=full_anchor_sources/HOLDOUT-074.md hash= start=-1 end=-1 quote="IMPORTANCE Combining pharmacotherapies for tobacco-dependence treatment may increase smoking abstinence. OBJECTIVE To determine efficacy and safety of varenicline and bupropion sustained-release (SR; combination therapy)"
evidence_excerpt: IMPORTANCE Combining pharmacotherapies for tobacco-dependence treatment may increase smoking abstinence. OBJECTIVE To determine efficacy and safety of varenicline and bupropion sustained-release (SR; combination therapy) compared with varenicline (monotherapy) in cigarette smokers. DESIGN, SETTING, AND PARTICIPANTS Randomized, blinded, placebo-controlled multicenter clinical trial with a 12-week treatment period and follow-up through week 52 conducted between October 2009 and April 2013 at 3 midwestern clinical research sites. Five hundred six adult (≥18 years) cigarette smokers were randomly assigned and 315 (62%) completed the study. INTERVENTIONS Twelve weeks of varenicline and bupropi...
```

### View B

```text
case: HOLDOUT-074
state: blocking
summary: Combination nicotine replacement therapies with varenicline or bupropion lead to significantly hi...
anchor_health: missing source=full_anchor_sources/HOLDOUT-074.md
open_gap: missing_anchor
why: thickened by hard trigger or anchor problem ; anchor_problem_visibility: missing ; review_due: true ; queue: unresolved_gate ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-074.md source_hash= source_version=holdout-v1 selector=text_quote+char_offset start=-1 end=-1 record_path=records/HOLDOUT-074.json evidence_path=evidence/HOLDOUT-074.md evidence_marker=EVIDENCE_HOLDOUT-074_ANCHOR quote="IMPORTANCE Combining pharmacotherapies for tobacco-dependence treatment may increase smoking abstinence. OBJECTIVE To determine efficacy and safety of varenicline and bupropion sustained-release (SR; combination therapy)"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: missing_anchor
source_anchor: status=missing path=full_anchor_sources/HOLDOUT-074.md hash= start=-1 end=-1 quote="IMPORTANCE Combining pharmacotherapies for tobacco-dependence treatment may increase smoking abstinence. OBJECTIVE To determine efficacy and safety of varenicline and bupropion sustained-release (SR; combination therapy)"
evidence_excerpt: IMPORTANCE Combining pharmacotherapies for tobacco-dependence treatment may increase smoking abstinence. OBJECTIVE To determine efficacy and safety of varenicline and bupropion sustained-release (SR; combination therapy) compared with varenicline (monotherapy) in cigarette smokers. DESIGN, SETTING, AND PARTICIPANTS Randomized, blinded, placebo-controlled multicenter clinical trial with a 12-week treatment period and follow-up through week 52 conducted between October 2009 and April 2013 at 3 midwestern clinical research sites. Five hundred six adult (≥18 years) cigarette smokers were randomly assigned and 315 (62%) completed the study. INTERVENTIONS Twelve weeks of varenicline and bupropi...
```
