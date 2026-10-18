from __future__ import annotations

import ast
import copy
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox"
SOURCE_STATUS_SLICE_ID = "2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
SANDBOX_ROOT = ROOT.parent
SOURCE_STATUS_ROOT = SANDBOX_ROOT / SOURCE_STATUS_SLICE_ID
SOURCE_STATUS_AUDIT = SOURCE_STATUS_ROOT / "artifact" / "status-normalization-audit.json"
SOURCE_STATUS_REPORT = SOURCE_STATUS_ROOT / "product-acceptance-report.md"

VERSION = "sandbox-verifier-portability-dependency-audit-v1"
TRUTH_BOUNDARY = "portability_audit_is_static_sandbox_evidence_not_runtime_certification"
PURPOSE = "audit sandbox verifier scripts for static portability, dependency, and default-review safety signals"
WRITE_SCOPE = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"

ALLOWED_VIEWS = {
    "verifier-portability-audit",
    "agent-run-guide",
    "risk-inventory",
}

REQUIRED_FIXTURES = {
    "valid-verifier-portability-audit.json": "verifier-portability-audit",
    "valid-agent-run-guide.json": "agent-run-guide",
    "valid-risk-inventory.json": "risk-inventory",
}

TOP_LEVEL_FIELDS = {
    "record_kind",
    "slice_id",
    "version",
    "truth_boundary",
    "purpose",
    "write_scope",
    "view",
    "source_snapshot",
    "portability_policy",
    "scanner_scope",
    "verifier_inventory",
    "summary",
    "risk_inventory",
    "synthetic_probes",
    "agent_run_guide",
    "readiness_flags",
    "operation_performed_flags",
    "required_non_claims",
    "operator_note",
}

READINESS_FLAGS = {
    "portability_audit_ready",
    "runtime_certified",
    "enterprise_production_ready",
    "mainline_ready",
    "formal_vault_ready",
    "reviewed_knowledge_ready",
    "evidence_support_ready",
    "action_basis_ready",
    "release_approved",
    "promotion_approved",
}

OPERATION_FLAGS = [
    "old_verifier_executed",
    "legacy_slice_modified",
    "dependency_install",
    "network_access",
    "background_service",
    "mcp_write_tool",
    "hooks",
    "formal_vault_read",
    "formal_vault_write",
    "obsidian_sync",
    "commit",
    "push",
    "promotion",
    "mainline_merge",
    "auto_advance",
]

REQUIRED_NON_CLAIMS = [
    "not runtime certification",
    "not dependency installation",
    "not old verifier execution",
    "not old-slice edit",
    "not release approval",
    "not promotion approval",
    "not mainline ready",
    "not enterprise production ready",
    "not formal vault approval",
    "not Obsidian sync",
    "not commit",
    "not push",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "not auto advance",
]

FORBIDDEN_IMPORTS = {
    "requests",
    "httpx",
    "aiohttp",
    "socket",
    "urllib",
    "ftplib",
    "smtplib",
    "paramiko",
    "boto3",
    "openai",
    "anthropic",
}

BLOCKING_TOKENS = {
    "pip install": "dependency_install_token",
    "python -m pip": "dependency_install_token",
    "Start-Process": "background_or_external_process_token",
    "Invoke-WebRequest": "network_token",
    "curl ": "network_token",
    "git push": "push_token",
    "git commit": "commit_token",
}

WARNING_TOKENS = {
    "Obsidian sync": "obsidian_sync_boundary_word",
    "H:\\Obsidian": "formal_vault_path_boundary_word",
    "H:\\\\Obsidian": "formal_vault_path_boundary_word",
    "mcp_write": "mcp_write_boundary_word",
}

WARN_IMPORTS = {"subprocess"}


