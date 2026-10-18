"""R1.5 supervised internal trial adapter preflight for VAKS guarded answers.

This sandbox tests the layer above the R1.4 gate: server-built request
envelopes, feature-flag off behavior, answer relevance gating, pre-Guard output
blocking, fallback safety, log redaction, and local latency.

It is offline, deterministic, and sandbox-only. It does not call a network, DB,
API, service, LLM, live retrieval system, Obsidian, wiki, raw source writer, or
Truth Core.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hmac
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import sys
import threading
import time
import unicodedata
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_ID = "vaks-supervised-trial-adapter-preflight-r1-5-r47-2026-06-25"
OUTPUT_ROOT = ROOT / "outputs" / "review"
DEFAULT_OUTPUT = OUTPUT_ROOT / RUN_ID
OUTPUT_NAME_PREFIX = "vaks-supervised-trial-adapter-preflight-r1-5-r47-"
VALID_OUTPUT_NAME_RE = re.compile(
    r"^vaks-supervised-trial-adapter-preflight-r1-5-r47-(quick-)?\d{4}-\d{2}-\d{2}$"
    r"|^vaks-supervised-trial-adapter-preflight-r1-5-r47-append-only-\d+-\d+$"
    r"|^vaks-supervised-trial-adapter-preflight-r1-5-r47-tamper-\d+-\d+-[a-z-]+$"
    r"|^vaks-supervised-trial-adapter-preflight-r1-5-r47-repeat-\d+-\d+-[ab]$"
)

R14_TOOL = ROOT / "tools" / "vaks_controlled_internal_live_wiring_r1_4.py"
SENSITIVE_TOKEN_PARTS = [
    ("SECRET", "-", "CUSTOMER", "-", "ALICE"),
    ("DANGEROUS", " OLD", " ANSWER"),
    ("立即导出", "客户", "名单"),
    ("客户", "名单"),
]
SENSITIVE_TOKENS = ["".join(parts) for parts in SENSITIVE_TOKEN_PARTS]
SENSITIVE_REDACTIONS = {
    token: f"[REDACTED:SENSITIVE_TOKEN_{index:03d}]"
    for index, token in enumerate(SENSITIVE_TOKENS, start=1)
}
UNKNOWN_SENSITIVE_PROBE_PARTS = [
    ("PRIVATE", "-", "ACME", "-", "PAYROLL", "-", "999"),
    ("PRIVATE", "-", "董事会", "-", "MERGER", "-", "777"),
]
UNKNOWN_SENSITIVE_PROBES = ["".join(parts) for parts in UNKNOWN_SENSITIVE_PROBE_PARTS]
RAW_PAYLOAD_SHA_FIELD = "raw_payload_" + "sha256_stored"
RAW_KEY_REPR_FIELD = "key_" + "repr"
NON_JSON_OBJECT_MARKER = "__non_json_" + "object__"
FALLBACK_REASON_CODES = {
    "adapter_rejected",
    "feature_flag_error",
    "feature_flag_off",
    "answer_relevance_failed",
    "adapter_release_sink_denied",
}
FALLBACK_RISK_CLASSES = {"low", "medium", "high", "action", "review"}
FINAL_RELEASE_STATES = {"released", "withheld", "review_required", "released_degraded"}
FINAL_ANSWER_POLICIES = {"direct", "qualified", "abstain", "review", "pending_evidence"}
FINAL_ATOMIC_PHASES = {"candidate_final", "pending_guard", "committed_final"}
FINAL_ANSWER_ALLOWED_KEYS = {
    "action_readiness_granted",
    "answer_policy",
    "atomic_release_phase",
    "case_id",
    "citations",
    "evaluation_state",
    "final_answer_id",
    "final_sha256",
    "final_text",
    "promotion_granted",
    "release_state",
    "reviewed_truth_granted",
    "status_label",
    "visible_claim_ids",
}
VISIBLE_OUTPUT_ALLOWED_KEYS = {"text", "sha256"}
EXTRA_FINAL_TRACE_FIELDS = {"debug_" + "raw_text", "raw_" + "candidate_body"}
ADAPTER_POLICY_KEYS = {
    "trusted_context_origin",
    "iam_subject_verified",
    "feature_flag_resolved_by",
}
USER_PAYLOAD_ALLOWED_KEYS = {"query", "query_sha256", "client_request_id"}
SERVER_CONTEXT_ALLOWED_KEYS = {
    "action_requested",
    "case_class",
    "domain",
    "feature_flag_resolved_by",
    "flag_source",
    "guarded_answer_mode",
    "iam_subject_verified",
    "principal_id",
    "query",
    "query_mode",
    "query_sha256",
    "risk_level",
    "supplied_by",
    "tenant_id",
    "trusted_context_origin",
}
FEATURE_FLAG_MODES = {"off", "enforce"}
LOG_HMAC_KEY_ID = "r1_5_sandbox_log_key_v1"
LOG_HMAC_KEY = b"r1.5 sandbox log hmac key; production must use secret key material"
TRIAL_PRINCIPAL_ALLOWLIST = {"internal-alpha"}
TRIAL_TENANT_ALLOWLIST = {"tenant-internal"}
TRIAL_QUERY_MODES = {"orientation", "source_inspection"}
TRIAL_RISK_LEVELS = {"low"}
TRIAL_DOMAINS = {"general", "source_lookup"}
TRIAL_CASE_CLASSES = {"user_facing"}
TRIAL_SUPPLIED_BY = {"trusted_runtime"}
TRIAL_FLAG_SOURCES = {"trusted_feature_flag_service"}
MAX_QUERY_CHARS = 2000
MAX_ID_CHARS = 128
JSON_SAFE_MAX_DEPTH = 32
JSON_SAFE_MAX_NODES = 5000
JSON_SAFE_MAX_ITEMS = 200
JSON_SAFE_MAX_STRING_CHARS = 4096


class NonJsonProbeObject:
    pass


class SensitiveReprProbeObject:
    def __repr__(self) -> str:
        return f"{SENSITIVE_TOKENS[1]}:{SENSITIVE_TOKENS[2]}"


class ExplodingReprProbeObject:
    def __repr__(self) -> str:
        raise RuntimeError("repr unavailable")


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def pretty_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def redact_sensitive_text(text: str) -> str:
    redacted = text
    for token in sorted(SENSITIVE_REDACTIONS, key=len, reverse=True):
        redacted = redacted.replace(token, SENSITIVE_REDACTIONS[token])
    return redacted


def bytes_payload_sensitive_hint(data: bytes) -> bool:
    decodings = ("utf-8", "utf-16", "utf-16le", "utf-16be")
    for encoding in decodings:
        try:
            text = data.decode(encoding)
        except UnicodeDecodeError:
            continue
        if redact_sensitive_text(text) != text:
            return True
    return False


def redacted_bytes_fingerprint(data: bytes, kind: str) -> dict[str, Any]:
    sensitive_hint = bytes_payload_sensitive_hint(data)
    structural_fingerprint = sha256_text(
        f"redacted-{kind}-payload:v1:length={len(data)}:sensitive_hint={sensitive_hint}"
    )
    return {
        "length": len(data),
        "structural_fingerprint": structural_fingerprint,
        "payload_sensitive_hint": sensitive_hint,
        RAW_PAYLOAD_SHA_FIELD: False,
    }


def audit_type_category(value: Any) -> str:
    cls = type(value)
    if cls.__module__ == "builtins":
        return cls.__name__
    return "custom_object"


def enum_audit(value: Any, allowed: set[str], *, role: str) -> dict[str, Any]:
    valid = isinstance(value, str) and value in allowed
    safe_role = role if isinstance(role, str) and role else "enum"
    return {
        "valid": valid,
        "value": value if valid else "",
        "value_type": audit_type_category(value),
        "raw_value_stored": valid,
        "structural_fingerprint": sha256_text(
            f"enum-audit:v1:role={safe_role}:valid={valid}:type={audit_type_category(value)}"
        ),
    }


def repr_audit_metadata(value: Any) -> dict[str, Any]:
    try:
        text = repr(value)
    except Exception:
        return {
            "repr_available": False,
            "repr_length": 0,
            "repr_sensitive_hint": False,
        }
    return {
        "repr_available": True,
        "repr_length": len(text),
        "repr_sensitive_hint": redact_sensitive_text(text) != text,
    }


def audit_sort_key(value: Any) -> tuple[str, str]:
    if isinstance(value, str):
        return ("str", redact_sensitive_text(value))
    if isinstance(value, (int, bool)) or value is None:
        return (audit_type_category(value), stable_json(value))
    if isinstance(value, float):
        return ("float", repr(value))
    if isinstance(value, (bytes, bytearray)):
        data = bytes(value)
        return (audit_type_category(value), stable_json(redacted_bytes_fingerprint(data, audit_type_category(value))))
    return (audit_type_category(value), stable_json(repr_audit_metadata(value)))


def json_safe_limit(kind: str, **metadata: Any) -> dict[str, Any]:
    return {
        "__json_safe_resource_limit__": {
            "kind": kind,
            **metadata,
        }
    }


def truncate_safe_string(text: str) -> str | dict[str, Any]:
    redacted = redact_sensitive_text(text)
    if len(redacted) <= JSON_SAFE_MAX_STRING_CHARS:
        return redacted
    structural_fingerprint = sha256_text(f"truncated-string:v1:length={len(redacted)}")
    return {
        "__json_safe_truncated_string__": {
            "length": len(redacted),
            "structural_fingerprint": structural_fingerprint,
            "truncated": True,
        }
    }


def unreleased_text_audit(text: Any, role: str) -> dict[str, Any]:
    text_valid = isinstance(text, str)
    safe_role = role if isinstance(role, str) and role else "unknown"
    if not text_valid:
        return {
            "text_valid": False,
            "text_type": audit_type_category(text),
            "text_length": 0,
            "text_sensitive_hint": False,
            "structural_fingerprint": sha256_text(
                f"unreleased-text:v1:role={safe_role}:valid=false:type={audit_type_category(text)}"
            ),
            "raw_text_sha256_stored": False,
        }
    redacted = redact_sensitive_text(text)
    sensitive_hint = redacted != text
    return {
        "text_valid": True,
        "text_type": "str",
        "text_length": len(text),
        "text_sensitive_hint": sensitive_hint,
        "structural_fingerprint": sha256_text(
            f"unreleased-text:v1:role={safe_role}:length={len(text)}:sensitive_hint={sensitive_hint}"
        ),
        "raw_text_sha256_stored": False,
    }


def sanitize_unreleased_final(final: Any) -> Any:
    if not isinstance(final, dict):
        return {
            "__unreleased_final_sanitized__": {
                "final_valid": False,
                "final_type": audit_type_category(final),
            }
        }
    keys = list(final.keys())
    non_string_key_count = sum(1 for key in keys if not isinstance(key, str))
    extra_key_count = sum(1 for key in keys if isinstance(key, str) and key not in FINAL_ANSWER_ALLOWED_KEYS)
    visible_claim_ids = final.get("visible_claim_ids", [])
    visible_claim_count = len(visible_claim_ids) if isinstance(visible_claim_ids, list) else 0
    return {
        "__unreleased_final_sanitized__": {
            "final_valid": True,
            "key_count": len(keys),
            "non_string_key_count": non_string_key_count,
            "extra_key_count": extra_key_count,
            "release_state": enum_audit(final.get("release_state", ""), FINAL_RELEASE_STATES, role="release_state"),
            "answer_policy": enum_audit(final.get("answer_policy", ""), FINAL_ANSWER_POLICIES, role="answer_policy"),
            "atomic_release_phase": enum_audit(
                final.get("atomic_release_phase", ""),
                FINAL_ATOMIC_PHASES,
                role="atomic_release_phase",
            ),
            "visible_claim_count": visible_claim_count,
            "final_text_audit": unreleased_text_audit(final.get("final_text", ""), "final-trace"),
            "final_text_stored": False,
            "final_sha256_stored": False,
        }
    }


def sanitize_unreleased_visible_output(output: Any) -> Any:
    if not isinstance(output, dict):
        return {
            "__unreleased_visible_output_sanitized__": {
                "output_valid": False,
                "output_type": audit_type_category(output),
            }
        }
    keys = list(output.keys())
    non_string_key_count = sum(1 for key in keys if not isinstance(key, str))
    extra_key_count = sum(1 for key in keys if isinstance(key, str) and key not in VISIBLE_OUTPUT_ALLOWED_KEYS)
    return {
        "__unreleased_visible_output_sanitized__": {
            "output_valid": True,
            "key_count": len(keys),
            "non_string_key_count": non_string_key_count,
            "extra_key_count": extra_key_count,
            "text_audit": unreleased_text_audit(output.get("text", ""), "visible-output-trace"),
            "text_stored": False,
            "sha256_stored": False,
        }
    }


def json_safe(
    value: Any,
    *,
    _depth: int = 0,
    _seen: set[int] | None = None,
    _budget: dict[str, int] | None = None,
) -> Any:
    if _seen is None:
        _seen = set()
    if _budget is None:
        _budget = {"nodes": 0}
    _budget["nodes"] += 1
    if _budget["nodes"] > JSON_SAFE_MAX_NODES:
        return json_safe_limit("node_limit", max_nodes=JSON_SAFE_MAX_NODES)
    if _depth > JSON_SAFE_MAX_DEPTH:
        return json_safe_limit("depth_limit", max_depth=JSON_SAFE_MAX_DEPTH)
    if isinstance(value, str):
        return truncate_safe_string(value)
    if isinstance(value, (int, bool)) or value is None:
        return value
    if isinstance(value, bytes):
        return {
            "__non_json_bytes__": redacted_bytes_fingerprint(value, "bytes")
        }
    if isinstance(value, bytearray):
        data = bytes(value)
        return {
            "__non_json_bytearray__": redacted_bytes_fingerprint(data, "bytearray")
        }
    if isinstance(value, float):
        if not math.isfinite(value):
            return {"__non_json_float__": repr(value)}
        return value
    if isinstance(value, dict):
        value_id = id(value)
        if value_id in _seen:
            return json_safe_limit("cycle", container_type="dict")
        _seen.add(value_id)
        converted_keys: list[str] = []
        has_non_string_key = False
        items = list(value.items())
        for key, _item in items[:JSON_SAFE_MAX_ITEMS]:
            if isinstance(key, str):
                converted_keys.append(redact_sensitive_text(key))
            else:
                has_non_string_key = True
                converted_keys.append(stable_json({
                    "key_category": audit_type_category(key),
                    "repr": repr_audit_metadata(key),
                }))
        item_limit = len(items) > JSON_SAFE_MAX_ITEMS
        if has_non_string_key or len(set(converted_keys)) != len(converted_keys):
            entries = [
                    {
                        "key_type_category": audit_type_category(key),
                        "key_repr_audit": repr_audit_metadata(key),
                    "value": json_safe(item, _depth=_depth + 1, _seen=_seen, _budget=_budget),
                    }
                for key, item in sorted(items[:JSON_SAFE_MAX_ITEMS], key=lambda pair: audit_sort_key(pair[0]))
            ]
            if item_limit:
                entries.append(json_safe_limit("item_limit", container_type="dict", item_count=len(items), emitted_count=JSON_SAFE_MAX_ITEMS))
            _seen.remove(value_id)
            return {
                "__json_safe_object_entries__": entries
            }
        safe: dict[str, Any] = {}
        for key, item in items[:JSON_SAFE_MAX_ITEMS]:
            safe[redact_sensitive_text(key)] = json_safe(item, _depth=_depth + 1, _seen=_seen, _budget=_budget)
        if item_limit:
            safe["__json_safe_resource_limit__"] = {
                "kind": "item_limit",
                "container_type": "dict",
                "item_count": len(items),
                "emitted_count": JSON_SAFE_MAX_ITEMS,
            }
        _seen.remove(value_id)
        return safe
    if isinstance(value, (list, tuple)):
        value_id = id(value)
        if value_id in _seen:
            return json_safe_limit("cycle", container_type=audit_type_category(value))
        _seen.add(value_id)
        items = list(value)
        safe_items = [
            json_safe(item, _depth=_depth + 1, _seen=_seen, _budget=_budget)
            for item in items[:JSON_SAFE_MAX_ITEMS]
        ]
        if len(items) > JSON_SAFE_MAX_ITEMS:
            safe_items.append(json_safe_limit(
                "item_limit",
                container_type=audit_type_category(value),
                item_count=len(items),
                emitted_count=JSON_SAFE_MAX_ITEMS,
            ))
        _seen.remove(value_id)
        return safe_items
    if isinstance(value, (set, frozenset)):
        value_id = id(value)
        if value_id in _seen:
            return json_safe_limit("cycle", container_type=audit_type_category(value))
        _seen.add(value_id)
        items = sorted(value, key=audit_sort_key)
        safe_items = [
            json_safe(item, _depth=_depth + 1, _seen=_seen, _budget=_budget)
            for item in items[:JSON_SAFE_MAX_ITEMS]
        ]
        if len(items) > JSON_SAFE_MAX_ITEMS:
            safe_items.append(json_safe_limit(
                "item_limit",
                container_type=audit_type_category(value),
                item_count=len(items),
                emitted_count=JSON_SAFE_MAX_ITEMS,
            ))
        _seen.remove(value_id)
        return {
            "__non_json_set_entries__": safe_items
        }
    return {"__non_json_object__": {"type_category": audit_type_category(value), "repr_audit": repr_audit_metadata(value)}}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def hmac_text(text: str) -> str:
    return hmac.new(LOG_HMAC_KEY, text.encode("utf-8"), hashlib.sha256).hexdigest()


def safe_text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def safe_sha256_text(value: Any) -> str:
    return sha256_text(safe_text(value))


def safe_hmac_text(value: Any) -> str:
    return hmac_text(safe_text(value))


def is_sha256_hex(value: str) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[0-9a-f]{64}", value))


def has_forbidden_text_char(value: str) -> bool:
    return any(unicodedata.category(char) in {"Cc", "Cf", "Cs"} for char in value)


def validate_text_field(
    value: Any,
    field: str,
    *,
    max_chars: int,
    nonempty: bool = True,
) -> list[str]:
    if not isinstance(value, str):
        return [f"{field}_not_string"]
    errors: list[str] = []
    if nonempty and not value:
        errors.append(f"{field}_empty")
    if len(value) > max_chars:
        errors.append(f"{field}_too_long")
    if value != value.strip():
        errors.append(f"{field}_has_outer_whitespace")
    if has_forbidden_text_char(value):
        errors.append(f"{field}_has_forbidden_character")
    return errors


def require_value(field: str, value: Any, allowed: set[str]) -> list[str]:
    if not isinstance(value, str):
        return []
    return [] if value in allowed else [f"{field}_not_allowed"]


def normalize_fallback_reason(reason_code: Any) -> str:
    if isinstance(reason_code, str) and reason_code in FALLBACK_REASON_CODES:
        return reason_code
    return "adapter_release_sink_denied"


def normalize_fallback_risk(risk_class: Any) -> str:
    if isinstance(risk_class, str) and risk_class in FALLBACK_RISK_CLASSES:
        return risk_class
    return "high"


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def exists_or_symlink(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def validate_output_dir(output_dir: Path) -> Path:
    resolved = output_dir.resolve()
    output_root = OUTPUT_ROOT.resolve()
    if not is_relative_to(resolved, output_root):
        raise ValueError(f"Output directory must be under {OUTPUT_ROOT.as_posix()}: {output_dir}")
    if any(ord(char) < 32 for char in resolved.name):
        raise ValueError("Output directory name must not contain control characters")
    if not VALID_OUTPUT_NAME_RE.fullmatch(resolved.name):
        raise ValueError(f"Output directory name is not an allowed R1.5 bundle name: {resolved.name}")
    return resolved


def write_lf(path: Path, text: str) -> None:
    write_bytes_no_clobber(path, text.encode("utf-8"))


def write_bytes_no_clobber(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if exists_or_symlink(path):
        raise FileExistsError(f"Output artifact already exists: {path}")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
    except Exception:
        try:
            path.unlink()
        except OSError:
            pass
        raise


def mkdir_no_symlink(path: Path) -> None:
    if exists_or_symlink(path):
        raise FileExistsError(f"Output directory already exists: {path}")
    path.mkdir(parents=True, exist_ok=False)


def copy_file_no_clobber(source: Path, destination: Path) -> None:
    write_bytes_no_clobber(destination, source.read_bytes())


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    write_lf(path, "".join(stable_json(json_safe(row)) + "\n" for row in rows))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def collect_hashes(root: Path, *, exclude: set[str] | None = None) -> dict[str, str]:
    exclude = exclude or set()
    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlink artifact is not allowed in review bundle: {path}")
        if not path.is_file():
            continue
        relative = rel(path, root)
        if relative in exclude:
            continue
        hashes[relative] = sha256_bytes(path.read_bytes())
    return hashes


def tree_hash(root: Path) -> str:
    return sha256_text(stable_json(collect_hashes(root)))


def zip_entry_name_is_safe(name: str) -> bool:
    if not isinstance(name, str) or not name:
        return False
    if "\\" in name or name.startswith("/") or name.startswith("//"):
        return False
    if re.match(r"^[A-Za-z]:", name):
        return False
    if any(ord(char) < 32 or ord(char) == 127 for char in name):
        return False
    parts = name.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return False
    return True


def zip_sidecar_digest(zip_path: Path) -> str:
    sidecar = Path(str(zip_path) + ".sha256")
    if not sidecar.is_file():
        return ""
    text = sidecar.read_text(encoding="utf-8").strip()
    if not text:
        return ""
    digest = text.split()[0]
    return digest if is_sha256_hex(digest) else ""


def zip_sidecar_exact_format_ok(zip_path: Path, digest: str) -> bool:
    sidecar = Path(str(zip_path) + ".sha256")
    if not sidecar.is_file() or not is_sha256_hex(digest):
        return False
    return sidecar.read_text(encoding="utf-8") == f"{digest}  {zip_path.name}\n"


def load_stack() -> dict[str, Any]:
    r14 = load_module(R14_TOOL, "vaks_r1_4_for_r1_5")
    r11 = r14.load_module(r14.R11_TOOL, "vaks_r1_1_for_r1_5")
    r12 = r14.load_module(r14.R12_TOOL, "vaks_r1_2_for_r1_5")
    r13 = r14.load_module(r14.R13_TOOL, "vaks_r1_3_for_r1_5")
    guard = r14.load_module(r14.VAKS_GUARD, "vaks_guard_for_r1_5")
    return {"r14": r14, "r11": r11, "r12": r12, "r13": r13, "guard": guard}


def dependency_checks(stack: dict[str, Any]) -> dict[str, Any]:
    r14 = stack["r14"]
    r14_self_test = r14.verify_bundle(r14.ROOT / "outputs" / "review" / "vaks-controlled-internal-live-wiring-r1-4-r4-2026-06-24")
    return {
        "status": "pass" if r14_self_test.get("status") == "pass" else "fail",
        "r1_4_runner_sha256": sha256_bytes(R14_TOOL.read_bytes()),
        "r1_4_self_test_status": r14_self_test.get("status"),
        "r1_4_direct_dependency": True,
    }


ALLOWED_IMPORT_MODULES = {
    "__future__",
    "argparse",
    "ast",
    "concurrent.futures",
    "copy",
    "dataclasses",
    "hashlib",
    "hmac",
    "importlib.util",
    "json",
    "math",
    "os",
    "pathlib",
    "random",
    "re",
    "shutil",
    "sys",
    "tempfile",
    "threading",
    "time",
    "typing",
    "unicodedata",
    "urllib.parse",
    "zipfile",
}
BANNED_IMPORT_MODULES = {
    "aiohttp",
    "anthropic",
    "boto3",
    "chromadb",
    "faiss",
    "haystack",
    "http.client",
    "langchain",
    "lancedb",
    "llama_index",
    "openai",
    "pinecone",
    "psycopg2",
    "pymongo",
    "qdrant_client",
    "redis",
    "requests",
    "socket",
    "sqlalchemy",
    "sqlite3",
    "subprocess",
    "urllib.request",
    "websocket",
    "websockets",
    "weaviate",
}


def imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.append(node.module or "")
    return sorted(set(modules))


def source_static_import_audit(stack: dict[str, Any]) -> dict[str, Any]:
    r14 = stack["r14"]
    paths = [
        Path(__file__),
        R14_TOOL,
        Path(r14.R11_TOOL),
        Path(r14.R12_TOOL),
        Path(r14.R13_TOOL),
        Path(r14.VAKS_GUARD),
    ]
    files: list[dict[str, Any]] = []
    disallowed: list[dict[str, str]] = []
    banned: list[dict[str, str]] = []
    for path in sorted({item.resolve() for item in paths}):
        rel_path = rel(path, ROOT) if is_relative_to(path, ROOT) else path.as_posix()
        modules = imported_modules(path)
        file_row = {
            "path": rel_path,
            "module_count": len(modules),
            "modules": modules,
        }
        files.append(file_row)
        for module in modules:
            if module not in ALLOWED_IMPORT_MODULES:
                disallowed.append({"path": rel_path, "module": module})
            if module in BANNED_IMPORT_MODULES:
                banned.append({"path": rel_path, "module": module})
    failure_count = len(disallowed) + len(banned)
    return {
        "status": "pass" if failure_count == 0 else "fail",
        "file_count": len(files),
        "allowed_import_modules": sorted(ALLOWED_IMPORT_MODULES),
        "banned_import_modules": sorted(BANNED_IMPORT_MODULES),
        "disallowed_import_count": len(disallowed),
        "banned_import_count": len(banned),
        "failure_count": failure_count,
        "files": files,
        "disallowed_imports": disallowed,
        "banned_imports": banned,
    }


def public_case_requests(stack: dict[str, Any]) -> list[dict[str, Any]]:
    r14 = stack["r14"]
    requests = r14.build_live_requests(stack["r11"], stack["r12"], stack["r13"])
    return [
        request
        for request in requests
        if request.get("request_id", "").startswith("live-")
        and request.get("trusted_runtime_context", {}).get("risk_level") == "low"
        and request.get("trusted_runtime_context", {}).get("domain") in {"general", "source_lookup"}
    ]


def server_context_for(base_request: dict[str, Any], *, mode: str = "enforce") -> dict[str, Any]:
    trusted = copy.deepcopy(base_request["trusted_runtime_context"])
    trusted["guarded_answer_mode"] = mode
    trusted["trusted_context_origin"] = "server_adapter"
    trusted["iam_subject_verified"] = True
    trusted["feature_flag_resolved_by"] = "server_flag_resolver"
    return trusted


def sanitize_log(result: dict[str, Any]) -> dict[str, Any]:
    final = result.get("final_answer", {})
    return {
        "request_id": safe_text(result.get("request_id", "")),
        "log_key_id": LOG_HMAC_KEY_ID,
        "principal_hmac": safe_hmac_text(result.get("user_id", "")),
        "tenant_hmac": safe_hmac_text(result.get("tenant_id", "")),
        "query_hmac": safe_hmac_text(result.get("effective_policy", {}).get("query_sha256", "")),
        "policy": {
            "query_mode": safe_text(result.get("query_mode", "")),
            "risk_level": safe_text(result.get("risk_level", "")),
            "domain": safe_text(result.get("domain", "")),
            "guarded_answer_mode": safe_text(result.get("guarded_answer_mode", "")),
        },
        "eligible": result.get("eligible_for_guarded_enforce", False),
        "guarded_applied": result.get("guarded_applied", False),
        "guard_status": safe_text(result.get("guard_status", "")),
        "release_sink_allowed": result.get("release_sink_allowed", False),
        "release_state": safe_text(final.get("release_state", "")),
        "answer_policy": safe_text(final.get("answer_policy", "")),
        "final_hmac": safe_hmac_text(result.get("user_visible_output", {}).get("sha256", "")),
        "reason_codes": [safe_text(reason) for reason in list(result.get("eligibility_reasons", []))[:12]],
    }


def log_contains_sensitive(log_rows: list[dict[str, Any]]) -> bool:
    text = "\n".join(stable_json(row) for row in log_rows)
    return any(token in text for token in SENSITIVE_TOKENS)


def log_contains_unsalted_identifier_or_query_hash(
    results: list[dict[str, Any]],
    log_rows: list[dict[str, Any]],
) -> bool:
    text = "\n".join(stable_json(row) for row in log_rows)
    candidates: set[str] = set()
    for row in results:
        r1_4_result = row.get("r1_4_result", {})
        for field in ("user_id", "tenant_id"):
            value = r1_4_result.get(field)
            if isinstance(value, str) and value:
                candidates.add(sha256_text(value))
        query_sha = r1_4_result.get("effective_policy", {}).get("query_sha256")
        if isinstance(query_sha, str) and query_sha:
            candidates.add(query_sha)
    return any(candidate in text for candidate in candidates)


def log_contains_unsalted_final_hash(results: list[dict[str, Any]], log_rows: list[dict[str, Any]]) -> bool:
    text = "\n".join(stable_json(row) for row in log_rows)
    candidates: set[str] = set()
    for row in results:
        final_hash = row.get("user_visible_output", {}).get("sha256")
        if isinstance(final_hash, str) and final_hash:
            candidates.add(final_hash)
    return any(candidate in text for candidate in candidates)


class AdapterReleaseSink:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._events: list[dict[str, Any]] = []
        self._user_visible_buffer = ""
        self._sealed = False
        self._committed_final: dict[str, Any] | None = None
        self._committed_sha256 = ""

    @property
    def events(self) -> list[dict[str, Any]]:
        with self._lock:
            return copy.deepcopy(self._events)

    @property
    def user_visible_buffer(self) -> str:
        with self._lock:
            return self._user_visible_buffer

    @property
    def sealed(self) -> bool:
        with self._lock:
            return self._sealed

    @property
    def committed_final(self) -> dict[str, Any] | None:
        with self._lock:
            return copy.deepcopy(self._committed_final)

    @property
    def committed_sha256(self) -> str:
        with self._lock:
            return self._committed_sha256

    def attempt_fact_text(self, text: str, stage: str) -> dict[str, Any]:
        with self._lock:
            text_valid = isinstance(text, str)
            event = {
                "stage": stage,
                "event": "fact_text_write_attempt",
                "text_audit": unreleased_text_audit(text, "pre-guard-fact-write"),
                "text_valid": text_valid,
                "text_type": audit_type_category(text),
                "allowed": False,
                "blocked": True,
                "sink_sealed": self._sealed,
                "committed_sha256_before": self._committed_sha256,
                "buffer_sha256_after": sha256_text(self._user_visible_buffer),
            }
            self._events.append(copy.deepcopy(event))
            return copy.deepcopy(event)

    def commit_candidate(self, final: dict[str, Any], *, guard_passed: bool, relevance_passed: bool) -> dict[str, Any]:
        with self._lock:
            final_valid = isinstance(final, dict)
            source_final = final if final_valid else {}
            raw_text = source_final.get("final_text", "")
            text_valid = isinstance(raw_text, str)
            text = raw_text if text_valid else ""
            actual_hash = sha256_text(text)
            declared_hash = source_final.get("final_sha256", "")
            declared_hash_valid = is_sha256_hex(declared_hash)
            declared_hash_matches_text = declared_hash == actual_hash
            guard_passed_valid = guard_passed is True
            relevance_passed_valid = relevance_passed is True
            final_keys = list(source_final.keys()) if final_valid else []
            final_non_string_key_count = sum(1 for key in final_keys if not isinstance(key, str))
            final_extra_key_count = sum(
                1 for key in final_keys if isinstance(key, str) and key not in FINAL_ANSWER_ALLOWED_KEYS
            )
            final_key_contract_passed = (
                final_valid
                and final_non_string_key_count == 0
                and final_extra_key_count == 0
            )
            sealed_before = self._sealed
            committed_before = self._committed_sha256
            validation_allowed = (
                final_valid
                and text_valid
                and final_key_contract_passed
                and guard_passed_valid
                and relevance_passed_valid
                and source_final.get("atomic_release_phase") == "committed_final"
                and source_final.get("release_state") == "released"
                and declared_hash_valid
                and declared_hash_matches_text
            )
            allowed = (not self._sealed) and validation_allowed
            if allowed:
                self._user_visible_buffer = text
                self._sealed = True
                self._committed_final = copy.deepcopy(source_final)
                self._committed_sha256 = actual_hash
            event = {
                "stage": "adapter_release_sink",
                "event": "candidate_commit_attempt",
                "sink_sealed_before": sealed_before,
                "committed_sha256_before": committed_before,
                "guard_passed": guard_passed if isinstance(guard_passed, bool) else None,
                "guard_passed_type": audit_type_category(guard_passed),
                "guard_passed_valid": guard_passed_valid,
                "relevance_passed": relevance_passed if isinstance(relevance_passed, bool) else None,
                "relevance_passed_type": audit_type_category(relevance_passed),
                "relevance_passed_valid": relevance_passed_valid,
                "final_valid": final_valid,
                "final_type": audit_type_category(final),
                "atomic_release_phase": enum_audit(
                    source_final.get("atomic_release_phase", ""),
                    FINAL_ATOMIC_PHASES,
                    role="candidate_atomic_release_phase",
                ),
                "release_state": enum_audit(
                    source_final.get("release_state", ""),
                    FINAL_RELEASE_STATES,
                    role="candidate_release_state",
                ),
                "final_key_contract_passed": final_key_contract_passed,
                "final_non_string_key_count": final_non_string_key_count,
                "final_extra_key_count": final_extra_key_count,
                "declared_final_sha256": declared_hash if allowed else "",
                "actual_final_sha256": actual_hash if allowed else "",
                "raw_candidate_sha256_stored": allowed,
                "rejected_candidate_text_audit": {} if allowed else unreleased_text_audit(raw_text, "candidate-commit"),
                "final_text_valid": text_valid,
                "final_text_type": audit_type_category(raw_text),
                "declared_hash_valid": declared_hash_valid,
                "declared_hash_matches_text": declared_hash_matches_text,
                "validation_allowed": validation_allowed,
                "allowed": allowed,
                "blocked_reason": "sink_sealed" if sealed_before and not allowed else ("" if allowed else "validation_failed"),
                "sink_sealed_after": self._sealed,
                "buffer_sha256_after": sha256_text(self._user_visible_buffer),
            }
            self._events.append(copy.deepcopy(event))
            return copy.deepcopy(event)

    def attempt_untrusted_fallback_text(self, text: str, reason_code: str) -> dict[str, Any]:
        with self._lock:
            text_valid = isinstance(text, str)
            event = {
                "stage": "adapter_release_sink",
                "event": "untrusted_fallback_text_attempt",
                "reason_code": reason_code,
                "text_audit": unreleased_text_audit(text, "untrusted-fallback-attempt"),
                "text_valid": text_valid,
                "text_type": audit_type_category(text),
                "allowed": False,
                "blocked": True,
                "sink_sealed": self._sealed,
                "committed_sha256_before": self._committed_sha256,
                "buffer_sha256_after": sha256_text(self._user_visible_buffer),
            }
            self._events.append(copy.deepcopy(event))
            return copy.deepcopy(event)

    def commit_safe_fallback(self, reason_code: str, *, risk_class: str = "low") -> tuple[dict[str, Any], dict[str, Any]]:
        with self._lock:
            normalized_reason = normalize_fallback_reason(reason_code)
            normalized_risk = normalize_fallback_risk(risk_class)
            review = normalized_risk in {"high", "action", "review"}
            final = fallback_text(normalized_reason, review=review)
            text = final["final_text"]
            sealed_before = self._sealed
            committed_before = self._committed_sha256
            allowed = not self._sealed
            if allowed:
                self._user_visible_buffer = text
                self._sealed = True
                self._committed_final = copy.deepcopy(final)
                self._committed_sha256 = sha256_text(text)
            returned_final = copy.deepcopy(self._committed_final) if self._committed_final is not None else final
            event = {
                "stage": "adapter_release_sink",
                "event": "safe_fallback_commit",
                "sink_sealed_before": sealed_before,
                "committed_sha256_before": committed_before,
                "release_state": final.get("release_state", ""),
                "answer_policy": final.get("answer_policy", ""),
                "reason_code": normalized_reason,
                "requested_reason_code_type": audit_type_category(reason_code),
                "risk_class": normalized_risk,
                "requested_risk_class_type": audit_type_category(risk_class),
                "final_sha256": sha256_text(text),
                "allowed": allowed,
                "safe_template": True,
                "blocked_reason": "" if allowed else "sink_sealed",
                "sink_sealed_after": self._sealed,
                "buffer_sha256_after": sha256_text(self._user_visible_buffer),
            }
            self._events.append(copy.deepcopy(event))
            return copy.deepcopy(returned_final), copy.deepcopy(event)


def validate_server_context(context: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(context, dict):
        return ["server_context_not_object"]
    for key in sorted(context, key=audit_sort_key):
        if not isinstance(key, str):
            errors.append(f"server_context_key_not_string:{audit_type_category(key)}")
        elif key not in SERVER_CONTEXT_ALLOWED_KEYS:
            errors.append("server_context_unknown_field")
    required_fields = {
        "action_requested",
        "case_class",
        "domain",
        "feature_flag_resolved_by",
        "flag_source",
        "guarded_answer_mode",
        "iam_subject_verified",
        "principal_id",
        "query",
        "query_mode",
        "query_sha256",
        "risk_level",
        "supplied_by",
        "tenant_id",
        "trusted_context_origin",
    }
    for field in sorted(required_fields - set(context)):
        errors.append(f"server_context_missing_field:{field}")
    if context.get("trusted_context_origin") != "server_adapter":
        errors.append("invalid_trusted_context_origin")
    if context.get("iam_subject_verified") is not True:
        errors.append("iam_subject_not_verified")
    if context.get("feature_flag_resolved_by") != "server_flag_resolver":
        errors.append("invalid_feature_flag_resolver")
    for field in ("principal_id", "tenant_id", "query_mode", "risk_level", "domain", "guarded_answer_mode"):
        if not isinstance(context.get(field, ""), str):
            errors.append(f"server_context_field_not_string:{field}")
    for field in ("query", "query_sha256", "case_class", "flag_source", "supplied_by"):
        if field in context and not isinstance(context.get(field), str):
            errors.append(f"server_context_field_not_string:{field}")
    if "action_requested" in context and not isinstance(context.get("action_requested"), bool):
        errors.append("server_context_field_not_bool:action_requested")
    for field in (
        "principal_id",
        "tenant_id",
        "query_mode",
        "risk_level",
        "domain",
        "guarded_answer_mode",
        "case_class",
        "flag_source",
        "supplied_by",
    ):
        errors.extend(validate_text_field(
            context.get(field, ""),
            f"server_context_{field}",
            max_chars=MAX_ID_CHARS,
        ))
    errors.extend(validate_text_field(
        context.get("query", ""),
        "server_context_query",
        max_chars=MAX_QUERY_CHARS,
    ))
    query_sha = context.get("query_sha256", "")
    if isinstance(query_sha, str):
        if not is_sha256_hex(query_sha):
            errors.append("server_context_query_sha256_not_sha256")
        elif isinstance(context.get("query"), str) and query_sha != sha256_text(context["query"]):
            errors.append("server_context_query_sha256_mismatch")
    errors.extend(require_value("principal_id", context.get("principal_id"), TRIAL_PRINCIPAL_ALLOWLIST))
    errors.extend(require_value("tenant_id", context.get("tenant_id"), TRIAL_TENANT_ALLOWLIST))
    errors.extend(require_value("query_mode", context.get("query_mode"), TRIAL_QUERY_MODES))
    errors.extend(require_value("risk_level", context.get("risk_level"), TRIAL_RISK_LEVELS))
    errors.extend(require_value("domain", context.get("domain"), TRIAL_DOMAINS))
    errors.extend(require_value("guarded_answer_mode", context.get("guarded_answer_mode"), FEATURE_FLAG_MODES))
    errors.extend(require_value("case_class", context.get("case_class"), TRIAL_CASE_CLASSES))
    errors.extend(require_value("flag_source", context.get("flag_source"), TRIAL_FLAG_SOURCES))
    errors.extend(require_value("supplied_by", context.get("supplied_by"), TRIAL_SUPPLIED_BY))
    if context.get("action_requested") is True:
        errors.append("action_requested_not_allowed_for_low_risk_trial")
    return errors


def validate_flag_mode(flag_mode: Any) -> list[str]:
    if not isinstance(flag_mode, str):
        return [f"flag_mode_not_string:{audit_type_category(flag_mode)}"]
    if flag_mode not in FEATURE_FLAG_MODES:
        return ["flag_mode_invalid"]
    return []


def validate_user_payload(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["user_payload_not_object"]
    for key in sorted(payload, key=audit_sort_key):
        if not isinstance(key, str):
            errors.append(f"user_payload_key_not_string:{audit_type_category(key)}")
        elif key not in USER_PAYLOAD_ALLOWED_KEYS:
            errors.append("user_payload_unknown_field")
    if not isinstance(payload.get("query", ""), str):
        errors.append("user_payload_query_not_string")
    else:
        errors.extend(validate_text_field(payload.get("query", ""), "user_payload_query", max_chars=MAX_QUERY_CHARS))
    if "query_sha256" in payload and not isinstance(payload.get("query_sha256"), str):
        errors.append("user_payload_query_sha256_not_string")
    elif "query_sha256" in payload:
        query_sha = payload.get("query_sha256", "")
        if not is_sha256_hex(query_sha):
            errors.append("user_payload_query_sha256_not_sha256")
        elif isinstance(payload.get("query"), str) and query_sha != sha256_text(payload["query"]):
            errors.append("user_payload_query_sha256_mismatch")
    if "client_request_id" in payload and not isinstance(payload.get("client_request_id"), str):
        errors.append("user_payload_client_request_id_not_string")
    elif "client_request_id" in payload:
        errors.extend(validate_text_field(
            payload.get("client_request_id", ""),
            "user_payload_client_request_id",
            max_chars=MAX_ID_CHARS,
        ))
    return errors


def normalize_claim_id_set(value: Any) -> tuple[set[str], bool, str]:
    if not isinstance(value, list):
        return set(), False, audit_type_category(value)
    normalized: set[str] = set()
    for item in value:
        if (
            not isinstance(item, str)
            or not item.strip()
            or item != item.strip()
            or any(ord(char) < 32 or ord(char) == 127 for char in item)
            or item in normalized
        ):
            return set(), False, audit_type_category(item)
        normalized.add(item)
    return normalized, True, "list"


def evaluate_marker_groups(marker_groups: Any, text: str) -> tuple[list[bool], bool, str]:
    if not isinstance(marker_groups, list):
        return [], False, audit_type_category(marker_groups)
    results: list[bool] = []
    valid = True
    for group in marker_groups:
        if not isinstance(group, list):
            valid = False
            results.append(False)
            continue
        normalized = [marker.lower() for marker in group if isinstance(marker, str) and len(marker) >= 3]
        if not normalized:
            valid = False
        results.append(bool(normalized) and any(marker in text for marker in normalized))
    return results, valid, "list"


def answer_relevance_evaluation(
    result: dict[str, Any],
    trial_case: dict[str, Any],
    candidate_final: dict[str, Any],
) -> dict[str, Any]:
    candidate_final_valid = isinstance(candidate_final, dict)
    if not candidate_final_valid:
        return {
            "passed": False,
            "skipped": False,
            "reason": "candidate_final_not_object",
            "alignment_id_match": False,
            "claim_ids_match": False,
            "claim_set_contract": "visible_claim_ids_exactly_equal_expected_claim_ids",
            "marker_groups_match": False,
            "candidate_hash_matches_text": False,
            "candidate_text_valid": False,
            "candidate_text_type": audit_type_category(candidate_final),
            "candidate_final_valid": False,
            "r1_4_user_visible_matches_candidate": False,
            "expected_claim_ids_valid": False,
            "visible_claim_ids_valid": False,
            "marker_groups_valid": False,
        }
    if candidate_final.get("release_state") != "released":
        return {
            "passed": True,
            "skipped": True,
            "reason": "not_released_candidate",
            "alignment_id_match": True,
            "claim_ids_match": True,
            "claim_set_contract": "visible_claim_ids_exactly_equal_expected_claim_ids",
            "marker_groups_match": True,
            "candidate_hash_matches_text": True,
            "candidate_text_valid": True,
            "candidate_text_type": "str",
            "candidate_final_valid": True,
            "r1_4_user_visible_matches_candidate": True,
            "expected_claim_ids_valid": True,
            "visible_claim_ids_valid": True,
            "marker_groups_valid": True,
        }
    raw_candidate_text = candidate_final.get("final_text", "")
    candidate_text_valid = isinstance(raw_candidate_text, str)
    candidate_text = raw_candidate_text if candidate_text_valid else ""
    candidate_declared_hash = candidate_final.get("final_sha256", "")
    candidate_actual_hash = sha256_text(candidate_text)
    candidate_hash_matches_text = (
        is_sha256_hex(candidate_declared_hash)
        and candidate_declared_hash == candidate_actual_hash
    )
    r1_4_visible = result.get("user_visible_output", {})
    r1_4_user_visible_matches_candidate = (
        r1_4_visible.get("text", "") == candidate_text
        and r1_4_visible.get("sha256", "") == candidate_declared_hash
        and candidate_hash_matches_text
    )
    text = candidate_text.lower()
    alignment = result.get("r1_3_result", {}).get("alignment", {})
    expected_alignment_id = trial_case.get("expected_alignment_id", "")
    expected_claim_ids, expected_claim_ids_valid, expected_claim_ids_type = normalize_claim_id_set(
        trial_case.get("expected_claim_ids", [])
    )
    visible_claim_ids, visible_claim_ids_valid, visible_claim_ids_type = normalize_claim_id_set(
        candidate_final.get("visible_claim_ids", [])
    )
    marker_groups = trial_case.get("expected_marker_groups", [])
    marker_group_results, marker_groups_valid, marker_groups_type = evaluate_marker_groups(marker_groups, text)
    alignment_id_match = bool(expected_alignment_id) and alignment.get("alignment_id") == expected_alignment_id
    claim_ids_match = (
        expected_claim_ids_valid
        and visible_claim_ids_valid
        and bool(expected_claim_ids)
        and visible_claim_ids == expected_claim_ids
    )
    marker_groups_match = marker_groups_valid and bool(marker_group_results) and all(marker_group_results)
    passed = (
        candidate_text_valid
        and
        alignment_id_match
        and claim_ids_match
        and marker_groups_match
        and candidate_hash_matches_text
        and r1_4_user_visible_matches_candidate
        and expected_claim_ids_valid
        and visible_claim_ids_valid
        and marker_groups_valid
    )
    raw_candidate_hashes_stored = passed
    raw_relevance_ids_stored = passed
    return {
        "passed": passed,
        "skipped": False,
        "alignment_id_match": alignment_id_match,
        "claim_ids_match": claim_ids_match,
        "claim_set_contract": "visible_claim_ids_exactly_equal_expected_claim_ids",
        "marker_groups_match": marker_groups_match,
        "candidate_hash_matches_text": candidate_hash_matches_text,
        "candidate_text_valid": candidate_text_valid,
        "candidate_text_type": audit_type_category(raw_candidate_text),
        "candidate_final_valid": candidate_final_valid,
        "r1_4_user_visible_matches_candidate": r1_4_user_visible_matches_candidate,
        "expected_claim_ids_valid": expected_claim_ids_valid,
        "visible_claim_ids_valid": visible_claim_ids_valid,
        "marker_groups_valid": marker_groups_valid,
        "expected_claim_ids_type": expected_claim_ids_type,
        "visible_claim_ids_type": visible_claim_ids_type,
        "marker_groups_type": marker_groups_type,
        "candidate_declared_sha256": candidate_declared_hash if raw_candidate_hashes_stored else "",
        "candidate_actual_sha256": candidate_actual_hash if raw_candidate_hashes_stored else "",
        "r1_4_user_visible_sha256": r1_4_visible.get("sha256", "") if raw_candidate_hashes_stored else "",
        "raw_candidate_sha256_stored": raw_candidate_hashes_stored,
        "candidate_text_audit": {} if raw_candidate_hashes_stored else unreleased_text_audit(raw_candidate_text, "relevance-candidate"),
        "r1_4_visible_text_audit": (
            {}
            if raw_candidate_hashes_stored
            else unreleased_text_audit(r1_4_visible.get("text", ""), "r1-4-visible-output")
        ),
        "marker_group_results": marker_group_results,
        "raw_relevance_ids_stored": raw_relevance_ids_stored,
        "expected_alignment_id": expected_alignment_id if raw_relevance_ids_stored else "",
        "actual_alignment_id": alignment.get("alignment_id", "") if raw_relevance_ids_stored else "",
        "expected_claim_ids": sorted(expected_claim_ids) if raw_relevance_ids_stored else [],
        "visible_claim_ids": sorted(visible_claim_ids) if raw_relevance_ids_stored else [],
        "expected_claim_id_count": len(expected_claim_ids),
        "visible_claim_id_count": len(visible_claim_ids),
    }


def fallback_text(reason: str, *, review: bool = False) -> dict[str, Any]:
    text = "The guarded answer could not be verified for this supervised trial request."
    if review:
        text = "This supervised trial request needs review. No unchecked answer was released."
    return {
        "final_text": text,
        "final_sha256": sha256_text(text),
        "release_state": "review_required" if review else "withheld",
        "answer_policy": "review" if review else "abstain",
        "status_label": "needs review" if review else "withheld",
        "fallback_reason": reason,
    }


def build_adapter_request(
    r14: Any,
    *,
    request_id: str,
    base_request: dict[str, Any],
    user_payload: dict[str, Any],
    server_context: dict[str, Any],
    flag_mode: str,
    fault_type: str = "",
) -> dict[str, Any]:
    query = user_payload.get("query", "")
    query_hash = sha256_text(query)
    trusted = copy.deepcopy(server_context)
    trusted["query"] = query
    trusted["query_sha256"] = query_hash
    trusted["guarded_answer_mode"] = flag_mode
    trusted["flag_source"] = "trusted_feature_flag_service"
    trusted["supplied_by"] = "trusted_runtime"
    user_clean = {
        "query": query,
        "query_sha256": user_payload.get("query_sha256", query_hash),
        "client_request_id": user_payload.get("client_request_id", request_id),
    }
    for key, value in user_payload.items():
        if key not in user_clean:
            user_clean[key] = value
    return {
        "request_id": request_id,
        "user_id": trusted.get("principal_id", ""),
        "tenant_id": trusted.get("tenant_id", ""),
        "query_mode": trusted.get("query_mode", ""),
        "risk_level": trusted.get("risk_level", ""),
        "domain": trusted.get("domain", ""),
        "guarded_answer_mode": trusted.get("guarded_answer_mode", ""),
        "trusted_runtime_context": trusted,
        "user_payload": user_clean,
        "user_text": query,
        "case": copy.deepcopy(base_request["case"]),
        "fault_type": fault_type,
        "case_class": trusted.get("case_class", "user_facing"),
    }


def process_adapter_case(
    stack: dict[str, Any],
    trial_case: dict[str, Any],
    output_dir: Path,
) -> dict[str, Any]:
    r14 = stack["r14"]
    started = time.perf_counter()
    sink = AdapterReleaseSink()
    pre_guard_text = trial_case.get("pre_guard_fact_text", "")
    if pre_guard_text:
        sink.attempt_fact_text(pre_guard_text, "before_guard")

    raw_user_payload = copy.deepcopy(trial_case["user_payload"])
    raw_server_context = copy.deepcopy(trial_case["server_context"])
    user_payload = raw_user_payload if isinstance(raw_user_payload, dict) else {}
    server_context = raw_server_context if isinstance(raw_server_context, dict) else {}
    user_policy_keys = set(user_payload) & (set(r14.USER_POLICY_KEYS) | ADAPTER_POLICY_KEYS)
    server_context_errors = validate_server_context(raw_server_context)
    user_payload_errors = validate_user_payload(raw_user_payload)
    flag_mode_errors = validate_flag_mode(trial_case.get("flag_mode"))
    query_binding_errors: list[str] = []
    if isinstance(raw_user_payload, dict) and isinstance(raw_server_context, dict):
        user_query = raw_user_payload.get("query")
        server_query = raw_server_context.get("query")
        if isinstance(user_query, str) and isinstance(server_query, str) and user_query != server_query:
            query_binding_errors.append("user_query_server_query_mismatch")
        server_query_sha = raw_server_context.get("query_sha256")
        if isinstance(user_query, str) and isinstance(server_query_sha, str) and is_sha256_hex(server_query_sha):
            if server_query_sha != sha256_text(user_query):
                query_binding_errors.append("server_query_sha256_does_not_match_user_query")
        server_mode = raw_server_context.get("guarded_answer_mode")
        flag_mode = trial_case.get("flag_mode")
        if isinstance(server_mode, str) and isinstance(flag_mode, str) and server_mode != flag_mode:
            query_binding_errors.append("server_guarded_answer_mode_flag_mode_mismatch")
    user_policy_errors = [f"user_payload_policy_field:{key}" for key in sorted(user_policy_keys)]
    reject_reasons = list(user_policy_errors)
    reject_reasons.extend(user_payload_errors)
    reject_reasons.extend(server_context_errors)
    reject_reasons.extend(flag_mode_errors)
    reject_reasons.extend(query_binding_errors)

    adapter_rejected = bool(reject_reasons)
    build_adapter_request_called = False
    untrusted_fallback_event: dict[str, Any] | None = None
    second_candidate_commit_event: dict[str, Any] | None = None
    second_fallback_commit_event: dict[str, Any] | None = None
    nonbool_gate_commit_event: dict[str, Any] | None = None
    sink_tamper_result: dict[str, Any] | None = None
    guarded_result: dict[str, Any] | None = None
    relevance = {
        "passed": True,
        "skipped": True,
        "reason": "not_evaluated",
        "alignment_id_match": True,
        "claim_ids_match": True,
        "marker_groups_match": True,
        "candidate_hash_matches_text": True,
        "r1_4_user_visible_matches_candidate": True,
    }
    candidate_commit_event: dict[str, Any] | None = None
    final_commit_event: dict[str, Any] | None = None

    if adapter_rejected:
        final, final_commit_event = sink.commit_safe_fallback("adapter_rejected")
    elif trial_case.get("flag_error"):
        final, final_commit_event = sink.commit_safe_fallback(
            "feature_flag_error",
            risk_class=server_context.get("risk_level", "low"),
        )
    elif trial_case["flag_mode"] == "off":
        final, final_commit_event = sink.commit_safe_fallback("feature_flag_off")
    else:
        build_adapter_request_called = True
        request = build_adapter_request(
            r14,
            request_id=trial_case["case_id"],
            base_request=trial_case["base_request"],
            user_payload=user_payload,
            server_context=server_context,
            flag_mode=trial_case["flag_mode"],
            fault_type=trial_case.get("fault_type", ""),
        )
        guarded_result = r14.process_live_request(
            stack["r11"],
            stack["r12"],
            stack["r13"],
            stack["guard"],
            request,
            output_dir / "r1_4_guarded_path",
        )
        candidate_final = copy.deepcopy(guarded_result["final_answer"])
        if trial_case.get("mutate_candidate_final_mismatch"):
            original_visible = copy.deepcopy(guarded_result.get("user_visible_output", {}))
            default_dangerous_text = f"{SENSITIVE_TOKENS[1]}: {SENSITIVE_TOKENS[2]}。"
            dangerous_text = trial_case.get("mutated_candidate_text", default_dangerous_text)
            candidate_final["final_text"] = dangerous_text
            candidate_final["final_sha256"] = sha256_text(dangerous_text)
            candidate_final["release_state"] = "released"
            candidate_final["answer_policy"] = "direct"
            candidate_final["atomic_release_phase"] = "committed_final"
            guarded_result["user_visible_output"] = original_visible
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if trial_case.get("mutate_extra_visible_claim"):
            visible_claim_ids = list(candidate_final.get("visible_claim_ids", []))
            if "extra-unrelated-claim" not in visible_claim_ids:
                visible_claim_ids.append("extra-unrelated-claim")
            candidate_final["visible_claim_ids"] = visible_claim_ids
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if trial_case.get("mutate_extra_candidate_trace"):
            candidate_final["debug_" + "raw_text"] = trial_case.get("legacy_unchecked_answer", SENSITIVE_TOKENS[0])
            candidate_final["trace"] = {
                "raw_" + "candidate_body": trial_case.get("legacy_unchecked_answer", SENSITIVE_TOKENS[1])
            }
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if trial_case.get("mutate_sensitive_release_fields"):
            sensitive_value = trial_case.get("legacy_unchecked_answer", SENSITIVE_TOKENS[0])
            candidate_final["release_state"] = sensitive_value
            candidate_final["answer_policy"] = sensitive_value
            candidate_final["atomic_release_phase"] = sensitive_value
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if trial_case.get("mutate_sensitive_visible_claim_id"):
            sensitive_value = trial_case.get("legacy_unchecked_answer", SENSITIVE_TOKENS[0])
            candidate_final["visible_claim_ids"] = ["c1", sensitive_value]
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if trial_case.get("mutate_malformed_candidate_text"):
            candidate_final["final_text"] = None
            candidate_final["final_sha256"] = "0" * 64
            candidate_final["release_state"] = "released"
            candidate_final["answer_policy"] = "direct"
            candidate_final["atomic_release_phase"] = "committed_final"
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if trial_case.get("mutate_unhashable_visible_claim_id"):
            candidate_final["visible_claim_ids"] = [{"id": "c1"}]
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if trial_case.get("mutate_nonlist_visible_claim_ids"):
            candidate_final["visible_claim_ids"] = 123
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if trial_case.get("mutate_nonobject_candidate_final"):
            candidate_final = ["not", "a", "final"]
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        malformed_claim_id_contract = trial_case.get("malformed_claim_id_contract", "")
        if malformed_claim_id_contract == "duplicate_visible":
            candidate_final["visible_claim_ids"] = ["c1", "c1"]
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if malformed_claim_id_contract == "duplicate_expected":
            candidate_final["visible_claim_ids"] = ["c1"]
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if malformed_claim_id_contract == "control":
            candidate_final["visible_claim_ids"] = ["c1\n"]
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        if malformed_claim_id_contract == "space":
            candidate_final["visible_claim_ids"] = [" c1 "]
            guarded_result["final_answer"] = copy.deepcopy(candidate_final)
        relevance = answer_relevance_evaluation(guarded_result, trial_case, candidate_final)
        candidate_commit_event = sink.commit_candidate(
            candidate_final,
            guard_passed=guarded_result.get("guard_status") == "pass",
            relevance_passed=bool(relevance["passed"]),
        )
        if candidate_commit_event.get("allowed"):
            final = candidate_final
        else:
            reason = "answer_relevance_failed" if not relevance["passed"] else "adapter_release_sink_denied"
            final, final_commit_event = sink.commit_safe_fallback(
                reason,
                risk_class=server_context.get("risk_level", "low"),
            )
        if trial_case.get("malicious_fallback_text"):
            untrusted_fallback_event = sink.attempt_untrusted_fallback_text(
                trial_case["malicious_fallback_text"],
                "adversarial_untrusted_fallback_text",
            )
        if trial_case.get("attempt_second_candidate_commit"):
            default_second_text = f"{SENSITIVE_TOKENS[1]}: {SENSITIVE_TOKENS[2]}。"
            second_text = trial_case.get("second_candidate_text", default_second_text)
            second_candidate = copy.deepcopy(candidate_final)
            second_candidate["final_text"] = second_text
            second_candidate["final_sha256"] = sha256_text(second_text)
            second_candidate["release_state"] = "released"
            second_candidate["answer_policy"] = "direct"
            second_candidate["atomic_release_phase"] = "committed_final"
            second_candidate_commit_event = sink.commit_candidate(
                second_candidate,
                guard_passed=True,
                relevance_passed=True,
            )
            if second_candidate_commit_event.get("allowed"):
                final = second_candidate
        if trial_case.get("attempt_second_fallback_commit"):
            second_fallback_final, second_fallback_commit_event = sink.commit_safe_fallback(
                "adapter_release_sink_denied",
                risk_class=server_context.get("risk_level", "low"),
            )
            if second_fallback_commit_event.get("allowed"):
                final = second_fallback_final
        if trial_case.get("attempt_nonbool_gate_commit"):
            nonbool_candidate = copy.deepcopy(candidate_final)
            nonbool_candidate["release_state"] = "released"
            nonbool_candidate["answer_policy"] = "direct"
            nonbool_candidate["atomic_release_phase"] = "committed_final"
            if not isinstance(nonbool_candidate.get("final_text"), str):
                nonbool_candidate["final_text"] = "DANGEROUS NONBOOL GATE"
                nonbool_candidate["final_sha256"] = sha256_text(nonbool_candidate["final_text"])
            guard_argument = trial_case.get("nonbool_guard_argument", True)
            relevance_argument = trial_case.get("nonbool_relevance_argument", True)
            nonbool_gate_commit_event = sink.commit_candidate(
                nonbool_candidate,
                guard_passed=guard_argument,
                relevance_passed=relevance_argument,
            )
            if nonbool_gate_commit_event.get("allowed"):
                final = nonbool_candidate
        adapter_candidate_allowed = bool(candidate_commit_event and candidate_commit_event.get("allowed"))
        guarded_result["candidate_final_answer"] = (
            copy.deepcopy(candidate_final)
            if adapter_candidate_allowed
            else sanitize_unreleased_final(candidate_final)
        )
        guarded_result["answer_relevance_evaluation"] = relevance
        guarded_result["answer_relevance_gate_triggered"] = not relevance["passed"]
        if not adapter_candidate_allowed:
            guarded_result["final_answer"] = sanitize_unreleased_final(guarded_result.get("final_answer"))
            guarded_result["user_visible_output"] = sanitize_unreleased_visible_output(
                guarded_result.get("user_visible_output")
            )

    if trial_case.get("attempt_sink_public_attribute_tamper"):
        tamper_attempts = []
        for attr, value in [
            ("user_visible_buffer", SENSITIVE_TOKENS[1]),
            ("sealed", False),
            ("committed_sha256", "0" * 64),
            ("committed_final", {"final_text": SENSITIVE_TOKENS[1]}),
        ]:
            try:
                setattr(sink, attr, value)
                tamper_attempts.append({"attribute": attr, "blocked": False, "error_class": ""})
            except Exception as exc:
                tamper_attempts.append({"attribute": attr, "blocked": True, "error_class": exc.__class__.__name__})
        before_event_count = len(sink.events)
        event_snapshot = sink.events
        event_snapshot.append({"event": "forged_event", "allowed": True})
        after_event_count = len(sink.events)
        sink_tamper_result = {
            "attempted": True,
            "public_attribute_tamper_blocked": all(item["blocked"] for item in tamper_attempts),
            "tamper_attempts": tamper_attempts,
            "event_snapshot_mutation_blocked": before_event_count == after_event_count,
            "event_count_before_snapshot_mutation": before_event_count,
            "event_count_after_snapshot_mutation": after_event_count,
            "buffer_sha256_after_tamper": sha256_text(sink.user_visible_buffer),
        }

    if guarded_result is None:
        guarded_result = {
            "request_id": trial_case["case_id"],
            "user_id": safe_text(server_context.get("principal_id", "")),
            "tenant_id": safe_text(server_context.get("tenant_id", "")),
            "query_mode": safe_text(server_context.get("query_mode", "")),
            "risk_level": safe_text(server_context.get("risk_level", "")),
            "domain": safe_text(server_context.get("domain", "")),
            "guarded_answer_mode": safe_text(trial_case.get("flag_mode", "")),
            "effective_policy": {
                "query_sha256": safe_sha256_text(user_payload.get("query", "")),
                "guarded_answer_mode": safe_text(trial_case.get("flag_mode", "")),
            },
            "eligible_for_guarded_enforce": False,
            "guarded_applied": False,
            "guard_status": "not_run",
            "release_sink_allowed": False,
            "final_answer": final,
            "user_visible_output": {"text": sink.user_visible_buffer, "sha256": sha256_text(sink.user_visible_buffer)},
            "eligibility_reasons": reject_reasons or [final.get("fallback_reason", "")],
            "answer_relevance_evaluation": relevance,
            "answer_relevance_gate_triggered": False,
        }

    old_answer = safe_text(trial_case.get("legacy_unchecked_answer", ""))
    user_visible_output = {"text": sink.user_visible_buffer, "sha256": sha256_text(sink.user_visible_buffer)}
    visible_text = user_visible_output["text"]
    result = {
        "request_id": trial_case["case_id"],
        "trial_case_id": trial_case["case_id"],
        "category": trial_case["category"],
        "non_json_fixture_value": bool(trial_case.get("non_json_fixture_value")),
        "non_string_key_fixture": bool(trial_case.get("non_string_key_fixture")),
        "non_json_object_fixture": bool(trial_case.get("non_json_object_fixture")),
        "repr_side_channel_fixture": bool(trial_case.get("repr_side_channel_fixture")),
        "exploding_repr_fixture": bool(trial_case.get("exploding_repr_fixture")),
        "json_resource_fixture": bool(trial_case.get("json_resource_fixture")),
        "adapter_rejected": adapter_rejected,
        "adapter_reject_reasons": reject_reasons,
        "user_policy_errors": user_policy_errors,
        "server_context_errors": server_context_errors,
        "flag_mode_errors": flag_mode_errors,
        "query_binding_errors": query_binding_errors,
        "server_context_accepted": not adapter_rejected,
        "build_adapter_request_called": build_adapter_request_called,
        "trusted_context_origin": safe_text(server_context.get("trusted_context_origin", "")),
        "iam_subject_verified": server_context.get("iam_subject_verified") is True,
        "feature_flag_resolved_by": safe_text(server_context.get("feature_flag_resolved_by", "")),
        "feature_flag_mode": safe_text(trial_case.get("flag_mode", "")),
        "feature_flag_error": bool(trial_case.get("flag_error")),
        "guarded_applied": guarded_result.get("guarded_applied", False),
        "guard_status": guarded_result.get("guard_status", ""),
        "internal_r1_4_release_sink_allowed": guarded_result.get("release_sink_allowed", False),
        "adapter_release_sink_allowed": bool(candidate_commit_event and candidate_commit_event.get("allowed")),
        "release_sink_allowed": bool(candidate_commit_event and candidate_commit_event.get("allowed")),
        "candidate_commit_event": candidate_commit_event,
        "final_commit_event": final_commit_event,
        "untrusted_fallback_event": untrusted_fallback_event,
        "second_candidate_commit_event": second_candidate_commit_event,
        "second_fallback_commit_event": second_fallback_commit_event,
        "nonbool_gate_commit_event": nonbool_gate_commit_event,
        "sink_tamper_result": sink_tamper_result,
        "final_answer": final,
        "user_visible_output": user_visible_output,
        "visible_events": sink.events,
        "pre_guard_fact_leaked": any(
            event.get("event") == "fact_text_write_attempt" and event.get("allowed") for event in sink.events
        ),
        "user_visible_buffer_sha256": sha256_text(sink.user_visible_buffer),
        "user_visible_output_from_sink": (
            user_visible_output.get("text", "") == sink.user_visible_buffer
            and user_visible_output.get("sha256", "") == sha256_text(sink.user_visible_buffer)
        ),
        "answer_relevance_evaluation": relevance,
        "answer_relevance_original_pass": relevance.get("passed", True),
        "answer_relevance_gate_triggered": not relevance.get("passed", True),
        "answer_relevance_release_safe": final.get("release_state") != "released" or relevance.get("passed", True),
        "old_answer_leaked": bool(old_answer and old_answer in visible_text),
        "r1_4_result": sanitize_r1_4_result_for_artifact(guarded_result),
        "elapsed_ms": round((time.perf_counter() - started) * 1000.0, 6),
    }
    result["log_event"] = sanitize_log(
        {
            **guarded_result,
            "release_sink_allowed": result["release_sink_allowed"],
            "final_answer": final,
            "user_visible_output": user_visible_output,
            "eligibility_reasons": reject_reasons or guarded_result.get("eligibility_reasons", []),
        }
    )
    return result


def build_trial_cases(stack: dict[str, Any]) -> list[dict[str, Any]]:
    base_requests = public_case_requests(stack)
    released_bases = []
    seen_drafts: set[str] = set()
    for request in base_requests:
        support_terms = request["case"].get("alignment_contract", {}).get("answer_terms", [])
        draft_text = request["case"].get("draft", {}).get("draft_text", "")
        if support_terms and draft_text not in seen_drafts:
            seen_drafts.add(draft_text)
            released_bases.append((request, support_terms))
    primary, primary_markers = released_bases[0]
    secondary, secondary_markers = released_bases[1]

    def marker_groups(base: dict[str, Any], markers: list[str]) -> list[list[str]]:
        terms = [term for term in markers if isinstance(term, str) and len(term) >= 3]
        if not terms:
            return []
        groups = [[terms[0]]]
        if len(terms) > 1:
            groups.append([terms[1]])
        return groups

    def common(
        case_id: str,
        category: str,
        base: dict[str, Any],
        markers: list[str],
        *,
        mode: str = "enforce",
        server_overrides: dict[str, Any] | None = None,
        user_overrides: dict[str, Any] | None = None,
        flag_error: bool = False,
        fault_type: str = "",
        pre_guard: bool = False,
        legacy: str = "",
        mutate_candidate: bool = False,
        malicious_fallback_text: str = "",
        mutate_extra_visible_claim: bool = False,
        mutate_extra_candidate_trace: bool = False,
        mutate_sensitive_release_fields: bool = False,
        mutate_sensitive_visible_claim_id: bool = False,
        mutate_malformed_candidate_text: bool = False,
        second_candidate_commit: bool = False,
        second_fallback_commit: bool = False,
        sink_public_attribute_tamper: bool = False,
        mutate_unhashable_visible_claim_id: bool = False,
        mutate_nonlist_visible_claim_ids: bool = False,
        mutate_bad_marker_group: bool = False,
        mutate_nonobject_candidate_final: bool = False,
        nonbool_gate_argument: str = "",
        sensitive_nonbool_gate_argument: str = "",
        malformed_claim_id_contract: str = "",
        user_payload_shape: str = "",
        server_context_shape: str = "",
        non_json_fixture_value: bool = False,
        non_string_key_fixture: bool = False,
        non_json_object_fixture: bool = False,
        repr_side_channel_fixture: bool = False,
        exploding_repr_fixture: bool = False,
        json_resource_fixture: bool = False,
    ) -> dict[str, Any]:
        context = server_context_for(base, mode=mode)
        if server_overrides:
            context.update(server_overrides)
        payload = {"query": base["case"]["query"], "query_sha256": sha256_text(base["case"]["query"])}
        if user_overrides:
            payload.update(user_overrides)
        case = {
            "case_id": case_id,
            "category": category,
            "base_request_id": base["request_id"],
            "base_request": base,
            "server_context": context,
            "user_payload": payload,
            "flag_mode": mode,
            "flag_error": flag_error,
            "fault_type": fault_type,
            "expected_answer_markers": markers,
            "expected_marker_groups": marker_groups(base, markers),
            "expected_alignment_id": base["case"].get("alignment_contract", {}).get("alignment_id", ""),
            "expected_claim_ids": base["case"].get("alignment_contract", {}).get("expected_claim_ids", []),
            "pre_guard_fact_text": base["case"].get("draft", {}).get("draft_text", "") if pre_guard else "",
            "legacy_unchecked_answer": legacy,
            "mutate_candidate_final_mismatch": mutate_candidate,
            "malicious_fallback_text": malicious_fallback_text,
            "mutate_extra_visible_claim": mutate_extra_visible_claim,
            "mutate_extra_candidate_trace": mutate_extra_candidate_trace,
            "mutate_sensitive_release_fields": mutate_sensitive_release_fields,
            "mutate_sensitive_visible_claim_id": mutate_sensitive_visible_claim_id,
            "mutate_malformed_candidate_text": mutate_malformed_candidate_text,
            "attempt_second_candidate_commit": second_candidate_commit,
            "attempt_second_fallback_commit": second_fallback_commit,
            "attempt_sink_public_attribute_tamper": sink_public_attribute_tamper,
            "mutate_unhashable_visible_claim_id": mutate_unhashable_visible_claim_id,
            "mutate_nonlist_visible_claim_ids": mutate_nonlist_visible_claim_ids,
            "mutate_bad_marker_group": mutate_bad_marker_group,
            "mutate_nonobject_candidate_final": mutate_nonobject_candidate_final,
            "attempt_nonbool_gate_commit": bool(nonbool_gate_argument or sensitive_nonbool_gate_argument),
            "nonbool_guard_argument": (
                sensitive_legacy
                if sensitive_nonbool_gate_argument == "guard"
                else ("false" if nonbool_gate_argument == "guard" else True)
            ),
            "nonbool_relevance_argument": (
                sensitive_legacy
                if sensitive_nonbool_gate_argument == "relevance"
                else (1 if nonbool_gate_argument == "relevance" else True)
            ),
            "malformed_claim_id_contract": malformed_claim_id_contract,
            "non_json_fixture_value": non_json_fixture_value,
            "non_string_key_fixture": non_string_key_fixture,
            "non_json_object_fixture": non_json_object_fixture,
            "repr_side_channel_fixture": repr_side_channel_fixture,
            "exploding_repr_fixture": exploding_repr_fixture,
            "json_resource_fixture": json_resource_fixture,
            "second_candidate_text": sensitive_legacy if second_candidate_commit else "",
        }
        if mutate_bad_marker_group:
            case["expected_marker_groups"] = [123]
        if malformed_claim_id_contract == "duplicate_visible":
            case["expected_claim_ids"] = ["c1"]
        if malformed_claim_id_contract == "duplicate_expected":
            case["expected_claim_ids"] = ["c1", "c1"]
        if malformed_claim_id_contract == "control":
            case["expected_claim_ids"] = ["c1\n"]
        if malformed_claim_id_contract == "space":
            case["expected_claim_ids"] = [" c1 "]
        if user_payload_shape == "nonobject":
            case["user_payload"] = ["not", "an", "object"]
        if server_context_shape == "nonobject":
            case["server_context"] = ["not", "an", "object"]
        return case

    sensitive_legacy = f"{SENSITIVE_TOKENS[1]}: 公司允许{SENSITIVE_TOKENS[2]}。 {SENSITIVE_TOKENS[0]}"
    sensitive_type_object = type(SENSITIVE_TOKENS[0], (), {})()
    exploding_user_key = ExplodingReprProbeObject()
    exploding_server_key = ExplodingReprProbeObject()
    cyclic_list: list[Any] = []
    cyclic_list.append(cyclic_list)
    deep_list: list[Any] = []
    cursor = deep_list
    for _index in range(JSON_SAFE_MAX_DEPTH + 5):
        child: list[Any] = []
        cursor.append(child)
        cursor = child
    large_list = list(range(JSON_SAFE_MAX_ITEMS + 25))
    long_string = "x" * (JSON_SAFE_MAX_STRING_CHARS + 128)
    long_sensitive_string = ("lead-" + SENSITIVE_TOKENS[0] + "-") * (JSON_SAFE_MAX_STRING_CHARS // 16)
    cases = [
        common("trial-001-happy-release", "happy_release", primary, primary_markers),
        common("trial-002-policy-injection", "server_envelope", primary, primary_markers,
               user_overrides={"risk_level": "low", "trusted_runtime_context": {"risk_level": "low"}}),
        common("trial-003-fake-server-origin", "server_envelope", primary, primary_markers,
               server_overrides={
                   "trusted_context_origin": "user_payload",
                   "iam_subject_verified": False,
                   "feature_flag_resolved_by": "user",
               }),
        common("trial-004-flag-off", "feature_flag_off", primary, primary_markers, mode="off"),
        common("trial-005-flag-error", "feature_flag_error", primary, primary_markers, flag_error=True),
        common("trial-006-answer-relevance-negative", "answer_relevance", primary, ["员工年假上限"]),
        common("trial-007-answer-relevance-shared-marker", "answer_relevance", primary, ["exact"]),
        common("trial-008-pre-guard-stream-attempt", "pre_guard_output", primary, primary_markers, pre_guard=True),
        common("trial-009-guard-error-fallback", "fallback", primary, primary_markers, fault_type="guard_error",
               legacy=sensitive_legacy),
        common("trial-010-log-redaction-sensitive", "log_redaction", secondary, secondary_markers,
               user_overrides={"client_note": SENSITIVE_TOKENS[0], "legacy_answer": sensitive_legacy},
               legacy=sensitive_legacy),
        common("trial-011-high-risk-fail-closed", "high_risk_fallback", primary, primary_markers,
               server_overrides={"risk_level": "high", "query_mode": "action", "domain": "finance"},
               legacy=sensitive_legacy),
        common("trial-012-second-happy-release", "happy_release", secondary, secondary_markers),
        common("trial-013-r1-4-final-user-visible-mismatch", "candidate_final_mismatch", primary, primary_markers,
               mutate_candidate=True, legacy=sensitive_legacy),
        common("trial-014-untrusted-fallback-text-attempt", "fallback_sink_contract", primary, primary_markers,
               fault_type="guard_error", malicious_fallback_text=sensitive_legacy, legacy=sensitive_legacy),
        common("trial-015-candidate-to-candidate-overwrite", "sink_write_once", secondary, secondary_markers,
               second_candidate_commit=True, legacy=sensitive_legacy),
        common("trial-016-fallback-to-candidate-overwrite", "sink_write_once", primary, primary_markers,
               fault_type="guard_error", second_candidate_commit=True, legacy=sensitive_legacy),
        common("trial-017-candidate-to-fallback-overwrite", "sink_write_once", secondary, secondary_markers,
               second_fallback_commit=True, legacy=sensitive_legacy),
        common("trial-018-extra-visible-claim", "answer_relevance", primary, primary_markers,
                mutate_extra_visible_claim=True),
        common("trial-019-extra-sensitive-candidate-trace", "candidate_schema", primary, primary_markers,
               mutate_extra_candidate_trace=True, legacy=sensitive_legacy),
        common("trial-020-sensitive-release-fields", "candidate_audit_minimization", primary, primary_markers,
               mutate_sensitive_release_fields=True, legacy=sensitive_legacy),
        common("trial-021-sensitive-visible-claim-id", "candidate_audit_minimization", primary, primary_markers,
               mutate_sensitive_visible_claim_id=True, legacy=sensitive_legacy),
        common("trial-022-sensitive-nonbool-guard-argument", "sink_audit_minimization", secondary, secondary_markers,
               sensitive_nonbool_gate_argument="guard", legacy=sensitive_legacy),
        common("trial-023-sensitive-nonbool-relevance-argument", "sink_audit_minimization", secondary, secondary_markers,
               sensitive_nonbool_gate_argument="relevance", legacy=sensitive_legacy),
        common("trial-024-malformed-candidate-text", "malformed_candidate", primary, primary_markers,
               mutate_malformed_candidate_text=True),
        common("trial-025-sink-public-attribute-tamper", "sink_api_hardening", secondary, secondary_markers,
               sink_public_attribute_tamper=True, legacy=sensitive_legacy),
        common("trial-026-unhashable-visible-claim-id", "malformed_relevance_contract", primary, primary_markers,
               mutate_unhashable_visible_claim_id=True),
        common("trial-027-nonlist-visible-claim-ids", "malformed_relevance_contract", primary, primary_markers,
               mutate_nonlist_visible_claim_ids=True),
        common("trial-028-bad-marker-group", "malformed_relevance_contract", primary, primary_markers,
               mutate_bad_marker_group=True),
        common("trial-029-nonobject-candidate-final", "malformed_relevance_contract", primary, primary_markers,
               mutate_nonobject_candidate_final=True),
        common("trial-030-nonbool-guard-argument", "sink_api_hardening", secondary, secondary_markers,
               nonbool_gate_argument="guard", legacy=sensitive_legacy),
        common("trial-031-nonbool-relevance-argument", "sink_api_hardening", secondary, secondary_markers,
               nonbool_gate_argument="relevance", legacy=sensitive_legacy),
        common("trial-032-duplicate-visible-claim-id", "malformed_relevance_contract", primary, primary_markers,
               malformed_claim_id_contract="duplicate_visible"),
        common("trial-033-duplicate-expected-claim-id", "malformed_relevance_contract", primary, primary_markers,
               malformed_claim_id_contract="duplicate_expected"),
        common("trial-034-control-char-claim-id", "malformed_relevance_contract", primary, primary_markers,
               malformed_claim_id_contract="control"),
        common("trial-035-space-padded-claim-id", "malformed_relevance_contract", primary, primary_markers,
               malformed_claim_id_contract="space"),
        common("trial-036-nonstring-query", "adapter_input_type", primary, primary_markers,
               user_overrides={"query": None}),
        common("trial-036b-nonstring-query-sha", "adapter_input_type", primary, primary_markers,
               user_overrides={"query_sha256": 123}),
        common("trial-033-nonstring-principal", "adapter_input_type", primary, primary_markers,
               server_overrides={"principal_id": {"id": "internal-user"}}),
        common("trial-034-nonstring-tenant", "adapter_input_type", primary, primary_markers,
               server_overrides={"tenant_id": ["tenant-internal"]}),
        common("trial-035-user-payload-not-object", "adapter_input_type", primary, primary_markers,
               user_payload_shape="nonobject"),
        common("trial-036-server-context-not-object", "adapter_input_type", primary, primary_markers,
               server_context_shape="nonobject"),
        common("trial-037-user-payload-unknown-field", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_note": SENSITIVE_TOKENS[0]}),
        common("trial-038-client-request-id-not-string", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": 123}),
        common("trial-039-server-context-unknown-field", "adapter_input_type", primary, primary_markers,
               server_overrides={"extra_context": SENSITIVE_TOKENS[0]}),
        common("trial-040-flag-mode-invalid-string", "adapter_input_type", primary, primary_markers,
               mode="enabled"),
        common("trial-041-flag-mode-invalid-bool", "adapter_input_type", primary, primary_markers,
               mode=True),
        common("trial-042-user-query-sha-mismatch", "adapter_input_type", primary, primary_markers,
               user_overrides={"query_sha256": "0" * 64}),
        common("trial-043-user-query-sha-invalid", "adapter_input_type", primary, primary_markers,
               user_overrides={"query_sha256": "not-a-sha"}),
        common("trial-044-user-query-control-char", "adapter_input_type", primary, primary_markers,
               user_overrides={"query": primary["case"]["query"] + "\u200b"}),
        common("trial-045-user-query-too-long", "adapter_input_type", primary, primary_markers,
               user_overrides={"query": "a" * (MAX_QUERY_CHARS + 1)}),
        common("trial-046-server-user-query-mismatch", "adapter_input_type", primary, primary_markers,
               server_overrides={
                   "query": "A different server-side query.",
                   "query_sha256": sha256_text("A different server-side query."),
               }),
        common("trial-047-server-query-sha-mismatch", "adapter_input_type", primary, primary_markers,
               server_overrides={"query_sha256": "0" * 64}),
        common("trial-048-context-mode-mismatch", "adapter_input_type", primary, primary_markers,
               server_overrides={"guarded_answer_mode": "off"}),
        common("trial-049-principal-not-allowlisted", "adapter_input_type", primary, primary_markers,
               server_overrides={"principal_id": "internal-beta"}),
        common("trial-050-principal-control-char", "adapter_input_type", primary, primary_markers,
               server_overrides={"principal_id": "internal-alpha\u200b"}),
        common("trial-051-client-request-id-control-char", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": "client-001\n"}),
        common("trial-052-user-query-nan", "adapter_input_type", primary, primary_markers,
               user_overrides={"query": float("nan")}, non_json_fixture_value=True),
        common("trial-053-user-extra-nan", "adapter_input_type", primary, primary_markers,
               user_overrides={"extra_nan": float("nan")}, non_json_fixture_value=True),
        common("trial-054-server-principal-nan", "adapter_input_type", primary, primary_markers,
               server_overrides={"principal_id": float("nan")}, non_json_fixture_value=True),
        common("trial-055-server-extra-inf", "adapter_input_type", primary, primary_markers,
               server_overrides={"extra_inf": float("inf")}, non_json_fixture_value=True),
        common("trial-056-user-nonstring-key-collision", "adapter_input_type", primary, primary_markers,
               user_overrides={1: "int-key-value", "1": "string-key-value"}, non_string_key_fixture=True),
        common("trial-057-server-nonstring-key", "adapter_input_type", primary, primary_markers,
               server_overrides={1: "int-key-value"}, non_string_key_fixture=True),
        common("trial-058-user-bytes-value", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": SENSITIVE_TOKENS[0].encode("utf-8")}, non_json_object_fixture=True),
        common("trial-059-user-set-value", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": {"client-a", "client-b"}}, non_json_object_fixture=True),
        common("trial-060-user-object-value", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": NonJsonProbeObject()}, non_json_object_fixture=True),
        common("trial-061-server-bytes-value", "adapter_input_type", primary, primary_markers,
               server_overrides={"principal_id": SENSITIVE_TOKENS[0].encode("utf-8")}, non_json_object_fixture=True),
        common("trial-062-user-sensitive-key", "adapter_input_type", primary, primary_markers,
               user_overrides={SENSITIVE_TOKENS[0]: "sensitive-key-value"}),
        common("trial-063-user-sensitive-key-redaction-collision", "adapter_input_type", primary, primary_markers,
               user_overrides={SENSITIVE_TOKENS[0]: "sensitive-key-value", SENSITIVE_REDACTIONS[SENSITIVE_TOKENS[0]]: "already-redacted-key"}),
        common("trial-064-user-bytearray-value", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": bytearray(SENSITIVE_TOKENS[0].encode("utf-8"))}, non_json_object_fixture=True),
        common("trial-065-user-utf16-bytes-value", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": SENSITIVE_TOKENS[0].encode("utf-16le")}, non_json_object_fixture=True),
        common("trial-066-server-utf16-bytearray-value", "adapter_input_type", primary, primary_markers,
               server_overrides={"principal_id": bytearray(SENSITIVE_TOKENS[0].encode("utf-16be"))}, non_json_object_fixture=True),
        common("trial-067-user-sensitive-repr-object", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": SensitiveReprProbeObject()}, non_json_object_fixture=True,
               repr_side_channel_fixture=True),
        common("trial-068-user-sensitive-type-name-object", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": sensitive_type_object}, non_json_object_fixture=True,
               repr_side_channel_fixture=True),
        common("trial-069-user-cyclic-list", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": cyclic_list}, json_resource_fixture=True),
        common("trial-070-user-deep-list", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": deep_list}, json_resource_fixture=True),
        common("trial-071-user-large-list", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": large_list}, json_resource_fixture=True),
        common("trial-072-user-long-string", "adapter_input_type", primary, primary_markers,
               user_overrides={"client_request_id": long_string}, json_resource_fixture=True),
        common("trial-073-user-long-sensitive-string", "adapter_input_type", primary, primary_markers,
                user_overrides={"client_request_id": long_sensitive_string}, json_resource_fixture=True),
        common("trial-074-user-exploding-repr-key", "adapter_input_type", primary, primary_markers,
               user_overrides={exploding_user_key: "untrusted-key-value"}, non_string_key_fixture=True,
               exploding_repr_fixture=True),
        common("trial-075-server-exploding-repr-key", "adapter_input_type", primary, primary_markers,
               server_overrides={exploding_server_key: "untrusted-key-value"}, non_string_key_fixture=True,
               exploding_repr_fixture=True),
        common("trial-076-unknown-sensitive-user-payload", "artifact_minimization", primary, primary_markers,
               user_overrides={"client_request_id": UNKNOWN_SENSITIVE_PROBES[0]}),
        common("trial-077-unknown-sensitive-query", "artifact_minimization", primary, primary_markers,
               user_overrides={
                   "query": UNKNOWN_SENSITIVE_PROBES[1],
                   "query_sha256": sha256_text(UNKNOWN_SENSITIVE_PROBES[1]),
               },
               server_overrides={
                   "query": UNKNOWN_SENSITIVE_PROBES[1],
                   "query_sha256": sha256_text(UNKNOWN_SENSITIVE_PROBES[1]),
               }),
    ]
    for case in cases:
        if case["case_id"] == "trial-007-answer-relevance-shared-marker":
            case["expected_marker_groups"] = [["exact"], ["annual leave", "年假"]]
    return cases


def jsonl_text(rows: list[dict[str, Any]]) -> str:
    return "".join(stable_json(json_safe(row)) + "\n" for row in rows)


def strict_jsonl_parse_failure_count(text: str) -> int:
    failures = 0

    def reject_nonstandard_constant(value: str) -> None:
        raise ValueError(f"non-standard JSON constant: {value}")

    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            json.loads(line, parse_constant=reject_nonstandard_constant)
        except Exception:
            failures += 1
    return failures


def sanitize_trial_case_for_artifact(case: dict[str, Any]) -> dict[str, Any]:
    server_context = case.get("server_context", {})
    user_payload = case.get("user_payload", {})
    marker_groups = case.get("expected_marker_groups", [])
    expected_claim_ids = case.get("expected_claim_ids", [])
    safe_case = {
        "case_id": safe_text(case.get("case_id", "")),
        "category": safe_text(case.get("category", "")),
        "base_request_id": safe_text(case.get("base_request_id", "")),
        "flag_mode": enum_audit(case.get("flag_mode", ""), FEATURE_FLAG_MODES, role="trial_flag_mode"),
        "flag_error": bool(case.get("flag_error")),
        "fault_type": enum_audit(case.get("fault_type", ""), {"", "guard_error"}, role="trial_fault_type"),
        "server_context_shape": {
            "is_object": isinstance(server_context, dict),
            "key_count": len(server_context) if isinstance(server_context, dict) else 0,
            "query_hmac": safe_hmac_text(server_context.get("query", "")) if isinstance(server_context, dict) else "",
            "query_sha256_valid": (
                isinstance(server_context, dict)
                and is_sha256_hex(server_context.get("query_sha256", ""))
            ),
            "policy": {
                "query_mode": safe_text(server_context.get("query_mode", "")) if isinstance(server_context, dict) else "",
                "risk_level": safe_text(server_context.get("risk_level", "")) if isinstance(server_context, dict) else "",
                "domain": safe_text(server_context.get("domain", "")) if isinstance(server_context, dict) else "",
                "case_class": safe_text(server_context.get("case_class", "")) if isinstance(server_context, dict) else "",
            },
        },
        "user_payload_shape": {
            "is_object": isinstance(user_payload, dict),
            "key_count": len(user_payload) if isinstance(user_payload, dict) else 0,
            "query_hmac": safe_hmac_text(user_payload.get("query", "")) if isinstance(user_payload, dict) else "",
            "query_sha256_valid": (
                isinstance(user_payload, dict)
                and (
                    "query_sha256" not in user_payload
                    or is_sha256_hex(user_payload.get("query_sha256", ""))
                )
            ),
        },
        "expected_contract_shape": {
            "alignment_hmac": safe_hmac_text(case.get("expected_alignment_id", "")),
            "marker_group_count": len(marker_groups) if isinstance(marker_groups, list) else 0,
            "expected_claim_id_count": len(expected_claim_ids) if isinstance(expected_claim_ids, list) else 0,
        },
        "mutation_flags": {
            key: bool(case.get(key))
            for key in sorted(case)
            if key.startswith("mutate_") or key.startswith("attempt_") or key.endswith("_fixture")
        },
        "raw_query_stored": False,
        "raw_payload_stored": False,
        "raw_server_context_stored": False,
        "raw_expected_markers_stored": False,
    }
    return safe_case


def sanitize_r1_4_result_for_artifact(result: Any) -> dict[str, Any]:
    if not isinstance(result, dict):
        return {
            "__r1_4_result_sanitized__": {
                "result_valid": False,
                "result_type": audit_type_category(result),
            }
        }
    effective_policy = result.get("effective_policy", {})
    query_binding = result.get("query_binding", {})
    alignment = result.get("r1_3_result", {}).get("alignment", {})
    release_events = result.get("release_sink_events", [])
    return {
        "__r1_4_result_sanitized__": {
            "result_valid": True,
            "request_id": safe_text(result.get("request_id", "")),
            "query_mode": safe_text(result.get("query_mode", "")),
            "risk_level": safe_text(result.get("risk_level", "")),
            "domain": safe_text(result.get("domain", "")),
            "guarded_answer_mode": safe_text(result.get("guarded_answer_mode", "")),
            "eligible_for_guarded_enforce": result.get("eligible_for_guarded_enforce") is True,
            "guarded_applied": result.get("guarded_applied") is True,
            "guard_status": safe_text(result.get("guard_status", "")),
            "release_sink_allowed": result.get("release_sink_allowed") is True,
            "effective_policy": {
                "query_hmac": (
                    safe_hmac_text(effective_policy.get("query", ""))
                    if isinstance(effective_policy, dict)
                    else ""
                ),
                "query_sha256_valid": (
                    isinstance(effective_policy, dict)
                    and is_sha256_hex(effective_policy.get("query_sha256", ""))
                ),
                "raw_query_stored": False,
                "raw_query_sha256_stored": False,
            },
            "query_binding": {
                "ok": (
                    isinstance(query_binding, dict)
                    and query_binding.get("ok") is True
                ),
                "error_count": (
                    len(query_binding.get("errors", []))
                    if isinstance(query_binding, dict) and isinstance(query_binding.get("errors", []), list)
                    else 0
                ),
                "raw_query_hashes_stored": False,
            },
            "alignment": {
                "alignment_hmac": (
                    safe_hmac_text(alignment.get("alignment_id", ""))
                    if isinstance(alignment, dict)
                    else ""
                ),
                "raw_alignment_id_stored": False,
            },
            "source_authority_coherence": {
                "ok": result.get("source_authority_coherence", {}).get("ok") is True
                if isinstance(result.get("source_authority_coherence"), dict)
                else False,
                "violation_count": result.get("source_authority_coherence", {}).get("violation_count", 0)
                if isinstance(result.get("source_authority_coherence"), dict)
                else 0,
            },
            "final_answer": sanitize_unreleased_final(result.get("final_answer", {})),
            "user_visible_output": sanitize_unreleased_visible_output(result.get("user_visible_output", {})),
            "release_sink_event_count": len(release_events) if isinstance(release_events, list) else 0,
            "raw_result_text_stored": False,
        }
    }


def sanitize_final_for_artifact(final: Any) -> dict[str, Any]:
    if not isinstance(final, dict):
        return {
            "__final_answer_sanitized__": {
                "final_valid": False,
                "final_type": audit_type_category(final),
                "raw_text_stored": False,
                "raw_sha256_stored": False,
            }
        }
    text = final.get("final_text", "")
    citations = final.get("citations", [])
    visible_claim_ids = final.get("visible_claim_ids", [])
    return {
        "__final_answer_sanitized__": {
            "final_valid": True,
            "release_state": enum_audit(final.get("release_state", ""), FINAL_RELEASE_STATES, role="artifact_release_state"),
            "answer_policy": enum_audit(final.get("answer_policy", ""), FINAL_ANSWER_POLICIES, role="artifact_answer_policy"),
            "atomic_release_phase": enum_audit(
                final.get("atomic_release_phase", ""),
                FINAL_ATOMIC_PHASES,
                role="artifact_atomic_release_phase",
            ),
            "text_audit": unreleased_text_audit(text, "artifact-final-answer"),
            "final_hmac": safe_hmac_text(text) if isinstance(text, str) else "",
            "citation_count": len(citations) if isinstance(citations, list) else 0,
            "visible_claim_count": len(visible_claim_ids) if isinstance(visible_claim_ids, list) else 0,
            "action_readiness_granted": final.get("action_readiness_granted") is True,
            "reviewed_truth_granted": final.get("reviewed_truth_granted") is True,
            "promotion_granted": final.get("promotion_granted") is True,
            "raw_text_stored": False,
            "raw_sha256_stored": False,
            "raw_citations_stored": False,
        }
    }


def sanitize_visible_output_for_artifact(output: Any) -> dict[str, Any]:
    if not isinstance(output, dict):
        return {
            "__user_visible_output_sanitized__": {
                "output_valid": False,
                "output_type": audit_type_category(output),
                "raw_text_stored": False,
                "raw_sha256_stored": False,
            }
        }
    text = output.get("text", "")
    return {
        "__user_visible_output_sanitized__": {
            "output_valid": True,
            "text_audit": unreleased_text_audit(text, "artifact-user-visible-output"),
            "text_hmac": safe_hmac_text(text) if isinstance(text, str) else "",
            "sha256_valid": is_sha256_hex(output.get("sha256", "")),
            "raw_text_stored": False,
            "raw_sha256_stored": False,
        }
    }


def sanitize_relevance_for_artifact(relevance: Any) -> dict[str, Any]:
    if not isinstance(relevance, dict):
        return {
            "__answer_relevance_sanitized__": {
                "valid": False,
                "type": audit_type_category(relevance),
                "raw_ids_stored": False,
                "raw_hashes_stored": False,
            }
        }
    return {
        "__answer_relevance_sanitized__": {
            "valid": True,
            "passed": relevance.get("passed") is True,
            "skipped": relevance.get("skipped") is True,
            "alignment_id_match": relevance.get("alignment_id_match") is True,
            "claim_ids_match": relevance.get("claim_ids_match") is True,
            "marker_groups_match": relevance.get("marker_groups_match") is True,
            "candidate_hash_matches_text": relevance.get("candidate_hash_matches_text") is True,
            "r1_4_user_visible_matches_candidate": relevance.get("r1_4_user_visible_matches_candidate") is True,
            "expected_claim_id_count": relevance.get("expected_claim_id_count", 0),
            "visible_claim_id_count": relevance.get("visible_claim_id_count", 0),
            "raw_ids_stored": False,
            "raw_hashes_stored": False,
        }
    }


def sanitize_sink_event_for_artifact(event: Any) -> dict[str, Any]:
    if not isinstance(event, dict):
        return {
            "__sink_event_sanitized__": {
                "event_valid": False,
                "event_type": audit_type_category(event),
                "raw_hashes_stored": False,
                "raw_text_stored": False,
            }
        }
    return {
        "__sink_event_sanitized__": {
            "event_valid": True,
            "event": safe_text(event.get("event", "")),
            "stage": safe_text(event.get("stage", "")),
            "allowed": event.get("allowed") is True,
            "blocked": event.get("blocked") is True,
            "blocked_reason": enum_audit(
                event.get("blocked_reason", ""),
                {"", "validation_failed", "sink_sealed"},
                role="sink_blocked_reason",
            ),
            "guard_passed_valid": event.get("guard_passed_valid") is True,
            "relevance_passed_valid": event.get("relevance_passed_valid") is True,
            "declared_hash_valid": event.get("declared_hash_valid") is True,
            "declared_hash_matches_text": event.get("declared_hash_matches_text") is True,
            "validation_allowed": event.get("validation_allowed") is True,
            "final_key_contract_passed": event.get("final_key_contract_passed") is True,
            "final_extra_key_count": event.get("final_extra_key_count", 0),
            "final_non_string_key_count": event.get("final_non_string_key_count", 0),
            "raw_hashes_stored": False,
            "raw_text_stored": False,
        }
    }


def sanitize_result_for_artifact(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "request_id": safe_text(row.get("request_id", "")),
        "trial_case_id": safe_text(row.get("trial_case_id", "")),
        "category": safe_text(row.get("category", "")),
        "adapter_rejected": row.get("adapter_rejected") is True,
        "guarded_applied": row.get("guarded_applied") is True,
        "guard_status": safe_text(row.get("guard_status", "")),
        "feature_flag_mode": enum_audit(row.get("feature_flag_mode", ""), FEATURE_FLAG_MODES, role="artifact_flag_mode"),
        "feature_flag_error": row.get("feature_flag_error") is True,
        "server_context_accepted": row.get("server_context_accepted") is True,
        "build_adapter_request_called": row.get("build_adapter_request_called") is True,
        "adapter_release_sink_allowed": row.get("adapter_release_sink_allowed") is True,
        "internal_r1_4_release_sink_allowed": row.get("internal_r1_4_release_sink_allowed") is True,
        "answer_relevance_gate_triggered": row.get("answer_relevance_gate_triggered") is True,
        "answer_relevance_release_safe": row.get("answer_relevance_release_safe") is True,
        "pre_guard_fact_leaked": row.get("pre_guard_fact_leaked") is True,
        "old_answer_leaked": row.get("old_answer_leaked") is True,
        "user_visible_output_from_sink": row.get("user_visible_output_from_sink") is True,
        "elapsed_ms": row.get("elapsed_ms", 0),
        "error_counts": {
            "adapter_reject_reason_count": len(row.get("adapter_reject_reasons", []))
            if isinstance(row.get("adapter_reject_reasons"), list)
            else 0,
            "user_policy_error_count": len(row.get("user_policy_errors", []))
            if isinstance(row.get("user_policy_errors"), list)
            else 0,
            "server_context_error_count": len(row.get("server_context_errors", []))
            if isinstance(row.get("server_context_errors"), list)
            else 0,
            "flag_mode_error_count": len(row.get("flag_mode_errors", []))
            if isinstance(row.get("flag_mode_errors"), list)
            else 0,
            "query_binding_error_count": len(row.get("query_binding_errors", []))
            if isinstance(row.get("query_binding_errors"), list)
            else 0,
        },
        "fixture_flags": {
            "non_json_fixture_value": row.get("non_json_fixture_value") is True,
            "non_string_key_fixture": row.get("non_string_key_fixture") is True,
            "non_json_object_fixture": row.get("non_json_object_fixture") is True,
            "repr_side_channel_fixture": row.get("repr_side_channel_fixture") is True,
            "exploding_repr_fixture": row.get("exploding_repr_fixture") is True,
            "json_resource_fixture": row.get("json_resource_fixture") is True,
        },
        "answer_relevance_evaluation": sanitize_relevance_for_artifact(row.get("answer_relevance_evaluation")),
        "candidate_commit_event": sanitize_sink_event_for_artifact(row.get("candidate_commit_event"))
        if row.get("candidate_commit_event") is not None
        else None,
        "final_commit_event": sanitize_sink_event_for_artifact(row.get("final_commit_event"))
        if row.get("final_commit_event") is not None
        else None,
        "second_candidate_commit_event": sanitize_sink_event_for_artifact(row.get("second_candidate_commit_event"))
        if row.get("second_candidate_commit_event") is not None
        else None,
        "second_fallback_commit_event": sanitize_sink_event_for_artifact(row.get("second_fallback_commit_event"))
        if row.get("second_fallback_commit_event") is not None
        else None,
        "nonbool_gate_commit_event": sanitize_sink_event_for_artifact(row.get("nonbool_gate_commit_event"))
        if row.get("nonbool_gate_commit_event") is not None
        else None,
        "visible_event_count": len(row.get("visible_events", [])) if isinstance(row.get("visible_events"), list) else 0,
        "r1_4_result": row.get("r1_4_result", {}),
        "final_answer": sanitize_final_for_artifact(row.get("final_answer")),
        "user_visible_output": sanitize_visible_output_for_artifact(row.get("user_visible_output")),
        "raw_result_text_stored": False,
        "raw_identity_stored": False,
        "raw_query_stored": False,
        "raw_error_values_stored": False,
    }


def metrics(
    results: list[dict[str, Any]],
    log_rows: list[dict[str, Any]],
    latency: dict[str, Any],
    cases: list[dict[str, Any]],
    direct_adversarial: dict[str, Any],
) -> dict[str, Any]:
    final_texts = "\n".join(row.get("user_visible_output", {}).get("text", "") for row in results)
    artifact_cases = [sanitize_trial_case_for_artifact(case) for case in cases]
    audit_jsonl_text = jsonl_text(artifact_cases)
    artifact_results = [sanitize_result_for_artifact(row) for row in results]
    audit_jsonl_text += jsonl_text(artifact_results)
    audit_jsonl_text += jsonl_text(log_rows)
    artifact_serialized_line_count = sum(1 for line in audit_jsonl_text.splitlines() if line.strip())
    artifact_strict_jsonl_failures = strict_jsonl_parse_failure_count(audit_jsonl_text)
    sensitive_token_hashes = {
        sha256_bytes(token.encode(encoding))
        for token in SENSITIVE_TOKENS
        for encoding in ("utf-8", "utf-16", "utf-16le", "utf-16be")
    }
    known_unreleased_sensitive_texts = {
        f"{SENSITIVE_TOKENS[1]}: 公司允许{SENSITIVE_TOKENS[2]}。 {SENSITIVE_TOKENS[0]}",
        f"{SENSITIVE_TOKENS[1]}: {SENSITIVE_TOKENS[2]}。",
        "DANGEROUS NONBOOL GATE",
    }
    known_unreleased_sensitive_text_hashes = {
        sha256_bytes(text.encode("utf-8"))
        for text in known_unreleased_sensitive_texts
    }

    def event_count(event_name: str, *, allowed: bool | None = None) -> int:
        count = 0
        for row in results:
            for event in row.get("visible_events", []):
                if event.get("event") != event_name:
                    continue
                if allowed is not None and event.get("allowed") is not allowed:
                    continue
                count += 1
        return count

    expected_build_count = sum(
        1
        for row in results
        if not row.get("adapter_rejected")
        and row.get("feature_flag_mode") != "off"
        and not row.get("feature_flag_error")
    )
    return {
        "trial_case_count": len(results),
        "released_count": sum(1 for row in results if row.get("final_answer", {}).get("release_state") == "released"),
        "server_context_accepted_count": sum(1 for row in results if row.get("server_context_accepted")),
        "build_adapter_request_expected_count": expected_build_count,
        "build_adapter_request_called_count": sum(1 for row in results if row.get("build_adapter_request_called")),
        "build_adapter_request_missing_when_expected_count": sum(
            1
            for row in results
            if not row.get("adapter_rejected")
            and row.get("feature_flag_mode") != "off"
            and not row.get("feature_flag_error")
            and not row.get("build_adapter_request_called")
        ),
        "server_context_invalid_count": sum(1 for row in results if row.get("server_context_errors")),
        "server_context_invalid_guarded_applied_count": sum(
            1 for row in results if row.get("server_context_errors") and row.get("guarded_applied")
        ),
        "server_context_invalid_released_count": sum(
            1
            for row in results
            if row.get("server_context_errors")
            and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "user_payload_policy_rejected_count": sum(1 for row in results if row.get("user_policy_errors")),
        "user_payload_invalid_count": sum(
            1
            for row in results
            if any(str(reason).startswith("user_payload_") for reason in row.get("adapter_reject_reasons", []))
        ),
        "user_payload_invalid_guarded_applied_count": sum(
            1
            for row in results
            if any(str(reason).startswith("user_payload_") for reason in row.get("adapter_reject_reasons", []))
            and row.get("guarded_applied")
        ),
        "user_payload_invalid_released_count": sum(
            1
            for row in results
            if any(str(reason).startswith("user_payload_") for reason in row.get("adapter_reject_reasons", []))
            and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "flag_mode_invalid_count": sum(1 for row in results if row.get("flag_mode_errors")),
        "flag_mode_invalid_guarded_applied_count": sum(
            1 for row in results if row.get("flag_mode_errors") and row.get("guarded_applied")
        ),
        "flag_mode_invalid_released_count": sum(
            1
            for row in results
            if row.get("flag_mode_errors")
            and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "non_json_fixture_value_case_count": sum(1 for row in results if row.get("non_json_fixture_value")),
        "non_json_fixture_value_guarded_applied_count": sum(
            1
            for row in results
            if row.get("non_json_fixture_value") and row.get("guarded_applied")
        ),
        "non_json_fixture_value_released_count": sum(
            1
            for row in results
            if row.get("non_json_fixture_value") and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "non_string_key_fixture_case_count": sum(1 for row in results if row.get("non_string_key_fixture")),
        "non_string_key_fixture_guarded_applied_count": sum(
            1 for row in results if row.get("non_string_key_fixture") and row.get("guarded_applied")
        ),
        "non_string_key_fixture_released_count": sum(
            1
            for row in results
            if row.get("non_string_key_fixture") and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "non_json_object_fixture_case_count": sum(1 for row in results if row.get("non_json_object_fixture")),
        "non_json_object_fixture_guarded_applied_count": sum(
            1 for row in results if row.get("non_json_object_fixture") and row.get("guarded_applied")
        ),
        "non_json_object_fixture_released_count": sum(
            1
            for row in results
            if row.get("non_json_object_fixture") and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "repr_side_channel_fixture_case_count": sum(1 for row in results if row.get("repr_side_channel_fixture")),
        "repr_side_channel_fixture_guarded_applied_count": sum(
            1 for row in results if row.get("repr_side_channel_fixture") and row.get("guarded_applied")
        ),
        "repr_side_channel_fixture_released_count": sum(
            1
            for row in results
            if row.get("repr_side_channel_fixture") and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "exploding_repr_fixture_case_count": sum(1 for row in results if row.get("exploding_repr_fixture")),
        "exploding_repr_fixture_guarded_applied_count": sum(
            1 for row in results if row.get("exploding_repr_fixture") and row.get("guarded_applied")
        ),
        "exploding_repr_fixture_released_count": sum(
            1
            for row in results
            if row.get("exploding_repr_fixture") and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "json_resource_fixture_case_count": sum(1 for row in results if row.get("json_resource_fixture")),
        "json_resource_fixture_guarded_applied_count": sum(
            1 for row in results if row.get("json_resource_fixture") and row.get("guarded_applied")
        ),
        "json_resource_fixture_released_count": sum(
            1
            for row in results
            if row.get("json_resource_fixture") and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "query_binding_error_count": sum(1 for row in results if row.get("query_binding_errors")),
        "query_binding_error_guarded_applied_count": sum(
            1 for row in results if row.get("query_binding_errors") and row.get("guarded_applied")
        ),
        "query_binding_error_released_count": sum(
            1
            for row in results
            if row.get("query_binding_errors")
            and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "feature_flag_off_guarded_applied_count": sum(1 for row in results if row["category"] == "feature_flag_off" and row.get("guarded_applied")),
        "feature_flag_error_guarded_applied_count": sum(1 for row in results if row["category"] == "feature_flag_error" and row.get("guarded_applied")),
        "answer_relevance_gate_triggered_count": sum(1 for row in results if row.get("answer_relevance_gate_triggered")),
        "answer_relevance_failure_internal_r1_4_allowed_count": sum(
            1
            for row in results
            if row.get("answer_relevance_gate_triggered")
            and row.get("r1_4_result", {}).get("__r1_4_result_sanitized__", {}).get("release_sink_allowed")
        ),
        "answer_relevance_failure_adapter_release_allowed_count": sum(
            1
            for row in results
            if row.get("answer_relevance_gate_triggered")
            and row.get("adapter_release_sink_allowed")
        ),
        "answer_relevance_failure_released_count": sum(
            1
            for row in results
            if row.get("answer_relevance_gate_triggered")
            and row.get("final_answer", {}).get("release_state") == "released"
        ),
        "candidate_user_visible_mismatch_count": sum(
            1
            for row in results
            if row.get("answer_relevance_evaluation", {}).get("r1_4_user_visible_matches_candidate") is False
        ),
        "candidate_user_visible_mismatch_adapter_release_allowed_count": sum(
            1
            for row in results
            if row.get("answer_relevance_evaluation", {}).get("r1_4_user_visible_matches_candidate") is False
            and row.get("adapter_release_sink_allowed")
        ),
        "candidate_hash_mismatch_adapter_release_allowed_count": sum(
            1
            for row in results
            if row.get("answer_relevance_evaluation", {}).get("candidate_hash_matches_text") is False
            and row.get("adapter_release_sink_allowed")
        ),
        "candidate_final_extra_key_contract_failure_count": sum(
            1
            for row in results
            if (row.get("candidate_commit_event") or {}).get("final_extra_key_count", 0) > 0
        ),
        "candidate_final_extra_key_adapter_release_allowed_count": sum(
            1
            for row in results
            if (row.get("candidate_commit_event") or {}).get("final_extra_key_count", 0) > 0
            and row.get("adapter_release_sink_allowed")
        ),
        "candidate_audit_minimization_case_count": sum(
            1 for row in results if row["category"] == "candidate_audit_minimization"
        ),
        "candidate_audit_minimization_adapter_release_allowed_count": sum(
            1
            for row in results
            if row["category"] == "candidate_audit_minimization"
            and row.get("adapter_release_sink_allowed")
        ),
        "sink_audit_minimization_case_count": sum(
            1 for row in results if row["category"] == "sink_audit_minimization"
        ),
        "sink_audit_minimization_gate_commit_allowed_count": sum(
            1
            for row in results
            if row["category"] == "sink_audit_minimization"
            and (row.get("nonbool_gate_commit_event") or {}).get("allowed")
        ),
        "claim_set_mismatch_count": sum(
            1
            for row in results
            if row.get("answer_relevance_evaluation", {}).get("skipped") is False
            and row.get("answer_relevance_evaluation", {}).get("claim_ids_match") is False
        ),
        "claim_set_mismatch_adapter_release_allowed_count": sum(
            1
            for row in results
            if row.get("answer_relevance_evaluation", {}).get("skipped") is False
            and row.get("answer_relevance_evaluation", {}).get("claim_ids_match") is False
            and row.get("adapter_release_sink_allowed")
        ),
        "malformed_candidate_text_count": sum(
            1
            for row in results
            if row.get("answer_relevance_evaluation", {}).get("candidate_text_valid") is False
        ),
        "malformed_candidate_text_adapter_release_allowed_count": sum(
            1
            for row in results
            if row.get("answer_relevance_evaluation", {}).get("candidate_text_valid") is False
            and row.get("adapter_release_sink_allowed")
        ),
        "malformed_relevance_contract_count": sum(
            1
            for row in results
            if row.get("answer_relevance_evaluation", {}).get("skipped") is False
            and (
                row.get("answer_relevance_evaluation", {}).get("candidate_final_valid") is False
                or row.get("answer_relevance_evaluation", {}).get("expected_claim_ids_valid") is False
                or row.get("answer_relevance_evaluation", {}).get("visible_claim_ids_valid") is False
                or row.get("answer_relevance_evaluation", {}).get("marker_groups_valid") is False
            )
        ),
        "malformed_relevance_contract_adapter_release_allowed_count": sum(
            1
            for row in results
            if row.get("answer_relevance_evaluation", {}).get("skipped") is False
            and (
                row.get("answer_relevance_evaluation", {}).get("candidate_final_valid") is False
                or row.get("answer_relevance_evaluation", {}).get("expected_claim_ids_valid") is False
                or row.get("answer_relevance_evaluation", {}).get("visible_claim_ids_valid") is False
                or row.get("answer_relevance_evaluation", {}).get("marker_groups_valid") is False
            )
            and row.get("adapter_release_sink_allowed")
        ),
        "pre_guard_fact_attempt_count": sum(
            1
            for row in results
            for event in row.get("visible_events", [])
            if event.get("event") == "fact_text_write_attempt"
        ),
        "pre_guard_fact_leak_count": sum(1 for row in results if row.get("pre_guard_fact_leaked")),
        "untrusted_fallback_text_attempt_count": event_count("untrusted_fallback_text_attempt"),
        "untrusted_fallback_text_allowed_count": event_count("untrusted_fallback_text_attempt", allowed=True),
        "second_candidate_commit_attempt_count": sum(1 for row in results if row.get("second_candidate_commit_event")),
        "second_candidate_commit_allowed_count": sum(
            1 for row in results if (row.get("second_candidate_commit_event") or {}).get("allowed")
        ),
        "second_fallback_commit_attempt_count": sum(1 for row in results if row.get("second_fallback_commit_event")),
        "second_fallback_commit_allowed_count": sum(
            1 for row in results if (row.get("second_fallback_commit_event") or {}).get("allowed")
        ),
        "sink_second_commit_allowed_count": sum(
            1
            for row in results
            if (row.get("second_candidate_commit_event") or {}).get("allowed")
            or (row.get("second_fallback_commit_event") or {}).get("allowed")
        ),
        "nonbool_gate_argument_attempt_count": sum(1 for row in results if row.get("nonbool_gate_commit_event")),
        "nonbool_gate_argument_adapter_release_allowed_count": sum(
            1 for row in results if (row.get("nonbool_gate_commit_event") or {}).get("allowed")
        ),
        "sink_public_attribute_tamper_attempt_count": sum(1 for row in results if row.get("sink_tamper_result")),
        "sink_public_attribute_tamper_success_count": sum(
            1
            for row in results
            if row.get("sink_tamper_result")
            and not row.get("sink_tamper_result", {}).get("public_attribute_tamper_blocked")
        ),
        "sink_event_snapshot_mutation_success_count": sum(
            1
            for row in results
            if row.get("sink_tamper_result")
            and not row.get("sink_tamper_result", {}).get("event_snapshot_mutation_blocked")
        ),
        "sink_buffer_output_mismatch_count": sum(1 for row in results if not row.get("user_visible_output_from_sink")),
        "safe_fallback_bad_state_count": sum(
            1
            for row in results
            for event in row.get("visible_events", [])
            if event.get("event") == "safe_fallback_commit"
            and (
                event.get("release_state") not in {"withheld", "review_required"}
                or event.get("answer_policy") not in {"abstain", "review"}
            )
        ),
        "fallback_old_answer_leak_count": sum(1 for row in results if row.get("old_answer_leaked")),
        "sensitive_log_leak_count": 1 if log_contains_sensitive(log_rows) else 0,
        "unsalted_identifier_or_query_hash_log_leak_count": (
            1 if log_contains_unsalted_identifier_or_query_hash(results, log_rows) else 0
        ),
        "unsalted_final_hash_log_leak_count": (
            1 if log_contains_unsalted_final_hash(results, log_rows) else 0
        ),
        "log_hmac_missing_count": sum(
            1
            for row in log_rows
            if row.get("log_key_id") != LOG_HMAC_KEY_ID
            or not is_sha256_hex(row.get("principal_hmac", ""))
            or not is_sha256_hex(row.get("tenant_hmac", ""))
            or not is_sha256_hex(row.get("query_hmac", ""))
            or not is_sha256_hex(row.get("final_hmac", ""))
        ),
        "legacy_log_hash_field_count": sum(
            1
            for row in log_rows
            if "principal_hash" in row
            or "tenant_hash" in row
            or "query_sha256" in row
            or "final_sha256" in row
        ),
        "visible_sensitive_text_leak_count": sum(1 for token in SENSITIVE_TOKENS if token in final_texts),
        "sensitive_jsonl_artifact_leak_count": sum(1 for token in SENSITIVE_TOKENS if token in audit_jsonl_text),
        "known_sensitive_token_sha256_artifact_leak_count": sum(
            1 for digest in sensitive_token_hashes if digest in audit_jsonl_text
        ),
        "known_unreleased_sensitive_text_sha256_artifact_leak_count": sum(
            1 for digest in known_unreleased_sensitive_text_hashes if digest in audit_jsonl_text
        ),
        "unknown_sensitive_probe_case_count": sum(1 for row in results if row["category"] == "artifact_minimization"),
        "unknown_sensitive_probe_artifact_leak_count": sum(
            1 for probe in UNKNOWN_SENSITIVE_PROBES if probe in audit_jsonl_text
        ),
        "artifact_serialized_line_count": artifact_serialized_line_count,
        "artifact_strict_jsonl_parse_failure_count": artifact_strict_jsonl_failures,
        "direct_adversarial_self_test_failure_count": direct_adversarial.get("failure_count", 1),
        "direct_adversarial_self_test_check_count": direct_adversarial.get("check_count", 0),
        "direct_adversarial_self_test_passed": direct_adversarial.get("status") == "pass",
        "redacted_sensitive_token_marker_count": sum(
            audit_jsonl_text.count(marker) for marker in SENSITIVE_REDACTIONS.values()
        ),
        "bytes_payload_sensitive_hint_marker_count": audit_jsonl_text.count('"payload_sensitive_hint":true'),
        "raw_payload_sha256_stored_count": audit_jsonl_text.count(
            chr(34) + RAW_PAYLOAD_SHA_FIELD + chr(34) + ":true"
        ),
        "repr_sensitive_hint_marker_count": audit_jsonl_text.count('"repr_sensitive_hint":true'),
        "raw_key_repr_artifact_field_count": audit_jsonl_text.count(
            chr(34) + RAW_KEY_REPR_FIELD + chr(34) + ":"
        ),
        "raw_non_json_object_type_field_count": audit_jsonl_text.count(
            chr(34) + NON_JSON_OBJECT_MARKER + chr(34) + ":{" + chr(34) + "type" + chr(34) + ":"
        ),
        "raw_final_extra_trace_field_count": sum(
            audit_jsonl_text.count(chr(34) + field + chr(34) + ":")
            for field in EXTRA_FINAL_TRACE_FIELDS
        ),
        "raw_final_text_artifact_field_count": audit_jsonl_text.count(chr(34) + "final_text" + chr(34) + ":"),
        "raw_visible_text_artifact_field_count": audit_jsonl_text.count(chr(34) + "text" + chr(34) + ":"),
        "raw_query_artifact_field_count": (
            audit_jsonl_text.count(chr(34) + "query" + chr(34) + ":")
            + audit_jsonl_text.count(chr(34) + "user_text" + chr(34) + ":")
        ),
        "raw_identity_artifact_field_count": (
            audit_jsonl_text.count(chr(34) + "user_id" + chr(34) + ":")
            + audit_jsonl_text.count(chr(34) + "tenant_id" + chr(34) + ":")
            + audit_jsonl_text.count(chr(34) + "principal_id" + chr(34) + ":")
        ),
        "raw_source_ref_artifact_field_count": (
            audit_jsonl_text.count(chr(34) + "source_ref" + chr(34) + ":")
            + audit_jsonl_text.count(chr(34) + "anchor_ref" + chr(34) + ":")
        ),
        "json_safe_resource_limit_marker_count": audit_jsonl_text.count('"__json_safe_resource_limit__":'),
        "json_safe_cycle_marker_count": audit_jsonl_text.count('"kind":"cycle"'),
        "json_safe_depth_limit_marker_count": audit_jsonl_text.count('"kind":"depth_limit"'),
        "json_safe_item_limit_marker_count": audit_jsonl_text.count('"kind":"item_limit"'),
        "json_safe_truncated_string_marker_count": audit_jsonl_text.count('"__json_safe_truncated_string__":'),
        "json_safe_truncated_raw_sample_field_count": audit_jsonl_text.count(
            chr(34) + "raw_sample" + chr(34) + ":"
        ),
        "json_safe_truncated_sample_text_field_count": audit_jsonl_text.count(
            chr(34) + "sample_text" + chr(34) + ":"
        ),
        "high_risk_released_count": sum(1 for row in results if row["category"] == "high_risk_fallback" and row.get("final_answer", {}).get("release_state") == "released"),
        "latency_p95_ms": latency["p95_ms"],
        "latency_p99_ms": latency["p99_ms"],
        "latency_budget_pass": latency["p95_ms"] <= 150.0,
    }


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((pct / 100.0) * (len(ordered) - 1)))))
    return ordered[index]


def run_latency(stack: dict[str, Any], trial_case: dict[str, Any], output_dir: Path, *, count: int) -> dict[str, Any]:
    elapsed: list[float] = []
    failures = 0
    for index in range(count):
        case = copy.deepcopy(trial_case)
        case["case_id"] = f"latency-{index:05d}"
        result = process_adapter_case(stack, case, output_dir)
        elapsed.append(result["elapsed_ms"])
        if result.get("final_answer", {}).get("release_state") != "released":
            failures += 1
    return {
        "sample_count": count,
        "failure_count": failures,
        "samples_ms": [round(value, 6) for value in elapsed],
        "avg_ms": round(sum(elapsed) / len(elapsed), 6) if elapsed else 0.0,
        "p95_ms": round(percentile(elapsed, 95), 6),
        "p99_ms": round(percentile(elapsed, 99), 6),
        "budget": "local adapter p95 <= 150ms; not production end-to-end SLO",
    }


def stress_signature(result: dict[str, Any]) -> dict[str, Any]:
    final = result.get("final_answer", {})
    return {
        "category": result.get("category", ""),
        "adapter_rejected": result.get("adapter_rejected") is True,
        "guarded_applied": result.get("guarded_applied") is True,
        "guard_status": result.get("guard_status", ""),
        "release_sink_allowed": result.get("release_sink_allowed") is True,
        "release_state": final.get("release_state", ""),
        "answer_policy": final.get("answer_policy", ""),
        "old_answer_leaked": result.get("old_answer_leaked") is True,
        "pre_guard_fact_leaked": result.get("pre_guard_fact_leaked") is True,
        "user_visible_output_from_sink": result.get("user_visible_output_from_sink") is True,
    }


def stress_case_has_sensitive_visible_text(result: dict[str, Any]) -> bool:
    visible = result.get("user_visible_output", {}).get("text", "")
    return isinstance(visible, str) and any(token in visible for token in SENSITIVE_TOKENS)


def stress_self_test(
    stack: dict[str, Any],
    cases: list[dict[str, Any]],
    output_dir: Path,
    *,
    quick: bool,
) -> dict[str, Any]:
    case_by_id = {case["case_id"]: case for case in cases}
    pure_ids = [
        "trial-002-policy-injection",
        "trial-004-flag-off",
    ]
    guarded_ids = [
        "trial-001-happy-release",
        "trial-006-answer-relevance-negative",
        "trial-009-guard-error-fallback",
    ]
    pure_iterations = 200 if quick else 20000
    parallel_iterations = 100 if quick else 12000
    guarded_iterations = 5 if quick else 100
    stress_dir = output_dir / "_stress_workspace"
    failure_samples: list[dict[str, Any]] = []
    signature_by_plan: dict[str, str] = {}
    sequential_count = 0
    parallel_count = 0

    def run_one(base_id: str, case_id: str, target_dir: Path) -> dict[str, Any]:
        case = copy.deepcopy(case_by_id[base_id])
        case["case_id"] = case_id
        return process_adapter_case(stack, case, target_dir)

    def record_result(plan: str, index: int, result: dict[str, Any]) -> None:
        signature = stable_json(stress_signature(result))
        expected = signature_by_plan.setdefault(plan, signature)
        errors = []
        if signature != expected:
            errors.append("signature_drift")
        if result.get("old_answer_leaked"):
            errors.append("old_answer_leaked")
        if result.get("pre_guard_fact_leaked"):
            errors.append("pre_guard_fact_leaked")
        if not result.get("user_visible_output_from_sink"):
            errors.append("user_visible_output_not_from_sink")
        if stress_case_has_sensitive_visible_text(result):
            errors.append("sensitive_visible_text")
        if result.get("category") == "happy_release" and not result.get("release_sink_allowed"):
            errors.append("happy_release_not_released")
        if result.get("category") in {"server_envelope", "feature_flag_off", "answer_relevance", "fallback"}:
            final = result.get("final_answer", {})
            if final.get("release_state") == "released":
                errors.append("blocked_category_released")
        if errors and len(failure_samples) < 20:
            failure_samples.append({
                "plan": plan,
                "index": index,
                "errors": errors,
                "signature": stress_signature(result),
            })

    try:
        mkdir_no_symlink(stress_dir)
        for base_id in pure_ids:
            plan = f"sequential:{base_id}"
            for index in range(pure_iterations):
                result = run_one(base_id, f"stress-seq-{base_id}-{index:05d}", stress_dir)
                record_result(plan, index, result)
                sequential_count += 1
        for base_id in guarded_ids:
            plan_dir = stress_dir / base_id
            mkdir_no_symlink(plan_dir)
            plan = f"guarded:{base_id}"
            for index in range(guarded_iterations):
                result = run_one(base_id, f"stress-guarded-{base_id}-{index:05d}", plan_dir)
                record_result(plan, index, result)
                sequential_count += 1

        parallel_inputs = [
            (pure_ids[index % len(pure_ids)], index)
            for index in range(parallel_iterations)
        ]

        def run_parallel(item: tuple[str, int]) -> tuple[int, dict[str, Any]]:
            base_id, index = item
            result = run_one(base_id, f"stress-parallel-{base_id}-{index:05d}", stress_dir)
            return index, result

        with ThreadPoolExecutor(max_workers=8) as pool:
            for index, result in pool.map(run_parallel, parallel_inputs):
                plan = f"parallel:{parallel_inputs[index][0]}"
                record_result(plan, index, result)
                parallel_count += 1
    finally:
        if exists_or_symlink(stress_dir):
            stress_dir.unlink() if stress_dir.is_symlink() or stress_dir.is_file() else shutil.rmtree(stress_dir)

    failure_count = len(failure_samples)
    cleanup_ok = not exists_or_symlink(stress_dir)
    return {
        "status": "pass" if failure_count == 0 and cleanup_ok else "fail",
        "sequential_count": sequential_count,
        "parallel_count": parallel_count,
        "total_count": sequential_count + parallel_count,
        "failure_count": failure_count,
        "cleanup_ok": cleanup_ok,
        "stress_workspace_exists_after": exists_or_symlink(stress_dir),
        "signature_plan_count": len(signature_by_plan),
        "failure_samples": failure_samples,
        "coverage": {
            "pure_case_ids": pure_ids,
            "guarded_case_ids": guarded_ids,
            "parallel_case_ids": pure_ids,
            "guarded_iterations_per_case": guarded_iterations,
            "pure_iterations_per_case": pure_iterations,
            "parallel_iterations_total": parallel_iterations,
        },
    }


def direct_adversarial_self_test() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add_check(name: str, passed: bool, details: dict[str, Any] | None = None) -> None:
        checks.append({
            "name": name,
            "passed": bool(passed),
            "details": details or {},
        })

    sink = AdapterReleaseSink()
    allowed_events: list[dict[str, Any]] = []
    allowed_lock = threading.Lock()

    def concurrent_candidate(index: int) -> None:
        text = f"concurrent-safe-output-{index}"
        candidate = {
            "final_text": text,
            "final_sha256": sha256_text(text),
            "release_state": "released",
            "answer_policy": "direct",
            "atomic_release_phase": "committed_final",
            "visible_claim_ids": ["c1"],
        }
        event = sink.commit_candidate(candidate, guard_passed=True, relevance_passed=True)
        with allowed_lock:
            allowed_events.append({
                "index": index,
                "allowed": event.get("allowed") is True,
                "blocked_reason": event.get("blocked_reason", ""),
            })

    threads = [threading.Thread(target=concurrent_candidate, args=(index,)) for index in range(64)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    allowed_count = sum(1 for event in allowed_events if event["allowed"])
    add_check(
        "concurrent_single_sink_write_once",
        allowed_count == 1 and sink.sealed,
        {"attempt_count": len(allowed_events), "allowed_count": allowed_count, "sink_sealed": sink.sealed},
    )

    committed_before = sink.committed_sha256
    buffer_before = sink.user_visible_buffer
    dangerous_text = "direct-adversarial-second-candidate"
    second_candidate = {
        "final_text": dangerous_text,
        "final_sha256": sha256_text(dangerous_text),
        "release_state": "released",
        "answer_policy": "direct",
        "atomic_release_phase": "committed_final",
        "visible_claim_ids": ["c1"],
    }
    second_candidate_event = sink.commit_candidate(second_candidate, guard_passed=True, relevance_passed=True)
    _, second_fallback_event = sink.commit_safe_fallback("adapter_rejected")
    fact_event = sink.attempt_fact_text("direct-adversarial-fact-write", "after_commit")
    add_check(
        "sealed_sink_rejects_later_candidate_fallback_and_fact_writes",
        (
            second_candidate_event.get("allowed") is False
            and second_fallback_event.get("allowed") is False
            and fact_event.get("allowed") is False
            and sink.committed_sha256 == committed_before
            and sink.user_visible_buffer == buffer_before
        ),
        {
            "second_candidate_allowed": second_candidate_event.get("allowed") is True,
            "second_fallback_allowed": second_fallback_event.get("allowed") is True,
            "fact_write_allowed": fact_event.get("allowed") is True,
            "committed_hash_unchanged": sink.committed_sha256 == committed_before,
            "buffer_unchanged": sink.user_visible_buffer == buffer_before,
        },
    )

    committed_copy = sink.committed_final
    if committed_copy is not None:
        committed_copy["final_text"] = "mutated-copy-should-not-change-sink"
    add_check(
        "committed_final_property_returns_copy",
        sink.user_visible_buffer == buffer_before,
        {"buffer_hash": sha256_text(sink.user_visible_buffer), "committed_hash": sink.committed_sha256},
    )

    candidate_text = "alpha beta"
    relevance_result = {
        "user_visible_output": {"text": candidate_text, "sha256": sha256_text(candidate_text)},
        "r1_3_result": {"alignment": {"alignment_id": "align-direct-adversarial"}},
    }
    relevance_case = {
        "expected_alignment_id": "align-direct-adversarial",
        "expected_claim_ids": ["c1"],
        "expected_marker_groups": [["alpha"], ["beta"]],
    }
    extra_claim_final = {
        "final_text": candidate_text,
        "final_sha256": sha256_text(candidate_text),
        "release_state": "released",
        "visible_claim_ids": ["c1", "extra-unrelated-claim"],
    }
    extra_claim_relevance = answer_relevance_evaluation(relevance_result, relevance_case, extra_claim_final)
    hash_bad_final = {
        "final_text": candidate_text,
        "final_sha256": "0" * 64,
        "release_state": "released",
        "visible_claim_ids": ["c1"],
    }
    hash_bad_relevance = answer_relevance_evaluation(relevance_result, relevance_case, hash_bad_final)
    add_check(
        "relevance_rejects_extra_visible_claim",
        extra_claim_relevance.get("passed") is False and extra_claim_relevance.get("claim_ids_match") is False,
        {
            "passed": extra_claim_relevance.get("passed") is True,
            "claim_ids_match": extra_claim_relevance.get("claim_ids_match") is True,
        },
    )
    add_check(
        "relevance_rejects_candidate_hash_mismatch",
        hash_bad_relevance.get("passed") is False and hash_bad_relevance.get("candidate_hash_matches_text") is False,
        {
            "passed": hash_bad_relevance.get("passed") is True,
            "candidate_hash_matches_text": hash_bad_relevance.get("candidate_hash_matches_text") is True,
        },
    )

    cyclic: list[Any] = []
    cyclic.append(cyclic)
    cyclic_json = stable_json(json_safe({"cycle": cyclic}))
    add_check(
        "json_safe_serializes_cycles_without_crashing",
        '"kind":"cycle"' in cyclic_json and "direct-adversarial" not in cyclic_json,
        {"cycle_marker_present": '"kind":"cycle"' in cyclic_json, "serialized_length": len(cyclic_json)},
    )

    deep_value: Any = "leaf"
    for _index in range(JSON_SAFE_MAX_DEPTH + 5):
        deep_value = [deep_value]
    deep_json = stable_json(json_safe({"deep": deep_value}))
    add_check(
        "json_safe_serializes_deep_values_with_depth_marker",
        '"kind":"depth_limit"' in deep_json,
        {"depth_marker_present": '"kind":"depth_limit"' in deep_json, "serialized_length": len(deep_json)},
    )

    long_sensitive_text = (SENSITIVE_TOKENS[0] + "-") * (JSON_SAFE_MAX_STRING_CHARS + 2)
    long_json = stable_json(json_safe({"long": long_sensitive_text}))
    add_check(
        "json_safe_truncates_long_sensitive_strings_without_raw_sample",
        (
            "__json_safe_truncated_string__" in long_json
            and SENSITIVE_TOKENS[0] not in long_json
            and '"raw_sample"' not in long_json
            and '"sample_text"' not in long_json
        ),
        {
            "truncation_marker_present": "__json_safe_truncated_string__" in long_json,
            "sensitive_token_present": SENSITIVE_TOKENS[0] in long_json,
            "raw_sample_present": '"raw_sample"' in long_json,
            "sample_text_present": '"sample_text"' in long_json,
        },
    )

    nonfinite_json = stable_json(json_safe({"nan": math.nan, "inf": math.inf, "neg_inf": -math.inf}))
    add_check(
        "json_safe_converts_nonfinite_floats_to_markers",
        (
            '"__non_json_float__":"nan"' in nonfinite_json
            and '"__non_json_float__":"inf"' in nonfinite_json
            and '"__non_json_float__":"-inf"' in nonfinite_json
        ),
        {"serialized": nonfinite_json},
    )

    unsafe_zip_names = [
        "../escape.txt",
        "safe/../escape.txt",
        "safe//double-empty.txt",
        "/absolute.txt",
        "C:/windows-drive.txt",
        "safe\\backslash.txt",
        "safe/./dot.txt",
        "safe/\nnewline.txt",
        "",
    ]
    safe_zip_names = ["CONTRACT.md", "provenance/vaks_supervised_trial_adapter_r1_5.py"]
    unsafe_rejected = all(not zip_entry_name_is_safe(name) for name in unsafe_zip_names)
    safe_accepted = all(zip_entry_name_is_safe(name) for name in safe_zip_names)
    add_check(
        "zip_entry_name_guard_rejects_traversal_and_absolute_forms",
        unsafe_rejected and safe_accepted,
        {
            "unsafe_rejected": unsafe_rejected,
            "safe_accepted": safe_accepted,
            "unsafe_case_count": len(unsafe_zip_names),
            "safe_case_count": len(safe_zip_names),
        },
    )

    failure_count = sum(1 for check in checks if not check["passed"])
    return {
        "schema_version": "r1.5-direct-adversarial-self-test",
        "status": "pass" if failure_count == 0 else "fail",
        "failure_count": failure_count,
        "check_count": len(checks),
        "checks": checks,
    }


def summary(
    metrics_row: dict[str, Any],
    deps: dict[str, Any],
    *,
    append_only_self_test_status: str | None = None,
) -> dict[str, Any]:
    hard_zero_keys = [
        "feature_flag_off_guarded_applied_count",
        "feature_flag_error_guarded_applied_count",
        "build_adapter_request_missing_when_expected_count",
        "server_context_invalid_guarded_applied_count",
        "server_context_invalid_released_count",
        "user_payload_invalid_guarded_applied_count",
        "user_payload_invalid_released_count",
        "flag_mode_invalid_guarded_applied_count",
        "flag_mode_invalid_released_count",
        "non_json_fixture_value_guarded_applied_count",
        "non_json_fixture_value_released_count",
        "non_string_key_fixture_guarded_applied_count",
        "non_string_key_fixture_released_count",
        "non_json_object_fixture_guarded_applied_count",
        "non_json_object_fixture_released_count",
        "repr_side_channel_fixture_guarded_applied_count",
        "repr_side_channel_fixture_released_count",
        "exploding_repr_fixture_guarded_applied_count",
        "exploding_repr_fixture_released_count",
        "json_resource_fixture_guarded_applied_count",
        "json_resource_fixture_released_count",
        "query_binding_error_guarded_applied_count",
        "query_binding_error_released_count",
        "answer_relevance_failure_adapter_release_allowed_count",
        "answer_relevance_failure_released_count",
        "candidate_user_visible_mismatch_adapter_release_allowed_count",
        "candidate_hash_mismatch_adapter_release_allowed_count",
        "candidate_final_extra_key_adapter_release_allowed_count",
        "candidate_audit_minimization_adapter_release_allowed_count",
        "sink_audit_minimization_gate_commit_allowed_count",
        "claim_set_mismatch_adapter_release_allowed_count",
        "malformed_candidate_text_adapter_release_allowed_count",
        "malformed_relevance_contract_adapter_release_allowed_count",
        "pre_guard_fact_leak_count",
        "untrusted_fallback_text_allowed_count",
        "second_candidate_commit_allowed_count",
        "second_fallback_commit_allowed_count",
        "sink_second_commit_allowed_count",
        "nonbool_gate_argument_adapter_release_allowed_count",
        "sink_public_attribute_tamper_success_count",
        "sink_event_snapshot_mutation_success_count",
        "sink_buffer_output_mismatch_count",
        "safe_fallback_bad_state_count",
        "fallback_old_answer_leak_count",
        "sensitive_log_leak_count",
        "unsalted_identifier_or_query_hash_log_leak_count",
        "unsalted_final_hash_log_leak_count",
        "log_hmac_missing_count",
        "legacy_log_hash_field_count",
        "visible_sensitive_text_leak_count",
        "sensitive_jsonl_artifact_leak_count",
        "known_sensitive_token_sha256_artifact_leak_count",
        "known_unreleased_sensitive_text_sha256_artifact_leak_count",
        "unknown_sensitive_probe_artifact_leak_count",
        "artifact_strict_jsonl_parse_failure_count",
        "direct_adversarial_self_test_failure_count",
        "raw_payload_sha256_stored_count",
        "raw_key_repr_artifact_field_count",
        "raw_non_json_object_type_field_count",
        "raw_final_extra_trace_field_count",
        "raw_final_text_artifact_field_count",
        "raw_visible_text_artifact_field_count",
        "raw_query_artifact_field_count",
        "raw_identity_artifact_field_count",
        "raw_source_ref_artifact_field_count",
        "json_safe_truncated_raw_sample_field_count",
        "json_safe_truncated_sample_text_field_count",
        "stress_workspace_exists_after",
        "source_static_disallowed_import_count",
        "source_static_banned_import_count",
        "high_risk_released_count",
    ]
    hard_zero_pass = all(metrics_row.get(key) == 0 for key in hard_zero_keys)
    required_stress_count = 500 if metrics_row.get("stress_quick_mode") else 50000
    stress_gate_pass = (
        metrics_row.get("stress_self_test_passed") is True
        and metrics_row.get("stress_total_count", 0) >= required_stress_count
    )
    source_static_gate_pass = (
        metrics_row.get("source_static_import_audit_passed") is True
        and metrics_row.get("source_static_import_file_count", 0) >= 5
    )
    positive_pass = (
        metrics_row.get("user_payload_policy_rejected_count", 0) >= 1
        and metrics_row.get("server_context_invalid_count", 0) >= 1
        and metrics_row.get("user_payload_invalid_count", 0) >= 1
        and metrics_row.get("flag_mode_invalid_count", 0) >= 1
        and metrics_row.get("non_json_fixture_value_case_count", 0) >= 4
        and metrics_row.get("non_string_key_fixture_case_count", 0) >= 2
        and metrics_row.get("non_json_object_fixture_case_count", 0) >= 9
        and metrics_row.get("repr_side_channel_fixture_case_count", 0) >= 2
        and metrics_row.get("exploding_repr_fixture_case_count", 0) >= 2
        and metrics_row.get("json_resource_fixture_case_count", 0) >= 5
        and metrics_row.get("unknown_sensitive_probe_case_count", 0) >= 2
        and metrics_row.get("artifact_serialized_line_count", 0) > 0
        and metrics_row.get("direct_adversarial_self_test_check_count", 0) >= 10
        and metrics_row.get("direct_adversarial_self_test_passed") is True
        and stress_gate_pass
        and source_static_gate_pass
        and metrics_row.get("query_binding_error_count", 0) >= 1
        and metrics_row.get("answer_relevance_gate_triggered_count", 0) >= 1
        and metrics_row.get("answer_relevance_failure_internal_r1_4_allowed_count", 0) >= 1
        and metrics_row.get("candidate_user_visible_mismatch_count", 0) >= 1
        and metrics_row.get("candidate_final_extra_key_contract_failure_count", 0) >= 1
        and metrics_row.get("candidate_audit_minimization_case_count", 0) >= 2
        and metrics_row.get("sink_audit_minimization_case_count", 0) >= 2
        and metrics_row.get("claim_set_mismatch_count", 0) >= 1
        and metrics_row.get("malformed_candidate_text_count", 0) >= 1
        and metrics_row.get("malformed_relevance_contract_count", 0) >= 3
        and metrics_row.get("pre_guard_fact_attempt_count", 0) >= 1
        and metrics_row.get("untrusted_fallback_text_attempt_count", 0) >= 1
        and metrics_row.get("second_candidate_commit_attempt_count", 0) >= 2
        and metrics_row.get("second_fallback_commit_attempt_count", 0) >= 1
        and metrics_row.get("nonbool_gate_argument_attempt_count", 0) >= 2
        and metrics_row.get("sink_public_attribute_tamper_attempt_count", 0) >= 1
        and metrics_row.get("legacy_log_hash_field_count") == 0
        and metrics_row.get("log_hmac_missing_count") == 0
        and metrics_row.get("released_count", 0) >= 2
        and metrics_row.get("latency_budget_pass") is True
    )
    append_only_self_test_pass = append_only_self_test_status in {None, "not_run", "pass"}
    status = (
        "pass"
        if hard_zero_pass
        and positive_pass
        and deps.get("status") == "pass"
        and append_only_self_test_pass
        else "fail"
    )
    return {
        "schema_version": "r1.5-supervised-trial-adapter-preflight",
        "status": status,
        "supervised_trial_adapter_recommendation": (
            "eligible_for_one_account_low_risk_supervised_enforce_trial" if status == "pass" else "not_ready"
        ),
        "canary_recommendation": "not_evaluated_run_supervised_trial_first",
        "hard_zero_keys": hard_zero_keys,
        "hard_zero_pass": hard_zero_pass,
        "positive_gate_pass": positive_pass,
        "dependency_pass": deps.get("status") == "pass",
        "stress_gate_pass": stress_gate_pass,
        "required_stress_count": required_stress_count,
        "source_static_gate_pass": source_static_gate_pass,
        "append_only_self_test_status": append_only_self_test_status or "not_run",
        "append_only_self_test_pass": append_only_self_test_pass,
        "metrics": metrics_row,
        "not_proven": [
            "production_runtime",
            "canary_ready",
            "enterprise_full_enforce",
            "real_iam_provider",
            "real_feature_flag_provider",
            "live_llm_quality",
            "live_retrieval_quality",
            "general_natural_language_semantic_relevance",
            "production_latency_slo",
            "reviewed_truth",
            "promotion",
            "action_readiness",
        ],
    }


def contract_md() -> str:
    return """# R1.5 Supervised Trial Adapter Preflight

