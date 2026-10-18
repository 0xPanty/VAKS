# Quick Main Core Review: baseline_full vs shell_core

先不要看 `hidden_variant_map.csv`，做完这一轮再看。
每个 assignment 先读 View A，再读 View B。用对应的 blank sheet 记录粗略耗时、是否会打开 full audit、有没有漏 serious 风险、click-back 是否顺、哪一版更轻、主观负担。

## QUICK-MAIN-001 / SCIFACT-001

Layer: `ordinary_stable` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-001
state: ordinary
summary: 0-dimensional biomaterials show inductive properties.
anchor_health: valid source=raw_sources/SCIFACT-001.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-001.md hash=c0cd541e64e3acf4a92b0d10210ab1486e9823ee3205ba73be6601377abe754e version=dataset-v1 selector=text_quote+char_offset start=165 end=385 quote="Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells. Examples include magnetic nanoparticles and quantum dots for stem cell labeling and in vivo tracking;"
record_pointer: path=records/SCIFACT-001.json
evidence_pointer: path=evidence/SCIFACT-001.md marker=EVIDENCE_SCIFACT-001_ANCHOR
source_label: qrel:1
evidence_excerpt: Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells. Examples include magnetic nanoparticles and quantum dots for stem cell labeling and in vivo tracking; nanoparticles, carbon nanotubes, and polyplexes for the intracellular delivery of genes/oligonucleotides and protein/peptides; and engineered nanometer-scale scaffolds for stem cell differentiation and transplantation. This review examines the use of nanotechnologies for stem cell tracking, diff...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: none
source_anchor: status=valid path=raw_sources/SCIFACT-001.md hash=c0cd541e64e3acf4a92b0d10210ab1486e9823ee3205ba73be6601377abe754e start=165 end=385 quote="Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells. Examples include magnetic nanoparticles and quantum dots for stem cell labeling and in vivo tracking;"
evidence_excerpt: Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells. Examples include magnetic nanoparticles and quantum dots for stem cell labeling and in vivo tracking; nanoparticles, carbon nanotubes, and polyplexes for the intracellular delivery of genes/oligonucleotides and protein/peptides; and engineered nanometer-scale scaffolds for stem cell differentiation and transplantation. This review examines the use of nanotechnologies for stem cell tracking, differentiation, and transplantation. We further discuss their utility and the potential concerns regarding their cytotoxicity.
```

### View B

```text
case: SCIFACT-001
state: ordinary
summary: 0-dimensional biomaterials show inductive properties.
anchor_health: valid source=raw_sources/SCIFACT-001.md
open_gap: ordinary_stable
why: light metadata stub
pointer_triad: source_path=raw_sources/SCIFACT-001.md source_hash=c0cd541e64e3acf4a92b0d10210ab1486e9823ee3205ba73be6601377abe754e source_version=dataset-v1 selector=text_quote+char_offset start=165 end=385 record_path=records/SCIFACT-001.json evidence_path=evidence/SCIFACT-001.md evidence_marker=EVIDENCE_SCIFACT-001_ANCHOR quote="Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells. Examples include magnetic nanoparticles and quantum dots for stem cell labeling and in vivo tracking;"
```

## QUICK-MAIN-002 / SCIFACT-002

Layer: `ordinary_stable` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-002
state: ordinary
summary: 1,000 genomes project enables mapping of genetic sequence variation consisting of rare variants w...
anchor_health: valid source=raw_sources/SCIFACT-002.md
open_gap: ordinary_stable
why: light metadata stub
pointer_triad: source_path=raw_sources/SCIFACT-002.md source_hash=6735bcf186bc4baaa7f9af10021654896e58f1633cdac910e09e2b381c2440d4 source_version=dataset-v1 selector=text_quote+char_offset start=260 end=480 record_path=records/SCIFACT-002.json evidence_path=evidence/SCIFACT-002.md evidence_marker=EVIDENCE_SCIFACT-002_ANCHOR quote="Genome-wide association studies (GWAS) have now identified at least 2,000 common variants that appear associated with common diseases or related traits (http://www.genome.gov/gwastudies), hundreds of which have been conv"
```

### View B

```text
case: SCIFACT-002
state: ordinary
summary: 1,000 genomes project enables mapping of genetic sequence variation consisting of rare variants with larger penetranc...
anchor_health: valid source=raw_sources/SCIFACT-002.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-002.md hash=6735bcf186bc4baaa7f9af10021654896e58f1633cdac910e09e2b381c2440d4 version=dataset-v1 selector=text_quote+char_offset start=260 end=480 quote="Genome-wide association studies (GWAS) have now identified at least 2,000 common variants that appear associated with common diseases or related traits (http://www.genome.gov/gwastudies), hundreds of which have been conv"
record_pointer: path=records/SCIFACT-002.json
evidence_pointer: path=evidence/SCIFACT-002.md marker=EVIDENCE_SCIFACT-002_ANCHOR
source_label: qrel:1
evidence_excerpt: Genome-wide association studies (GWAS) have now identified at least 2,000 common variants that appear associated with common diseases or related traits (http://www.genome.gov/gwastudies), hundreds of which have been convincingly replicated. It is generally thought that the associated markers reflect the effect of a nearby common (minor allele frequency >0.05) causal site, which is associated with the marker, leading to extensive resequencing efforts to find causal sites. We propose as an alternative explanation ...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: none
source_anchor: status=valid path=raw_sources/SCIFACT-002.md hash=6735bcf186bc4baaa7f9af10021654896e58f1633cdac910e09e2b381c2440d4 start=260 end=480 quote="Genome-wide association studies (GWAS) have now identified at least 2,000 common variants that appear associated with common diseases or related traits (http://www.genome.gov/gwastudies), hundreds of which have been conv"
evidence_excerpt: Genome-wide association studies (GWAS) have now identified at least 2,000 common variants that appear associated with common diseases or related traits (http://www.genome.gov/gwastudies), hundreds of which have been convincingly replicated. It is generally thought that the associated markers reflect the effect of a nearby common (minor allele frequency >0.05) causal site, which is associated with the marker, leading to extensive resequencing efforts to find causal sites. We propose as an alternative explanation that variants much less common than the associated one may create "synthetic associations" by occurring, stochastically, more often in association with one of the alleles at the co...
```

## QUICK-MAIN-003 / SCIFACT-003

Layer: `ordinary_stable` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-003
state: ordinary
summary: 1/2000 in UK have abnormal PrP positivity.
anchor_health: valid source=raw_sources/SCIFACT-003.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-003.md hash=3d14d826c6a9216a50774d744b97d77cce44f2b68cd3f4e2b71b7d63112ce4be version=dataset-v1 selector=text_quote+char_offset start=154 end=374 quote="OBJECTIVES To carry out a further survey of archived appendix samples to understand better the differences between existing estimates of the prevalence of subclinical infection with prions after the bovine spongiform enc"
record_pointer: path=records/SCIFACT-003.json
evidence_pointer: path=evidence/SCIFACT-003.md marker=EVIDENCE_SCIFACT-003_ANCHOR
source_label: qrel:1
evidence_excerpt: OBJECTIVES To carry out a further survey of archived appendix samples to understand better the differences between existing estimates of the prevalence of subclinical infection with prions after the bovine spongiform encephalopathy epizootic and to see whether a broader birth cohort was affected, and to understand better the implications for the management of blood and blood products and for the handling of surgical instruments. DESIGN Irreversibly unlinked and anonymised large scale survey of archived appendix ...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: none
source_anchor: status=valid path=raw_sources/SCIFACT-003.md hash=3d14d826c6a9216a50774d744b97d77cce44f2b68cd3f4e2b71b7d63112ce4be start=154 end=374 quote="OBJECTIVES To carry out a further survey of archived appendix samples to understand better the differences between existing estimates of the prevalence of subclinical infection with prions after the bovine spongiform enc"
evidence_excerpt: OBJECTIVES To carry out a further survey of archived appendix samples to understand better the differences between existing estimates of the prevalence of subclinical infection with prions after the bovine spongiform encephalopathy epizootic and to see whether a broader birth cohort was affected, and to understand better the implications for the management of blood and blood products and for the handling of surgical instruments. DESIGN Irreversibly unlinked and anonymised large scale survey of archived appendix samples. SETTING Archived appendix samples from the pathology departments of 41 UK hospitals participating in the earlier survey, and additional hospitals in regions with lower lev...
```

### View B

```text
case: SCIFACT-003
state: ordinary
summary: 1/2000 in UK have abnormal PrP positivity.
anchor_health: valid source=raw_sources/SCIFACT-003.md
open_gap: ordinary_stable
why: light metadata stub
pointer_triad: source_path=raw_sources/SCIFACT-003.md source_hash=3d14d826c6a9216a50774d744b97d77cce44f2b68cd3f4e2b71b7d63112ce4be source_version=dataset-v1 selector=text_quote+char_offset start=154 end=374 record_path=records/SCIFACT-003.json evidence_path=evidence/SCIFACT-003.md evidence_marker=EVIDENCE_SCIFACT-003_ANCHOR quote="OBJECTIVES To carry out a further survey of archived appendix samples to understand better the differences between existing estimates of the prevalence of subclinical infection with prions after the bovine spongiform enc"
```

## QUICK-MAIN-004 / SCIFACT-004

Layer: `ordinary_stable` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-004
state: ordinary
summary: 5% of perinatal mortality is due to low birth weight.
anchor_health: valid source=raw_sources/SCIFACT-004.md
open_gap: ordinary_stable
why: light metadata stub
pointer_triad: source_path=raw_sources/SCIFACT-004.md source_hash=0e7990d0073c733ca9da8ccbee75a3e81f89ce2cd74bad7658664b4e5aaee00c source_version=dataset-v1 selector=text_quote+char_offset start=165 end=385 record_path=records/SCIFACT-004.json evidence_path=evidence/SCIFACT-004.md evidence_marker=EVIDENCE_SCIFACT-004_ANCHOR quote="CONTEXT One key target of the United Nations Millennium Development goals is to reduce the prevalence of underweight among children younger than 5 years by half between 1990 and 2015. OBJECTIVE To estimate trends in chil"
```

