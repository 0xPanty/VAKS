---
type: source
status: source-captured
title:
source_id:
source_uri:
source_url:
source_type: video
platform:
platform_id:
author:
publisher:
published_at:
updated_at:
duration:
captured_at:
captured_by: Codex
raw_location: raw/videos/
processing_mode: inbox
processing_level: light
processing_tier: light
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public
transcript_method: none
transcript_location:
segments_location:
transcript_metadata_location:
ledger_location:
media_retention: not_downloaded
source_status: unknown
topics: []
content_form: video
language:
version_or_time_scope:
entities: []
aliases: []
entity_refs: []
project_refs: []
source_family:
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags: []
---

# 视频资料：

## Intake Boundary

Video source records provide provenance, transcript locations, and confirmed
discovery metadata.

They do not create reviewed evidence, project borrowing conclusions, or action
basis.

`topics`, `entities`, and `tags` are recall / filtering metadata only.

## 获取与转写

```yaml
subtitle_status:
transcript_method: public_subtitle | local_asr | user_supplied | none
asr_model:
asr_device:
transcript_quality: high | medium | low | unknown
media_retention: deleted | kept | not_downloaded
scratch_cleanup:
project_visible_artifacts: yes | no
transcript_metadata_location:
ledger_location:
```

## Discovery Metadata

```yaml
topics: []
content_form: video
language:
version_or_time_scope:
entities: []
aliases: []
entity_refs: []
tags: []
```

## 可抽取 Candidate Points

Use candidate notes for real knowledge points. Do not encode them as video
source tags.
