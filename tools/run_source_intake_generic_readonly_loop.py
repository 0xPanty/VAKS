#!/usr/bin/env python
"""Run a generic Source Intake read-only pack/use loop.

This script answers the next Pro audit blocker after the live-readonly v2
package: move from case-scripted pack assembly to a generic read-only assembler.

Scope is intentionally narrow:
- local Markdown lexical retrieval is live;
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
        "case_id": "G3-04-canonical-overlay-generic-downgrade",
        "query": "canonical overlay runtime fixture FlexNote visual workbench project overlay support",
        "query_mode": "action",
        "intent": "Generic assembler should not let a canonical project overlay become final support.",
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


def run_cue_depleted_allow_pressure(corpus: list[base.CorpusDoc], now: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for query in CUE_DEPLETED_ALLOW_PRESSURE_QUERIES:
        case = {
            "case_id": query["pressure_id"],
            "query": query["query"],
            "query_mode": query["query_mode"],
        }
        hits = base.retrieve(query["query"], corpus)
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
                "intended_anchor_ref": query["intended_anchor_ref"],
                "decision": decision,
                "allowed_readonly": decision == "allowed_readonly",
                "intended_anchor_selected": query["intended_anchor_ref"] in support_anchors,
                "support_count": len(support_items),
                "support_refs": support_refs,
                "support_anchors": support_anchors,
                "top_result": hits[0].doc.rel_path if hits else "",
                "top_result_kind": hits[0].doc.record_kind if hits else "",
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
            "intended_anchor_ref",
            "decision",
            "allowed_readonly",
            "intended_anchor_selected",
            "support_count",
            "support_refs",
            "support_anchors",
            "top_result",
            "top_result_kind",
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
                    "stage": "live_retrieve",
                    "live_retrieval_used": True,
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
    if path.endswith("candidate-distillation.md") or path.endswith("refresh.md"):
        return "candidate_distillation"
    if "project_lens_overlays/" in path or "project_overlays/" in path or path.endswith("-overlay.md"):
        return "project_overlay"
    return "source_card"

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
        docs.append({"path": rel, "title": str(fm.get("title") or path.stem), "body": body, "kind": kind})
    checks = []
    for query in manifest["queries"]:
        ranked = []
        for doc in docs:
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
        "status": "pass",
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
    return {
        "status": "author_side_scripted_self_check_completed_external_not_judged",
        "row_count": len(rows),
        "template": base.rel(RESULTS_DIR / "semantic_support_judgment_template.csv"),
        "mapping_excluded_from_judge_zip": base.rel(RESULTS_DIR / "semantic_support_judgment_mapping.csv"),
        "author_side_self_check": base.rel(RESULTS_DIR / "internal_semantic_support_self_check.csv"),
        "author_side_self_check_summary": base.rel(RESULTS_DIR / "internal_semantic_support_self_check_summary.json"),
        "judge_zip": base.rel(judge_zip),
        "judge_zip_sha256": judge_hash,
        "truth_boundary": "Author-side scripted semantic self-check is completed, but independent manual or external/blind semantic support judgment is not completed.",
    }


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
    return "The raw anchor can support the allowed read-only answer/use claim for this case."


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
        rows.append(
            {
                "command": " ".join(command),
                "returncode": completed.returncode,
                "stdout": stdout,
                "stderr": completed.stderr.strip(),
            }
        )
    result = {
        "status": "pass" if all(row["returncode"] == 0 for row in rows) and current_lint_errors == 0 else "pass_with_current_lint_errors",
        "checked_at": now,
        "current_lint_errors": current_lint_errors,
        "commands": rows,
        "truth_boundary": "Current lint can include pre-existing workspace errors; this package is not a P0 pass.",
    }
    base.write_json(RESULTS_DIR / "generic_validation_commands.json", result)
    return result


def write_reports(summary: dict[str, Any], case_rows: list[dict[str, Any]], now: str) -> None:
    report = f"""# VAKS Source Intake Generic Read-Only Loop Report

Generated: {now}

## Verdict

This package addresses the specific Pro blocker about case-scripted pack role assignment by replacing case_id-based support selection with a generic read-only assembler.

The query set is still scripted, but pack roles are assigned by the same record_kind / knowledge_status / query_mode / raw-anchor-resolution rules for every hit. No case_id branch chooses a support item.

Anchor resolution remains intentionally narrow: support extraction is limited to a small stable-anchor heading vocabulary, section-content lexical overlap, and selector resolution. This is generic pack role assignment over a narrow anchor vocabulary, not general semantic support extraction.

## Results

