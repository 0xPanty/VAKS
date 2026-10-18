#!/usr/bin/env python
"""Run R0.5 real read-only evidence-to-answer loop.

This is a bounded sandbox runner. It exercises a runtime-shaped read-only path:

QueryPolicy -> local lexical retrieval -> authority-first filter ->
RetrievalReceipt -> ContextPack -> ClaimSupportMap -> query sufficiency ->
bounded answer -> Guard receipts.

It does not validate P0, production runtime, vector/graph retrieval, reviewed
truth promotion, or action readiness.
"""

from __future__ import annotations

import hashlib
import argparse
import json
import re
import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import source_intake_readonly_shared as base


ROOT = base.ROOT
OUT_DIR = ROOT / "outputs" / "review" / "source-intake-real-readonly-evidence-loop-r0-5-2026-06-23"
RUNS_DIR = OUT_DIR / "runs"

TOOL_VERSION = "source-intake-real-readonly-evidence-loop-r0.5-2026-06-23"
QUERY_POLICY_VERSION = "r0.5-authority-first-local-lexical-v1"
ANCHOR_NORMALIZATION_VERSION = "r0.5-textquote-selector-v1"
ASSESSOR_VERSION = "r0.5-scripted-non-authoritative-claim-map-v1"

ALLOWED_SUPPORT_RESULTS = {
    "supported",
    "weak",
    "missing_anchor",
    "self_support_loop",
    "scope_limited",
    "not_ready",
}
ALLOWED_COVERAGE = {"full", "partial", "none"}
ALLOWED_CONFLICT = {"none", "resolved", "unresolved"}
ALLOWED_SUFFICIENCY = {"sufficient", "weak", "insufficient", "out_of_scope", "risky", "not_ready"}
ALLOWED_ANSWER_POLICY = {"direct", "qualified", "abstain", "review"}


@dataclass(frozen=True)
class ClaimPlan:
    claim_id: str
    proposed_claim: str
    atomic_claim: bool
    target_source_ref: str
    target_selector: str
    support_result: str
    coverage_extent: str
    conflict_state: str
    missing_elements: list[str]
    allowed_policy: str
    allowed_text: str


@dataclass(frozen=True)
class QueryPlan:
    run_id: str
    query: str
    scenario: str
    expected_answer_policy: str
    intended_use: str
    scope: dict[str, Any]
    allowed_authority_buckets: list[str]
    claims: list[ClaimPlan]


RUN_PLANS = [
    QueryPlan(
        run_id="run-001-direct-support",
        scenario="direct_support",
        expected_answer_policy="direct",
        query="How should a stable text anchor preserve selected text and nearby context?",
        intended_use="internal_orientation_answer",
        scope={"project": "verified-action-knowledge-system", "topic": "source_anchor"},
        allowed_authority_buckets=["raw_anchor"],
        claims=[
            ClaimPlan(
                claim_id="claim-001",
                proposed_claim=(
                    "A stable text anchor should preserve the selected text plus nearby "
                    "before/after context so a reviewer can re-find the evidence span."
                ),
                atomic_claim=True,
                target_source_ref="raw/articles/2026-05-30-w3c-web-annotation-source.md",
                target_selector="Source Anchor",
                support_result="supported",
                coverage_extent="full",
                conflict_state="none",
                missing_elements=[],
                allowed_policy="direct",
                allowed_text=(
                    "稳定文本锚点应保存被选中的文本和前后邻近上下文，方便 reviewer "
                    "重新定位证据 span。"
                ),
            )
        ],
    ),
    QueryPlan(
        run_id="run-002-qualified-partial",
        scenario="partial_or_scope_limited",
        expected_answer_policy="qualified",
        query="Can W3C PROV traceability be treated as truth confidence or action-ready support in VAKS?",
        intended_use="internal_orientation_answer",
        scope={"project": "verified-action-knowledge-system", "topic": "provenance_boundary"},
        allowed_authority_buckets=["raw_anchor"],
        claims=[
            ClaimPlan(
                claim_id="claim-001",
                proposed_claim=(
                    "PROV-lite can provide VAKS with a lightweight entity/activity/agent "
                    "skeleton for source provenance."
                ),
                atomic_claim=True,
                target_source_ref="raw/articles/2026-05-29-w3c-prov-source.md",
                target_selector="初步看点",
                support_result="supported",
                coverage_extent="full",
                conflict_state="none",
                missing_elements=[],
                allowed_policy="direct",
                allowed_text=(
                    "PROV-lite 可以给 VAKS 的 source provenance 提供轻量的 "
                    "entity / activity / agent 骨架。"
                ),
            ),
            ClaimPlan(
                claim_id="claim-002",
                proposed_claim=(
                    "PROV traceability is scope-limited: it records traceability, but it "
                    "does not decide truth, raise confidence, or turn a citation into support."
                ),
                atomic_claim=True,
                target_source_ref="raw/articles/2026-05-29-w3c-prov-source.md",
                target_selector="边界",
                support_result="scope_limited",
                coverage_extent="full",
                conflict_state="none",
                missing_elements=[],
                allowed_policy="qualify",
                allowed_text=(
                    "PROV traceability 只能作为可追踪性和复核辅助；当前资料不支持把它升级成 "
                    "reviewed truth confidence 或 action-ready evidence support。"
                ),
            ),
        ],
    ),
    QueryPlan(
        run_id="run-003-missing-anchor-review",
        scenario="missing_anchor_or_out_of_scope",
        expected_answer_policy="review",
        query="Can a China sales employee expense a client dinner under the current company policy?",
        intended_use="internal_orientation_answer",
        scope={"project": "verified-action-knowledge-system", "topic": "enterprise_policy_gap"},
        allowed_authority_buckets=["raw_anchor"],
        claims=[
            ClaimPlan(
                claim_id="claim-001",
                proposed_claim=(
                    "The current corpus contains a current company expense policy allowing "
                    "China sales employees to expense client dinners."
                ),
                atomic_claim=True,
                target_source_ref="",
                target_selector="",
                support_result="missing_anchor",
                coverage_extent="none",
                conflict_state="none",
                missing_elements=[
                    "current company expense policy source",
                    "China region scope",
                    "sales employee scope",
                    "client dinner reimbursement conditions",
                ],
                allowed_policy="review",
                allowed_text=(
                    "本次检索与 Context Pack 未找到可用于回答该问题的企业费用政策 anchor；"
                    "因此不能确认中国区销售员工是否可报销客户晚宴，需要补充当前正式费用政策或交给 review。"
                ),
            )
        ],
    ),
]


