---
record_kind: topic_retrieval_pack
status: candidate
topic_id: source-intake-routing
truth_boundary: navigation_only
created_at: 2026-06-07
default_include_path_roles:
  - mainline_docs
  - templates
  - latest_handoff
  - index
default_exclude_path_roles:
  - old_sandbox
  - baseline_copy
  - package_copy
  - zip_file
  - repo_snapshot
  - archived_overlay
lanes:
  mainline:
    - SOURCE_INTAKE.md
    - templates/source-record.md
    - templates/video-source.md
    - templates/candidate-distillation.md
    - templates/query-run.md
  candidate:
    - outputs/review/*candidate-distillation.md
  raw:
    - raw/articles/
    - raw/videos/
    - raw/repos/
  overlay:
    - outputs/review/project_overlays/VAKS/
  audit:
    - outputs/review/source-intake-control-flow-sandbox-2026-06-06/checks/
allowed_use:
  - navigation
  - query expansion
  - include/exclude defaults
forbidden_use:
  - truth
  - reviewed relation
  - action basis
  - ontology
---

# Fixture: Source Intake Topic Retrieval Pack

## Expected Behavior

This pack gives a clean entry route for the topic.

It does not decide truth.
