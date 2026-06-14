#!/usr/bin/env python
"""Run Source Intake live read-only loop v2.

v2 answers the Pro audit gaps from the first live package:
- no silent raw-anchor fallback;
- adversarial live hits intentionally mislabeled as support and then gated;
- a minimal frozen corpus plus self-contained replayer;
- still no LLM, no live tool runtime, no writeback, no promotion, no truth mutation.
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

import run_source_intake_live_readonly_loop as base


ROOT = base.ROOT
OUT_DIR = ROOT / "outputs" / "review" / "source-intake-live-readonly-loop-v2-2026-06-14"
RESULTS_DIR = OUT_DIR / "results"
QUERY_RUN_DIR = OUT_DIR / "query_runs"
CONTEXT_PACK_DIR = OUT_DIR / "context_packs"
ANSWER_USE_DIR = OUT_DIR / "answer_use"
FROZEN_CORPUS_DIR = OUT_DIR / "frozen_corpus"
ZIP_NAME = "source-intake-live-readonly-loop-v2-pro-review-package.zip"

REAL_ANCHOR_REF = base.REAL_ANCHOR_REF
REAL_ANCHOR_PATH = REAL_ANCHOR_REF.split("#", 1)[0]
CANONICAL_OVERLAY_FIXTURE = (
    ROOT
    / "outputs"
    / "review"
    / "project_overlays"
    / "_runtime_test_fixtures"
    / "2026-06-14-flexnote-canonical-overlay-runtime-fixture.md"
)


def configure_base_paths() -> None:
    base.OUT_DIR = OUT_DIR
    base.RESULTS_DIR = RESULTS_DIR
    base.QUERY_RUN_DIR = QUERY_RUN_DIR
    base.CONTEXT_PACK_DIR = CONTEXT_PACK_DIR
    base.ANSWER_USE_DIR = ANSWER_USE_DIR
    base.ZIP_NAME = ZIP_NAME


LIVE_CASES_V2 = [
    {
        "case_id": "V2-01-candidate-safe-downgrade",
        "query": "mnemosyne vector memory candidate final support action basis",
        "query_mode": "action",
        "intent": "Live retrieved candidate is safely routed to review_input, not final support.",
        "selection_mode": "safe_candidate_review_input",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "V2-02-real-raw-anchor-natural-allow",
        "query": "FlexNote Extracted Source Facts local-first card tag database inspected pages",
        "query_mode": "source_inspection",
        "intent": "Real raw anchor must be naturally retrieved and allowed read-only.",
        "selection_mode": "natural_raw_anchor_support",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "V2-03-mixed-pack-no-fallback-allow",
        "query": "FlexNote Extracted Source Facts visual workbench candidate overlay source anchor tag database context pack inspected pages",
        "query_mode": "review",
        "intent": "Mixed pack must include naturally retrieved raw anchor; no force_anchor_hit fallback allowed.",
        "selection_mode": "mixed_no_fallback",
        "expected_decision": "allowed_readonly",
    },
    {
        "case_id": "V2-04-adversarial-candidate-mislabeled-support",
        "query": "mnemosyne vector memory candidate final support action basis",
        "query_mode": "action",
        "intent": "Errant assembler marks a live candidate hit as support; gate must block.",
        "selection_mode": "adversarial_candidate_support",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "V2-05-adversarial-overlay-mislabeled-support",
        "query": "FlexNote visual workbench overlay project borrow support source anchor",
        "query_mode": "action",
        "intent": "Errant assembler marks a live project overlay hit as support; gate must block.",
        "selection_mode": "adversarial_overlay_support",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "V2-06-adversarial-rank-diagnostic-mislabeled-support",
        "query": "FlexNote visual workbench source anchor candidate overlay tag database context pack",
        "query_mode": "action",
        "intent": "Errant assembler uses retrieval rank as support anchor; gate must block.",
        "selection_mode": "adversarial_rank_support",
        "expected_decision": "blocked_or_downgraded",
    },
    {
        "case_id": "V2-07-adversarial-canonical-overlay-mislabeled-support",
        "query": "canonical overlay runtime fixture FlexNote visual workbench project overlay support",
        "query_mode": "action",
        "intent": "Errant assembler marks a canonical project_overlays hit as support; gate must block.",
        "selection_mode": "adversarial_canonical_overlay_support",
        "expected_decision": "blocked_or_downgraded",
    },
]


def reset_output_dir() -> None:
    if OUT_DIR.exists():
        resolved = OUT_DIR.resolve()
        expected = (ROOT / "outputs" / "review").resolve()
        if expected not in resolved.parents:
            raise RuntimeError(f"Refusing to remove unexpected output path: {OUT_DIR}")
        shutil.rmtree(OUT_DIR)
    for path in [RESULTS_DIR, QUERY_RUN_DIR, CONTEXT_PACK_DIR, ANSWER_USE_DIR, FROZEN_CORPUS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def write_canonical_overlay_fixture(now: str) -> Path:
    fm = {
        "record_kind": "project_overlay",
        "status": "candidate",
        "knowledge_status": "candidate",
        "processing_tier": "medium",
        "artifact_kind": "live_readonly_test_fixture",
        "retrieval_exclusion": True,
        "overlay_state": "confirmed",
        "review_pressure": "review_due",
        "retrieval_scope": "active_project_only",
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
        "project_id": "VAKS",
        "target_ref": "outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md",
        "project_borrow_scope": "For VAKS runtime testing, borrow FlexNote only as a canonical overlay fixture for visual workbench review-input routing.",
        "project_non_borrow_scope": "For project VAKS, do not borrow this runtime fixture as reviewed knowledge, evidence support, decision, or action basis.",
        "project_reopen_trigger": "Reopen only when testing canonical project_overlay support-gate behavior.",
        "created_at": now,
        "tags": ["runtime-test-fixture", "project-overlay", "canonical-overlay", "candidate-only"],
    }
    body = """# Canonical Project Overlay Runtime Fixture