This sandbox tests the real trial adapter risks that remain after R1.4:

- server-constructed trusted request envelope;
- user payload and trusted runtime context type validation before guarded path;
- user payload allowlist: only query, query_sha256, and client_request_id are
  accepted;
- user query hash must be valid and match the user query when supplied;
- trusted runtime context allowlist and feature flag mode enum validation before
  guarded path;
- trusted runtime context values are restricted to the one-account low-risk
  supervised trial allowlist;
- user query, trusted query, trusted query hash, and feature flag mode must bind
  consistently before guarded path;
- adapter rejection reason codes are stable categories and do not include raw
  rejected field values;
- non-standard JSON values such as NaN and Infinity in fixtures are rejected by
  the adapter and recorded with safe audit markers rather than emitted as
  non-standard JSON;
- non-string object keys in fixtures are rejected by the adapter and recorded
  as typed audit entries so key collisions cannot hide input evidence;
- non-string keys whose repr fails are still rejected and recorded with safe
  repr-unavailable metadata rather than crashing validation;
- non-JSON values such as bytes, sets, and arbitrary objects are rejected by
  the adapter and recorded with safe metadata rather than raw repr/body text;
- JSONL audit artifacts redact synthetic sensitive test strings while keeping
  explicit redaction markers for reviewability;
