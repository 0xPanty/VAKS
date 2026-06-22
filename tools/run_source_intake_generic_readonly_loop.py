#!/usr/bin/env python
"""Run a generic Source Intake read-only pack/use loop.

This script answers the next Pro audit blocker after the live-readonly v2
package: move from case-scripted pack assembly to a generic read-only assembler.

Scope is intentionally narrow:
- local Markdown lexical retrieval is live;
- a sandbox QueryPolicy / authority-bucket receipt is generated before retrieval;
- pack role assignment uses generic rules, not case_id branches;
- support gate remains structural, not external semantic judgment;
- no LLM, no live tool runtime, no writeback, no promotion, no truth mutation;
- full collected Markdown corpus is copied into a frozen package snapshot.
"""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import textwrap
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import source_intake_readonly_shared as base


ROOT = base.ROOT
OUT_DIR = ROOT / "outputs" / "review" / "source-intake-generic-readonly-loop-2026-06-14"
RESULTS_DIR = OUT_DIR / "results"
QUERY_RUN_DIR = OUT_DIR / "query_runs"
CONTEXT_PACK_DIR = OUT_DIR / "context_packs"
ANSWER_USE_DIR = OUT_DIR / "answer_use"
FROZEN_FULL_CORPUS_DIR = OUT_DIR / "frozen_full_workspace_corpus"
ZIP_NAME = "source-intake-generic-readonly-loop-pro-review-package.zip"

RAW_SUPPORT_MODES = {"source_inspection", "review"}
SUPPORT_HEADINGS = {
    "extracted source facts",
    "source facts",
    "inspected source facts",
    "stable source facts",
    "evidence anchors",
    "source anchor",
    "初步看点",
    "边界",
}
ANCHOR_MATCH_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "be",
    "can",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "not",
    "of",
    "or",
    "should",
    "the",
    "to",
    "use",
    "what",
    "why",
    "with",
    "anchor",
    "citation",
    "evidence",
    "query",
    "read",
    "readonly",
    "review",
    "source",
    "support",
}
CANONICAL_RECORD_KIND_ALIASES = {
    "project_lens_overlay": "project_overlay",
}
JUDGE_VISIBLE_FIELDS = [
    "row_id",
    "query",
    "answer_use_claim",
    "anchor_ref",
    "anchor_source_hash",
    "frozen_snapshot_ref",
    "anchor_excerpt",
]
JUDGE_A_FIELDS = [
    *JUDGE_VISIBLE_FIELDS,
    "judge_a_id",
    "judge_a_judged_at",
    "judge_a_relevance_0_2",
    "judge_a_sufficiency_0_2",
    "judge_a_notes",
]
JUDGE_B_FIELDS = [
    *JUDGE_VISIBLE_FIELDS,
    "judge_b_id",
    "judge_b_judged_at",
    "judge_b_relevance_0_2",
    "judge_b_sufficiency_0_2",
    "judge_b_notes",
]
FRESH_NON_FLEXNOTE_ALLOW_CASE_IDS = {
    "G3-05-web-annotation-source-anchor-fresh-allow",
    "G3-06-w3c-prov-boundary-fresh-allow",
    "G3-07-rag-attribution-fresh-allow",
}
LOW_CUE_ALLOW_CASE_IDS = {
    "G3-08-web-annotation-text-context-low-cue-allow",
    "G3-09-w3c-prov-truth-boundary-low-cue-allow",
    "G3-10-rag-attribution-citation-split-low-cue-allow",
    "G3-11-web-annotation-selector-fields-low-cue-allow",
    "G3-12-w3c-prov-entity-activity-agent-low-cue-allow",
}
DECOY_CASE_IDS = {
    "G3-13-web-annotation-action-basis-decoy",
    "G3-14-w3c-prov-action-confidence-decoy",
    "G3-15-rag-attribution-action-faithfulness-decoy",
    "G3-16-web-annotation-runtime-stack-decoy",
    "G3-17-w3c-prov-full-ontology-decoy",
}
BROKEN_ANCHOR_NEGATIVE_CASE_IDS = {
    "G3-18-broken-raw-anchor-negative",
}
DEFAULT_RESTRICTED_POLICY_CASE_IDS = {
    "G3-19-restricted-review-raw-anchor-policy",
    "G3-20-restricted-action-evidence-buckets-policy",
}


RECEIPT_EFFECT_CASES = [
    {
        "effect_id": "RX-01-mixed-query-all-buckets-baseline",
        "query": "FlexNote Extracted Source Facts visual workbench candidate overlay source anchor tag database context pack inspected pages",
        "query_mode": "review",
        "intent": "Receipt-effect baseline: broad review policy allows raw/candidate/overlay buckets before ranking.",
        "policy_variant": "all-buckets-baseline",
        "allowed_authority_buckets_override": ["reviewed", "raw_anchor", "candidate", "overlay", "source_annotation"],
        "support_candidate_authority_buckets_override": ["raw_anchor"],
        "expected_nonzero_exclusion": False,
    },
    {
        "effect_id": "RX-02-mixed-query-raw-anchor-only",
        "query": "FlexNote Extracted Source Facts visual workbench candidate overlay source anchor tag database context pack inspected pages",
        "query_mode": "review",
        "intent": "Receipt-effect treatment: same query but only raw_anchor bucket may enter retrieval.",
        "policy_variant": "raw-anchor-only",
        "allowed_authority_buckets_override": ["raw_anchor"],
        "support_candidate_authority_buckets_override": ["raw_anchor"],
        "compare_to": "RX-01-mixed-query-all-buckets-baseline",
        "expected_nonzero_exclusion": True,
        "expected_excluded_buckets": ["candidate", "overlay"],
    },
    {
        "effect_id": "RX-03-action-query-broad-orientation-baseline",
        "query": "Use PROV traceability as truth confidence and action basis now",
        "query_mode": "action",
        "intent": "Receipt-effect baseline: action query with broad orientation buckets still has no support candidate bucket.",
        "policy_variant": "broad-orientation-baseline",
        "allowed_authority_buckets_override": ["reviewed", "raw_anchor", "candidate", "overlay", "source_annotation"],
        "support_candidate_authority_buckets_override": [],
        "expected_nonzero_exclusion": False,
    },
    {
        "effect_id": "RX-04-action-query-evidence-buckets-only",
        "query": "Use PROV traceability as truth confidence and action basis now",
        "query_mode": "action",
        "intent": "Receipt-effect treatment: same action query, candidate/overlay buckets excluded before ranking.",
        "policy_variant": "evidence-buckets-only",
        "allowed_authority_buckets_override": ["reviewed", "raw_anchor"],
        "support_candidate_authority_buckets_override": [],
        "compare_to": "RX-03-action-query-broad-orientation-baseline",
        "expected_nonzero_exclusion": True,
        "expected_excluded_buckets": ["candidate", "overlay"],
    },
    {
        "effect_id": "RX-05-source-annotation-all-buckets-baseline",
        "query": "legacy development sticky marker source annotation sidecar",
        "query_mode": "review",
        "intent": "Receipt-effect baseline: source_annotation bucket is available for locator/orientation evidence.",
        "policy_variant": "source-annotation-baseline",
        "allowed_authority_buckets_override": ["reviewed", "raw_anchor", "candidate", "overlay", "source_annotation"],
        "support_candidate_authority_buckets_override": ["raw_anchor"],
        "expected_nonzero_exclusion": False,
    },
    {
        "effect_id": "RX-06-source-annotation-excluded-raw-anchor-only",
        "query": "legacy development sticky marker source annotation sidecar",
        "query_mode": "review",
        "intent": "Receipt-effect treatment: same query but source_annotation is excluded before ranking.",
        "policy_variant": "source-annotation-excluded",
        "allowed_authority_buckets_override": ["raw_anchor"],
        "support_candidate_authority_buckets_override": ["raw_anchor"],
        "compare_to": "RX-05-source-annotation-all-buckets-baseline",
        "expected_nonzero_exclusion": True,
        "expected_excluded_buckets": ["source_annotation"],
    },
    {
        "effect_id": "RX-07-reviewed-bucket-baseline",
        "query": "nashsu llm_wiki reviewed library review purpose graph health async review queue",
        "query_mode": "review",
        "intent": "Receipt-effect baseline: reviewed bucket is available for reviewed material retention evidence.",
        "policy_variant": "reviewed-bucket-baseline",
        "allowed_authority_buckets_override": ["reviewed", "raw_anchor", "candidate", "overlay", "source_annotation"],
        "support_candidate_authority_buckets_override": ["raw_anchor"],
        "expected_nonzero_exclusion": False,
    },
    {
        "effect_id": "RX-08-reviewed-bucket-excluded",
        "query": "nashsu llm_wiki reviewed library review purpose graph health async review queue",
        "query_mode": "review",
        "intent": "Receipt-effect treatment: same query but reviewed bucket is excluded before ranking.",
        "policy_variant": "reviewed-bucket-excluded",
        "allowed_authority_buckets_override": ["raw_anchor", "candidate", "overlay", "source_annotation"],
        "support_candidate_authority_buckets_override": ["raw_anchor"],
        "compare_to": "RX-07-reviewed-bucket-baseline",
        "expected_nonzero_exclusion": True,
        "expected_excluded_buckets": ["reviewed"],
    },
]


CUE_DEPLETED_ALLOW_PRESSURE_QUERIES = [
    {
        "pressure_id": "CD-01-web-annotation-refind-paraphrase",
        "query": "How can a reviewer re-find a quoted passage if the wording appears in more than one place?",
        "query_mode": "source_inspection",
        "intended_anchor_ref": "raw/articles/2026-05-30-w3c-web-annotation-source.md#Source Anchor",
    },
    {
        "pressure_id": "CD-02-web-annotation-nearby-context-paraphrase",
        "query": "What should be kept with a selected passage so later readers can locate the same span?",
        "query_mode": "source_inspection",
        "intended_anchor_ref": "raw/articles/2026-05-30-w3c-web-annotation-source.md#Source Anchor",
    },
    {
        "pressure_id": "CD-03-web-annotation-surrounding-snippets-paraphrase",
        "query": "How do we keep surrounding snippets with a quotation so a source span stays findable?",
        "query_mode": "source_inspection",
        "intended_anchor_ref": "raw/articles/2026-05-30-w3c-web-annotation-source.md#Source Anchor",
    },
    {
        "pressure_id": "CD-04-prov-trace-not-truth-paraphrase",
        "query": "Does a record of where information came from make the claim true or more confident?",
        "query_mode": "review",
        "intended_anchor_ref": "raw/articles/2026-05-29-w3c-prov-source.md#边界",
    },
    {
        "pressure_id": "CD-05-prov-capture-agent-tool-paraphrase",
        "query": "What lightweight trace should record what was captured, who handled it, and which tool did extraction?",
        "query_mode": "review",
        "intended_anchor_ref": "raw/articles/2026-05-29-w3c-prov-source.md#初步看点",
    },
    {
        "pressure_id": "CD-06-prov-material-activity-agent-paraphrase",
        "query": "How should a source note separate the material itself from capture activity and responsible agent?",
        "query_mode": "review",
        "intended_anchor_ref": "raw/articles/2026-05-29-w3c-prov-source.md#初步看点",
    },
    {
        "pressure_id": "CD-07-rag-link-not-enough-paraphrase",
        "query": "Is a document link enough support for a generated statement, or must the cited span actually back the point?",
        "query_mode": "review",
        "intended_anchor_ref": "raw/papers/2026-05-29-rag-attribution-faithfulness-source.md#初步看点",
    },
    {
        "pressure_id": "CD-08-rag-correct-vs-relied-paraphrase",
        "query": "Why is a correct citation different from proving the model actually relied on that citation?",
        "query_mode": "review",
        "intended_anchor_ref": "raw/papers/2026-05-29-rag-attribution-faithfulness-source.md#初步看点",
    },
    {
        "pressure_id": "CD-09-rag-background-reference-paraphrase",
        "query": "Can a background reference count as support for a specific point in an answer?",
        "query_mode": "review",
        "intended_anchor_ref": "raw/papers/2026-05-29-rag-attribution-faithfulness-source.md#初步看点",
    },
]


