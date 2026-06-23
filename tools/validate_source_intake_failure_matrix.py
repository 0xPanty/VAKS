#!/usr/bin/env python
"""Run adversarial Source Intake failure-matrix checks."""

from __future__ import annotations

import argparse
import csv
import json
import tempfile
from pathlib import Path
from typing import Any

import yaml

import validate_source_intake_contract as contract


OUT_DIR = Path("outputs/review/source-intake-control-flow-hardening-2026-06-12/results")


FRONTMATTER_CASES: list[dict[str, Any]] = [
    {
        "id": "FM-01",
        "scenario": "Medium candidate becomes action basis",
        "frontmatter": {
            "record_kind": "candidate_distillation",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "retrieval_policy": {
                "policy_kind": "orientation_only",
                "pack_allowed": "activation_only",
                "action_basis_allowed": True,
                "warning_code": "candidate_not_action_basis",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": True,
            "truth_mutation_allowed": False,
        },
        "expected_check": "authority_bypass",
    },
    {
        "id": "FM-02",
        "scenario": "Suggested overlay persists without confirmation",
        "frontmatter": {
            "record_kind": "project_overlay",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "overlay_state": "suggested",
            "retrieval_scope": "active_project_only",
            "default_retrieval": False,
            "retrieval_policy": {
                "policy_kind": "project_context_only",
                "pack_allowed": "none",
                "action_basis_allowed": False,
                "warning_code": "overlay_unconfirmed",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "suggested_overlay_persisted",
    },
    {
        "id": "FM-03",
        "scenario": "Confirmed overlay leaks outside active project",
        "frontmatter": {
            "record_kind": "project_overlay",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "overlay_state": "confirmed",
            "retrieval_scope": "global",
            "default_retrieval": False,
            "retrieval_policy": {
                "policy_kind": "project_context_only",
                "pack_allowed": "activation_only",
                "action_basis_allowed": False,
                "warning_code": "overlay_not_authority",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "overlay_scope",
    },
    {
        "id": "FM-08",
        "scenario": "Archived overlay remains in default retrieval",
        "frontmatter": {
            "record_kind": "project_overlay",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "overlay_state": "archived",
            "retrieval_scope": "archived_excluded",
            "default_retrieval": True,
            "retrieval_policy": {
                "policy_kind": "project_context_only",
                "pack_allowed": "activation_only",
                "action_basis_allowed": False,
                "warning_code": "archived_overlay_excluded",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "archived_overlay_default_retrieval",
    },
    {
        "id": "FM-10",
        "scenario": "Enum drift bypasses filter",
        "frontmatter": {
            "record_kind": "candidate_distillation",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "overlay_state": "candidate",
            "retrieval_policy": {
                "policy_kind": "candidate_only",
                "pack_allowed": "context_with_warning",
                "action_basis_allowed": False,
                "warning_code": "candidate_not_reviewed",
            },
            "promotion_gate": "evidence_aware_review_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "enum_registry",
    },
    {
        "id": "FM-11",
        "scenario": "Feedback directly mutates reviewed truth",
        "frontmatter": {
            "record_kind": "feedback_event",
            "knowledge_status": "candidate",
            "processing_tier": "light",
            "event_kind": "misleading_orientation",
            "target_ref": "wiki/claims/example.md",
            "observed_in_context": "project:test",
            "event_time": "2026-06-12",
            "review_pressure_effect": "none",
            "retrieval_policy": {
                "policy_kind": "project_context_only",
                "pack_allowed": "review_input_only",
                "action_basis_allowed": False,
                "warning_code": "feedback_not_truth",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": True,
        },
        "expected_check": "authority_bypass",
    },
    {
        "id": "FM-13",
        "scenario": "Candidate missing source/provisional/candidate points",
        "frontmatter": {
            "record_kind": "candidate_distillation",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "retrieval_policy": {
                "policy_kind": "orientation_only",
                "pack_allowed": "activation_only",
                "action_basis_allowed": False,
                "warning_code": "candidate_not_action_basis",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "missing_required_field",
    },
    {
        "id": "FM-14",
        "scenario": "Source card claims reviewed knowledge status",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "reviewed",
            "processing_tier": "light",
            "source_id": "demo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-12",
            "title": "Demo",
            "why_saved": "test",
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_card_status",
    },
    {
        "id": "FM-15",
        "scenario": "Confirmed overlay enters global default retrieval",
        "frontmatter": {
            "record_kind": "project_overlay",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "overlay_state": "confirmed",
            "retrieval_scope": "active_project_only",
            "default_retrieval": True,
            "project_id": "VAKS",
            "target_ref": "raw/repos/demo.md",
            "project_borrow_scope": "demo",
            "project_non_borrow_scope": "For project VAKS, do not currently borrow X as Y because Z. Reopen if evidence changes.",
            "project_reopen_trigger": "if evidence changes",
            "retrieval_policy": {
                "policy_kind": "project_context_only",
                "pack_allowed": "activation_only",
                "action_basis_allowed": False,
                "warning_code": "overlay_not_authority",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "confirmed_overlay_default_retrieval",
    },
    {
        "id": "FM-16",
        "scenario": "Accepted heavy review skips forbidden proxy check",
        "frontmatter": {
            "record_kind": "heavy_review_open",
            "knowledge_status": "candidate",
            "processing_tier": "heavy",
            "promotion_gate": "v0_2_13_required",
            "review_status": "accepted",
            "claim": "Demo claim",
            "source_anchor_refs": ["raw/demo.md#anchor"],
            "warrant": "Independent anchor supports claim.",
            "scope": "demo",
            "gaps": ["none"],
            "residual_risk": "low",
            "forbidden_support_proxies_checked": False,
            "retrieval_policy": {
                "policy_kind": "reviewed_support_only",
                "pack_allowed": "reviewed_support",
                "action_basis_allowed": False,
                "warning_code": "heavy_review_open_not_passed",
            },
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "forbidden_proxy_check_missing",
    },
    {
        "id": "FM-17",
        "scenario": "Feedback lacks project/context scope",
        "frontmatter": {
            "record_kind": "feedback_event",
            "knowledge_status": "candidate",
            "processing_tier": "light",
            "event_kind": "misleading_orientation",
            "target_ref": "wiki/claims/demo.md",
            "event_time": "2026-06-12",
            "review_pressure_effect": "review_due",
            "retrieval_policy": {
                "policy_kind": "project_context_only",
                "pack_allowed": "review_input_only",
                "action_basis_allowed": False,
                "warning_code": "feedback_not_truth",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "missing_required_field",
    },
    {
        "id": "FM-18",
        "scenario": "Confirmed overlay lacks project and target refs",
        "frontmatter": {
            "record_kind": "project_overlay",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "overlay_state": "confirmed",
            "retrieval_scope": "active_project_only",
            "default_retrieval": False,
            "project_borrow_scope": "demo",
            "project_non_borrow_scope": "For project VAKS, do not currently borrow X as Y because Z. Reopen if evidence changes.",
            "project_reopen_trigger": "if evidence changes",
            "retrieval_policy": {
                "policy_kind": "project_context_only",
                "pack_allowed": "activation_only",
                "action_basis_allowed": False,
                "warning_code": "overlay_not_authority",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "missing_required_field",
    },
    {
        "id": "FM-19",
        "scenario": "Query-run uses invalid query_mode",
        "frontmatter": {
            "record_kind": "query_run_trace",
            "query_mode": "decide_now",
            "selected_items": [],
        },
        "expected_check": "enum_registry",
    },
    {
        "id": "FM-20",
        "scenario": "Query-run candidate item is direct support",
        "frontmatter": {
            "record_kind": "query_run_trace",
            "query_mode": "action",
            "selected_items": [
                {
                    "ref": "outputs/review/candidate.md",
                    "record_kind": "candidate_distillation",
                    "knowledge_status": "candidate",
                    "pack_role": "support",
                    "warning_code": "candidate_not_action_basis",
                    "action_basis_allowed": False,
                    "independent_anchor_ref": "",
                    "selected_by": {"semantic": True},
                }
            ],
        },
        "expected_check": "non_support_record_marked_support",
    },
    {
        "id": "FM-20A",
        "scenario": "Query-run source annotation item is direct support",
        "frontmatter": {
            "record_kind": "query_run_trace",
            "query_id": "fm-20a",
            "query_time": "2026-06-14",
            "question_summary": "Can an annotation act as support?",
            "verbatim_input": "test",
            "query_mode": "action",
            "requested_authority_bucket": "reviewed_support_only",
            "active_project": "VAKS",
            "human_confirmation_required": True,
            "selected_items": [
                {
                    "ref": "outputs/review/source_annotations/demo/ann-001.md",
                    "record_kind": "source_annotation",
                    "knowledge_status": "candidate",
                    "pack_role": "support",
                    "warning_code": "annotation_not_support",
                    "action_basis_allowed": False,
                    "independent_anchor_ref": "raw/demo.md#ann-001",
                    "selected_by": {"annotation_id": "ann-001"},
                }
            ],
        },
        "expected_check": "non_support_record_marked_support",
    },
    {
        "id": "FM-20B",
        "scenario": "Source annotation is incorrectly marked as heavy processing",
        "frontmatter": {
            "record_kind": "source_annotation",
            "knowledge_status": "candidate",
            "processing_tier": "heavy",
            "annotation_id": "ann-heavy",
            "source_ref": "raw/demo.md",
            "selector_type": "TextQuoteSelector",
            "selector_exact": "Demo quote",
            "anchor_status": "exact_verified",
            "annotation_role": "candidate_seed",
            "support_checked": False,
            "evidence_support_status": "not_checked",
            "retrieval_policy": {
                "policy_kind": "orientation_only",
                "pack_allowed": "review_input_only",
                "action_basis_allowed": False,
                "warning_code": "annotation_not_support",
            },
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_annotation_processing_tier",
    },
    {
        "id": "FM-21",
        "scenario": "Heavy review warrant uses benchmark/proxy as support",
        "frontmatter": {
            "record_kind": "heavy_review_open",
            "knowledge_status": "candidate",
            "processing_tier": "heavy",
            "promotion_gate": "v0_2_13_required",
            "review_status": "pending",
            "claim": "Demo claim",
            "source_anchor_refs": ["raw/demo.md#anchor"],
            "warrant": "benchmark passed and graph rank is high",
            "scope": "demo",
            "gaps": ["needs review"],
            "residual_risk": "medium",
            "forbidden_support_proxies_checked": False,
            "retrieval_policy": {
                "policy_kind": "orientation_only",
                "pack_allowed": "review_input_only",
                "action_basis_allowed": False,
                "warning_code": "heavy_review_open_not_passed",
            },
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "proxy_support_in_warrant",
    },
    {
        "id": "FM-22",
        "scenario": "Candidate distillation omits canonical record_kind",
        "frontmatter": {
            "type": "candidate_distillation",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "provisional": True,
            "derived_from": ["raw/repos/demo.md"],
            "candidate_points": ["demo"],
            "retrieval_policy": {
                "policy_kind": "orientation_only",
                "pack_allowed": "activation_only",
                "action_basis_allowed": False,
                "warning_code": "candidate_not_action_basis",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "canonical_serialization",
    },
    {
        "id": "FM-23",
        "scenario": "Legacy source_record omits canonical source_card record_kind",
        "frontmatter": {
            "type": "source_record",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "demo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-13",
            "title": "Demo",
            "why_saved": "test",
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "canonical_serialization",
    },
    {
        "id": "FM-24",
        "scenario": "Query-run trace only serializes query_mode and skips receipt contract",
        "frontmatter": {
            "record_kind": "query_run_trace",
            "query_mode": "orientation",
        },
        "expected_check": "missing_required_field",
    },
    {
        "id": "FM-25",
        "scenario": "Context-pack manifest skips top-level pack contract",
        "frontmatter": {
            "record_kind": "context_pack_manifest",
            "query_mode": "orientation",
        },
        "expected_check": "missing_required_field",
    },
    {
        "id": "FM-26",
        "scenario": "Overlay suggestion persists as standalone record",
        "frontmatter": {
            "record_kind": "overlay_suggestion",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "retrieval_policy": {
                "policy_kind": "project_context_only",
                "pack_allowed": "none",
                "action_basis_allowed": False,
                "warning_code": "overlay_unconfirmed",
            },
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "suggested_overlay_persisted",
    },
    {
        "id": "FM-27",
        "scenario": "Raw source why_saved placeholder has no body capture reason",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "demo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-13",
            "title": "Demo",
            "why_saved": "see_body_or_legacy_record",
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_why_saved_placeholder_without_body_reason",
    },
    {
        "id": "FM-28",
        "scenario": "Raw source card carries top-level relations as authority-like metadata",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "demo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-13",
            "title": "Demo",
            "why_saved": "test",
            "relations": [
                {
                    "target": "wiki/claims/demo.md",
                    "type": "supports",
                    "strength": 5,
                    "confidence": "high",
                    "evidence": ["raw/demo.md"],
                }
            ],
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_card_relation_authority_metadata",
    },
    {
        "id": "FM-29",
        "scenario": "Duplicate YAML key hides boundary field through last-wins parsing",
        "frontmatter_text": """record_kind: source_card
knowledge_status: raw
processing_tier: light
source_id: demo
source_url: https://example.com
raw_location: raw/demo-a.md
raw_location: raw/demo-b.md
captured_at: 2026-06-13
title: Demo
why_saved: test
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
""",
        "expected_check": "duplicate_yaml_key",
    },
    {
        "id": "FM-30",
        "scenario": "Legacy project_lens_overlay passes as if canonical overlay without warning",
        "frontmatter": {
            "type": "project_lens_overlay",
            "record_kind": "project_overlay",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "overlay_state": "confirmed",
            "retrieval_scope": "active_project_only",
            "default_retrieval": False,
            "project_id": "VAKS",
            "target_ref": "see_derived_from_or_body",
            "project_borrow_scope": "see_target_layers_or_body",
            "project_non_borrow_scope": "see_non_target_layers_or_body",
            "project_reopen_trigger": "review_if_project_scope_or_evidence_changes",
            "retrieval_policy": {
                "policy_kind": "project_context_only",
                "pack_allowed": "activation_only",
                "action_basis_allowed": False,
                "warning_code": "overlay_not_authority",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "legacy_project_lens_overlay_compatibility",
    },
    {
        "id": "FM-31",
        "scenario": "Raw source card carries top-level confidence outside capture namespace",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "demo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-13",
            "title": "Demo",
            "why_saved": "test",
            "confidence": "high",
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_card_confidence_not_namespaced",
    },
    {
        "id": "FM-32",
        "scenario": "Confirmed overlay uses placeholder for semantic required field",
        "frontmatter": {
            "record_kind": "project_overlay",
            "knowledge_status": "candidate",
            "processing_tier": "medium",
            "overlay_state": "confirmed",
            "retrieval_scope": "active_project_only",
            "default_retrieval": False,
            "project_id": "VAKS",
            "target_ref": "see_derived_from_or_body",
            "project_borrow_scope": "see_target_layers_or_body",
            "project_non_borrow_scope": "see_non_target_layers_or_body",
            "project_reopen_trigger": "review_if_project_scope_or_evidence_changes",
            "retrieval_policy": {
                "policy_kind": "project_context_only",
                "pack_allowed": "activation_only",
                "action_basis_allowed": False,
                "warning_code": "overlay_not_authority",
            },
            "promotion_gate": "v0_2_13_required",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "confirmed_overlay_placeholder_value",
    },
    {
        "id": "FM-33",
        "scenario": "Legacy source_integrity remains compatibility warning only",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "demo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-23",
            "title": "Demo",
            "why_saved": "test",
            "source_integrity": {
                "source_hash": "sha256:legacy",
                "snapshot_hash": "sha256:legacy",
                "ingest_state": "unknown",
            },
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "legacy_source_integrity_compatibility",
    },
    {
        "id": "FM-34",
        "scenario": "Top-level vsrc source_id contradicts source_identity.source_id",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "vsrc:1:repo:github.com/example/one",
            "source_url": "https://example.com",
            "captured_at": "2026-06-23",
            "title": "Demo",
            "why_saved": "test",
            "source_identity": {
                "schema_version": 1,
                "source_id": "vsrc:1:repo:github.com/example/two",
                "kind": "repo",
                "canonical_locator": "git+https://github.com/example/two",
                "identity_profile": "repo-provider-native/v1",
                "aliases": [],
            },
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_identity_top_level_mismatch",
    },
    {
        "id": "FM-35",
        "scenario": "Retrieval selects item from legacy_raw_metadata",
        "frontmatter": {
            "record_kind": "query_run_trace",
            "query_id": "demo",
            "query_time": "2026-06-13",
            "question_summary": "demo",
            "verbatim_input": "demo",
            "query_mode": "orientation",
            "requested_authority_bucket": "raw",
            "active_project": "VAKS",
            "human_confirmation_required": False,
            "included_buckets": ["raw"],
            "excluded_buckets": [],
            "retrieval_filters": {},
            "selected_items": [
                {
                    "ref": "raw/demo.md#legacy_raw_metadata",
                    "record_kind": "source_card",
                    "knowledge_status": "raw",
                    "pack_role": "orientation",
                    "warning_code": "raw_is_provenance_only",
                    "action_basis_allowed": False,
                    "independent_anchor_ref": "",
                    "selected_by": {"legacy_raw_metadata": True},
                }
            ],
            "support_checks": [],
        },
        "expected_check": "legacy_raw_metadata_used_for_selection",
    },
    {
        "id": "FM-36",
        "scenario": "v1 source_identity missing required schema_version",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "vsrc:1:repo:github.com/example/repo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-23",
            "title": "Demo",
            "why_saved": "test",
            "source_identity": {
                "source_id": "vsrc:1:repo:github.com/example/repo",
                "kind": "repo",
                "canonical_locator": "git+https://github.com/example/repo",
                "identity_profile": "repo-provider-native/v1",
                "aliases": [],
            },
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_identity_missing_field",
    },
    {
        "id": "FM-37",
        "scenario": "source_identity kind contradicts vsrc kind",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "vsrc:1:repo:github.com/example/repo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-23",
            "title": "Demo",
            "why_saved": "test",
            "source_identity": {
                "schema_version": 1,
                "source_id": "vsrc:1:repo:github.com/example/repo",
                "kind": "video",
                "canonical_locator": "git+https://github.com/example/repo",
                "identity_profile": "repo-provider-native/v1",
                "aliases": [],
            },
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_identity_kind_mismatch",
    },
    {
        "id": "FM-38",
        "scenario": "source_identity becomes a capture-history database",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "vsrc:1:repo:github.com/example/repo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-23",
            "title": "Demo",
            "why_saved": "test",
            "source_identity": {
                "schema_version": 1,
                "source_id": "vsrc:1:repo:github.com/example/repo",
                "kind": "repo",
                "canonical_locator": "git+https://github.com/example/repo",
                "identity_profile": "repo-provider-native/v1",
                "aliases": [],
                "capture_history": ["raw/captures/demo/capture-envelope.json"],
            },
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_identity_extra_field",
    },
    {
        "id": "FM-39",
        "scenario": "source_identity alias is not a typed string mapping",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "vsrc:1:repo:github.com/example/repo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-23",
            "title": "Demo",
            "why_saved": "test",
            "source_identity": {
                "schema_version": 1,
                "source_id": "vsrc:1:repo:github.com/example/repo",
                "kind": "repo",
                "canonical_locator": "git+https://github.com/example/repo",
                "identity_profile": "repo-provider-native/v1",
                "aliases": [123],
            },
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_identity_alias_shape",
    },
    {
        "id": "FM-40",
        "scenario": "latest_observed_capture_ref leaks an absolute local path",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "vsrc:1:repo:github.com/example/repo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-23",
            "title": "Demo",
            "why_saved": "test",
            "source_identity": {
                "schema_version": 1,
                "source_id": "vsrc:1:repo:github.com/example/repo",
                "kind": "repo",
                "canonical_locator": "git+https://github.com/example/repo",
                "identity_profile": "repo-provider-native/v1",
                "aliases": [],
            },
            "latest_observed_capture_ref": "C:/Users/Administrator/raw/captures/demo/capture-envelope.json",
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "latest_observed_capture_ref_format",
    },
    {
        "id": "FM-41",
        "scenario": "provider_object_id alias uses non-lowercase provider host",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "vsrc:1:repo:github.com/example/repo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-23",
            "title": "Demo",
            "why_saved": "test",
            "source_identity": {
                "schema_version": 1,
                "source_id": "vsrc:1:repo:github.com/example/repo",
                "kind": "repo",
                "canonical_locator": "git+https://github.com/example/repo",
                "identity_profile": "repo-provider-locator/v1",
                "aliases": [{"kind": "provider_object_id", "value": "GitHub.com:repository:R_kgDOdemo"}],
            },
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_identity_provider_object_id_format",
    },
    {
        "id": "FM-42",
        "scenario": "source_identity aliases contain duplicate provider object IDs",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "vsrc:1:repo:github.com/example/repo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-23",
            "title": "Demo",
            "why_saved": "test",
            "source_identity": {
                "schema_version": 1,
                "source_id": "vsrc:1:repo:github.com/example/repo",
                "kind": "repo",
                "canonical_locator": "git+https://github.com/example/repo",
                "identity_profile": "repo-provider-locator/v1",
                "aliases": [
                    {"kind": "provider_object_id", "value": "github.com:repository:R_kgDOdemo"},
                    {"kind": "provider_object_id", "value": "github.com:repository:R_kgDOdemo"},
                ],
            },
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_identity_alias_duplicate",
    },
    {
        "id": "FM-43",
        "scenario": "source_identity alias kind is outside the v1 allowlist",
        "frontmatter": {
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "processing_tier": "light",
            "source_id": "vsrc:1:repo:github.com/example/repo",
            "source_url": "https://example.com",
            "captured_at": "2026-06-23",
            "title": "Demo",
            "why_saved": "test",
            "source_identity": {
                "schema_version": 1,
                "source_id": "vsrc:1:repo:github.com/example/repo",
                "kind": "repo",
                "canonical_locator": "git+https://github.com/example/repo",
                "identity_profile": "repo-provider-locator/v1",
                "aliases": [{"kind": "truth_score", "value": "github.com:repository:R_kgDOdemo"}],
            },
            "retrieval_policy": {
                "policy_kind": "source_identity_only",
                "pack_allowed": "drilldown_required",
                "action_basis_allowed": False,
                "warning_code": "raw_is_provenance_only",
            },
            "promotion_gate": "none",
            "action_basis_allowed": False,
            "truth_mutation_allowed": False,
        },
        "expected_check": "source_identity_alias_kind_unsupported",
    },
]


RECEIPT_CASES: list[dict[str, Any]] = [
    {
        "id": "FM-04",
        "scenario": "Project non-borrow scope becomes universal ban",
        "artifact": {
            "record_kind": "project_overlay",
            "project_id": "VAKS",
            "project_non_borrow_scope": "Under no circumstances should anyone use X; categorically avoid it.",
            "project_reopen_trigger": "if evidence changes",
        },
        "expected_check": "universal_ban_wording",
    },
    {
        "id": "FM-05",
        "scenario": "Candidate summary is marked support without raw anchor",
        "artifact": {
            "selected_items": [
                {
                    "ref": "outputs/review/candidate.md",
                    "record_kind": "candidate_distillation",
                    "knowledge_status": "candidate",
                    "pack_role": "support",
                    "warning_code": "candidate_not_action_basis",
                    "independent_anchor_ref": "",
                }
            ]
        },
        "expected_check": "candidate_as_support",
    },
    {
        "id": "FM-06",
        "scenario": "Broken anchor is cited in action mode",
        "artifact": {
            "query_mode": "action",
            "selected_items": [
                {
                    "ref": "raw/repos/example-source.md",
                    "record_kind": "source_card",
                    "knowledge_status": "raw",
                    "pack_role": "anchor",
                    "review_pressure": "none",
                    "anchor_status": "broken",
                }
            ],
        },
        "expected_check": "broken_anchor_action_use",
    },
    {
        "id": "FM-07",
        "scenario": "Repeated negative feedback does not create review_due",
        "artifact": {
            "record_kind": "feedback_event",
            "event_kind": "misleading_orientation",
            "negative_count_same_scope": 2,
            "review_pressure_effect": "none",
        },
        "expected_check": "missing_review_pressure",
    },
    {
        "id": "FM-09",
        "scenario": "Heavy Review Open is treated as Review Passed",
        "artifact": {
            "selected_items": [
                {
                    "ref": "templates/heavy-review-open.md",
                    "record_kind": "heavy_review_open",
                    "knowledge_status": "candidate",
                    "review_status": "pending",
                    "pack_role": "support",
                }
            ]
        },
        "expected_check": "pending_heavy_review_as_support",
    },
    {
        "id": "FM-12",
        "scenario": "Diagnostic score becomes support",
        "artifact": {
            "selected_items": [
                {
                    "ref": "dashboard:hit/demo",
                    "record_kind": "candidate_distillation",
                    "knowledge_status": "candidate",
                    "pack_role": "support",
                    "selected_by": {"lexical": True, "semantic": True, "metadata": True},
                    "independent_anchor_ref": "",
                }
            ]
        },
        "expected_check": "diagnostic_signal_as_support",
    },
]


def run_frontmatter_case(root: Path, registry: dict[str, Any], case: dict[str, Any]) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        rel = Path(f"{case['id']}.md")
        if "frontmatter_text" in case:
            yaml_text = case["frontmatter_text"]
        else:
            yaml_text = yaml.safe_dump(case["frontmatter"], sort_keys=False, allow_unicode=True)
        text = "---\n" + yaml_text + "---\n\n# Bad Fixture\n"
        (tmp_root / rel).write_text(text, encoding="utf-8")
        issues: list[dict[str, Any]] = []
        contract.validate_file(tmp_root, rel, registry, issues)
        return sorted({issue["check"] for issue in issues})


def run_receipt_case(case: dict[str, Any]) -> list[str]:
    artifact = case["artifact"]
    checks: list[str] = []
    text = json.dumps(artifact, ensure_ascii=False).lower()
    if case["id"] == "FM-04":
        if any(word in text for word in contract.UNIVERSAL_BAN_TERMS):
            checks.append("universal_ban_wording")
    if case["id"] == "FM-05":
        for item in artifact.get("selected_items", []):
            if item.get("knowledge_status") == "candidate" and item.get("pack_role") == "support":
                checks.append("candidate_as_support")
            if item.get("pack_role") == "support" and not item.get("independent_anchor_ref"):
                checks.append("missing_independent_anchor")
    if case["id"] == "FM-06":
        if artifact.get("query_mode") == "action":
            for item in artifact.get("selected_items", []):
                if item.get("anchor_status") == "broken" and item.get("review_pressure") != "blocked":
                    checks.append("broken_anchor_action_use")
    if case["id"] == "FM-07":
        if artifact.get("negative_count_same_scope", 0) >= 2 and artifact.get("review_pressure_effect") not in {"review_due", "blocked"}:
            checks.append("missing_review_pressure")
    if case["id"] == "FM-09":
        for item in artifact.get("selected_items", []):
            if item.get("record_kind") == "heavy_review_open" and item.get("review_status") != "accepted" and item.get("pack_role") == "support":
                checks.append("pending_heavy_review_as_support")
    if case["id"] == "FM-12":
        for item in artifact.get("selected_items", []):
            selected_by = item.get("selected_by", {})
            if item.get("pack_role") == "support" and selected_by and not item.get("independent_anchor_ref"):
                checks.append("diagnostic_signal_as_support")
    return sorted(set(checks))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run adversarial Source Intake failure-matrix checks.")
    parser.add_argument("--out-dir", default=str(OUT_DIR), help="Directory for failure matrix CSV/JSON results.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    root = Path(".").resolve()
    registry = contract.load_registry(root)
    rows: list[dict[str, Any]] = []
    for case in FRONTMATTER_CASES:
        checks = run_frontmatter_case(root, registry, case)
        rows.append(
            {
                "id": case["id"],
                "scenario": case["scenario"],
                "expected_check": case["expected_check"],
                "detected_checks": ";".join(checks),
                "blocked": case["expected_check"] in checks,
            }
        )
    for case in RECEIPT_CASES:
        checks = run_receipt_case(case)
        rows.append(
            {
                "id": case["id"],
                "scenario": case["scenario"],
                "expected_check": case["expected_check"],
                "detected_checks": ";".join(checks),
                "blocked": case["expected_check"] in checks,
            }
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "source_intake_failure_matrix_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "scenario", "expected_check", "detected_checks", "blocked"])
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "case_count": len(rows),
        "blocked_count": sum(1 for row in rows if row["blocked"]),
        "status": "pass" if all(row["blocked"] for row in rows) else "fail",
    }
    (out_dir / "source_intake_failure_matrix_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