- JSONL audit artifacts redact sensitive dictionary keys and convert
  redaction-induced key collisions into typed entries instead of overwriting;
- bytes/bytearray audit metadata uses a structural fingerprint derived from
  type, length, and a sensitive-hint flag, never a raw payload SHA256, so
  encoded sensitive values cannot become enumerable audit fingerprints;
- non-string key repr and custom object type names are recorded only as safe
  metadata, not as raw repr/type strings;
- JSONL audit serialization has explicit depth, node, item-count, long-string,
  and cycle markers so malicious fixture structure cannot crash bundle
  generation or expand without bound;
- oversized strings are represented without storing a raw leading text fragment,
  preventing truncation records from leaking unknown sensitive text;
- feature flag off / error behavior;
- adapter-level ReleaseSink after relevance and before user-visible release;
- write-once / sealed adapter ReleaseSink after the first successful commit;
- direct adversarial self-test for same-sink concurrent candidate commits,
  post-commit candidate/fallback/fact write attempts, copied committed-final
  mutation, extra visible claim rejection, and candidate hash mismatch;
- direct adversarial self-test for audit serialization cycles, deep nesting,
  long sensitive strings, and non-finite floats;
- direct adversarial self-test for ZIP entry name safety, including traversal,
  absolute path, Windows drive path, backslash, dot-segment, empty-segment, and
  control-character cases;
