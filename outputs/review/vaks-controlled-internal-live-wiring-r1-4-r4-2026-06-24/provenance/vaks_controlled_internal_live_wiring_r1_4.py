"""R1.4 controlled internal live-wiring pressure harness for VAKS Guarded Answer.

This sandbox tests the production control surface around the already audited
R1.1/R1.3 guarded answer path:

request policy -> feature flag -> eligibility -> guarded path -> release sink
-> user-visible output.

It is intentionally offline and sandbox-only. It does not write to Obsidian,
Truth Core, wiki, raw sources, a database, a service, or a network API.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import time
import unicodedata
import urllib.parse
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_ID = "vaks-controlled-internal-live-wiring-r1-4-r4-2026-06-24"
DEFAULT_OUTPUT = ROOT / "outputs" / "review" / RUN_ID
OUTPUT_ROOT = ROOT / "outputs" / "review"
OUTPUT_NAME_PREFIX = "vaks-controlled-internal-live-wiring-r1-4-r4-"
VALID_OUTPUT_NAME_RE = re.compile(
    r"^vaks-controlled-internal-live-wiring-r1-4-r4-(quick-)?\d{4}-\d{2}-\d{2}$"
    r"|^vaks-controlled-internal-live-wiring-r1-4-r4-append-only-\d+-\d+$"
)
R11_TOOL = ROOT / "tools" / "vaks_guarded_answer_wiring.py"
R12_TOOL = ROOT / "tools" / "vaks_guarded_answer_runtime_comparison_r1_2.py"
R13_TOOL = ROOT / "tools" / "vaks_guarded_answer_replay_simulation_r1_3.py"
VAKS_GUARD = ROOT / "tools" / "vaks_guard.py"
R11_OUTPUT = ROOT / "outputs" / "review" / "vaks-guarded-answer-wiring-r1-1-2026-06-23"
R12_OUTPUT = ROOT / "outputs" / "review" / "vaks-guarded-answer-runtime-comparison-r1-2-2026-06-23"
R13_OUTPUT = ROOT / "outputs" / "review" / "vaks-guarded-answer-production-shaped-replay-r1-3-r3-2026-06-24"
FORMAL_OBSIDIAN_VAULT = Path("H:/Obsidian/资料库")
RAW_ROOT = ROOT / "raw"

INTERNAL_ALLOWLIST = {"internal-alpha", "internal-beta", "admin-smoke"}
TENANT_ALLOWLIST = {"tenant-internal"}
LOW_RISK_MODES = {"orientation", "source_inspection"}
DOMAIN_ALLOWLIST = {"general", "source_lookup"}
TRUSTED_POLICY_SOURCE = "trusted_runtime"
TRUSTED_FLAG_SOURCE = "trusted_feature_flag_service"
USER_POLICY_KEYS = {
    "trusted_policy_context",
    "trusted_runtime_context",
    "query_mode",
    "risk_level",
    "domain",
    "guarded_answer_mode",
    "action_requested",
    "tenant_id",
    "principal_id",
    "flag_source",
    "supplied_by",
}

USER_FACING_CASE_IDS = [
    "case-001-direct-web-annotation",
    "case-002-direct-prov",
    "case-003-direct-rag-attribution",
    "case-004-direct-r05",
    "case-005-partial-flexnote",
    "case-006-scope-outsourcing",
    "case-007-partial-no-expression",
    "case-008-partial-composite",
    "case-009-missing-anchor",
    "case-010-candidate-only",
    "case-011-rank-score",
    "case-012-stale-policy",
    "case-013-conflict",
    "case-014-mixed-answer",
    "case-034-supported-plus-partial",
    "case-039-all-supported-multi-claim",
]


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def pretty_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def is_sha256_hex(value: str) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[0-9a-f]{64}", value))


def write_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    write_lf(path, "".join(stable_json(row) + "\n" for row in rows))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_output_dir(output_dir: Path) -> Path:
    resolved = output_dir.resolve()
    output_root = OUTPUT_ROOT.resolve()
    if not is_relative_to(resolved, output_root):
        raise ValueError(f"Output directory must be under {OUTPUT_ROOT.as_posix()}: {output_dir}")
    if any(ord(char) < 32 for char in resolved.name):
        raise ValueError("Output directory name must not contain control characters")
    if not VALID_OUTPUT_NAME_RE.fullmatch(resolved.name):
        raise ValueError(f"Output directory name is not an allowed R1.4 r4 bundle name: {resolved.name}")
    return resolved


def collect_hashes(root: Path, *, exclude: set[str] | None = None) -> dict[str, str]:
    exclude = exclude or set()
    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = rel(path, root)
        if relative in exclude:
            continue
        hashes[relative] = sha256_bytes(path.read_bytes())
    return hashes


def tree_hash(root: Path, *, exclude: set[str] | None = None) -> str:
    return sha256_text(stable_json(collect_hashes(root, exclude=exclude)))


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(round((pct / 100.0) * (len(ordered) - 1))))
    return ordered[index]


def dependency_checks(r11: Any, r12: Any, r13: Any) -> dict[str, Any]:
    checks: dict[str, Any] = {
        "r1_1_tool_sha256": sha256_bytes(R11_TOOL.read_bytes()),
        "r1_2_tool_sha256": sha256_bytes(R12_TOOL.read_bytes()),
        "r1_3_tool_sha256": sha256_bytes(R13_TOOL.read_bytes()),
        "vaks_guard_sha256": sha256_bytes(VAKS_GUARD.read_bytes()),
        "r1_1_output": R11_OUTPUT.as_posix(),
        "r1_2_output": R12_OUTPUT.as_posix(),
        "r1_3_output": R13_OUTPUT.as_posix(),
    }
    try:
        checks["r1_1_self_test"] = r11.verify_bundle(R11_OUTPUT)
    except Exception as exc:  # pragma: no cover - recorded in bundle
        checks["r1_1_self_test"] = {"status": "error", "error": repr(exc)}
    try:
        checks["r1_2_self_test"] = r12.verify_bundle(R12_OUTPUT)
    except Exception as exc:  # pragma: no cover - recorded in bundle
        checks["r1_2_self_test"] = {"status": "error", "error": repr(exc)}
    try:
        checks["r1_3_self_test"] = r13.verify_bundle(R13_OUTPUT)
    except Exception as exc:  # pragma: no cover - recorded in bundle
        checks["r1_3_self_test"] = {"status": "error", "error": repr(exc)}
    checks["status"] = (
        "pass"
        if checks["r1_1_self_test"].get("status") == "pass"
        and checks["r1_2_self_test"].get("status") == "pass"
        and checks["r1_3_self_test"].get("status") == "pass"
        else "fail"
    )
    return checks


def clone_live_case(r11: Any, r13: Any, base: dict[str, Any], request_id: str, query: str) -> dict[str, Any]:
    cloned = r13.clone_case(r11, base, request_id, query, source_slice="r1_4_controlled_live_fixture")
    aligned = r13.attach_alignment(cloned, topic_source=base["case_id"])
    bind_case_query(aligned, query)
    return aligned


def bind_case_query(case: dict[str, Any], query: str) -> None:
    query_hash = sha256_text(query)
    case["query"] = query
    case["request_query_sha256"] = query_hash
    case.setdefault("draft", {})["query"] = query
    case["draft"]["query_sha256"] = query_hash
    case.setdefault("alignment_contract", {})["query_sha256"] = query_hash


def validate_query_binding(request: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    user_payload = request.get("user_payload") if isinstance(request.get("user_payload"), dict) else {}
    trusted = request.get("trusted_runtime_context") if isinstance(request.get("trusted_runtime_context"), dict) else {}
    errors: list[str] = []
    user_query = str(user_payload.get("query", ""))
    trusted_query = str(trusted.get("query", ""))
    user_hash = user_payload.get("query_sha256", "")
    trusted_hash = trusted.get("query_sha256", "")
    computed_user_hash = sha256_text(user_query)
    computed_trusted_hash = sha256_text(trusted_query)
    if not user_query:
        errors.append("missing_user_query")
    if not trusted_query:
        errors.append("missing_trusted_query")
    if user_hash != computed_user_hash:
        errors.append("user_query_hash_mismatch")
    if trusted_hash != computed_trusted_hash:
        errors.append("trusted_query_hash_mismatch")
    if user_query != trusted_query:
        errors.append("user_query_trusted_query_mismatch")
    if case.get("query") != trusted_query:
        errors.append("case_query_mismatch")
    if case.get("request_query_sha256") != trusted_hash:
        errors.append("case_query_hash_mismatch")
    if case.get("draft", {}).get("query") != trusted_query:
        errors.append("draft_query_mismatch")
    if case.get("draft", {}).get("query_sha256") != trusted_hash:
        errors.append("draft_query_hash_mismatch")
    if case.get("alignment_contract", {}).get("query_sha256") != trusted_hash:
        errors.append("alignment_query_hash_mismatch")
    return {
        "ok": not errors,
        "errors": errors,
        "user_query_sha256": user_hash,
        "trusted_query_sha256": trusted_hash,
        "computed_user_query_sha256": computed_user_hash,
    }


def output_hash(final: dict[str, Any]) -> str:
    return sha256_text(final.get("final_text", ""))


class LiveReleaseSink:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []
        self.guard_passed = False

    def attempt_stream_fact(self, text: str, stage: str) -> None:
        self.events.append(
            {
                "stage": stage,
                "event": "pre_guard_fact_stream_attempt",
                "text_sha256": sha256_text(text),
                "allowed": False,
                "blocked": True,
            }
        )

    def commit(self, final: dict[str, Any]) -> dict[str, Any]:
        declared_hash = final.get("final_sha256", "")
        actual_hash = output_hash(final)
        declared_hash_valid = is_sha256_hex(declared_hash)
        declared_hash_matches_text = declared_hash == actual_hash
        allowed = (
            self.guard_passed
            and final.get("atomic_release_phase") == "committed_final"
            and final.get("release_state") == "released"
            and declared_hash_valid
            and declared_hash_matches_text
        )
        event = {
            "stage": "release_sink",
            "event": "user_visible_commit_attempt",
            "guard_passed": self.guard_passed,
            "atomic_release_phase": final.get("atomic_release_phase", ""),
            "release_state": final.get("release_state", ""),
            "declared_final_sha256": declared_hash,
            "actual_final_sha256": actual_hash,
            "final_sha256": actual_hash,
            "declared_hash_valid": declared_hash_valid,
            "declared_hash_matches_text": declared_hash_matches_text,
            "allowed": allowed,
        }
        self.events.append(event)
        return event

    def leaked_before_guard(self) -> bool:
        return any(
            event.get("event") == "pre_guard_fact_stream_attempt" and event.get("allowed")
            for event in self.events
        )


def fallback_visible_text(reason: str, *, high_risk: bool) -> dict[str, Any]:
    if high_risk:
        text = "This request needs review. No unchecked answer was released."
        policy = "review"
        release_state = "review_required"
        label = "needs review"
    else:
        text = "Evidence verification is unavailable. No unchecked answer was released."
        policy = "abstain"
        release_state = "withheld"
        label = "not enough verified evidence"
    final = {
        "final_text": text,
        "final_sha256": sha256_text(text),
        "answer_policy": policy,
        "status_label": label,
        "release_state": release_state,
        "evaluation_state": "unavailable",
        "atomic_release_phase": f"controlled_live_fallback:{reason}",
        "visible_claim_ids": [],
        "citations": [],
        "action_readiness_granted": False,
        "reviewed_truth_granted": False,
        "promotion_granted": False,
    }
    return final


def normalize_domain(value: Any) -> str:
    return str(value or "").strip().lower()


def effective_policy(request: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    trusted = request.get("trusted_runtime_context")
    user_payload = request.get("user_payload") if isinstance(request.get("user_payload"), dict) else {}
    reasons: list[str] = []
    if not isinstance(trusted, dict):
        trusted = {}
        reasons.append("missing_trusted_runtime_context")
    forbidden_user_keys = sorted(USER_POLICY_KEYS.intersection(user_payload))
    if forbidden_user_keys:
        reasons.append("user_payload_policy_fields_present:" + ",".join(forbidden_user_keys))

    policy = {
        "principal_id": trusted.get("principal_id", ""),
        "tenant_id": trusted.get("tenant_id", ""),
        "query_mode": trusted.get("query_mode", ""),
        "risk_level": trusted.get("risk_level", ""),
        "domain": normalize_domain(trusted.get("domain", "")),
        "guarded_answer_mode": trusted.get("guarded_answer_mode", ""),
        "action_requested": bool(trusted.get("action_requested", False)),
        "supplied_by": trusted.get("supplied_by", ""),
        "flag_source": trusted.get("flag_source", ""),
        "case_class": trusted.get("case_class", ""),
        "query": trusted.get("query", ""),
        "query_sha256": trusted.get("query_sha256", ""),
    }

    required_matches = {
        "user_id": "principal_id",
        "tenant_id": "tenant_id",
        "query_mode": "query_mode",
        "risk_level": "risk_level",
        "guarded_answer_mode": "guarded_answer_mode",
    }
    for top_key, trusted_key in required_matches.items():
        if request.get(top_key) != policy.get(trusted_key):
            reasons.append(f"top_level_mismatch:{top_key}")
    if normalize_domain(request.get("domain", "")) != policy["domain"]:
        reasons.append("top_level_mismatch:domain")

    if policy["supplied_by"] != TRUSTED_POLICY_SOURCE:
        reasons.append("invalid_policy_source")
    if policy["flag_source"] != TRUSTED_FLAG_SOURCE:
        reasons.append("invalid_flag_source")
    if policy["guarded_answer_mode"] != "enforce":
        reasons.append("mode_not_enforce")
    if policy["principal_id"] not in INTERNAL_ALLOWLIST:
        reasons.append("principal_not_internal_allowlist")
    if policy["tenant_id"] not in TENANT_ALLOWLIST:
        reasons.append("tenant_not_allowlisted")
    if policy["risk_level"] != "low":
        reasons.append("risk_not_low")
    if policy["query_mode"] not in LOW_RISK_MODES:
        reasons.append("query_mode_not_low_risk")
    if policy["domain"] not in DOMAIN_ALLOWLIST:
        reasons.append("domain_not_allowlisted")
    if policy["action_requested"]:
        reasons.append("action_requested")
    if policy["case_class"] != "user_facing":
        reasons.append("case_not_user_facing")
    return policy, reasons


def is_eligible(request: dict[str, Any]) -> tuple[bool, list[str]]:
    _, reasons = effective_policy(request)
    return not reasons, reasons


def write_guard_allows(path: Path, output_dir: Path) -> bool:
    resolved = path.resolve()
    output_resolved = output_dir.resolve()
    try:
        formal = FORMAL_OBSIDIAN_VAULT.resolve()
    except OSError:
        formal = FORMAL_OBSIDIAN_VAULT
    if is_relative_to(resolved, formal):
        return False
    if is_relative_to(resolved, (ROOT / "wiki").resolve()):
        return False
    if is_relative_to(resolved, (ROOT / "raw").resolve()):
        return False
    return is_relative_to(resolved, output_resolved)


def has_control_char(value: str) -> bool:
    return any(ord(char) < 32 for char in value)


def path_text_errors(value: str, field_name: str) -> list[str]:
    errors: list[str] = []
    if value != value.strip():
        errors.append(f"{field_name}_surrounding_whitespace")
    if unicodedata.normalize("NFC", value) != value:
        errors.append(f"{field_name}_non_nfc")
    if has_control_char(value):
        errors.append(f"{field_name}_control_char")
    if "%" in value:
        errors.append(f"{field_name}_percent_encoding")
        if re.search(r"%(?![0-9A-Fa-f]{2})", value):
            errors.append(f"{field_name}_invalid_percent_escape")
        try:
            decoded = urllib.parse.unquote(value, errors="strict")
        except UnicodeDecodeError:
            decoded = ""
            errors.append(f"{field_name}_invalid_percent_decoding")
        if decoded:
            if has_control_char(decoded):
                errors.append(f"{field_name}_decoded_control_char")
            if "\\" in decoded:
                errors.append(f"{field_name}_decoded_backslash")
            decoded_parts = [part for part in re.split(r"[\\/]+", decoded) if part]
            if any(part in {".", ".."} for part in decoded_parts):
                errors.append(f"{field_name}_decoded_dot_segment")
            if unicodedata.normalize("NFC", decoded) != decoded:
                errors.append(f"{field_name}_decoded_non_nfc")
    return errors


def has_symlink_component(path: Path, stop_at: Path) -> bool:
    current = stop_at
    try:
        relative = path.relative_to(stop_at)
    except ValueError:
        return False
    for part in relative.parts:
        current = current / part
        if current.exists() and current.is_symlink():
            return True
    return False


def canonical_source_path(source_ref: str) -> tuple[Path | None, list[str]]:
    errors: list[str] = []
    if not source_ref:
        return None, errors
    errors.extend(path_text_errors(source_ref, "source_ref"))
    if "\\" in source_ref:
        errors.append("source_ref_backslash")
    source_path = Path(source_ref)
    if source_path.is_absolute():
        errors.append("source_ref_absolute")
        candidate = source_path
    else:
        candidate = ROOT / source_path
    if ".." in source_path.parts:
        errors.append("source_ref_dotdot")
    resolved = candidate.resolve(strict=False)
    raw_root = RAW_ROOT.resolve()
    if not is_relative_to(resolved, raw_root):
        errors.append("source_ref_outside_raw_root")
    if has_symlink_component(resolved, raw_root):
        errors.append("source_ref_symlink_component")
    return resolved, errors


def canonical_authority_for_source(source_ref: str) -> dict[str, str]:
    resolved, errors = canonical_source_path(source_ref)
    if errors or resolved is None:
        return {"authority_bucket": "", "record_kind": "", "resolved_path": resolved.as_posix() if resolved else ""}
    record_kind = "source_card" if resolved.suffix.lower() in {".md", ".json"} else "raw_blob"
    return {"authority_bucket": "raw_source", "record_kind": record_kind, "resolved_path": resolved.as_posix()}


def source_authority_coherence(case: dict[str, Any]) -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    if not isinstance(case.get("claim_support_map", []), list):
        return {
            "ok": False,
            "violation_count": 1,
            "violations": [{"claim_id": "", "source_ref": "", "reason": "claim_support_map_not_list"}],
        }
    for support in case.get("claim_support_map", []):
        source_ref = support.get("source_ref", "")
        if not source_ref:
            continue
        bucket = support.get("support_authority_bucket", "")
        record_kind = support.get("support_record_kind", "")
        resolved, path_errors = canonical_source_path(source_ref)
        for error in path_errors:
            violations.append(
                {
                    "claim_id": support.get("claim_id", ""),
                    "source_ref": source_ref,
                    "reason": error,
                }
            )
        canonical = canonical_authority_for_source(source_ref)
        if canonical["authority_bucket"] and bucket != canonical["authority_bucket"]:
            violations.append(
                {
                    "claim_id": support.get("claim_id", ""),
                    "source_ref": source_ref,
                    "reason": "authority_bucket_mismatch",
                }
            )
        if canonical["record_kind"] and record_kind != canonical["record_kind"]:
            violations.append(
                {
                    "claim_id": support.get("claim_id", ""),
                    "source_ref": source_ref,
                    "reason": "record_kind_mismatch",
                }
            )
        anchor_ref = support.get("anchor_ref", "")
        if anchor_ref:
            anchor_text_errors = path_text_errors(anchor_ref, "anchor_ref")
            if anchor_text_errors or "\\" in anchor_ref:
                violations.append(
                    {
                        "claim_id": support.get("claim_id", ""),
                        "source_ref": source_ref,
                        "reason": "anchor_ref_invalid_characters",
                    }
                )
                for error in anchor_text_errors:
                    violations.append(
                        {
                            "claim_id": support.get("claim_id", ""),
                            "source_ref": source_ref,
                            "reason": error,
                        }
                    )
            anchor_source = anchor_ref.split("#", 1)[0]
            if anchor_source != source_ref:
                violations.append(
                    {
                        "claim_id": support.get("claim_id", ""),
                        "source_ref": source_ref,
                        "reason": "anchor_source_mismatch",
                    }
                )
            anchor_resolved, anchor_errors = canonical_source_path(anchor_source)
            if anchor_errors:
                violations.append(
                    {
                        "claim_id": support.get("claim_id", ""),
                        "source_ref": source_ref,
                        "reason": "anchor_source_invalid",
                    }
                )
            if resolved is not None and anchor_resolved is not None and resolved != anchor_resolved:
                violations.append(
                    {
                        "claim_id": support.get("claim_id", ""),
                        "source_ref": source_ref,
                        "reason": "anchor_resolved_source_mismatch",
                    }
                )
        if bucket == "raw_source" and path_errors:
            violations.append(
                {
                    "claim_id": support.get("claim_id", ""),
                    "source_ref": source_ref,
                    "reason": "raw_source_claimed_for_invalid_path",
                }
            )
    return {
        "ok": not violations,
        "violation_count": len(violations),
        "violations": violations,
    }


def build_live_requests(r11: Any, r12: Any, r13: Any) -> list[dict[str, Any]]:
    all_cases = r12.runtime_cases(r11)
    base_cases = [case for case in all_cases if case["case_id"] in USER_FACING_CASE_IDS]
    requests: list[dict[str, Any]] = []

    def make_request(
        *,
        request_id: str,
        user_id: str,
        tenant_id: str,
        query_mode: str,
        risk_level: str,
        domain: str,
        mode: str,
        case: dict[str, Any],
        fault_type: str = "",
        case_class: str = "user_facing",
        trusted_overrides: dict[str, Any] | None = None,
        top_overrides: dict[str, Any] | None = None,
        user_payload_overrides: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        query = case["query"]
        query_hash = sha256_text(query)
        trusted = {
            "supplied_by": TRUSTED_POLICY_SOURCE,
            "flag_source": TRUSTED_FLAG_SOURCE,
            "principal_id": user_id,
            "tenant_id": tenant_id,
            "query_mode": query_mode,
            "risk_level": risk_level,
            "domain": domain,
            "guarded_answer_mode": mode,
            "action_requested": query_mode == "action",
            "case_class": case_class,
            "query": query,
            "query_sha256": query_hash,
        }
        if trusted_overrides:
            trusted.update(trusted_overrides)
        user_payload = {
            "query": query,
            "query_sha256": query_hash,
        }
        if user_payload_overrides:
            user_payload.update(user_payload_overrides)
        request = {
            "request_id": request_id,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "query_mode": query_mode,
            "risk_level": risk_level,
            "domain": domain,
            "guarded_answer_mode": mode,
            "trusted_runtime_context": trusted,
            "user_payload": user_payload,
            "user_text": user_payload.get("query", ""),
            "case": case,
            "fault_type": fault_type,
            "case_class": case_class,
        }
        if top_overrides:
            request.update(top_overrides)
        return request

    personas = [
        ("internal-alpha", "orientation", "low", "general", "enforce"),
        ("internal-beta", "source_inspection", "low", "source_lookup", "enforce"),
        ("external-user", "orientation", "low", "general", "enforce"),
        ("internal-alpha", "review", "medium", "general", "enforce"),
        ("internal-alpha", "action", "high", "finance", "enforce"),
        ("internal-alpha", "orientation", "low", "Legal", "enforce"),
        ("internal-alpha", "orientation", "low", "general", "off"),
    ]
    for index, base in enumerate(base_cases, start=1):
        for p_index, (user_id, query_mode, risk_level, domain, mode) in enumerate(personas, start=1):
            request_id = f"live-{index:03d}-{p_index:02d}"
            query_prefix = {
                "orientation": "Please orient me: ",
                "source_inspection": "Show source basis only: ",
                "review": "Review for decision: ",
                "action": "Can I act on this now: ",
            }.get(query_mode, "")
            case = clone_live_case(r11, r13, base, request_id, query_prefix + base["query"])
            case["query_mode"] = query_mode
            case["risk_level"] = risk_level
            case["curated_user_case"] = True
            requests.append(
                make_request(
                    request_id=request_id,
                    user_id=user_id,
                    tenant_id="tenant-internal",
                    query_mode=query_mode,
                    risk_level=risk_level,
                    domain=domain,
                    mode=mode,
                    case=case,
                )
            )

    adversarial_base = base_cases[0]
    adversarial_specs = [
        (
            "policy-bypass-supplied-by-user",
            {"supplied_by": "user"},
            {},
            {},
        ),
        (
            "policy-bypass-top-tenant-external",
            {},
            {"tenant_id": "tenant-external"},
            {},
        ),
        (
            "policy-bypass-trusted-high-top-low",
            {"risk_level": "high", "query_mode": "action", "domain": "finance", "action_requested": True},
            {"risk_level": "low", "query_mode": "orientation", "domain": "general"},
            {},
        ),
        (
            "policy-bypass-domain-case-legal",
            {"domain": "Legal"},
            {"domain": "Legal"},
            {},
        ),
        (
            "policy-bypass-flag-source-user",
            {"flag_source": "user"},
            {},
            {},
        ),
        (
            "policy-bypass-user-payload-context",
            {},
            {},
            {"trusted_policy_context": {"risk_level": "low"}, "query_mode": "orientation"},
        ),
        (
            "query-binding-user-text-mismatch",
            {},
            {},
            {"query": "员工年假上限是多少？", "query_sha256": sha256_text("员工年假上限是多少？")},
        ),
        (
            "query-binding-user-hash-mismatch",
            {},
            {},
            {"query_sha256": "0" * 64},
        ),
    ]
    for index, (name, trusted_overrides, top_overrides, user_payload_overrides) in enumerate(adversarial_specs, start=1):
        request_id = f"adversarial-{index:03d}-{name}"
        case = clone_live_case(r11, r13, adversarial_base, request_id, "Policy bypass attempt: " + name)
        case["query_mode"] = "orientation"
        case["risk_level"] = "low"
        case["curated_user_case"] = True
        requests.append(
            make_request(
                request_id=request_id,
                user_id="internal-alpha",
                tenant_id="tenant-internal",
                query_mode="orientation",
                risk_level="low",
                domain="general",
                mode="enforce",
                case=case,
                trusted_overrides=trusted_overrides,
                top_overrides=top_overrides,
                user_payload_overrides=user_payload_overrides,
            )
        )

    source_traversal_specs = [
        ("source-traversal-dotdot", "raw/../outputs/review/evil-runtime-artifact.md"),
        ("source-percent-encoded-dotdot", "raw/%2e%2e/outputs/review/evil-runtime-artifact.md"),
        ("source-backslash", "raw\\articles\\2026-05-30-w3c-web-annotation-source.md"),
        ("source-absolute", str((ROOT / "outputs" / "review" / "evil.md").resolve())),
    ]
    for index, (name, bad_source_ref) in enumerate(source_traversal_specs, start=1):
        request_id = f"adversarial-source-{index:03d}-{name}"
        case = clone_live_case(r11, r13, adversarial_base, request_id, "Source authority bypass attempt: " + name)
        case["query_mode"] = "orientation"
        case["risk_level"] = "low"
        for support in case.get("claim_support_map", []):
            if support.get("source_ref"):
                support["source_ref"] = bad_source_ref
                support["anchor_ref"] = bad_source_ref + "#fake-anchor"
                support["support_authority_bucket"] = "raw_source"
                support["support_record_kind"] = "source_card"
        requests.append(
            make_request(
                request_id=request_id,
                user_id="internal-alpha",
                tenant_id="tenant-internal",
                query_mode="orientation",
                risk_level="low",
                domain="general",
                mode="enforce",
                case=case,
            )
        )

    fault_templates = [
        ("guard_block", "case-001-direct-web-annotation", "low", "orientation", "general"),
        ("guard_error", "case-001-direct-web-annotation", "low", "orientation", "general"),
        ("guard_timeout", "case-001-direct-web-annotation", "low", "orientation", "general"),
        ("retrieval_empty", "case-005-partial-flexnote", "low", "orientation", "general"),
        ("acl_denied", "case-005-partial-flexnote", "low", "orientation", "general"),
        ("feature_flag_error", "case-001-direct-web-annotation", "low", "orientation", "general"),
        ("streaming_fact_text_before_brake", "case-016-action-injection", "low", "orientation", "general"),
        ("invalid_json_draft", "case-001-direct-web-annotation", "low", "orientation", "general"),
        ("bad_final_hash_after_guard", "case-001-direct-web-annotation", "low", "orientation", "general"),
    ]
    by_id = {case["case_id"]: case for case in all_cases}
    for index, (fault_type, base_id, risk_level, query_mode, domain) in enumerate(fault_templates, start=1):
        request_id = f"fault-live-{index:03d}-{fault_type}"
        base = by_id[base_id]
        case = clone_live_case(r11, r13, base, request_id, "Controlled live fault: " + fault_type)
        case["query_mode"] = query_mode
        case["risk_level"] = risk_level
        case["curated_user_case"] = True
        requests.append(
            make_request(
                request_id=request_id,
                user_id="internal-alpha",
                tenant_id="tenant-internal",
                query_mode=query_mode,
                risk_level=risk_level,
                domain=domain,
                mode="enforce",
                case=case,
                fault_type=fault_type,
            )
        )
    return requests


def process_live_request(
    r11: Any,
    r12: Any,
    r13: Any,
    vaks_guard: Any,
    request: dict[str, Any],
    output_dir: Path,
) -> dict[str, Any]:
    started = time.perf_counter()
    sink = LiveReleaseSink()
    policy, eligibility_reasons = effective_policy(request)
    query_binding = validate_query_binding(request, request["case"])
    if not query_binding["ok"]:
        eligibility_reasons = eligibility_reasons + ["query_binding_failed:" + ",".join(query_binding["errors"])]
    eligible = not eligibility_reasons
    source_status = source_authority_coherence(request["case"])
    if not source_status["ok"]:
        eligible = False
        eligibility_reasons = eligibility_reasons + ["source_authority_coherence_failed"]
    high_risk = policy.get("risk_level") == "high" or policy.get("query_mode") == "action"
    r13_result: dict[str, Any] | None = None
    guarded_applied = False
    if not eligible:
        final = fallback_visible_text("not_eligible_for_controlled_enforce", high_risk=high_risk)
        guard_status = "not_run"
        output_event = sink.commit(final)
    else:
        guarded_applied = True
        r13_request = {
            "request_id": request["request_id"],
            "kind": "prodlike_replay",
            "feature_flag_mode": "enforce",
            "fault_type": request.get("fault_type", ""),
            "case": request["case"],
        }
        if request.get("fault_type") == "streaming_fact_text_before_brake":
            sink.attempt_stream_fact(request["case"].get("draft", {}).get("draft_text", ""), "generate_draft")
        r13_result = r13.process_request(r11, r12, vaks_guard, r13_request, output_dir / "guarded_path")
        guard_status = r13_result.get("guard_status", "unknown")
        final = copy.deepcopy(r13_result.get("final_answer", {}))
        if request.get("fault_type") == "bad_final_hash_after_guard":
            final["final_sha256"] = "0" * 64
        if not (
            guard_status == "pass"
            and final.get("atomic_release_phase") == "committed_final"
            and final.get("release_state") == "released"
        ):
            final = fallback_visible_text("guarded_path_not_releasable", high_risk=high_risk)
        sink.guard_passed = guard_status == "pass"
        output_event = sink.commit(final)
        if not output_event.get("allowed"):
            final = fallback_visible_text("release_sink_denied", high_risk=high_risk)

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    visible_text = final.get("final_text", "")
    final_sha = output_hash(final)
    result = {
        "request_id": request["request_id"],
        "user_id": policy.get("principal_id", ""),
        "tenant_id": policy.get("tenant_id", ""),
        "query_mode": policy.get("query_mode", ""),
        "risk_level": policy.get("risk_level", ""),
        "domain": policy.get("domain", ""),
        "guarded_answer_mode": policy.get("guarded_answer_mode", ""),
        "top_level_request": {
            "user_id": request.get("user_id", ""),
            "tenant_id": request.get("tenant_id", ""),
            "query_mode": request.get("query_mode", ""),
            "risk_level": request.get("risk_level", ""),
            "domain": request.get("domain", ""),
            "guarded_answer_mode": request.get("guarded_answer_mode", ""),
        },
        "effective_policy": policy,
        "query_binding": query_binding,
        "eligible_for_guarded_enforce": eligible,
        "eligibility_reasons": eligibility_reasons,
        "policy_binding_error": any(reason.startswith("top_level_mismatch:") for reason in eligibility_reasons),
        "source_authority_coherence": source_status,
        "guarded_applied": guarded_applied,
        "fault_type": request.get("fault_type", ""),
        "guard_status": guard_status,
        "release_sink_events": sink.events,
        "release_sink_allowed": bool(output_event.get("allowed")),
        "release_sink_final_sha256": output_event.get("final_sha256", ""),
        "final_answer": final,
        "user_visible_output": {
            "text": visible_text,
            "sha256": final_sha,
            "release_state": final.get("release_state", ""),
            "answer_policy": final.get("answer_policy", ""),
            "status_label": final.get("status_label", ""),
        },
        "pre_guard_fact_text_leaked": sink.leaked_before_guard(),
        "r1_3_result": {
            "request_id": r13_result.get("request_id") if r13_result else "",
            "release_state": r13_result.get("release_state") if r13_result else "",
            "answer_policy": r13_result.get("answer_policy") if r13_result else "",
            "guard_status": r13_result.get("guard_status") if r13_result else "",
            "alignment": r13_result.get("alignment") if r13_result else {},
            "comparison": r13_result.get("comparison") if r13_result else {},
            "runtime_fault": r13_result.get("runtime_fault") if r13_result else {},
        },
        "elapsed_ms": round(elapsed_ms, 6),
    }
    return result


def run_live_matrix(r11: Any, r12: Any, r13: Any, vaks_guard: Any, output_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    requests = build_live_requests(r11, r12, r13)
    results = [
        process_live_request(r11, r12, r13, vaks_guard, request, output_dir)
        for request in requests
    ]
    return requests, results


def workspace_safety_checks(output_dir: Path) -> dict[str, Any]:
    attempted = [
        output_dir / "allowed-sandbox-write-probe.txt",
        output_dir.parent / f"{output_dir.name}_evil" / "prefix-trick.md",
        FORMAL_OBSIDIAN_VAULT / "vaks-r1-4-should-not-write.md",
        ROOT / "wiki" / "vaks-r1-4-should-not-write.md",
        ROOT / "raw" / "vaks-r1-4-should-not-write.md",
    ]
    checks = []
    for path in attempted:
        allowed = write_guard_allows(path, output_dir)
        checks.append({"path": path.as_posix(), "allowed": allowed})
    return {
        "formal_obsidian_path": FORMAL_OBSIDIAN_VAULT.as_posix(),
        "checks": checks,
        "blocked_non_sandbox_write_count": sum(1 for item in checks if not item["allowed"]),
        "allowed_non_sandbox_write_count": sum(
            1
            for item in checks
            if item["allowed"] and not item["path"].startswith(output_dir.as_posix())
        ),
        "status": "pass" if checks[0]["allowed"] and all(not item["allowed"] for item in checks[1:]) else "fail",
        "note": "No write is attempted for blocked paths; this is a path-policy probe only.",
    }


def result_metrics(results: list[dict[str, Any]], workspace_checks: dict[str, Any]) -> dict[str, Any]:
    eligible = [row for row in results if row["eligible_for_guarded_enforce"]]
    ineligible = [row for row in results if not row["eligible_for_guarded_enforce"]]
    released = [row for row in results if row["final_answer"].get("release_state") == "released"]
    guarded_released = [row for row in released if row["guarded_applied"]]
    metrics = {
        "request_count": len(results),
        "eligible_request_count": len(eligible),
        "ineligible_request_count": len(ineligible),
        "guarded_applied_count": sum(1 for row in results if row["guarded_applied"]),
        "guarded_released_count": len(guarded_released),
        "ineligible_guarded_applied_count": sum(1 for row in ineligible if row["guarded_applied"]),
        "external_user_guarded_applied_count": sum(
            1 for row in results if row["user_id"] not in INTERNAL_ALLOWLIST and row["guarded_applied"]
        ),
        "blocked_domain_guarded_applied_count": sum(
            1 for row in results if row["domain"] not in DOMAIN_ALLOWLIST and row["guarded_applied"]
        ),
        "policy_binding_error_guarded_applied_count": sum(
            1 for row in results if row.get("policy_binding_error") and row["guarded_applied"]
        ),
        "query_binding_failure_count": sum(1 for row in results if not row.get("query_binding", {}).get("ok", False)),
        "query_binding_failure_guarded_applied_count": sum(
            1 for row in results if not row.get("query_binding", {}).get("ok", False) and row["guarded_applied"]
        ),
        "query_binding_failure_released_count": sum(
            1
            for row in results
            if not row.get("query_binding", {}).get("ok", False)
            and row["final_answer"].get("release_state") == "released"
        ),
        "invalid_policy_source_guarded_applied_count": sum(
            1
            for row in results
            if any(
                reason in {"invalid_policy_source", "invalid_flag_source"}
                for reason in row.get("eligibility_reasons", [])
            )
            and row["guarded_applied"]
        ),
        "non_user_facing_guarded_applied_count": sum(
            1
            for row in results
            if row.get("effective_policy", {}).get("case_class") != "user_facing"
            and row["guarded_applied"]
        ),
        "source_authority_coherence_failure_count": sum(
            1 for row in results if not row.get("source_authority_coherence", {}).get("ok", False)
        ),
        "source_authority_coherence_failure_guarded_applied_count": sum(
            1
            for row in results
            if not row.get("source_authority_coherence", {}).get("ok", False)
            and row["guarded_applied"]
        ),
        "source_authority_coherence_failure_released_count": sum(
            1
            for row in results
            if not row.get("source_authority_coherence", {}).get("ok", False)
            and row["final_answer"].get("release_state") == "released"
        ),
        "high_risk_guarded_released_count": sum(
            1 for row in results if row["risk_level"] == "high" and row["final_answer"].get("release_state") == "released"
        ),
        "action_mode_guarded_released_count": sum(
            1 for row in results if row["query_mode"] == "action" and row["final_answer"].get("release_state") == "released"
        ),
        "guard_failed_visible_release_count": sum(
            1
            for row in results
            if row["guard_status"] in {"block", "error", "timeout"}
            and row["final_answer"].get("release_state") in {"released", "released_degraded"}
        ),
        "release_sink_denied_but_visible_count": sum(
            1
            for row in results
            if not row["release_sink_allowed"]
            and row["final_answer"].get("release_state") in {"released", "released_degraded"}
        ),
        "sink_hash_mismatch_count": sum(
            1
            for row in results
            if row["release_sink_allowed"]
            and row["release_sink_final_sha256"] != row["user_visible_output"]["sha256"]
        ),
        "declared_final_hash_mismatch_denied_count": sum(
            1
            for row in results
            for event in row.get("release_sink_events", [])
            if event.get("event") == "user_visible_commit_attempt"
            and not event.get("declared_hash_matches_text", True)
            and not event.get("allowed", False)
        ),
        "pre_guard_fact_text_leak_count": sum(1 for row in results if row["pre_guard_fact_text_leaked"]),
        "action_readiness_granted_count": sum(
            1 for row in results if row["final_answer"].get("action_readiness_granted")
        ),
        "reviewed_truth_granted_count": sum(
            1 for row in results if row["final_answer"].get("reviewed_truth_granted")
        ),
        "promotion_granted_count": sum(1 for row in results if row["final_answer"].get("promotion_granted")),
        "workspace_allowed_non_sandbox_write_count": workspace_checks["allowed_non_sandbox_write_count"],
        "workspace_safety_status": workspace_checks["status"],
        "fallback_count": sum(1 for row in results if row["final_answer"].get("release_state") != "released"),
        "avg_elapsed_ms": round(sum(row["elapsed_ms"] for row in results) / len(results), 6) if results else 0.0,
        "p95_elapsed_ms": round(percentile([row["elapsed_ms"] for row in results], 95), 6),
        "p99_elapsed_ms": round(percentile([row["elapsed_ms"] for row in results], 99), 6),
    }
    return metrics


def fast_gate_decision(sample: dict[str, Any]) -> tuple[bool, str]:
    eligible, reasons = is_eligible(sample)
    if not eligible:
        return False, ",".join(reasons)
    if sample.get("guard_status") != "pass":
        return False, "guard_not_pass"
    if sample.get("release_state") != "released":
        return False, "not_released"
    return True, "released"


def run_pressure(results: list[dict[str, Any]], *, sequential_count: int = 500_000, parallel_count: int = 120_000) -> dict[str, Any]:
    samples = [
        {
            "guarded_answer_mode": row["guarded_answer_mode"],
            "user_id": row["user_id"],
            "tenant_id": row["tenant_id"],
            "query_mode": row["query_mode"],
            "risk_level": row["risk_level"],
            "domain": row["domain"],
            "trusted_runtime_context": copy.deepcopy(row.get("effective_policy", {})),
            "guard_status": row["guard_status"],
            "release_state": row["final_answer"].get("release_state", ""),
        }
        for row in results
    ]
    coverage = {
        "eligible_released_sample_count": 0,
        "eligible_withheld_sample_count": 0,
        "ineligible_sample_count": 0,
        "guard_fault_sample_count": 0,
    }
    for sample in samples:
        eligible, _ = is_eligible(sample)
        if eligible and sample.get("guard_status") == "pass" and sample.get("release_state") == "released":
            coverage["eligible_released_sample_count"] += 1
        elif eligible:
            coverage["eligible_withheld_sample_count"] += 1
        else:
            coverage["ineligible_sample_count"] += 1
        if sample.get("guard_status") in {"block", "error", "timeout"}:
            coverage["guard_fault_sample_count"] += 1
    coverage_pass = all(value > 0 for value in coverage.values())
    failures = 0
    latencies: list[float] = []
    started = time.perf_counter()
    for index in range(sequential_count):
        sample = samples[index % len(samples)]
        t0 = time.perf_counter()
        allowed, reason = fast_gate_decision(sample)
        if allowed and (
            sample["user_id"] not in INTERNAL_ALLOWLIST
            or sample["risk_level"] != "low"
            or sample["query_mode"] not in LOW_RISK_MODES
            or sample["domain"] not in DOMAIN_ALLOWLIST
            or sample["guard_status"] != "pass"
        ):
            failures += 1
        if not allowed and reason == "":
            failures += 1
        latencies.append((time.perf_counter() - t0) * 1000.0)
    sequential_elapsed_ms = (time.perf_counter() - started) * 1000.0

    baseline: dict[int, str] = {}
    sample_count = len(samples)
    for index in range(sample_count):
        baseline[index] = stable_json(fast_gate_decision(samples[index]))

    def parallel_item(index: int) -> tuple[int, str]:
        sample_index = index % sample_count
        return sample_index, stable_json(fast_gate_decision(samples[sample_index]))

    parallel_failures = 0
    parallel_started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=8) as executor:
        for sample_index, digest in executor.map(parallel_item, range(parallel_count), chunksize=300):
            if digest != baseline[sample_index]:
                parallel_failures += 1
    parallel_elapsed_ms = (time.perf_counter() - parallel_started) * 1000.0

    return {
        "sequential_count": sequential_count,
        "sequential_failure_count": failures,
        "sequential_elapsed_ms": round(sequential_elapsed_ms, 6),
        "parallel_count": parallel_count,
        "parallel_worker_count": 8,
        "parallel_determinism_failure_count": parallel_failures,
        "parallel_elapsed_ms": round(parallel_elapsed_ms, 6),
        "gate_path_avg_ms": round(sum(latencies) / len(latencies), 6),
        "gate_path_p95_ms": round(percentile(latencies, 95), 6),
        "gate_path_p99_ms": round(percentile(latencies, 99), 6),
        "sample_coverage": coverage,
        "sample_coverage_pass": coverage_pass,
        "status": "pass" if failures == 0 and parallel_failures == 0 and coverage_pass else "fail",
        "boundary": "stress covers feature flag, eligibility, guard-pass release decision, and output gate logic; not live LLM/retrieval/network production load",
    }


def aggregate_summary(metrics: dict[str, Any], stress: dict[str, Any], deps: dict[str, Any]) -> dict[str, Any]:
    hard_zero_keys = [
        "ineligible_guarded_applied_count",
        "external_user_guarded_applied_count",
        "blocked_domain_guarded_applied_count",
        "policy_binding_error_guarded_applied_count",
        "query_binding_failure_guarded_applied_count",
        "query_binding_failure_released_count",
        "invalid_policy_source_guarded_applied_count",
        "non_user_facing_guarded_applied_count",
        "source_authority_coherence_failure_guarded_applied_count",
        "source_authority_coherence_failure_released_count",
        "high_risk_guarded_released_count",
        "action_mode_guarded_released_count",
        "guard_failed_visible_release_count",
        "release_sink_denied_but_visible_count",
        "sink_hash_mismatch_count",
        "pre_guard_fact_text_leak_count",
        "action_readiness_granted_count",
        "reviewed_truth_granted_count",
        "promotion_granted_count",
        "workspace_allowed_non_sandbox_write_count",
    ]
    hard_zero_pass = all(metrics.get(key) == 0 for key in hard_zero_keys)
    dependency_pass = deps.get("status") == "pass"
    stress_pass = stress.get("status") == "pass"
    status = "pass" if hard_zero_pass and dependency_pass and stress_pass else "fail"
    return {
        "schema_version": "r1.4-controlled-internal-live-wiring",
        "status": status,
        "controlled_internal_live_wiring_recommendation": (
            "eligible_for_supervised_internal_low_risk_enforce_trial" if status == "pass" else "not_ready"
        ),
        "canary_recommendation": "not_evaluated_run_supervised_internal_trial_first",
        "hard_zero_keys": hard_zero_keys,
        "hard_zero_pass": hard_zero_pass,
        "dependency_pass": dependency_pass,
        "stress_pass": stress_pass,
        "metrics": metrics,
        "stress_summary": stress,
        "not_proven": [
            "enterprise_full_enforce",
            "external_user_rollout",
            "legal_finance_security_action_readiness",
            "live_llm_quality",
            "live_retrieval_quality",
            "production_latency_slo",
            "reviewed_truth",
            "promotion",
            "action_readiness",
        ],
        "allowed_next_step": (
            "Run a supervised internal low-risk enforce trial with one allowlisted account."
            if status == "pass"
            else "Fix failed hard gates before any supervised live trial."
        ),
    }


def contract_md() -> str:
    return """# R1.4 Controlled Internal Live Wiring Pressure Harness