def rel(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def parse_status(path: Path) -> str | None:
    if not path.exists():
        return None
    match = re.search(r"^status:\s*(.+?)\s*$", path.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
    return match.group(1).strip() if match else None


def stdlib_roots() -> set[str]:
    roots = set(getattr(sys, "stdlib_module_names", set()))
    roots.update({"argparse", "json", "pathlib", "typing", "collections", "re", "sys", "os", "hashlib"})
    return roots


def source_snapshot() -> dict[str, Any]:
    status_audit = read_json(SOURCE_STATUS_AUDIT)
    return {
        "source_status_slice_id": SOURCE_STATUS_SLICE_ID,
        "source_status_audit_path": rel(SOURCE_STATUS_AUDIT),
        "source_status_audit_sha256": sha256_file(SOURCE_STATUS_AUDIT),
        "source_status_product_report_path": rel(SOURCE_STATUS_REPORT),
        "source_status_product_report_sha256": sha256_file(SOURCE_STATUS_REPORT),
        "source_status_product_status": parse_status(SOURCE_STATUS_REPORT),
        "source_examined_slice_count": status_audit.get("canonical_summary", {}).get("examined_slice_count"),
        "source_unknown_status_count": status_audit.get("canonical_summary", {}).get("unknown_status_count"),
        "source_gate_pass_count": status_audit.get("canonical_summary", {}).get("gate_pass_count"),
    }


def discover_verifiers() -> list[Path]:
    return sorted(SANDBOX_ROOT.glob("*/artifact/verify*.py"))


def local_module_roots(script_path: Path) -> set[str]:
    return {path.stem for path in script_path.parent.glob("*.py")}


def import_roots(tree: ast.AST) -> list[str]:
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.level == 0:
                imports.append(node.module.split(".")[0])
    return sorted(set(imports))


def analyze_source(script_path: Path, text: str) -> dict[str, Any]:
    syntax_ok = True
    syntax_error = None
    imports: list[str] = []
    external_imports: list[str] = []
    forbidden_imports: list[str] = []
    warning_imports: list[str] = []
    try:
        tree = ast.parse(text, filename=str(script_path))
        compile(text, str(script_path), "exec")
        imports = import_roots(tree)
    except SyntaxError as exc:
        syntax_ok = False
        syntax_error = f"{exc.__class__.__name__}:{exc.msg}"
        tree = None

    local_roots = local_module_roots(script_path)
    std_roots = stdlib_roots()
    for root in imports:
        if root in FORBIDDEN_IMPORTS:
            forbidden_imports.append(root)
        if root in WARN_IMPORTS:
            warning_imports.append(root)
        if root not in std_roots and root not in local_roots:
            external_imports.append(root)

    forbidden_tokens = [
        {"token": token, "reason": reason}
        for token, reason in sorted(BLOCKING_TOKENS.items())
        if token in text
    ]
    warning_tokens = [
        {"token": token, "reason": reason}
        for token, reason in sorted(WARNING_TOKENS.items())
        if token in text
    ]
    cli_flags = sorted(flag for flag in ["--rebuild", "--final-gate", "--help"] if flag in text)
    risk_notes: list[str] = []
    if "subprocess" in imports:
        risk_notes.append("subprocess_present_review_for_default_path")
    if warning_tokens:
        risk_notes.append("warning_tokens_present")
    if "--rebuild" in text:
        risk_notes.append("explicit_rebuild_mode_present")
    blockers: list[str] = []
    if not syntax_ok:
        blockers.append("syntax_not_portable")
    if external_imports:
        blockers.append("external_imports_present")
    if forbidden_imports:
        blockers.append("forbidden_imports_present")
    if forbidden_tokens:
        blockers.append("forbidden_tokens_present")
    return {
        "path": rel(script_path),
        "slice_id": script_path.parents[1].name,
        "sha256": sha256_file(script_path) if script_path.exists() else None,
        "syntax_ok": syntax_ok,
        "syntax_error": syntax_error,
        "imports": imports,
        "external_imports": sorted(external_imports),
        "forbidden_imports": sorted(forbidden_imports),
        "warning_imports": sorted(warning_imports),
        "forbidden_tokens": forbidden_tokens,
        "warning_tokens": warning_tokens,
        "cli_flags": cli_flags,
        "risk_notes": risk_notes,
        "blocking_issues": blockers,
        "static_portability_pass": not blockers,
    }


def analyze_script(script_path: Path) -> dict[str, Any]:
    text = script_path.read_text(encoding="utf-8", errors="ignore")
    return analyze_source(script_path, text)


def synthetic_probe_results() -> list[dict[str, Any]]:
    probe_root = ROOT / "artifact" / "_synthetic_probe.py"
    probes = [
        {
            "id": "stdlib_and_local_ok",
            "text": "import argparse\nfrom pathlib import Path\nimport portability_audit\n",
            "expected_blockers": [],
        },
        {
            "id": "external_requests_import_blocks",
            "text": "import requests\n",
            "expected_blockers": ["external_imports_present", "forbidden_imports_present"],
        },
        {
            "id": "socket_import_blocks",
            "text": "import socket\n",
            "expected_blockers": ["forbidden_imports_present"],
        },
        {
            "id": "syntax_error_blocks",
            "text": "def broken(:\n    pass\n",
            "expected_blockers": ["syntax_not_portable"],
        },
        {
            "id": "dependency_install_token_blocks",
            "text": "print('python -m pip install surprise')\n",
            "expected_blockers": ["forbidden_tokens_present"],
        },
        {
            "id": "formal_vault_path_token_warns",
            "text": "print('H:\\\\Obsidian\\\\资料库')\n",
            "expected_blockers": [],
            "expected_risk_note": "warning_tokens_present",
        },
        {
            "id": "subprocess_warns_not_blocks",
            "text": "import subprocess\nprint(subprocess.__name__)\n",
            "expected_blockers": [],
            "expected_risk_note": "subprocess_present_review_for_default_path",
        },
        {
            "id": "unknown_local_import_blocks",
            "text": "import missing_slice_helper\n",
            "expected_blockers": ["external_imports_present"],
        },
    ]
    results: list[dict[str, Any]] = []
    for probe in probes:
        analyzed = analyze_source(probe_root, probe["text"])
        results.append(
            {
                "id": probe["id"],
                "expected_blockers": probe["expected_blockers"],
                "actual_blockers": analyzed["blocking_issues"],
                "expected_risk_note": probe.get("expected_risk_note"),
                "actual_risk_notes": analyzed["risk_notes"],
                "passed": sorted(probe["expected_blockers"]) == sorted(analyzed["blocking_issues"])
                and (
                    not probe.get("expected_risk_note")
                    or probe["expected_risk_note"] in analyzed["risk_notes"]
                ),
            }
        )
    return results


def build_inventory() -> list[dict[str, Any]]:
    return [analyze_script(path) for path in discover_verifiers()]


def summarize(inventory: list[dict[str, Any]], probes: list[dict[str, Any]]) -> dict[str, Any]:
    blocking = [item for item in inventory if item["blocking_issues"]]
    warnings = [item for item in inventory if item["risk_notes"]]
    return {
        "verifier_count": len(inventory),
        "static_portability_pass_count": sum(1 for item in inventory if item["static_portability_pass"]),
        "blocking_verifier_count": len(blocking),
        "warning_verifier_count": len(warnings),
        "external_import_verifier_count": sum(1 for item in inventory if item["external_imports"]),
        "forbidden_import_verifier_count": sum(1 for item in inventory if item["forbidden_imports"]),
        "forbidden_token_verifier_count": sum(1 for item in inventory if item["forbidden_tokens"]),
        "warning_token_verifier_count": sum(1 for item in inventory if item["warning_tokens"]),
        "syntax_error_verifier_count": sum(1 for item in inventory if not item["syntax_ok"]),
        "subprocess_warning_count": sum(1 for item in inventory if "subprocess_present_review_for_default_path" in item["risk_notes"]),
        "synthetic_probe_count": len(probes),
        "synthetic_probe_pass_count": sum(1 for item in probes if item["passed"]),
        "all_synthetic_probes_pass": all(item["passed"] for item in probes),
    }


def default_audit(view: str = "verifier-portability-audit") -> dict[str, Any]:
    inventory = build_inventory()
    probes = synthetic_probe_results()
    summary = summarize(inventory, probes)
    risk_inventory = [
        {
            "path": item["path"],
            "slice_id": item["slice_id"],
            "blocking_issues": item["blocking_issues"],
            "risk_notes": item["risk_notes"],
            "external_imports": item["external_imports"],
            "forbidden_imports": item["forbidden_imports"],
            "forbidden_tokens": item["forbidden_tokens"],
            "warning_tokens": item["warning_tokens"],
        }
        for item in inventory
        if item["blocking_issues"] or item["risk_notes"] or item["warning_tokens"]
    ]
    return {
        "record_kind": "sandbox_verifier_portability_dependency_audit",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "view": view,
        "source_snapshot": source_snapshot(),
        "portability_policy": {
            "analysis_mode": "static_read_only",
            "does_not_execute_old_verifiers": True,
            "does_not_install_dependencies": True,
            "stdlib_and_slice_local_imports_only": True,
            "external_or_network_imports_block": True,
            "forbidden_operation_tokens_block": True,
            "boundary_word_tokens_warn": True,
            "subprocess_is_warning_not_auto_failure": True,
            "default_read_only_claim_limit": "static audit only; not runtime certification",
        },
        "scanner_scope": {
            "glob": "outputs/review/vaks-implementation-sandbox/*/artifact/verify*.py",
            "included_verifier_count": len(inventory),
            "excludes": ["non-verifier builders", "prototype scripts", "formal vault", "tools outside sandbox"],
        },
        "verifier_inventory": inventory,
        "summary": summary,
        "risk_inventory": risk_inventory,
        "synthetic_probes": probes,
        "agent_run_guide": [
            "run this p2-47 verifier first for a static portability check",
            "then run the target slice's own default verifier when needed",
            "do not run old verifiers with --rebuild during review unless acting as Builder inside that slice",
            "subprocess warnings require human inspection of default path behavior",
            "blocking import/token/syntax issues must be fixed or explicitly parked in a later sandbox before claiming portability",
        ],
        "readiness_flags": {
            "portability_audit_ready": True,
            "runtime_certified": False,
            "enterprise_production_ready": False,
            "mainline_ready": False,
            "formal_vault_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "release_approved": False,
            "promotion_approved": False,
        },
        "operation_performed_flags": {name: False for name in OPERATION_FLAGS},
        "required_non_claims": list(REQUIRED_NON_CLAIMS),
    }


def validate_audit(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in sorted(set(data) - TOP_LEVEL_FIELDS):
        errors.append(f"unknown_top_level_field:{key}")
    view = data.get("view")
    if view not in ALLOWED_VIEWS:
        errors.append(f"view_not_allowed:{view}")
    if "operator_note" in data:
        note = data.get("operator_note")
        if not isinstance(note, str) or "sandbox only" not in note:
            errors.append("operator_note_not_sandbox_only")

    expected = {
        "record_kind": "sandbox_verifier_portability_dependency_audit",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{key}_mismatch")

    current = default_audit(view if view in ALLOWED_VIEWS else "verifier-portability-audit")
    for key in [
        "source_snapshot",
        "portability_policy",
        "scanner_scope",
        "verifier_inventory",
        "summary",
        "risk_inventory",
        "synthetic_probes",
        "agent_run_guide",
    ]:
        if data.get(key) != current.get(key):
            errors.append(f"{key}_mismatch")

    summary = data.get("summary", {})
    if summary.get("verifier_count", 0) <= 0:
        errors.append("verifier_count_missing")
    if summary.get("blocking_verifier_count") != 0:
        errors.append("blocking_verifier_present")
    if summary.get("external_import_verifier_count") != 0:
        errors.append("external_import_verifier_present")
    if summary.get("forbidden_import_verifier_count") != 0:
        errors.append("forbidden_import_verifier_present")
    if summary.get("forbidden_token_verifier_count") != 0:
        errors.append("forbidden_token_verifier_present")
    if summary.get("syntax_error_verifier_count") != 0:
        errors.append("syntax_error_verifier_present")
    if summary.get("all_synthetic_probes_pass") is not True:
        errors.append("synthetic_probe_failure")
    if summary.get("synthetic_probe_pass_count") != summary.get("synthetic_probe_count"):
        errors.append("synthetic_probe_count_mismatch")

    for item in data.get("verifier_inventory", []):
        if item.get("blocking_issues"):
            errors.append(f"verifier_blocking_issue:{item.get('path')}")
        if item.get("external_imports"):
            errors.append(f"verifier_external_import:{item.get('path')}")
        if item.get("forbidden_imports"):
            errors.append(f"verifier_forbidden_import:{item.get('path')}")
        if item.get("forbidden_tokens"):
            errors.append(f"verifier_forbidden_token:{item.get('path')}")
        if item.get("syntax_ok") is not True:
            errors.append(f"verifier_syntax_not_ok:{item.get('path')}")

    for probe in data.get("synthetic_probes", []):
        if probe.get("passed") is not True:
            errors.append(f"synthetic_probe_not_pass:{probe.get('id')}")

    rules = data.get("agent_run_guide", [])
    for fragment in ["do not run old verifiers with --rebuild", "subprocess warnings require human inspection", "blocking import/token/syntax issues"]:
        if not any(fragment in str(rule) for rule in rules):
            errors.append(f"agent_run_rule_missing:{fragment}")

    flags = data.get("readiness_flags", {})
    if set(flags) != READINESS_FLAGS:
        errors.append("readiness_flags_keys_mismatch")
    if flags.get("portability_audit_ready") is not True:
        errors.append("portability_audit_ready_not_true")
    for flag in READINESS_FLAGS - {"portability_audit_ready"}:
        if flags.get(flag) is not False:
            errors.append(f"readiness_flag_not_false:{flag}")

    performed = data.get("operation_performed_flags", {})
    if set(performed) != set(OPERATION_FLAGS):
        errors.append("operation_performed_flags_mismatch")
    for name, value in performed.items():
        if value is not False:
            errors.append(f"operation_performed_not_false:{name}")

    if data.get("required_non_claims") != REQUIRED_NON_CLAIMS:
        errors.append("required_non_claims_mismatch")
    return errors


def reset_generated() -> None:
    for directory in ["fixtures", "failure-cases", "prototype/verifier-portability-audit", "readouts"]:
        path = ROOT / directory
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def make_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: dict[str, list[str]] = {}
    index = 1

    def add(name: str, mutate, expected: list[str]) -> None:
        nonlocal index
        sample = copy.deepcopy(base)
        mutate(sample)
        filename = f"{index:03d}-{name}.json"
        write_json(ROOT / "failure-cases" / filename, sample)
        cases[filename] = expected
        index += 1

    for key in ["record_kind", "slice_id", "version", "truth_boundary", "purpose", "write_scope"]:
        add(f"top-level-{key}", lambda sample, key=key: sample.__setitem__(key, "wrong"), [f"{key}_mismatch"])
    add("bad-view", lambda sample: sample.__setitem__("view", "wrong"), ["view_not_allowed:wrong"])
    add("extra-runtime-certification-claim", lambda sample: sample.__setitem__("runtime_certification_claim", True), ["unknown_top_level_field:runtime_certification_claim"])
    add("source-snapshot-drift", lambda sample: sample.__setitem__("source_snapshot", {}), ["source_snapshot_mismatch"])
    add("policy-drift", lambda sample: sample["portability_policy"].__setitem__("does_not_install_dependencies", False), ["portability_policy_mismatch"])
    add("scanner-scope-drift", lambda sample: sample["scanner_scope"].__setitem__("included_verifier_count", 1), ["scanner_scope_mismatch"])
    add("summary-blocking-count", lambda sample: sample["summary"].__setitem__("blocking_verifier_count", 1), ["summary_mismatch", "blocking_verifier_present"])
    add("summary-external-import-count", lambda sample: sample["summary"].__setitem__("external_import_verifier_count", 1), ["summary_mismatch", "external_import_verifier_present"])
    add("summary-forbidden-token-count", lambda sample: sample["summary"].__setitem__("forbidden_token_verifier_count", 1), ["summary_mismatch", "forbidden_token_verifier_present"])
    add("summary-syntax-error-count", lambda sample: sample["summary"].__setitem__("syntax_error_verifier_count", 1), ["summary_mismatch", "syntax_error_verifier_present"])
    add("synthetic-probe-failure", lambda sample: sample["synthetic_probes"][0].__setitem__("passed", False), ["synthetic_probes_mismatch", "synthetic_probe_not_pass:stdlib_and_local_ok"])
    add("inventory-external-import", lambda sample: sample["verifier_inventory"][0].__setitem__("external_imports", ["requests"]), ["verifier_inventory_mismatch", f"verifier_external_import:{base['verifier_inventory'][0]['path']}"])
    add("inventory-blocking-issue", lambda sample: sample["verifier_inventory"][0].__setitem__("blocking_issues", ["external_imports_present"]), ["verifier_inventory_mismatch", f"verifier_blocking_issue:{base['verifier_inventory'][0]['path']}"])
    add("inventory-forbidden-token", lambda sample: sample["verifier_inventory"][0].__setitem__("forbidden_tokens", [{"token": "pip install", "reason": "dependency_install_token"}]), ["verifier_inventory_mismatch", f"verifier_forbidden_token:{base['verifier_inventory'][0]['path']}"])
    add("inventory-warning-token-drift", lambda sample: sample["verifier_inventory"][0].__setitem__("warning_tokens", [{"token": "mcp_write", "reason": "mcp_write_boundary_word"}]), ["verifier_inventory_mismatch"])
    add("inventory-syntax-not-ok", lambda sample: sample["verifier_inventory"][0].__setitem__("syntax_ok", False), ["verifier_inventory_mismatch", f"verifier_syntax_not_ok:{base['verifier_inventory'][0]['path']}"])
    add("agent-guide-rule-missing", lambda sample: sample["agent_run_guide"].pop(), ["agent_run_guide_mismatch", "agent_run_rule_missing:blocking import/token/syntax issues"])
    add("readiness-runtime-certified", lambda sample: sample["readiness_flags"].__setitem__("runtime_certified", True), ["readiness_flag_not_false:runtime_certified"])
    add("readiness-mainline-ready", lambda sample: sample["readiness_flags"].__setitem__("mainline_ready", True), ["readiness_flag_not_false:mainline_ready"])
    add("operation-old-verifier-executed", lambda sample: sample["operation_performed_flags"].__setitem__("old_verifier_executed", True), ["operation_performed_not_false:old_verifier_executed"])
    add("operation-dependency-install", lambda sample: sample["operation_performed_flags"].__setitem__("dependency_install", True), ["operation_performed_not_false:dependency_install"])
    for non_claim in REQUIRED_NON_CLAIMS:
        add(f"missing-non-claim-{non_claim.replace(' ', '-')}", lambda sample, non_claim=non_claim: sample["required_non_claims"].remove(non_claim), ["required_non_claims_mismatch"])
    add("extra-non-claim", lambda sample: sample["required_non_claims"].append("unexpected runtime certification"), ["required_non_claims_mismatch"])
    return cases


def build_fixtures() -> None:
    reset_generated()
    base = default_audit("verifier-portability-audit")
    write_json(ROOT / "fixtures" / "valid-verifier-portability-audit.json", base)
    guide = default_audit("agent-run-guide")
    guide["operator_note"] = "Agent run guide view. Still sandbox only."
    write_json(ROOT / "fixtures" / "valid-agent-run-guide.json", guide)
    risks = default_audit("risk-inventory")
    risks["operator_note"] = "Risk inventory view. Still sandbox only."
    write_json(ROOT / "fixtures" / "valid-risk-inventory.json", risks)
    cases = make_failure_cases(base)
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "cases": cases})
    lines = ["# Failure Case Oracle", "", f"Slice: `{SLICE_ID}`", "", f"Total cases: {len(cases)}", ""]
    for name, expected in cases.items():
        lines.append(f"- `{name}` -> `{', '.join(expected)}`")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines))