### View B

```text
case: SCIFACT-004
state: ordinary
summary: 5% of perinatal mortality is due to low birth weight.
anchor_health: valid source=raw_sources/SCIFACT-004.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-004.md hash=0e7990d0073c733ca9da8ccbee75a3e81f89ce2cd74bad7658664b4e5aaee00c version=dataset-v1 selector=text_quote+char_offset start=165 end=385 quote="CONTEXT One key target of the United Nations Millennium Development goals is to reduce the prevalence of underweight among children younger than 5 years by half between 1990 and 2015. OBJECTIVE To estimate trends in chil"
record_pointer: path=records/SCIFACT-004.json
evidence_pointer: path=evidence/SCIFACT-004.md marker=EVIDENCE_SCIFACT-004_ANCHOR
source_label: qrel:1
evidence_excerpt: CONTEXT One key target of the United Nations Millennium Development goals is to reduce the prevalence of underweight among children younger than 5 years by half between 1990 and 2015. OBJECTIVE To estimate trends in childhood underweight by geographic regions of the world. DESIGN, SETTING, AND PARTICIPANTS Time series study of prevalence of underweight, defined as weight 2 SDs below the mean weight for age of the National Center for Health Statistics and World Health Organization (WHO) reference population. Nati...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: none
source_anchor: status=valid path=raw_sources/SCIFACT-004.md hash=0e7990d0073c733ca9da8ccbee75a3e81f89ce2cd74bad7658664b4e5aaee00c start=165 end=385 quote="CONTEXT One key target of the United Nations Millennium Development goals is to reduce the prevalence of underweight among children younger than 5 years by half between 1990 and 2015. OBJECTIVE To estimate trends in chil"
evidence_excerpt: CONTEXT One key target of the United Nations Millennium Development goals is to reduce the prevalence of underweight among children younger than 5 years by half between 1990 and 2015. OBJECTIVE To estimate trends in childhood underweight by geographic regions of the world. DESIGN, SETTING, AND PARTICIPANTS Time series study of prevalence of underweight, defined as weight 2 SDs below the mean weight for age of the National Center for Health Statistics and World Health Organization (WHO) reference population. National prevalence rates derived from the WHO Global Database on Child Growth and Malnutrition, which includes data on approximately 31 million children younger than 5 years who parti...
```

## QUICK-MAIN-005 / SCIFACT-061

Layer: `action_challenge_conflict` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-061
state: blocking
summary: Carriers of the alcohol aldehyde dehydrogenase deficiency mutation drink less that non-carries.
anchor_health: valid source=raw_sources/SCIFACT-061.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-061.md hash=95df712b5955895b55d68ae8460a45f2dc74fe100df66d3c6fd6062f7fbc04b8 version=dataset-v1 selector=text_quote+char_offset start=207 end=427 quote="BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension. However, observational studies are subject to confounding by other behavioural and sociodemographic factors, while clinical"
record_pointer: path=records/SCIFACT-061.json
evidence_pointer: path=evidence/SCIFACT-061.md marker=EVIDENCE_SCIFACT-061_ANCHOR
source_label: qrel:1
evidence_excerpt: BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension. However, observational studies are subject to confounding by other behavioural and sociodemographic factors, while clinical trials are difficult to implement and have limited follow-up time. Mendelian randomization can provide robust evidence on the nature of this association by use of a common polymorphism in aldehyde dehydrogenase 2 (ALDH2) as a surrogate for measuring alcohol consumption. ALDH2 encodes a major enz...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: action_basis
source_anchor: status=valid path=raw_sources/SCIFACT-061.md hash=95df712b5955895b55d68ae8460a45f2dc74fe100df66d3c6fd6062f7fbc04b8 start=207 end=427 quote="BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension. However, observational studies are subject to confounding by other behavioural and sociodemographic factors, while clinical"
evidence_excerpt: BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension. However, observational studies are subject to confounding by other behavioural and sociodemographic factors, while clinical trials are difficult to implement and have limited follow-up time. Mendelian randomization can provide robust evidence on the nature of this association by use of a common polymorphism in aldehyde dehydrogenase 2 (ALDH2) as a surrogate for measuring alcohol consumption. ALDH2 encodes a major enzyme involved in alcohol metabolism. Individuals homozygous for the null variant (*2*2) experience adverse symptoms when drinking alcohol and consequently drink considerably less al...
```

### View B

```text
case: SCIFACT-061
state: blocking
summary: Carriers of the alcohol aldehyde dehydrogenase deficiency mutation drink less that non-carries.
anchor_health: valid source=raw_sources/SCIFACT-061.md
open_gap: action_basis
why: thickened by hard trigger or anchor problem ; review_due: true ; queue: unresolved_gate
pointer_triad: source_path=raw_sources/SCIFACT-061.md source_hash=95df712b5955895b55d68ae8460a45f2dc74fe100df66d3c6fd6062f7fbc04b8 source_version=dataset-v1 selector=text_quote+char_offset start=207 end=427 record_path=records/SCIFACT-061.json evidence_path=evidence/SCIFACT-061.md evidence_marker=EVIDENCE_SCIFACT-061_ANCHOR quote="BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension. However, observational studies are subject to confounding by other behavioural and sociodemographic factors, while clinical"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: action_basis
source_anchor: status=valid path=raw_sources/SCIFACT-061.md hash=95df712b5955895b55d68ae8460a45f2dc74fe100df66d3c6fd6062f7fbc04b8 start=207 end=427 quote="BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension. However, observational studies are subject to confounding by other behavioural and sociodemographic factors, while clinical"
evidence_excerpt: BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension. However, observational studies are subject to confounding by other behavioural and sociodemographic factors, while clinical trials are difficult to implement and have limited follow-up time. Mendelian randomization can provide robust evidence on the nature of this association by use of a common polymorphism in aldehyde dehydrogenase 2 (ALDH2) as a surrogate for measuring alcohol consumption. ALDH2 encodes a major enzyme involved in alcohol metabolism. Individuals homozygous for the null variant (*2*2) experience adverse symptoms when drinking alcohol and consequently drink considerably less al...
```

## QUICK-MAIN-006 / SCIFACT-062

Layer: `action_challenge_conflict` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-062
state: blocking
summary: Cataract and trachoma are the primary cause of blindness in Southern Sudan.
anchor_health: valid source=raw_sources/SCIFACT-062.md
open_gap: explicit_challenge
why: thickened by hard trigger or anchor problem ; review_due: true ; queue: unresolved_gate
pointer_triad: source_path=raw_sources/SCIFACT-062.md source_hash=a0c08fa7e712409a24d37dc6874781d29822324fdb4492e2da6d818a5465a982 source_version=dataset-v1 selector=text_quote+char_offset start=187 end=407 record_path=records/SCIFACT-062.json evidence_path=evidence/SCIFACT-062.md evidence_marker=EVIDENCE_SCIFACT-062_ANCHOR quote="Background Blindness and low vision are thought to be common in southern Sudan. However, the magnitude and geographical distribution are largely unknown. We aimed to estimate the prevalence of blindness and low vision, i"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: explicit_challenge
source_anchor: status=valid path=raw_sources/SCIFACT-062.md hash=a0c08fa7e712409a24d37dc6874781d29822324fdb4492e2da6d818a5465a982 start=187 end=407 quote="Background Blindness and low vision are thought to be common in southern Sudan. However, the magnitude and geographical distribution are largely unknown. We aimed to estimate the prevalence of blindness and low vision, i"
evidence_excerpt: Background Blindness and low vision are thought to be common in southern Sudan. However, the magnitude and geographical distribution are largely unknown. We aimed to estimate the prevalence of blindness and low vision, identify the main causes of blindness and low vision, and estimate targets for blindness prevention programs in Mankien payam (district), southern Sudan.
```

