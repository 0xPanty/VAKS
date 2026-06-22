---
type: source
record_kind: source_card
status: source-captured
title: "PaperTrail: A Claim-Evidence Interface for Grounding Provenance in LLM-based Scholarly Q&A"
source_id: 2026-05-29-papertrail-source
source_uri: https://arxiv.org/abs/2602.21045
source_url: https://arxiv.org/abs/2602.21045
source_type: paper
authors:
  - Anna Martin-Boyle
  - Cara A.C. Leckey
  - Martha C. Brown
  - Harmanpreet Kaur
publisher: arXiv
venue: ACM CHI 2026
published_at: 2026-02-24
captured_at: 2026-05-29
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-05-29
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2602.21045v1
source_status: active
raw_location:
review_priority: normal
review_owner: Codex
formalization_status: source-only
topics:
  - provenance
  - context-pack
  - coverage-map
  - claim-evidence
projects:
  - verified-action-knowledge-system
source_family: papertrail
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []

knowledge_status: raw
processing_tier: light
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---

# 来源记录：PaperTrail

## 为什么收录

Pro 第五个补充建议吸收 PaperTrail 的一个核心启发：普通 citation 对严肃验证粒度太粗，context pack 应该展示关键判断的证据覆盖情况。

本项目只吸收 `coverage_map` 思路，不实现 PaperTrail 的完整界面、不做全量遗漏扫描、不把 coverage status 变成 truth 更新机制。

## 来源信息

- 论文：PaperTrail: A Claim-Evidence Interface for Grounding Provenance in LLM-based Scholarly Q&A
- 作者：Anna Martin-Boyle, Cara A.C. Leckey, Martha C. Brown, Harmanpreet Kaur
- arXiv：https://arxiv.org/abs/2602.21045
- 提交时间：2026-02-24
- 会议状态：ACM CHI 2026

## 初步看点

- PaperTrail 指出，普通 source citation 对学术问答的验证来说粒度太粗。
- 它把 LLM answer 和 source documents 拆成 discrete claims / evidence，并映射 supported assertions、unsupported claims 和 omitted source information。
- 用户研究显示，细粒度 provenance 会降低盲目信任，但验证任务仍然有认知负担。

## 吸收方式

```text
Use the idea, not the UI.

Context pack is not a citation list.
Context pack should expose key point coverage:
  supported
  weakly_supported
  challenged
  missing_evidence
  out_of_scope
  not_verifiable
  risk_flags / risk_refs / action_readiness
```

## 边界

```text
coverage_map is an audit surface, not a truth layer.
coverage_status does not automatically change confidence.
missing_evidence does not mean false.
challenged does not mean rejected.
critical_omissions are known major omissions only, not exhaustive omission detection.
Use progressive disclosure: overview first, details on demand.
```

## 可抽取 Candidate Points

1. Context packs should show key point coverage, not just citations.
2. Coverage should include support, weak support, challenges, missing evidence, out-of-scope points, risk, and critical omissions.
3. More detailed provenance can reduce blind trust, but can also increase verification burden.
4. Coverage should use progressive disclosure: overview first, point details on demand.

## 下一步

- Test `coverage_map` in the first manual context pack / action basis trial.
- Do not build a full UI before the schema and manual trial prove useful.