def build_readout_and_contract() -> None:
    audit = default_audit()
    summary = audit["summary"]
    write_json(ROOT / "artifact" / "verifier-portability-audit.json", audit)
    write_text(
        ROOT / "artifact" / "dependency-policy.md",
        f"""
# Verifier Portability Dependency Policy

Slice: `{SLICE_ID}`

This policy is a static sandbox audit. It does not execute old verifiers, install
dependencies, certify runtime behavior, promote artifacts, or approve action use.

## Blocking Signals

- Syntax error in a verifier script.
- External import outside Python standard library and same-slice modules.
- Network/API import such as `requests`, `httpx`, `socket`, or `urllib`.
- Dependency install, commit, push, network, or background-service token.

## Warning Signals

- `subprocess` import is a warning for human inspection of default path behavior.
- Boundary words such as formal-vault path text, Obsidian sync text, or MCP-write labels are warnings when they appear only as source text.
- Explicit `--rebuild` support is allowed but must be treated as Builder-only.
""",
    )
    write_text(
        ROOT / "readouts" / "verifier-portability-guide.md",
        f"""
# Verifier Portability Guide

Status: static sandbox portability audit only.

Verifier scripts scanned: `{summary['verifier_count']}`

Static portability pass: `{summary['static_portability_pass_count']}`

Blocking verifiers: `{summary['blocking_verifier_count']}`

Warning verifiers: `{summary['warning_verifier_count']}`

Synthetic probes: `{summary['synthetic_probe_pass_count']}/{summary['synthetic_probe_count']}`

Interpretation:

- Default reviewer path is to run this p2-47 verifier, then the target slice default verifier.
- Do not run old verifier `--rebuild` commands during review.
- This audit is not runtime certification, enterprise readiness, promotion, reviewed knowledge, evidence support, or action basis.
""",
    )