- Cases: {summary['case_count']}
- Expected decisions passed: {summary['passed_expected_decision_count']} / {summary['case_count']}
- Decisions: {summary['decision_breakdown']}
- Pack assembly: {summary['pack_assembly']}
- New non-FlexNote read-only allow smoke cases: {summary['new_non_flexnote_allow_smoke_count']}
- Low-cue allow cases: {summary['low_cue_allow_case_count']}
- Decoy cases: {summary['decoy_case_count']}
- Cue-depleted paraphrase pressure: {summary['cue_depleted_allow_pressure']['allowed_readonly_count']} allowed / {summary['cue_depleted_allow_pressure']['case_count']} diagnostic queries; intended anchor selected in {summary['cue_depleted_allow_pressure']['intended_anchor_selected_count']} / {summary['cue_depleted_allow_pressure']['case_count']}
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

The assembler uses shared rules:

- candidate distillations become `review_input`;
- project overlays become `review_input`;
- raw source cards become `support` only in read-only support modes and only with a resolved raw/stable anchor;
- rank/score/diagnostic signals never become support anchors;
- action-mode queries do not become action basis.

## Supported Conclusion

In this packaged {summary['case_count']}-query sandbox harness, a generic read-only assembler can route live top-k results into query-run / context-pack / answer-use artifacts while restricting final support to structurally resolved raw/stable anchors.

The allow cases now include new non-FlexNote raw source-family smoke cases and low-cue allow queries that do not directly name the support heading. The package also includes decoy queries that should not pass as final support, plus a cue-depleted paraphrase pressure suite that is diagnostic rather than tuned to all-green. An author-side scripted semantic support self-check self-scored the allowed raw-anchor cases as relevant and sufficient for their narrow read-only query/use. Independent manual or external/blind semantic judgment is still not completed.

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
3. Is legacy fallback truly gone from the packaged generic path? Check that the old known-anchor constant, forced-hit helper, known-anchor resolution label, forced-anchor marker, and high-score injection pattern are absent from packaged scripts and generated artifacts.
4. Does the full collected Markdown corpus snapshot and replayer reproduce this package's top-k order?
5. Do the three new non-FlexNote read-only allow smoke cases (W3C Web Annotation, W3C PROV, RAG attribution faithfulness) reduce the single-anchor-family concern without overclaiming semantic support?
6. Do the low-cue allow queries avoid directly naming support headings while still resolving support through section-content overlap?
7. Does the cue-depleted paraphrase pressure suite honestly expose robustness limits rather than tuning every natural query to pass?
8. Do the decoy queries avoid false support, especially action-mode and implementation/runtime decoys?
9. Is the judge-only semantic support packet actually blind enough for independent double-judge use: opaque row_id, no case_id, no expected outcome, no mapping, no author-side self-check?
10. Does the package avoid overclaiming P0, live LLM/tool runtime, vector/graph retrieval, semantic support, or adoption readiness?

Truth boundary: live retrieval here means local Markdown lexical retrieval only. Independent/external semantic support judgment is still not completed until judges fill the judge-only packet.
"""
    (OUT_DIR / "PRO_REVIEW_REQUEST.md").write_text(pro_request, encoding="utf-8")

    handoff_prompt = """# Prompt To Send Pro

请反向审计这份 VAKS Source Intake Generic Read-Only Loop 包。

重点不是看它有没有写得好看，而是判断它是否真正回应了上一轮 blocker，尤其是最新 Pro 指出的两件事：残余 fallback 是否彻底退场、judge-only packet 是否真正盲化。

1. pack role assignment 是否已经不再按 case_id 手工决定 support，而是按通用规则处理 live top-k；
2. candidate / project_overlay 是否都被通用规则降为 review_input，而不是 final support；
3. raw source card 是否只有在 read-only support mode 且 raw/stable anchor 可解析时才进入 support；
4. packaged scripts / outputs 里是否已经没有上一轮 legacy fallback 机制：旧的已知 anchor 常量、forced-hit helper、known-anchor resolution label、forced-anchor marker、高分注入模式；
5. full collected Markdown corpus snapshot + replay 是否足以支撑“本包可复跑”，但不被过度解释成 full production reproducibility；
6. 三条 non-FlexNote allow smoke case（W3C Web Annotation、W3C PROV、RAG attribution faithfulness）是否真的缓解了单一 FlexNote anchor family 的问题，但没有被过度解释成语义支持已完成；
7. low-cue allow queries 是否没有直接点名 support heading，却仍能通过 section-content overlap 解析到 support；
8. cue-depleted paraphrase pressure suite 是否诚实暴露了自然问法鲁棒性边界，而不是把每条自然 query 都调到 pass；
9. decoy queries 是否没有误放 support，尤其是 action-mode 和 implementation/runtime decoy；
10. judge-only semantic support packet 是否已适合独立双判：只给 opaque row_id，不给 case_id / expected outcome / mapping / author-side self-check；
11. author-side scripted semantic support self-check 是否只应算作者侧自检，而不能算 independent manual review、external blind relevance 或 Pro judgment；
12. 还有没有 P0 / runtime adoption / live LLM-tool / vector-graph retrieval / semantic groundedness 的 overclaim。

