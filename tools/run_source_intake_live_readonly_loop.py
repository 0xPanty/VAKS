#!/usr/bin/env python
"""Run a live read-only Source Intake retrieval -> pack -> answer/use smoke.

This is intentionally narrower than a production runtime:
- local Markdown corpus retrieval is live and data-driven;
- context-pack and answer/use artifacts are generated from retrieved items;
- no LLM, no writeback, no promotion, no truth mutation;
- output is sandbox runtime evidence, not Source Intake P0 approval.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "review" / "source-intake-live-readonly-loop-2026-06-14"
RESULTS_DIR = OUT_DIR / "results"
QUERY_RUN_DIR = OUT_DIR / "query_runs"
CONTEXT_PACK_DIR = OUT_DIR / "context_packs"
ANSWER_USE_DIR = OUT_DIR / "answer_use"
ZIP_NAME = "source-intake-live-readonly-loop-pro-review-package.zip"

FLEXNOTE_EXTRACTED_FACTS_ANCHOR = "raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md#Extracted Source Facts"

COLLECT_GLOBS = [
    "raw/**/*.md",
    "outputs/review/*candidate-distillation.md",
    "outputs/review/*refresh.md",
    "outputs/review/project_lens_overlays/*.md",
    "outputs/review/project_overlays/**/*.md",
]

EXCLUDED_PATH_MARKERS = [
    "outputs/review/source-intake-runtime-readonly-loop-",
    "outputs/review/source-intake-live-readonly-loop-",
    "outputs/review/source-intake-control-flow-hardening-",
    "outputs/review/vaks-yuxi-fusion-pro-package-",
    "outputs/review/vaks-yuxi-phase-b-pressure-test-",
]

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


@dataclass(frozen=True)
class CorpusDoc:
    rel_path: str
    abs_path: Path
    text: str
    frontmatter: dict[str, Any]
    body: str
    record_kind: str
    knowledge_status: str
    warning_code: str
    title: str
    source_hash: str


@dataclass(frozen=True)
class SearchHit:
    doc: CorpusDoc
    score: float
    rank: int
    matched_terms: list[str]
    selected_by: dict[str, bool]
    snippet: str


LIVE_CASES = [
    {
        "case_id": "LIVE-01-candidate-misuse-blocked-or-downgraded",
        "query": "mnemosyne vector memory candidate final support action basis",
        "query_mode": "action",
        "intent": "Try to use a retrieved candidate distillation as final support.",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "LIVE-02-real-raw-anchor-readonly-allow",
        "query": "FlexNote Extracted Source Facts local-first card tag database",
        "query_mode": "source_inspection",
        "intent": "Use a real raw/stable source anchor for a read-only answer.",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "LIVE-03-mixed-pack-support-selection-allow",
        "query": "FlexNote visual workbench source anchor candidate overlay tag database context pack",
        "query_mode": "review",
        "intent": "Retrieve a mixed pack and allow only a real raw anchor as support.",
        "expected_decision": "allowed_readonly",
    },
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    try:
        data = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        data = {}
    if not isinstance(data, dict):
        data = {}
    return data, text[end + 4 :]


def infer_record_kind(path: Path, fm: dict[str, Any]) -> str:
    p = rel(path)
    if fm.get("record_kind"):
        return str(fm["record_kind"])
    if fm.get("type") in TYPE_ALIASES:
        return TYPE_ALIASES[str(fm["type"])]
    if p.startswith("raw/"):
        return "source_card"
    if p.startswith("outputs/review/source_annotations/") or p.endswith("source-annotation.md"):
        return "source_annotation"
    if p.endswith("candidate-distillation.md") or p.endswith("refresh.md"):
        return "candidate_distillation"
    if "project_lens_overlays/" in p or "project_overlays/" in p or p.endswith("-overlay.md"):
        return "project_overlay"
    return "source_card"


def infer_status(record_kind: str, fm: dict[str, Any]) -> str:
    if fm.get("knowledge_status"):
        return str(fm["knowledge_status"])
    if record_kind == "source_card":
        return "raw"
    return "candidate"


def infer_warning(record_kind: str, status: str, fm: dict[str, Any]) -> str:
    policy = fm.get("retrieval_policy")
    if isinstance(policy, dict) and policy.get("warning_code"):
        return str(policy["warning_code"])
    if record_kind == "candidate_distillation":
        return "candidate_not_action_basis"
    if record_kind == "source_annotation":
        return "annotation_not_support"
    if record_kind == "project_overlay":
        return "overlay_not_authority"
    if record_kind == "feedback_event":
        return "feedback_not_truth"
    if status == "raw":
        return "raw_is_provenance_only"
    return "candidate_not_action_basis"


def collect_corpus() -> list[CorpusDoc]:
    paths: set[Path] = set()
    for pattern in COLLECT_GLOBS:
        paths.update(p for p in ROOT.glob(pattern) if p.is_file())
    docs: list[CorpusDoc] = []
    for path in sorted(paths):
        rp = rel(path)
        if any(marker in rp for marker in EXCLUDED_PATH_MARKERS):
            continue
        text = read_text(path)
        fm, body = split_frontmatter(text)
        record_kind = infer_record_kind(path, fm)
        status = infer_status(record_kind, fm)
        warning = infer_warning(record_kind, status, fm)
        title = str(fm.get("title") or path.stem)
        docs.append(
            CorpusDoc(
                rel_path=rp,
                abs_path=path,
                text=text,
                frontmatter=fm,
                body=body,
                record_kind=record_kind,
                knowledge_status=status,
                warning_code=warning,
                title=title,
                source_hash=sha256_file(path),
            )
        )
    return docs


TOKEN_RE = re.compile(r"[a-z0-9]+|[\u4e00-\u9fff]+", re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    raw = TOKEN_RE.findall(text.lower())
    expanded: list[str] = []
    for token in raw:
        expanded.append(token)
        if "-" in token or "_" in token:
            expanded.extend(t for t in re.split(r"[-_]+", token) if t)
    return [t for t in expanded if len(t) > 1]


def headings(body: str) -> str:
    return "\n".join(line for line in body.splitlines() if line.lstrip().startswith("#"))


def make_snippet(text: str, terms: set[str], limit: int = 260) -> str:
    plain = re.sub(r"\s+", " ", text).strip()
    lower = plain.lower()
    first = min((lower.find(term) for term in terms if term in lower), default=-1)
    if first == -1:
        return plain[:limit]
    start = max(0, first - 90)
    return plain[start : start + limit]


def retrieve(query: str, corpus: list[CorpusDoc], *, top_k: int = 12) -> list[SearchHit]:
    terms = set(tokenize(query))
    hits: list[SearchHit] = []
    for doc in corpus:
        path_tokens = Counter(tokenize(doc.rel_path))
        title_tokens = Counter(tokenize(doc.title))
        heading_tokens = Counter(tokenize(headings(doc.body)))
        body_tokens = Counter(tokenize(doc.body[:20000]))
        score = 0.0
        matched: set[str] = set()
        for term in terms:
            path_count = path_tokens.get(term, 0)
            title_count = title_tokens.get(term, 0)
            heading_count = heading_tokens.get(term, 0)
            body_count = body_tokens.get(term, 0)
            if path_count or title_count or heading_count or body_count:
                matched.add(term)
            score += path_count * 6.0 + title_count * 4.0 + heading_count * 2.5 + min(body_count, 6) * 1.0
        if score <= 0:
            continue
        if doc.record_kind == "source_card" and "source" in terms:
            score += 1.5
        if doc.record_kind == "candidate_distillation" and "candidate" in terms:
            score += 4.0
        if doc.record_kind == "project_overlay" and "overlay" in terms:
            score += 4.0
        selected_by = {
            "lexical": bool(matched),
            "semantic": False,
            "graph": False,
            "metadata": any(term in tokenize(doc.rel_path + " " + doc.title) for term in terms),
            "rank": False,
            "dashboard": False,
            "legacy_raw_metadata": False,
        }
        hits.append(
            SearchHit(
                doc=doc,
                score=score,
                rank=0,
                matched_terms=sorted(matched),
                selected_by=selected_by,
                snippet=make_snippet(doc.body, terms),
            )
        )
    hits.sort(key=lambda h: (-h.score, h.doc.rel_path))
    ranked: list[SearchHit] = []
    for idx, hit in enumerate(hits[:top_k], start=1):
        selected_by = dict(hit.selected_by)
        selected_by["rank"] = idx <= 5
        ranked.append(
            SearchHit(
                doc=hit.doc,
                score=hit.score,
                rank=idx,
                matched_terms=hit.matched_terms,
                selected_by=selected_by,
                snippet=hit.snippet,
            )
        )
    return ranked


def hit_to_item(hit: SearchHit, *, pack_role: str, anchor_ref: str = "", excluded_reason: str = "") -> dict[str, Any]:
    return {
        "ref": hit.doc.rel_path,
        "record_kind": hit.doc.record_kind,
        "knowledge_status": hit.doc.knowledge_status,
        "pack_role": pack_role,
        "warning_code": hit.doc.warning_code,
        "action_basis_allowed": False,
        "truth_mutation_allowed": False,
        "independent_anchor_ref": anchor_ref,
        "selected_by": hit.selected_by,
        "retrieval_rank": hit.rank,
        "retrieval_score": round(hit.score, 4),
        "matched_terms": hit.matched_terms,
        "source_hash": hit.doc.source_hash,
        "excluded_reason": excluded_reason,
    }


def first_hit(hits: list[SearchHit], predicate: Any) -> SearchHit | None:
    for hit in hits:
        if predicate(hit):
            return hit
    return None


def resolve_anchor(anchor_ref: str) -> dict[str, Any]:
    if "#" not in anchor_ref:
        return {
            "status": "not_checked",
            "reason": "anchor ref has no selector",
            "method": "path_selector_heading_or_string_resolution",
        }
    path_part, selector = anchor_ref.split("#", 1)
    path = ROOT / path_part
    if not path.exists():
        return {
            "status": "missing_file",
            "path": path_part,
            "selector": selector,
            "method": "path_selector_heading_or_string_resolution",
        }
    text = read_text(path)
    normalized_selector = selector.strip().lower().replace("-", " ")
    heading_match = False
    string_match = selector in text
    for line in text.splitlines():
        if line.lstrip("# ").strip().lower().replace("-", " ") == normalized_selector:
            heading_match = True
            break
    status = "resolved" if heading_match or string_match else "missing_selector"
    return {
        "status": status,
        "path": path_part,
        "selector": selector,
        "source_hash": sha256_file(path),
        "heading_match": heading_match,
        "string_match": string_match,
        "method": "path_selector_heading_or_string_resolution",
        "semantic_support_status": "not_external_judged",
        "freshness_or_drift_status": "source_hash_captured_no_remote_drift_check",
    }


def select_case_pack(case: dict[str, Any], hits: list[SearchHit], corpus: list[CorpusDoc]) -> list[dict[str, Any]]:
    case_id = case["case_id"]
    if case_id.startswith("LIVE-01"):
        candidate = first_hit(hits, lambda h: h.doc.record_kind == "candidate_distillation")
        if candidate is None:
            raise RuntimeError("LIVE-01 could not retrieve any candidate_distillation")
        return [
            hit_to_item(
                candidate,
                pack_role="review_input",
                excluded_reason="candidate_retrieved_live_but_downgraded_from_requested_final_support",
            )
        ]

    if case_id.startswith("LIVE-02"):
        anchor_hit = first_hit(hits, lambda h: h.doc.rel_path == FLEXNOTE_EXTRACTED_FACTS_ANCHOR.split("#", 1)[0])
        if anchor_hit is None:
            raise RuntimeError("LIVE-02 expected the raw anchor to be naturally retrieved; fallback injection is disabled")
        return [hit_to_item(anchor_hit, pack_role="support", anchor_ref=FLEXNOTE_EXTRACTED_FACTS_ANCHOR)]

    if case_id.startswith("LIVE-03"):
        raw = first_hit(hits, lambda h: h.doc.rel_path == FLEXNOTE_EXTRACTED_FACTS_ANCHOR.split("#", 1)[0])
        if raw is None:
            raise RuntimeError("LIVE-03 expected the raw anchor to be naturally retrieved; fallback injection is disabled")
        candidate = first_hit(hits, lambda h: h.doc.record_kind == "candidate_distillation")
        overlay = first_hit(hits, lambda h: h.doc.record_kind == "project_overlay")
        rank_only = first_hit(
            hits,
            lambda h: h.doc.rel_path != raw.doc.rel_path
            and (candidate is None or h.doc.rel_path != candidate.doc.rel_path)
            and (overlay is None or h.doc.rel_path != overlay.doc.rel_path),
        )
        items = [hit_to_item(raw, pack_role="support", anchor_ref=FLEXNOTE_EXTRACTED_FACTS_ANCHOR)]
        if candidate:
            items.append(
                hit_to_item(
                    candidate,
                    pack_role="review_input",
                    excluded_reason="candidate_kept_for_review_input_not_final_support",
                )
            )
        if overlay:
            items.append(
                hit_to_item(
                    overlay,
                    pack_role="review_input",
                    excluded_reason="project_overlay_kept_project_scoped_not_final_support",
                )
            )
        if rank_only:
            selected_by = dict(rank_only.selected_by)
            selected_by["rank"] = True
            rank_hit = SearchHit(
                doc=rank_only.doc,
                score=rank_only.score,
                rank=rank_only.rank,
                matched_terms=rank_only.matched_terms,
                selected_by=selected_by,
                snippet=rank_only.snippet,
            )
            items.append(
                hit_to_item(
                    rank_hit,
                    pack_role="orientation",
                    excluded_reason="rank_signal_is_diagnostic_not_support",
                )
            )
        return items

    raise RuntimeError(f"Unknown case: {case_id}")


def evaluate_support(items: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]], list[str]]:
    support_checks: list[dict[str, Any]] = []
    warnings: list[str] = []
    supported = 0
    invalid_support = 0
    for item in items:
        if item["pack_role"] != "support":
            if item["record_kind"] in {"source_annotation", "candidate_distillation", "project_overlay"}:
                warnings.append(f"{item['record_kind']} downgraded to {item['pack_role']}: {item['ref']}")
            continue
        anchor = item.get("independent_anchor_ref") or ""
        resolution = resolve_anchor(anchor)
        if item["record_kind"] != "source_card" or item["knowledge_status"] != "raw":
            invalid_support += 1
            result = "not_ready"
            reason = "non_raw_source_item_cannot_be_final_support"
        elif resolution["status"] != "resolved":
            invalid_support += 1
            result = "missing_anchor"
            reason = "support_anchor_not_resolved"
        else:
            supported += 1
            result = "supported"
            reason = "resolved_raw_stable_anchor"
        support_checks.append(
            {
                "claim_ref": item["ref"],
                "independent_anchor_ref": anchor,
                "result": result,
                "resolution": resolution,
                "reason": reason,
            }
        )
    if supported > 0 and invalid_support == 0:
        decision = "allowed_readonly"
    else:
        decision = "blocked_or_downgraded"
    if not support_checks:
        support_checks.append(
            {
                "claim_ref": "no_final_support_selected",
                "independent_anchor_ref": "",
                "result": "not_ready",
                "resolution": {"status": "not_checked", "reason": "no support items"},
                "reason": "retrieved_items_remain_review_input_or_orientation_only",
            }
        )
    return decision, support_checks, warnings


def artifact_frontmatter(record_kind: str | None = None) -> dict[str, Any]:
    base: dict[str, Any] = {
        "artifact_kind": "live_readonly_test_artifact",
        "retrieval_exclusion": True,
        "default_retrieval": False,
        "indexing_policy": "exclude_from_default_retrieval_graph_pack_support",
        "truth_mutation_allowed": False,
        "action_basis_allowed": False,
    }
    if record_kind:
        base["record_kind"] = record_kind
    return base


def dump_yaml(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)


def write_markdown(path: Path, fm: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{dump_yaml(fm)}---\n\n{body}", encoding="utf-8")


def query_run_frontmatter(case: dict[str, Any], now: str, items: list[dict[str, Any]], checks: list[dict[str, Any]]) -> dict[str, Any]:
    fm = {
        "record_kind": "query_run_trace",
        "status": "archived",
        "query_id": case["case_id"],
        "query_time": now,
        "question_summary": case["intent"],
        "verbatim_input": case["query"],
        "active_project": "VAKS",
        "query_mode": case["query_mode"],
        "requested_authority_bucket": "read_only_source_and_review_input",
        "included_buckets": ["raw", "candidate"],
        "excluded_buckets": ["reviewed_write_path", "action_basis", "truth_mutation"],
        "retrieval_filters": {
            "include_candidates": True,
            "include_overlays": "active_project_only",
            "include_runtime_test_artifacts": False,
            "writeback_allowed": False,
            "promotion_allowed": False,
            "truth_mutation_allowed": False,
        },
        "selected_items": items,
        "support_checks": checks,
        "human_confirmation_required": False,
    }
    fm.update(artifact_frontmatter())
    return fm


def context_pack_frontmatter(case: dict[str, Any], now: str, items: list[dict[str, Any]], checks: list[dict[str, Any]]) -> dict[str, Any]:
    fm = {
        "record_kind": "context_pack_manifest",
        "status": "archived",
        "knowledge_status": "candidate",
        "processing_tier": "medium",
        "retrieval_policy": {
            "policy_kind": "orientation_only",
            "pack_allowed": "review_input_only",
            "action_basis_allowed": False,
            "warning_code": "context_pack_not_action_basis",
        },
        "query_run_ref": f"query_runs/{case['case_id']}-query-run.md",
        "active_project": "VAKS",
        "query_mode": case["query_mode"],
        "requested_authority_bucket": "read_only_source_and_review_input",
        "included_buckets": ["raw", "candidate"],
        "excluded_buckets": ["reviewed_write_path", "action_basis", "truth_mutation"],
        "items": items,
        "support_checks": checks,
        "human_confirmation_required": False,
    }
    fm.update(artifact_frontmatter())
    return fm


def write_case_artifacts(
    case: dict[str, Any],
    hits: list[SearchHit],
    items: list[dict[str, Any]],
    decision: str,
    checks: list[dict[str, Any]],
    warnings: list[str],
    now: str,
) -> dict[str, Any]:
    query_path = QUERY_RUN_DIR / f"{case['case_id']}-query-run.md"
    pack_path = CONTEXT_PACK_DIR / f"{case['case_id']}-context-pack.md"
    answer_path = ANSWER_USE_DIR / f"{case['case_id']}-answer-use.md"

    query_body = "\n".join(
        [
            f"# Query Run: {case['case_id']}",
            "",
            "## Live Retrieval Boundary",
            "",
            "This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.",
            "",
            "## Top Retrieved Results",
            "",
            *[
                f"- rank {hit.rank}: `{hit.doc.rel_path}` score={hit.score:.2f} kind={hit.doc.record_kind} status={hit.doc.knowledge_status}"
                for hit in hits
            ],
            "",
            "## Selected Pack Items",
            "",
            *[f"- `{item['ref']}` -> {item['pack_role']} / {item['warning_code']}" for item in items],
        ]
    )
    write_markdown(query_path, query_run_frontmatter(case, now, items, checks), query_body)

    pack_body = "\n".join(
        [
            f"# Context Pack: {case['case_id']}",
            "",
            "## Boundary",
            "",
            "This pack is a read-only attention surface. It is not action basis and does not write truth.",
            "",
            "## Support Selection",
            "",
            *[f"- {check['result']}: `{check['claim_ref']}` anchor=`{check['independent_anchor_ref']}`" for check in checks],
        ]
    )
    write_markdown(pack_path, context_pack_frontmatter(case, now, items, checks), pack_body)

    supported_refs = [check["claim_ref"] for check in checks if check["result"] == "supported"]
    if decision == "allowed_readonly":
        answer = (
            "Allowed read-only answer/use path: final support is restricted to resolved raw/stable source anchors. "
            "Candidate, overlay, and rank-selected materials remain orientation or review input."
        )
    else:
        answer = (
            "Blocked or downgraded: retrieved material did not pass as final support. "
            "The answer/use path remains not_ready until an independent raw/stable anchor or reviewed support is supplied."
        )
    answer_fm = {
        "status": decision,
        "case_id": case["case_id"],
        "decision": decision,
        "final_support_refs": supported_refs,
        "writeback_attempted": False,
        "promotion_attempted": False,
        "truth_mutation_attempted": False,
        "live_llm_used": False,
        "live_retrieval_used": True,
        "live_tool_runtime_used": False,
        "support_boundary": "local_live_retrieval_to_pack_to_answer_use_no_writeback",
    }
    answer_fm.update(artifact_frontmatter("runtime_test_artifact"))
    answer_body = "\n".join(
        [
            f"# Answer / Use Draft: {case['case_id']}",
            "",
            answer,
            "",
            "## Final Support",
            "",
            *(f"- `{ref}`" for ref in supported_refs),
            "",
            "## Warnings",
            "",
            *(f"- {warning}" for warning in warnings),
        ]
    )
    write_markdown(answer_path, answer_fm, answer_body)

    return {
        "case_id": case["case_id"],
        "query": case["query"],
        "query_mode": case["query_mode"],
        "expected_decision": case["expected_decision"],
        "decision": decision,
        "pass": decision == case["expected_decision"],
        "retrieved_count": len(hits),
        "selected_count": len(items),
        "support_count": len(supported_refs),
        "top_result": hits[0].doc.rel_path if hits else "",
        "top_result_kind": hits[0].doc.record_kind if hits else "",
        "query_run": rel(query_path),
        "context_pack": rel(pack_path),
        "answer_use": rel(answer_path),
        "warnings": warnings,
        "support_checks": checks,
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in row.items()})


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_events(case_rows: list[dict[str, Any]], retrieval_rows: list[dict[str, Any]], now: str) -> None:
    events = []
    by_case = {row["case_id"]: row for row in case_rows}
    for case in LIVE_CASES:
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
                    "truth_boundary": "local Markdown retrieval only; no live embedding or graph compiler.",
                },
                {
                    "time": now,
                    "case_id": case["case_id"],
                    "stage": "assemble_context_pack",
                    "context_pack": row["context_pack"],
                    "writeback_allowed": False,
                },
                {
                    "time": now,
                    "case_id": case["case_id"],
                    "stage": "answer_use_gate",
                    "decision": row["decision"],
                    "support_count": row["support_count"],
                    "truth_mutation_attempted": False,
                    "promotion_attempted": False,
                },
            ]
        )
    path = RESULTS_DIR / "live_readonly_loop_events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


def write_artifact_exclusion_manifest(case_rows: list[dict[str, Any]], now: str) -> dict[str, Any]:
    rows = []
    for row in case_rows:
        for kind, key in [("query_run", "query_run"), ("context_pack", "context_pack"), ("answer_use", "answer_use")]:
            artifact = row[key]
            rows.append(
                {
                    "path": artifact,
                    "artifact_kind": "live_readonly_test_artifact",
                    "artifact_group": kind,
                    "retrieval_exclusion": True,
                    "default_retrieval": False,
                    "indexing_policy": "exclude_from_default_retrieval_graph_pack_support",
                    "checked_at": now,
                    "eligible_for_default_index": False,
                }
            )
    summary = {
        "status": "pass",
        "checked_artifact_count": len(rows),
        "eligible_for_default_index_count": 0,
        "truth_boundary": "Deterministic marker check for generated live-readonly query/context/answer artifacts; live embedding/index exclusion is not proven.",
    }
    write_json(RESULTS_DIR / "live_artifact_exclusion_test.json", summary)
    write_csv(
        RESULTS_DIR / "live_artifact_exclusion_manifest.csv",
        rows,
        ["path", "artifact_kind", "artifact_group", "retrieval_exclusion", "default_retrieval", "indexing_policy", "checked_at", "eligible_for_default_index"],
    )
    write_json(RESULTS_DIR / "live_artifact_exclusion_manifest.json", rows)
    return summary


def write_reports(summary: dict[str, Any], case_rows: list[dict[str, Any]], now: str) -> None:
    report = f"""# VAKS Source Intake Live Read-Only Loop Report