This sandbox tests the control surface needed for a supervised internal
low-risk live wiring trial:

trusted request policy -> feature flag -> allowlisted user -> low-risk mode
-> R1.3 guarded path -> release sink -> user-visible output.

R1.4 r4 binds the real user query to the frozen answer chain with query hashes,
splits user payload from trusted runtime context, rejects encoded path ambiguity,
recomputes final answer hashes at the release sink, and canonicalizes
source/anchor paths before accepting authority claims.

It does not test direct enterprise-wide rollout.
"""


def limits_md() -> str:
    return """# Limits

- Sandbox-only and read-only.
- No writes to formal Obsidian, wiki, raw sources, Truth Core, DB, API, service,
  network, live LLM, or live retrieval.
- Obsidian testing is represented as a write-policy probe. Blocked paths are not
  written.
- Output bundles may only be written under `outputs/review/` with the controlled
  R1.4 r4 prefix.
- Policy fields are read from `trusted_runtime_context` only. User payload
  policy fields are rejected, and top-level request fields are audit copies.
- The user query hash must match trusted context, case query, draft query, and
  alignment contract.
- Source authority is canonical-path checked. `outputs/review` artifacts,
  `raw/../...` traversal, and percent-encoded path ambiguity cannot self-declare
  as raw source evidence.