- public sink state is exposed as read-only properties, not mutable release state;
- Guard and relevance commit gates require strict boolean `true`, not truthy
  strings or numbers;
- answer relevance gate on the exact candidate final before the adapter release commit;
- R1.4 final/user-visible coherence before adapter commit;
- candidate final envelopes must use the allowlisted final-answer fields only;
  extra debug/trace fields fail closed and are not copied into audit artifacts;
- exact visible claim-set matching for the fixture contract;
- malformed candidate final text is structurally rejected, not released;
- malformed relevance contract fields such as non-list claim ids, unhashable
  claim ids, invalid marker groups, or non-object candidate finals are
  structurally rejected, not released;
- duplicate, control-character, or whitespace-padded claim ids are
  structurally rejected, not released;
- no fact text before Guard through the same adapter sink;
- fallback is generated from adapter-owned allowlisted templates only;
- user-visible output is read only from the adapter sink buffer;
- logs do not contain sensitive raw text, unsalted principal/tenant SHA256,
  raw query SHA256, or raw final-answer SHA256; sandbox logs use HMAC-shaped
  identifiers;
- append-only package generation treats pre-existing directories, ZIPs,
  sidecars, artifacts, and symlinks as blockers;
- output directory enforcement rejects raw, wiki, Obsidian, sibling-prefix,
  bad-name, and control-character output targets before creating directories;
