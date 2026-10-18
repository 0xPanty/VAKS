from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from copy import deepcopy
from datetime import date
from pathlib import Path


SLICE_ID = "2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox"
VERSION = "0.1.0"

SOURCE_SLICES = [
    {
        "slice_id": "2026-06-15-p2-44-sandbox-evidence-ledger-sandbox",
        "role": "evidence ledger and improvement inventory",
        "verifier": "artifact/verify_evidence_ledger.py",
        "primary_artifact": "artifact/evidence-ledger.json",
        "readout": "ledger-packets/plain-answer.md",
    },
    {
        "slice_id": "2026-06-15-p2-45-sandbox-release-candidate-handoff-sandbox",
        "role": "release-candidate handoff packet without release authority",
        "verifier": "artifact/verify_release_candidate_handoff.py",
        "primary_artifact": "artifact/release-candidate-handoff.json",
        "readout": "handoff-packets/release-candidate-handoff.md",
    },
    {
        "slice_id": "2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox",
        "role": "legacy status normalization guide",
        "verifier": "artifact/verify_status_normalization_audit.py",
        "primary_artifact": "artifact/status-normalization-audit.json",
        "readout": "readouts/status-normalization-guide.md",
    },
    {
        "slice_id": "2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox",
        "role": "static verifier portability and dependency audit",
        "verifier": "artifact/verify_portability_audit.py",
        "primary_artifact": "artifact/verifier-portability-audit.json",
        "readout": "readouts/verifier-portability-guide.md",
        "launch_gate_role": "diagnostic_drift_sensitive_not_launch_gate",
        "known_current_note": "Product report is PASS, but the dynamic verifier can fail after later slices add new verifier files; treat that as drift-sensitive diagnostic context, not a launch green gate.",
    },
    {
        "slice_id": "2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox",
        "role": "checksum freeze and drift detector for p2-44 through p2-47",
        "verifier": "artifact/verify_freeze_bundle.py",
        "primary_artifact": "artifact/evidence-chain-freeze-manifest.json",
        "readout": "readouts/evidence-chain-freeze-guide.md",
        "launch_gate_role": "required_freeze_final_gate",
    },
]

REQUIRED_NON_CLAIMS = [
    "not re-acceptance",
    "not runtime certification",
    "not old verifier execution",
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
    "not user approval",
]

FORBIDDEN_READINESS_TRUE = [
    "re_acceptance_performed",
    "runtime_certified",
    "release_approved",
    "promotion_approved",
    "mainline_ready",
    "enterprise_production_ready",
    "formal_vault_ready",
    "reviewed_knowledge_ready",
    "evidence_support_ready",
    "action_basis_ready",
    "user_approval_collected",
]

FORBIDDEN_OPERATION_TRUE = [
    "old_slice_modified",
    "old_verifier_executed",
    "automated_old_verifier_batch",
    "commit",
    "push",
    "obsidian_sync",
    "formal_vault_write",
    "mainline_merge",
    "promotion",
    "dependency_install",
    "background_service",
    "hooks",
    "mcp_write_tool",
    "network_access",
    "auto_advance",
]

REQUIRED_STOP_CONDITIONS = [
    "freeze_verifier_failed",
    "checksum_or_status_drift_detected",
    "source_product_status_not_pass_product_grade",
    "protected_path_touched_by_current_slice",
    "operator_scope_would_write_outside_current_sandbox",
    "authority_confusion_detected",
    "portability_verifier_claimed_green_despite_known_scope_drift",
    "user_approval_required_for_mainline_or_formal_vault",
]

REQUIRED_SEQUENCE = [
    "01-scope-card",
    "02-freeze-final-gate",
    "03-evidence-ledger-read",
    "04-release-handoff-read",
    "05-status-normalization-read",
    "06-portability-read",
    "07-plain-answer-compose",
    "08-stop-or-escalate",
]