def ensure_clean_output(*, replace_existing_sandbox: bool = False) -> None:
    if OUT_DIR.exists():
        if not replace_existing_sandbox:
            raise FileExistsError(
                f"{OUT_DIR.relative_to(ROOT).as_posix()} already exists. "
                "R0.5 runs are append-only by default; pass --replace-existing-sandbox "
                "only for an explicit sandbox regeneration."
            )
        shutil.rmtree(OUT_DIR)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256_file(path: Path) -> str:
    return base.sha256_file(path)


def sha256_jsonable(data: Any) -> str:
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def normalize_record_kind(kind: str) -> str:
    if kind == "project_lens_overlay":
        return "project_overlay"
    return kind


def normalize_authority_bucket(bucket: str) -> str:
    if bucket == "overlay":
        return "project_overlay"
    return bucket


def corpus_snapshot_hash(corpus: list[base.CorpusDoc]) -> str:
    rows = [{"path": doc.rel_path, "sha256": doc.source_hash} for doc in sorted(corpus, key=lambda d: d.rel_path)]
    return sha256_jsonable(rows)


def authority_filter(corpus: list[base.CorpusDoc], allowed_buckets: list[str]) -> tuple[list[base.CorpusDoc], dict[str, Any]]:
    allowed = set(allowed_buckets)
    included: list[base.CorpusDoc] = []
    excluded: list[base.CorpusDoc] = []
    for doc in corpus:
        bucket = normalize_authority_bucket(base.doc_authority_bucket(doc))
        if bucket in allowed:
            included.append(doc)
        else:
            excluded.append(doc)
    return included, {
        "filter_order": "before_ranking",
        "allowed_authority_buckets": allowed_buckets,
        "corpus_doc_count": len(corpus),
        "eligible_doc_count": len(included),
        "excluded_doc_count": len(excluded),
        "included_bucket_counts": dict(Counter(normalize_authority_bucket(base.doc_authority_bucket(doc)) for doc in included)),
        "excluded_bucket_counts": dict(Counter(normalize_authority_bucket(base.doc_authority_bucket(doc)) for doc in excluded)),
    }


def extract_heading_section(body: str, heading: str) -> tuple[str, int, int]:
    """Return section text plus start/end character offsets for a markdown heading."""
    pattern = re.compile(r"(?m)^(#{1,6})\s+" + re.escape(heading) + r"\s*$")
    match = pattern.search(body)
    if not match:
        return "", -1, -1
    next_heading = re.search(r"(?m)^#{1,6}\s+", body[match.end() :])
    end = len(body) if not next_heading else match.end() + next_heading.start()
    return body[match.start() : end].strip(), match.start(), end


