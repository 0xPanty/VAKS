---
type: source
status: source-captured
title: "RyanCodrai/turbovec"
source_id: 2026-06-11-RyanCodrai-turbovec-source
source_uri: https://github.com/RyanCodrai/turbovec
source_url: https://github.com/RyanCodrai/turbovec
source_type: repository
author: Ryan Codrai
publisher: GitHub / PyPI
created_at: 2026-03-26
captured_at: 2026-06-11
captured_by: Codex
version_or_commit: fcc1eb8e06c52764907b677128845995309219e0
release_version_checked: turbovec 0.7.1
release_checked_at: 2026-06-11
processing_mode: explicit_strong_distill
processing_level: heavy
processing_tier: heavy
review_priority: high
review_owner: Codex
formalization_status: candidate-generated
knowledge_status: raw
action_basis_allowed: false
truth_mutation_allowed: false
source_integrity:
  repository_head: fcc1eb8e06c52764907b677128845995309219e0
  py_v0_7_1_tag: f80156e536885369772d356a7879870b1b3d22d5
  snapshot_location: raw/repos/_snapshots/2026-06-11-RyanCodrai-turbovec-fcc1eb8-source.zip
  snapshot_sha256: ec1795bb0d4fe86ac64be41f4ae26ce4afcc34b7fe9e8f2d910b4d72643deb16
  pypi_sdist_sha256: 06e6710e54fc0e4640575601fcdf782c598f9cd66ff1a561b7be5d79d645e3af
adapter_ingest:
  adapter_name: web + GitHub API + PyPI JSON + git ls-remote + source snapshot
  adapter_version: manual-codex-2026-06-11
  capture_method: repository metadata, package metadata, primary paper/blog pages, raw source files, codeload snapshot
  extraction_trace:
    - GitHub repository metadata checked 2026-06-11
    - PyPI package JSON checked 2026-06-11
    - git ls-remote checked HEAD and py-v0.7.1 tag
    - raw README, docs/api.md, pyproject, Cargo.toml, Rust/Python bindings, integration docs, and benchmark scripts inspected
    - Google Research blog, OpenReview, and arXiv TurboQuant references inspected
  known_limits:
    - Benchmarks were inspected, not rerun locally.
    - README benchmark claims are project-published, not independent validation.
    - GitHub stars and PyPI release metadata are point-in-time facts captured on 2026-06-11.
source_status: active
raw_location: raw/repos/_snapshots/2026-06-11-RyanCodrai-turbovec-fcc1eb8-source.zip
topics:
  - vector-search
  - retrieval-cache
  - local-rag
  - embedded-index
  - turboquant
  - hybrid-retrieval
  - context-pack-preparation
  - derived-cache
  - privacy
  - agent-context
projects:
  - verified-action-knowledge-system
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - source/repo
  - source/pypi
  - topic/vector-search
  - topic/retrieval-cache
  - topic/local-rag
  - candidate-only
---

# turbovec Source Record

## Why Captured

The user requested a strong distillation of `turbovec` and asked whether the
library helps VAKS vector retrieval.

This source is relevant to VAKS because it is a young, embedded vector index
library around TurboQuant-style 2-4 bit vector compression, online ingest, local
search, stable external IDs, and search-time allowlist filtering.

Boundary:

```text
repository/source/package = raw source evidence
README benchmarks = candidate implementation signal
TurboQuant paper/blog = algorithm background
VAKS fit judgment = candidate-only design review
promotion = later evidence-aware review / local benchmark only
```

## Source Identity

```yaml
repository: https://github.com/RyanCodrai/turbovec
package: https://pypi.org/project/turbovec/
package_version_checked: 0.7.1
repository_head_checked: fcc1eb8e06c52764907b677128845995309219e0
license: MIT
python_requires: ">=3.9"
pypi_status_classifier: "Development Status :: 3 - Alpha"
primary_algorithm_references:
  - https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/
  - https://openreview.net/forum?id=tO3ASKZlok
  - https://arxiv.org/abs/2504.19874
```

Point-in-time metadata captured on 2026-06-11:

```yaml
github_stars: 10680
github_forks: 918
github_open_issues: 10
github_pushed_at: 2026-06-10T16:18:48Z
pypi_latest_upload: 2026-06-09T21:08:46Z
```

## Inspected Repository Areas

```text
README.md
docs/api.md
docs/integrations/langchain.md
docs/integrations/llama_index.md
turbovec/src/lib.rs
turbovec/src/id_map.rs
turbovec-python/src/lib.rs
turbovec-python/pyproject.toml
Cargo.toml
benchmarks/suite/compression.py
benchmarks/suite/recall_d1536_4bit.py
benchmarks/suite/speed_d1536_4bit_x86_st.py
```

## Extracted Architecture Signal

For VAKS, the important source signal is not "replace all retrieval with this
library." The useful signal is narrower:

```text
Markdown/YAML remains authority
SQLite/BM25/metadata remains filter and authority-bucket layer
turbovec may become a local derived dense retrieval cache
allowlist search can rerank only approved candidate IDs
IdMapIndex can map vectors back to stable VAKS source/chunk IDs
compressed local vectors may make air-gapped context-pack retrieval cheaper
```

## Candidate Risks

```text
Alpha package status
young repository
self-published benchmarks
no local VAKS benchmark yet
Windows performance not verified on this machine
2-bit recall may be too weak for some corpora
vector retrieval score is not support, truth confidence, or action readiness
```

## Immediate Routing

```yaml
borrow_value: strong
borrow_order: P1_for_retrieval_cache_P2_for_core_dependency
design_use_allowed: true
implementation_use_allowed: sandbox_only
review_required_before_mainline_dependency: true
```

