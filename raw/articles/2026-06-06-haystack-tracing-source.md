---
type: source
status: source-captured
title: "Haystack Tracing"
source_id: haystack-tracing-2026
source_uri: https://docs.haystack.deepset.ai/docs/tracing
source_url: https://docs.haystack.deepset.ai/docs/tracing
source_type: official_documentation
platform: web
author: "deepset / Haystack"
publisher: Haystack Documentation
published_at:
updated_at:
captured_at: 2026-06-06
captured_by: Codex
raw_location: raw/articles/2026-06-06-haystack-tracing-source.md
processing_mode: public-web-read
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
source_status: active
confidence_cap_reason: "Official documentation read from public web; tracing is operational observability, not evidence support."
topics:
  - tracing
  - opentelemetry
  - pipeline-observability
  - content-tracing
  - query-run-receipt
  - privacy-boundary
projects:
  - verified-action-knowledge-system
candidate_relation_suggestions:
  - candidate:pipeline_trace_as_query_run_receipt
  - candidate:content_tracing_default_off_privacy_boundary
  - candidate:trace_backend_not_truth_authority
tags:
  - raw-article
  - haystack
  - tracing
  - opentelemetry
  - candidate-only
---

# Source Record: Haystack Tracing

## Why Saved

This Haystack documentation is relevant to the VAKS retrieval/query contract
because it shows a mature RAG/LLM pipeline tool treating tracing as a first-class
operational concern.

For VAKS, the useful idea is not a tracing backend. The useful idea is:

```text
query-run steps should be observable and replayable enough to debug
planner / recall / rerank / pack / answer / evidence-binding failures.
```

## Source Boundary

```text
Official docs = external source provenance.
This card = raw/source record.
Extraction note = candidate comprehension.
Candidate points = review input only.
No reviewed VAKS knowledge is created by this record.
```

## What Was Observed

Haystack supports tracing backends such as OpenTelemetry and Datadog. It can
auto-detect configured tracing, and it can also be configured directly in code.

The page has an important safety boundary: content tracing, which records
pipeline component input/output values, is disabled by default to avoid sending
sensitive user information to a tracing backend. It must be explicitly enabled.

## VAKS Candidate Signals

Potential candidate knowledge points:

```text
pipeline_trace_as_query_run_receipt:
  VAKS query-run should record stage events and warnings, not just final pack.

content_tracing_default_off_privacy_boundary:
  storing snippets/prompts/answers in receipts should be intentional and scoped.

trace_backend_not_truth_authority:
  trace data explains what happened; it does not prove that the answer is true.
```

## Not Adopted Yet

Do not treat this source as:

```text
permission to build an observability platform
permission to log all content by default
proof that traced outputs are correct
mandatory OpenTelemetry schema for VAKS
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md
```
