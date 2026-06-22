#!/usr/bin/env python
"""Shared helpers for Source Intake read-only loop evidence packages.

This module intentionally contains no live-case definitions, known-anchor fallback,
forced-hit helper, package runner, or production runtime claims. It is a shared
sandbox utility layer for local Markdown lexical retrieval, artifact writing,
anchor resolution, and validation command wrappers.
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
OUT_DIR = ROOT / "outputs" / "review" / "source-intake-readonly-shared"
RESULTS_DIR = OUT_DIR / "results"
QUERY_RUN_DIR = OUT_DIR / "query_runs"
CONTEXT_PACK_DIR = OUT_DIR / "context_packs"
ANSWER_USE_DIR = OUT_DIR / "answer_use"
ZIP_NAME = "source-intake-readonly-shared.zip"


COLLECT_GLOBS = [
    "raw/**/*.md",
    "outputs/review/*candidate-distillation.md",
    "outputs/review/*refresh.md",
    "outputs/review/source_annotations/**/*.md",
    "outputs/review/project_lens_overlays/*.md",
    "outputs/review/project_overlays/**/*.md",
    "wiki/summaries/2026-05-26-llm-wiki-architecture-review.md",
]

EXCLUDED_PATH_MARKERS = [
    "outputs/review/source-intake-runtime-readonly-loop-",
    "outputs/review/source-intake-live-readonly-loop-",
    "outputs/review/source-intake-control-flow-hardening-",
    "outputs/review/vaks-yuxi-fusion-pro-package-",
    "outputs/review/vaks-yuxi-phase-b-pressure-test-",
    "outputs/review/project_overlays/_runtime_test_fixtures/",
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
    if p.startswith("wiki/") and str(fm.get("status", "")).lower() == "reviewed":
        return "reviewed_material"
    if p.endswith("candidate-distillation.md") or p.endswith("refresh.md"):
        return "candidate_distillation"
    if "project_lens_overlays/" in p or "project_overlays/" in p or p.endswith("-overlay.md"):
        return "project_overlay"
    return "source_card"


def infer_status(record_kind: str, fm: dict[str, Any]) -> str:
    if fm.get("knowledge_status"):
        return str(fm["knowledge_status"])
    if str(fm.get("status", "")).lower() == "reviewed":
        return "reviewed"
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
    if record_kind == "reviewed_material":
        return "reviewed_material_context_only_in_sandbox"
    if record_kind == "feedback_event":
        return "feedback_not_truth"
    if status == "raw":
        return "raw_is_provenance_only"
    return "candidate_not_action_basis"


def authority_bucket(record_kind: str, knowledge_status: str) -> str:
    """Classify intake surfaces into retrieval authority buckets."""
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


def doc_authority_bucket(doc: CorpusDoc) -> str:
    return authority_bucket(doc.record_kind, doc.knowledge_status)


def query_policy_for_case(case: dict[str, Any]) -> dict[str, Any]:
    """Build a small authority-first QueryPolicy for the sandbox runner.

    This is a receipt contract, not production query planning. It intentionally
    keeps retrieval local/lexical while making bucket and role eligibility
    explicit before ranking.
    """
    query_mode = str(case.get("query_mode", "orientation"))
    readonly_support_mode = query_mode in {"source_inspection", "review"}
    risk_tier = "high" if query_mode == "action" else "medium" if query_mode == "review" else "low"
    default_allowed_buckets = [
        "reviewed",
        "raw_anchor",
        "candidate",
        "overlay",
        "source_annotation",
    ]
    allowed_buckets = case.get("allowed_authority_buckets_override") or case.get("allowed_authority_buckets") or default_allowed_buckets
    allowed_buckets = [str(bucket) for bucket in allowed_buckets]
    default_support_candidate_buckets = ["raw_anchor"] if readonly_support_mode else []
    support_candidate_buckets = (
        case.get("support_candidate_authority_buckets_override")
        or case.get("support_candidate_authority_buckets")
        or default_support_candidate_buckets
    )
    support_candidate_buckets = [str(bucket) for bucket in support_candidate_buckets if str(bucket) in allowed_buckets]
    allowed_roles = ["orientation", "review_input", "diagnostic"]
    if support_candidate_buckets:
        allowed_roles.append("support_candidate")
    policy_variant = str(case.get("policy_variant") or "default")
    return {
        "policy_id": str(case.get("query_policy_id") or f"qp-{query_mode}-{policy_variant}-authority-first-local-lexical-v1"),
        "policy_version": "2026-06-15-pro-retrieval-plane-step1",
        "use_mode": query_mode,
        "risk_tier": risk_tier,
        "intent": case.get("intent", ""),
        "authority_filter_mode": "bucket_first_before_ranking",
        "allowed_authority_buckets": allowed_buckets,
        "support_candidate_authority_buckets": support_candidate_buckets,
        "allowed_roles": allowed_roles,
        "retrieval_channels": ["local_lexical"],
        "disabled_channels": ["dense_vector", "sparse_semantic", "graph_overlay", "rrf_hybrid_fusion", "second_stage_rerank"],
        "fusion_method": "none_single_local_lexical_channel",
        "fusion_scope": "within_authority_bucket_only_when_multiple_channels_exist",
        "rerank_method": "none",
        "max_hops": 0,
        "enable_graph": False,
        "enable_expansion": False,
        "needs_claim_binding": query_mode in {"review", "action"},
        "writeback_allowed": False,
        "promotion_allowed": False,
        "truth_mutation_allowed": False,
    }


def filter_corpus_by_query_policy(corpus: list[CorpusDoc], policy: dict[str, Any]) -> tuple[list[CorpusDoc], dict[str, Any]]:
    allowed = set(policy.get("allowed_authority_buckets") or [])
    before = Counter(doc_authority_bucket(doc) for doc in corpus)
    included: list[CorpusDoc] = []
    excluded: list[CorpusDoc] = []
    for doc in corpus:
        if doc_authority_bucket(doc) in allowed:
            included.append(doc)
        else:
            excluded.append(doc)
    after = Counter(doc_authority_bucket(doc) for doc in included)
    excluded_counts = Counter(doc_authority_bucket(doc) for doc in excluded)
    receipt = {
        "authority_filter_mode": policy.get("authority_filter_mode"),
        "pre_filter_doc_count": len(corpus),
        "post_filter_doc_count": len(included),
        "excluded_doc_count": len(excluded),
        "pre_filter_bucket_counts": dict(before),
        "post_filter_bucket_counts": dict(after),
        "excluded_bucket_counts": dict(excluded_counts),
        "excluded_path_sample": [doc.rel_path for doc in excluded[:10]],
    }
    return included, receipt


def retrieve_with_query_policy(
    case: dict[str, Any],
    corpus: list[CorpusDoc],
    *,
    top_k: int = 12,
) -> tuple[dict[str, Any], dict[str, Any], list[SearchHit]]:
    policy = query_policy_for_case(case)
    filtered, receipt = filter_corpus_by_query_policy(corpus, policy)
    hits = retrieve(str(case["query"]), filtered, top_k=top_k)
    receipt.update(
        {
            "query_policy_id": policy["policy_id"],
            "retrieval_channels": policy["retrieval_channels"],
            "fusion_method": policy["fusion_method"],
            "rerank_method": policy["rerank_method"],
            "returned_hit_count": len(hits),
        }
    )
    return policy, receipt, hits


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
    bucket = doc_authority_bucket(hit.doc)
    support_eligibility = "eligible" if pack_role in {"support", "anchor"} else "ineligible"
    support_representation = "raw_excerpt" if pack_role in {"support", "anchor"} else "none"
    return {
        "ref": hit.doc.rel_path,
        "record_kind": hit.doc.record_kind,
        "knowledge_status": hit.doc.knowledge_status,
        "authority_bucket": bucket,
        "pack_role": pack_role,
        "retrieval_role": "support_candidate" if pack_role in {"support", "anchor"} else pack_role,
        "support_eligibility": support_eligibility,
        "eligibility_basis": [excluded_reason or ("resolved_raw_stable_anchor" if support_eligibility == "eligible" else "not_support_eligible")],
        "match_representation": "raw_markdown_lexical_match",
        "support_representation": support_representation,
        "retrieval_channels": ["local_lexical"],
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
    class NoAliasDumper(yaml.SafeDumper):
        def ignore_aliases(self, data: Any) -> bool:
            return True

    return yaml.dump(data, Dumper=NoAliasDumper, sort_keys=False, allow_unicode=True, width=120)


def write_markdown(path: Path, fm: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{dump_yaml(fm)}---\n\n{body}", encoding="utf-8")


def retrieval_filters_from_policy(policy: dict[str, Any]) -> dict[str, Any]:
    allowed_buckets = set(policy.get("allowed_authority_buckets") or [])
    include_overlays: bool | str = "active_project_only" if "overlay" in allowed_buckets else False
    return {
        "authority_bucket_filter_applied_before_ranking": True,
        "include_candidates": "candidate" in allowed_buckets,
        "include_overlays": include_overlays,
        "include_source_annotations": "source_annotation" in allowed_buckets,
        "include_runtime_test_artifacts": False,
        "writeback_allowed": False,
        "promotion_allowed": False,
        "truth_mutation_allowed": False,
    }


def query_run_frontmatter(case: dict[str, Any], now: str, items: list[dict[str, Any]], checks: list[dict[str, Any]]) -> dict[str, Any]:
    policy = case.get("query_policy") or query_policy_for_case(case)
    bucket_receipt = case.get("bucket_receipt") or {}
    fm = {
        "record_kind": "query_run_trace",
        "status": "archived",
        "query_id": case["case_id"],
        "query_time": now,
        "question_summary": case["intent"],
        "verbatim_input": case["query"],
        "active_project": "VAKS",
        "query_mode": case["query_mode"],
        "use_mode": policy.get("use_mode"),
        "risk_tier": policy.get("risk_tier"),
        "policy_ref": policy.get("policy_id"),
        "requested_authority_bucket": "authority_first_readonly_bucket_plan",
        "included_buckets": policy.get("allowed_authority_buckets", []),
        "excluded_buckets": ["reviewed_write_path", "action_basis", "truth_mutation"],
        "query_policy": policy,
        "retrieval_bucket_receipt": bucket_receipt,
        "retrieval_filters": retrieval_filters_from_policy(policy),
        "selected_items": items,
        "support_checks": checks,
        "human_confirmation_required": False,
    }
    fm.update(artifact_frontmatter())
    return fm


def context_pack_frontmatter(case: dict[str, Any], now: str, items: list[dict[str, Any]], checks: list[dict[str, Any]]) -> dict[str, Any]:
    policy = case.get("query_policy") or query_policy_for_case(case)
    bucket_receipt = case.get("bucket_receipt") or {}
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
        "use_mode": policy.get("use_mode"),
        "risk_tier": policy.get("risk_tier"),
        "policy_ref": policy.get("policy_id"),
        "requested_authority_bucket": "authority_first_readonly_bucket_plan",
        "included_buckets": policy.get("allowed_authority_buckets", []),
        "excluded_buckets": ["reviewed_write_path", "action_basis", "truth_mutation"],
        "query_policy": policy,
        "retrieval_bucket_receipt": bucket_receipt,
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
            "## Query Policy",
            "",
            f"- policy: `{(case.get('query_policy') or {}).get('policy_id', '')}`",
            f"- allowed authority buckets: `{', '.join((case.get('query_policy') or {}).get('allowed_authority_buckets', []))}`",
            f"- support candidate buckets: `{', '.join((case.get('query_policy') or {}).get('support_candidate_authority_buckets', []))}`",
            f"- retrieval channels: `{', '.join((case.get('query_policy') or {}).get('retrieval_channels', []))}`",
            "",
            "## Top Retrieved Results",
            "",
            *[
                f"- rank {hit.rank}: `{hit.doc.rel_path}` score={hit.score:.2f} bucket={doc_authority_bucket(hit.doc)} kind={hit.doc.record_kind} status={hit.doc.knowledge_status}"
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
    supported_anchor_refs = [check["independent_anchor_ref"] for check in checks if check["result"] == "supported"]
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
        "final_support_anchor_refs": supported_anchor_refs,
        "writeback_attempted": False,
        "promotion_attempted": False,
        "truth_mutation_attempted": False,
        "live_llm_used": False,
        "live_local_lexical_retrieval_used": True,
        "retrieval_scope": "local_markdown_corpus_lexical_retrieval",
        "live_tool_runtime_used": False,
        "support_boundary": "local_markdown_lexical_retrieval_to_pack_to_answer_use_no_writeback",
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
            *(
                f"- `{ref}` anchor=`{anchor}`"
                for ref, anchor in zip(supported_refs, supported_anchor_refs)
            ),
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