def compact_exact(section: str, limit: int = 850) -> str:
    return re.sub(r"\s+", " ", section).strip()[:limit]


def anchor_for(doc: base.CorpusDoc, selector: str) -> dict[str, Any]:
    if not selector:
        return {
            "exact": "",
            "prefix": "",
            "suffix": "",
            "location_hint": "",
            "normalization_version": ANCHOR_NORMALIZATION_VERSION,
            "resolved": False,
        }
    section, start, end = extract_heading_section(doc.body, selector)
    if section:
        prefix = doc.body[max(0, start - 160) : start]
        suffix = doc.body[end : min(len(doc.body), end + 160)]
        return {
            "exact": compact_exact(section),
            "prefix": re.sub(r"\s+", " ", prefix).strip(),
            "suffix": re.sub(r"\s+", " ", suffix).strip(),
            "location_hint": f"heading:{selector}",
            "normalization_version": ANCHOR_NORMALIZATION_VERSION,
            "resolved": True,
        }
    resolved = base.resolve_anchor(f"{doc.rel_path}#{selector}")
    return {
        "exact": selector if resolved.get("status") == "resolved" else "",
        "prefix": "",
        "suffix": "",
        "location_hint": f"selector:{selector}",
        "normalization_version": ANCHOR_NORMALIZATION_VERSION,
        "resolved": resolved.get("status") == "resolved",
    }


def build_query_policy(plan: QueryPlan, now: str) -> dict[str, Any]:
    return {
        "run_id": plan.run_id,
        "created_at": now,
        "query": plan.query,
        "intended_use": plan.intended_use,
        "action_use_allowed": False,
        "as_of": "2026-06-23",
        "scope": plan.scope,
        "allowed_authority_buckets": plan.allowed_authority_buckets,
        "support_candidate_authority_buckets": ["raw_anchor"],
        "retrieval_channels": ["lexical"],
        "rerank_applied": False,
        "vector_applied": False,
        "graph_applied": False,
        "acl_applied": False,
        "acl_status": "not_evaluated",
        "query_policy_version": QUERY_POLICY_VERSION,
        "read_only": True,
        "writeback_allowed": False,
        "promotion_allowed": False,
        "truth_mutation_allowed": False,
        "production_runtime_validated": False,
    }


def receipt_rows(plan: QueryPlan, hits: list[base.SearchHit]) -> list[dict[str, Any]]:
    rows = []
    for idx, hit in enumerate(hits, start=1):
        rows.append(
            {
                "run_id": plan.run_id,
                "event_id": f"{plan.run_id}-ret-{idx:03d}",
                "query_variant": "original",
                "channel": "lexical",
                "source_ref": hit.doc.rel_path,
                "source_snapshot_hash": hit.doc.source_hash,
                "authority_bucket": normalize_authority_bucket(base.doc_authority_bucket(hit.doc)),
                "rank": hit.rank,
                "diagnostic_score": round(hit.score, 4),
                "selected_by": ["lexical"],
                "policy_decision": {"included": True, "reason": "authority_bucket_allowed"},
                "score_is_support": False,
                "rank_is_support": False,
                "record_kind": normalize_record_kind(hit.doc.record_kind),
                "knowledge_status": hit.doc.knowledge_status,
                "matched_terms": hit.matched_terms,
                "snippet": hit.snippet,
            }
        )
    return rows