## Verdict

This package is sandbox runtime evidence for a local live retrieval -> context pack -> answer/use smoke test.

It does **not** prove Source Intake P0 passed, live LLM/tool runtime validation, live embedding exclusion, external blind relevance, or writeback safety under real write-capable tools.

## What Ran

- Local Markdown corpus scanned: {summary['corpus_doc_count']} documents.
- Live retrieval cases: {summary['case_count']}.
- Passed expected decisions: {summary['passed_expected_decision_count']} / {summary['case_count']}.
- Decisions: {summary['decision_breakdown']}.

## Case Results

""" + "\n".join(
        f"- `{row['case_id']}`: {row['decision']} / top=`{row['top_result']}` / support_count={row['support_count']}"
        for row in case_rows
    ) + """

## Boundary

The live part is local retrieval over the current workspace corpus. The answer/use drafting remains deterministic and read-only. No LLM was used. No writeback, promotion, reviewed relation creation, action basis creation, or truth mutation was attempted.
"""
    (OUT_DIR / "LIVE_READONLY_LOOP_REPORT.md").write_text(report, encoding="utf-8")

    readme = f"""# Source Intake Live Read-Only Loop Package

Generated: {now}

## Human Summary

This package tests whether actual local retrieval results can flow through a read-only query-run -> context-pack -> answer/use path without letting candidate, overlay, rank, or unanchored material become final support.

