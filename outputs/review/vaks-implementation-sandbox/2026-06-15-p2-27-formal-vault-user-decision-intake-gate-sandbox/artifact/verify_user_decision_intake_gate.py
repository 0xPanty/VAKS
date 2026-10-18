from __future__ import annotations

import argparse
import hashlib
import html.parser
import importlib.util
import json
import re
import sys
from pathlib import Path


SLICE_ID = "2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox"
PACKET_SLICE_ID = "2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox"

FORBIDDEN_OPERATIONS = [
    "formal_vault_read",
    "formal_vault_scan",
    "formal_vault_write",
    "formal_vault_hash",
    "formal_vault_snapshot",
    "obsidian_sync",
    "commit",
    "push",
    "promotion",
    "dependency_install",
    "background_service",
    "mcp_write_tool",
    "hooks",
    "real_base_files",
    "production_ui",
    "local_storage_write",
    "network_post",
    "actual_approval_collection",
    "actual_user_approval",
    "actual_user_decision_collection",
    "user_approval_inference",
    "action_basis_creation",
    "reviewed_knowledge_creation",
    "external_notification",
    "real_user_text_storage",
    "real_user_text_capture",
    "write_gate_opening",
]

REQUIRED_BOUNDARY_PHRASES = [
    "sandbox only",
    "user decision intake gate draft only",
    "future capture only",
    "not actual approval",
    "approval not collected",
    "real user text not stored",
    "formal vault not accessed",
    "dry-run only",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "does not approve",
    "no formal vault write",
    "no formal vault read",
    "no sync",
    "no commit",
    "no push",
    "no promotion",
    "requires separate user approval",
    "requires separate execution slice",
]

REQUIRED_FUTURE_FIELDS = {
    "decision_id",
    "decision_verdict",
    "future_user_exact_text_reference",
    "user_turn_id",
    "timestamp_utc",
    "packet_hash",
    "source_bundle_hash",
    "scope_hash",
    "rehearsal_hash",
    "intake_gate_hash",
    "operator_or_agent_id",
    "scope_ids",
    "explicit_exclusions_ack",
    "rollback_ack",
    "hash_ack",
    "dirty_state_ack",
    "extra_files_requested",
}

AUTHORITY_CONFUSING_PATTERNS = [
    "approval collected now",
    "actual approval collected",
    "ready to write formal vault",
    "formal vault approval granted",
    "action basis approved",
    "reviewed truth",
    "merge approved",
    "sync approved",
    "promotion approved",
    "real user text stored",
]


class IntakeHTMLParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sandbox_only = False
        self.intake_gate_only = False
        self.future_capture_only = False
        self.no_approval = False
        self.no_real_user_text_storage = False
        self.no_write = False
        self.no_sync = False
        self.no_authority = False
        self.roles: set[str] = set()
        self.cards: list[dict[str, str]] = []
        self.buttons: list[str] = []
        self.button_texts: list[str] = []
        self.inputs: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.forms = 0
        self.downloads = 0
        self.contenteditable = 0
        self._current_button: str | None = None
        self._in_script = False
        self.script_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: v or "" for k, v in attrs}
        if tag == "html":
            self.sandbox_only = attr.get("data-sandbox-only") == "true"
            self.intake_gate_only = attr.get("data-user-decision-intake-gate-only") == "true"
            self.future_capture_only = attr.get("data-future-capture-only") == "true"
            self.no_approval = attr.get("data-no-approval") == "true"
            self.no_real_user_text_storage = attr.get("data-no-real-user-text-storage") == "true"
            self.no_write = attr.get("data-no-write") == "true"
            self.no_sync = attr.get("data-no-sync") == "true"
            self.no_authority = attr.get("data-no-authority") == "true"
        if "data-role" in attr:
            self.roles.add(attr["data-role"])
        if tag == "article" and "card" in attr.get("class", "").split():
            self.cards.append({"kind": attr.get("data-kind", ""), "search": attr.get("data-search", "")})
        if tag == "button":
            self.buttons.append(attr.get("data-filter", ""))
            self._current_button = ""
        if tag == "input":
            self.inputs.append({"id": attr.get("id", ""), "type": attr.get("type", ""), "name": attr.get("name", "")})
        if tag == "form":
            self.forms += 1
        if tag == "a":
            self.anchors.append({"href": attr.get("href", ""), "download": attr.get("download", "")})
            if "download" in attr:
                self.downloads += 1
        if attr.get("contenteditable", "").lower() == "true":
            self.contenteditable += 1
        if tag == "script" and attr.get("id") == "intake-data":
            self._in_script = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._in_script = False
        if tag == "button" and self._current_button is not None:
            self.button_texts.append(self._current_button.strip())
            self._current_button = None

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self.script_text += data
        if self._current_button is not None:
            self._current_button += data


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def sandbox_root() -> Path:
    return root().parent