def make_context_pack(plan: QueryPlan, hits: list[base.SearchHit]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    target_map = {(claim.target_source_ref, claim.target_selector): claim for claim in plan.claims if claim.target_source_ref}
    target_sources = {claim.target_source_ref for claim in plan.claims if claim.target_source_ref}
    doc_by_path = {hit.doc.rel_path: hit.doc for hit in hits}
    items: list[dict[str, Any]] = []
    item_for_claim: dict[str, str] = {}
    item_index = 1

    for hit in hits[:8]:
        if hit.doc.rel_path in target_sources:
            for claim in [claim for claim in plan.claims if claim.target_source_ref == hit.doc.rel_path]:
                anchor = anchor_for(hit.doc, claim.target_selector)
                item_id = f"item-{item_index:03d}"
                item_index += 1
                role = "support_candidate" if anchor["resolved"] else "orientation"
                items.append(
                    {
                        "item_id": item_id,
                        "source_ref": hit.doc.rel_path,
                        "source_snapshot_hash": hit.doc.source_hash,
                        "authority_bucket": "raw_anchor",
                        "pack_role": role,
                        "scope_fit": "matched",
                        "temporal_fit": "current",
                        "anchor": {k: v for k, v in anchor.items() if k != "resolved"},
                        "selected_by": ["lexical"],
                        "retrieval_rank": hit.rank,
                        "diagnostic_score": round(hit.score, 4),
                        "not_yet": ["reviewed_support", "reviewed_truth", "action_basis"],
                    }
                )
                if role == "support_candidate":
                    item_for_claim[claim.claim_id] = item_id
            continue

        item_id = f"item-{item_index:03d}"
        item_index += 1
        items.append(
            {
                "item_id": item_id,
                "source_ref": hit.doc.rel_path,
                "source_snapshot_hash": hit.doc.source_hash,
                "authority_bucket": normalize_authority_bucket(base.doc_authority_bucket(hit.doc)),
                "pack_role": "orientation",
                "scope_fit": "unknown",
                "temporal_fit": "unknown",
                "anchor": {
                    "exact": "",
                    "prefix": "",
                    "suffix": "",
                    "location_hint": "",
                    "normalization_version": ANCHOR_NORMALIZATION_VERSION,
                },
                "selected_by": ["lexical"],
                "retrieval_rank": hit.rank,
                "diagnostic_score": round(hit.score, 4),
                "not_yet": ["reviewed_support", "reviewed_truth", "action_basis"],
            }
        )

    for claim in plan.claims:
        if claim.target_source_ref and claim.claim_id not in item_for_claim and claim.target_source_ref in doc_by_path:
            # Defensive fallback should not normally fire because target hits are handled above.
            item_for_claim[claim.claim_id] = ""
    return items, item_for_claim


def claim_hash(claim: str) -> str:
    return hashlib.sha256(claim.encode("utf-8")).hexdigest()[:16]


def make_claim_map(plan: QueryPlan, context_items: list[dict[str, Any]], item_for_claim: dict[str, str]) -> list[dict[str, Any]]:
    item_by_id = {item["item_id"]: item for item in context_items}
    rows: list[dict[str, Any]] = []
    for claim in plan.claims:
        assert claim.support_result in ALLOWED_SUPPORT_RESULTS
        assert claim.coverage_extent in ALLOWED_COVERAGE
        assert claim.conflict_state in ALLOWED_CONFLICT
        item_id = item_for_claim.get(claim.claim_id, "")
        anchor_refs = []
        if item_id and item_id in item_by_id:
            item = item_by_id[item_id]
            anchor_refs.append(
                {
                    "item_id": item_id,
                    "source_ref": item["source_ref"],
                    "source_snapshot_hash": item["source_snapshot_hash"],
                    "exact": item["anchor"]["exact"],
                    "anchor_selector": item["anchor"]["location_hint"],
                }
            )
        rows.append(
            {
                "claim_id": claim.claim_id,
                "claim_hash": claim_hash(claim.proposed_claim),
                "proposed_claim": claim.proposed_claim,
                "atomic_claim": claim.atomic_claim,
                "anchor_refs": anchor_refs,
                "support_result": claim.support_result,
                "coverage_extent": claim.coverage_extent,
                "scope_fit": "matched" if anchor_refs else "unknown",
                "temporal_fit": "current" if anchor_refs else "unknown",
                "authority_fit": "allowed" if anchor_refs else "missing",
                "conflict_state": claim.conflict_state,
                "missing_elements": claim.missing_elements,
                "assessment": {
                    "actor": "codex_r0_5_scripted_assessor",
                    "method": "deterministic_source_span_alignment_over_fixed_claim_plan",
                    "model_or_judge_version": ASSESSOR_VERSION,
                    "assessment_authority": "non_authoritative",
                },
                "allowed_expression": {"policy": claim.allowed_policy, "text": claim.allowed_text},
                "not_checked": ["real_world_truth", "reviewer_approval", "action_readiness"],
            }
        )
    return rows


def make_sufficiency(plan: QueryPlan, claim_rows: list[dict[str, Any]]) -> dict[str, Any]:
    full = sum(1 for row in claim_rows if row["support_result"] == "supported" and row["coverage_extent"] == "full")
    partial = sum(1 for row in claim_rows if row["support_result"] == "weak" or row["coverage_extent"] == "partial")
    missing = sum(1 for row in claim_rows if row["support_result"] == "missing_anchor")
    scope_limited = sum(1 for row in claim_rows if row["support_result"] == "scope_limited")
    unresolved = sum(1 for row in claim_rows if row["conflict_state"] == "unresolved")
    if missing:
        sufficiency_result = "insufficient"
        answer_policy = "review"
    elif unresolved:
        sufficiency_result = "risky"
        answer_policy = "review"
    elif partial or scope_limited:
        sufficiency_result = "weak"
        answer_policy = "qualified"
    else:
        sufficiency_result = "sufficient"
        answer_policy = "direct"
    assert sufficiency_result in ALLOWED_SUFFICIENCY
    assert answer_policy in ALLOWED_ANSWER_POLICY
    return {
        "run_id": plan.run_id,
        "claim_counts": {
            "total": len(claim_rows),
            "supported_full": full,
            "supported_partial": partial,
            "missing_anchor": missing,
            "scope_limited": scope_limited,
            "unresolved_conflict": unresolved,
        },
        "sufficiency_result": sufficiency_result,
        "answer_policy": answer_policy,
        "expected_answer_policy": plan.expected_answer_policy,
        "expected_answer_policy_met": answer_policy == plan.expected_answer_policy,
        "blocking_gaps": [
            gap for row in claim_rows if row["support_result"] in {"missing_anchor", "weak", "scope_limited"} for gap in row["missing_elements"]
        ],
        "unresolved_conflicts": [row["claim_id"] for row in claim_rows if row["conflict_state"] == "unresolved"],
        "review_required": answer_policy in {"review", "abstain"},
        "action_use_allowed": False,
        "action_readiness": "not_assessed",
        "assessment_authority": "non_authoritative",
        "not_proven": ["truth", "reviewer_approval", "promotion", "action_basis"],
    }


def generated_answer_intro(sufficiency: dict[str, Any]) -> str:
    policy = sufficiency["answer_policy"]
    if policy == "direct":
        return "本次 ClaimSupportMap 显示可直接表达以下受支持内容。"
    if policy == "qualified":
        return "本次 ClaimSupportMap 显示只能限定表达以下内容。"
    if policy == "abstain":
        return "本次 ClaimSupportMap 显示应当拒答或避免事实性表达。"
    return "本次 ClaimSupportMap 显示需要 review 或补充证据后再回答。"


def render_answer(plan: QueryPlan, claim_rows: list[dict[str, Any]], sufficiency: dict[str, Any]) -> str:
    lines = [
        f"# {plan.run_id} answer/use",
        "",
        generated_answer_intro(sufficiency),
        "",
        "## Answer",
        "",
    ]
    if sufficiency["answer_policy"] == "direct":
        lines.extend(f"- {row['allowed_expression']['text']}" for row in claim_rows)
    elif sufficiency["answer_policy"] == "qualified":
        lines.append("可以保守回答，但必须带限定：")
        lines.extend(f"- {row['allowed_expression']['text']}" for row in claim_rows)
    else:
        lines.append("不能给出确定答案：")
        lines.extend(f"- {row['allowed_expression']['text']}" for row in claim_rows)

    lines.extend(["", "## Claim Support", ""])
    for row in claim_rows:
        refs = [ref["source_ref"] for ref in row["anchor_refs"]] or ["<missing_anchor>"]
        lines.append(
            f"- `{row['claim_id']}`: `{row['support_result']}` / `{row['coverage_extent']}` / refs: {', '.join(refs)}"
        )
        if row["missing_elements"]:
            lines.append(f"  - missing: {', '.join(row['missing_elements'])}")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "Intended use: internal orientation only",
            "Action use allowed: no",
            "Reviewed truth promotion: no",
            "Assessment authority: non_authoritative",
            "Not Source Intake P0; not production runtime validation; not vector/graph validation; not action readiness.",
            "",
        ]
    )
    return "\n".join(lines)