### View B

```text
case: SCIFACT-062
state: blocking
summary: Cataract and trachoma are the primary cause of blindness in Southern Sudan.
anchor_health: valid source=raw_sources/SCIFACT-062.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-062.md hash=a0c08fa7e712409a24d37dc6874781d29822324fdb4492e2da6d818a5465a982 version=dataset-v1 selector=text_quote+char_offset start=187 end=407 quote="Background Blindness and low vision are thought to be common in southern Sudan. However, the magnitude and geographical distribution are largely unknown. We aimed to estimate the prevalence of blindness and low vision, i"
record_pointer: path=records/SCIFACT-062.json
evidence_pointer: path=evidence/SCIFACT-062.md marker=EVIDENCE_SCIFACT-062_ANCHOR
source_label: qrel:1
evidence_excerpt: Background Blindness and low vision are thought to be common in southern Sudan. However, the magnitude and geographical distribution are largely unknown. We aimed to estimate the prevalence of blindness and low vision, identify the main causes of blindness and low vision, and estimate targets for blindness prevention programs in Mankien payam (district), southern Sudan.
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: explicit_challenge
source_anchor: status=valid path=raw_sources/SCIFACT-062.md hash=a0c08fa7e712409a24d37dc6874781d29822324fdb4492e2da6d818a5465a982 start=187 end=407 quote="Background Blindness and low vision are thought to be common in southern Sudan. However, the magnitude and geographical distribution are largely unknown. We aimed to estimate the prevalence of blindness and low vision, i"
evidence_excerpt: Background Blindness and low vision are thought to be common in southern Sudan. However, the magnitude and geographical distribution are largely unknown. We aimed to estimate the prevalence of blindness and low vision, identify the main causes of blindness and low vision, and estimate targets for blindness prevention programs in Mankien payam (district), southern Sudan.
```

## QUICK-MAIN-007 / SCIFACT-063

Layer: `action_challenge_conflict` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-063
state: blocking
summary: Cell autonomous sex determination in somatic cells does not occur in Galliformes.
anchor_health: valid source=raw_sources/SCIFACT-063.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-063.md hash=1e17964ee23f2cf95015f0c47dc9656e7b5de705d7ea9ddc8522ba9d3e7375e7 version=dataset-v1 selector=text_quote+char_offset start=193 end=413 quote="In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to app"
record_pointer: path=records/SCIFACT-063.json
evidence_pointer: path=evidence/SCIFACT-063.md marker=EVIDENCE_SCIFACT-063_ANCHOR
source_label: qrel:1
evidence_excerpt: In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to apply to all vertebrates, this has yet to be established. Here we have examined three lateral gynandromorph chickens (a rare, naturally occurring phenomenon in which one side of the animal appears male and the other female) to investigate the sex-determining mechanism in birds. These studies demonst...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: conflict
source_anchor: status=valid path=raw_sources/SCIFACT-063.md hash=1e17964ee23f2cf95015f0c47dc9656e7b5de705d7ea9ddc8522ba9d3e7375e7 start=193 end=413 quote="In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to app"
evidence_excerpt: In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to apply to all vertebrates, this has yet to be established. Here we have examined three lateral gynandromorph chickens (a rare, naturally occurring phenomenon in which one side of the animal appears male and the other female) to investigate the sex-determining mechanism in birds. These studies demonstrated that gynandromorph birds are genuine male:female chimaeras, and indicated that male and female avian somatic cells may have an inherent sex identity. To test this hypothesis,...
```

### View B

```text
case: SCIFACT-063
state: blocking
summary: Cell autonomous sex determination in somatic cells does not occur in Galliformes.
anchor_health: valid source=raw_sources/SCIFACT-063.md
open_gap: conflict
why: thickened by hard trigger or anchor problem ; review_due: true ; queue: unresolved_gate
pointer_triad: source_path=raw_sources/SCIFACT-063.md source_hash=1e17964ee23f2cf95015f0c47dc9656e7b5de705d7ea9ddc8522ba9d3e7375e7 source_version=dataset-v1 selector=text_quote+char_offset start=193 end=413 record_path=records/SCIFACT-063.json evidence_path=evidence/SCIFACT-063.md evidence_marker=EVIDENCE_SCIFACT-063_ANCHOR quote="In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to app"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: conflict
source_anchor: status=valid path=raw_sources/SCIFACT-063.md hash=1e17964ee23f2cf95015f0c47dc9656e7b5de705d7ea9ddc8522ba9d3e7375e7 start=193 end=413 quote="In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to app"
evidence_excerpt: In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to apply to all vertebrates, this has yet to be established. Here we have examined three lateral gynandromorph chickens (a rare, naturally occurring phenomenon in which one side of the animal appears male and the other female) to investigate the sex-determining mechanism in birds. These studies demonstrated that gynandromorph birds are genuine male:female chimaeras, and indicated that male and female avian somatic cells may have an inherent sex identity. To test this hypothesis,...
```

## QUICK-MAIN-008 / SCIFACT-064

Layer: `action_challenge_conflict` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-064
state: blocking
summary: Cell autonomous sex determination in somatic cells occurs in Passeriformes.
anchor_health: valid source=raw_sources/SCIFACT-064.md
open_gap: action_basis
why: thickened by hard trigger or anchor problem ; review_due: true ; queue: unresolved_gate
pointer_triad: source_path=raw_sources/SCIFACT-064.md source_hash=89c96bd23c9fc887590a6e270d53f161b1b2afadfdf956b474ded92e17832417 source_version=dataset-v1 selector=text_quote+char_offset start=187 end=407 record_path=records/SCIFACT-064.json evidence_path=evidence/SCIFACT-064.md evidence_marker=EVIDENCE_SCIFACT-064_ANCHOR quote="In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to app"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: action_basis
source_anchor: status=valid path=raw_sources/SCIFACT-064.md hash=89c96bd23c9fc887590a6e270d53f161b1b2afadfdf956b474ded92e17832417 start=187 end=407 quote="In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to app"
evidence_excerpt: In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to apply to all vertebrates, this has yet to be established. Here we have examined three lateral gynandromorph chickens (a rare, naturally occurring phenomenon in which one side of the animal appears male and the other female) to investigate the sex-determining mechanism in birds. These studies demonstrated that gynandromorph birds are genuine male:female chimaeras, and indicated that male and female avian somatic cells may have an inherent sex identity. To test this hypothesis,...
```

### View B