def workspace_root() -> Path:
    return sandbox_root().parents[2]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_json(data: object) -> str:
    raw = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_builder() -> object:
    path = root() / "artifact" / "user_decision_intake_gate_builder.py"
    spec = importlib.util.spec_from_file_location("user_decision_intake_gate_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load builder: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def frontmatter_status(text: str) -> str:
    if not text.startswith("---\n"):
        return "missing_frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return "missing_frontmatter_end"
    for line in text[4:end].splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def source_rehearsal_config() -> dict:
    return load_json(sandbox_root() / SOURCE_SLICE_ID / "fixtures" / "valid-decision-rehearsal-config.json")


def source_packet_config() -> dict:
    return load_json(sandbox_root() / PACKET_SLICE_ID / "fixtures" / "valid-approval-packet-config.json")


def is_bad_target(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return (
        re.match(r"^[A-Za-z]:/", normalized) is not None
        or normalized.startswith("/")
        or ".." in normalized.split("/")
        or normalized.startswith("wiki/")
        or normalized.startswith("templates/")
        or normalized.startswith("tools/")
        or "Obsidian" in value
    )


def validate_source_path(source_path: str, fid: str, errors: list[str]) -> None:
    if not source_path:
        errors.append(f"source_input_path_missing:{fid}")
        return
    normalized = source_path.replace("\\", "/")
    allowed_prefixes = [
        f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/",
        f"outputs/review/vaks-implementation-sandbox/{PACKET_SLICE_ID}/",
    ]
    if is_bad_target(normalized) or not any(normalized.startswith(prefix) for prefix in allowed_prefixes):
        errors.append(f"source_input_path_invalid:{fid}")
        return
    source_abs = (workspace_root() / normalized).resolve()
    try:
        source_abs.relative_to(workspace_root())
    except ValueError:
        errors.append(f"source_input_path_invalid:{fid}")
        return
    if not source_abs.exists():
        errors.append(f"source_input_missing:{fid}")


def gate_material(cfg: dict) -> dict:
    samples = []
    for sample in cfg.get("synthetic_intake_samples", []):
        item = dict(sample)
        item.pop("required_intake_gate_hash", None)
        hashes = dict(item.get("hash_claims", {}))
        hashes.pop("intake_gate_hash", None)
        item["hash_claims"] = hashes
        samples.append(item)
    receipt = dict(cfg.get("non_approval_receipt", {}))
    receipt.pop("intake_gate_hash", None)
    contract = dict(cfg.get("intake_contract", {}))
    contract.pop("required_intake_gate_hash", None)
    return {
        "intake_gate_version": cfg.get("intake_gate_version"),
        "source_slice": cfg.get("source_slice"),
        "source_input_bundle_hash": cfg.get("source_input_bundle_hash"),
        "source_rehearsal_hash": cfg.get("source_rehearsal_hash"),
        "source_packet_hash": cfg.get("source_packet_hash"),
        "source_packet_source_bundle_hash": cfg.get("source_packet_source_bundle_hash"),
        "source_packet_scope_hash": cfg.get("source_packet_scope_hash"),
        "intake_contract": contract,
        "synthetic_intake_samples": samples,
        "non_approval_receipt": receipt,
        "stop_conditions": cfg.get("stop_conditions", []),
    }


def validate_config(cfg: dict) -> list[str]:
    errors: list[str] = []
    rehearsal = source_rehearsal_config()
    packet = source_packet_config()
    if cfg.get("slice_id") != SLICE_ID:
        errors.append("wrong_slice_id")
    if cfg.get("source_slice") != SOURCE_SLICE_ID:
        errors.append("wrong_source_slice")
    if cfg.get("packet_slice") != PACKET_SLICE_ID:
        errors.append("wrong_packet_slice")

    expected_scope = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"
    if cfg.get("write_scope") != [expected_scope]:
        errors.append("invalid_write_scope")
    for scope in cfg.get("write_scope", []):
        normalized = scope.replace("\\", "/")
        if not normalized.startswith(expected_scope):
            errors.append("invalid_write_scope")
        if any(bad in normalized for bad in ["wiki/claims", "wiki/patterns", "wiki/decisions", "templates/", "tools/", "H:/Obsidian"]):
            errors.append("invalid_write_scope")

    ops = cfg.get("operations", {})
    if ops.get("default_read_only") is not True:
        errors.append("default_not_read_only")
    if ops.get("rebuild_requires_explicit_flag") is not True:
        errors.append("rebuild_not_explicit")
    for op in FORBIDDEN_OPERATIONS:
        if ops.get(op) is not False:
            errors.append(f"forbidden_operation:{op}")

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase not in cfg.get("boundary_phrases", []):
            errors.append(f"missing_boundary_phrase:{phrase}")

    for item in cfg.get("source_inputs", []):
        fid = item.get("id", "unknown")
        source_path = item.get("source_path", "")
        validate_source_path(source_path, fid, errors)
        if source_path and f"source_input_path_invalid:{fid}" not in errors and f"source_input_missing:{fid}" not in errors:
            actual = sha256(workspace_root() / source_path.replace("\\", "/"))
            if item.get("source_sha256") != actual:
                errors.append(f"source_input_hash_mismatch:{fid}")
        if item.get("content_binding") != "exact_source_sha256":
            errors.append(f"source_input_content_binding_missing:{fid}")
    if cfg.get("source_input_bundle_hash") != sha256_json(cfg.get("source_inputs", [])):
        errors.append("source_input_bundle_hash_mismatch")
    if cfg.get("source_rehearsal_hash") != rehearsal.get("rehearsal_hash"):
        errors.append("source_rehearsal_hash_mismatch")
    if cfg.get("source_packet_hash") != packet.get("packet_hash"):
        errors.append("source_packet_hash_mismatch")
    if cfg.get("source_packet_source_bundle_hash") != packet.get("source_bundle_hash"):
        errors.append("source_packet_source_bundle_hash_mismatch")
    if cfg.get("source_packet_scope_hash") != packet.get("approval_scope", {}).get("scope_hash"):
        errors.append("source_packet_scope_hash_mismatch")

    if cfg.get("intake_gate_hash_material") != gate_material(cfg):
        errors.append("intake_gate_hash_material_mismatch")
    expected_gate_hash = sha256_json(gate_material(cfg))
    if not cfg.get("intake_gate_hash"):
        errors.append("intake_gate_hash_missing")
    elif cfg.get("intake_gate_hash") != expected_gate_hash:
        errors.append("intake_gate_hash_mismatch")

    contract = cfg.get("intake_contract", {})
    if contract.get("current_slice_collects_approval") is not False:
        errors.append("contract_allows_current_approval_collection")
    if contract.get("future_user_turn_required") is not True:
        errors.append("contract_missing_future_user_turn_required")
    if contract.get("actual_user_input_disallowed_in_this_slice") is not True:
        errors.append("contract_allows_actual_user_input")
    if contract.get("real_user_text_storage_disallowed_in_this_slice") is not True:
        errors.append("contract_allows_real_user_text_storage")
    if contract.get("future_user_exact_text_reference_required") is not True:
        errors.append("contract_missing_future_text_reference_required")
    if contract.get("exact_confirmation_phrases_required_for_approve") is not True:
        errors.append("contract_missing_exact_confirmation_phrases")
    if contract.get("hash_match_required") is not True:
        errors.append("contract_missing_hash_match_required")
    if contract.get("deny_blocks_write") is not True:
        errors.append("contract_deny_does_not_block")
    if contract.get("revise_blocks_write") is not True:
        errors.append("contract_revise_does_not_block")
    if contract.get("approved_outcome_not_actionable_in_this_slice") is not True:
        errors.append("contract_allows_approved_outcome_actionable")
    if contract.get("separate_future_execution_slice_required") is not True:
        errors.append("contract_missing_separate_execution_slice")
    missing_fields = REQUIRED_FUTURE_FIELDS - set(contract.get("required_future_fields", []))
    for field in sorted(missing_fields):
        errors.append(f"contract_missing_required_future_field:{field}")
    if contract.get("required_packet_hash") != cfg.get("source_packet_hash"):
        errors.append("contract_packet_hash_mismatch")
    if contract.get("required_source_bundle_hash") != cfg.get("source_packet_source_bundle_hash"):
        errors.append("contract_source_bundle_hash_mismatch")
    if contract.get("required_scope_hash") != cfg.get("source_packet_scope_hash"):
        errors.append("contract_scope_hash_mismatch")
    if contract.get("required_rehearsal_hash") != cfg.get("source_rehearsal_hash"):
        errors.append("contract_rehearsal_hash_mismatch")
    if contract.get("required_intake_gate_hash") != cfg.get("intake_gate_hash"):
        errors.append("contract_intake_gate_hash_mismatch")
    required_phrases = {item["id"]: item["future_confirmation_phrase"] for item in packet.get("approval_questions", [])}
    if contract.get("required_confirmation_phrases") != required_phrases:
        errors.append("contract_confirmation_phrases_mismatch")

    samples = cfg.get("synthetic_intake_samples", [])
    sample_ids = {item.get("id") for item in samples}
    required_samples = {
        "future_approve_reference_capture",
        "future_deny_reference_capture",
        "future_revision_reference_capture",
    }
    for required in required_samples:
        if required not in sample_ids:
            errors.append(f"missing_intake_sample:{required}")
    if len(samples) < cfg.get("product_metrics", {}).get("required_intake_samples", 3):
        errors.append("too_few_intake_samples")

    required_exclusions = set(contract.get("required_exclusions", []))
    required_scope_ids = set(contract.get("required_scope_ids", []))
    for sample in samples:
        sid = sample.get("id", "unknown")
        verdict = sample.get("decision_verdict")
        if sample.get("synthetic_only") is not True:
            errors.append(f"sample_not_synthetic:{sid}")
        if sample.get("actual_user_input") is not False:
            errors.append(f"sample_uses_actual_user_input:{sid}")
        if sample.get("approval_collected_now") is not False:
            errors.append(f"sample_collects_approval_now:{sid}")
        if sample.get("real_user_text_stored") is not False:
            errors.append(f"sample_stores_real_user_text:{sid}")
        if sample.get("captured_user_text"):
            errors.append(f"sample_captures_user_text:{sid}")
        if not str(sample.get("future_user_exact_text_reference", "")).startswith("future_turn_ref:"):
            errors.append(f"sample_missing_future_text_reference:{sid}")
        if sample.get("formal_vault_accessed") is not False:
            errors.append(f"sample_accesses_formal_vault:{sid}")
        if sample.get("formal_vault_write_allowed_now") is not False:
            if verdict == "DENIED_BY_USER":
                errors.append(f"denied_sample_allows_write:{sid}")
            elif verdict == "NEEDS_REVISION":
                errors.append(f"revise_sample_allows_write:{sid}")
            else:
                errors.append(f"sample_allows_formal_vault_write_now:{sid}")
        if sample.get("action_basis_created") is not False:
            errors.append(f"sample_creates_action_basis:{sid}")
        if sample.get("reviewed_knowledge_created") is not False:
            errors.append(f"sample_creates_reviewed_knowledge:{sid}")
        for field, code in [
            ("sync_allowed", "sample_allows_sync"),
            ("commit_allowed", "sample_allows_commit"),
            ("push_allowed", "sample_allows_push"),
            ("promotion_allowed", "sample_allows_promotion"),
        ]:
            if sample.get(field) is not False:
                errors.append(f"{code}:{sid}")
        if sample.get("extra_files_requested") is not False:
            errors.append(f"sample_extra_files_requested:{sid}")
        hashes = sample.get("hash_claims", {})
        if hashes.get("packet_hash") != cfg.get("source_packet_hash"):
            errors.append(f"sample_packet_hash_mismatch:{sid}")
        if hashes.get("source_bundle_hash") != cfg.get("source_packet_source_bundle_hash"):
            errors.append(f"sample_source_bundle_hash_mismatch:{sid}")
        if hashes.get("scope_hash") != cfg.get("source_packet_scope_hash"):
            errors.append(f"sample_scope_hash_mismatch:{sid}")
        if hashes.get("rehearsal_hash") != cfg.get("source_rehearsal_hash"):
            errors.append(f"sample_rehearsal_hash_mismatch:{sid}")
        if hashes.get("intake_gate_hash") != cfg.get("intake_gate_hash"):
            errors.append(f"sample_intake_gate_hash_mismatch:{sid}")
        if sample.get("required_intake_gate_hash") != cfg.get("intake_gate_hash"):
            errors.append(f"sample_required_intake_gate_hash_mismatch:{sid}")
        if set(sample.get("scope_ids", [])) != required_scope_ids:
            errors.append(f"sample_scope_ids_mismatch:{sid}")
        if verdict == "APPROVED_BY_USER":
            phrase_claims = sample.get("phrase_claims", {})
            for qid, phrase in required_phrases.items():
                if phrase_claims.get(qid) != phrase:
                    errors.append(f"approved_missing_confirmation_phrase:{sid}:{qid}")
            confirmed = set(sample.get("confirmed_question_ids", []))
            for qid in required_phrases:
                if qid not in confirmed:
                    errors.append(f"approved_missing_confirmed_question:{sid}:{qid}")
            exclusions = set(sample.get("explicit_exclusions_ack", []))
            for item in required_exclusions:
                if item not in exclusions:
                    errors.append(f"approved_missing_exclusion_ack:{sid}:{item}")
            if sample.get("rollback_ack") is not True:
                errors.append(f"approved_missing_rollback_ack:{sid}")
            if sample.get("hash_ack") is not True:
                errors.append(f"approved_missing_hash_ack:{sid}")
            if sample.get("dirty_state_ack") is not True:
                errors.append(f"approved_missing_dirty_state_ack:{sid}")
            if sample.get("expected_gate_result") == "READY_TO_WRITE":
                errors.append(f"approved_sample_result_actionable:{sid}")
            if sample.get("expected_gate_result") != "VALID_FUTURE_APPROVAL_RECORD_BUT_NOT_ACTIONABLE_IN_THIS_SLICE":
                errors.append(f"approved_sample_result_bad:{sid}")
        if verdict == "DENIED_BY_USER" and sample.get("expected_gate_result") != "BLOCKED_BY_FUTURE_DENIAL_RECORD":
            errors.append(f"denied_sample_result_bad:{sid}")
        if verdict == "NEEDS_REVISION" and sample.get("expected_gate_result") != "BLOCKED_PENDING_PACKET_REVISION":
            errors.append(f"revise_sample_result_bad:{sid}")

    receipt = cfg.get("non_approval_receipt", {})
    if receipt.get("approval_collected_now") is not False:
        errors.append("non_approval_receipt_claims_approval")
    if receipt.get("actual_user_input_used") is not False:
        errors.append("non_approval_receipt_uses_actual_user_input")
    if receipt.get("real_user_text_stored") is not False:
        errors.append("non_approval_receipt_real_user_text_stored")
    if receipt.get("formal_vault_accessed") is not False:
        errors.append("non_approval_receipt_formal_vault_accessed")
    if receipt.get("intake_gate_hash") and cfg.get("intake_gate_hash") and receipt.get("intake_gate_hash") != cfg.get("intake_gate_hash"):
        errors.append("non_approval_receipt_intake_gate_hash_mismatch")

    stop_text = "\n".join(cfg.get("stop_conditions", [])).lower()
    for required in [
        "actual user approval",
        "actual user decision",
        "real user text storage",
        "formal vault read",
        "formal vault write",
        "obsidian sync",
        "commit",
        "push",
        "promotion",
        "decision inferred",
        "future user exact text reference",
        "confirmation phrase",
        "packet hash mismatch",
        "source bundle hash mismatch",
        "scope hash mismatch",
        "rehearsal hash mismatch",
        "intake gate hash mismatch",
        "action basis",
        "denied or revise",
        "extra files",
        "dirty-state",
    ]:
        if required not in stop_text:
            errors.append(f"missing_stop_condition:{required}")

    authority_text = json.dumps(
        {
            "purpose": cfg.get("purpose", ""),
            "stop_conditions": cfg.get("stop_conditions", []),
            "non_claims": receipt.get("non_claims", []),
            "sample_text": [s.get("expected_gate_result", "") for s in samples],
        },
        ensure_ascii=False,
    ).lower()
    if any(pattern in authority_text for pattern in AUTHORITY_CONFUSING_PATTERNS):
        errors.append("authority_confusing_text")

    controls = cfg.get("inspector_controls", {})
    actual_inputs = {(item.get("id", ""), item.get("type", "")) for item in controls.get("inputs", [])}
    if actual_inputs != {("q", "search")}:
        errors.append("inspector_inputs_not_allowlisted")
    actual_buttons = {item.get("filter", "") for item in controls.get("buttons", [])}
    if actual_buttons != {"all", "contract", "approve_reference", "blocks", "receipt", "stops"}:
        errors.append("inspector_buttons_not_allowlisted")
    for button in controls.get("buttons", []):
        label = button.get("label", "").strip().lower()
        if label in {"approve", "save", "sync", "commit", "push", "write", "promote", "execute", "submit"}:
            errors.append(f"inspector_control_not_allowed:button:{label}")
    if cfg.get("product_metrics", {}).get("minimum_failure_cases", 0) < 64:
        errors.append("minimum_failure_cases_too_low")
    return sorted(set(errors))


def check_failure_cases() -> dict:
    oracle = load_json(root() / "artifact" / "failure-case-oracle.json")
    mismatches = []
    expected_files = {entry["file"] for entry in oracle}
    actual_files = {path.name for path in (root() / "failure-cases").glob("*.json")}
    for name in sorted(expected_files - actual_files):
        mismatches.append({"file": name, "missing": True})
    for name in sorted(actual_files - expected_files):
        mismatches.append({"file": name, "extra": True})
    for entry in oracle:
        path = root() / "failure-cases" / entry["file"]
        if not path.exists():
            continue
        errors = validate_config(load_json(path))
        missing = [code for code in entry["expected_failures"] if code not in errors]
        extra = [code for code in errors if code not in entry["expected_failures"]]
        if missing or extra:
            mismatches.append({"file": entry["file"], "missing_expected": missing, "extra": extra, "actual": errors})
    return {"count": len(oracle), "mismatches": mismatches}


def resolve_markdown_link(page: Path, target: str) -> Path | None:
    if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
        return None
    clean = target.split("#", 1)[0].replace("%20", " ")
    if not clean:
        return None
    return (page.parent / clean).resolve()


def page_links(page: Path) -> set[str]:
    text = page.read_text(encoding="utf-8")
    links = set(re.findall(r"\[\[([^\]]+)\]\]", text))
    links.update(match.group(1) for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text))
    if "user-decision-intake-gate-inspector.html" in text:
        links.add("user-decision-intake-gate-inspector.html")
    return links


def check_wikilinks(proto: Path) -> list[str]:
    issues = []
    pages = {path.stem for path in proto.glob("*.md")}
    for page in proto.glob("*.md"):
        for link in re.findall(r"\[\[([^\]]+)\]\]", page.read_text(encoding="utf-8")):
            target = link.split("|", 1)[0].split("#", 1)[0]
            if target not in pages:
                issues.append(f"broken_wikilink:{page.name}:{target}")
    return issues


def check_markdown_links(proto: Path) -> list[str]:
    issues = []
    for page in proto.rglob("*.md"):
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", page.read_text(encoding="utf-8")):
            target = match.group(1)
            resolved = resolve_markdown_link(page, target)
            if resolved is None:
                continue
            if not resolved.exists():
                issues.append(f"broken_markdown_link:{page.name}:{target}")
    return issues


def check_html(path: Path) -> dict:
    issues = []
    if not path.exists():
        return {"issues": ["html_missing"], "summary": {}}
    text = path.read_text(encoding="utf-8")
    parser = IntakeHTMLParser()
    parser.feed(text)
    summary = {
        "sandbox_only": parser.sandbox_only,
        "intake_gate_only": parser.intake_gate_only,
        "future_capture_only": parser.future_capture_only,
        "no_approval": parser.no_approval,
        "no_real_user_text_storage": parser.no_real_user_text_storage,
        "no_write": parser.no_write,
        "no_sync": parser.no_sync,
        "no_authority": parser.no_authority,
        "cards": len(parser.cards),
        "roles": sorted(parser.roles),
        "forms": parser.forms,
        "buttons": parser.buttons,
        "button_texts": parser.button_texts,
        "inputs": parser.inputs,
        "anchors": len(parser.anchors),
        "downloads": parser.downloads,
        "contenteditable": parser.contenteditable,
    }
    if not parser.sandbox_only:
        issues.append("html_missing_sandbox_marker")
    if not parser.intake_gate_only:
        issues.append("html_missing_intake_gate_marker")
    if not parser.future_capture_only:
        issues.append("html_missing_future_capture_marker")
    if not parser.no_approval:
        issues.append("html_missing_no_approval_marker")
    if not parser.no_real_user_text_storage:
        issues.append("html_missing_no_real_user_text_storage_marker")
    if not parser.no_write:
        issues.append("html_missing_no_write_marker")
    if not parser.no_sync:
        issues.append("html_missing_no_sync_marker")
    if not parser.no_authority:
        issues.append("html_missing_no_authority_marker")
    for role in ["intake-filter", "intake-cards", "boundary-rail"]:
        if role not in parser.roles:
            issues.append(f"html_missing_role:{role}")
    if parser.forms:
        issues.append("html_form_present")
    if parser.downloads:
        issues.append("html_download_link_present")
    if parser.contenteditable:
        issues.append("html_contenteditable_present")
    if parser.inputs != [{"id": "q", "type": "search", "name": ""}]:
        issues.append("html_inputs_not_allowlisted")
    if parser.buttons != ["all", "contract", "approve_reference", "blocks", "receipt", "stops"]:
        issues.append("html_buttons_not_allowlisted")
    for text_value in parser.button_texts:
        if text_value.strip().lower() in {"approve", "save", "sync", "commit", "push", "write", "promote", "execute", "submit"}:
            issues.append(f"html_write_or_approval_button_present:{text_value.strip().lower()}")
    if re.search(r"\b(fetch|XMLHttpRequest|sendBeacon|localStorage|sessionStorage)\b", text):
        issues.append("html_network_or_storage_api_present")
    if re.search(r"\b(approve|save|sync|write|commit|push|promote|execute|submit)\s*\(", text, flags=re.IGNORECASE):
        issues.append("html_write_or_approval_function_present")
    for anchor in parser.anchors:
        href = anchor.get("href", "").lower()
        if href.startswith(("http://", "https://", "mailto:", "javascript:")) or anchor.get("download"):
            issues.append("html_forbidden_anchor")
    try:
        data = json.loads(parser.script_text)
        if len(data.get("synthetic_intake_samples", [])) < 3:
            issues.append("html_embedded_samples_missing")
        if data.get("non_approval_receipt", {}).get("approval_collected_now") is not False:
            issues.append("html_embedded_receipt_claims_approval")
        if data.get("non_approval_receipt", {}).get("real_user_text_stored") is not False:
            issues.append("html_embedded_receipt_real_user_text_stored")
    except Exception as exc:
        issues.append(f"html_embedded_data_invalid:{exc}")
    lower = text.lower()
    for phrase in [
        "user decision intake gate draft only",
        "future capture only",
        "not actual approval",
        "approval not collected",
        "real user text not stored",
        "formal vault not accessed",
        "no formal vault write",
        "not action basis",
    ]:
        if phrase not in lower:
            issues.append(f"html_missing_boundary_phrase:{phrase}")
    return {"issues": sorted(set(issues)), "summary": summary}


def check_actual_journeys(proto: Path, html_ok: bool) -> dict:
    issues = []
    results = {}
    pages = {
        "home": proto / "00 User Decision Intake Gate Home.md",
        "contract": proto / "01 Future Decision Contract.md",
        "fields": proto / "02 Required Capture Fields.md",
        "approve": proto / "03 Future Approval Checklist.md",
        "blocks": proto / "04 Deny Or Revise Blocks.md",
        "receipt": proto / "05 Non Approval Receipt.md",
        "stops": proto / "06 Stop Conditions.md",
    }
    for key, path in pages.items():
        if not path.exists():
            issues.append(f"journey_missing_page:{key}")
    if issues:
        return {"results": results, "issues": issues}
    home_links = page_links(pages["home"])
    contract_text = " ".join(pages["contract"].read_text(encoding="utf-8").lower().split())
    approve_text = " ".join(pages["approve"].read_text(encoding="utf-8").lower().split())
    receipt_links = page_links(pages["receipt"])
    if "01 Future Decision Contract" not in home_links or "separate future execution slice" not in contract_text:
        issues.append("journey_path_missing:contract_review")
    else:
        results["contract_review"] = {"links_verified": True, "max_links": 2}
    if "02 Required Capture Fields" not in home_links or "03 Future Approval Checklist" not in home_links:
        issues.append("journey_path_missing:capture_to_approval_review")
    else:
        results["capture_to_approval_review"] = {"links_verified": True, "max_links": 2}
    if "not actionable in this slice" not in approve_text:
        issues.append("journey_path_missing:approval_non_actionable_review")
    else:
        results["approval_non_actionable_review"] = {"links_verified": True, "max_links": 1}
    if "06 Stop Conditions" not in receipt_links:
        issues.append("journey_path_missing:receipt_to_stops")
    else:
        results["receipt_to_stops"] = {"links_verified": True, "max_links": 2}
    if "user-decision-intake-gate-inspector.html" not in home_links or not html_ok:
        issues.append("journey_path_missing:inspector_review")
    else:
        results["inspector_review"] = {"links_verified": True, "max_links": 2, "html_allowlist_ok": html_ok}
    return {"results": results, "issues": issues}


def check_prototype(cfg: dict) -> dict:
    proto = root() / "prototype" / "formal-vault-user-decision-intake-gate"
    issues = []
    required = [
        "00 User Decision Intake Gate Home.md",
        "01 Future Decision Contract.md",
        "02 Required Capture Fields.md",
        "03 Future Approval Checklist.md",
        "04 Deny Or Revise Blocks.md",
        "05 Non Approval Receipt.md",
        "06 Stop Conditions.md",
        "07 Reviewer Packet.md",
        "user-decision-intake-gate-inspector.html",
        "Receipts/formal-vault-user-decision-intake-gate-receipt.json",
    ]
    for file in required:
        if not (proto / file).exists():
            issues.append(f"missing_prototype_file:{file}")
    for path in proto.rglob("*"):
        rel = path.relative_to(proto).as_posix()
        if path.suffix == ".base":
            issues.append(f"real_base_file_present:{rel}")
        if path.name == ".obsidian":
            issues.append("obsidian_config_present")
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            issues.append(f"python_cache_present:{rel}")
    if proto.exists():
        issues.extend(check_wikilinks(proto))
        issues.extend(check_markdown_links(proto))
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in proto.rglob("*")
        if path.is_file() and path.suffix in {".md", ".html", ".json"}
    )
    lower = text.lower()
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase.lower() not in lower:
            issues.append(f"prototype_missing_boundary_phrase:{phrase}")
    for pattern in AUTHORITY_CONFUSING_PATTERNS:
        if pattern in lower:
            issues.append(f"prototype_authority_confusing_text:{pattern}")

    receipt_summary = {}
    receipt_path = proto / "Receipts" / "formal-vault-user-decision-intake-gate-receipt.json"
    if receipt_path.exists():
        receipt = load_json(receipt_path)
        receipt_summary = {
            "slice_id": receipt.get("slice_id"),
            "source_slice": receipt.get("source_slice"),
            "formal_vault_accessed": receipt.get("formal_vault_accessed"),
            "approval_collected_now": receipt.get("approval_collected_now"),
            "actual_user_input_used": receipt.get("actual_user_input_used"),
            "real_user_text_stored": receipt.get("real_user_text_stored"),
            "source_hashes": len(receipt.get("source_hashes", {})),
            "sample_count": receipt.get("sample_count"),
        }
        if receipt.get("slice_id") != SLICE_ID:
            issues.append("receipt_wrong_slice_id")
        if receipt.get("source_slice") != SOURCE_SLICE_ID:
            issues.append("receipt_wrong_source_slice")
        if receipt.get("formal_vault_accessed") is not False:
            issues.append("receipt_formal_vault_accessed")
        if receipt.get("approval_collected_now") is not False:
            issues.append("receipt_approval_collected_now")
        if receipt.get("actual_user_input_used") is not False:
            issues.append("receipt_actual_user_input_used")
        if receipt.get("real_user_text_stored") is not False:
            issues.append("receipt_real_user_text_stored")
        if receipt.get("sample_count") != len(cfg.get("synthetic_intake_samples", [])):
            issues.append("receipt_sample_count_mismatch")
        if receipt.get("intake_gate_hash") != cfg.get("intake_gate_hash"):
            issues.append("receipt_intake_gate_hash_mismatch")
        forbidden = receipt.get("forbidden_operations", {})
        for op in FORBIDDEN_OPERATIONS:
            if op not in forbidden:
                issues.append(f"receipt_missing_forbidden_operation:{op}")
            elif forbidden.get(op) is not False:
                issues.append(f"receipt_forbidden_operation_true:{op}")
        for key, value in receipt.get("source_hashes", {}).items():
            if value == "missing":
                issues.append(f"receipt_missing_source_hash:{key}")

    html = check_html(proto / "user-decision-intake-gate-inspector.html")
    issues.extend(html["issues"])
    journeys = check_actual_journeys(proto, html_ok=not html["issues"])
    issues.extend(journeys["issues"])
    return {
        "prototype_path": str(proto),
        "issues": sorted(set(issues)),
        "receipt": receipt_summary,
        "html": html["summary"],
        "actual_journeys": journeys["results"],
    }