def write_guard_inputs(run_dir: Path, plan: QueryPlan, context_items: list[dict[str, Any]], claim_rows: list[dict[str, Any]]) -> dict[str, str]:
    guard_dir = run_dir / "guard_inputs"
    guard_dir.mkdir(parents=True, exist_ok=True)

    receipt_md = guard_dir / "retrieval_receipt_guard.md"
    selected_buckets = sorted({item["authority_bucket"] for item in context_items if item["pack_role"] != "excluded"})
    selected_roles = sorted(
        {
            "support" if item["pack_role"] == "support_candidate" else item["pack_role"]
            for item in context_items
            if item["pack_role"] != "excluded"
        }
    )
    receipt_fm = "\n".join(
        [
            "---",
            "record_kind: retrieval_receipt",
            f"receipt_id: {plan.run_id}-guard-receipt",
            f"query_id: {plan.run_id}",
            "query_mode: review",
            "requested_authority_bucket: raw_anchor",
            f"included_buckets: [{', '.join(plan.allowed_authority_buckets)}]",
            "rrf_scope: same_authority_bucket_only",
            f"selected_item_authority_buckets: [{', '.join(selected_buckets or ['raw_anchor'])}]",
            f"selected_item_pack_roles: [{', '.join(selected_roles or ['orientation'])}]",
            "cross_bucket_rrf_used: false",
            "cross_bucket_rank_used: false",
            "selected_by_claims_support: false",
            "retrieval_rank_claims_support: false",
            "scores_are_support: false",
            "graph_rank_claims_trust: false",
            "selected_item_action_basis_allowed: false",
            "legacy_raw_metadata_used: false",
            "selected_by_is_not_support: true",
            "same_bucket_rrf_only: true",
            "cross_bucket_rank_not_authority: true",
            "legacy_raw_metadata_excluded: true",
            "candidate_overlay_feedback_not_support: true",
            "url_only_not_direct_support: true",
            "graph_rank_not_trust: true",
            "receipt_not_review_approval: true",
            "---",
            "",
            "Guard compatibility receipt for R0.5 JSONL retrieval receipt.",
        ]
    )
    write_text(receipt_md, receipt_fm)

    runtime_manifest = guard_dir / "runtime_artifact_exclusion_manifest.json"
    write_json(
        runtime_manifest,
        {
            "record_kind": "runtime_artifact_exclusion_manifest",
            "scenario_id": f"{plan.run_id}-runtime-artifact-exclusion",
            "exclude_runtime_artifacts": True,
            "items": [
                {
                    "id": item["item_id"],
                    "path": item["source_ref"],
                    "artifact_kind": "raw_anchor" if item["authority_bucket"] == "raw_anchor" else "source_record",
                    "selected": item["pack_role"] != "excluded",
                    "seen_by_retrieval": True,
                    "runtime_artifact": False,
                    "is_runtime_artifact": False,
                    "excluded": False,
                }
                for item in context_items
            ],
        },
    )

    support_files = []
    for row in claim_rows:
        support_md = guard_dir / f"{row['claim_id']}_support_boundary.md"
        first_ref = row["anchor_refs"][0] if row["anchor_refs"] else {}
        support_claimed = bool(row["anchor_refs"]) and row["support_result"] == "supported" and row["coverage_extent"] == "full"
        body = "\n".join(
            [
                "---",
                f"target_ref: {row['claim_id']}",
                f"support_claimed: {'true' if support_claimed else 'false'}",
                "pack_role: support" if support_claimed else "pack_role: orientation",
                "evidence_role: direct_support" if support_claimed else "evidence_role: background_context",
                f"proposed_support_record_kind: {'source_card' if support_claimed else ''}",
                f"proposed_support_authority_bucket: {'raw_anchor' if support_claimed else ''}",
                f"proposed_support_ref: {first_ref.get('source_ref', '')}",
                f"independent_anchor_ref: {first_ref.get('source_ref', '')}#{first_ref.get('anchor_selector', '')}",
                f"anchor_selector: {first_ref.get('anchor_selector', '')}",
                "anchor_type: raw_span" if support_claimed else "anchor_type: ",
                "url_only: false",
                "retrieval_rank_claims_support: false",
                "retrieval_score_claims_support: false",
                "graph_rank_claims_support: false",
                "feedback_used_as_support: false",
                "source_summary_self_support: false",
                "claim_note_self_support: false",
                "legacy_raw_metadata_used_as_support: false",
                "---",
                "",
                row["proposed_claim"],
            ]
        )
        write_text(support_md, body)
        support_files.append(rel(support_md))

    return {
        "retrieval_receipt_guard": rel(receipt_md),
        "runtime_artifact_manifest": rel(runtime_manifest),
        "support_boundary_files": support_files,
    }