```text
case: SCIFACT-064
state: blocking
summary: Cell autonomous sex determination in somatic cells occurs in Passeriformes.
anchor_health: valid source=raw_sources/SCIFACT-064.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-064.md hash=89c96bd23c9fc887590a6e270d53f161b1b2afadfdf956b474ded92e17832417 version=dataset-v1 selector=text_quote+char_offset start=187 end=407 quote="In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to app"
record_pointer: path=records/SCIFACT-064.json
evidence_pointer: path=evidence/SCIFACT-064.md marker=EVIDENCE_SCIFACT-064_ANCHOR
source_label: qrel:1
evidence_excerpt: In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to apply to all vertebrates, this has yet to be established. Here we have examined three lateral gynandromorph chickens (a rare, naturally occurring phenomenon in which one side of the animal appears male and the other female) to investigate the sex-determining mechanism in birds. These studies demonst...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: action_basis
source_anchor: status=valid path=raw_sources/SCIFACT-064.md hash=89c96bd23c9fc887590a6e270d53f161b1b2afadfdf956b474ded92e17832417 start=187 end=407 quote="In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to app"
evidence_excerpt: In the mammalian model of sex determination, embryos are considered to be sexually indifferent until the transient action of a sex-determining gene initiates gonadal differentiation. Although this model is thought to apply to all vertebrates, this has yet to be established. Here we have examined three lateral gynandromorph chickens (a rare, naturally occurring phenomenon in which one side of the animal appears male and the other female) to investigate the sex-determining mechanism in birds. These studies demonstrated that gynandromorph birds are genuine male:female chimaeras, and indicated that male and female avian somatic cells may have an inherent sex identity. To test this hypothesis,...
```

## QUICK-MAIN-009 / SCIFACT-116

Layer: `anchor_problem` | Anchor status: `missing` | Pool: `main_public`

### View A

```text
case: SCIFACT-116
state: blocking
summary: Headaches are not correlated with cognitive impairment.
anchor_health: missing source=raw_sources/SCIFACT-116.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-116.md hash= version=dataset-v1 selector=text_quote+char_offset start=-1 end=-1 quote="OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities, brain infarcts, and cognition. DESIGN Population based, cross sectional study. SETTING Epidemiology of"
record_pointer: path=records/SCIFACT-116.json
evidence_pointer: path=evidence/SCIFACT-116.md marker=EVIDENCE_SCIFACT-116_ANCHOR
source_label: qrel:1
evidence_excerpt: OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities, brain infarcts, and cognition. DESIGN Population based, cross sectional study. SETTING Epidemiology of Vascular Ageing study, Nantes, France. PARTICIPANTS 780 participants (mean age 69, 58.5% women) with detailed headache assessment. MAIN OUTCOME MEASURES Brain scans were evaluated for volume of white matter hyperintensities (by fully automated imaging processing) and for classification of infarc...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: missing_anchor
source_anchor: status=missing path=raw_sources/SCIFACT-116.md hash= start=-1 end=-1 quote="OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities, brain infarcts, and cognition. DESIGN Population based, cross sectional study. SETTING Epidemiology of"
evidence_excerpt: OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities, brain infarcts, and cognition. DESIGN Population based, cross sectional study. SETTING Epidemiology of Vascular Ageing study, Nantes, France. PARTICIPANTS 780 participants (mean age 69, 58.5% women) with detailed headache assessment. MAIN OUTCOME MEASURES Brain scans were evaluated for volume of white matter hyperintensities (by fully automated imaging processing) and for classification of infarcts (by visual reading with a standardised assessment grid). Cognitive function was assessed by a battery of tests including the mini-mental state examination. RESULTS 163 (20.9%) p...
```

### View B

```text
case: SCIFACT-116
state: blocking
summary: Headaches are not correlated with cognitive impairment.
anchor_health: missing source=raw_sources/SCIFACT-116.md
open_gap: missing_anchor
why: thickened by hard trigger or anchor problem ; anchor_problem_visibility: missing ; review_due: true ; queue: unresolved_gate
pointer_triad: source_path=raw_sources/SCIFACT-116.md source_hash= source_version=dataset-v1 selector=text_quote+char_offset start=-1 end=-1 record_path=records/SCIFACT-116.json evidence_path=evidence/SCIFACT-116.md evidence_marker=EVIDENCE_SCIFACT-116_ANCHOR quote="OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities, brain infarcts, and cognition. DESIGN Population based, cross sectional study. SETTING Epidemiology of"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: missing_anchor
source_anchor: status=missing path=raw_sources/SCIFACT-116.md hash= start=-1 end=-1 quote="OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities, brain infarcts, and cognition. DESIGN Population based, cross sectional study. SETTING Epidemiology of"
evidence_excerpt: OBJECTIVE To evaluate the association of overall and specific headaches with volume of white matter hyperintensities, brain infarcts, and cognition. DESIGN Population based, cross sectional study. SETTING Epidemiology of Vascular Ageing study, Nantes, France. PARTICIPANTS 780 participants (mean age 69, 58.5% women) with detailed headache assessment. MAIN OUTCOME MEASURES Brain scans were evaluated for volume of white matter hyperintensities (by fully automated imaging processing) and for classification of infarcts (by visual reading with a standardised assessment grid). Cognitive function was assessed by a battery of tests including the mini-mental state examination. RESULTS 163 (20.9%) p...
```

## QUICK-MAIN-010 / SCIFACT-117

Layer: `anchor_problem` | Anchor status: `stale` | Pool: `main_public`

### View A

```text
case: SCIFACT-117
state: for_review
summary: Healthcare delivery efficiency in crowded delivery centers is impaired by improving structural, l...
anchor_health: stale source=raw_sources/SCIFACT-117.md
open_gap: stale_pointer
why: thickened by hard trigger or anchor problem ; anchor_problem_visibility: stale ; review_due: true ; queue: unresolved_gate
pointer_triad: source_path=raw_sources/SCIFACT-117.md source_hash=e78b671b03f196455088d086a947dff3e46fa7d1fabb20d9734fda115cef0f66 source_version=dataset-v1 selector=text_quote+char_offset start=-1 end=-1 record_path=records/SCIFACT-117.json evidence_path=evidence/SCIFACT-117.md evidence_marker=EVIDENCE_SCIFACT-117_ANCHOR quote="BACKGROUND The World Health Organization (WHO) released revised guidelines in 2015 recommending that all people living with HIV, regardless of CD4 count, initiate antiretroviral therapy (ART) upon diagnosis. However, few"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: stale_pointer
source_anchor: status=stale path=raw_sources/SCIFACT-117.md hash=e78b671b03f196455088d086a947dff3e46fa7d1fabb20d9734fda115cef0f66 start=-1 end=-1 quote="BACKGROUND The World Health Organization (WHO) released revised guidelines in 2015 recommending that all people living with HIV, regardless of CD4 count, initiate antiretroviral therapy (ART) upon diagnosis. However, few"
evidence_excerpt: BACKGROUND The World Health Organization (WHO) released revised guidelines in 2015 recommending that all people living with HIV, regardless of CD4 count, initiate antiretroviral therapy (ART) upon diagnosis. However, few studies have projected the global resources needed for rapid scale-up of ART. Under the Health Policy Project, we conducted modeling analyses for 97 countries to estimate eligibility for and numbers on ART from 2015 to 2020, along with the facility-level financial resources required. We compared the estimated financial requirements to estimated funding available. METHODS AND FINDINGS Current coverage levels and future need for treatment were based on country-specific epid...
```

### View B

```text
case: SCIFACT-117
state: for_review
summary: Healthcare delivery efficiency in crowded delivery centers is impaired by improving structural, logistical, and inter...
anchor_health: stale source=raw_sources/SCIFACT-117.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-117.md hash=e78b671b03f196455088d086a947dff3e46fa7d1fabb20d9734fda115cef0f66 version=dataset-v1 selector=text_quote+char_offset start=-1 end=-1 quote="BACKGROUND The World Health Organization (WHO) released revised guidelines in 2015 recommending that all people living with HIV, regardless of CD4 count, initiate antiretroviral therapy (ART) upon diagnosis. However, few"
record_pointer: path=records/SCIFACT-117.json
evidence_pointer: path=evidence/SCIFACT-117.md marker=EVIDENCE_SCIFACT-117_ANCHOR
source_label: qrel:1
evidence_excerpt: BACKGROUND The World Health Organization (WHO) released revised guidelines in 2015 recommending that all people living with HIV, regardless of CD4 count, initiate antiretroviral therapy (ART) upon diagnosis. However, few studies have projected the global resources needed for rapid scale-up of ART. Under the Health Policy Project, we conducted modeling analyses for 97 countries to estimate eligibility for and numbers on ART from 2015 to 2020, along with the facility-level financial resources required. We compared...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: stale_pointer
source_anchor: status=stale path=raw_sources/SCIFACT-117.md hash=e78b671b03f196455088d086a947dff3e46fa7d1fabb20d9734fda115cef0f66 start=-1 end=-1 quote="BACKGROUND The World Health Organization (WHO) released revised guidelines in 2015 recommending that all people living with HIV, regardless of CD4 count, initiate antiretroviral therapy (ART) upon diagnosis. However, few"
evidence_excerpt: BACKGROUND The World Health Organization (WHO) released revised guidelines in 2015 recommending that all people living with HIV, regardless of CD4 count, initiate antiretroviral therapy (ART) upon diagnosis. However, few studies have projected the global resources needed for rapid scale-up of ART. Under the Health Policy Project, we conducted modeling analyses for 97 countries to estimate eligibility for and numbers on ART from 2015 to 2020, along with the facility-level financial resources required. We compared the estimated financial requirements to estimated funding available. METHODS AND FINDINGS Current coverage levels and future need for treatment were based on country-specific epid...
```