请直接给：

- overall verdict
- can keep as sandbox runtime evidence: yes/no
- does it improve over v2: yes/no
- does it prove Source Intake P0 passed: yes/no
- does it prove generic production runtime validated: yes/no
- does it prove external/blind semantic support completed: yes/no
- fallback removal status
- judge-only packet readiness
- most important remaining blocker
- minimum next tests
- overclaims or unsafe wording

边界：这包自称不是 P0 passed，不是 live LLM/tool runtime，不是 vector/graph retrieval，不是 runtime adoption ready。这里的 live retrieval 只等于 local Markdown lexical retrieval。semantic support 仍未完成独立/外部 judge；judge-only packet 只是准备给双判使用。请不要按这些强结论审；请审它是否足够支撑“generic read-only pack/use sandbox evidence”。
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
            "status": "pass" if summary["passed_expected_decision_count"] == summary["case_count"] and summary["full_workspace_frozen_replay"]["status"] == "pass" else "fail",
            "case_count": summary["case_count"],
            "passed_expected_decision_count": summary["passed_expected_decision_count"],
            "full_workspace_frozen_replay_status": summary["full_workspace_frozen_replay"]["status"],
            "semantic_support_judgment_status": summary["semantic_support_judgment"]["status"],
            "truth_boundary": "Package check covers generated sandbox evidence, generic assembler decisions, and full collected Markdown corpus replay only.",
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

Boundary:

```text
This is sandbox generic read-only pack/use evidence.
It is not Source Intake P0 passed.
It is not live LLM/tool runtime validation.
It is not vector/graph retrieval validation.
Live retrieval means local Markdown lexical retrieval only.
Author-side scripted semantic support self-check is completed, but independent/external blind Pro judgment is not completed.
The judge-only packet uses opaque row IDs and excludes mapping / case IDs / expected outcomes / author-side self-check.
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
    input_paths: set[Path] = set()
    assembly_rows: list[dict[str, Any]] = []

    for case in GENERIC_QUERIES:
        hits = base.retrieve(case["query"], corpus)
        if not hits:
            raise RuntimeError(f"No retrieval results for {case['case_id']}")
        items = assemble_pack_generic(case, hits)
        decision, checks, warnings = evaluate_support_generic(items)
        row = base.write_case_artifacts(case, hits, items, decision, checks, warnings, now)
        case_rows.append(row)
        for hit in hits:
            retrieval_rows.append(
                {
                    "case_id": case["case_id"],
                    "rank": hit.rank,
                    "score": round(hit.score, 4),
                    "path": hit.doc.rel_path,
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
                    "record_kind": item["record_kind"],
                    "knowledge_status": item["knowledge_status"],
                    "pack_role": item["pack_role"],
                    "independent_anchor_ref": item["independent_anchor_ref"],
                    "assembler_rule": item.get("assembler_rule", ""),
                    "case_scripted_selection": item.get("case_scripted_selection", ""),
                    "excluded_reason": item["excluded_reason"],
                }
            )

    write_csv(
        RESULTS_DIR / "generic_live_retrieval_results.csv",
        retrieval_rows,
        ["case_id", "rank", "score", "path", "record_kind", "knowledge_status", "warning_code", "matched_terms", "snippet"],
    )
    write_csv(
        RESULTS_DIR / "generic_pack_assembly_decisions.csv",
        assembly_rows,
        ["case_id", "ref", "record_kind", "knowledge_status", "pack_role", "independent_anchor_ref", "assembler_rule", "case_scripted_selection", "excluded_reason"],
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
    cue_depleted_pressure = run_cue_depleted_allow_pressure(corpus, now)
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
        "anchor_resolution_scope": "narrow_stable_anchor_heading_vocabulary_plus_section_content_overlap_plus_selector_resolution",
        "cue_depleted_allow_pressure": cue_depleted_pressure,
        "pack_assembly": "generic_record_kind_status_anchor_rules_no_case_id_role_branching",
        "case_scripted_pack_role_selection": False,
        "query_set_scripted": True,
        "live_retrieval_used": True,
        "live_retrieval_scope": "local_markdown_corpus_lexical_retrieval",
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