REQUIRED_STEP_RULES = {
    "01-scope-card": {
        "stop_if": ["protected_path_touched_by_current_slice", "operator_scope_would_write_outside_current_sandbox"],
        "operator_action_contains": ["current work writes only inside this p2-49 sandbox path"],
    },
    "02-freeze-final-gate": {
        "stop_if": ["freeze_verifier_failed", "checksum_or_status_drift_detected"],
        "operator_action_contains": ["checksum freeze final gate"],
        "command_contains": ["verify_freeze_bundle.py", "--final-gate"],
    },
    "06-portability-read": {
        "stop_if": ["authority_confusion_detected", "portability_verifier_claimed_green_despite_known_scope_drift"],
        "operator_action_contains": ["Do not treat p2-47 as a current launch green gate", "dynamic scope scan drift"],
        "known_current_note_contains": ["dynamic verifier can fail", "drift-sensitive diagnostic context", "not a launch green gate"],
    },
    "08-stop-or-escalate": {
        "stop_if": REQUIRED_STOP_CONDITIONS,
        "operator_action_contains": ["do not continue to the next slice"],
    },
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def slice_root() -> Path:
    return Path(__file__).resolve().parents[1]


def rel(path: Path) -> str:
    return path.resolve().relative_to(repo_root()).as_posix()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def frontmatter_status(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    match = re.match(r"---\r?\n(?P<body>.*?)\r?\n---", text, re.S)
    if not match:
        return None
    for line in match.group("body").splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def file_entry(path: Path) -> dict:
    return {
        "path": rel(path),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else None,
        "sha256": sha256(path) if path.exists() else None,
        "frontmatter_status": frontmatter_status(path) if path.suffix.lower() == ".md" else None,
    }


def build_source_chain() -> list[dict]:
    root = repo_root()
    chain = []
    for item in SOURCE_SLICES:
        base = root / "outputs" / "review" / "vaks-implementation-sandbox" / item["slice_id"]
        verifier = base / item["verifier"]
        verifier_command_path = item["verifier"].replace("/", "\\")
        product_report = base / "product-acceptance-report.md"
        verification = base / "verification.md"
        chain.append(
            {
                "slice_id": item["slice_id"],
                "role": item["role"],
                "source_root": rel(base),
                "required_status": "pass_product_grade",
                "product_acceptance_report": file_entry(product_report),
                "verification_report": file_entry(verification),
                "primary_artifact": file_entry(base / item["primary_artifact"]),
                "readout": file_entry(base / item["readout"]),
                "verifier": file_entry(verifier),
                "manual_read_only_verifier_command": f"python -B .\\outputs\\review\\vaks-implementation-sandbox\\{item['slice_id']}\\{verifier_command_path}",
                "manual_run_policy": "read_only_on_demand_after_freeze_passes",
                "launch_gate_role": item.get("launch_gate_role", "supporting_reference_not_launch_gate"),
                "known_current_note": item.get("known_current_note", ""),
            }
        )
    return chain


def build_checklist() -> dict:
    source_chain = build_source_chain()
    freeze_slice = SOURCE_SLICES[-1]["slice_id"]
    today = date.today().isoformat()
    return {
        "record_kind": "sandbox_operator_launch_checklist",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "generated_at": today,
        "purpose": "turn p2-44 through p2-48 into a manual read-only operator launch checklist",
        "truth_boundary": "operator_checklist_for_sandbox_handoff_not_authority",
        "write_scope": f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/",
        "source_chain": source_chain,
        "launch_sequence": [
            {
                "step_id": "01-scope-card",
                "title": "Confirm current slice scope",
                "operator_action": "Confirm the current work writes only inside this p2-49 sandbox path and treats unrelated dirty tree entries as pre-existing baseline.",
                "command_hint": f"git status --short -- .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}",
                "writes_allowed": False,
                "stop_if": ["protected_path_touched_by_current_slice", "operator_scope_would_write_outside_current_sandbox"],
            },
            {
                "step_id": "02-freeze-final-gate",
                "title": "Run the p2-48 freeze verifier first",
                "operator_action": "Run the checksum freeze final gate before trusting the handoff chain.",
                "command_hint": f"python -B .\\outputs\\review\\vaks-implementation-sandbox\\{freeze_slice}\\artifact\\verify_freeze_bundle.py --final-gate",
                "expected": {"passed": True, "missing_file_count": 0, "report_status_mismatch_count": 0},
                "writes_allowed": False,
                "stop_if": ["freeze_verifier_failed", "checksum_or_status_drift_detected"],
            },
            {
                "step_id": "03-evidence-ledger-read",
                "title": "Read p2-44 for what improved",
                "operator_action": "Use the evidence ledger as a status and improvement inventory only.",
                "source_slice": SOURCE_SLICES[0]["slice_id"],
                "writes_allowed": False,
                "stop_if": ["source_product_status_not_pass_product_grade", "authority_confusion_detected"],
            },
            {
                "step_id": "04-release-handoff-read",
                "title": "Read p2-45 for user-facing handoff wording",
                "operator_action": "Use the handoff packet to explain sandbox readiness without claiming release approval.",
                "source_slice": SOURCE_SLICES[1]["slice_id"],
                "writes_allowed": False,
                "stop_if": ["authority_confusion_detected"],
            },
            {
                "step_id": "05-status-normalization-read",
                "title": "Use p2-46 to interpret legacy statuses",
                "operator_action": "Resolve old report wording through the status normalization guide before drawing a pass/fail conclusion.",
                "source_slice": SOURCE_SLICES[2]["slice_id"],
                "writes_allowed": False,
                "stop_if": ["source_product_status_not_pass_product_grade"],
            },
            {
                "step_id": "06-portability-read",
                "title": "Use p2-47 before running verifiers on another machine",
                "operator_action": "Check portability warnings and dependency assumptions before manual verifier execution. Do not treat p2-47 as a current launch green gate; later slices can make its dynamic scope scan drift.",
                "source_slice": SOURCE_SLICES[3]["slice_id"],
                "writes_allowed": False,
                "known_current_note": SOURCE_SLICES[3]["known_current_note"],
                "stop_if": ["authority_confusion_detected", "portability_verifier_claimed_green_despite_known_scope_drift"],
            },
            {
                "step_id": "07-plain-answer-compose",
                "title": "Compose plain-language status",
                "operator_action": "Answer what is done, what improved, what passed, and what remains sandbox-only.",
                "writes_allowed": False,
                "required_answer_parts": [
                    "completed_slice_chain",
                    "verification_counts",
                    "reviewer_boundary_product_verdicts",
                    "sandbox_not_mainline",
                    "user_approval_needed_for_any_promotion",
                ],
                "stop_if": ["authority_confusion_detected"],
            },
            {
                "step_id": "08-stop-or-escalate",
                "title": "Stop on drift or authority crossing",
                "operator_action": "If any stop condition fires, do not continue to the next slice and ask the user or repair the current slice.",
                "writes_allowed": False,
                "stop_if": REQUIRED_STOP_CONDITIONS,
            },
        ],
        "stop_conditions": REQUIRED_STOP_CONDITIONS,
        "readiness_flags": {
            "operator_launch_checklist_ready": True,
            **{key: False for key in FORBIDDEN_READINESS_TRUE},
        },
        "operation_flags": {key: False for key in FORBIDDEN_OPERATION_TRUE},
        "required_non_claims": REQUIRED_NON_CLAIMS,
        "manual_command_policy": {
            "default_command_is_this_slice_verifier": True,
            "old_verifier_commands_are_documented_not_auto_executed": True,
            "old_verifier_batch_execution_forbidden": True,
            "rebuild_flags_are_builder_only": True,
            "no_dependency_installation": True,
        },
        "acceptance_contract": {
            "positive_fixture_count": 3,
            "requires_failure_case_oracle": True,
            "requires_reviewer": True,
            "requires_boundary_auditor": True,
            "requires_gpt_5_5_extra_high_product_acceptance": True,
            "product_acceptance_is_only_pass_authority_for_next_slice": True,
        },
    }


def validate_config(data: dict) -> list[str]:
    errors: list[str] = []
    expected_top = {
        "record_kind": "sandbox_operator_launch_checklist",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": "operator_checklist_for_sandbox_handoff_not_authority",
        "write_scope": f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/",
    }
    for key, expected in expected_top.items():
        if data.get(key) != expected:
            errors.append(f"top_level_{key}")

    source_chain = data.get("source_chain")
    if not isinstance(source_chain, list) or len(source_chain) != len(SOURCE_SLICES):
        errors.append("source_chain_count")
        source_chain = []
    else:
        expected_ids = [item["slice_id"] for item in SOURCE_SLICES]
        actual_ids = [item.get("slice_id") for item in source_chain]
        if actual_ids != expected_ids:
            errors.append("source_chain_order")
        for item in source_chain:
            if item.get("required_status") != "pass_product_grade":
                errors.append(f"source_required_status_{item.get('slice_id', 'unknown')}")
            report = item.get("product_acceptance_report", {})
            if report.get("frontmatter_status") != "pass_product_grade":
                errors.append(f"source_product_status_{item.get('slice_id', 'unknown')}")
            for key in ["product_acceptance_report", "verification_report", "primary_artifact", "readout", "verifier"]:
                entry = item.get(key, {})
                if entry.get("exists") is not True:
                    errors.append(f"source_missing_{item.get('slice_id', 'unknown')}_{key}")
            command = item.get("manual_read_only_verifier_command", "")
            if "python -B" not in command or "verify_" not in command:
                errors.append(f"source_bad_verifier_command_{item.get('slice_id', 'unknown')}")
            if item.get("manual_run_policy") != "read_only_on_demand_after_freeze_passes":
                errors.append(f"source_bad_manual_run_policy_{item.get('slice_id', 'unknown')}")
            if item.get("slice_id") == "2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox":
                if item.get("launch_gate_role") != "diagnostic_drift_sensitive_not_launch_gate":
                    errors.append("p2_47_gate_role_not_drift_sensitive")
                if "dynamic verifier can fail" not in item.get("known_current_note", ""):
                    errors.append("p2_47_known_current_note_missing")
            if item.get("slice_id") == "2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox":
                if item.get("launch_gate_role") != "required_freeze_final_gate":
                    errors.append("p2_48_gate_role_not_required_freeze")

    sequence = data.get("launch_sequence")
    if not isinstance(sequence, list):
        errors.append("launch_sequence_missing")
        sequence = []
    actual_steps = [step.get("step_id") for step in sequence if isinstance(step, dict)]
    if actual_steps != REQUIRED_SEQUENCE:
        errors.append("launch_sequence_order")
    for step in sequence:
        if not isinstance(step, dict):
            errors.append("launch_sequence_step_not_object")
            continue
        if step.get("writes_allowed") is not False:
            errors.append(f"step_writes_allowed_{step.get('step_id', 'unknown')}")
        step_id = step.get("step_id", "unknown")
        rules = REQUIRED_STEP_RULES.get(step_id, {})
        stop_if = step.get("stop_if", [])
        for condition in rules.get("stop_if", []):
            if condition not in stop_if:
                errors.append(f"step_missing_stop_if_{step_id}_{condition}")
        action = step.get("operator_action", "")
        for token in rules.get("operator_action_contains", []):
            if token not in action:
                errors.append(f"step_action_missing_{step_id}_{token.replace(' ', '_')}")
        command = step.get("command_hint", "")
        for token in rules.get("command_contains", []):
            if token not in command:
                errors.append(f"step_command_missing_{step_id}_{token.replace(' ', '_')}")
        note = step.get("known_current_note", "")
        for token in rules.get("known_current_note_contains", []):
            if token not in note:
                errors.append(f"step_note_missing_{step_id}_{token.replace(' ', '_')}")
    freeze_step = next((step for step in sequence if isinstance(step, dict) and step.get("step_id") == "02-freeze-final-gate"), {})
    freeze_command = freeze_step.get("command_hint", "")
    if "verify_freeze_bundle.py" not in freeze_command or "--final-gate" not in freeze_command:
        errors.append("freeze_final_gate_command")

    stop_conditions = data.get("stop_conditions")
    if not isinstance(stop_conditions, list):
        errors.append("stop_conditions_missing")
        stop_conditions = []
    for condition in REQUIRED_STOP_CONDITIONS:
        if condition not in stop_conditions:
            errors.append(f"missing_stop_condition_{condition}")

    readiness = data.get("readiness_flags", {})
    if readiness.get("operator_launch_checklist_ready") is not True:
        errors.append("operator_launch_checklist_not_ready")
    for key in FORBIDDEN_READINESS_TRUE:
        if readiness.get(key) is not False:
            errors.append(f"readiness_{key}_not_false")

    operations = data.get("operation_flags", {})
    for key in FORBIDDEN_OPERATION_TRUE:
        if operations.get(key) is not False:
            errors.append(f"operation_{key}_not_false")

    non_claims = data.get("required_non_claims")
    if not isinstance(non_claims, list):
        errors.append("required_non_claims_missing")
        non_claims = []
    for claim in REQUIRED_NON_CLAIMS:
        if claim not in non_claims:
            errors.append(f"missing_non_claim_{claim.replace(' ', '_')}")
    extras = [claim for claim in non_claims if claim not in REQUIRED_NON_CLAIMS]
    if extras:
        errors.append("extra_non_claim")

    policy = data.get("manual_command_policy", {})
    required_policy = {
        "default_command_is_this_slice_verifier": True,
        "old_verifier_commands_are_documented_not_auto_executed": True,
        "old_verifier_batch_execution_forbidden": True,
        "rebuild_flags_are_builder_only": True,
        "no_dependency_installation": True,
    }
    for key, expected in required_policy.items():
        if policy.get(key) is not expected:
            errors.append(f"manual_command_policy_{key}")

    contract = data.get("acceptance_contract", {})
    if contract.get("requires_gpt_5_5_extra_high_product_acceptance") is not True:
        errors.append("acceptance_missing_gpt_5_5_extra_high")
    if contract.get("product_acceptance_is_only_pass_authority_for_next_slice") is not True:
        errors.append("acceptance_product_not_only_gate")

    return sorted(set(errors))


def mutate(base: dict, name: str) -> dict:
    data = deepcopy(base)
    if name == "top-level-record-kind":
        data["record_kind"] = "operator_launch_checklist"
    elif name == "top-level-slice-id":
        data["slice_id"] = "wrong-slice"
    elif name == "top-level-version":
        data["version"] = "0.0.0"
    elif name == "top-level-truth-boundary":
        data["truth_boundary"] = "operator_checklist_is_authority"
    elif name == "top-level-write-scope":
        data["write_scope"] = "outputs/review/"
    elif name == "source-chain-count":
        data["source_chain"] = data["source_chain"][:-1]
    elif name == "source-chain-order":
        data["source_chain"][0], data["source_chain"][1] = data["source_chain"][1], data["source_chain"][0]
    elif name == "source-product-status":
        data["source_chain"][0]["product_acceptance_report"]["frontmatter_status"] = "pending"
    elif name == "source-missing-verifier":
        data["source_chain"][0]["verifier"]["exists"] = False
    elif name == "source-bad-command":
        data["source_chain"][0]["manual_read_only_verifier_command"] = "python old.py"
    elif name == "source-bad-manual-run-policy":
        data["source_chain"][0]["manual_run_policy"] = "auto_execute"
    elif name == "p2-47-wrong-gate-role":
        data["source_chain"][3]["launch_gate_role"] = "required_green_gate"
    elif name == "p2-47-known-note-missing":
        data["source_chain"][3]["known_current_note"] = ""
    elif name == "p2-48-wrong-gate-role":
        data["source_chain"][4]["launch_gate_role"] = "supporting_reference_not_launch_gate"
    elif name == "launch-sequence-order":
        data["launch_sequence"][1], data["launch_sequence"][2] = data["launch_sequence"][2], data["launch_sequence"][1]
    elif name == "step-writes-allowed":
        data["launch_sequence"][0]["writes_allowed"] = True
    elif name == "freeze-final-gate-command":
        data["launch_sequence"][1]["command_hint"] = "python -B verifier.py"
    elif name == "freeze-step-stop-if-missing":
        data["launch_sequence"][1]["stop_if"] = []
    elif name == "p2-47-step-current-green-gate-text":
        data["launch_sequence"][5]["operator_action"] = "Treat p2-47 as a current launch green gate."
    elif name == "p2-47-step-note-missing":
        data["launch_sequence"][5]["known_current_note"] = ""
    elif name == "p2-47-step-stop-if-missing":
        data["launch_sequence"][5]["stop_if"] = ["authority_confusion_detected"]
    elif name == "stop-step-stop-if-missing":
        data["launch_sequence"][7]["stop_if"] = []
    elif name.startswith("missing-stop-"):
        condition = name.removeprefix("missing-stop-")
        data["stop_conditions"] = [c for c in data["stop_conditions"] if c != condition]
    elif name == "operator-checklist-not-ready":
        data["readiness_flags"]["operator_launch_checklist_ready"] = False
    elif name.startswith("readiness-"):
        key = name.removeprefix("readiness-")
        data["readiness_flags"][key] = True
    elif name.startswith("operation-"):
        key = name.removeprefix("operation-")
        data["operation_flags"][key] = True
    elif name.startswith("missing-non-claim-"):
        claim = name.removeprefix("missing-non-claim-").replace("_", " ")
        data["required_non_claims"] = [item for item in data["required_non_claims"] if item != claim]
    elif name == "extra-non-claim":
        data["required_non_claims"].append("production approved")
    elif name.startswith("manual-policy-"):
        key = name.removeprefix("manual-policy-")
        data["manual_command_policy"][key] = False
    elif name == "acceptance-missing-gpt55":
        data["acceptance_contract"]["requires_gpt_5_5_extra_high_product_acceptance"] = False
    elif name == "acceptance-product-not-only-gate":
        data["acceptance_contract"]["product_acceptance_is_only_pass_authority_for_next_slice"] = False
    else:
        raise ValueError(f"unknown mutation: {name}")
    return data


def failure_mutations() -> list[str]:
    names = [
        "top-level-record-kind",
        "top-level-slice-id",
        "top-level-version",
        "top-level-truth-boundary",
        "top-level-write-scope",
        "source-chain-count",
        "source-chain-order",
        "source-product-status",
        "source-missing-verifier",
        "source-bad-command",
        "source-bad-manual-run-policy",
        "p2-47-wrong-gate-role",
        "p2-47-known-note-missing",
        "p2-48-wrong-gate-role",
        "launch-sequence-order",
        "step-writes-allowed",
        "freeze-final-gate-command",
        "freeze-step-stop-if-missing",
        "p2-47-step-current-green-gate-text",
        "p2-47-step-note-missing",
        "p2-47-step-stop-if-missing",
        "stop-step-stop-if-missing",
        "operator-checklist-not-ready",
        "extra-non-claim",
        "acceptance-missing-gpt55",
        "acceptance-product-not-only-gate",
    ]
    names.extend(f"missing-stop-{condition}" for condition in REQUIRED_STOP_CONDITIONS)
    names.extend(f"readiness-{key}" for key in FORBIDDEN_READINESS_TRUE)
    names.extend(f"operation-{key}" for key in FORBIDDEN_OPERATION_TRUE)
    names.extend(f"missing-non-claim-{claim.replace(' ', '_')}" for claim in REQUIRED_NON_CLAIMS)
    names.extend(
        [
            "manual-policy-default_command_is_this_slice_verifier",
            "manual-policy-old_verifier_commands_are_documented_not_auto_executed",
            "manual-policy-old_verifier_batch_execution_forbidden",
            "manual-policy-rebuild_flags_are_builder_only",
            "manual-policy-no_dependency_installation",
        ]
    )
    return names


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def markdown_contract(checklist: dict) -> str:
    return f"""---
record_kind: sandbox_contract
slice_id: {SLICE_ID}
status: built_pending_review
---

# Operator Launch Checklist Contract

This contract turns p2-44 through p2-48 into a manual read-only operator launch sequence.

It is not re-acceptance, runtime certification, old verifier execution, release approval, promotion approval, mainline readiness, enterprise production readiness, formal vault approval, Obsidian sync, commit authorization, push authorization, reviewed knowledge, evidence support, action basis, auto advance, or user approval.

Required order:

1. Confirm p2-49 scope.
2. Run p2-48 `verify_freeze_bundle.py --final-gate`.
3. Read p2-44 evidence ledger for improvement inventory.
4. Read p2-45 handoff for user-facing wording.
5. Read p2-46 status normalization before interpreting legacy statuses.
6. Read p2-47 portability audit before manual old-verifier execution on another machine.
   Treat p2-47 as diagnostic and drift-sensitive, not as a current launch green gate.
7. Compose a plain answer with sandbox-only boundaries.
8. Stop or escalate on drift, authority confusion, protected path touch, or user-approval requirement.

Default command for this slice:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_operator_launch_checklist.py
```

Builder-only rebuild command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_operator_launch_checklist.py --rebuild
```

The checklist has {len(checklist['source_chain'])} source slices and {len(checklist['launch_sequence'])} ordered steps.
"""


def markdown_oracle(oracle: dict[str, list[str]]) -> str:
    lines = [
        "---",
        "record_kind: failure_case_oracle_doc",
        f"slice_id: {SLICE_ID}",
        "status: built_pending_review",
        "---",
        "",
        "# Failure Case Oracle",
        "",
        "Each failure case must fail with the listed verifier errors.",
        "",
    ]
    for filename, errors in sorted(oracle.items()):
        lines.append(f"- `{filename}`: {', '.join(errors)}")
    lines.append("")
    return "\n".join(lines)


def readout(checklist: dict) -> str:
    return f"""---
record_kind: operator_launch_readout
slice_id: {SLICE_ID}
status: built_pending_review
---

# Operator Launch Checklist

Use this as the human-facing launch surface after p2-48 passes.

## Quick Start

1. Run the p2-48 freeze final gate:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox\\artifact\\verify_freeze_bundle.py --final-gate
```

2. If it fails, stop. Do not use the handoff chain until the changed source slice is inspected.
3. If it passes, read p2-44 for the improvement ledger, p2-45 for handoff wording, p2-46 for status interpretation, and p2-47 for portability risk.
4. Treat p2-47 as drift-sensitive diagnostic context, not as a current launch green gate.
5. Answer plainly: sandbox product-grade chain is verified, but it is still not mainline, not formal vault, not reviewed knowledge, not evidence support, and not action basis.

## Source Chain

{chr(10).join(f"- `{item['slice_id']}`: {item['role']}" for item in checklist['source_chain'])}

## Stop Immediately If

{chr(10).join(f"- `{condition}`" for condition in REQUIRED_STOP_CONDITIONS)}

## Non-Claims

{chr(10).join(f"- {claim}" for claim in REQUIRED_NON_CLAIMS)}
"""


def prototype_files(checklist: dict) -> dict[str, str]:
    receipt = {
        "record_kind": "operator_launch_prototype_receipt",
        "slice_id": SLICE_ID,
        "source_slice_count": len(checklist["source_chain"]),
        "launch_step_count": len(checklist["launch_sequence"]),
        "truth_boundary": checklist["truth_boundary"],
        "required_non_claims": REQUIRED_NON_CLAIMS,
    }
    index = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>VAKS Operator Launch Checklist</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">Sandbox only</p>
      <h1>Operator Launch Checklist</h1>
      <p>Run the freeze check first. Stop on drift. Do not treat this as mainline or action authority.</p>
    </header>
    <section id="summary"></section>
    <section id="steps"></section>
    <section id="boundaries"></section>
  </main>
  <script src="app.js"></script>
</body>
</html>
"""
    style = """body{margin:0;font-family:Arial,sans-serif;background:#f7f7f4;color:#202124}main{max-width:980px;margin:0 auto;padding:32px 20px}header{border-bottom:2px solid #202124;padding-bottom:18px}.eyebrow{text-transform:uppercase;font-size:12px;letter-spacing:.08em;color:#666}h1{font-size:34px;margin:8px 0 10px}.panel{border:1px solid #c9c9c0;border-radius:6px;background:white;margin:18px 0;padding:18px}.step{display:grid;grid-template-columns:110px 1fr;gap:12px;border-top:1px solid #ddd;padding:12px 0}.code{font-family:Consolas,monospace;background:#f0f0eb;padding:8px;border-radius:4px;overflow:auto}.warn{color:#8a3a00;font-weight:700}ul{padding-left:20px}"""
    app = f"""const checklist = {json.dumps(checklist, indent=2, ensure_ascii=False)};
document.getElementById('summary').innerHTML = `<div class="panel"><strong>${{checklist.source_chain.length}}</strong> source slices, <strong>${{checklist.launch_sequence.length}}</strong> launch steps. <span class="warn">Sandbox only.</span></div>`;
document.getElementById('steps').innerHTML = `<div class="panel"><h2>Steps</h2>${{checklist.launch_sequence.map(step => `<div class="step"><strong>${{step.step_id}}</strong><div><b>${{step.title}}</b><p>${{step.operator_action}}</p>${{step.command_hint ? `<div class="code">${{step.command_hint}}</div>` : ''}}</div></div>`).join('')}}</div>`;
document.getElementById('boundaries').innerHTML = `<div class="panel"><h2>Stop Immediately If</h2><ul>${{checklist.stop_conditions.map(item => `<li>${{item}}</li>`).join('')}}</ul><h2>Non-Claims</h2><ul>${{checklist.required_non_claims.map(item => `<li>${{item}}</li>`).join('')}}</ul></div>`;
"""
    return {
        "prototype/operator-launch-checklist/receipt.json": json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        "prototype/operator-launch-checklist/index.html": index,
        "prototype/operator-launch-checklist/style.css": style,
        "prototype/operator-launch-checklist/app.js": app,
    }


def report_text(name: str, status: str, body: str) -> str:
    return f"""---
record_kind: sandbox_report
slice_id: {SLICE_ID}
report: {name}
status: {status}
---

# {name.replace('-', ' ').title()}

{body}
"""


def rebuild() -> dict:
    root = slice_root()
    for generated_dir in ["fixtures", "failure-cases", "readouts", "prototype"]:
        target = root / generated_dir
        if target.exists():
            shutil.rmtree(target)
    checklist = build_checklist()
    write_json(root / "artifact" / "operator-launch-checklist.json", checklist)
    write_text(root / "artifact" / "operator-launch-checklist-contract.md", markdown_contract(checklist))
    write_text(root / "readouts" / "operator-launch-checklist.md", readout(checklist))

    fixtures = {
        "valid-operator-launch-checklist.json": checklist,
        "valid-launch-sequence.json": {**checklist, "fixture_focus": "launch_sequence"},
        "valid-boundary-stop-policy.json": {**checklist, "fixture_focus": "boundary_stop_policy"},
    }
    for filename, data in fixtures.items():
        write_json(root / "fixtures" / filename, data)

    oracle: dict[str, list[str]] = {}
    for idx, name in enumerate(failure_mutations(), start=1):
        data = mutate(checklist, name)
        errors = validate_config(data)
        filename = f"{idx:03d}-{name}.json"
        write_json(root / "failure-cases" / filename, data)
        oracle[filename] = errors
    write_json(root / "artifact" / "failure-case-oracle.json", oracle)
    write_text(root / "artifact" / "failure-case-oracle.md", markdown_oracle(oracle))

    for path, text in prototype_files(checklist).items():
        write_text(root / path, text)

    write_text(
        root / "slice-plan.md",
        report_text(
            "slice-plan",
            "built_pending_review",
            "Build a read-only operator launch checklist for p2-44 through p2-48. It must order the freeze gate first, then read ledger/handoff/status/portability materials, and stop on drift or authority confusion.",
        ),
    )
    write_text(
        root / "source-map.md",
        report_text(
            "source-map",
            "built_pending_review",
            "Sources are p2-44 evidence ledger, p2-45 release-candidate handoff, p2-46 status normalization audit, p2-47 portability audit, and p2-48 checksum freeze bundle. This map is not reviewed truth, evidence support, action basis, mainline readiness, or formal vault approval.",
        ),
    )
    write_text(
        root / "verification.md",
        report_text(
            "verification",
            "local_verification_passed_pending_review",
            f"Run `python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_operator_launch_checklist.py` for the default read-only verifier. Run `--final-gate` only after Reviewer, Boundary, and Product reports are written.",
        ),
    )
    write_text(
        root / "reviewer-report.md",
        report_text("reviewer-report", "pending_reviewer", "Pending independent Reviewer check."),
    )
    write_text(
        root / "boundary-audit.md",
        report_text("boundary-audit", "pending_boundary_audit", "Pending independent Boundary Auditor check."),
    )
    write_text(
        root / "product-acceptance-report.md",
        report_text("product-acceptance-report", "pending_product_acceptance", "Pending GPT-5.5 extra-high Product Acceptance."),
    )
    write_text(
        root / "next-step.md",
        report_text(
            "next-step",
            "pending_product_acceptance",
            "If Product Acceptance passes, the next useful slice is a final sandbox closeout readiness dossier that packages what is ready for possible user-approved promotion without granting promotion.",
        ),
    )
    return checklist


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    if args.rebuild:
        checklist = rebuild()
    else:
        checklist = json.loads((slice_root() / "artifact" / "operator-launch-checklist.json").read_text(encoding="utf-8"))
    errors = validate_config(checklist)
    print(json.dumps({"slice_id": SLICE_ID, "rebuilt": args.rebuild, "errors": errors}, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