## QUICK-MAIN-011 / SCIFACT-118

Layer: `anchor_problem` | Anchor status: `drift` | Pool: `main_public`

### View A

```text
case: SCIFACT-118
state: for_review
summary: Helminths interfere with immune system control of macrophages activated by IL-4 favor Mycobacterium tuberculosis repl...
anchor_health: drift source=raw_sources/SCIFACT-118.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-118.md hash=dcc79c9bf47e5d304097abc820ff72a768309a2689f0c7c5eafb0e459bc750da version=dataset-v1 selector=text_quote+char_offset start=244 end=464 quote="Autophagy is a recently recognized immune effector mechanism against intracellular pathogens. The role of autophagy in innate immunity has been well established, but the extent of its regulation by the adaptive immune re"
record_pointer: path=records/SCIFACT-118.json
evidence_pointer: path=evidence/SCIFACT-118.md marker=EVIDENCE_SCIFACT-118_ANCHOR
source_label: qrel:1
evidence_excerpt: Autophagy is a recently recognized immune effector mechanism against intracellular pathogens. The role of autophagy in innate immunity has been well established, but the extent of its regulation by the adaptive immune response is less well understood. The T helper 1 (Th1) cell cytokine IFN-gamma induces autophagy in macrophages to eliminate Mycobacterium tuberculosis. Here, we report that Th2 cytokines affect autophagy in macrophages and their ability to control intracellular M. tuberculosis. IL-4 and IL-13 abro...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: selector_drift
source_anchor: status=drift path=raw_sources/SCIFACT-118.md hash=dcc79c9bf47e5d304097abc820ff72a768309a2689f0c7c5eafb0e459bc750da start=244 end=464 quote="Autophagy is a recently recognized immune effector mechanism against intracellular pathogens. The role of autophagy in innate immunity has been well established, but the extent of its regulation by the adaptive immune re"
evidence_excerpt: Autophagy is a recently recognized immune effector mechanism against intracellular pathogens. The role of autophagy in innate immunity has been well established, but the extent of its regulation by the adaptive immune response is less well understood. The T helper 1 (Th1) cell cytokine IFN-gamma induces autophagy in macrophages to eliminate Mycobacterium tuberculosis. Here, we report that Th2 cytokines affect autophagy in macrophages and their ability to control intracellular M. tuberculosis. IL-4 and IL-13 abrogated autophagy and autophagy-mediated killing of intracellular mycobacteria in murine and human macrophages. Inhibition of starvation-induced autophagy by IL-4 and IL-13 was depen...
```

### View B

```text
case: SCIFACT-118
state: for_review
summary: Helminths interfere with immune system control of macrophages activated by IL-4 favor Mycobacteri...
anchor_health: drift source=raw_sources/SCIFACT-118.md
open_gap: selector_drift
why: thickened by hard trigger or anchor problem ; anchor_problem_visibility: drift ; review_due: true ; queue: unresolved_gate
pointer_triad: source_path=raw_sources/SCIFACT-118.md source_hash=dcc79c9bf47e5d304097abc820ff72a768309a2689f0c7c5eafb0e459bc750da source_version=dataset-v1 selector=text_quote+char_offset start=244 end=464 record_path=records/SCIFACT-118.json evidence_path=evidence/SCIFACT-118.md evidence_marker=EVIDENCE_SCIFACT-118_ANCHOR quote="Autophagy is a recently recognized immune effector mechanism against intracellular pathogens. The role of autophagy in innate immunity has been well established, but the extent of its regulation by the adaptive immune re"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: selector_drift
source_anchor: status=drift path=raw_sources/SCIFACT-118.md hash=dcc79c9bf47e5d304097abc820ff72a768309a2689f0c7c5eafb0e459bc750da start=244 end=464 quote="Autophagy is a recently recognized immune effector mechanism against intracellular pathogens. The role of autophagy in innate immunity has been well established, but the extent of its regulation by the adaptive immune re"
evidence_excerpt: Autophagy is a recently recognized immune effector mechanism against intracellular pathogens. The role of autophagy in innate immunity has been well established, but the extent of its regulation by the adaptive immune response is less well understood. The T helper 1 (Th1) cell cytokine IFN-gamma induces autophagy in macrophages to eliminate Mycobacterium tuberculosis. Here, we report that Th2 cytokines affect autophagy in macrophages and their ability to control intracellular M. tuberculosis. IL-4 and IL-13 abrogated autophagy and autophagy-mediated killing of intracellular mycobacteria in murine and human macrophages. Inhibition of starvation-induced autophagy by IL-4 and IL-13 was depen...
```

## QUICK-MAIN-012 / HOLDOUT-029

Layer: `anchor_jumpback_failure` | Anchor status: `missing` | Pool: `adversarial_holdout`

### View A

```text
case: HOLDOUT-029
state: blocking
summary: Articles published in open access format are less likely to be cited than traditional journals.
anchor_health: missing source=full_anchor_sources/HOLDOUT-029.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=full_anchor_sources/HOLDOUT-029.md hash= version=holdout-v1 selector=text_quote+char_offset start=-1 end=-1 quote="PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized a"
record_pointer: path=records/HOLDOUT-029.json
evidence_pointer: path=evidence/HOLDOUT-029.md marker=EVIDENCE_HOLDOUT-029_ANCHOR
source_label: qrel:1
evidence_excerpt: PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized and cited than non-OA articles. As such, it adds objective support to the belief we have always held that open-access publication speeds up scientific dialog between researchers and, consequently, should be extended to the whole scientific literature as quickly as possible. It is therefore fitting...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: missing_anchor
source_anchor: status=missing path=full_anchor_sources/HOLDOUT-029.md hash= start=-1 end=-1 quote="PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized a"
evidence_excerpt: PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized and cited than non-OA articles. As such, it adds objective support to the belief we have always held that open-access publication speeds up scientific dialog between researchers and, consequently, should be extended to the whole scientific literature as quickly as possible. It is therefore fitting that we publish such a paper. We have long argued that papers freely available in a journal will be more often read and cited than those behind a subscription barrier. However, so...
```

### View B

```text
case: HOLDOUT-029
state: blocking
summary: Articles published in open access format are less likely to be cited than traditional journals.
anchor_health: missing source=full_anchor_sources/HOLDOUT-029.md
open_gap: missing_anchor
why: thickened by hard trigger or anchor problem ; anchor_problem_visibility: missing ; review_due: true ; queue: unresolved_gate
pointer_triad: source_path=full_anchor_sources/HOLDOUT-029.md source_hash= source_version=holdout-v1 selector=text_quote+char_offset start=-1 end=-1 record_path=records/HOLDOUT-029.json evidence_path=evidence/HOLDOUT-029.md evidence_marker=EVIDENCE_HOLDOUT-029_ANCHOR quote="PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized a"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: missing_anchor
source_anchor: status=missing path=full_anchor_sources/HOLDOUT-029.md hash= start=-1 end=-1 quote="PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized a"
evidence_excerpt: PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized and cited than non-OA articles. As such, it adds objective support to the belief we have always held that open-access publication speeds up scientific dialog between researchers and, consequently, should be extended to the whole scientific literature as quickly as possible. It is therefore fitting that we publish such a paper. We have long argued that papers freely available in a journal will be more often read and cited than those behind a subscription barrier. However, so...
```

