from __future__ import annotations

import argparse
import hashlib
import html.parser
import importlib.util
import json
import re
import sys
from pathlib import Path


SLICE_ID = "2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox"

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
    "user_approval_inference",
    "action_basis_creation",
    "reviewed_knowledge_creation",
    "external_notification",
]
REQUIRED_BOUNDARY_PHRASES = [
    "sandbox only",
    "decision rehearsal only",
    "synthetic decisions only",
    "not actual approval",
    "approval not collected",
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
]
AUTHORITY_CONFUSING_PATTERNS = [
    "synthetic approval creates action basis",
    "approval collected now",
    "formal vault approval granted",
    "action basis approved",
    "ready to write formal vault",
    "reviewed truth",
    "merge approved",
    "sync approved",
    "promotion approved",
]


class RehearsalHTMLParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sandbox_only = False
        self.rehearsal_only = False
        self.synthetic_only = False
        self.no_approval = False
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
            self.rehearsal_only = attr.get("data-decision-rehearsal-only") == "true"
            self.synthetic_only = attr.get("data-synthetic-only") == "true"
            self.no_approval = attr.get("data-no-approval") == "true"
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
        if tag == "script" and attr.get("id") == "rehearsal-data":
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
    path = root() / "artifact" / "decision_rehearsal_builder.py"
    spec = importlib.util.spec_from_file_location("decision_rehearsal_builder", path)
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


def rehearsal_material(cfg: dict) -> dict:
    scenarios = []
    for scenario in cfg.get("decision_scenarios", []):
        item = dict(scenario)
        item.pop("required_rehearsal_hash", None)
        scenarios.append(item)
    receipt = dict(cfg.get("non_approval_receipt", {}))
    receipt.pop("rehearsal_hash", None)
    return {
        "rehearsal_version": cfg.get("rehearsal_version"),
        "source_slice": cfg.get("source_slice"),
        "source_input_bundle_hash": cfg.get("source_input_bundle_hash"),
        "source_packet_hash": cfg.get("source_packet_hash"),
        "source_packet_source_bundle_hash": cfg.get("source_packet_source_bundle_hash"),
        "source_packet_scope_hash": cfg.get("source_packet_scope_hash"),
        "decision_rules": cfg.get("decision_rules", {}),
        "decision_scenarios": scenarios,
        "non_approval_receipt": receipt,
        "stop_conditions": cfg.get("stop_conditions", []),
    }


def source_packet_config() -> dict:
    return load_json(sandbox_root() / SOURCE_SLICE_ID / "fixtures" / "valid-approval-packet-config.json")


def validate_source_path(source_path: str, expected_prefix: str, fid: str, errors: list[str]) -> None:
    if not source_path:
        errors.append(f"source_input_path_missing:{fid}")
        return
    normalized = source_path.replace("\\", "/")
    if is_bad_target(normalized) or not normalized.startswith(expected_prefix):
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