- local stress self-test repeatedly exercises adapter rejection, feature-flag
  off, guarded release, relevance failure, Guard error fallback, and parallel
  pure-gate paths;
- stress temporary workspaces must be removed before packaging and must not
  appear in the review directory or ZIP;
- source import audit checks this runner and frozen local dependencies for
  allowlisted stdlib imports and banned network/DB/LLM/client imports;
- local adapter latency is measured.

It supports only a one-account, low-risk, supervised internal enforce trial.
It does not approve Canary or production rollout.
"""


def limits_md() -> str:
    return """# Limits

- Offline, stdlib-only, sandbox-only.
- No live IAM, live feature flag service, live LLM, live retrieval, DB, API,
  service, network call, Obsidian write, wiki write, raw write, or Truth Core write.
- Trusted runtime context must carry `trusted_context_origin=server_adapter`,
  `iam_subject_verified=true`, and `feature_flag_resolved_by=server_flag_resolver`.
- User payload must be an object and may only contain query, query_sha256, and
  client_request_id. Those fields must be strings when present. Trusted runtime
  context must be an object with only allowlisted fields, and principal/tenant/
  mode/risk/domain/flag fields must be strings where applicable.
- User query, client request id, and trusted runtime fields must be within
  bounded lengths and must not contain control, surrogate, or format
  characters. User-provided query_sha256 must be valid SHA256 hex and match the
  query.