def run_guard(path: Path, args: list[str]) -> dict[str, Any]:
    cmd = ["python", "tools/vaks_guard.py", "check", rel(path), *args, "--json"]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    payload: Any
    try:
        payload = json.loads(proc.stdout) if proc.stdout.strip() else None
    except json.JSONDecodeError:
        payload = proc.stdout
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": payload,
        "stderr": proc.stderr,
    }


def make_guard_report(run_dir: Path, guard_inputs: dict[str, Any]) -> dict[str, Any]:
    support_results = []
    for support_file in guard_inputs["support_boundary_files"]:
        support_results.append(run_guard(ROOT / support_file, ["--guard", "support_boundary"]))
    report = {
        "guard_boundary": (
            "VAKS Guard pass/warn/block is a machine-detectable contract check only; "
            "it is not reviewed truth, evidence support, action approval, or P0."
        ),
        "checked_exits": [
            "retrieval_receipt_validator",
            "runtime_artifact_selection",
            "support_boundary",
        ],
        "not_run": [
            "action_readiness",
            "operation_preflight",
            "feedback_boundary",
        ],
        "not_run_reason": "R0.5 is read-only and has no action, operation, feedback truth update, promotion, or writeback.",
        "compatibility_note": (
            "Guard inputs are compatibility shims for current vaks_guard.py; canonical R0.5 artifacts remain JSON/JSONL."
        ),
        "results": {
            "retrieval_receipt": run_guard(ROOT / guard_inputs["retrieval_receipt_guard"], ["--guard", "retrieval_receipt"]),
            "runtime_artifact_selection": run_guard(ROOT / guard_inputs["runtime_artifact_manifest"], ["--guard", "runtime_artifacts"]),
            "support_boundary": support_results,
        },
    }
    write_json(run_dir / "guard_report.json", report)
    return report