def check_source_status() -> dict:
    src = sandbox_root() / SOURCE_SLICE_ID
    product = src / "product-acceptance-report.md"
    next_step = src / "next-step.md"
    verification = src / "verification.md"
    issues = []
    product_status = frontmatter_status(product.read_text(encoding="utf-8")) if product.exists() else "missing"
    next_status = frontmatter_status(next_step.read_text(encoding="utf-8")) if next_step.exists() else "missing"
    verification_text = verification.read_text(encoding="utf-8") if verification.exists() else ""
    if product_status != "pass_product_grade":
        issues.append(f"source_product_not_pass:{product_status}")
    if next_status != "pass_product_grade_pending_user_next_slice_decision":
        issues.append(f"source_next_step_unexpected:{next_status}")
    if "passed: true" not in verification_text or "failure_cases: 61" not in verification_text:
        issues.append("source_final_gate_evidence_missing")
    return {"product_status": product_status, "next_status": next_status, "issues": issues}


def check_required_reports(final_gate: bool = False) -> dict:
    statuses = {}
    issues = []
    for name in [
        "slice-plan.md",
        "source-map.md",
        "verification.md",
        "reviewer-report.md",
        "boundary-audit.md",
        "product-acceptance-report.md",
        "next-step.md",
    ]:
        path = root() / name
        if not path.exists():
            issues.append(f"missing_required_report:{name}")
            continue
        statuses[name] = frontmatter_status(path.read_text(encoding="utf-8"))
    if final_gate:
        required = {
            "reviewer-report.md": "reviewer_pass",
            "boundary-audit.md": "boundary_pass",
            "product-acceptance-report.md": "pass_product_grade",
        }
        for name, expected in required.items():
            actual = statuses.get(name, "missing_status").lower()
            if actual != expected:
                issues.append(f"final_gate_bad_status:{name}:{actual}:expected:{expected}")
        actual_next = statuses.get("next-step.md", "missing_status").lower()
        if actual_next != "pass_product_grade_pending_user_next_slice_decision":
            issues.append(f"final_gate_bad_status:next-step.md:{actual_next}:expected:pass_product_grade_pending_user_next_slice_decision")
    return {"statuses": statuses, "issues": issues}