def validate_config(cfg: dict) -> list[str]:
    errors: list[str] = []
    source_cfg = source_packet_config()
    if cfg.get("slice_id") != SLICE_ID:
        errors.append("wrong_slice_id")
    if cfg.get("source_slice") != SOURCE_SLICE_ID:
        errors.append("wrong_source_slice")
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

    source_prefix = f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/"
    for item in cfg.get("source_inputs", []):
        fid = item.get("id", "unknown")
        source_path = item.get("source_path", "")
        validate_source_path(source_path, source_prefix, fid, errors)
        if source_path and f"source_input_path_invalid:{fid}" not in errors and f"source_input_missing:{fid}" not in errors:
            actual = sha256(workspace_root() / source_path.replace("\\", "/"))
            if item.get("source_sha256") != actual:
                errors.append(f"source_input_hash_mismatch:{fid}")
        if item.get("content_binding") != "exact_source_sha256":
            errors.append(f"source_input_content_binding_missing:{fid}")
    if cfg.get("source_input_bundle_hash") != sha256_json(cfg.get("source_inputs", [])):
        errors.append("source_input_bundle_hash_mismatch")
    if cfg.get("source_packet_hash") != source_cfg.get("packet_hash"):
        errors.append("source_packet_hash_mismatch")
    if cfg.get("source_packet_source_bundle_hash") != source_cfg.get("source_bundle_hash"):
        errors.append("source_packet_source_bundle_hash_mismatch")
    if cfg.get("source_packet_scope_hash") != source_cfg.get("approval_scope", {}).get("scope_hash"):
        errors.append("source_packet_scope_hash_mismatch")

    if cfg.get("rehearsal_hash_material") != rehearsal_material(cfg):
        errors.append("rehearsal_hash_material_mismatch")
    expected_rehearsal_hash = sha256_json(rehearsal_material(cfg))
    if not cfg.get("rehearsal_hash"):
        errors.append("rehearsal_hash_missing")
    elif cfg.get("rehearsal_hash") != expected_rehearsal_hash:
        errors.append("rehearsal_hash_mismatch")

    rules = cfg.get("decision_rules", {})
    if rules.get("synthetic_only") is not True:
        errors.append("rule_not_synthetic_only")
    if rules.get("actual_user_input_disallowed") is not True:
        errors.append("rule_allows_actual_user_input")
    if rules.get("actual_approval_collection_disallowed") is not True:
        errors.append("rule_allows_actual_approval_collection")
    if rules.get("approved_outcome_not_actionable") is not True:
        errors.append("rule_allows_approved_outcome_actionable")
    if rules.get("requires_packet_hash") != cfg.get("source_packet_hash"):
        errors.append("rule_packet_hash_mismatch")
    if rules.get("requires_source_bundle_hash") != cfg.get("source_packet_source_bundle_hash"):
        errors.append("rule_source_bundle_hash_mismatch")
    if rules.get("requires_scope_hash") != cfg.get("source_packet_scope_hash"):
        errors.append("rule_scope_hash_mismatch")
    if rules.get("deny_always_blocks_write") is not True:
        errors.append("rule_deny_does_not_block")
    if rules.get("revise_always_blocks_write") is not True:
        errors.append("rule_revise_does_not_block")
    if rules.get("rollback_and_hash_ack_required_for_approved") is not True:
        errors.append("rule_missing_rollback_hash_ack")

    scenarios = cfg.get("decision_scenarios", [])
    ids = {item.get("id") for item in scenarios}
    required_ids = {"synthetic_approve_exact_packet", "synthetic_deny_write", "synthetic_needs_revision"}
    for required in required_ids:
        if required not in ids:
            errors.append(f"missing_decision_scenario:{required}")
    if len(scenarios) < cfg.get("product_metrics", {}).get("required_decision_scenarios", 3):
        errors.append("too_few_decision_scenarios")

    required_qids = set(rules.get("requires_all_question_ids_for_approved", []))
    for item in scenarios:
        sid = item.get("id", "unknown")
        verdict = item.get("decision_verdict")
        if item.get("synthetic_only") is not True:
            errors.append(f"scenario_not_synthetic:{sid}")
        if item.get("actual_user_input") is not False:
            errors.append(f"scenario_uses_actual_user_input:{sid}")
        if item.get("user_approval_text_present") is not False:
            errors.append(f"scenario_has_actual_user_text:{sid}")
        if item.get("approval_collected_now") is not False:
            errors.append(f"scenario_collects_approval_now:{sid}")
        if item.get("formal_vault_accessed") is not False:
            errors.append(f"scenario_accesses_formal_vault:{sid}")
        if item.get("formal_vault_write_allowed_now") is not False:
            if verdict == "DENIED_BY_USER":
                errors.append(f"denied_scenario_allows_write:{sid}")
            elif verdict == "NEEDS_REVISION":
                errors.append(f"revise_scenario_allows_write:{sid}")
            else:
                errors.append(f"scenario_allows_formal_vault_write_now:{sid}")
        if item.get("action_basis_created") is not False:
            errors.append(f"scenario_creates_action_basis:{sid}")
        if item.get("reviewed_knowledge_created") is not False:
            errors.append(f"scenario_creates_reviewed_knowledge:{sid}")
        for field, code in [
            ("sync_allowed", "scenario_allows_sync"),
            ("commit_allowed", "scenario_allows_commit"),
            ("push_allowed", "scenario_allows_push"),
            ("promotion_allowed", "scenario_allows_promotion"),
        ]:
            if item.get(field) is not False:
                errors.append(f"{code}:{sid}")
        if item.get("extra_files_requested") is not False:
            errors.append(f"scenario_extra_files_requested:{sid}")
        hashes = item.get("hash_claims", {})
        if hashes.get("packet_hash") != cfg.get("source_packet_hash"):
            errors.append(f"scenario_packet_hash_mismatch:{sid}")
        if hashes.get("source_bundle_hash") != cfg.get("source_packet_source_bundle_hash"):
            errors.append(f"scenario_source_bundle_hash_mismatch:{sid}")
        if hashes.get("scope_hash") != cfg.get("source_packet_scope_hash"):
            errors.append(f"scenario_scope_hash_mismatch:{sid}")
        if verdict == "APPROVED_BY_USER":
            confirmed = set(item.get("confirmed_question_ids", []))
            for qid in required_qids:
                if qid not in confirmed:
                    errors.append(f"approved_missing_required_question:{sid}:{qid}")
            if item.get("expected_result") == "READY_TO_WRITE":
                errors.append(f"approved_scenario_result_actionable:{sid}")
            if item.get("expected_result") != "SIMULATED_APPROVAL_VALID_BUT_NOT_ACTIONABLE":
                errors.append(f"approved_scenario_result_bad:{sid}")
            if item.get("rollback_ack") is not True:
                errors.append(f"approved_missing_rollback_ack:{sid}")
            if item.get("hash_ack") is not True:
                errors.append(f"approved_missing_hash_ack:{sid}")
            if item.get("dirty_state_ack") is not True:
                errors.append(f"approved_missing_dirty_state_ack:{sid}")
        if verdict == "DENIED_BY_USER" and item.get("expected_result") != "BLOCKED_BY_SYNTHETIC_DENIAL":
            errors.append(f"denied_scenario_result_bad:{sid}")
        if verdict == "NEEDS_REVISION" and item.get("expected_result") != "BLOCKED_PENDING_PACKET_REVISION":
            errors.append(f"revise_scenario_result_bad:{sid}")

    receipt = cfg.get("non_approval_receipt", {})
    if receipt.get("approval_collected_now") is not False:
        errors.append("non_approval_receipt_claims_approval")
    if receipt.get("actual_user_input_used") is not False:
        errors.append("non_approval_receipt_uses_actual_user_input")
    if receipt.get("formal_vault_accessed") is not False:
        errors.append("non_approval_receipt_formal_vault_accessed")
    if receipt.get("rehearsal_hash") and cfg.get("rehearsal_hash") and receipt.get("rehearsal_hash") != cfg.get("rehearsal_hash"):
        errors.append("non_approval_receipt_rehearsal_hash_mismatch")

    stop_text = "\n".join(cfg.get("stop_conditions", [])).lower()
    for required in ["actual user approval", "formal vault read", "formal vault write", "obsidian sync", "commit", "push", "promotion", "packet hash mismatch", "source bundle hash mismatch", "scope hash mismatch", "rehearsal hash mismatch", "action basis", "denied or revise", "extra files"]:
        if required not in stop_text:
            errors.append(f"missing_stop_condition:{required}")
    authority_text = json.dumps(
        {
            "purpose": cfg.get("purpose", ""),
            "stop_conditions": cfg.get("stop_conditions", []),
            "non_claims": receipt.get("non_claims", []),
            "scenario_text": [s.get("synthetic_user_text", "") for s in scenarios],
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
    if actual_buttons != {"all", "scenarios", "rules", "receipt", "stops"}:
        errors.append("inspector_buttons_not_allowlisted")
    for button in controls.get("buttons", []):
        label = button.get("label", "").strip().lower()
        if label in {"approve", "save", "sync", "commit", "push", "write", "promote", "execute", "submit"}:
            errors.append(f"inspector_control_not_allowed:button:{label}")
    if cfg.get("product_metrics", {}).get("minimum_failure_cases", 0) < 54:
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
    if "decision-rehearsal-inspector.html" in text:
        links.add("decision-rehearsal-inspector.html")
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
    parser = RehearsalHTMLParser()
    parser.feed(text)
    summary = {
        "sandbox_only": parser.sandbox_only,
        "rehearsal_only": parser.rehearsal_only,
        "synthetic_only": parser.synthetic_only,
        "no_approval": parser.no_approval,
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
    if not parser.rehearsal_only:
        issues.append("html_missing_rehearsal_marker")
    if not parser.synthetic_only:
        issues.append("html_missing_synthetic_marker")
    if not parser.no_approval:
        issues.append("html_missing_no_approval_marker")
    if not parser.no_write:
        issues.append("html_missing_no_write_marker")
    if not parser.no_sync:
        issues.append("html_missing_no_sync_marker")
    if not parser.no_authority:
        issues.append("html_missing_no_authority_marker")
    for role in ["rehearsal-filter", "rehearsal-cards", "boundary-rail"]:
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
    if parser.buttons != ["all", "scenarios", "rules", "receipt", "stops"]:
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
        if len(data.get("decision_scenarios", [])) < 3:
            issues.append("html_embedded_scenarios_missing")
        if data.get("non_approval_receipt", {}).get("approval_collected_now") is not False:
            issues.append("html_embedded_receipt_claims_approval")
    except Exception as exc:
        issues.append(f"html_embedded_data_invalid:{exc}")
    lower = text.lower()
    for phrase in ["decision rehearsal only", "synthetic decisions only", "not actual approval", "approval not collected", "formal vault not accessed", "no formal vault write", "not action basis"]:
        if phrase not in lower:
            issues.append(f"html_missing_boundary_phrase:{phrase}")
    return {"issues": sorted(set(issues)), "summary": summary}


def check_actual_journeys(proto: Path, html_ok: bool) -> dict:
    issues = []
    results = {}
    pages = {
        "home": proto / "00 Decision Rehearsal Home.md",
        "matrix": proto / "01 Scenario Matrix.md",
        "approval": proto / "02 Synthetic Approval Rehearsal.md",
        "denial": proto / "03 Synthetic Denial Rehearsal.md",
        "revision": proto / "04 Synthetic Revision Rehearsal.md",
        "rules": proto / "05 Decision Rules.md",
        "receipt": proto / "06 Non Approval Receipt.md",
        "stops": proto / "07 Stop Conditions.md",
    }
    for key, path in pages.items():
        if not path.exists():
            issues.append(f"journey_missing_page:{key}")
    if issues:
        return {"results": results, "issues": issues}
    home_links = page_links(pages["home"])
    matrix_links = page_links(pages["matrix"])
    approval_links = page_links(pages["approval"])
    rules_text = pages["rules"].read_text(encoding="utf-8").lower()
    receipt_links = page_links(pages["receipt"])
    if "01 Scenario Matrix" not in home_links or "07 Stop Conditions" not in matrix_links:
        issues.append("journey_path_missing:scenario_review")
    else:
        results["scenario_review"] = {"links_verified": True, "max_links": 2}
    if "02 Synthetic Approval Rehearsal" not in home_links or "07 Stop Conditions" not in approval_links:
        issues.append("journey_path_missing:approval_rehearsal_review")
    else:
        results["approval_rehearsal_review"] = {"links_verified": True, "max_links": 2}
    if "05 Decision Rules" not in home_links or "not approve" not in rules_text:
        issues.append("journey_path_missing:rules_review")
    else:
        results["rules_review"] = {"links_verified": True, "max_links": 2}
    if "06 Non Approval Receipt" not in home_links or "07 Stop Conditions" not in receipt_links:
        issues.append("journey_path_missing:receipt_review")
    else:
        results["receipt_review"] = {"links_verified": True, "max_links": 2}
    if "decision-rehearsal-inspector.html" not in home_links or not html_ok:
        issues.append("journey_path_missing:inspector_review")
    else:
        results["inspector_review"] = {"links_verified": True, "max_links": 2, "html_allowlist_ok": html_ok}
    return {"results": results, "issues": issues}


def check_prototype(cfg: dict) -> dict:
    proto = root() / "prototype" / "formal-vault-write-decision-rehearsal"
    issues = []
    required = [
        "00 Decision Rehearsal Home.md",
        "01 Scenario Matrix.md",
        "02 Synthetic Approval Rehearsal.md",
        "03 Synthetic Denial Rehearsal.md",
        "04 Synthetic Revision Rehearsal.md",
        "05 Decision Rules.md",
        "06 Non Approval Receipt.md",
        "07 Stop Conditions.md",
        "08 Reviewer Packet.md",
        "decision-rehearsal-inspector.html",
        "Receipts/formal-vault-write-decision-rehearsal-receipt.json",
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
    receipt_path = proto / "Receipts" / "formal-vault-write-decision-rehearsal-receipt.json"
    if receipt_path.exists():
        receipt = load_json(receipt_path)
        receipt_summary = {
            "slice_id": receipt.get("slice_id"),
            "source_slice": receipt.get("source_slice"),
            "formal_vault_accessed": receipt.get("formal_vault_accessed"),
            "approval_collected_now": receipt.get("approval_collected_now"),
            "actual_user_input_used": receipt.get("actual_user_input_used"),
            "source_hashes": len(receipt.get("source_hashes", {})),
            "scenario_count": receipt.get("scenario_count"),
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
        if receipt.get("scenario_count") != len(cfg.get("decision_scenarios", [])):
            issues.append("receipt_scenario_count_mismatch")
        if receipt.get("rehearsal_hash") != cfg.get("rehearsal_hash"):
            issues.append("receipt_rehearsal_hash_mismatch")
        forbidden = receipt.get("forbidden_operations", {})
        for op in FORBIDDEN_OPERATIONS:
            if op not in forbidden:
                issues.append(f"receipt_missing_forbidden_operation:{op}")
            elif forbidden.get(op) is not False:
                issues.append(f"receipt_forbidden_operation_true:{op}")
        for key, value in receipt.get("source_hashes", {}).items():
            if value == "missing":
                issues.append(f"receipt_missing_source_hash:{key}")
    html = check_html(proto / "decision-rehearsal-inspector.html")
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
    if "passed: true" not in verification_text or "failure_cases: 49" not in verification_text:
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
        root() / "fixtures" / "valid-decision-rehearsal-config.json",
        root() / "fixtures" / "valid-denial-rehearsal-config.json",
        root() / "fixtures" / "valid-revision-rehearsal-config.json",
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
    if failure_results["count"] < main_cfg.get("product_metrics", {}).get("minimum_failure_cases", 54):
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