## QUICK-MAIN-013 / HOLDOUT-030

Layer: `anchor_jumpback_failure` | Anchor status: `stale` | Pool: `adversarial_holdout`

### View A

```text
case: HOLDOUT-030
state: for_review
summary: Articles published in open access format are more likely to be cited than traditional journals.
anchor_health: stale source=full_anchor_sources/HOLDOUT-030.md
open_gap: stale_pointer
why: thickened by hard trigger or anchor problem ; anchor_problem_visibility: stale ; review_due: true ; queue: unresolved_gate
pointer_triad: source_path=full_anchor_sources/HOLDOUT-030.md source_hash=643a2d5a0f6527c31c83c031f150ecff8179d3f869fcfd12e78dc01e97f4a352 source_version=holdout-v1 selector=text_quote+char_offset start=-1 end=-1 record_path=records/HOLDOUT-030.json evidence_path=evidence/HOLDOUT-030.md evidence_marker=EVIDENCE_HOLDOUT-030_ANCHOR quote="PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized a"
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: stale_pointer
source_anchor: status=stale path=full_anchor_sources/HOLDOUT-030.md hash=643a2d5a0f6527c31c83c031f150ecff8179d3f869fcfd12e78dc01e97f4a352 start=-1 end=-1 quote="PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized a"
evidence_excerpt: PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized and cited than non-OA articles. As such, it adds objective support to the belief we have always held that open-access publication speeds up scientific dialog between researchers and, consequently, should be extended to the whole scientific literature as quickly as possible. It is therefore fitting that we publish such a paper. We have long argued that papers freely available in a journal will be more often read and cited than those behind a subscription barrier. However, so...
```

### View B

```text
case: HOLDOUT-030
state: for_review
summary: Articles published in open access format are more likely to be cited than traditional journals.
anchor_health: stale source=full_anchor_sources/HOLDOUT-030.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=full_anchor_sources/HOLDOUT-030.md hash=643a2d5a0f6527c31c83c031f150ecff8179d3f869fcfd12e78dc01e97f4a352 version=holdout-v1 selector=text_quote+char_offset start=-1 end=-1 quote="PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized a"
record_pointer: path=records/HOLDOUT-030.json
evidence_pointer: path=evidence/HOLDOUT-030.md marker=EVIDENCE_HOLDOUT-030_ANCHOR
source_label: qrel:1
evidence_excerpt: PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized and cited than non-OA articles. As such, it adds objective support to the belief we have always held that open-access publication speeds up scientific dialog between researchers and, consequently, should be extended to the whole scientific literature as quickly as possible. It is therefore fitting...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: stale_pointer
source_anchor: status=stale path=full_anchor_sources/HOLDOUT-030.md hash=643a2d5a0f6527c31c83c031f150ecff8179d3f869fcfd12e78dc01e97f4a352 start=-1 end=-1 quote="PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized a"
evidence_excerpt: PLoS Biology publishes today a research article by Gunther Eysenbach that is not about biology. It is about citations. It provides robust evidence that open-access articles (OA articles) are more immediately recognized and cited than non-OA articles. As such, it adds objective support to the belief we have always held that open-access publication speeds up scientific dialog between researchers and, consequently, should be extended to the whole scientific literature as quickly as possible. It is therefore fitting that we publish such a paper. We have long argued that papers freely available in a journal will be more often read and cited than those behind a subscription barrier. However, so...
```

## QUICK-MAIN-014 / SCIFACT-131

Layer: `resolved_repeated_recurrence` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-131
state: resolved_folded
summary: Hypocretin neurones induce panicprone state in rats.
anchor_health: valid source=raw_sources/SCIFACT-131.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-131.md hash=f85a121b9f1e7aaba3557fe6f7d73c41d79e889324699658f79a6f0afee7f725 version=dataset-v1 selector=text_quote+char_offset start=164 end=384 quote="Panic disorder is a severe anxiety disorder with recurrent, debilitating panic attacks. In individuals with panic disorder there is evidence of decreased central gamma-aminobutyric acid (GABA) activity as well as marked "
record_pointer: path=records/SCIFACT-131.json
evidence_pointer: path=evidence/SCIFACT-131.md marker=EVIDENCE_SCIFACT-131_ANCHOR
source_label: qrel:1
evidence_excerpt: Panic disorder is a severe anxiety disorder with recurrent, debilitating panic attacks. In individuals with panic disorder there is evidence of decreased central gamma-aminobutyric acid (GABA) activity as well as marked increases in autonomic and respiratory responses after intravenous infusions of hypertonic sodium lactate. In a rat model of panic disorder, chronic inhibition of GABA synthesis in the dorsomedial-perifornical hypothalamus of rats produces anxiety-like states and a similar vulnerability to sodium...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: none
source_anchor: status=valid path=raw_sources/SCIFACT-131.md hash=f85a121b9f1e7aaba3557fe6f7d73c41d79e889324699658f79a6f0afee7f725 start=164 end=384 quote="Panic disorder is a severe anxiety disorder with recurrent, debilitating panic attacks. In individuals with panic disorder there is evidence of decreased central gamma-aminobutyric acid (GABA) activity as well as marked "
evidence_excerpt: Panic disorder is a severe anxiety disorder with recurrent, debilitating panic attacks. In individuals with panic disorder there is evidence of decreased central gamma-aminobutyric acid (GABA) activity as well as marked increases in autonomic and respiratory responses after intravenous infusions of hypertonic sodium lactate. In a rat model of panic disorder, chronic inhibition of GABA synthesis in the dorsomedial-perifornical hypothalamus of rats produces anxiety-like states and a similar vulnerability to sodium lactate-induced cardioexcitatory responses. The dorsomedial-perifornical hypothalamus is enriched in neurons containing orexin (ORX, also known as hypocretin), which have a crucia...
```

### View B

```text
case: SCIFACT-131
state: resolved_folded
summary: Hypocretin neurones induce panicprone state in rats.
anchor_health: valid source=raw_sources/SCIFACT-131.md
open_gap: resolved_repeated_recurrence
why: resolved folded stub ; feedback: categorical no truth change
pointer_triad: source_path=raw_sources/SCIFACT-131.md source_hash=f85a121b9f1e7aaba3557fe6f7d73c41d79e889324699658f79a6f0afee7f725 source_version=dataset-v1 selector=text_quote+char_offset start=164 end=384 record_path=records/SCIFACT-131.json evidence_path=evidence/SCIFACT-131.md evidence_marker=EVIDENCE_SCIFACT-131_ANCHOR quote="Panic disorder is a severe anxiety disorder with recurrent, debilitating panic attacks. In individuals with panic disorder there is evidence of decreased central gamma-aminobutyric acid (GABA) activity as well as marked "
```

## QUICK-MAIN-015 / SCIFACT-132

Layer: `resolved_repeated_recurrence` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-132
state: resolved_folded
summary: Hypoglycemia increases the risk of dementia.
anchor_health: valid source=raw_sources/SCIFACT-132.md
open_gap: resolved_repeated_recurrence
why: resolved folded stub ; feedback: categorical no truth change
pointer_triad: source_path=raw_sources/SCIFACT-132.md source_hash=f46c574d50963c411c1466980fe1f5718accf3a5a3ce274c250c59e0d105076e source_version=dataset-v1 selector=text_quote+char_offset start=156 end=376 record_path=records/SCIFACT-132.json evidence_path=evidence/SCIFACT-132.md evidence_marker=EVIDENCE_SCIFACT-132_ANCHOR quote="CONTEXT Although acute hypoglycemia may be associated with cognitive impairment in children with type 1 diabetes, no studies to date have evaluated whether hypoglycemia is a risk factor for dementia in older patients wit"
```

### View B