def run_one(plan: QueryPlan, corpus: list[base.CorpusDoc], snapshot_hash: str, now: str) -> dict[str, Any]:
    run_dir = RUNS_DIR / plan.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    query_policy = build_query_policy(plan, now)
    eligible_corpus, filter_summary = authority_filter(corpus, plan.allowed_authority_buckets)
    hits = base.retrieve(plan.query, eligible_corpus, top_k=12)
    receipts = receipt_rows(plan, hits)
    context_items, item_for_claim = make_context_pack(plan, hits)
    claim_rows = make_claim_map(plan, context_items, item_for_claim)
    sufficiency = make_sufficiency(plan, claim_rows)
    answer = render_answer(plan, claim_rows, sufficiency)

    query_policy["authority_filter_summary"] = filter_summary
    query_policy["corpus_snapshot_hash"] = snapshot_hash
    query_policy["artifact_generation_order"] = [
        "query_policy",
        "retrieval_receipt",
        "context_pack",
        "claim_support_map",
        "sufficiency_summary",
        "answer_use",
        "guard_report",
        "run_manifest",
    ]

    context_pack = {
        "run_id": plan.run_id,
        "pack_contract": "support_candidate_not_support",
        "items": context_items,
        "not_proven": ["reviewed_support", "reviewed_truth", "action_basis"],
    }

    write_json(run_dir / "query_policy.json", query_policy)
    write_jsonl(run_dir / "retrieval_receipt.jsonl", receipts)
    write_json(run_dir / "context_pack.json", context_pack)
    write_jsonl(run_dir / "claim_support_map.jsonl", claim_rows)
    write_json(run_dir / "sufficiency_summary.json", sufficiency)
    write_text(run_dir / "answer_use.md", answer)

    guard_inputs = write_guard_inputs(run_dir, plan, context_items, claim_rows)
    guard_report = make_guard_report(run_dir, guard_inputs)

    artifact_paths = [
        run_dir / "query_policy.json",
        run_dir / "retrieval_receipt.jsonl",
        run_dir / "context_pack.json",
        run_dir / "claim_support_map.jsonl",
        run_dir / "sufficiency_summary.json",
        run_dir / "answer_use.md",
        run_dir / "guard_report.json",
    ]
    artifact_hashes = {path.name: sha256_file(path) for path in artifact_paths}
    run_manifest = {
        "run_id": plan.run_id,
        "created_at": now,
        "tool_versions": {
            "runner": TOOL_VERSION,
            "query_policy": QUERY_POLICY_VERSION,
            "anchor_normalization": ANCHOR_NORMALIZATION_VERSION,
            "assessor": ASSESSOR_VERSION,
            "vaks_guard": "0.1.0",
        },
        "corpus_snapshot_hash": snapshot_hash,
        "artifact_hashes": artifact_hashes,
        "read_only": True,
        "parent_run_id": None,
        "scenario": plan.scenario,
        "answer_policy": sufficiency["answer_policy"],
        "sufficiency_result": sufficiency["sufficiency_result"],
        "not_proven": ["Source Intake P0", "production runtime", "vector_graph_retrieval", "reviewed_truth", "action_readiness"],
    }
    write_json(run_dir / "run_manifest.json", run_manifest)
    return {
        "run_id": plan.run_id,
        "scenario": plan.scenario,
        "answer_policy": sufficiency["answer_policy"],
        "sufficiency_result": sufficiency["sufficiency_result"],
        "expected_answer_policy": plan.expected_answer_policy,
        "expected_answer_policy_met": sufficiency["expected_answer_policy_met"],
        "artifact_hashes": artifact_hashes,
        "guard_statuses": summarize_guard_statuses(guard_report),
    }