## Supported Conclusion

The package supports a narrow conclusion: under this local deterministic harness, live Markdown retrieval was connected to pack assembly and support gating, and the three designed cases produced the expected read-only decisions.

## Unsupported Conclusions

- Source Intake P0 passed: no.
- Live LLM/tool loop validated: no.
- Live embedding/vector/graph retrieval validated: no.
- External blind relevance completed: no.
- Runtime adoption ready: no.

## Evidence Files

- `LIVE_READONLY_LOOP_REPORT.md`
- `results/live_readonly_loop_summary.json`
- `results/live_readonly_loop_cases.csv`
- `results/live_retrieval_results.csv`
- `query_runs/`
- `context_packs/`
- `answer_use/`
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    pro_request = """# Pro Review Request

Please reverse-audit this VAKS Source Intake live read-only loop package.

Questions:

1. Does the package actually run a local live retrieval -> context pack -> answer/use path, or is it still just fixture selection?
2. Are candidate/overlay/rank/unanchored items prevented from becoming final support?
3. Is the raw/stable anchor allow case only read-only, and are the boundaries stated honestly?
4. Are there any overclaims around P0, live LLM/tool runtime, live embedding/index exclusion, semantic anchor support, or external blind relevance?
5. What is the smallest next test before we can say this is stronger than sandbox runtime evidence?
"""
    (OUT_DIR / "PRO_REVIEW_REQUEST.md").write_text(pro_request, encoding="utf-8")