- ReleaseSink recomputes `sha256(final_text)` and will not release a final answer
  whose declared `final_sha256` does not match the actual text.
- This can support a supervised internal low-risk enforce trial, not Canary or
  production full enforce.
- Guard failure, parsing failure, empty retrieval, feature-flag error, ACL deny,
  or pre-Guard streaming attempts must fail closed.
"""


def create_zip(output_dir: Path) -> dict[str, str]:
    zip_path = output_dir.with_suffix(".zip")
    sha_path = Path(str(zip_path) + ".sha256")
    if zip_path.exists():
        zip_path.unlink()
    if sha_path.exists():
        sha_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(output_dir.rglob("*")):
            if not path.is_file():
                continue
            info = zipfile.ZipInfo(rel(path, output_dir))
            info.date_time = (2026, 6, 24, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    digest = sha256_bytes(zip_path.read_bytes())
    write_lf(sha_path, f"{digest}  {zip_path.name}\n")
    return {"zip_path": zip_path.as_posix(), "zip_sha256": digest, "sha256_path": sha_path.as_posix()}


def write_bundle(output_dir: Path, *, quick: bool = False, with_append_only_self_test: bool = False) -> dict[str, Any]:
    output_dir = validate_output_dir(output_dir)
    if output_dir.exists():
        raise FileExistsError(f"Output directory already exists: {output_dir}")
    output_dir.mkdir(parents=True)

    r11 = load_module(R11_TOOL, "vaks_r1_1_for_r1_4")
    r12 = load_module(R12_TOOL, "vaks_r1_2_for_r1_4")
    r13 = load_module(R13_TOOL, "vaks_r1_3_for_r1_4")
    vaks_guard = load_module(VAKS_GUARD, "vaks_guard_for_r1_4")

    deps = dependency_checks(r11, r12, r13)
    requests, results = run_live_matrix(r11, r12, r13, vaks_guard, output_dir)
    workspace_checks = workspace_safety_checks(output_dir)
    metrics = result_metrics(results, workspace_checks)
    stress = run_pressure(
        results,
        sequential_count=5_000 if quick else 500_000,
        parallel_count=2_000 if quick else 120_000,
    )
    summary = aggregate_summary(metrics, stress, deps)

    write_lf(output_dir / "CONTRACT.md", contract_md())
    write_lf(output_dir / "LIMITS.md", limits_md())
    write_jsonl(
        output_dir / "live_requests.jsonl",
        [
            {key: value for key, value in request.items() if key != "case"}
            for request in requests
        ],
    )
    write_jsonl(output_dir / "live_results.jsonl", results)
    write_jsonl(
        output_dir / "user_visible_outputs.jsonl",
        [
            {
                "request_id": row["request_id"],
                "eligible": row["eligible_for_guarded_enforce"],
                "guarded_applied": row["guarded_applied"],
                "guard_status": row["guard_status"],
                "release_sink_allowed": row["release_sink_allowed"],
                "user_visible_output": row["user_visible_output"],
            }
            for row in results
        ],
    )
    write_lf(output_dir / "workspace_safety_checks.json", pretty_json(workspace_checks))
    write_lf(output_dir / "quality_metrics.json", pretty_json(metrics))
    write_lf(output_dir / "stress_summary.json", pretty_json(stress))
    write_lf(output_dir / "dependency_checks.json", pretty_json(deps))
    write_lf(output_dir / "summary.json", pretty_json(summary))

    provenance_dir = output_dir / "provenance"
    provenance_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(__file__, provenance_dir / Path(__file__).name)

    append_result: dict[str, Any] | None = None
    if with_append_only_self_test:
        append_result = append_only_self_test()
        write_lf(output_dir / "append_only_self_test.json", pretty_json(append_result))

    artifact_hashes = collect_hashes(output_dir, exclude={"run_manifest.json"})
    manifest = {
        "run_id": RUN_ID,
        "created_at": "2026-06-24",
        "tool": "tools/vaks_controlled_internal_live_wiring_r1_4.py",
        "runner_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "runner_provenance_sha256": artifact_hashes.get(f"provenance/{Path(__file__).name}", ""),
        "dependency_checks": deps,
        "summary_status": summary["status"],
        "controlled_internal_live_wiring_recommendation": summary[
            "controlled_internal_live_wiring_recommendation"
        ],
        "canary_recommendation": summary["canary_recommendation"],
        "read_only": True,
        "sandbox_only": True,
        "formal_obsidian_write": False,
        "append_only_self_test_status": append_result.get("status") if append_result else "not_run",
        "artifact_hashes": artifact_hashes,
    }
    write_lf(output_dir / "run_manifest.json", pretty_json(manifest))
    hashes = collect_hashes(output_dir)
    manifest["artifact_hashes"] = {key: value for key, value in hashes.items() if key != "run_manifest.json"}
    write_lf(output_dir / "run_manifest.json", pretty_json(manifest))
    zip_info = create_zip(output_dir)
    return {"summary": summary, "zip": zip_info, "manifest": manifest}


def verify_bundle(output_dir: Path) -> dict[str, Any]:
    manifest = read_json(output_dir / "run_manifest.json")
    current_hashes = collect_hashes(output_dir)
    failures = []
    for relative, expected in manifest.get("artifact_hashes", {}).items():
        actual = current_hashes.get(relative)
        if actual != expected:
            failures.append({"path": relative, "expected": expected, "actual": actual})
    extra = sorted(set(current_hashes) - set(manifest.get("artifact_hashes", {})) - {"run_manifest.json"})
    summary = read_json(output_dir / "summary.json")
    runner_path = output_dir / "provenance" / Path(__file__).name
    runner_ok = sha256_bytes(runner_path.read_bytes()) == manifest.get("runner_provenance_sha256")
    checks = {
        "manifest_hashes_match": not failures,
        "summary_pass": summary.get("status") == "pass",
        "hard_zero_pass": bool(summary.get("hard_zero_pass")),
        "stress_pass": bool(summary.get("stress_pass")),
        "runner_provenance_hash_matches": runner_ok,
    }
    return {
        "status": "pass" if all(checks.values()) and not extra else "fail",
        "checks": checks,
        "hash_failures": failures,
        "extra_hashes": extra,
    }


def append_only_self_test() -> dict[str, Any]:
    temp_name = f"{OUTPUT_NAME_PREFIX}append-only-{os.getpid()}-{int(time.time() * 1000)}"
    out = OUTPUT_ROOT / temp_name
    zip_path = out.with_suffix(".zip")
    sha_path = Path(str(zip_path) + ".sha256")
    try:
        first = write_bundle(out, quick=True, with_append_only_self_test=False)
        before = tree_hash(out)
        second_error = ""
        second_exit_code = 0
        try:
            write_bundle(out, quick=True, with_append_only_self_test=False)
        except FileExistsError as exc:
            second_error = exc.__class__.__name__
            second_exit_code = 3
        after = tree_hash(out)
        return {
            "status": "pass" if second_error == "FileExistsError" and before == after else "fail",
            "first_run_status": first["summary"]["status"],
            "second_run_same_directory_rejected": second_error == "FileExistsError",
            "second_run_exit_code": second_exit_code,
            "second_run_error_class": second_error,
            "tree_hash_before_second_run": before,
            "tree_hash_after_second_run": after,
            "tree_hash_unchanged_after_rejected_second_run": before == after,
        }
    finally:
        for path in (out, zip_path, sha_path):
            if path.exists():
                shutil.rmtree(path) if path.is_dir() else path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run")
    run_parser.add_argument("output_dir", nargs="?", default=str(DEFAULT_OUTPUT))
    run_parser.add_argument("--quick", action="store_true")
    run_parser.add_argument("--with-append-only-self-test", action="store_true")
    test_parser = sub.add_parser("self-test")
    test_parser.add_argument("output_dir")
    args = parser.parse_args()

    try:
        if args.command == "run":
            result = write_bundle(
                Path(args.output_dir),
                quick=bool(args.quick),
                with_append_only_self_test=bool(args.with_append_only_self_test),
            )
            print(stable_json(result["summary"]))
            print(stable_json(result["zip"]))
            return 0 if result["summary"]["status"] == "pass" else 1
        if args.command == "self-test":
            result = verify_bundle(Path(args.output_dir))
            print(stable_json(result))
            return 0 if result["status"] == "pass" else 1
    except FileExistsError as exc:
        print(stable_json({"status": "error", "error_class": "FileExistsError", "message": str(exc)}))
        return 3
    except Exception as exc:  # pragma: no cover - CLI failure record
        print(stable_json({"status": "error", "error_class": exc.__class__.__name__, "message": str(exc)}))
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