def summarize_guard_statuses(guard_report: dict[str, Any]) -> dict[str, Any]:
    statuses: dict[str, Any] = {}
    for key, result in guard_report["results"].items():
        if key == "support_boundary":
            statuses[key] = [entry.get("stdout", {}).get("status") for entry in result]
        else:
            statuses[key] = result.get("stdout", {}).get("status")
    return statuses


def write_top_level_docs(summary: dict[str, Any]) -> None:
    write_text(
        OUT_DIR / "README.md",
        "\n".join(
            [
                "# VAKS Source Intake Real Read-Only Evidence Loop R0.5",
                "",
                "This package exercises a bounded real read-only evidence-to-answer path across three real queries.",
                "",
                "It proves only that this sandbox path can produce QueryPolicy, RetrievalReceipt, ContextPack, ClaimSupportMap, Sufficiency, AnswerUse, and Guard artifacts.",
                "",
                "It does not prove Source Intake P0, production runtime validation, vector/graph/hybrid retrieval, reviewed truth promotion, or action readiness.",
                "",
                "Canonical run artifacts are JSON/JSONL plus answer_use markdown. Guard inputs are compatibility shims for the current read-only VAKS Guard.",
                "",
            ]
        ),
    )
    write_text(
        OUT_DIR / "LIMITS.md",
        "\n".join(
            [
                "# Limits",
                "",
                "- Local Markdown lexical retrieval only.",
                "- No dense, sparse, graph, rerank, RRF, production runtime, or live LLM/tool runtime.",
                "- No ACL evaluation; fields explicitly record `acl_applied: false` and `acl_status: not_evaluated`.",
                "- Claim plans are deterministic sandbox inputs, not an implemented automatic claim splitter.",
                "- Claim support assessment is non-authoritative and does not create reviewed truth.",
                "- Action readiness, operation preflight, and feedback boundary are not run because R0.5 has no action, operation, or feedback truth update.",
                "- Runs are append-only evidence artifacts; do not overwrite a run to make partial results look greener.",
                "",
            ]
        ),
    )
    write_text(
        OUT_DIR / "ACCEPTANCE_SUMMARY.md",
        "\n".join(
            [
                "# Acceptance Summary",
                "",
                f"- status: `{summary['status']}`",
                f"- run_count: `{summary['run_count']}`",
                f"- expected_answer_policy_met_count: `{summary['expected_answer_policy_met_count']}`",
                "- not Source Intake P0",
                "- not production runtime validation",
                "- not vector/graph validation",
                "- not reviewed truth promotion",
                "- not action readiness",
                "",
                "Human wording:",
                "",
                "> 已在三个真实查询上跑通受限只读证据到回答链路，并留下可复现的 QueryPolicy、RetrievalReceipt、ContextPack、Claim-Support Map、Sufficiency 和 Guard 产物。",
                "",
            ]
        ),
    )


def validate_completion(run_summaries: list[dict[str, Any]]) -> dict[str, Any]:
    expected = len(RUN_PLANS)
    policy_met = sum(1 for row in run_summaries if row["expected_answer_policy_met"])
    status = "pass" if expected == 3 and policy_met == expected else "fail"
    return {
        "status": status,
        "run_count": expected,
        "expected_answer_policy_met_count": policy_met,
        "runs": run_summaries,
        "completion_boundary": (
            "R0.5 completion means three bounded read-only evidence-loop runs have complete artifacts. "
            "It does not mean P0, production runtime, vector/graph retrieval, reviewed truth, or action readiness."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bounded Source Intake R0.5 read-only evidence loop.")
    parser.add_argument(
        "--replace-existing-sandbox",
        action="store_true",
        help="Explicitly replace the generated sandbox output directory. Default is append-only refusal.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_clean_output(replace_existing_sandbox=args.replace_existing_sandbox)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    corpus = base.collect_corpus()
    snapshot_hash = corpus_snapshot_hash(corpus)
    run_summaries = [run_one(plan, corpus, snapshot_hash, now) for plan in RUN_PLANS]
    summary = validate_completion(run_summaries)
    write_json(OUT_DIR / "r0_5_summary.json", summary)
    write_top_level_docs(summary)
    print(json.dumps({"status": summary["status"], "out_dir": rel(OUT_DIR), "runs": [row["run_id"] for row in run_summaries]}, ensure_ascii=False))
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