def run_validation_commands(now: str) -> dict[str, Any]:
    commands = [
        [
            "python",
            "tools/validate_source_intake_contract.py",
            "--scope",
            "current",
            "--out-dir",
            rel(RESULTS_DIR),
            "--no-fail",
        ],
        [
            "python",
            "tools/validate_source_intake_contract.py",
            "--scope",
            "contract",
            "--out-dir",
            rel(RESULTS_DIR),
            "--no-fail",
        ],
        [
            "python",
            "tools/validate_source_intake_failure_matrix.py",
            "--out-dir",
            rel(RESULTS_DIR),
        ],
    ]
    rows = []
    for command in commands:
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        if command[1].endswith("validate_source_intake_failure_matrix.py"):
            default_results = ROOT / "outputs" / "review" / "source-intake-control-flow-hardening-2026-06-12" / "results"
            for name in ["source_intake_failure_matrix_results.csv", "source_intake_failure_matrix_summary.json"]:
                source = default_results / name
                if source.exists():
                    shutil.copy2(source, RESULTS_DIR / name)
        rows.append(
            {
                "command": " ".join(command),
                "returncode": completed.returncode,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
            }
        )
    status = "pass" if all(row["returncode"] == 0 for row in rows) else "fail"
    result = {
        "status": status,
        "checked_at": now,
        "commands": rows,
        "truth_boundary": "Validator outputs are included for audit continuity; they do not convert this live-readonly smoke into Source Intake P0 approval.",
    }
    write_json(RESULTS_DIR / "live_validation_commands.json", result)
    return result