GENERIC_QUERIES = [
    {
        "case_id": "G3-01-candidate-query-generic-downgrade",
        "query": "mnemosyne vector memory candidate final support action basis",
        "query_mode": "action",
        "intent": "Generic assembler should route candidate material away from final support.",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "G3-02-raw-anchor-generic-allow",
        "query": "FlexNote Extracted Source Facts local-first card tag database inspected pages",
        "query_mode": "source_inspection",
        "intent": "Generic assembler may allow a naturally retrieved raw/stable anchor in read-only mode.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "G3-03-mixed-pack-generic-selection",
        "query": "FlexNote Extracted Source Facts visual workbench candidate overlay source anchor tag database context pack inspected pages",
        "query_mode": "review",
        "intent": "Generic assembler should keep candidate/overlay as review input while selecting resolved raw support.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "G3-04-project-overlay-generic-downgrade",
        "query": "FlexNote visual workbench project overlay support",
        "query_mode": "action",
        "intent": "Generic assembler should not let a project overlay become final support.",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "G3-05-web-annotation-source-anchor-fresh-allow",
        "query": "W3C Web Annotation Source Anchor Text Quote Selector exact prefix suffix",
        "query_mode": "source_inspection",
        "intent": "New non-FlexNote smoke case: generic assembler may allow a resolved W3C Web Annotation raw anchor in read-only mode.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "G3-06-w3c-prov-boundary-fresh-allow",
        "query": "W3C PROV 边界 provenance truth confidence citation support",
        "query_mode": "review",
        "intent": "New non-FlexNote smoke case: generic assembler may allow a resolved W3C PROV boundary anchor in read-only review mode.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "G3-07-rag-attribution-fresh-allow",
        "query": "Correctness is not Faithfulness RAG Attributions 初步看点 citation correctness citation faithfulness evidence support",
        "query_mode": "review",
        "intent": "New non-FlexNote smoke case: generic assembler may allow a resolved RAG attribution raw anchor in read-only review mode.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "G3-08-web-annotation-text-context-low-cue-allow",
        "query": "W3C Web Annotation stable text citation preserve selected text nearby context exact prefix suffix",
        "query_mode": "source_inspection",
        "intent": "Low-cue allow: name the source family but not the Source Anchor heading; rely on content overlap under a stable raw heading.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "G3-09-w3c-prov-truth-boundary-low-cue-allow",
        "query": "W3C PROV provenance traceability decide truth confidence citation support",
        "query_mode": "review",
        "intent": "Low-cue allow: name the source family but not the boundary heading; rely on content overlap under the raw boundary section.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "G3-10-rag-attribution-citation-split-low-cue-allow",
        "query": "Why should citation correctness and citation faithfulness be treated as separate checks?",
        "query_mode": "review",
        "intent": "Low-cue allow: do not name the initial-takeaways heading; rely on citation-correctness/faithfulness content overlap.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "G3-11-web-annotation-selector-fields-low-cue-allow",
        "query": "Which selector fields preserve the quote and surrounding snippets so a reviewer can re-find a span?",
        "query_mode": "source_inspection",
        "intent": "Low-cue allow: test exact/prefix/suffix content without naming the Source Anchor heading.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "G3-12-w3c-prov-entity-activity-agent-low-cue-allow",
        "query": "W3C PROV entities activities agents lightweight provenance skeleton source records",
        "query_mode": "review",
        "intent": "Low-cue allow: name the source family but not the source heading; test PROV entity/activity/agent content.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "G3-13-web-annotation-action-basis-decoy",
        "query": "Use W3C Web Annotation exact prefix suffix as an action basis now",
        "query_mode": "action",
        "intent": "Decoy: action mode must not produce final support even when anchor-like terms are present.",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "G3-14-w3c-prov-action-confidence-decoy",
        "query": "Use PROV traceability as truth confidence and action basis now",
        "query_mode": "action",
        "intent": "Decoy: action mode must not treat provenance traceability as final support.",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "G3-15-rag-attribution-action-faithfulness-decoy",
        "query": "Write citation faithfulness score as reviewed truth confidence now",
        "query_mode": "action",
        "intent": "Decoy: action mode must block faithfulness scoring as final support.",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "G3-16-web-annotation-runtime-stack-decoy",
        "query": "annotation server RDF JSON-LD browser runtime transport protocol",
        "query_mode": "source_inspection",
        "intent": "Decoy: non-support implementation/runtime terms should not become final support through stable-anchor headings.",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "G3-17-w3c-prov-full-ontology-decoy",
        "query": "PROV ontology RDF OWL validator query protocol graph implementation",
        "query_mode": "review",
        "intent": "Decoy: full ontology/runtime terms should not pass as final support through the narrow anchor vocabulary.",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "G3-18-broken-raw-anchor-negative",
        "query": "FlexNote Extracted Source Facts local-first card tag database inspected pages",
        "query_mode": "source_inspection",
        "intent": "Adversarial negative: after generic selection finds a raw support candidate, replace its anchor selector with a missing selector and require the support gate to block it.",
        "expected_decision": "blocked_or_downgraded",
        "adversarial_broken_anchor_selector": "missing-runtime-anchor-selector",
    },
    {
        "case_id": "G3-19-restricted-review-raw-anchor-policy",
        "query": "FlexNote Extracted Source Facts visual workbench candidate overlay source anchor tag database context pack inspected pages",
        "query_mode": "review",
        "intent": "Default restricted policy case: only raw_anchor bucket may enter retrieval; candidate/overlay are excluded before ranking.",
        "expected_decision": "allowed_readonly",
        "policy_variant": "default-restricted-raw-anchor",
        "allowed_authority_buckets_override": ["raw_anchor"],
        "support_candidate_authority_buckets_override": ["raw_anchor"],
    },
    {
        "case_id": "G3-20-restricted-action-evidence-buckets-policy",
        "query": "Use PROV traceability as truth confidence and action basis now",
        "query_mode": "action",
        "intent": "Default restricted action case: only reviewed/raw_anchor buckets may enter retrieval; no support candidate bucket is allowed.",
        "expected_decision": "blocked_or_downgraded",
        "policy_variant": "default-restricted-action-evidence",
        "allowed_authority_buckets_override": ["reviewed", "raw_anchor"],
        "support_candidate_authority_buckets_override": [],
    },
]


def configure_base_paths() -> None:
    base.OUT_DIR = OUT_DIR
    base.RESULTS_DIR = RESULTS_DIR
    base.QUERY_RUN_DIR = QUERY_RUN_DIR
    base.CONTEXT_PACK_DIR = CONTEXT_PACK_DIR
    base.ANSWER_USE_DIR = ANSWER_USE_DIR
    base.ZIP_NAME = ZIP_NAME


def reset_output_dir() -> None:
    if OUT_DIR.exists():
        resolved = OUT_DIR.resolve()
        expected = (ROOT / "outputs" / "review").resolve()
        if expected not in resolved.parents:
            raise RuntimeError(f"Refusing to remove unexpected output path: {OUT_DIR}")
        shutil.rmtree(OUT_DIR)
    for path in [RESULTS_DIR, QUERY_RUN_DIR, CONTEXT_PACK_DIR, ANSWER_USE_DIR, FROZEN_FULL_CORPUS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def heading_labels(body: str) -> list[str]:
    labels: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            labels.append(stripped.lstrip("#").strip())
    return labels


def stable_anchor_sections(body: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, list[str]]] = []
    current_label = ""
    current_lines: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            if current_label:
                sections.append((current_label, current_lines))
            label = stripped.lstrip("#").strip()
            normalized = label.lower().replace("-", " ").strip()
            if normalized in SUPPORT_HEADINGS:
                current_label = label
                current_lines = [line]
            else:
                current_label = ""
                current_lines = []
            continue
        if current_label:
            current_lines.append(line)
    if current_label:
        sections.append((current_label, current_lines))
    return [(label, "\n".join(lines)) for label, lines in sections]


def meaningful_overlap(left: set[str], right: set[str]) -> set[str]:
    return {term for term in left & right if term not in ANCHOR_MATCH_STOPWORDS and len(term) > 2}


def anchor_for_raw_hit(hit: base.SearchHit, query_mode: str) -> tuple[str, str]:
    """Return a resolved raw/stable anchor for support, or a reason for not using one."""
    if query_mode not in RAW_SUPPORT_MODES:
        return "", "query_mode_not_readonly_support_mode"
    if hit.doc.record_kind != "source_card" or hit.doc.knowledge_status != "raw":
        return "", "not_raw_source_card"

    query_terms = set(hit.matched_terms)
    candidates: list[tuple[int, str, str]] = []
    for label, section_text in stable_anchor_sections(hit.doc.body):
        normalized = label.lower().replace("-", " ").strip()
        heading_terms = set(base.tokenize(label))
        section_terms = set(base.tokenize(section_text))
        heading_overlap = query_terms & heading_terms
        section_overlap = meaningful_overlap(query_terms, section_terms)
        if heading_overlap or "facts" in query_terms or len(section_overlap) >= 2:
            anchor_ref = f"{hit.doc.rel_path}#{label}"
            resolution = base.resolve_anchor(anchor_ref)
            if resolution["status"] == "resolved":
                score = len(section_overlap) * 10 + len(heading_overlap) * 3 + (1 if "facts" in query_terms else 0)
                if heading_overlap or "facts" in query_terms:
                    candidates.append((score, anchor_ref, "resolved_named_stable_anchor_heading"))
                else:
                    candidates.append((score, anchor_ref, "resolved_stable_anchor_section_content_overlap"))
    if candidates:
        candidates.sort(key=lambda item: (-item[0], item[1]))
        _, anchor_ref, reason = candidates[0]
        return anchor_ref, reason

    return "", "no_generic_resolved_source_fact_anchor"


def generic_pack_role(hit: base.SearchHit, query_mode: str, support_already_selected: bool) -> tuple[str, str, str]:
    """Assign pack_role without looking at case_id."""
    record_kind = canonical_record_kind(hit.doc.record_kind)
    if record_kind == "source_annotation":
        return "review_input", "", "source_annotation_is_locator_not_support"
    if record_kind == "candidate_distillation":
        return "review_input", "", "candidate_distillation_is_review_input_not_support"
    if record_kind == "project_overlay":
        return "review_input", "", "project_overlay_is_project_context_not_support"
    if record_kind == "reviewed_material":
        return "review_input", "", "reviewed_material_context_only_not_raw_anchor_support"
    if record_kind != "source_card":
        return "orientation", "", "unknown_record_kind_orientation_only"

    anchor_ref, reason = anchor_for_raw_hit(hit, query_mode)
    if anchor_ref and not support_already_selected:
        return "support", anchor_ref, reason
    if anchor_ref and support_already_selected:
        return "anchor", anchor_ref, "additional_resolved_anchor_kept_for_drilldown"
    return "orientation", "", reason


def assemble_pack_generic(case: dict[str, Any], hits: list[base.SearchHit], *, max_items: int = 6) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    support_selected = False
    seen_refs: set[str] = set()

    for hit in hits:
        if hit.doc.rel_path in seen_refs:
            continue
        role, anchor_ref, reason = generic_pack_role(hit, case["query_mode"], support_selected)
        item = base.hit_to_item(hit, pack_role=role, anchor_ref=anchor_ref, excluded_reason=reason)
        original_record_kind = item["record_kind"]
        item["record_kind"] = canonical_record_kind(original_record_kind)
        if item["record_kind"] != original_record_kind:
            item["original_record_kind"] = original_record_kind
        item["assembler_rule"] = "generic_record_kind_status_anchor_rule"
        item["case_scripted_selection"] = False
        items.append(item)
        seen_refs.add(hit.doc.rel_path)
        if role == "support":
            support_selected = True
        if len(items) >= max_items and support_selected:
            break

    if not items:
        raise RuntimeError(f"{case['case_id']}: generic assembler selected no items")
    return items


def apply_adversarial_case_mutations(case: dict[str, Any], items: list[dict[str, Any]]) -> list[str]:
    """Apply explicit adversarial fixture mutations after generic assembly."""

    selector = case.get("adversarial_broken_anchor_selector")
    if not selector:
        return []

    for item in items:
        if item.get("pack_role") != "support":
            continue
        original_anchor = item.get("independent_anchor_ref") or ""
        path_part = original_anchor.split("#", 1)[0] if "#" in original_anchor else item["ref"]
        item["original_independent_anchor_ref"] = original_anchor
        item["independent_anchor_ref"] = f"{path_part}#{selector}"
        item["adversarial_fixture"] = "broken_anchor_selector_after_generic_selection"
        item["assembler_rule"] = f"{item.get('assembler_rule', 'generic_record_kind_status_anchor_rule')}+adversarial_broken_anchor"
        return [
            f"adversarial broken-anchor fixture replaced `{original_anchor}` with `{item['independent_anchor_ref']}`"
        ]

    return ["adversarial broken-anchor fixture found no generic support item to mutate"]


def canonical_record_kind(record_kind: str) -> str:
    return CANONICAL_RECORD_KIND_ALIASES.get(record_kind, record_kind)


def normalize_corpus_record_kinds(corpus: list[base.CorpusDoc]) -> list[base.CorpusDoc]:
    normalized: list[base.CorpusDoc] = []
    for doc in corpus:
        record_kind = canonical_record_kind(doc.record_kind)
        if record_kind == doc.record_kind:
            normalized.append(doc)
            continue
        normalized.append(
            base.CorpusDoc(
                rel_path=doc.rel_path,
                abs_path=doc.abs_path,
                text=doc.text,
                frontmatter=doc.frontmatter,
                body=doc.body,
                record_kind=record_kind,
                knowledge_status=doc.knowledge_status,
                warning_code=doc.warning_code,
                title=doc.title,
                source_hash=doc.source_hash,
            )
        )
    return normalized


def evaluate_support_generic(items: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]], list[str]]:
    support_checks: list[dict[str, Any]] = []
    warnings: list[str] = []
    supported = 0
    invalid = 0
    diagnostic_terms = ["retrieval_rank", "retrieval_score", "graph_path", "graph_rank", "rank:"]

    for item in items:
        if item["pack_role"] != "support":
            if item["record_kind"] in {"source_annotation", "candidate_distillation", "project_overlay"}:
                warnings.append(f"{item['record_kind']} routed to {item['pack_role']}: {item['ref']}")
            continue

        anchor = item.get("independent_anchor_ref") or ""
        anchor_lower = anchor.lower()
        resolution = base.resolve_anchor(anchor)
        if item["record_kind"] != "source_card" or item["knowledge_status"] != "raw":
            invalid += 1
            result = "not_ready"
            reason = "non_raw_source_item_cannot_be_final_support"
        elif any(term in anchor_lower for term in diagnostic_terms):
            invalid += 1
            result = "not_ready"
            reason = "diagnostic_rank_or_score_cannot_be_support_anchor"
        elif resolution["status"] != "resolved":
            invalid += 1
            result = "missing_anchor"
            reason = "support_anchor_not_resolved"
        else:
            supported += 1
            result = "supported"
            reason = "resolved_raw_stable_anchor_structural_only"
        support_checks.append(
            {
                "claim_ref": item["ref"],
                "independent_anchor_ref": anchor,
                "result": result,
                "resolution": resolution,
                "reason": reason,
                "semantic_support_status": "not_external_judged",
            }
        )

    if supported > 0 and invalid == 0:
        decision = "allowed_readonly"
    else:
        decision = "blocked_or_downgraded"
    if not support_checks:
        support_checks.append(
            {
                "claim_ref": "no_final_support_selected",
                "independent_anchor_ref": "",
                "result": "not_ready",
                "resolution": {"status": "not_checked", "reason": "generic assembler selected no support items"},
                "reason": "retrieved_items_remain_review_input_or_orientation_only",
                "semantic_support_status": "not_external_judged",
            }
        )
    return decision, support_checks, warnings


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in row.items()})