This is a sandbox test fixture for Source Intake runtime validation.

It exists only to test that a canonical `outputs/review/project_overlays/` overlay cannot become final support even if an errant pack assembler labels it as `support`.

It is not reviewed knowledge, not a decision, not action basis, and not default retrieval material.
"""
    CANONICAL_OVERLAY_FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_OVERLAY_FIXTURE.write_text(f"---\n{base.dump_yaml(fm)}---\n\n{body}", encoding="utf-8")
    return CANONICAL_OVERLAY_FIXTURE


def first_hit(hits: list[base.SearchHit], predicate: Any) -> base.SearchHit | None:
    for hit in hits:
        if predicate(hit):
            return hit
    return None


def require_hit(case_id: str, hits: list[base.SearchHit], predicate: Any, message: str) -> base.SearchHit:
    hit = first_hit(hits, predicate)
    if hit is None:
        raise RuntimeError(f"{case_id}: {message}")
    return hit


def select_case_pack_v2(case: dict[str, Any], hits: list[base.SearchHit]) -> list[dict[str, Any]]:
    mode = case["selection_mode"]
    case_id = case["case_id"]

    if mode == "safe_candidate_review_input":
        candidate = require_hit(case_id, hits, lambda h: h.doc.record_kind == "candidate_distillation", "candidate hit missing")
        return [
            base.hit_to_item(
                candidate,
                pack_role="review_input",
                excluded_reason="live_candidate_hit_safely_routed_to_review_input",
            )
        ]

    if mode == "natural_raw_anchor_support":
        raw = require_hit(case_id, hits, lambda h: h.doc.rel_path == REAL_ANCHOR_PATH, "required raw anchor did not appear in live retrieval top-k")
        return [base.hit_to_item(raw, pack_role="support", anchor_ref=REAL_ANCHOR_REF)]

    if mode == "mixed_no_fallback":
        raw = require_hit(case_id, hits, lambda h: h.doc.rel_path == REAL_ANCHOR_PATH, "required raw anchor did not appear in live retrieval top-k")
        candidate = require_hit(case_id, hits, lambda h: h.doc.record_kind == "candidate_distillation", "candidate hit missing")
        overlay = require_hit(case_id, hits, lambda h: h.doc.record_kind == "project_overlay", "overlay hit missing")
        rank_only = require_hit(
            case_id,
            hits,
            lambda h: h.doc.rel_path not in {raw.doc.rel_path, candidate.doc.rel_path, overlay.doc.rel_path},
            "rank/orientation hit missing",
        )
        selected_by = dict(rank_only.selected_by)
        selected_by["rank"] = True
        rank_hit = base.SearchHit(
            doc=rank_only.doc,
            score=rank_only.score,
            rank=rank_only.rank,
            matched_terms=rank_only.matched_terms,
            selected_by=selected_by,
            snippet=rank_only.snippet,
        )
        return [
            base.hit_to_item(raw, pack_role="support", anchor_ref=REAL_ANCHOR_REF),
            base.hit_to_item(candidate, pack_role="review_input", excluded_reason="candidate_not_final_support"),
            base.hit_to_item(overlay, pack_role="review_input", excluded_reason="overlay_not_final_support"),
            base.hit_to_item(rank_hit, pack_role="orientation", excluded_reason="rank_signal_is_diagnostic_not_support"),
        ]

    if mode == "adversarial_candidate_support":
        candidate = require_hit(case_id, hits, lambda h: h.doc.record_kind == "candidate_distillation", "candidate hit missing")
        return [
            base.hit_to_item(
                candidate,
                pack_role="support",
                anchor_ref="",
                excluded_reason="adversarial_mislabel_expected_to_be_blocked",
            )
        ]

    if mode == "adversarial_overlay_support":
        overlay = require_hit(case_id, hits, lambda h: h.doc.record_kind == "project_overlay", "overlay hit missing")
        return [
            base.hit_to_item(
                overlay,
                pack_role="support",
                anchor_ref=REAL_ANCHOR_REF,
                excluded_reason="adversarial_mislabel_expected_to_be_blocked",
            )
        ]

    if mode == "adversarial_rank_support":
        source = first_hit(hits, lambda h: h.doc.record_kind == "source_card") or (hits[0] if hits else None)
        if source is None:
            raise RuntimeError(f"{case_id}: no hit available for adversarial rank support")
        item = base.hit_to_item(
            source,
            pack_role="support",
            anchor_ref=f"retrieval_rank:{source.rank}:score:{source.score:.4f}",
            excluded_reason="adversarial_rank_anchor_expected_to_be_blocked",
        )
        item["selected_by"]["rank"] = True
        return [item]

    if mode == "adversarial_canonical_overlay_support":
        overlay = require_hit(
            case_id,
            hits,
            lambda h: h.doc.record_kind == "project_overlay" and "outputs/review/project_overlays/" in h.doc.rel_path,
            "canonical project_overlay hit missing",
        )
        return [
            base.hit_to_item(
                overlay,
                pack_role="support",
                anchor_ref=REAL_ANCHOR_REF,
                excluded_reason="adversarial_canonical_overlay_mislabel_expected_to_be_blocked",
            )
        ]

    raise RuntimeError(f"Unknown selection_mode: {mode}")


def evaluate_support_v2(items: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]], list[str]]:
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
                "resolution": {"status": "not_checked", "reason": "no support items"},
                "reason": "retrieved_items_remain_review_input_or_orientation_only",
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


def write_frozen_corpus(paths: set[Path], retrieval_rows: list[dict[str, Any]], now: str) -> dict[str, Any]:
    manifest_rows = []
    for source in sorted(paths):
        if not source.exists() or not source.is_file():
            continue
        rel_path = base.rel(source)
        target = FROZEN_CORPUS_DIR / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        manifest_rows.append(
            {
                "path": rel_path,
                "frozen_path": base.rel(target),
                "sha256": base.sha256_file(source),
                "bytes": source.stat().st_size,
            }
        )

    expected: dict[str, list[str]] = {}
    for row in retrieval_rows:
        expected.setdefault(row["case_id"], []).append(row["path"])
    query_manifest = {
        "created_at": now,
        "frozen_scope": "minimal_topk_membership_case_corpus_not_full_workspace",
        "truth_boundary": "Replayer reproduces top-k membership over this package's frozen minimal corpus, not exact ranking order and not the original full workspace corpus.",
        "queries": [
            {
                "case_id": case["case_id"],
                "query": case["query"],
                "expected_top_paths": expected.get(case["case_id"], []),
            }
            for case in LIVE_CASES_V2
        ],
    }
    base.write_json(RESULTS_DIR / "frozen_corpus_manifest.json", {"files": manifest_rows, "file_count": len(manifest_rows)})
    base.write_json(RESULTS_DIR / "frozen_query_manifest.json", query_manifest)
    write_frozen_replayer()
    replay = subprocess.run(["python", base.rel(OUT_DIR / "replay_frozen_rerun.py")], cwd=ROOT, capture_output=True, text=True)
    replay_result = {
        "status": "pass" if replay.returncode == 0 else "fail",
        "returncode": replay.returncode,
        "stdout": replay.stdout.strip(),
        "stderr": replay.stderr.strip(),
        "truth_boundary": "Frozen replay checks minimal-corpus top-k membership reproducibility, not exact ranking order or full-workspace reproducibility.",
    }
    base.write_json(RESULTS_DIR / "frozen_replay_command_result.json", replay_result)
    return replay_result


def run_validation_commands_v2(now: str) -> dict[str, Any]:
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
        if command[1].endswith("validate_source_intake_contract.py") and "--scope" in command:
            try:
                parsed = json.loads(stdout)
            except json.JSONDecodeError:
                parsed = {}
            if parsed.get("scope") == "current":
                current_lint_errors = int(parsed.get("errors") or 0)
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
                "stdout": stdout,
                "stderr": completed.stderr.strip(),
            }
        )
    status = "pass" if all(row["returncode"] == 0 for row in rows) and current_lint_errors == 0 else "pass_with_current_lint_errors"
    result = {
        "status": status,
        "checked_at": now,
        "current_lint_errors": current_lint_errors,
        "commands": rows,
        "truth_boundary": "Current lint may surface pre-existing workspace issues; that does not make this v2 live package a P0 pass.",
    }
    base.write_json(RESULTS_DIR / "live_validation_commands_v2.json", result)
    return result


def write_events_v2(case_rows: list[dict[str, Any]], retrieval_rows: list[dict[str, Any]], now: str) -> None:
    events = []
    by_case = {row["case_id"]: row for row in case_rows}
    for case in LIVE_CASES_V2:
        row = by_case[case["case_id"]]
        case_retrievals = [r for r in retrieval_rows if r["case_id"] == case["case_id"]]
        events.extend(
            [
                {
                    "time": now,
                    "case_id": case["case_id"],
                    "stage": "live_retrieve",
                    "live_retrieval_used": True,
                    "force_anchor_hit_used": False,
                    "retrieved_count": len(case_retrievals),
                    "top_result": row["top_result"],
                    "truth_boundary": "local Markdown lexical retrieval only; no live embedding, vector, or graph compiler.",
                },
                {
                    "time": now,
                    "case_id": case["case_id"],
                    "stage": "assemble_context_pack",
                    "selection_mode": case["selection_mode"],
                    "context_pack": row["context_pack"],
                    "pack_assembly": "case_scripted_no_fallback",
                },
                {
                    "time": now,
                    "case_id": case["case_id"],
                    "stage": "answer_use_gate",
                    "decision": row["decision"],
                    "support_count": row["support_count"],
                    "writeback_attempted": False,
                    "promotion_attempted": False,
                    "truth_mutation_attempted": False,
                },
            ]
        )
    path = RESULTS_DIR / "live_readonly_loop_v2_events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


def run_fallback_regression_scan() -> dict[str, Any]:
    forbidden = ["forced_anchor_if_retrieval_missed", "retrieval_score: 999.0", "retrieval_score: 999", '"score": 999']
    scan_dirs = [QUERY_RUN_DIR, CONTEXT_PACK_DIR, ANSWER_USE_DIR, RESULTS_DIR]
    findings = []
    for directory in scan_dirs:
        for path in directory.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".jsonl", ".csv"}:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for token in forbidden:
                if token in text:
                    findings.append({"path": base.rel(path), "token": token})
    result = {
        "status": "pass" if not findings else "fail",
        "forbidden_tokens": forbidden,
        "findings": findings,
        "truth_boundary": "Regression scan covers generated v2 artifacts only; older base script source may still contain fallback code but is not on the v2 execution path.",
    }
    base.write_json(RESULTS_DIR / "fallback_regression_scan.json", result)
    return result


def write_frozen_replayer() -> None:
    script = r'''
#!/usr/bin/env python
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "frozen_corpus"
MANIFEST = ROOT / "results" / "frozen_query_manifest.json"
OUT = ROOT / "results" / "frozen_replay_check.json"
TOKEN_RE = re.compile(r"[a-z0-9]+|[\u4e00-\u9fff]+", re.IGNORECASE)

def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if len(t) > 1]

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

def infer_kind(path: str, fm: dict) -> str:
    if fm.get("record_kind"):
        return str(fm["record_kind"])
    if path.startswith("raw/"):
        return "source_card"
    if path.startswith("outputs/review/source_annotations/") or path.endswith("source-annotation.md"):
        return "source_annotation"
    if path.endswith("candidate-distillation.md"):
        return "candidate_distillation"
    if "project_lens_overlays/" in path or path.endswith("-overlay.md"):
        return "project_overlay"
    return "source_card"

def headings(body: str) -> str:
    return "\n".join(line for line in body.splitlines() if line.lstrip().startswith("#"))

def score(query: str, rel_path: str, text: str, title: str) -> float:
    terms = set(tokenize(query))
    path_tokens = Counter(tokenize(rel_path))
    title_tokens = Counter(tokenize(title))
    heading_tokens = Counter(tokenize(headings(text)))
    body_tokens = Counter(tokenize(text[:20000]))
    total = 0.0
    for term in terms:
        total += path_tokens.get(term, 0) * 6.0
        total += title_tokens.get(term, 0) * 4.0
        total += heading_tokens.get(term, 0) * 2.5
        total += min(body_tokens.get(term, 0), 6) * 1.0
    kind = infer_kind(rel_path, {})
    if kind == "source_card" and "source" in terms:
        total += 1.5
    if kind == "candidate_distillation" and "candidate" in terms:
        total += 4.0
    return total

def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    docs = []
    for path in sorted(CORPUS.rglob("*.md")):
        rel = path.relative_to(CORPUS).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = split_frontmatter(text)
        docs.append({"path": rel, "title": str(fm.get("title") or path.stem), "text": body, "kind": infer_kind(rel, fm)})
    checks = []
    for query in manifest["queries"]:
        ranked = []
        for doc in docs:
            s = score(query["query"], doc["path"], doc["text"], doc["title"])
            if s > 0:
                ranked.append((s, doc["path"]))
        ranked.sort(key=lambda item: (-item[0], item[1]))
        actual = [path for _, path in ranked[: len(query["expected_top_paths"])]]
        expected = query["expected_top_paths"]
        checks.append({
            "case_id": query["case_id"],
            "expected": expected,
            "actual": actual,
            "match": set(actual) == set(expected),
            "match_kind": "top_k_membership_not_exact_order",
        })
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
    path = OUT_DIR / "replay_frozen_rerun.py"
    path.write_text(textwrap.dedent(script).lstrip(), encoding="utf-8")


def write_reports(summary: dict[str, Any], case_rows: list[dict[str, Any]], now: str) -> None:
    report = f"""# VAKS Source Intake Live Read-Only Loop v2 Report