- The bounded trial allowlist is one internal principal and tenant, low risk,
  orientation/source_inspection, and general/source_lookup domains. Action and
  high-risk requests fail closed at the adapter preflight.
- Feature flag mode must be either `off` or `enforce`.
- Answer relevance is checked with frozen alignment id, expected claim ids, and
  marker groups against the exact candidate final. This is not a general
  semantic relevance model.
- Adapter safe fallback text is generated internally from allowlisted templates;
  callers cannot pass arbitrary fallback bodies.
- Adapter candidate commit accepts only a narrow final-answer envelope. Unknown
  candidate final fields are treated as a schema failure, not as metadata to
  preserve.
- Adapter rejection reason codes should be treated as categories; raw rejected
  values are not embedded in the reason code.
- Trial logs use deterministic HMAC-shaped identifiers with a sandbox key so
  this bundle can be reproduced. Production must use secret runtime key
  material; this sandbox does not prove production log-key management.
- JSONL audit artifacts redact synthetic sensitive test strings while retaining
  explicit redaction markers. The provenance source copy remains executable
  review evidence and may contain synthetic test-token construction logic.
- JSONL audit artifact keys are also redacted. If redaction would make two keys
  collide, the object is recorded as typed entries rather than a normal JSON
  object so evidence is not silently overwritten.