```text
case: SCIFACT-132
state: resolved_folded
summary: Hypoglycemia increases the risk of dementia.
anchor_health: valid source=raw_sources/SCIFACT-132.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-132.md hash=f46c574d50963c411c1466980fe1f5718accf3a5a3ce274c250c59e0d105076e version=dataset-v1 selector=text_quote+char_offset start=156 end=376 quote="CONTEXT Although acute hypoglycemia may be associated with cognitive impairment in children with type 1 diabetes, no studies to date have evaluated whether hypoglycemia is a risk factor for dementia in older patients wit"
record_pointer: path=records/SCIFACT-132.json
evidence_pointer: path=evidence/SCIFACT-132.md marker=EVIDENCE_SCIFACT-132_ANCHOR
source_label: qrel:1
evidence_excerpt: CONTEXT Although acute hypoglycemia may be associated with cognitive impairment in children with type 1 diabetes, no studies to date have evaluated whether hypoglycemia is a risk factor for dementia in older patients with type 2 diabetes. OBJECTIVE To determine if hypoglycemic episodes severe enough to require hospitalization are associated with an increased risk of dementia in a population of older patients with type 2 diabetes followed up for 27 years. DESIGN, SETTING, AND PATIENTS A longitudinal cohort study ...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: none
source_anchor: status=valid path=raw_sources/SCIFACT-132.md hash=f46c574d50963c411c1466980fe1f5718accf3a5a3ce274c250c59e0d105076e start=156 end=376 quote="CONTEXT Although acute hypoglycemia may be associated with cognitive impairment in children with type 1 diabetes, no studies to date have evaluated whether hypoglycemia is a risk factor for dementia in older patients wit"
evidence_excerpt: CONTEXT Although acute hypoglycemia may be associated with cognitive impairment in children with type 1 diabetes, no studies to date have evaluated whether hypoglycemia is a risk factor for dementia in older patients with type 2 diabetes. OBJECTIVE To determine if hypoglycemic episodes severe enough to require hospitalization are associated with an increased risk of dementia in a population of older patients with type 2 diabetes followed up for 27 years. DESIGN, SETTING, AND PATIENTS A longitudinal cohort study from 1980-2007 of 16,667 patients with a mean age of 65 years and type 2 diabetes who are members of an integrated health care delivery system in northern California. MAIN OUTCOME ...
```

## QUICK-MAIN-016 / SCIFACT-133

Layer: `resolved_repeated_recurrence` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-133
state: resolved_folded
summary: Hypothalamic glutamate neurotransmission is crucial to energy balance.
anchor_health: valid source=raw_sources/SCIFACT-133.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-133.md hash=d82af761b45fcbff3e5fa0fb99d2591223f3f534a14d727df5dee469aa842527 version=dataset-v1 selector=text_quote+char_offset start=182 end=402 quote="The importance of neuropeptides in the hypothalamus has been experimentally established. Due to difficulties in assessing function in vivo, the roles of the fast-acting neurotransmitters glutamate and GABA are largely un"
record_pointer: path=records/SCIFACT-133.json
evidence_pointer: path=evidence/SCIFACT-133.md marker=EVIDENCE_SCIFACT-133_ANCHOR
source_label: qrel:1
evidence_excerpt: The importance of neuropeptides in the hypothalamus has been experimentally established. Due to difficulties in assessing function in vivo, the roles of the fast-acting neurotransmitters glutamate and GABA are largely unknown. Synaptic vesicular transporters (VGLUTs for glutamate and VGAT for GABA) are required for vesicular uptake and, consequently, synaptic release of neurotransmitters. Ventromedial hypothalamic (VMH) neurons are predominantly glutamatergic and express VGLUT2. To evaluate the role of glutamate...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: none
source_anchor: status=valid path=raw_sources/SCIFACT-133.md hash=d82af761b45fcbff3e5fa0fb99d2591223f3f534a14d727df5dee469aa842527 start=182 end=402 quote="The importance of neuropeptides in the hypothalamus has been experimentally established. Due to difficulties in assessing function in vivo, the roles of the fast-acting neurotransmitters glutamate and GABA are largely un"
evidence_excerpt: The importance of neuropeptides in the hypothalamus has been experimentally established. Due to difficulties in assessing function in vivo, the roles of the fast-acting neurotransmitters glutamate and GABA are largely unknown. Synaptic vesicular transporters (VGLUTs for glutamate and VGAT for GABA) are required for vesicular uptake and, consequently, synaptic release of neurotransmitters. Ventromedial hypothalamic (VMH) neurons are predominantly glutamatergic and express VGLUT2. To evaluate the role of glutamate release from VMH neurons, we generated mice lacking VGLUT2 selectively in SF1 neurons (a major subset of VMH neurons). These mice have hypoglycemia during fasting secondary to imp...
```

### View B

```text
case: SCIFACT-133
state: resolved_folded
summary: Hypothalamic glutamate neurotransmission is crucial to energy balance.
anchor_health: valid source=raw_sources/SCIFACT-133.md
open_gap: resolved_repeated_recurrence
why: resolved folded stub ; feedback: categorical no truth change
pointer_triad: source_path=raw_sources/SCIFACT-133.md source_hash=d82af761b45fcbff3e5fa0fb99d2591223f3f534a14d727df5dee469aa842527 source_version=dataset-v1 selector=text_quote+char_offset start=182 end=402 record_path=records/SCIFACT-133.json evidence_path=evidence/SCIFACT-133.md evidence_marker=EVIDENCE_SCIFACT-133_ANCHOR quote="The importance of neuropeptides in the hypothalamus has been experimentally established. Due to difficulties in assessing function in vivo, the roles of the fast-acting neurotransmitters glutamate and GABA are largely un"
```

## QUICK-MAIN-017 / SCIFACT-151

Layer: `authority_leak_bait` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-151
state: ordinary
summary: Incidence rates of cervical cancer have increased due to nationwide screening programs based primarily on cytology to...
anchor_health: valid source=raw_sources/SCIFACT-151.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-151.md hash=f046068e4ca7ead89d7c18e8f5f2007168b0cac0c139623bc3912e201c4ffaa5 version=dataset-v1 selector=text_quote+char_offset start=261 end=481 quote="With respect to cervical cancer management, Finland and the Netherlands are comparable in relevant characteristics, e.g., fertility rate, age-of-mother at first birth and a national screening programme for several years."
record_pointer: path=records/SCIFACT-151.json
evidence_pointer: path=evidence/SCIFACT-151.md marker=EVIDENCE_SCIFACT-151_ANCHOR
source_label: qrel:1
evidence_excerpt: With respect to cervical cancer management, Finland and the Netherlands are comparable in relevant characteristics, e.g., fertility rate, age-of-mother at first birth and a national screening programme for several years. The aim of this study is to compare trends in incidence of and mortality from cervical cancer in Finland and the Netherlands in relation to the introduction and intensity of the screening programmes. Therefore, incidence and mortality rates were calculated using the Cancer Registries of Finland ...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: none
source_anchor: status=valid path=raw_sources/SCIFACT-151.md hash=f046068e4ca7ead89d7c18e8f5f2007168b0cac0c139623bc3912e201c4ffaa5 start=261 end=481 quote="With respect to cervical cancer management, Finland and the Netherlands are comparable in relevant characteristics, e.g., fertility rate, age-of-mother at first birth and a national screening programme for several years."
evidence_excerpt: With respect to cervical cancer management, Finland and the Netherlands are comparable in relevant characteristics, e.g., fertility rate, age-of-mother at first birth and a national screening programme for several years. The aim of this study is to compare trends in incidence of and mortality from cervical cancer in Finland and the Netherlands in relation to the introduction and intensity of the screening programmes. Therefore, incidence and mortality rates were calculated using the Cancer Registries of Finland and the Netherlands. Data on screening intensity were obtained from the Finnish Cancer Registry and the Dutch evaluation centre at ErasmusMC-Rotterdam. Women aged 30-60 have been s...
```

### View B

```text
case: SCIFACT-151
state: ordinary
summary: Incidence rates of cervical cancer have increased due to nationwide screening programs based prim...
anchor_health: valid source=raw_sources/SCIFACT-151.md
open_gap: authority_leak_bait
authority_boundary: dashboard_as_truth is diagnostic only
pointer_triad: source_path=raw_sources/SCIFACT-151.md source_hash=f046068e4ca7ead89d7c18e8f5f2007168b0cac0c139623bc3912e201c4ffaa5 source_version=dataset-v1 selector=text_quote+char_offset start=261 end=481 record_path=records/SCIFACT-151.json evidence_path=evidence/SCIFACT-151.md evidence_marker=EVIDENCE_SCIFACT-151_ANCHOR quote="With respect to cervical cancer management, Finland and the Netherlands are comparable in relevant characteristics, e.g., fertility rate, age-of-mother at first birth and a national screening programme for several years."
```