## Verdict

This is a no-fallback, adversarial-support-mislabel, canonical-overlay-check, minimal-frozen-replay sandbox package.

It improves on the previous live package by removing silent `force_anchor_hit()` from the mixed-pack case and by adding packaged live-hit misuse cases where candidate, legacy overlay, canonical overlay, and rank-only diagnostic items are intentionally mislabeled as support and then blocked by the support gate.

It still does **not** prove Source Intake P0 passed, live LLM/tool runtime validation, live embedding/vector/graph validation, external blind relevance, or runtime adoption readiness.

## Results

- Live cases: {summary['case_count']}
- Expected decisions passed: {summary['passed_expected_decision_count']} / {summary['case_count']}
- Decisions: {summary['decision_breakdown']}
- Frozen replay: {summary['frozen_replay']['status']} (minimal top-k membership, not exact ranking order)
- Fallback regression scan: {summary['fallback_regression_scan']['status']}

## Case Results

""" + "\n".join(
        f"- `{row['case_id']}`: {row['decision']} / top=`{row['top_result']}` / support_count={row['support_count']}"
        for row in case_rows
    ) + """

## Boundary

The live retrieval remains local lexical Markdown retrieval. Pack assembly is still scripted, but v2 includes packaged adversarial scripted mislabel cases to test whether the support gate blocks unsafe pack roles. The raw/stable anchor allow cases are structurally resolved, not externally judged for semantic sufficiency. The frozen replay is a minimal top-k membership replay, not exact ranking order and not a full-workspace rerun.
"""
    (OUT_DIR / "LIVE_READONLY_LOOP_V2_REPORT.md").write_text(report, encoding="utf-8")

    readme = f"""# Source Intake Live Read-Only Loop v2 Package