def run(rebuild: bool = False, final_gate: bool = False) -> dict:
    if rebuild:
        builder = load_builder()
        builder.build()
    fixtures = [
        root() / "fixtures" / "valid-user-decision-intake-gate-config.json",
        root() / "fixtures" / "valid-deny-user-decision-intake-config.json",
        root() / "fixtures" / "valid-revise-user-decision-intake-config.json",
    ]
    fixture_results = []
    for fixture in fixtures:
        fixture_results.append({"file": fixture.name, "errors": validate_config(load_json(fixture))})
    main_cfg = load_json(fixtures[0])
    failure_results = check_failure_cases()
    prototype_results = check_prototype(main_cfg)
    source_results = check_source_status()
    report_results = check_required_reports(final_gate=final_gate)
    failures = []
    if any(result["errors"] for result in fixture_results):
        failures.append("positive_fixture_errors")
    if failure_results["mismatches"]:
        failures.append("failure_case_mismatches")
    if failure_results["count"] < main_cfg.get("product_metrics", {}).get("minimum_failure_cases", 64):
        failures.append("too_few_failure_cases")
    if prototype_results["issues"]:
        failures.append("prototype_issues")
    if source_results["issues"]:
        failures.append("source_status_issues")
    if report_results["issues"]:
        failures.append("required_report_issues")
    return {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "rebuild": rebuild,
        "final_gate": final_gate,
        "passed": not failures,
        "failures": failures,
        "positive_fixtures": fixture_results,
        "failure_cases": failure_results,
        "prototype": prototype_results,
        "source_status": source_results,
        "required_reports": report_results,
        "non_claims": [
            "sandbox verification only",
            "not actual approval",
            "not a user decision record",
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "not mainline approval",
            "not formal vault approval",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = run(rebuild=args.rebuild, final_gate=args.final_gate)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