## QUICK-MAIN-018 / SCIFACT-152

Layer: `authority_leak_bait` | Anchor status: `valid` | Pool: `main_public`

### View A

```text
case: SCIFACT-152
state: ordinary
summary: Increased microtubule acetylation repairs LRRK2 Roc-COR domain mutation induced locomotor deficits.
anchor_health: valid source=raw_sources/SCIFACT-152.md
open_gap: authority_leak_bait
authority_boundary: test_pass_as_truth is diagnostic only
pointer_triad: source_path=raw_sources/SCIFACT-152.md source_hash=81c9b11481915559b18b700b97b10bd128248225697ef8926e7b93699c4489b5 source_version=dataset-v1 selector=text_quote+char_offset start=211 end=431 record_path=records/SCIFACT-152.json evidence_path=evidence/SCIFACT-152.md evidence_marker=EVIDENCE_SCIFACT-152_ANCHOR quote="Leucine-rich repeat kinase 2 (LRRK2) mutations are the most common genetic cause of Parkinson's disease. LRRK2 is a multifunctional protein affecting many cellular processes and has been described to bind microtubules. D"
```

### View B

```text
case: SCIFACT-152
state: ordinary
summary: Increased microtubule acetylation repairs LRRK2 Roc-COR domain mutation induced locomotor deficits.
anchor_health: valid source=raw_sources/SCIFACT-152.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=raw_sources/SCIFACT-152.md hash=81c9b11481915559b18b700b97b10bd128248225697ef8926e7b93699c4489b5 version=dataset-v1 selector=text_quote+char_offset start=211 end=431 quote="Leucine-rich repeat kinase 2 (LRRK2) mutations are the most common genetic cause of Parkinson's disease. LRRK2 is a multifunctional protein affecting many cellular processes and has been described to bind microtubules. D"
record_pointer: path=records/SCIFACT-152.json
evidence_pointer: path=evidence/SCIFACT-152.md marker=EVIDENCE_SCIFACT-152_ANCHOR
source_label: qrel:1
evidence_excerpt: Leucine-rich repeat kinase 2 (LRRK2) mutations are the most common genetic cause of Parkinson's disease. LRRK2 is a multifunctional protein affecting many cellular processes and has been described to bind microtubules. Defective microtubule-based axonal transport is hypothesized to contribute to Parkinson's disease, but whether LRRK2 mutations affect this process to mediate pathogenesis is not known. Here we find that LRRK2 containing pathogenic Roc-COR domain mutations (R1441C, Y1699C) preferentially associates...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: none
source_anchor: status=valid path=raw_sources/SCIFACT-152.md hash=81c9b11481915559b18b700b97b10bd128248225697ef8926e7b93699c4489b5 start=211 end=431 quote="Leucine-rich repeat kinase 2 (LRRK2) mutations are the most common genetic cause of Parkinson's disease. LRRK2 is a multifunctional protein affecting many cellular processes and has been described to bind microtubules. D"
evidence_excerpt: Leucine-rich repeat kinase 2 (LRRK2) mutations are the most common genetic cause of Parkinson's disease. LRRK2 is a multifunctional protein affecting many cellular processes and has been described to bind microtubules. Defective microtubule-based axonal transport is hypothesized to contribute to Parkinson's disease, but whether LRRK2 mutations affect this process to mediate pathogenesis is not known. Here we find that LRRK2 containing pathogenic Roc-COR domain mutations (R1441C, Y1699C) preferentially associates with deacetylated microtubules, and inhibits axonal transport in primary neurons and in Drosophila, causing locomotor deficits in vivo. In vitro, increasing microtubule acetylatio...
```

## QUICK-MAIN-019 / HOLDOUT-045

Layer: `over_grouping_near_miss` | Anchor status: `valid` | Pool: `adversarial_holdout`

### View A

```text
case: HOLDOUT-045
state: ordinary
summary: Basophils counteract disease development in patients with systemic lupus erythematosus (SLE).
anchor_health: valid source=full_anchor_sources/HOLDOUT-045.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=full_anchor_sources/HOLDOUT-045.md hash=06e1a5c81f074719e5c0567377c7820f074aab9f18de58c00a539d76c8f72f07 version=holdout-v1 selector=text_quote+char_offset start=205 end=425 quote="In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activation of basophils by autoreactive IgE ca"
record_pointer: path=records/HOLDOUT-045.json
evidence_pointer: path=evidence/HOLDOUT-045.md marker=EVIDENCE_HOLDOUT-045_ANCHOR
source_label: qrel:1
evidence_excerpt: In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activation of basophils by autoreactive IgE causes their homing to lymph nodes, promoting T helper type 2 (T(H)2) cell differentiation and enhancing the production of self-reactive antibodies that cause lupus-like nephritis in mice lacking the Src family protein tyrosine kinase Lyn (Lyn(-/-) mice). Individuals with SLE also have elevated ser...
FULL_AUDIT_OPEN
deep_packet_retained: true
signals: none
source_anchor: status=valid path=full_anchor_sources/HOLDOUT-045.md hash=06e1a5c81f074719e5c0567377c7820f074aab9f18de58c00a539d76c8f72f07 start=205 end=425 quote="In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activation of basophils by autoreactive IgE ca"
evidence_excerpt: In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activation of basophils by autoreactive IgE causes their homing to lymph nodes, promoting T helper type 2 (T(H)2) cell differentiation and enhancing the production of self-reactive antibodies that cause lupus-like nephritis in mice lacking the Src family protein tyrosine kinase Lyn (Lyn(-/-) mice). Individuals with SLE also have elevated serum IgE, self-reactive IgEs and activated basophils that express CD62 ligand (CD62L) and the major histocompatibility complex (MHC) class II molecule human leukocyte antigen-DR (HLA...
```

### View B

```text
case: HOLDOUT-045
state: ordinary
summary: Basophils counteract disease development in patients with systemic lupus erythematosus (SLE).
anchor_health: valid source=full_anchor_sources/HOLDOUT-045.md
open_gap: over_grouping_near_miss
why: light metadata stub ; feedback: categorical no truth change
pointer_triad: source_path=full_anchor_sources/HOLDOUT-045.md source_hash=06e1a5c81f074719e5c0567377c7820f074aab9f18de58c00a539d76c8f72f07 source_version=holdout-v1 selector=text_quote+char_offset start=205 end=425 record_path=records/HOLDOUT-045.json evidence_path=evidence/HOLDOUT-045.md evidence_marker=EVIDENCE_HOLDOUT-045_ANCHOR quote="In systemic lupus erythematosus (SLE), self-reactive antibodies can target the kidney (lupus nephritis), leading to functional failure and possible mortality. We report that activation of basophils by autoreactive IgE ca"
```

## QUICK-MAIN-020 / HOLDOUT-073

Layer: `serious_folded_violation` | Anchor status: `valid` | Pool: `adversarial_holdout`

### View A

```text
case: HOLDOUT-073
state: regressed
summary: Cold exposure reduces BAT recruitment.
anchor_health: valid source=full_anchor_sources/HOLDOUT-073.md
open_gap: baseline full audit visible
why: baseline_full all details open
source_pointer: path=full_anchor_sources/HOLDOUT-073.md hash=59ac41c10e6c838a3da5c9a2dfd3ea439519014fbbc6dedb4bec64fff37f5c9a version=holdout-v1 selector=text_quote+char_offset start=150 end=370 quote="Molecular mechanisms underlying the cold-associated high cardiovascular risk remain unknown. Here, we show that the cold-triggered food-intake-independent lipolysis significantly increased plasma levels of small low-dens"
record_pointer: path=records/HOLDOUT-073.json
evidence_pointer: path=evidence/HOLDOUT-073.md marker=EVIDENCE_HOLDOUT-073_ANCHOR
source_label: qrel:1
evidence_excerpt: Molecular mechanisms underlying the cold-associated high cardiovascular risk remain unknown. Here, we show that the cold-triggered food-intake-independent lipolysis significantly increased plasma levels of small low-density lipoprotein (LDL) remnants, leading to accelerated development of atherosclerotic lesions in mice. In two genetic mouse knockout models (apolipoprotein E(-/-) [ApoE(-/-)] and LDL receptor(-/-) [Ldlr(-/-)] mice), persistent cold exposure stimulated atherosclerotic plaque growth by increasing l...
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