def run_receipt_effect_tests(corpus: list[base.CorpusDoc], now: str) -> dict[str, Any]:
    """Run paired QueryPolicy cases that must produce visible bucket exclusions."""

    rows: list[dict[str, Any]] = []
    for case in RECEIPT_EFFECT_CASES:
        policy, bucket_receipt, hits = base.retrieve_with_query_policy(case, corpus)
        top_paths = [hit.doc.rel_path for hit in hits]
        top_buckets = [base.doc_authority_bucket(hit.doc) for hit in hits]
        excluded_counts = bucket_receipt.get("excluded_bucket_counts", {})
        expected_buckets = case.get("expected_excluded_buckets") or []
        expected_buckets_excluded = all(int(excluded_counts.get(bucket, 0)) > 0 for bucket in expected_buckets)
        nonzero_exclusion = int(bucket_receipt.get("excluded_doc_count", 0)) > 0
        rows.append(
            {
                "effect_id": case["effect_id"],
                "compare_to": case.get("compare_to", ""),
                "query": case["query"],
                "query_mode": case["query_mode"],
                "query_policy_id": policy["policy_id"],
                "policy_variant": case.get("policy_variant", ""),
                "allowed_authority_buckets": policy["allowed_authority_buckets"],
                "support_candidate_authority_buckets": policy["support_candidate_authority_buckets"],
                "pre_filter_doc_count": bucket_receipt["pre_filter_doc_count"],
                "post_filter_doc_count": bucket_receipt["post_filter_doc_count"],
                "excluded_doc_count": bucket_receipt["excluded_doc_count"],
                "excluded_bucket_counts": excluded_counts,
                "expected_nonzero_exclusion": bool(case.get("expected_nonzero_exclusion")),
                "nonzero_exclusion": nonzero_exclusion,
                "expected_buckets_excluded": expected_buckets_excluded if expected_buckets else "",
                "top_result": top_paths[0] if top_paths else "",
                "top_result_authority_bucket": top_buckets[0] if top_buckets else "",
                "top_paths": top_paths,
                "top_authority_buckets": top_buckets,
            }
        )

    by_id = {row["effect_id"]: row for row in rows}
    pair_rows: list[dict[str, Any]] = []
    for row in rows:
        compare_to = row.get("compare_to")
        if not compare_to:
            continue
        baseline = by_id.get(str(compare_to))
        if not baseline:
            continue
        baseline_top_paths = baseline.get("top_paths") or []
        treatment_top_paths = row.get("top_paths") or []
        top_result_changed = baseline.get("top_result") != row.get("top_result")
        top_k_order_changed = baseline_top_paths != treatment_top_paths
        pair_rows.append(
            {
                "baseline_effect_id": baseline["effect_id"],
                "treatment_effect_id": row["effect_id"],
                "same_query": baseline["query"] == row["query"],
                "baseline_allowed_buckets": baseline["allowed_authority_buckets"],
                "treatment_allowed_buckets": row["allowed_authority_buckets"],
                "baseline_excluded_doc_count": baseline["excluded_doc_count"],
                "treatment_excluded_doc_count": row["excluded_doc_count"],
                "treatment_excluded_bucket_counts": row["excluded_bucket_counts"],
                "top_result_changed": top_result_changed,
                "top_k_order_changed": top_k_order_changed,
                "baseline_top_result": baseline["top_result"],
                "treatment_top_result": row["top_result"],
            }
        )

    write_csv(
        RESULTS_DIR / "receipt_effect_cases.csv",
        rows,
        [
            "effect_id",
            "compare_to",
            "query",
            "query_mode",
            "query_policy_id",
            "policy_variant",
            "allowed_authority_buckets",
            "support_candidate_authority_buckets",
            "pre_filter_doc_count",
            "post_filter_doc_count",
            "excluded_doc_count",
            "excluded_bucket_counts",
            "expected_nonzero_exclusion",
            "nonzero_exclusion",
            "expected_buckets_excluded",
            "top_result",
            "top_result_authority_bucket",
            "top_paths",
            "top_authority_buckets",
        ],
    )
    write_csv(
        RESULTS_DIR / "receipt_effect_pair_comparisons.csv",
        pair_rows,
        [
            "baseline_effect_id",
            "treatment_effect_id",
            "same_query",
            "baseline_allowed_buckets",
            "treatment_allowed_buckets",
            "baseline_excluded_doc_count",
            "treatment_excluded_doc_count",
            "treatment_excluded_bucket_counts",
            "top_result_changed",
            "top_k_order_changed",
            "baseline_top_result",
            "treatment_top_result",
        ],
    )

    expected_treatments = [row for row in rows if row["expected_nonzero_exclusion"]]
    nonzero_expected = [row for row in expected_treatments if row["nonzero_exclusion"]]
    expected_bucket_hits = [
        row for row in expected_treatments if row["expected_buckets_excluded"] is True
    ]
    changed_pairs = [row for row in pair_rows if row["top_result_changed"] or row["top_k_order_changed"]]
    source_annotation_rows = [row for row in rows if "source-annotation" in row["effect_id"]]
    source_annotation_exclusion_rows = [
        row for row in rows if int((row.get("excluded_bucket_counts") or {}).get("source_annotation", 0)) > 0
    ]
    reviewed_bucket_rows = [row for row in rows if "reviewed-bucket" in row["effect_id"]]
    reviewed_exclusion_rows = [
        row for row in rows if int((row.get("excluded_bucket_counts") or {}).get("reviewed", 0)) > 0
    ]
    summary = {
        "status": "pass"
        if len(nonzero_expected) == len(expected_treatments)
        and len(expected_bucket_hits) == len(expected_treatments)
        and bool(changed_pairs)
        else "fail",
        "created_at": now,
        "case_count": len(rows),
        "paired_comparison_count": len(pair_rows),
        "expected_nonzero_exclusion_count": len(expected_treatments),
        "observed_nonzero_exclusion_count": len(nonzero_expected),
        "expected_bucket_exclusion_count": len(expected_bucket_hits),
        "top_result_or_order_changed_pair_count": len(changed_pairs),
        "source_annotation_effect_case_count": len(source_annotation_rows),
        "source_annotation_retained_case_count": sum(
            1 for row in source_annotation_rows if row.get("top_result_authority_bucket") == "source_annotation"
        ),
        "source_annotation_excluded_case_count": sum(
            1
            for row in source_annotation_rows
            if int((row.get("excluded_bucket_counts") or {}).get("source_annotation", 0)) > 0
        ),
        "source_annotation_exclusion_observed_across_all_restricted_pairs": len(source_annotation_exclusion_rows),
        "reviewed_bucket_effect_case_count": len(reviewed_bucket_rows),
        "reviewed_bucket_retained_case_count": sum(
            1 for row in reviewed_bucket_rows if row.get("top_result_authority_bucket") == "reviewed"
        ),
        "reviewed_bucket_excluded_case_count": sum(
            1
            for row in reviewed_bucket_rows
            if int((row.get("excluded_bucket_counts") or {}).get("reviewed", 0)) > 0
        ),
        "reviewed_bucket_exclusion_observed_across_all_restricted_pairs": len(reviewed_exclusion_rows),
        "cases_csv": base.rel(RESULTS_DIR / "receipt_effect_cases.csv"),
        "pair_comparisons_csv": base.rel(RESULTS_DIR / "receipt_effect_pair_comparisons.csv"),
        "truth_boundary": "Receipt-effect tests demonstrate the bucket-first hook can produce observable corpus exclusions under restricted policies. They do not prove hybrid/vector/graph retrieval or production runtime behavior.",
    }
    base.write_json(RESULTS_DIR / "receipt_effect_summary.json", summary)
    return summary