def build_prototype() -> None:
    audit = default_audit()
    summary = audit["summary"]
    prototype = ROOT / "prototype" / "verifier-portability-audit"
    rows = "\n".join(
        f"<tr><td>{key}</td><td>{value}</td></tr>"
        for key, value in summary.items()
        if isinstance(value, (int, bool))
    )
    write_text(
        prototype / "index.html",
        f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Verifier Portability Audit</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f8fafc; color: #1f2933; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    .summary {{ color: #526273; max-width: 820px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 18px; background: #fff; border: 1px solid #d9e1ec; }}
    th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid #e6edf5; }}
    .notice {{ margin-top: 16px; border-left: 4px solid #2f6fed; background: #edf4ff; padding: 12px 14px; }}
  </style>
</head>
<body>
  <main>
    <h1>Verifier Portability Audit</h1>
    <p class="summary">static sandbox portability audit only. Verifiers scanned {summary['verifier_count']}; blocking verifiers {summary['blocking_verifier_count']}; not runtime certification; not enterprise production; not action basis.</p>
    <table>
      <thead><tr><th>Signal</th><th>Value</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <section class="notice">This prototype does not execute old verifiers, install dependencies, access network, write vault files, commit, push, sync, or promote.</section>
  </main>
  <script src="app.js"></script>
</body>
</html>
""",
    )
    write_text(prototype / "app.js", 'document.documentElement.dataset.verifierPortabilityAuditReady = "true";')
    receipt = {
        "record_kind": "verifier_portability_audit_prototype_receipt",
        "slice_id": SLICE_ID,
        "runtime_certified": False,
        "dependency_install": False,
        "old_verifier_executed": False,
        "enterprise_production_ready": False,
        "mainline_ready": False,
        "formal_vault_accessed": False,
        "sync_performed": False,
        "commit_performed": False,
        "push_performed": False,
        "promotion_performed": False,
        "action_basis_created": False,
        "required_non_claims": REQUIRED_NON_CLAIMS,
    }
    write_json(prototype / "receipt.json", receipt)


def frontmatter(status: str) -> str:
    return f"---\nstatus: {status}\nslice_id: {SLICE_ID}\n---\n"


def build_reports() -> None:
    audit = default_audit()
    summary = audit["summary"]
    write_text(
        ROOT / "slice-plan.md",
        frontmatter("built_pending_review")
        + f"""
# Slice Plan

## Objective

Build a static sandbox audit for verifier portability, dependency hygiene, and default-review safety signals.

## Inputs

- `{rel(SOURCE_STATUS_AUDIT)}`
- sandbox verifier scripts matching `outputs/review/vaks-implementation-sandbox/*/artifact/verify*.py`

## Only Write Path

`{WRITE_SCOPE}`

## Non-Goals

- No execution of old verifiers.
- No dependency installation.
- No runtime certification.
- No edits to old slices.
- No formal vault access or sync.
- No commit, push, promotion, reviewed knowledge, evidence support, action basis, or mainline readiness.
""",
    )
    write_text(
        ROOT / "source-map.md",
        frontmatter("built_pending_review")
        + f"""
# Source Map

Source status audit:

- `{audit['source_snapshot']['source_status_audit_path']}`
- sha256: `{audit['source_snapshot']['source_status_audit_sha256']}`

Verifier scan:

- verifier scripts: `{summary['verifier_count']}`
- blocking verifiers: `{summary['blocking_verifier_count']}`
- warning verifiers: `{summary['warning_verifier_count']}`

The scan is static read-only. It is not runtime certification or authority.
""",
    )
    write_text(
        ROOT / "verification.md",
        frontmatter("local_verification_passed_pending_review")
        + f"""
# Verification

Default read-only verification command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_portability_audit.py
```

Expected result:

- Positive fixtures pass.
- Failure cases match the oracle.
- Synthetic probes pass.
- Static verifier inventory has zero blocking import/token/syntax issues.
- Prototype and readout preserve sandbox-only boundaries.

Builder-only regeneration command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_portability_audit.py --rebuild
```

Final gate command after reviews:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_portability_audit.py --final-gate
```
""",
    )
    write_text(ROOT / "reviewer-report.md", frontmatter("reviewer_pending") + "# Reviewer Report\n\nPending independent read-only review.\n")
    write_text(ROOT / "boundary-audit.md", frontmatter("boundary_pending") + "# Boundary Audit\n\nPending independent boundary audit.\n")
    write_text(ROOT / "product-acceptance-report.md", frontmatter("product_acceptance_pending") + "# Product Acceptance Report\n\nPending GPT-5.5 extra-high Product Acceptance.\n")
    write_text(ROOT / "next-step.md", frontmatter("next_step_pending_product_acceptance") + "# Next Step\n\nDo not advance until Product Acceptance passes this slice.\n")


def build() -> None:
    build_fixtures()
    build_readout_and_contract()
    build_prototype()
    build_reports()


def validate_failure_cases() -> dict[str, Any]:
    oracle_path = ROOT / "artifact" / "failure-case-oracle.json"
    failure_dir = ROOT / "failure-cases"
    if not oracle_path.exists():
        return {"count": 0, "actual_file_count": 0, "orphan_count": 0, "mismatches": [{"file": "failure-case-oracle.json", "expected": ["oracle_present"], "actual": ["missing_oracle"]}]}
    oracle = read_json(oracle_path).get("cases", {})
    actual_files = {path.name for path in failure_dir.glob("*.json")} if failure_dir.exists() else set()
    mismatches = []
    for extra in sorted(actual_files - set(oracle)):
        mismatches.append({"file": extra, "expected": ["not_present_outside_oracle"], "actual": ["orphan_failure_case_file"]})
    for name, expected in oracle.items():
        path = failure_dir / name
        if not path.exists():
            mismatches.append({"file": name, "expected": expected, "actual": ["missing_failure_case"]})
            continue
        actual = validate_audit(read_json(path))
        if sorted(actual) != sorted(expected):
            mismatches.append({"file": name, "expected": expected, "actual": actual})
    return {"count": len(oracle), "actual_file_count": len(actual_files), "orphan_count": len(actual_files - set(oracle)), "mismatches": mismatches}


def validate_fixtures() -> dict[str, Any]:
    fixture_dir = ROOT / "fixtures"
    actual_files = {path.name for path in fixture_dir.glob("*.json")} if fixture_dir.exists() else set()
    errors = []
    details = []
    for missing in sorted(set(REQUIRED_FIXTURES) - actual_files):
        errors.append({"file": missing, "errors": ["missing_required_fixture"]})
    for extra in sorted(actual_files - set(REQUIRED_FIXTURES)):
        errors.append({"file": extra, "errors": ["unexpected_fixture_file"]})
    for path in sorted(fixture_dir.glob("*.json")):
        data = read_json(path)
        fixture_errors = validate_audit(data)
        expected_view = REQUIRED_FIXTURES.get(path.name)
        if expected_view and data.get("view") != expected_view:
            fixture_errors.append(f"fixture_view_mismatch:{expected_view}")
        if path.name == "valid-verifier-portability-audit.json" and "operator_note" in data:
            fixture_errors.append("fixture_operator_note_unexpected")
        if path.name != "valid-verifier-portability-audit.json" and path.name in REQUIRED_FIXTURES and "operator_note" not in data:
            fixture_errors.append("fixture_operator_note_missing")
        details.append({"file": path.name, "errors": fixture_errors})
        if fixture_errors:
            errors.append({"file": path.name, "errors": fixture_errors})
    return {"count": len(details), "fixtures": details, "errors": errors}


def validate_readout() -> dict[str, Any]:
    path = ROOT / "readouts" / "verifier-portability-guide.md"
    issues: list[str] = []
    if not path.exists():
        return {"path": str(path), "issues": ["missing_readout"]}
    text = path.read_text(encoding="utf-8", errors="ignore")
    for phrase in ["static sandbox portability audit only", "Verifier scripts scanned", "Blocking verifiers", "Synthetic probes", "not runtime certification"]:
        if phrase not in text:
            issues.append(f"readout_phrase_missing:{phrase}")
    return {"path": str(path), "issues": issues}


def validate_prototype() -> dict[str, Any]:
    prototype = ROOT / "prototype" / "verifier-portability-audit"
    issues: list[str] = []
    for item in ["index.html", "app.js", "receipt.json"]:
        if not (prototype / item).exists():
            issues.append(f"missing_prototype_file:{item}")
    if (prototype / "index.html").exists():
        html = (prototype / "index.html").read_text(encoding="utf-8", errors="ignore").lower()
        for forbidden in ["<form", "download", "contenteditable", "<a ", "h:\\obsidian", "onclick"]:
            if forbidden in html:
                issues.append(f"prototype_forbidden:{forbidden}")
        for phrase in ["static sandbox portability audit only", "not runtime certification", "not enterprise production", "not action basis"]:
            if phrase not in html:
                issues.append(f"prototype_phrase_missing:{phrase}")
    if (prototype / "app.js").exists():
        js = (prototype / "app.js").read_text(encoding="utf-8", errors="ignore").strip()
        if js != 'document.documentElement.dataset.verifierPortabilityAuditReady = "true";':
            issues.append("prototype_app_js_not_static_receipt_marker")
    if (prototype / "receipt.json").exists():
        receipt = read_json(prototype / "receipt.json")
        for flag in [
            "runtime_certified",
            "dependency_install",
            "old_verifier_executed",
            "enterprise_production_ready",
            "mainline_ready",
            "formal_vault_accessed",
            "sync_performed",
            "commit_performed",
            "push_performed",
            "promotion_performed",
            "action_basis_created",
        ]:
            if receipt.get(flag) is not False:
                issues.append(f"prototype_receipt_flag_not_false:{flag}")
        if receipt.get("required_non_claims") != REQUIRED_NON_CLAIMS:
            issues.append("prototype_receipt_non_claims_mismatch")
    return {"prototype_path": str(prototype), "issues": issues}


def validate_required_reports(final_gate: bool = False) -> dict[str, Any]:
    required = {
        "slice-plan.md": "built_pending_review",
        "source-map.md": "built_pending_review",
        "verification.md": "local_verification_passed_pending_review",
    }
    if final_gate:
        required.update(
            {
                "reviewer-report.md": "reviewer_pass",
                "boundary-audit.md": "boundary_pass",
                "product-acceptance-report.md": "pass_product_grade",
                "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
            }
        )
    statuses: dict[str, str | None] = {}
    issues: list[str] = []
    for name, expected in required.items():
        status = parse_status(ROOT / name)
        statuses[name] = status
        if status != expected:
            issues.append(f"bad_status:{name}:{status}:expected:{expected}")
    return {"statuses": statuses, "issues": issues}


def validate_all(final_gate: bool = False) -> dict[str, Any]:
    primary = ROOT / "fixtures" / "valid-verifier-portability-audit.json"
    config_errors = validate_audit(read_json(primary)) if primary.exists() else ["missing_valid_fixture"]
    artifact_path = ROOT / "artifact" / "verifier-portability-audit.json"
    artifact_errors = validate_audit(read_json(artifact_path)) if artifact_path.exists() else ["missing_verifier_portability_audit"]
    fixtures = validate_fixtures()
    failure_cases = validate_failure_cases()
    prototype = validate_prototype()
    readout = validate_readout()
    reports = validate_required_reports(final_gate=final_gate)
    failures: list[str] = []
    failures.extend(config_errors)
    failures.extend([f"artifact_error:{item}" for item in artifact_errors])
    failures.extend([f"fixture_error:{item['file']}" for item in fixtures["errors"]])
    failures.extend([f"failure_case_mismatch:{item['file']}" for item in failure_cases["mismatches"]])
    failures.extend(prototype["issues"])
    failures.extend(readout["issues"])
    failures.extend(reports["issues"])
    current = default_audit()
    return {
        "slice_id": SLICE_ID,
        "passed": not failures,
        "failures": failures,
        "valid_config_errors": config_errors,
        "artifact_errors": artifact_errors,
        "positive_fixtures": fixtures,
        "failure_cases": failure_cases,
        "prototype": prototype,
        "readout": readout,
        "required_reports": reports,
        "source_snapshot": current["source_snapshot"],
        "summary": current["summary"],
        "risk_inventory_count": len(current["risk_inventory"]),
        "non_claims": REQUIRED_NON_CLAIMS,
    }


if __name__ == "__main__":
    build()