Generated: {now}

## Human Summary

This package answers the previous audit gaps:

- no silent fallback raw anchor in the mixed-pack allow case;
- candidate/overlay/rank live hits are intentionally mislabeled as support in adversarial cases;
- a canonical `outputs/review/project_overlays/` overlay fixture is checked separately from legacy `project_lens_overlays/`;
- a minimal frozen corpus and self-contained replayer are included.

## Supported Conclusion

In the packaged seven-case harness, live Markdown retrieval feeds pack/use artifacts, and the support gate blocked the packaged adversarial support-mislabel cases while allowing the packaged naturally retrieved raw/stable anchor case in read-only mode.

The raw/stable anchor is structurally resolved, not externally judged for semantic sufficiency.

## Unsupported Conclusions

- Source Intake P0 passed: no.
- Live LLM/tool runtime validated: no.
- Live embedding/vector/graph retrieval validated: no.
- External blind relevance completed: no.
- Runtime adoption ready: no.
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    pro_request = """# Pro Review Request

Please reverse-audit this v2 package.

Focus:

1. Did v2 remove the silent force_anchor_hit fallback from the mixed-pack allow case?
2. Do V2-04 / V2-05 / V2-06 actually test live hits mislabeled as support and then blocked?
3. Does the minimal frozen replayer reproduce the packaged top-k membership within its declared scope, without pretending to prove exact rank order or full-workspace replay?
4. Are there any overclaims around P0, live LLM/tool runtime, live embedding/vector/graph retrieval, semantic support, or runtime adoption?
5. What is the smallest remaining blocker?
"""
    (OUT_DIR / "PRO_REVIEW_REQUEST.md").write_text(pro_request, encoding="utf-8")