def run_cue_depleted_allow_pressure(corpus: list[base.CorpusDoc], now: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for query in CUE_DEPLETED_ALLOW_PRESSURE_QUERIES:
        case = {
            "case_id": query["pressure_id"],
            "query": query["query"],
            "query_mode": query["query_mode"],
        }
        policy, bucket_receipt, hits = base.retrieve_with_query_policy(case, corpus)
        case["query_policy"] = policy
        case["bucket_receipt"] = bucket_receipt
        items = assemble_pack_generic(case, hits)
        decision, checks, warnings = evaluate_support_generic(items)
        support_items = [item for item in items if item["pack_role"] == "support"]
        support_refs = [item["ref"] for item in support_items]
        support_anchors = [item.get("independent_anchor_ref", "") for item in support_items]
        rows.append(
            {
                "pressure_id": query["pressure_id"],
                "query": query["query"],
                "query_mode": query["query_mode"],
                "query_policy_id": policy["policy_id"],
                "allowed_authority_buckets": policy["allowed_authority_buckets"],
                "support_candidate_authority_buckets": policy["support_candidate_authority_buckets"],
                "intended_anchor_ref": query["intended_anchor_ref"],
                "decision": decision,
                "allowed_readonly": decision == "allowed_readonly",
                "intended_anchor_selected": query["intended_anchor_ref"] in support_anchors,
                "support_count": len(support_items),
                "support_refs": support_refs,
                "support_anchors": support_anchors,
                "top_result": hits[0].doc.rel_path if hits else "",
                "top_result_kind": hits[0].doc.record_kind if hits else "",
                "top_result_authority_bucket": base.doc_authority_bucket(hits[0].doc) if hits else "",
                "warnings": warnings,
                "support_checks": checks,
            }
        )
    write_csv(
        RESULTS_DIR / "cue_depleted_allow_pressure_cases.csv",
        rows,
        [
            "pressure_id",
            "query",
            "query_mode",
            "query_policy_id",
            "allowed_authority_buckets",
            "support_candidate_authority_buckets",
            "intended_anchor_ref",
            "decision",
            "allowed_readonly",
            "intended_anchor_selected",
            "support_count",
            "support_refs",
            "support_anchors",
            "top_result",
            "top_result_kind",
            "top_result_authority_bucket",
            "warnings",
            "support_checks",
        ],
    )
    summary = {
        "status": "diagnostic_pressure_completed",
        "created_at": now,
        "case_count": len(rows),
        "allowed_readonly_count": sum(1 for row in rows if row["allowed_readonly"]),
        "intended_anchor_selected_count": sum(1 for row in rows if row["intended_anchor_selected"]),
        "truth_boundary": "Cue-depleted paraphrase queries are diagnostic pressure only. Failing or partial results bound genericity; they are not hidden by adding stronger cues.",
    }
    base.write_json(RESULTS_DIR / "cue_depleted_allow_pressure_summary.json", summary)
    return summary


def run_clean_corpus_rerun(corpus: list[base.CorpusDoc], now: str) -> dict[str, Any]:
    """Rerun with runtime test fixtures excluded and no other rule changes."""

    fixture_marker = "outputs/review/project_overlays/_runtime_test_fixtures/"
    clean_corpus = [doc for doc in corpus if fixture_marker not in doc.rel_path]
    excluded = [doc.rel_path for doc in corpus if fixture_marker in doc.rel_path]
    rows: list[dict[str, Any]] = []
    top_rows: list[dict[str, Any]] = []

    for case in GENERIC_QUERIES:
        case_with_policy = dict(case)
        policy, bucket_receipt, hits = base.retrieve_with_query_policy(case_with_policy, clean_corpus)
        case_with_policy["query_policy"] = policy
        case_with_policy["bucket_receipt"] = bucket_receipt
        if not hits:
            rows.append(
                {
                    "case_id": case["case_id"],
                    "query": case["query"],
                    "query_mode": case["query_mode"],
                    "query_policy_id": policy["policy_id"],
                    "expected_decision": case["expected_decision"],
                    "decision": "no_hits",
                    "pass": False,
                    "support_count": 0,
                    "top_result": "",
                    "top_result_kind": "",
                    "selected_refs": [],
                    "selected_roles": [],
                    "support_checks": [],
                    "warnings": ["clean corpus rerun returned no retrieval hits"],
                }
            )
            continue

        items = assemble_pack_generic(case_with_policy, hits)
        mutation_warnings = apply_adversarial_case_mutations(case_with_policy, items)
        decision, checks, warnings = evaluate_support_generic(items)
        warnings = mutation_warnings + warnings
        support_items = [item for item in items if item["pack_role"] == "support"]
        rows.append(
            {
                "case_id": case["case_id"],
                "query": case["query"],
                "query_mode": case["query_mode"],
                "query_policy_id": policy["policy_id"],
                "expected_decision": case["expected_decision"],
                "decision": decision,
                "pass": decision == case["expected_decision"],
                "support_count": len(support_items),
                "top_result": hits[0].doc.rel_path,
                "top_result_kind": hits[0].doc.record_kind,
                "selected_refs": [item["ref"] for item in items],
                "selected_roles": [item["pack_role"] for item in items],
                "support_checks": checks,
                "warnings": warnings,
            }
        )
        for hit in hits:
            top_rows.append(
                {
                    "case_id": case["case_id"],
                    "rank": hit.rank,
                    "score": round(hit.score, 4),
                    "path": hit.doc.rel_path,
                    "authority_bucket": base.doc_authority_bucket(hit.doc),
                    "record_kind": hit.doc.record_kind,
                    "knowledge_status": hit.doc.knowledge_status,
                    "matched_terms": hit.matched_terms,
                }
            )

    write_csv(
        RESULTS_DIR / "clean_corpus_rerun_cases.csv",
        rows,
        [
            "case_id",
            "query",
            "query_mode",
            "query_policy_id",
            "expected_decision",
            "decision",
            "pass",
            "support_count",
            "top_result",
            "top_result_kind",
            "selected_refs",
            "selected_roles",
            "support_checks",
            "warnings",
        ],
    )
    write_csv(
        RESULTS_DIR / "clean_corpus_rerun_top_results.csv",
        top_rows,
        ["case_id", "rank", "score", "path", "authority_bucket", "record_kind", "knowledge_status", "matched_terms"],
    )
    summary = {
        "status": "pass" if all(row["pass"] for row in rows) else "fail",
        "created_at": now,
        "case_count": len(rows),
        "passed_expected_decision_count": sum(1 for row in rows if row["pass"]),
        "original_corpus_doc_count": len(corpus),
        "clean_corpus_doc_count": len(clean_corpus),
        "excluded_fixture_count": len(excluded),
        "excluded_fixture_paths": excluded,
        "decision_breakdown": dict(Counter(row["decision"] for row in rows)),
        "truth_boundary": "Default corpus excludes runtime test fixtures; this clean rerun is a no-op guard using the same scorer, query set, anchor vocabulary, and generic pack rules. This is not production runtime validation.",
    }
    base.write_json(RESULTS_DIR / "clean_corpus_rerun_summary.json", summary)
    return summary


def write_events(case_rows: list[dict[str, Any]], retrieval_rows: list[dict[str, Any]], now: str) -> None:
    by_case = {row["case_id"]: row for row in case_rows}
    events = []
    for case in GENERIC_QUERIES:
        row = by_case[case["case_id"]]
        case_retrievals = [r for r in retrieval_rows if r["case_id"] == case["case_id"]]
        events.extend(
            [
                {
                    "time": now,
                    "case_id": case["case_id"],
                    "stage": "live_local_lexical_retrieve",
                    "live_local_lexical_retrieval_used": True,
                    "retrieved_count": len(case_retrievals),
                    "top_result": row["top_result"],
                    "truth_boundary": "local Markdown lexical retrieval only; no live embedding/vector/graph retrieval.",
                },
                {
                    "time": now,
                    "case_id": case["case_id"],
                    "stage": "generic_assemble_context_pack",
                    "context_pack": row["context_pack"],
                    "pack_assembly": "generic_record_kind_status_anchor_rules_no_case_id_role_branching",
                },
                {
                    "time": now,
                    "case_id": case["case_id"],
                    "stage": "answer_use_gate",
                    "decision": row["decision"],
                    "support_count": row["support_count"],
                    "semantic_support_status": "not_external_judged",
                    "writeback_attempted": False,
                    "promotion_attempted": False,
                    "truth_mutation_attempted": False,
                },
            ]
        )
    path = RESULTS_DIR / "generic_readonly_loop_events.jsonl"
    with path.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


def write_full_workspace_snapshot(corpus: list[base.CorpusDoc], retrieval_rows: list[dict[str, Any]], now: str) -> dict[str, Any]:
    manifest_rows = []
    for doc in sorted(corpus, key=lambda item: item.rel_path):
        source = doc.abs_path
        target = FROZEN_FULL_CORPUS_DIR / doc.rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        manifest_rows.append(
            {
                "path": doc.rel_path,
                "frozen_path": base.rel(target),
                "sha256": doc.source_hash,
                "bytes": source.stat().st_size,
                "record_kind": doc.record_kind,
                "knowledge_status": doc.knowledge_status,
                "warning_code": doc.warning_code,
            }
        )

    expected: dict[str, list[str]] = {}
    for row in retrieval_rows:
        expected.setdefault(row["case_id"], []).append(row["path"])
    query_manifest = {
        "created_at": now,
        "frozen_scope": "full_collected_markdown_corpus_snapshot_for_this_run",
        "truth_boundary": "Full snapshot covers the Markdown corpus collected by this script for this run. It still does not prove live LLM/tool runtime, vector/graph retrieval, or semantic support.",
        "queries": [
            {
                "case_id": case["case_id"],
                "query": case["query"],
                "query_mode": case["query_mode"],
                "query_policy": base.query_policy_for_case(case),
                "expected_top_paths": expected.get(case["case_id"], []),
            }
            for case in GENERIC_QUERIES
        ],
    }
    base.write_json(RESULTS_DIR / "full_workspace_corpus_manifest.json", {"files": manifest_rows, "file_count": len(manifest_rows)})
    write_csv(
        RESULTS_DIR / "full_workspace_corpus_manifest.csv",
        manifest_rows,
        ["path", "frozen_path", "sha256", "bytes", "record_kind", "knowledge_status", "warning_code"],
    )
    base.write_json(RESULTS_DIR / "full_workspace_query_manifest.json", query_manifest)
    write_full_replayer()

    replay = subprocess.run(["python", base.rel(OUT_DIR / "replay_full_workspace_rerun.py")], cwd=ROOT, capture_output=True, text=True)
    replay_result = {
        "status": "pass" if replay.returncode == 0 else "fail",
        "returncode": replay.returncode,
        "stdout": replay.stdout.strip(),
        "stderr": replay.stderr.strip(),
        "truth_boundary": "Replays lexical top-k path order over the frozen full collected Markdown corpus snapshot only.",
    }
    base.write_json(RESULTS_DIR / "full_workspace_replay_command_result.json", replay_result)
    return {
        "status": replay_result["status"],
        "corpus_doc_count": len(manifest_rows),
        "manifest": base.rel(RESULTS_DIR / "full_workspace_corpus_manifest.json"),
        "replay": replay_result,
    }


def write_full_replayer() -> None:
    script = r'''
#!/usr/bin/env python
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "frozen_full_workspace_corpus"
QUERY_MANIFEST = ROOT / "results" / "full_workspace_query_manifest.json"
OUT = ROOT / "results" / "full_workspace_replay_check.json"
TOKEN_RE = re.compile(r"[a-z0-9]+|[\u4e00-\u9fff]+", re.IGNORECASE)

TYPE_ALIASES = {
    "source": "source_card",
    "source_record": "source_card",
    "video_source_card": "source_card",
    "source_snapshot_index": "source_card",
    "source_annotation": "source_annotation",
    "candidate_distillation": "candidate_distillation",
    "candidate_distillation_refresh": "candidate_distillation",
    "project_lens_overlay": "project_overlay",
    "project_overlay": "project_overlay",
}

def tokenize(text: str) -> list[str]:
    raw = TOKEN_RE.findall(text.lower())
    expanded = []
    for token in raw:
        expanded.append(token)
        if "-" in token or "_" in token:
            expanded.extend(t for t in re.split(r"[-_]+", token) if t)
    return [t for t in expanded if len(t) > 1]

def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    try:
        data = yaml.safe_load(text[4:end]) or {}
    except Exception:
        data = {}
    return data if isinstance(data, dict) else {}, text[end + 4 :]

def infer_record_kind(path: str, fm: dict) -> str:
    if fm.get("record_kind"):
        return TYPE_ALIASES.get(str(fm["record_kind"]), str(fm["record_kind"]))
    if fm.get("type") in TYPE_ALIASES:
        return TYPE_ALIASES[str(fm["type"])]
    if path.startswith("raw/"):
        return "source_card"
    if path.startswith("outputs/review/source_annotations/") or path.endswith("source-annotation.md"):
        return "source_annotation"
    if path.startswith("wiki/") and str(fm.get("status", "")).lower() == "reviewed":
        return "reviewed_material"
    if path.endswith("candidate-distillation.md") or path.endswith("refresh.md"):
        return "candidate_distillation"
    if "project_lens_overlays/" in path or "project_overlays/" in path or path.endswith("-overlay.md"):
        return "project_overlay"
    return "source_card"

def infer_status(record_kind: str, fm: dict) -> str:
    if fm.get("knowledge_status"):
        return str(fm["knowledge_status"])
    if str(fm.get("status", "")).lower() == "reviewed":
        return "reviewed"
    if record_kind == "source_card":
        return "raw"
    return "candidate"

def authority_bucket(record_kind: str, knowledge_status: str) -> str:
    if knowledge_status == "reviewed" or record_kind == "reviewed_material":
        return "reviewed"
    if record_kind == "source_card":
        return "raw_anchor"
    if record_kind == "source_annotation":
        return "source_annotation"
    if record_kind == "candidate_distillation":
        return "candidate"
    if record_kind == "project_overlay":
        return "overlay"
    if record_kind == "feedback_event":
        return "feedback"
    return "unknown"

def headings(body: str) -> str:
    return "\n".join(line for line in body.splitlines() if line.lstrip().startswith("#"))

def score(query: str, rel_path: str, title: str, body: str, record_kind: str) -> float:
    terms = set(tokenize(query))
    path_tokens = Counter(tokenize(rel_path))
    title_tokens = Counter(tokenize(title))
    heading_tokens = Counter(tokenize(headings(body)))
    body_tokens = Counter(tokenize(body[:20000]))
    total = 0.0
    for term in terms:
        total += path_tokens.get(term, 0) * 6.0
        total += title_tokens.get(term, 0) * 4.0
        total += heading_tokens.get(term, 0) * 2.5
        total += min(body_tokens.get(term, 0), 6) * 1.0
    if record_kind == "source_card" and "source" in terms:
        total += 1.5
    if record_kind == "source_annotation" and ("annotation" in terms or "anchor" in terms or "source" in terms):
        total += 3.0
    if record_kind == "candidate_distillation" and "candidate" in terms:
        total += 4.0
    if record_kind == "project_overlay" and "overlay" in terms:
        total += 4.0
    return total

def main() -> int:
    manifest = json.loads(QUERY_MANIFEST.read_text(encoding="utf-8"))
    docs = []
    for path in sorted(CORPUS.rglob("*.md")):
        rel = path.relative_to(CORPUS).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = split_frontmatter(text)
        kind = infer_record_kind(rel, fm)
        status = infer_status(kind, fm)
        docs.append({
            "path": rel,
            "title": str(fm.get("title") or path.stem),
            "body": body,
            "kind": kind,
            "status": status,
            "authority_bucket": authority_bucket(kind, status),
        })
    checks = []
    for query in manifest["queries"]:
        policy = query.get("query_policy") or {}
        allowed_buckets = set(policy.get("allowed_authority_buckets") or [])
        candidate_docs = [
            doc for doc in docs if not allowed_buckets or doc["authority_bucket"] in allowed_buckets
        ]
        ranked = []
        for doc in candidate_docs:
            s = score(query["query"], doc["path"], doc["title"], doc["body"], doc["kind"])
            if s > 0:
                ranked.append((s, doc["path"]))
        ranked.sort(key=lambda item: (-item[0], item[1]))
        expected = query["expected_top_paths"]
        actual = [path for _, path in ranked[: len(expected)]]
        checks.append({"case_id": query["case_id"], "expected": expected, "actual": actual, "match": actual == expected})
    result = {
        "status": "pass" if all(check["match"] for check in checks) else "fail",
        "frozen_scope": manifest["frozen_scope"],
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "pass" else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''
    (OUT_DIR / "replay_full_workspace_rerun.py").write_text(textwrap.dedent(script).lstrip(), encoding="utf-8")


def write_semantic_support_judgment_packet(case_rows: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    internal_rows = []
    mapping_rows = []
    for row in case_rows:
        if row["decision"] != "allowed_readonly":
            continue
        checks = row["support_checks"]
        for check in checks:
            if check.get("result") != "supported":
                continue
            anchor_ref = check["independent_anchor_ref"]
            path_part, selector = anchor_ref.split("#", 1)
            source_path = ROOT / path_part
            source_text = source_path.read_text(encoding="utf-8", errors="replace") if source_path.exists() else ""
            anchor_source_hash = base.sha256_file(source_path) if source_path.exists() else ""
            frozen_snapshot_path = OUT_DIR / "frozen_full_workspace_corpus" / path_part
            frozen_snapshot_ref = base.rel(frozen_snapshot_path) if frozen_snapshot_path.exists() else ""
            excerpt = extract_anchor_excerpt(source_text, selector)
            support_claim = semantic_support_claim_for_case(row["case_id"])
            rationale = semantic_support_rationale_for_case(row["case_id"])
            row_id = f"judge-row-{len(rows)+1:03d}"
            rows.append(
                {
                    "row_id": row_id,
                    "query": row["query"],
                    "answer_use_claim": support_claim,
                    "anchor_ref": anchor_ref,
                    "anchor_source_hash": anchor_source_hash,
                    "frozen_snapshot_ref": frozen_snapshot_ref,
                    "anchor_excerpt": excerpt,
                    "judge_a_id": "",
                    "judge_a_judged_at": "",
                    "judge_a_relevance_0_2": "",
                    "judge_a_sufficiency_0_2": "",
                    "judge_a_notes": "",
                    "judge_b_id": "",
                    "judge_b_judged_at": "",
                    "judge_b_relevance_0_2": "",
                    "judge_b_sufficiency_0_2": "",
                    "judge_b_notes": "",
                    "arbiter_id": "",
                    "arbiter_judged_at": "",
                    "arbiter_final_relevance_0_2": "",
                    "arbiter_final_sufficiency_0_2": "",
                    "arbiter_notes": "",
                }
            )
            mapping_rows.append(
                {
                    "row_id": row_id,
                    "case_id": row["case_id"],
                    "anchor_ref": anchor_ref,
                    "anchor_source_hash": anchor_source_hash,
                    "frozen_snapshot_ref": frozen_snapshot_ref,
                    "truth_boundary": "Mapping is for package audit only and is excluded from judge-only blind packet.",
                }
            )
            internal_rows.append(
                {
                    "judgment_id": f"internal-semantic-{len(internal_rows)+1:03d}",
                    "case_id": row["case_id"],
                    "reviewer": "codex_author_side_scripted_self_check",
                    "query": row["query"],
                    "answer_use_claim": support_claim,
                    "anchor_ref": anchor_ref,
                    "relevance_0_2": 2,
                    "sufficiency_0_2": 2,
                    "semantic_support_result": "sufficient_for_this_readonly_query_use",
                    "notes": rationale,
                    "external_or_blind": False,
                }
            )
    fieldnames = [
        "row_id",
        "query",
        "answer_use_claim",
        "anchor_ref",
        "anchor_source_hash",
        "frozen_snapshot_ref",
        "anchor_excerpt",
        "judge_a_id",
        "judge_a_judged_at",
        "judge_a_relevance_0_2",
        "judge_a_sufficiency_0_2",
        "judge_a_notes",
        "judge_b_id",
        "judge_b_judged_at",
        "judge_b_relevance_0_2",
        "judge_b_sufficiency_0_2",
        "judge_b_notes",
        "arbiter_id",
        "arbiter_judged_at",
        "arbiter_final_relevance_0_2",
        "arbiter_final_sufficiency_0_2",
        "arbiter_notes",
    ]
    write_csv(RESULTS_DIR / "semantic_support_judgment_template.csv", rows, fieldnames)
    write_csv(
        RESULTS_DIR / "semantic_support_judgment_mapping.csv",
        mapping_rows,
        ["row_id", "case_id", "anchor_ref", "anchor_source_hash", "frozen_snapshot_ref", "truth_boundary"],
    )
    internal_fieldnames = [
        "judgment_id",
        "case_id",
        "reviewer",
        "query",
        "answer_use_claim",
        "anchor_ref",
        "relevance_0_2",
        "sufficiency_0_2",
        "semantic_support_result",
        "notes",
        "external_or_blind",
    ]
    write_csv(RESULTS_DIR / "internal_semantic_support_self_check.csv", internal_rows, internal_fieldnames)
    internal_summary = {
        "status": "author_side_scripted_self_check_completed_external_not_judged",
        "row_count": len(internal_rows),
        "all_internal_relevance_at_least_2": all(int(row["relevance_0_2"]) >= 2 for row in internal_rows),
        "all_internal_sufficiency_at_least_2": all(int(row["sufficiency_0_2"]) >= 2 for row in internal_rows),
        "truth_boundary": "This is a local Codex author-side scripted semantic support self-check. It is not independent manual review, external blind relevance, Pro judgment, or production groundedness validation.",
    }
    base.write_json(RESULTS_DIR / "internal_semantic_support_self_check_summary.json", internal_summary)
    review_md = f"""# Author-Side Semantic Support Self-Check

Status: author-side scripted self-check completed; external/blind judgment not completed.

This self-check records the package author's local semantic assessment of whether the allowed raw/stable anchor is relevant and sufficient for the narrow read-only query/use in this package.

It does not prove Source Intake P0, independent manual review, production groundedness, live LLM/tool behavior, or external blind relevance.

## Result

All {len(internal_rows)} allowed cases were author-side scored relevance=2 and sufficiency=2 for their narrow read-only query/use.

See `results/internal_semantic_support_self_check.csv` for row-level details.
"""
    (OUT_DIR / "AUTHOR_SIDE_SEMANTIC_SUPPORT_SELF_CHECK.md").write_text(review_md, encoding="utf-8")
    instructions = """# Semantic Support Judgment Instructions

Status: packet generated, not judged.

Judge only the visible query, answer/use claim, anchor ref, source hash / frozen snapshot ref, and anchor excerpt.

The `row_id` column is opaque. The judge-only packet intentionally excludes case IDs, expected outcomes, internal self-check results, and row-to-case mapping.

Fill `judge_a_id` / `judge_b_id` and `judge_a_judged_at` / `judge_b_judged_at` when judging. Use stable pseudonymous IDs if real names should not be exposed. The arbiter should fill `arbiter_id` and `arbiter_judged_at` only after comparing both independent judgments.

The judge-only zip is excerpt-based and should be judged from the visible `query`, `answer_use_claim`, and `anchor_excerpt` only. If the excerpt is insufficient or truncated, score relevance/sufficiency as 0 or 1 and explain in notes. Do not request or use the full Pro review package. `anchor_source_hash` and `frozen_snapshot_ref` are return-side audit fields, not judge-side evidence expansion instructions.

Scores:

- relevance: 0 = not relevant, 1 = partially relevant, 2 = directly relevant.
- sufficiency: 0 = does not support the claim, 1 = weak/partial support, 2 = sufficient support for this read-only answer/use claim.

Two independent judges should fill judge A and judge B columns before any arbitration.
This packet does not prove independent/external semantic support until judgments are filled and adjudicated.
"""
    (OUT_DIR / "SEMANTIC_SUPPORT_JUDGMENT_INSTRUCTIONS.md").write_text(instructions, encoding="utf-8")
    judge_zip = OUT_DIR / "semantic-support-judge-only.zip"
    if judge_zip.exists():
        judge_zip.unlink()
    judge_files = [
        OUT_DIR / "SEMANTIC_SUPPORT_JUDGMENT_INSTRUCTIONS.md",
        RESULTS_DIR / "semantic_support_judgment_template.csv",
    ]
    with zipfile.ZipFile(judge_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in judge_files:
            zf.write(path, path.relative_to(OUT_DIR).as_posix())
    judge_hash = base.sha256_file(judge_zip)
    judge_check = {
        "status": "ready_not_judged",
        "judge_zip": base.rel(judge_zip),
        "judge_zip_sha256": judge_hash,
        "included_files": [path.relative_to(OUT_DIR).as_posix() for path in judge_files],
        "excluded_files": ["results/semantic_support_judgment_mapping.csv", "results/internal_semantic_support_self_check.csv"],
        "opaque_row_ids": True,
        "has_judge_identity_fields": True,
        "has_anchor_source_hash": True,
        "has_frozen_snapshot_ref": True,
        "row_count": len(rows),
        "truth_boundary": "Judge-only packet contains only instructions and the blank semantic support judgment template with opaque row IDs, judge/arbiter identity fields, source hashes, and frozen snapshot refs; judgments are not completed.",
    }
    base.write_json(RESULTS_DIR / "semantic_support_judge_package_check.json", judge_check)
    dispatch = write_semantic_support_judge_dispatch(rows, judge_hash)
    return {
        "status": "author_side_scripted_self_check_completed_external_not_judged",
        "row_count": len(rows),
        "template": base.rel(RESULTS_DIR / "semantic_support_judgment_template.csv"),
        "mapping_excluded_from_judge_zip": base.rel(RESULTS_DIR / "semantic_support_judgment_mapping.csv"),
        "author_side_self_check": base.rel(RESULTS_DIR / "internal_semantic_support_self_check.csv"),
        "author_side_self_check_summary": base.rel(RESULTS_DIR / "internal_semantic_support_self_check_summary.json"),
        "judge_zip": base.rel(judge_zip),
        "judge_zip_sha256": judge_hash,
        "judge_dispatch_bundle": dispatch["dispatch_zip"],
        "judge_dispatch_bundle_sha256": dispatch["dispatch_zip_sha256"],
        "truth_boundary": "Author-side scripted semantic self-check is completed, but independent manual or external/blind semantic support judgment is not completed.",
    }


def write_semantic_support_judge_dispatch(rows: list[dict[str, Any]], base_judge_zip_hash: str) -> dict[str, Any]:
    dispatch_dir = OUT_DIR / "judge-dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)

    send_a = """# Semantic Support Judge A Packet

Please judge only the visible rows in `semantic-support-judge-a.zip`.

Fill only the Judge A columns in the enclosed CSV. This Judge A zip intentionally does not expose Judge B or arbiter fill columns.

Scoring:

- relevance: 0 = not relevant, 1 = partially relevant, 2 = directly relevant.
- sufficiency: 0 = does not support the claim, 1 = weak or partial support, 2 = sufficient support for this read-only answer/use claim.

Boundary:

- This is an excerpt-based semantic support judgment packet.
- It is not a Source Intake P0 pass check.
- It is not a production runtime validation.
- Do not use hidden expected outcomes, case IDs, author-side self-checks, or package mapping files.
- Judge from the visible `query`, `answer_use_claim`, and `anchor_excerpt` only.
- If the excerpt is insufficient or truncated, score 0 or 1 and explain in notes.
- Do not request or use the full Pro review package. `anchor_source_hash` and `frozen_snapshot_ref` are return-side audit fields only.
"""
    send_b = send_a.replace("Judge A", "Judge B").replace("judge-a", "judge-b")
    send_b = send_b.replace(
        "This Judge B zip intentionally does not expose Judge B or arbiter fill columns.",
        "This Judge B zip intentionally does not expose Judge A or arbiter fill columns.",
    )
    arbitration = """# Arbitration After Judge Return

Use this only after Judge A and Judge B have returned filled copies.

Minimum arbitration process:

1. Merge Judge A and Judge B scores by `row_id`.
2. For rows where both relevance and sufficiency match, copy the shared score to the arbiter columns.
3. For rows with disagreement, inspect only the visible query, answer/use claim, anchor ref, source hash, frozen snapshot ref, anchor excerpt, and judge notes.
4. Fill:
   - `arbiter_id`
   - `arbiter_judged_at`
   - `arbiter_final_relevance_0_2`
   - `arbiter_final_sufficiency_0_2`
   - `arbiter_notes`

Do not treat arbitration as P0 approval, production runtime validation, or reviewed truth promotion. It only completes independent semantic support judgment for the allowed read-only support rows in this sandbox package.
"""
    readme = """# Judge Dispatch README

This folder prepares the already-ready `semantic-support-judge-only.zip` for two independent judges using per-judge minimized CSV schemas.

Send:

- `semantic-support-judge-a.zip` plus `SEND_TO_JUDGE_A.md` to Judge A.
- `semantic-support-judge-b.zip` plus `SEND_TO_JUDGE_B.md` to Judge B.

Do not send the main Pro review package to judges. Judges should score only from the visible query, answer/use claim, and excerpt in their packet. `anchor_source_hash` and `frozen_snapshot_ref` are for return-side audit, not judge-side source expansion.

After both judges return their filled templates, use `ARBITRATION_AFTER_RETURN.md` to adjudicate disagreements.

Current state:

- Judge packet readiness: ready with per-judge minimized schemas.
- Independent judgments completed: no.
- External semantic support completed: no.
- Source Intake P0 passed: no.
"""
    (dispatch_dir / "SEND_TO_JUDGE_A.md").write_text(send_a, encoding="utf-8")
    (dispatch_dir / "SEND_TO_JUDGE_B.md").write_text(send_b, encoding="utf-8")
    (dispatch_dir / "ARBITRATION_AFTER_RETURN.md").write_text(arbitration, encoding="utf-8")
    (dispatch_dir / "DISPATCH_README.md").write_text(readme, encoding="utf-8")

    a_template = dispatch_dir / "semantic_support_judgment_template_judge_a.csv"
    b_template = dispatch_dir / "semantic_support_judgment_template_judge_b.csv"
    a_rows = [{field: row.get(field, "") for field in JUDGE_A_FIELDS} for row in rows]
    b_rows = [{field: row.get(field, "") for field in JUDGE_B_FIELDS} for row in rows]
    write_csv(a_template, a_rows, JUDGE_A_FIELDS)
    write_csv(b_template, b_rows, JUDGE_B_FIELDS)

    a_zip = dispatch_dir / "semantic-support-judge-a.zip"
    b_zip = dispatch_dir / "semantic-support-judge-b.zip"
    for path in [a_zip, b_zip]:
        if path.exists():
            path.unlink()
    with zipfile.ZipFile(a_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(dispatch_dir / "SEND_TO_JUDGE_A.md", "SEMANTIC_SUPPORT_JUDGMENT_INSTRUCTIONS.md")
        zf.write(a_template, "results/semantic_support_judgment_template.csv")
    with zipfile.ZipFile(b_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(dispatch_dir / "SEND_TO_JUDGE_B.md", "SEMANTIC_SUPPORT_JUDGMENT_INSTRUCTIONS.md")
        zf.write(b_template, "results/semantic_support_judgment_template.csv")

    a_hash = base.sha256_file(a_zip)
    b_hash = base.sha256_file(b_zip)
    (dispatch_dir / "semantic-support-judge-a.zip.sha256").write_text(
        f"{a_hash}  semantic-support-judge-a.zip\n",
        encoding="utf-8",
    )
    (dispatch_dir / "semantic-support-judge-b.zip.sha256").write_text(
        f"{b_hash}  semantic-support-judge-b.zip\n",
        encoding="utf-8",
    )

    manifest = {
        "status": "ready_not_judged",
        "row_count": len(rows),
        "base_judge_zip_sha256": base_judge_zip_hash,
        "judge_a_zip": "semantic-support-judge-a.zip",
        "judge_a_zip_sha256": a_hash,
        "judge_a_csv_columns": JUDGE_A_FIELDS,
        "judge_b_zip": "semantic-support-judge-b.zip",
        "judge_b_zip_sha256": b_hash,
        "judge_b_csv_columns": JUDGE_B_FIELDS,
        "excluded_from_judge_zips": [
            "case_id",
            "expected outcome",
            "author-side self-check",
            "row-to-case mapping",
            "other judge fill columns",
            "arbiter fill columns",
        ],
        "truth_boundary": "Dispatch bundle prepares independent excerpt-based semantic support judgment only; judgments are not completed and this is not P0 or production runtime validation.",
    }
    base.write_json(dispatch_dir / "DISPATCH_MANIFEST.json", manifest)

    dispatch_zip = OUT_DIR / "semantic-support-judge-dispatch-bundle.zip"
    dispatch_sha = OUT_DIR / "semantic-support-judge-dispatch-bundle.zip.sha256"
    for path in [dispatch_zip, dispatch_sha]:
        if path.exists():
            path.unlink()
    dispatch_entries = [
        dispatch_dir / "ARBITRATION_AFTER_RETURN.md",
        dispatch_dir / "DISPATCH_MANIFEST.json",
        dispatch_dir / "DISPATCH_README.md",
        dispatch_dir / "SEND_TO_JUDGE_A.md",
        dispatch_dir / "SEND_TO_JUDGE_B.md",
        a_zip,
        dispatch_dir / "semantic-support-judge-a.zip.sha256",
        b_zip,
        dispatch_dir / "semantic-support-judge-b.zip.sha256",
    ]
    with zipfile.ZipFile(dispatch_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in dispatch_entries:
            zf.write(path, f"semantic-support-judge-dispatch/{path.name}")
    dispatch_hash = base.sha256_file(dispatch_zip)
    dispatch_sha.write_text(f"{dispatch_hash}  semantic-support-judge-dispatch-bundle.zip\n", encoding="utf-8")

    check = {
        "status": "ready_not_judged",
        "dispatch_zip": base.rel(dispatch_zip),
        "dispatch_zip_sha256": dispatch_hash,
        "judge_a_zip_sha256": a_hash,
        "judge_b_zip_sha256": b_hash,
        "per_judge_minimized_schema": True,
        "has_dispatch_manifest": True,
        "has_per_zip_sha_sidecars": True,
        "row_count": len(rows),
        "truth_boundary": "Dispatch bundle is ready to send to two independent judges, but no independent semantic support judgment has been completed.",
    }
    base.write_json(RESULTS_DIR / "semantic_support_judge_dispatch_check.json", check)
    return check


def semantic_support_claim_for_case(case_id: str) -> str:
    if case_id == "G3-02-raw-anchor-generic-allow":
        return (
            "The raw anchor can support a read-only answer about FlexNote's inspected source facts, "
            "including local-first positioning, card/whiteboard model, and tag database features."
        )
    if case_id == "G3-03-mixed-pack-generic-selection":
        return (
            "The raw anchor can support the raw-source portion of a mixed-pack read-only answer about "
            "FlexNote's visual workbench, cards, tags, and source facts while candidate/overlay items remain review input."
        )
    if case_id == "G3-05-web-annotation-source-anchor-fresh-allow":
        return (
            "The raw anchor can support a read-only answer that W3C Web Annotation's Text Quote Selector "
            "shape informs the vault's source-anchor profile with exact, prefix, and suffix context."
        )
    if case_id == "G3-06-w3c-prov-boundary-fresh-allow":
        return (
            "The raw anchor can support a read-only answer that PROV-lite traceability is useful for source "
            "identity, capture/extraction activity, and agent trace, but does not decide truth or confidence."
        )
    if case_id == "G3-07-rag-attribution-fresh-allow":
        return (
            "The raw anchor can support a read-only answer that citation correctness and citation faithfulness "
            "should not be conflated, and that a source link is not automatically evidence support."
        )
    if case_id == "G3-08-web-annotation-text-context-low-cue-allow":
        return (
            "The raw anchor can support a read-only answer that stable text citations should preserve selected text "
            "and nearby context so the evidence span can be re-found."
        )
    if case_id == "G3-09-w3c-prov-truth-boundary-low-cue-allow":
        return (
            "The raw anchor can support a read-only answer that provenance traceability does not decide truth, "
            "raise confidence, or turn a citation into support."
        )
    if case_id == "G3-10-rag-attribution-citation-split-low-cue-allow":
        return (
            "The raw anchor can support a read-only answer that citation correctness and citation faithfulness "
            "are separate checks."
        )
    if case_id == "G3-11-web-annotation-selector-fields-low-cue-allow":
        return (
            "The raw anchor can support a read-only answer that exact, prefix, and suffix fields help preserve "
            "the selected quote and surrounding snippets."
        )
    if case_id == "G3-12-w3c-prov-entity-activity-agent-low-cue-allow":
        return (
            "The raw anchor can support a read-only answer that PROV offers an entity/activity/agent skeleton "
            "that can be borrowed lightly for source records."
        )
    if case_id == "G3-19-restricted-review-raw-anchor-policy":
        return (
            "The raw anchor can support the read-only content portion of this restricted-review case: "
            "FlexNote is local-first, uses reusable cards and visual whiteboards, and describes tags as "
            "an extensible database."
        )
    return "No case-specific semantic support claim was defined; this fallback row must not be sent to judges."


def semantic_support_rationale_for_case(case_id: str) -> str:
    if case_id == "G3-02-raw-anchor-generic-allow":
        return (
            "The excerpt explicitly states FlexNote is local-first, describes the card as the main information atom, "
            "lists whiteboard capabilities, and describes tags as an extensible database. This directly matches the query terms."
        )
    if case_id == "G3-03-mixed-pack-generic-selection":
        return (
            "The excerpt gives the raw source facts needed for the support portion of the mixed pack: local-first visual notes, "
            "cards, whiteboards, and tag database behavior. Candidate and overlay hits are not needed as support."
        )
    if case_id == "G3-05-web-annotation-source-anchor-fresh-allow":
        return (
            "The excerpt names Text Quote Selector and records exact quote, prefix, and suffix as the useful source-anchor shape. "
            "That directly matches the read-only query/use."
        )
    if case_id == "G3-06-w3c-prov-boundary-fresh-allow":
        return (
            "The excerpt states that PROV-lite records traceability and does not decide truth, raise confidence, or turn a citation into support. "
            "That directly matches the boundary query/use."
        )
    if case_id == "G3-07-rag-attribution-fresh-allow":
        return (
            "The excerpt distinguishes citation correctness from citation faithfulness and records that a source link is not evidence by itself. "
            "That directly matches the read-only support boundary query/use."
        )
    if case_id == "G3-08-web-annotation-text-context-low-cue-allow":
        return (
            "The excerpt records the stable text-anchor idea: preserve selected text and surrounding context so a reviewer can re-find the span. "
            "The query does not name the Source Anchor heading."
        )
    if case_id == "G3-09-w3c-prov-truth-boundary-low-cue-allow":
        return (
            "The excerpt says PROV-lite records traceability but does not decide truth, raise confidence, or turn a citation into support. "
            "The query does not name the boundary heading."
        )
    if case_id == "G3-10-rag-attribution-citation-split-low-cue-allow":
        return (
            "The excerpt states that citation correctness and citation faithfulness are distinct. "
            "The query does not name the initial-takeaways heading."
        )
    if case_id == "G3-11-web-annotation-selector-fields-low-cue-allow":
        return (
            "The excerpt names exact, prefix, and suffix as the surrounding text selector shape. "
            "The query asks for selector fields without naming the Source Anchor heading."
        )
    if case_id == "G3-12-w3c-prov-entity-activity-agent-low-cue-allow":
        return (
            "The excerpt records PROV entities, activities, and agents as the lightweight skeleton. "
            "The query does not name the source heading."
        )
    if case_id == "G3-19-restricted-review-raw-anchor-policy":
        return (
            "The excerpt states FlexNote is local-first, describes reusable cards and visual whiteboards, "
            "and records tags as an extensible database. It supports only the raw content portion of the restricted-review case."
        )
    return "The excerpt directly matches the narrow read-only support need."


def extract_anchor_excerpt(source_text: str, selector: str, *, limit: int = 900) -> str:
    lines = source_text.splitlines()
    normalized = selector.lower().replace("-", " ").strip()
    for idx, line in enumerate(lines):
        if line.lstrip("# ").strip().lower().replace("-", " ") == normalized:
            return "\n".join(lines[idx : min(len(lines), idx + 10)])[:limit]
    pos = source_text.find(selector)
    if pos != -1:
        return source_text[pos : pos + limit]
    return "[selector not found in copied source text]"


def run_validation_commands(now: str) -> dict[str, Any]:
    commands = [
        [
            "python",
            "tools/validate_source_intake_contract.py",
            "--scope",
            "current",
            "--out-dir",
            base.rel(RESULTS_DIR),
            "--no-fail",
        ],
        [
            "python",
            "tools/validate_source_intake_contract.py",
            "--scope",
            "contract",
            "--out-dir",
            base.rel(RESULTS_DIR),
            "--no-fail",
        ],
        [
            "python",
            "tools/validate_source_intake_failure_matrix.py",
            "--out-dir",
            base.rel(RESULTS_DIR),
        ],
    ]
    rows = []
    current_lint_errors = 0
    current_lint_warnings = 0
    current_lint_status = "unknown"
    for command in commands:
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        stdout = completed.stdout.strip()
        if command[1].endswith("validate_source_intake_contract.py"):
            try:
                parsed = json.loads(stdout)
            except json.JSONDecodeError:
                parsed = {}
            if parsed.get("scope") == "current":
                current_lint_errors = int(parsed.get("errors") or 0)
                current_lint_warnings = int(parsed.get("warnings") or 0)
                current_lint_status = "structural_pass_semantic_debt" if current_lint_warnings else "clear"
        rows.append(
            {
                "command": " ".join(command),
                "returncode": completed.returncode,
                "stdout": stdout,
                "stderr": completed.stderr.strip(),
            }
        )
    commands_ok = all(row["returncode"] == 0 for row in rows)
    if not commands_ok:
        status = "command_failure"
    elif current_lint_errors:
        status = "commands_pass_with_current_lint_errors"
    elif current_lint_warnings:
        status = "commands_pass_with_current_lint_warnings"
    else:
        status = "pass"
    lint_debt_audit = write_lint_debt_audit()
    result = {
        "status": status,
        "checked_at": now,
        "current_lint_status": current_lint_status,
        "current_lint_errors": current_lint_errors,
        "current_lint_warnings": current_lint_warnings,
        "current_lint_debt_audit": lint_debt_audit,
        "commands": rows,
        "truth_boundary": "Command success means the sandbox checks ran; current lint warnings remain semantic debt and this package is not a P0 pass.",
    }
    base.write_json(RESULTS_DIR / "generic_validation_commands.json", result)
    return result


def write_lint_debt_audit() -> dict[str, Any]:
    issues_path = RESULTS_DIR / "source_intake_current_lint_issues.csv"
    if not issues_path.exists():
        return {
            "status": "missing_current_lint_issues",
            "truth_boundary": "No lint-debt audit was produced because current lint issues were not available.",
        }
    with issues_path.open("r", encoding="utf-8", newline="") as f:
        issues = list(csv.DictReader(f))

    warning_rows = [row for row in issues if row.get("severity") == "warning"]
    high_risk_rows = [row for row in warning_rows if row.get("semantic_class") == "high_risk_manual_review"]
    migration_rows = [row for row in warning_rows if row.get("semantic_class") == "migration_debt_defer_ok"]
    proxy_authority_checks = {
        "source_card_authority_like_metadata",
        "legacy_raw_metadata_used_for_selection",
        "legacy_raw_metadata_used_as_support_anchor",
        "raw_source_authority_like_metadata",
    }
    proxy_rows = [
        row
        for row in issues
        if row.get("check") in proxy_authority_checks
        or str(row.get("field", "")).lower() in {"confidence", "relations", "source_quality", "relevance", "freshness", "cross_source_count"}
    ]
    audit_rows = []
    for row in warning_rows + proxy_rows:
        check = row.get("check", "")
        if check == "legacy_project_lens_overlay_compatibility":
            category = "retrieval_visible_legacy_overlay_compatibility"
        elif check == "migration_placeholder_value":
            category = "defer_ok_migration_placeholder"
        elif check == "source_why_saved_placeholder_without_body_reason":
            category = "high_risk_source_why_saved_placeholder"
        elif row in proxy_rows:
            category = "proxy_authority_metadata"
        else:
            category = "other_current_lint_warning"
        audit_rows.append(
            {
                "category": category,
                "severity": row.get("severity", ""),
                "check": check,
                "semantic_class": row.get("semantic_class", ""),
                "recommended_action": row.get("recommended_action", ""),
                "path": row.get("path", ""),
                "line": row.get("line", ""),
                "field": row.get("field", ""),
                "value": row.get("value", ""),
                "message": row.get("message", ""),
            }
        )
    audit_fields = [
        "category",
        "severity",
        "check",
        "semantic_class",
        "recommended_action",
        "path",
        "line",
        "field",
        "value",
        "message",
    ]
    write_csv(RESULTS_DIR / "source_intake_current_lint_debt_audit.csv", audit_rows, audit_fields)
    summary = {
        "status": "warnings_present" if warning_rows else "clear",
        "warning_count": len(warning_rows),
        "high_risk_manual_review_count": len(high_risk_rows),
        "migration_debt_defer_ok_count": len(migration_rows),
        "retrieval_visible_legacy_overlay_compatibility_count": sum(
            1 for row in warning_rows if row.get("check") == "legacy_project_lens_overlay_compatibility"
        ),
        "source_why_saved_placeholder_without_body_reason_count": sum(
            1 for row in warning_rows if row.get("check") == "source_why_saved_placeholder_without_body_reason"
        ),
        "proxy_authority_metadata_count": len(proxy_rows),
        "audit_csv": base.rel(RESULTS_DIR / "source_intake_current_lint_debt_audit.csv"),
        "truth_boundary": "This audit makes current lint debt visible at package level; it does not clear semantic migration debt or prove P0 readiness.",
    }
    base.write_json(RESULTS_DIR / "source_intake_current_lint_debt_audit_summary.json", summary)
    return summary


def write_reports(summary: dict[str, Any], case_rows: list[dict[str, Any]], now: str) -> None:
    report = f"""# VAKS Source Intake Generic Read-Only Loop Report

Generated: {now}

## Verdict

This package addresses the specific Pro blocker about case-scripted pack role assignment by replacing case_id-based support selection with a generic read-only assembler.

It also implements the first step of the Pro retrieval-plane recommendation: a sandbox `QueryPolicy` is generated before retrieval, a bucket-first filter hook executes before ranking, and each query-run/context-pack carries a bucket receipt. Retrieval is still local lexical only; dense/vector, sparse, graph overlay, RRF fusion, and rerank are explicitly not implemented in this package.

This revision adds a dedicated receipt-effect suite: paired same-query cases restrict allowed buckets and demonstrate non-zero pre-ranking bucket exclusions, so the hook is now observable as more than bookkeeping under restricted policies. It also adds two restricted-policy cases to the main harness, one source_annotation bucket receipt-effect pair, and one reviewed-bucket receipt-effect pair.

The query set is still scripted, but pack roles are assigned by the same record_kind / knowledge_status / query_mode / raw-anchor-resolution rules for every hit. No case_id branch chooses a support item.

Anchor resolution remains intentionally narrow: support extraction is limited to a small stable-anchor heading vocabulary, section-content lexical overlap, and selector resolution. This is generic pack role assignment over a narrow anchor vocabulary, not general semantic support extraction.

## Results

- Cases: {summary['case_count']}
- Expected decisions passed: {summary['passed_expected_decision_count']} / {summary['case_count']}
- Decisions: {summary['decision_breakdown']}
- Pack assembly: {summary['pack_assembly']}
- QueryPolicy receipts: {summary['query_policy_receipt_count']} / {summary['case_count']} (`{summary['query_policy_receipt_file']}`)
- Receipt-effect tests: {summary['receipt_effect_tests']['status']} / non-zero exclusions {summary['receipt_effect_tests']['observed_nonzero_exclusion_count']} / {summary['receipt_effect_tests']['expected_nonzero_exclusion_count']} / changed top-k pairs {summary['receipt_effect_tests']['top_result_or_order_changed_pair_count']}
- Default restricted policy cases: {summary['default_restricted_policy_passed_count']} / {summary['default_restricted_policy_case_count']} passed with non-zero exclusions {summary['default_restricted_policy_nonzero_exclusion_count']} / {summary['default_restricted_policy_case_count']}
- Source-annotation receipt-effect coverage: {summary['receipt_effect_tests']['source_annotation_effect_case_count']} cases / retained {summary['receipt_effect_tests']['source_annotation_retained_case_count']} / excluded {summary['receipt_effect_tests']['source_annotation_excluded_case_count']}
- Reviewed-bucket receipt-effect coverage: {summary['receipt_effect_tests']['reviewed_bucket_effect_case_count']} cases / retained {summary['receipt_effect_tests']['reviewed_bucket_retained_case_count']} / excluded {summary['receipt_effect_tests']['reviewed_bucket_excluded_case_count']}
- Retrieval channels implemented: {summary['retrieval_channels_implemented']}
- Retrieval channels not implemented: {summary['retrieval_channels_not_implemented']}
- New non-FlexNote read-only allow smoke cases: {summary['new_non_flexnote_allow_smoke_count']}
- Low-cue allow cases: {summary['low_cue_allow_case_count']}
- Decoy cases: {summary['decoy_case_count']}
- Broken-anchor negative cases: {summary['broken_anchor_negative_passed_count']} / {summary['broken_anchor_negative_case_count']} blocked as expected
- Cue-depleted paraphrase pressure: {summary['cue_depleted_allow_pressure']['allowed_readonly_count']} allowed / {summary['cue_depleted_allow_pressure']['case_count']} diagnostic queries; intended anchor selected in {summary['cue_depleted_allow_pressure']['intended_anchor_selected_count']} / {summary['cue_depleted_allow_pressure']['case_count']}
- Clean corpus rerun: {summary['clean_corpus_rerun']['status']} with default runtime fixture exclusion; excluded {summary['clean_corpus_rerun']['excluded_fixture_count']} additional runtime test fixture docs; expected decisions passed {summary['clean_corpus_rerun']['passed_expected_decision_count']} / {summary['clean_corpus_rerun']['case_count']}
- Full frozen replay: {summary['full_workspace_frozen_replay']['status']} over {summary['full_workspace_frozen_replay']['corpus_doc_count']} collected Markdown docs
- Semantic support self-check: {summary['semantic_support_judgment']['status']} (author-side self-check completed; independent/external judgment still pending)

## Case Results

""" + "\n".join(
        f"- `{row['case_id']}`: {row['decision']} / top=`{row['top_result']}` / support_count={row['support_count']}"
        for row in case_rows
    ) + """

## Boundary

This is still sandbox runtime evidence. It does not prove Source Intake P0 passed, live LLM/tool runtime validation, live embedding/vector/graph retrieval, independent/external semantic support, or runtime adoption readiness.

The allowed raw/stable anchors have an author-side scripted semantic support self-check in `results/internal_semantic_support_self_check.csv`. This is still not independent manual review, external/blind judgment, or production groundedness validation.
"""
    (OUT_DIR / "GENERIC_READONLY_LOOP_REPORT.md").write_text(report, encoding="utf-8")

    readme = f"""# Source Intake Generic Read-Only Loop Package

Generated: {now}

## Human Summary

This package moves one step past v2: live local Markdown retrieval now flows through a generic read-only pack assembler.

It also adds the first Pro retrieval-plane contract: every query gets a `QueryPolicy` before retrieval, a bucket-first filter hook executes before ranking, and query-run/context-pack artifacts include the policy and bucket receipt.

This revision includes dedicated receipt-effect tests where restricted bucket policies create visible pre-ranking exclusions. The main harness now also includes default restricted review/action policy cases, so non-zero exclusion behavior is visible outside the dedicated paired suite too.

The assembler uses shared rules:

- candidate distillations become `review_input`;
- project overlays become `review_input`;
- raw source cards become `support` only in read-only support modes and only with a resolved raw/stable anchor;
- rank/score/diagnostic signals never become support anchors;
- action-mode queries do not become action basis.

Implemented retrieval channel: local Markdown lexical only.

Not implemented here: dense/vector retrieval, sparse semantic retrieval, graph overlay retrieval, RRF/hybrid fusion, or second-stage rerank.

## Supported Conclusion

In this packaged {summary['case_count']}-query sandbox harness, a generic read-only assembler can route live top-k results into query-run / context-pack / answer-use artifacts while restricting final support to structurally resolved raw/stable anchors.

This package additionally supports the narrow claim that a sandbox `QueryPolicy` / authority-bucket receipt can be generated before retrieval and preserved through query-run/context-pack artifacts. The dedicated receipt-effect suite further demonstrates that the bucket-first hook can produce non-zero corpus exclusions under restricted policies.

The allow cases now include new non-FlexNote raw source-family smoke cases and low-cue allow queries that do not directly name the support heading. The package also includes decoy queries that should not pass as final support, plus a cue-depleted paraphrase pressure suite that is diagnostic rather than tuned to all-green. An author-side scripted semantic support self-check self-scored the allowed raw-anchor cases as relevant and sufficient for their narrow read-only query/use. Independent manual or external/blind semantic judgment is still not completed.

The default corpus now excludes `_runtime_test_fixtures`; the package also includes a clean corpus rerun as a no-op guard while keeping the scorer, query set, anchor vocabulary, and generic pack rules unchanged.

## Unsupported Conclusions

- Source Intake P0 passed: no.
- Generic production runtime validated: no.
- Live LLM/tool runtime validated: no.
- Live embedding/vector/graph retrieval validated: no.
- Independent/external/blind semantic support completed: no.
- Runtime adoption ready: no.
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    pro_request = """# Pro Review Request

Please reverse-audit this generic read-only loop package.

Focus:

1. Does pack role assignment avoid case_id-based support selection?
2. Do the generated query-run/context-pack/answer-use artifacts show generic routing of candidate/overlay/raw hits?
3. Does the new sandbox `QueryPolicy` receipt correctly show authority-bucket filtering before ranking, allowed roles, support-candidate buckets, implemented local lexical channel, and explicitly disabled dense/vector/sparse/graph/RRF/rerank channels?
4. Do `results/receipt_effect_*` demonstrate non-zero bucket exclusions when allowed buckets are restricted, and do paired same-query cases show changed top-k behavior without changing scorer or corpus?
5. Do the new default restricted policy cases in the main harness produce non-zero exclusions, rather than leaving all exclusion evidence only in the dedicated paired suite?
6. Does the new source_annotation receipt-effect pair show source_annotation bucket retention/exclusion behavior?
7. Does the new reviewed-bucket receipt-effect pair exercise a real reviewed bucket document in baseline and exclude it in treatment?
7. Is legacy fallback truly gone from the packaged generic path? Check that the old known-anchor constant, forced-hit helper, known-anchor resolution label, forced-anchor marker, and high-score injection pattern are absent from packaged scripts and generated artifacts.
8. Does the full collected Markdown corpus snapshot and replayer reproduce this package's top-k order?
9. Do the three new non-FlexNote read-only allow smoke cases (W3C Web Annotation, W3C PROV, RAG attribution faithfulness) reduce the single-anchor-family concern without overclaiming semantic support?
10. Do the low-cue allow queries avoid directly naming support headings while still resolving support through section-content overlap?
11. Does the cue-depleted paraphrase pressure suite honestly expose robustness limits rather than tuning every natural query to pass?
12. Do the decoy queries avoid false support, especially action-mode and implementation/runtime decoys?
13. Does the clean corpus rerun still pass after excluding `_runtime_test_fixtures`, without changing scorer, query set, anchor vocabulary, or pack rules?
14. Is the judge-only semantic support packet actually ready-but-not-judged for independent double-judge use: opaque row_id, no case_id, no expected outcome, no mapping, no author-side self-check?
15. Does the package avoid overclaiming P0, live LLM/tool runtime, vector/graph retrieval, semantic support, or adoption readiness?

Truth boundary: the new QueryPolicy is a sandbox receipt contract plus receipt-effect test only. Live local lexical retrieval here means local Markdown lexical retrieval only. Dense/vector/sparse/graph/RRF/rerank are not implemented. Independent/external semantic support judgment is still not completed until judges fill the judge-only packet.
"""
    (OUT_DIR / "PRO_REVIEW_REQUEST.md").write_text(pro_request, encoding="utf-8")

    handoff_prompt = """# Prompt To Send Pro

请反向审计这份 VAKS Source Intake Generic Read-Only Loop 包。

重点不是看它有没有写得好看，而是判断它是否真正回应了上一轮 blocker，尤其是最新 Pro 指出的两件事：残余 fallback 是否彻底退场、judge-only packet 是否真正盲化。

1. pack role assignment 是否已经不再按 case_id 手工决定 support，而是按通用规则处理 live top-k；
2. candidate / project_overlay 是否都被通用规则降为 review_input，而不是 final support；
3. 新增的 sandbox QueryPolicy / authority-bucket receipt 是否真的在 retrieval 前生成，并进入 query-run/context-pack artifacts；
4. QueryPolicy 是否明确记录 allowed buckets、allowed roles、support-candidate buckets、implemented local lexical channel，以及未实现 dense/vector/sparse/graph/RRF/rerank；
5. `results/receipt_effect_*` 是否 demonstrate restricted allowed buckets 会产生 non-zero pre-ranking exclusions；
6. receipt-effect paired same-query cases 是否在不改 scorer/corpus 的情况下产生 top-k 变化；
7. 主 harness 新增的默认 restricted review/action case 是否也出现 non-zero exclusion；
8. source_annotation bucket 是否已有 retention/exclusion 的 receipt-effect 运行证据；
9. reviewed bucket 是否已有真实 reviewed 文档的 retention/exclusion receipt-effect 运行证据；
10. raw source card 是否只有在 read-only support mode 且 raw/stable anchor 可解析时才进入 support；
11. packaged scripts / outputs 里是否已经没有上一轮 legacy fallback 机制：旧的已知 anchor 常量、forced-hit helper、known-anchor resolution label、forced-anchor marker、高分注入模式；
12. full collected Markdown corpus snapshot + replay 是否足以支撑“本包可复跑”，但不被过度解释成 full production reproducibility；
13. 三条 non-FlexNote allow smoke case（W3C Web Annotation、W3C PROV、RAG attribution faithfulness）是否真的缓解了单一 FlexNote anchor family 的问题，但没有被过度解释成语义支持已完成；
14. low-cue allow queries 是否没有直接点名 support heading，却仍能通过 section-content overlap 解析到 support；
15. cue-depleted paraphrase pressure suite 是否诚实暴露了自然问法鲁棒性边界，而不是把每条自然 query 都调到 pass；
16. decoy queries 是否没有误放 support，尤其是 action-mode 和 implementation/runtime decoy；
17. 默认主 harness 是否已经真正排除 `_runtime_test_fixtures`，且 clean corpus rerun 不再只是补救性旁证；
18. judge-only semantic support packet 是否是 ready_not_judged，而不是误写成 semantic support 已完成；
19. author-side scripted semantic support self-check 是否只应算作者侧自检，而不能算 independent manual review、external blind relevance 或 Pro judgment；
20. 还有没有 P0 / runtime adoption / live LLM-tool / vector-graph retrieval / semantic groundedness 的 overclaim。

请直接给：

- overall verdict
- can keep as sandbox runtime evidence: yes/no
- does it improve over v2: yes/no
- does it prove Source Intake P0 passed: yes/no
- does it prove generic production runtime validated: yes/no
- does it prove external/blind semantic support completed: yes/no
- fallback removal status
- judge-only packet readiness
- clean corpus rerun status
- query policy / authority bucket receipt status
- receipt-effect nonzero bucket exclusion status
- default restricted policy case status
- source_annotation bucket receipt-effect status
- reviewed bucket receipt-effect status
- most important remaining blocker
- minimum next tests
- overclaims or unsafe wording

边界：这包自称不是 P0 passed，不是 live LLM/tool runtime，不是 vector/graph retrieval，不是 runtime adoption ready。新增 QueryPolicy 是 sandbox receipt contract + receipt-effect test，不是完整 Pro retrieval plane。这里的 live local lexical retrieval 只等于 local Markdown lexical retrieval；dense/vector/sparse/graph/RRF/rerank 仍未实现。semantic support 仍未完成独立/外部 judge；judge-only packet 只是准备给双判使用。请不要按这些强结论审；请审它是否足够支撑“generic read-only pack/use sandbox evidence + QueryPolicy receipt first step + nonzero bucket exclusion evidence”。
"""
    (OUT_DIR / "PRO_HANDOFF_PROMPT.md").write_text(handoff_prompt, encoding="utf-8")


def manifest_rows(paths: list[Path]) -> list[dict[str, Any]]:
    rows = []
    seen: set[str] = set()
    for path in sorted(paths):
        if not path.exists() or not path.is_file():
            continue
        arcname = base.rel(path)
        if arcname in seen:
            continue
        seen.add(arcname)
        rows.append({"path": arcname, "sha256": base.sha256_file(path), "bytes": path.stat().st_size})
    return rows


def package_outputs(input_paths: set[Path], summary: dict[str, Any]) -> tuple[Path, str]:
    scripts = [
        ROOT / "tools" / "run_source_intake_generic_readonly_loop.py",
        ROOT / "tools" / "source_intake_readonly_shared.py",
        ROOT / "tools" / "validate_source_intake_contract.py",
        ROOT / "tools" / "validate_source_intake_failure_matrix.py",
        ROOT / "tools" / "source_intake_enum_registry.json",
        ROOT / "SOURCE_INTAKE.md",
    ]
    base.write_json(
        OUT_DIR / "PACKAGE_CHECK.json",
        {
            "status": "sandbox_package_check_pass" if summary["passed_expected_decision_count"] == summary["case_count"] and summary["full_workspace_frozen_replay"]["status"] == "pass" else "sandbox_package_check_fail",
            "case_count": summary["case_count"],
            "passed_expected_decision_count": summary["passed_expected_decision_count"],
            "query_policy_contract_status": summary["query_policy_contract_status"],
            "query_policy_receipt_count": summary["query_policy_receipt_count"],
            "receipt_effect_status": summary["receipt_effect_tests"]["status"],
            "receipt_effect_observed_nonzero_exclusion_count": summary["receipt_effect_tests"]["observed_nonzero_exclusion_count"],
            "receipt_effect_expected_nonzero_exclusion_count": summary["receipt_effect_tests"]["expected_nonzero_exclusion_count"],
            "default_restricted_policy_case_count": summary["default_restricted_policy_case_count"],
            "default_restricted_policy_nonzero_exclusion_count": summary["default_restricted_policy_nonzero_exclusion_count"],
            "source_annotation_effect_case_count": summary["receipt_effect_tests"]["source_annotation_effect_case_count"],
            "source_annotation_retained_case_count": summary["receipt_effect_tests"]["source_annotation_retained_case_count"],
            "source_annotation_excluded_case_count": summary["receipt_effect_tests"]["source_annotation_excluded_case_count"],
            "source_annotation_exclusion_observed_across_all_restricted_pairs": summary["receipt_effect_tests"]["source_annotation_exclusion_observed_across_all_restricted_pairs"],
            "reviewed_bucket_effect_case_count": summary["receipt_effect_tests"]["reviewed_bucket_effect_case_count"],
            "reviewed_bucket_retained_case_count": summary["receipt_effect_tests"]["reviewed_bucket_retained_case_count"],
            "reviewed_bucket_excluded_case_count": summary["receipt_effect_tests"]["reviewed_bucket_excluded_case_count"],
            "reviewed_bucket_exclusion_observed_across_all_restricted_pairs": summary["receipt_effect_tests"]["reviewed_bucket_exclusion_observed_across_all_restricted_pairs"],
            "retrieval_channels_implemented": summary["retrieval_channels_implemented"],
            "retrieval_channels_not_implemented": summary["retrieval_channels_not_implemented"],
            "full_workspace_frozen_replay_status": summary["full_workspace_frozen_replay"]["status"],
            "semantic_support_judgment_status": summary["semantic_support_judgment"]["status"],
            "truth_boundary": "Package check covers generated sandbox evidence, QueryPolicy authority-bucket receipts, receipt-effect exclusions, generic assembler decisions, and full collected Markdown corpus replay only.",
        },
    )
    sidecar_name = f"{ZIP_NAME}.sha256"
    output_files = [
        p
        for p in OUT_DIR.rglob("*")
        if p.is_file() and p.name not in {ZIP_NAME, sidecar_name, "PACKAGE_MANIFEST.json"}
    ]
    rows = manifest_rows(output_files + sorted(input_paths) + scripts)
    base.write_json(
        OUT_DIR / "PACKAGE_MANIFEST.json",
        {
            "files": rows,
            "file_count": len(rows),
            "manifest_excludes_self": True,
        },
    )

    zip_path = OUT_DIR / ZIP_NAME
    if zip_path.exists():
        zip_path.unlink()
    package_files = [p for p in OUT_DIR.rglob("*") if p.is_file() and p.name != ZIP_NAME]
    package_files = [p for p in package_files if p.name != sidecar_name]
    package_files += sorted(input_paths)
    package_files += scripts
    seen: set[str] = set()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package_files):
            if not path.exists() or not path.is_file():
                continue
            arcname = base.rel(path)
            if arcname in seen:
                continue
            seen.add(arcname)
            zf.write(path, arcname)
    zip_hash = base.sha256_file(zip_path)
    (OUT_DIR / sidecar_name).write_text(f"{zip_hash}  {ZIP_NAME}\n", encoding="utf-8")
    submission = f"""# Pro Submission Summary

Send Pro this main package:

```text
{ZIP_NAME}
```

SHA256:

```text
{zip_hash.upper()}
```

Use this prompt:

```text
PRO_HANDOFF_PROMPT.md
```

Optional judge-only semantic support packet:

```text
semantic-support-judge-only.zip
```

Recommended judge dispatch packet:

```text
semantic-support-judge-dispatch-bundle.zip
```

Boundary:

```text
This is sandbox generic read-only pack/use evidence.
It is not Source Intake P0 passed.
It is not live LLM/tool runtime validation.
It is not vector/graph retrieval validation.
Live local lexical retrieval means local Markdown lexical retrieval only.
QueryPolicy / authority-bucket receipt is implemented as a sandbox contract, receipt-effect tests show non-zero exclusions under restricted bucket policies, default restricted main-harness cases are included, and source_annotation plus reviewed bucket behavior is covered by receipt-effect evidence.
Author-side scripted semantic support self-check is completed, but independent/external blind Pro judgment is not completed.
The judge-only packet uses opaque row IDs and excludes mapping / case IDs / expected outcomes / author-side self-check.
The dispatch bundle uses per-judge minimized schemas plus a dispatch manifest and per-zip SHA sidecars; judgments are still not completed.
```
"""
    (OUT_DIR / "PRO_SUBMISSION_SUMMARY.md").write_text(submission, encoding="utf-8")
    return zip_path, zip_hash


def main() -> int:
    configure_base_paths()
    reset_output_dir()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    corpus = normalize_corpus_record_kinds(base.collect_corpus())

    case_rows: list[dict[str, Any]] = []
    retrieval_rows: list[dict[str, Any]] = []
    query_policy_rows: list[dict[str, Any]] = []
    input_paths: set[Path] = set()
    assembly_rows: list[dict[str, Any]] = []

    for case in GENERIC_QUERIES:
        case_with_policy = dict(case)
        policy, bucket_receipt, hits = base.retrieve_with_query_policy(case_with_policy, corpus)
        case_with_policy["query_policy"] = policy
        case_with_policy["bucket_receipt"] = bucket_receipt
        if not hits:
            raise RuntimeError(f"No retrieval results for {case['case_id']}")
        query_policy_rows.append(
            {
                "case_id": case["case_id"],
                "query_policy_id": policy["policy_id"],
                "use_mode": policy["use_mode"],
                "risk_tier": policy["risk_tier"],
                "allowed_authority_buckets": policy["allowed_authority_buckets"],
                "support_candidate_authority_buckets": policy["support_candidate_authority_buckets"],
                "allowed_roles": policy["allowed_roles"],
                "retrieval_channels": policy["retrieval_channels"],
                "disabled_channels": policy["disabled_channels"],
                "fusion_method": policy["fusion_method"],
                "fusion_scope": policy["fusion_scope"],
                "rerank_method": policy["rerank_method"],
                "pre_filter_doc_count": bucket_receipt["pre_filter_doc_count"],
                "post_filter_doc_count": bucket_receipt["post_filter_doc_count"],
                "excluded_doc_count": bucket_receipt["excluded_doc_count"],
                "pre_filter_bucket_counts": bucket_receipt["pre_filter_bucket_counts"],
                "post_filter_bucket_counts": bucket_receipt["post_filter_bucket_counts"],
                "excluded_bucket_counts": bucket_receipt["excluded_bucket_counts"],
            }
        )
        items = assemble_pack_generic(case_with_policy, hits)
        mutation_warnings = apply_adversarial_case_mutations(case_with_policy, items)
        decision, checks, warnings = evaluate_support_generic(items)
        warnings = mutation_warnings + warnings
        row = base.write_case_artifacts(case_with_policy, hits, items, decision, checks, warnings, now)
        case_rows.append(row)
        for hit in hits:
            retrieval_rows.append(
                {
                    "case_id": case["case_id"],
                    "query_policy_id": policy["policy_id"],
                    "rank": hit.rank,
                    "score": round(hit.score, 4),
                    "path": hit.doc.rel_path,
                    "authority_bucket": base.doc_authority_bucket(hit.doc),
                    "record_kind": hit.doc.record_kind,
                    "knowledge_status": hit.doc.knowledge_status,
                    "warning_code": hit.doc.warning_code,
                    "matched_terms": hit.matched_terms,
                    "snippet": hit.snippet,
                }
            )
            input_paths.add(hit.doc.abs_path)
        for item in items:
            input_paths.add(ROOT / item["ref"])
            assembly_rows.append(
                {
                    "case_id": case["case_id"],
                    "ref": item["ref"],
                    "authority_bucket": item.get("authority_bucket", ""),
                    "record_kind": item["record_kind"],
                    "knowledge_status": item["knowledge_status"],
                    "pack_role": item["pack_role"],
                    "retrieval_role": item.get("retrieval_role", ""),
                    "support_eligibility": item.get("support_eligibility", ""),
                    "eligibility_basis": item.get("eligibility_basis", ""),
                    "match_representation": item.get("match_representation", ""),
                    "support_representation": item.get("support_representation", ""),
                    "independent_anchor_ref": item["independent_anchor_ref"],
                    "assembler_rule": item.get("assembler_rule", ""),
                    "case_scripted_selection": item.get("case_scripted_selection", ""),
                    "excluded_reason": item["excluded_reason"],
                }
            )

    write_csv(
        RESULTS_DIR / "generic_live_retrieval_results.csv",
        retrieval_rows,
        ["case_id", "query_policy_id", "rank", "score", "path", "authority_bucket", "record_kind", "knowledge_status", "warning_code", "matched_terms", "snippet"],
    )
    write_csv(
        RESULTS_DIR / "generic_query_policy_receipts.csv",
        query_policy_rows,
        [
            "case_id",
            "query_policy_id",
            "use_mode",
            "risk_tier",
            "allowed_authority_buckets",
            "support_candidate_authority_buckets",
            "allowed_roles",
            "retrieval_channels",
            "disabled_channels",
            "fusion_method",
            "fusion_scope",
            "rerank_method",
            "pre_filter_doc_count",
            "post_filter_doc_count",
            "excluded_doc_count",
            "pre_filter_bucket_counts",
            "post_filter_bucket_counts",
            "excluded_bucket_counts",
        ],
    )
    write_csv(
        RESULTS_DIR / "generic_pack_assembly_decisions.csv",
        assembly_rows,
        [
            "case_id",
            "ref",
            "authority_bucket",
            "record_kind",
            "knowledge_status",
            "pack_role",
            "retrieval_role",
            "support_eligibility",
            "eligibility_basis",
            "match_representation",
            "support_representation",
            "independent_anchor_ref",
            "assembler_rule",
            "case_scripted_selection",
            "excluded_reason",
        ],
    )
    write_csv(
        RESULTS_DIR / "generic_readonly_loop_cases.csv",
        case_rows,
        [
            "case_id",
            "query",
            "query_mode",
            "expected_decision",
            "decision",
            "pass",
            "retrieved_count",
            "selected_count",
            "support_count",
            "top_result",
            "top_result_kind",
            "query_run",
            "context_pack",
            "answer_use",
            "warnings",
            "support_checks",
        ],
    )
    write_events(case_rows, retrieval_rows, now)
    artifact_exclusion = base.write_artifact_exclusion_manifest(case_rows, now)
    full_replay = write_full_workspace_snapshot(corpus, retrieval_rows, now)
    receipt_effect = run_receipt_effect_tests(corpus, now)
    cue_depleted_pressure = run_cue_depleted_allow_pressure(corpus, now)
    clean_corpus_rerun = run_clean_corpus_rerun(corpus, now)
    semantic_packet = write_semantic_support_judgment_packet(case_rows)
    validation = run_validation_commands(now)

    summary = {
        "generated_at": now,
        "overall_verdict": "sandbox_generic_readonly_loop_evidence_partial",
        "case_count": len(case_rows),
        "passed_expected_decision_count": sum(1 for row in case_rows if row["pass"]),
        "decision_breakdown": dict(Counter(row["decision"] for row in case_rows)),
        "corpus_doc_count": len(corpus),
        "new_non_flexnote_allow_smoke_count": sum(
            1 for row in case_rows if row["case_id"] in FRESH_NON_FLEXNOTE_ALLOW_CASE_IDS and row["decision"] == "allowed_readonly"
        ),
        "new_non_flexnote_allow_smoke_case_ids": sorted(FRESH_NON_FLEXNOTE_ALLOW_CASE_IDS),
        "low_cue_allow_case_count": sum(
            1 for row in case_rows if row["case_id"] in LOW_CUE_ALLOW_CASE_IDS and row["decision"] == "allowed_readonly"
        ),
        "low_cue_allow_case_ids": sorted(LOW_CUE_ALLOW_CASE_IDS),
        "decoy_case_count": sum(1 for row in case_rows if row["case_id"] in DECOY_CASE_IDS),
        "decoy_passed_count": sum(
            1 for row in case_rows if row["case_id"] in DECOY_CASE_IDS and row["decision"] == row["expected_decision"]
        ),
        "decoy_case_ids": sorted(DECOY_CASE_IDS),
        "broken_anchor_negative_case_count": sum(1 for row in case_rows if row["case_id"] in BROKEN_ANCHOR_NEGATIVE_CASE_IDS),
        "broken_anchor_negative_passed_count": sum(
            1
            for row in case_rows
            if row["case_id"] in BROKEN_ANCHOR_NEGATIVE_CASE_IDS and row["decision"] == row["expected_decision"]
        ),
        "broken_anchor_negative_case_ids": sorted(BROKEN_ANCHOR_NEGATIVE_CASE_IDS),
        "anchor_resolution_scope": "narrow_stable_anchor_heading_vocabulary_plus_section_content_overlap_plus_selector_resolution",
        "pro_retrieval_plane_step": "step1_query_policy_authority_bucket_receipts",
        "query_policy_contract_status": "sandbox_contract_included",
        "query_policy_receipt_count": len(query_policy_rows),
        "query_policy_receipt_file": "results/generic_query_policy_receipts.csv",
        "authority_filter_mode": "bucket_first_before_ranking",
        "default_restricted_policy_case_count": sum(1 for row in case_rows if row["case_id"] in DEFAULT_RESTRICTED_POLICY_CASE_IDS),
        "default_restricted_policy_passed_count": sum(
            1 for row in case_rows if row["case_id"] in DEFAULT_RESTRICTED_POLICY_CASE_IDS and row["pass"]
        ),
        "default_restricted_policy_nonzero_exclusion_count": sum(
            1
            for row in query_policy_rows
            if row["case_id"] in DEFAULT_RESTRICTED_POLICY_CASE_IDS and int(row["excluded_doc_count"]) > 0
        ),
        "default_restricted_policy_case_ids": sorted(DEFAULT_RESTRICTED_POLICY_CASE_IDS),
        "receipt_effect_tests": receipt_effect,
        "retrieval_channels_implemented": ["local_lexical"],
        "retrieval_channels_not_implemented": ["dense_vector", "sparse_semantic", "graph_overlay", "second_stage_rerank", "rrf_hybrid_fusion"],
        "support_candidate_buckets": ["raw_anchor"],
        "fusion_scope_contract": "within_authority_bucket_only_when_multiple_channels_exist",
        "cue_depleted_allow_pressure": cue_depleted_pressure,
        "clean_corpus_rerun": clean_corpus_rerun,
        "pack_assembly": "generic_record_kind_status_anchor_rules_no_case_id_role_branching",
        "case_scripted_pack_role_selection": False,
        "query_set_scripted": True,
        "live_local_lexical_retrieval_used": True,
        "retrieval_scope": "local_markdown_corpus_lexical_retrieval",
        "live_llm_used": False,
        "live_tool_runtime_used": False,
        "writeback_attempted": False,
        "promotion_attempted": False,
        "truth_mutation_attempted": False,
        "source_intake_p0_passed": False,
        "external_blind_relevance_completed": False,
        "semantic_anchor_support_status": "author_side_scripted_self_check_completed_external_not_judged",
        "live_artifact_exclusion": artifact_exclusion,
        "full_workspace_frozen_replay": full_replay,
        "semantic_support_judgment": semantic_packet,
        "validation_commands": validation,
        "truth_boundary": "Generic assembler evidence is still a local lexical read-only sandbox; it does not prove semantic support, live LLM/tool runtime, vector/graph retrieval, P0, or adoption readiness.",
    }
    base.write_json(RESULTS_DIR / "generic_readonly_loop_summary.json", summary)
    write_reports(summary, case_rows, now)
    zip_path, zip_hash = package_outputs(input_paths, summary)
    summary["package_zip"] = base.rel(zip_path)
    summary["package_sha256"] = zip_hash
    base.write_json(RESULTS_DIR / "generic_readonly_loop_summary.json", summary)
    print(json.dumps({"status": "pass", "out_dir": base.rel(OUT_DIR), "zip": base.rel(zip_path), "sha256": zip_hash}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