- JSONL audit artifacts must not store raw `repr()` output or raw custom object
  type names. They record a safe type category, repr length, and a sensitive
  hint flag instead.
- If an object's `repr()` is unavailable or raises, the audit record must stay
  structured and fail closed without emitting object text.
- JSONL audit serialization is bounded. Cycles, deep nesting, oversized
  collections, and oversized strings are represented by explicit resource-limit
  or truncation markers rather than by unbounded recursion or full expansion.
- The direct adversarial self-test exercises JSON serialization edge cases
  independently of the fixed trial fixtures.
- The local stress self-test is still an in-process sandbox test. It does not
  represent real IAM, network, live retrieval, live LLM, or production load.
- Source import audit is static and import-level. It can catch direct banned
  imports, but it is not a runtime firewall or production egress control.
- Stress workspaces are temporary scratch and must not become review evidence;
  bundle verification fails if `_stress_workspace` artifacts or ZIP entries are
  present.
- Oversized string markers store length and a structural fingerprint only; they
  do not store raw leading text fragments.
- JSONL artifact writing converts non-standard floats such as NaN and Infinity
  into explicit audit markers. They remain invalid request values and must not
  enter guarded release.
- JSONL artifact candidates are strict-parsed before summary pass is granted,
  rejecting non-standard JSON constants such as raw NaN or Infinity.
- JSONL artifact writing converts objects with non-string keys or converted-key
  collisions into explicit typed entries. They remain invalid request values
  and must not enter guarded release.
- JSONL artifact writing records bytes/bytearray by length, a
  payload_sensitive_hint flag, and a structural fingerprint that does not hash
  raw payload bytes. It must not store raw sensitive-token SHA256 values as an
  audit side channel. Sets are recorded as typed entries, and arbitrary objects
  by type only. Raw object repr/body text must not be emitted.
- The strict JSONL parse gate covers the generated trial case, result, and log
  audit rows. It is an artifact integrity gate, not a production API contract.
- The adapter sink buffer is the sole user-visible output source in this
  sandbox.
- The adapter sink is write-once: after a successful candidate or fallback
  commit, later candidate/fallback commits and fact-text writes must not change
  the buffer.
- The direct adversarial self-test is still a local method-level test. It
  exercises concurrent calls inside one Python process, not distributed
  cross-process release coordination.
- Candidate commit requires `guard_passed is true` and
  `relevance_passed is true`; truthy non-boolean values must fail closed.
- Public sink state and event snapshots are read-only views in this sandbox;
  mutating a returned event snapshot must not change internal sink state.
- Candidate final text must be a string and must match its SHA256 before release.
- Candidate final, visible claim ids, expected claim ids, and marker groups must
  be structurally valid before relevance can pass.
- Claim ids must be unique, trimmed, non-empty strings without control
  characters.
- Latency is local adapter path latency, not production end-to-end latency.
- Review bundle output paths, ZIP paths, SHA256 sidecar paths, and individual
  artifact paths are append-only; pre-existing symlinks are treated as
  pre-existing paths.
- Bundle output must stay under `outputs/review` with an allowlisted bundle
  name. The append-only self-test probes forbidden raw/wiki/Obsidian and
  sibling-prefix paths and requires rejection before directory creation.
- Bundle self-test verifies ZIP sidecar SHA256, ZIP integrity, duplicate entry
  count, unsafe entry names, fixed ZIP timestamps/compression, entry set
  equality with the output directory, and entry hash equality with directory
  artifacts.
- Append-only self-test also runs tamper negative controls for artifact hash
  modification, missing artifact, extra artifact, ZIP SHA256 sidecar
  modification, sidecar format mismatch, unsafe ZIP entry injection, duplicate
  ZIP entry injection, and ZIP entry content mismatch.
- ZIP entry name safety is also tested with explicit negative controls for
  traversal, absolute, Windows-drive, backslash, dot-segment, empty-segment, and
  control-character forms.
- Trial approval is limited to one allowlisted internal account and low-risk
  orientation/source_inspection.