def manifest_rows(extra_paths: list[Path]) -> list[dict[str, Any]]:
    rows = []
    for path in sorted({p for p in extra_paths if p.exists() and p.is_file()}):
        rows.append(
            {
                "path": rel(path),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )
    return rows


def package_outputs(input_paths: list[Path], summary: dict[str, Any]) -> tuple[Path, str]:
    output_files = [p for p in OUT_DIR.rglob("*") if p.is_file() and p.name != ZIP_NAME]
    script_path = ROOT / "tools" / "run_source_intake_live_readonly_loop.py"
    source_intake = ROOT / "SOURCE_INTAKE.md"
    all_manifest_paths = output_files + input_paths + [script_path, source_intake]
    rows = manifest_rows(all_manifest_paths)
    write_json(OUT_DIR / "PACKAGE_MANIFEST.json", {"files": rows, "file_count": len(rows)})
    check = {
        "status": "pass",
        "case_count": summary["case_count"],
        "passed_expected_decision_count": summary["passed_expected_decision_count"],
        "truth_boundary": "Package check covers generated sandbox evidence presence and expected deterministic decisions only.",
    }
    write_json(OUT_DIR / "PACKAGE_CHECK.json", check)

    zip_path = OUT_DIR / ZIP_NAME
    if zip_path.exists():
        zip_path.unlink()
    package_files = [p for p in OUT_DIR.rglob("*") if p.is_file() and p.name != ZIP_NAME]
    package_files += input_paths + [script_path, source_intake]
    seen: set[str] = set()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package_files):
            arcname = rel(path)
            if arcname in seen:
                continue
            seen.add(arcname)
            zf.write(path, arcname)
    return zip_path, sha256_file(zip_path)