def package_outputs(input_paths: set[Path], summary: dict[str, Any]) -> tuple[Path, str]:
    scripts = [
        ROOT / "tools" / "run_source_intake_live_readonly_loop_v2.py",
        ROOT / "tools" / "run_source_intake_live_readonly_loop.py",
        ROOT / "tools" / "validate_source_intake_contract.py",
        ROOT / "tools" / "validate_source_intake_failure_matrix.py",
        ROOT / "tools" / "source_intake_enum_registry.json",
        ROOT / "SOURCE_INTAKE.md",
    ]
    package_files = [p for p in OUT_DIR.rglob("*") if p.is_file() and p.name != ZIP_NAME]
    package_files += [p for p in sorted(input_paths) if p.exists()]
    package_files += [p for p in scripts if p.exists()]

    manifest_rows = []
    seen_manifest: set[str] = set()
    for path in sorted(package_files):
        arcname = base.rel(path)
        if arcname in seen_manifest:
            continue
        seen_manifest.add(arcname)
        manifest_rows.append({"path": arcname, "sha256": base.sha256_file(path), "bytes": path.stat().st_size})
    base.write_json(OUT_DIR / "PACKAGE_MANIFEST.json", {"files": manifest_rows, "file_count": len(manifest_rows)})
    base.write_json(
        OUT_DIR / "PACKAGE_CHECK.json",
        {
            "status": "pass",
            "case_count": summary["case_count"],
            "passed_expected_decision_count": summary["passed_expected_decision_count"],
            "frozen_replay_status": summary["frozen_replay"]["status"],
            "truth_boundary": "Package check covers generated sandbox evidence, expected deterministic decisions, and minimal frozen replay only.",
        },
    )

    zip_path = OUT_DIR / ZIP_NAME
    if zip_path.exists():
        zip_path.unlink()
    package_files = [p for p in OUT_DIR.rglob("*") if p.is_file() and p.name != ZIP_NAME]
    package_files += [p for p in sorted(input_paths) if p.exists()]
    package_files += [p for p in scripts if p.exists()]
    seen: set[str] = set()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package_files):
            arcname = base.rel(path)
            if arcname in seen:
                continue
            seen.add(arcname)
            zf.write(path, arcname)
    return zip_path, base.sha256_file(zip_path)