"""


def create_zip(output_dir: Path) -> dict[str, str]:
    zip_path = output_dir.with_suffix(".zip")
    sha_path = Path(str(zip_path) + ".sha256")
    if exists_or_symlink(zip_path):
        raise FileExistsError(f"ZIP already exists: {zip_path}")
    if exists_or_symlink(sha_path):
        raise FileExistsError(f"SHA256 sidecar already exists: {sha_path}")
    fd = os.open(zip_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    try:
        with os.fdopen(fd, "wb") as handle:
            with zipfile.ZipFile(handle, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for path in sorted(output_dir.rglob("*"), key=lambda item: rel(item, output_dir)):
                    if path.is_symlink():
                        raise ValueError(f"Symlink artifact is not allowed in ZIP: {path}")
                    if not path.is_file():
                        continue
                    info = zipfile.ZipInfo(rel(path, output_dir))
                    info.date_time = (2026, 6, 24, 0, 0, 0)
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, path.read_bytes())
    except Exception:
        try:
            zip_path.unlink()
        except OSError:
            pass
        raise
    digest = sha256_bytes(zip_path.read_bytes())
    write_lf(sha_path, f"{digest}  {zip_path.name}\n")
    return {"zip_path": zip_path.as_posix(), "zip_sha256": digest, "sha256_path": sha_path.as_posix()}


def write_bundle(output_dir: Path, *, quick: bool = False, with_append_only_self_test: bool = False) -> dict[str, Any]:
    output_dir = validate_output_dir(output_dir)
    if exists_or_symlink(output_dir):
        raise FileExistsError(f"Output directory already exists: {output_dir}")
    if exists_or_symlink(output_dir.with_suffix(".zip")):
        raise FileExistsError(f"ZIP already exists: {output_dir.with_suffix('.zip')}")
    sha_sidecar = Path(str(output_dir.with_suffix(".zip")) + ".sha256")
    if exists_or_symlink(sha_sidecar):
        raise FileExistsError(f"SHA256 sidecar already exists: {sha_sidecar}")
    mkdir_no_symlink(output_dir)

    stack = load_stack()
    deps = dependency_checks(stack)
    source_static_audit = source_static_import_audit(stack)
    cases = build_trial_cases(stack)
    results = [process_adapter_case(stack, case, output_dir) for case in cases]
    logs = [row["log_event"] for row in results]
    latency = run_latency(stack, cases[0], output_dir, count=20 if quick else 300)
    direct_adversarial = direct_adversarial_self_test()
    stress_result = stress_self_test(stack, cases, output_dir, quick=quick)
    metrics_row = metrics(results, logs, latency, cases, direct_adversarial)
    metrics_row.update({
        "stress_self_test_passed": stress_result.get("status") == "pass",
        "stress_quick_mode": bool(quick),
        "stress_sequential_count": stress_result.get("sequential_count", 0),
        "stress_parallel_count": stress_result.get("parallel_count", 0),
        "stress_total_count": stress_result.get("total_count", 0),
        "stress_failure_count": stress_result.get("failure_count", 0),
        "stress_cleanup_ok": stress_result.get("cleanup_ok") is True,
        "stress_workspace_exists_after": stress_result.get("stress_workspace_exists_after") is True,
        "stress_signature_plan_count": stress_result.get("signature_plan_count", 0),
        "source_static_import_audit_passed": source_static_audit.get("status") == "pass",
        "source_static_import_file_count": source_static_audit.get("file_count", 0),
        "source_static_disallowed_import_count": source_static_audit.get("disallowed_import_count", 0),
        "source_static_banned_import_count": source_static_audit.get("banned_import_count", 0),
    })
    append_result: dict[str, Any] | None = None
    if with_append_only_self_test:
        append_result = append_only_self_test()
    summary_row = summary(
        metrics_row,
        deps,
        append_only_self_test_status=append_result.get("status") if append_result else None,
    )

    write_lf(output_dir / "CONTRACT.md", contract_md())
    write_lf(output_dir / "LIMITS.md", limits_md())
    write_jsonl(output_dir / "trial_cases.jsonl", [sanitize_trial_case_for_artifact(case) for case in cases])
    write_jsonl(output_dir / "trial_results.jsonl", [sanitize_result_for_artifact(row) for row in results])
    write_jsonl(output_dir / "trial_logs.jsonl", logs)
    write_lf(output_dir / "latency_metrics.json", pretty_json(latency))
    write_lf(output_dir / "direct_adversarial_self_test.json", pretty_json(direct_adversarial))
    write_lf(output_dir / "stress_self_test.json", pretty_json(stress_result))
    write_lf(output_dir / "source_static_import_audit.json", pretty_json(source_static_audit))
    write_lf(output_dir / "quality_metrics.json", pretty_json(metrics_row))
    write_lf(output_dir / "dependency_checks.json", pretty_json(deps))
    write_lf(output_dir / "summary.json", pretty_json(summary_row))

    provenance_dir = output_dir / "provenance"
    mkdir_no_symlink(provenance_dir)
    copy_file_no_clobber(Path(__file__), provenance_dir / Path(__file__).name)

    if with_append_only_self_test:
        write_lf(output_dir / "append_only_self_test.json", pretty_json(append_result))

    artifact_hashes = collect_hashes(output_dir)
    manifest = {
        "run_id": RUN_ID,
        "created_at": "2026-06-25",
        "tool": "tools/vaks_supervised_trial_adapter_r1_5.py",
        "runner_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "runner_provenance_sha256": artifact_hashes.get(f"provenance/{Path(__file__).name}", ""),
        "r1_4_runner_sha256": deps.get("r1_4_runner_sha256", ""),
        "summary_status": summary_row["status"],
        "supervised_trial_adapter_recommendation": summary_row["supervised_trial_adapter_recommendation"],
        "canary_recommendation": summary_row["canary_recommendation"],
        "read_only": True,
        "sandbox_only": True,
        "formal_obsidian_write": False,
        "append_only_self_test_status": append_result.get("status") if append_result else "not_run",
        "artifact_hashes": artifact_hashes,
    }
    write_lf(output_dir / "run_manifest.json", pretty_json(manifest))
    zip_info = create_zip(output_dir)
    return {"summary": summary_row, "zip": zip_info, "manifest": manifest}


def verify_bundle(output_dir: Path) -> dict[str, Any]:
    manifest = read_json(output_dir / "run_manifest.json")
    current_hashes = collect_hashes(output_dir)
    failures = []
    for relative, expected in manifest.get("artifact_hashes", {}).items():
        actual = current_hashes.get(relative)
        if actual != expected:
            failures.append({"path": relative, "expected": expected, "actual": actual})
    extra = sorted(set(current_hashes) - set(manifest.get("artifact_hashes", {})) - {"run_manifest.json"})
    stress_workspace_artifacts = sorted(
        path for path in current_hashes
        if path == "_stress_workspace" or path.startswith("_stress_workspace/")
    )
    summary_path = output_dir / "summary.json"
    summary_row: dict[str, Any] = {}
    summary_read_error = ""
    if summary_path.is_file():
        try:
            summary_row = read_json(summary_path)
        except Exception as exc:
            summary_read_error = exc.__class__.__name__
    else:
        summary_read_error = "missing"
    runner_path = output_dir / "provenance" / Path(__file__).name
    runner_ok = (
        runner_path.is_file()
        and sha256_bytes(runner_path.read_bytes()) == manifest.get("runner_provenance_sha256")
    )
    zip_path = output_dir.with_suffix(".zip")
    sidecar_path = Path(str(zip_path) + ".sha256")
    zip_digest = sha256_bytes(zip_path.read_bytes()) if zip_path.is_file() else ""
    sidecar_digest = zip_sidecar_digest(zip_path)
    zip_duplicate_entries = 0
    zip_unsafe_entries = 0
    zip_bad_mtime_entries = 0
    zip_bad_compression_entries = 0
    zip_entry_order_ok = False
    zip_hash_failures: list[dict[str, Any]] = []
    zip_extra_entries: list[str] = []
    zip_missing_entries: list[str] = []
    stress_workspace_zip_entries: list[str] = []
    zip_integrity_ok = False
    expected_zip_entries = set(current_hashes)
    try:
        with zipfile.ZipFile(zip_path, "r") as archive:
            names = archive.namelist()
            zip_entry_order_ok = names == sorted(names)
            zip_duplicate_entries = len(names) - len(set(names))
            zip_unsafe_entries = sum(1 for name in names if not zip_entry_name_is_safe(name))
            zip_bad_mtime_entries = sum(
                1 for info in archive.infolist()
                if info.date_time != (2026, 6, 24, 0, 0, 0)
            )
            zip_bad_compression_entries = sum(
                1 for info in archive.infolist()
                if info.compress_type != zipfile.ZIP_DEFLATED
            )
            zip_extra_entries = sorted(set(names) - expected_zip_entries)
            zip_missing_entries = sorted(expected_zip_entries - set(names))
            stress_workspace_zip_entries = sorted(
                name for name in names
                if name == "_stress_workspace" or name.startswith("_stress_workspace/")
            )
            for name in sorted(set(names) & expected_zip_entries):
                actual = sha256_bytes(archive.read(name))
                expected = current_hashes.get(name)
                if actual != expected:
                    zip_hash_failures.append({"path": name, "expected": expected, "actual": actual})
            zip_integrity_ok = archive.testzip() is None
    except Exception as exc:
        zip_hash_failures.append({"path": zip_path.as_posix(), "error_class": exc.__class__.__name__})
    checks = {
        "manifest_hashes_match": not failures,
        "summary_pass": summary_row.get("status") == "pass",
        "hard_zero_pass": bool(summary_row.get("hard_zero_pass")),
        "runner_provenance_hash_matches": runner_ok,
        "zip_exists": zip_path.is_file(),
        "zip_sidecar_exists": sidecar_path.is_file(),
        "zip_sidecar_matches_zip": bool(zip_digest) and sidecar_digest == zip_digest,
        "zip_sidecar_exact_format": zip_sidecar_exact_format_ok(zip_path, zip_digest),
        "zip_integrity_ok": zip_integrity_ok,
        "zip_entry_set_matches_directory": not zip_extra_entries and not zip_missing_entries,
        "zip_entry_hashes_match_directory": not zip_hash_failures,
        "no_stress_workspace_artifacts": not stress_workspace_artifacts,
        "zip_has_no_stress_workspace_entries": not stress_workspace_zip_entries,
        "zip_entry_order_fixed": zip_entry_order_ok,
        "zip_has_no_duplicate_entries": zip_duplicate_entries == 0,
        "zip_has_no_unsafe_entries": zip_unsafe_entries == 0,
        "zip_entry_mtime_fixed": zip_bad_mtime_entries == 0,
        "zip_entry_compression_fixed": zip_bad_compression_entries == 0,
    }
    return {
        "status": "pass" if all(checks.values()) and not extra else "fail",
        "checks": checks,
        "hash_failures": failures,
        "extra_hashes": extra,
        "summary_read_error": summary_read_error,
        "stress_workspace_artifacts": stress_workspace_artifacts,
        "zip_forensics": {
            "zip_path": zip_path.as_posix(),
            "zip_sha256": zip_digest,
            "sidecar_sha256": sidecar_digest,
            "duplicate_entry_count": zip_duplicate_entries,
            "unsafe_entry_count": zip_unsafe_entries,
            "bad_mtime_entry_count": zip_bad_mtime_entries,
            "bad_compression_entry_count": zip_bad_compression_entries,
            "entry_order_fixed": zip_entry_order_ok,
            "extra_entries": zip_extra_entries,
            "missing_entries": zip_missing_entries,
            "stress_workspace_entries": stress_workspace_zip_entries,
            "hash_failures": zip_hash_failures,
        },
    }


def copy_bundle_for_tamper(source_dir: Path, target_dir: Path) -> None:
    if exists_or_symlink(target_dir):
        raise FileExistsError(f"Tamper target already exists: {target_dir}")
    if exists_or_symlink(target_dir.with_suffix(".zip")):
        raise FileExistsError(f"Tamper ZIP already exists: {target_dir.with_suffix('.zip')}")
    target_sha = Path(str(target_dir.with_suffix(".zip")) + ".sha256")
    if exists_or_symlink(target_sha):
        raise FileExistsError(f"Tamper SHA sidecar already exists: {target_sha}")
    shutil.copytree(source_dir, target_dir, symlinks=False)
    shutil.copy2(source_dir.with_suffix(".zip"), target_dir.with_suffix(".zip"))
    shutil.copy2(Path(str(source_dir.with_suffix(".zip")) + ".sha256"), target_sha)


def tamper_negative_self_test(source_dir: Path) -> dict[str, Any]:
    base = f"{OUTPUT_NAME_PREFIX}tamper-{os.getpid()}-{int(time.time() * 1000)}"
    targets = {
        "artifact": OUTPUT_ROOT / f"{base}-artifact",
        "missing": OUTPUT_ROOT / f"{base}-missing",
        "extra": OUTPUT_ROOT / f"{base}-extra",
        "sidecar": OUTPUT_ROOT / f"{base}-sidecar",
        "sidecar-format": OUTPUT_ROOT / f"{base}-sidecar-format",
        "zip": OUTPUT_ROOT / f"{base}-zip",
        "zip-duplicate": OUTPUT_ROOT / f"{base}-zip-duplicate",
        "zip-content": OUTPUT_ROOT / f"{base}-zip-content",
    }
    checks: list[dict[str, Any]] = []
    try:
        for target in targets.values():
            copy_bundle_for_tamper(source_dir, target)

        tampered_summary = targets["artifact"] / "summary.json"
        tampered_summary.unlink()
        write_lf(tampered_summary, "{}\n")
        artifact_result = verify_bundle(targets["artifact"])
        checks.append({
            "name": "artifact_tamper_detected",
            "passed": artifact_result.get("status") == "fail"
            and artifact_result.get("checks", {}).get("manifest_hashes_match") is False,
            "observed_status": artifact_result.get("status"),
            "manifest_hashes_match": artifact_result.get("checks", {}).get("manifest_hashes_match"),
        })

        (targets["missing"] / "summary.json").unlink()
        missing_result = verify_bundle(targets["missing"])
        checks.append({
            "name": "missing_artifact_detected",
            "passed": missing_result.get("status") == "fail"
            and missing_result.get("checks", {}).get("manifest_hashes_match") is False,
            "observed_status": missing_result.get("status"),
            "manifest_hashes_match": missing_result.get("checks", {}).get("manifest_hashes_match"),
        })

        write_lf(targets["extra"] / "unexpected-extra-artifact.txt", "unexpected\n")
        extra_result = verify_bundle(targets["extra"])
        checks.append({
            "name": "extra_artifact_detected",
            "passed": extra_result.get("status") == "fail"
            and "unexpected-extra-artifact.txt" in extra_result.get("extra_hashes", []),
            "observed_status": extra_result.get("status"),
            "extra_hashes": extra_result.get("extra_hashes", []),
        })

        sidecar_path = Path(str(targets["sidecar"].with_suffix(".zip")) + ".sha256")
        sidecar_path.write_text("0" * 64 + f"  {targets['sidecar'].with_suffix('.zip').name}\n", encoding="utf-8")
        sidecar_result = verify_bundle(targets["sidecar"])
        checks.append({
            "name": "sidecar_tamper_detected",
            "passed": sidecar_result.get("status") == "fail"
            and sidecar_result.get("checks", {}).get("zip_sidecar_matches_zip") is False,
            "observed_status": sidecar_result.get("status"),
            "zip_sidecar_matches_zip": sidecar_result.get("checks", {}).get("zip_sidecar_matches_zip"),
        })

        sidecar_format_zip = targets["sidecar-format"].with_suffix(".zip")
        sidecar_format_path = Path(str(sidecar_format_zip) + ".sha256")
        sidecar_format_digest = sha256_bytes(sidecar_format_zip.read_bytes())
        sidecar_format_path.write_text(
            f"{sidecar_format_digest}  wrong-name.zip\n",
            encoding="utf-8",
        )
        sidecar_format_result = verify_bundle(targets["sidecar-format"])
        checks.append({
            "name": "sidecar_format_tamper_detected",
            "passed": sidecar_format_result.get("status") == "fail"
            and sidecar_format_result.get("checks", {}).get("zip_sidecar_matches_zip") is True
            and sidecar_format_result.get("checks", {}).get("zip_sidecar_exact_format") is False,
            "observed_status": sidecar_format_result.get("status"),
            "zip_sidecar_matches_zip": sidecar_format_result.get("checks", {}).get("zip_sidecar_matches_zip"),
            "zip_sidecar_exact_format": sidecar_format_result.get("checks", {}).get("zip_sidecar_exact_format"),
        })

        with zipfile.ZipFile(targets["zip"].with_suffix(".zip"), "a", compression=zipfile.ZIP_DEFLATED) as archive:
            info = zipfile.ZipInfo("../escape.txt")
            info.date_time = (2026, 6, 24, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, b"escape")
        zip_result = verify_bundle(targets["zip"])
        checks.append({
            "name": "zip_unsafe_entry_tamper_detected",
            "passed": zip_result.get("status") == "fail"
            and zip_result.get("checks", {}).get("zip_has_no_unsafe_entries") is False,
            "observed_status": zip_result.get("status"),
            "zip_has_no_unsafe_entries": zip_result.get("checks", {}).get("zip_has_no_unsafe_entries"),
            "unsafe_entry_count": zip_result.get("zip_forensics", {}).get("unsafe_entry_count"),
        })

        with zipfile.ZipFile(targets["zip-duplicate"].with_suffix(".zip"), "a", compression=zipfile.ZIP_DEFLATED) as archive:
            info = zipfile.ZipInfo("summary.json")
            info.date_time = (2026, 6, 24, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, b"duplicate summary")
        duplicate_result = verify_bundle(targets["zip-duplicate"])
        checks.append({
            "name": "zip_duplicate_entry_tamper_detected",
            "passed": duplicate_result.get("status") == "fail"
            and duplicate_result.get("checks", {}).get("zip_has_no_duplicate_entries") is False,
            "observed_status": duplicate_result.get("status"),
            "zip_has_no_duplicate_entries": duplicate_result.get("checks", {}).get("zip_has_no_duplicate_entries"),
            "duplicate_entry_count": duplicate_result.get("zip_forensics", {}).get("duplicate_entry_count"),
        })

        with zipfile.ZipFile(targets["zip-content"].with_suffix(".zip"), "a", compression=zipfile.ZIP_DEFLATED) as archive:
            info = zipfile.ZipInfo("summary.json")
            info.date_time = (2026, 6, 24, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, b"tampered content")
        content_result = verify_bundle(targets["zip-content"])
        checks.append({
            "name": "zip_content_tamper_detected",
            "passed": content_result.get("status") == "fail"
            and content_result.get("checks", {}).get("zip_entry_hashes_match_directory") is False,
            "observed_status": content_result.get("status"),
            "zip_entry_hashes_match_directory": content_result.get("checks", {}).get("zip_entry_hashes_match_directory"),
            "zip_hash_failure_count": len(content_result.get("zip_forensics", {}).get("hash_failures", [])),
        })

        failure_count = sum(1 for check in checks if not check["passed"])
        return {
            "status": "pass" if failure_count == 0 else "fail",
            "check_count": len(checks),
            "failure_count": failure_count,
            "checks": checks,
        }
    finally:
        for target in targets.values():
            for path in (target, target.with_suffix(".zip"), Path(str(target.with_suffix(".zip")) + ".sha256")):
                if exists_or_symlink(path):
                    path.unlink() if path.is_symlink() or path.is_file() else shutil.rmtree(path)


def forbidden_output_path_self_test() -> dict[str, Any]:
    base = f"{OUTPUT_NAME_PREFIX}forbidden-{os.getpid()}-{int(time.time() * 1000)}"
    candidates = [
        ("raw_root", ROOT / "raw" / base),
        ("wiki_root", ROOT / "wiki" / base),
        ("review_prefix_trick", ROOT / "outputs" / "review_evil" / base),
        ("bad_review_name", OUTPUT_ROOT / f"{base}-badname"),
        ("control_char_name", OUTPUT_ROOT / f"{base}\ncontrol"),
        ("obsidian_vault", Path("H:/Obsidian/资料库") / base),
    ]
    checks: list[dict[str, Any]] = []
    for name, path in candidates:
        existed_before = exists_or_symlink(path)
        error_class = ""
        created = False
        try:
            write_bundle(path, quick=True, with_append_only_self_test=False)
        except Exception as exc:
            error_class = exc.__class__.__name__
        finally:
            created = exists_or_symlink(path) and not existed_before
            if created:
                path.unlink() if path.is_symlink() or path.is_file() else shutil.rmtree(path)
        checks.append({
            "name": name,
            "path": path.as_posix(),
            "error_class": error_class,
            "created": created,
            "passed": error_class == "ValueError" and not created,
        })
    failure_count = sum(1 for check in checks if not check["passed"])
    return {
        "status": "pass" if failure_count == 0 else "fail",
        "check_count": len(checks),
        "failure_count": failure_count,
        "checks": checks,
    }


def without_latency_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: without_latency_fields(item)
            for key, item in value.items()
            if not key.startswith("latency_") and key != "elapsed_ms"
        }
    if isinstance(value, list):
        return [without_latency_fields(item) for item in value]
    return value


def stable_artifact_repeatability_self_test() -> dict[str, Any]:
    base = f"{OUTPUT_NAME_PREFIX}repeat-{os.getpid()}-{int(time.time() * 1000)}"
    left = OUTPUT_ROOT / f"{base}-a"
    right = OUTPUT_ROOT / f"{base}-b"
    stable_text_files = [
        "trial_cases.jsonl",
        "trial_logs.jsonl",
        "dependency_checks.json",
    ]
    stable_normalized_jsonl_files = [
        "trial_results.jsonl",
    ]
    stable_normalized_json_files = [
        "quality_metrics.json",
        "summary.json",
    ]
    checks: list[dict[str, Any]] = []
    try:
        left_result = write_bundle(left, quick=True, with_append_only_self_test=False)
        right_result = write_bundle(right, quick=True, with_append_only_self_test=False)
        for relative in stable_text_files:
            left_text = (left / relative).read_text(encoding="utf-8")
            right_text = (right / relative).read_text(encoding="utf-8")
            checks.append({
                "name": f"{relative}_exact_match",
                "passed": left_text == right_text,
                "left_sha256": sha256_text(left_text),
                "right_sha256": sha256_text(right_text),
            })
        for relative in stable_normalized_jsonl_files:
            left_rows = [
                without_latency_fields(json.loads(line))
                for line in (left / relative).read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            right_rows = [
                without_latency_fields(json.loads(line))
                for line in (right / relative).read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            left_text = "".join(stable_json(row) + "\n" for row in left_rows)
            right_text = "".join(stable_json(row) + "\n" for row in right_rows)
            checks.append({
                "name": f"{relative}_normalized_match",
                "passed": left_text == right_text,
                "normalization": "latency_and_elapsed_fields_removed",
                "left_sha256": sha256_text(left_text),
                "right_sha256": sha256_text(right_text),
            })
        for relative in stable_normalized_json_files:
            left_normalized = without_latency_fields(read_json(left / relative))
            right_normalized = without_latency_fields(read_json(right / relative))
            left_text = stable_json(left_normalized)
            right_text = stable_json(right_normalized)
            checks.append({
                "name": f"{relative}_normalized_match",
                "passed": left_text == right_text,
                "normalization": "latency_fields_removed",
                "left_sha256": sha256_text(left_text),
                "right_sha256": sha256_text(right_text),
            })
        checks.append({
            "name": "both_runs_pass",
            "passed": left_result["summary"]["status"] == "pass"
            and right_result["summary"]["status"] == "pass",
            "left_status": left_result["summary"]["status"],
            "right_status": right_result["summary"]["status"],
        })
        failure_count = sum(1 for check in checks if not check["passed"])
        return {
            "status": "pass" if failure_count == 0 else "fail",
            "check_count": len(checks),
            "failure_count": failure_count,
            "checks": checks,
            "not_compared_as_deterministic": [
                "latency_metrics.json",
                "zip_sha256",
                "run_manifest artifact hashes",
            ],
        }
    finally:
        for target in (left, right):
            for path in (target, target.with_suffix(".zip"), Path(str(target.with_suffix(".zip")) + ".sha256")):
                if exists_or_symlink(path):
                    path.unlink() if path.is_symlink() or path.is_file() else shutil.rmtree(path)


def append_only_self_test() -> dict[str, Any]:
    temp_name = f"{OUTPUT_NAME_PREFIX}append-only-{os.getpid()}-{int(time.time() * 1000)}"
    out = OUTPUT_ROOT / temp_name
    zip_path = out.with_suffix(".zip")
    sha_path = Path(str(zip_path) + ".sha256")
    sidecar_name = f"{OUTPUT_NAME_PREFIX}append-only-{os.getpid()}-{int(time.time() * 1000) + 1}"
    sidecar_out = OUTPUT_ROOT / sidecar_name
    sidecar_zip = sidecar_out.with_suffix(".zip")
    sidecar_sha = Path(str(sidecar_zip) + ".sha256")
    artifact_name = f"{OUTPUT_NAME_PREFIX}append-only-{os.getpid()}-{int(time.time() * 1000) + 2}"
    artifact_out = OUTPUT_ROOT / artifact_name
    artifact_path = artifact_out / "artifact.txt"
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
        write_bytes_no_clobber(sidecar_zip, b"pre-existing zip")
        sidecar_error = ""
        sidecar_dir_created = False
        try:
            write_bundle(sidecar_out, quick=True, with_append_only_self_test=False)
        except FileExistsError as exc:
            sidecar_error = exc.__class__.__name__
            sidecar_dir_created = exists_or_symlink(sidecar_out)
        mkdir_no_symlink(artifact_out)
        write_lf(artifact_path, "first\n")
        artifact_overwrite_error = ""
        artifact_text_after = artifact_path.read_text(encoding="utf-8")
        try:
            write_lf(artifact_path, "second\n")
        except FileExistsError as exc:
            artifact_overwrite_error = exc.__class__.__name__
        artifact_text_after_rejected_write = artifact_path.read_text(encoding="utf-8")
        tamper_result = tamper_negative_self_test(out)
        forbidden_output_result = forbidden_output_path_self_test()
        repeatability_result = stable_artifact_repeatability_self_test()
        return {
            "status": "pass" if (
                second_error == "FileExistsError"
                and before == after
                and sidecar_error == "FileExistsError"
                and not sidecar_dir_created
                and artifact_overwrite_error == "FileExistsError"
                and artifact_text_after == artifact_text_after_rejected_write == "first\n"
                and tamper_result.get("status") == "pass"
                and forbidden_output_result.get("status") == "pass"
                and repeatability_result.get("status") == "pass"
            ) else "fail",
            "first_run_status": first["summary"]["status"],
            "second_run_same_directory_rejected": second_error == "FileExistsError",
            "second_run_exit_code": second_exit_code,
            "second_run_error_class": second_error,
            "tree_hash_before_second_run": before,
            "tree_hash_after_second_run": after,
            "tree_hash_unchanged_after_rejected_second_run": before == after,
            "preexisting_zip_rejected": sidecar_error == "FileExistsError",
            "preexisting_zip_left_output_dir_uncreated": not sidecar_dir_created,
            "artifact_overwrite_rejected": artifact_overwrite_error == "FileExistsError",
            "artifact_overwrite_error_class": artifact_overwrite_error,
            "artifact_text_unchanged_after_rejected_write": artifact_text_after == artifact_text_after_rejected_write,
            "tamper_negative_self_test": tamper_result,
            "forbidden_output_path_self_test": forbidden_output_result,
            "stable_artifact_repeatability_self_test": repeatability_result,
        }
    finally:
        for path in (out, zip_path, sha_path, sidecar_out, sidecar_zip, sidecar_sha, artifact_out):
            if exists_or_symlink(path):
                path.unlink() if path.is_symlink() or path.is_file() else shutil.rmtree(path)


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
    except Exception as exc:
        print(stable_json({"status": "error", "error_class": exc.__class__.__name__, "message": str(exc)}))
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