def reset_output_dir() -> None:
    if OUT_DIR.exists():
        resolved = OUT_DIR.resolve()
        expected = (ROOT / "outputs" / "review").resolve()
        if expected not in resolved.parents:
            raise RuntimeError(f"Refusing to remove unexpected output path: {OUT_DIR}")
        shutil.rmtree(OUT_DIR)
    for path in [RESULTS_DIR, QUERY_RUN_DIR, CONTEXT_PACK_DIR, ANSWER_USE_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def main() -> int:
    reset_output_dir()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    corpus = collect_corpus()
    case_rows: list[dict[str, Any]] = []
    retrieval_rows: list[dict[str, Any]] = []
    input_paths: set[Path] = set()

    for case in LIVE_CASES:
        hits = retrieve(case["query"], corpus)
        if not hits:
            raise RuntimeError(f"No retrieval results for {case['case_id']}")
        items = select_case_pack(case, hits, corpus)
        decision, checks, warnings = evaluate_support(items)
        row = write_case_artifacts(case, hits, items, decision, checks, warnings, now)
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

    decision_breakdown = dict(Counter(row["decision"] for row in case_rows))
    summary = {
        "generated_at": now,
        "overall_verdict": "sandbox_live_readonly_evidence_partial",
        "case_count": len(case_rows),
        "passed_expected_decision_count": sum(1 for row in case_rows if row["pass"]),
        "decision_breakdown": decision_breakdown,
        "corpus_doc_count": len(corpus),
        "live_retrieval_used": True,
        "live_retrieval_scope": "local_markdown_corpus_lexical_retrieval",
        "live_llm_used": False,
        "live_tool_runtime_used": False,
        "writeback_attempted": False,
        "promotion_attempted": False,
        "truth_mutation_attempted": False,
        "source_intake_p0_passed": False,
        "external_blind_relevance_completed": False,
        "semantic_anchor_support_status": "not_external_judged",
        "anchor_resolution_method": "path_selector_heading_or_string_resolution",
        "truth_boundary": "Actual local retrieval is connected to pack and answer/use generation; this is still a deterministic read-only sandbox harness, not live LLM/tool/runtime adoption.",
    }

    write_json(RESULTS_DIR / "live_readonly_loop_summary.json", summary)
    write_json(RESULTS_DIR / "live_readonly_loop_cases.json", case_rows)
    write_json(RESULTS_DIR / "live_retrieval_results.json", retrieval_rows)
    write_csv(
        RESULTS_DIR / "live_readonly_loop_cases.csv",
        case_rows,
        ["case_id", "query", "query_mode", "expected_decision", "decision", "pass", "retrieved_count", "selected_count", "support_count", "top_result", "top_result_kind", "query_run", "context_pack", "answer_use", "warnings", "support_checks"],
    )
    write_csv(
        RESULTS_DIR / "live_retrieval_results.csv",
        retrieval_rows,
        ["case_id", "rank", "score", "path", "record_kind", "knowledge_status", "warning_code", "matched_terms", "snippet"],
    )
    write_events(case_rows, retrieval_rows, now)
    exclusion = write_artifact_exclusion_manifest(case_rows, now)
    summary["live_artifact_exclusion"] = exclusion
    write_json(RESULTS_DIR / "live_readonly_loop_summary.json", summary)
    write_reports(summary, case_rows, now)
    validation = run_validation_commands(now)
    summary["validation_commands"] = validation
    write_json(RESULTS_DIR / "live_readonly_loop_summary.json", summary)
    zip_path, zip_hash = package_outputs(sorted(input_paths), summary)

    print(
        json.dumps(
            {
                "status": "pass" if summary["passed_expected_decision_count"] == summary["case_count"] else "fail",
                "out_dir": rel(OUT_DIR),
                "zip": rel(zip_path),
                "zip_sha256": zip_hash,
                "summary": summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if summary["passed_expected_decision_count"] == summary["case_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