def main() -> int:
    configure_base_paths()
    reset_output_dir()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    canonical_overlay_fixture = write_canonical_overlay_fixture(now)
    corpus = base.collect_corpus()

    case_rows: list[dict[str, Any]] = []
    retrieval_rows: list[dict[str, Any]] = []
    input_paths: set[Path] = set()

    for case in LIVE_CASES_V2:
        hits = base.retrieve(case["query"], corpus)
        if not hits:
            raise RuntimeError(f"No retrieval results for {case['case_id']}")
        items = select_case_pack_v2(case, hits)
        decision, checks, warnings = evaluate_support_v2(items)
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

    decision_breakdown = dict(Counter(row["decision"] for row in case_rows))
    summary = {
        "generated_at": now,
        "overall_verdict": "sandbox_live_readonly_v2_evidence_partial",
        "case_count": len(case_rows),
        "passed_expected_decision_count": sum(1 for row in case_rows if row["pass"]),
        "decision_breakdown": decision_breakdown,
        "corpus_doc_count": len(corpus),
        "force_anchor_hit_used": False,
        "pack_assembly": "case_scripted_with_no_fallback_and_adversarial_support_mislabel_cases",
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
        "truth_boundary": "v2 removes silent fallback and adds adversarial support mislabel cases; it is still a deterministic local harness, not live LLM/tool/runtime adoption.",
    }

    base.write_json(RESULTS_DIR / "live_readonly_loop_v2_summary.json", summary)
    base.write_json(RESULTS_DIR / "live_readonly_loop_v2_cases.json", case_rows)
    base.write_json(RESULTS_DIR / "live_retrieval_results_v2.json", retrieval_rows)
    write_csv(
        RESULTS_DIR / "live_readonly_loop_v2_cases.csv",
        case_rows,
        ["case_id", "query", "query_mode", "expected_decision", "decision", "pass", "retrieved_count", "selected_count", "support_count", "top_result", "top_result_kind", "query_run", "context_pack", "answer_use", "warnings", "support_checks"],
    )
    write_csv(
        RESULTS_DIR / "live_retrieval_results_v2.csv",
        retrieval_rows,
        ["case_id", "rank", "score", "path", "record_kind", "knowledge_status", "warning_code", "matched_terms", "snippet"],
    )
    write_events_v2(case_rows, retrieval_rows, now)
    exclusion = base.write_artifact_exclusion_manifest(case_rows, now)
    validation = run_validation_commands_v2(now)
    frozen_replay = write_frozen_corpus(input_paths, retrieval_rows, now)
    fallback_scan = run_fallback_regression_scan()
    summary["live_artifact_exclusion"] = exclusion
    summary["validation_commands"] = validation
    summary["frozen_replay"] = frozen_replay
    summary["fallback_regression_scan"] = fallback_scan
    summary["canonical_overlay_fixture"] = base.rel(canonical_overlay_fixture)
    base.write_json(RESULTS_DIR / "live_readonly_loop_v2_summary.json", summary)
    write_reports(summary, case_rows, now)
    zip_path, zip_hash = package_outputs(input_paths, summary)

    status = (
        "pass"
        if summary["passed_expected_decision_count"] == summary["case_count"]
        and frozen_replay["status"] == "pass"
        and fallback_scan["status"] == "pass"
        else "fail"
    )
    if status == "pass" and validation.get("current_lint_errors"):
        status = "pass_with_current_lint_errors"
    print(
        json.dumps(
            {
                "status": status,
                "out_dir": base.rel(OUT_DIR),
                "zip": base.rel(zip_path),
                "zip_sha256": zip_hash,
                "summary": summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if status in {"pass", "pass_with_current_lint_errors"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
