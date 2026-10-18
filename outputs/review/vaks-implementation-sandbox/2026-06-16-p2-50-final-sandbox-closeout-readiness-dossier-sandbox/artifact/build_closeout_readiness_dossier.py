from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from copy import deepcopy
from datetime import date
from pathlib import Path


SLICE_ID = "2026-06-16-p2-50-final-sandbox-closeout-readiness-dossier-sandbox"
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
        "role": "release-candidate handoff without release authority",
        "verifier": "artifact/verify_release_candidate_handoff.py",
        "primary_artifact": "artifact/release-candidate-handoff.json",
        "readout": "handoff-packets/release-candidate-handoff.md",
    },
    {
        "slice_id": "2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox",
        "role": "legacy status normalization compatibility audit",
        "verifier": "artifact/verify_status_normalization_audit.py",
        "primary_artifact": "artifact/status-normalization-audit.json",
        "readout": "readouts/status-normalization-guide.md",
    },
    {
        "slice_id": "2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox",
        "role": "verifier portability diagnostic reference",
        "verifier": "artifact/verify_portability_audit.py",
        "primary_artifact": "artifact/verifier-portability-audit.json",
        "readout": "readouts/verifier-portability-guide.md",
        "known_current_note": "Historical Product PASS, but current dynamic verifier is drift-sensitive after later verifier files were added; not a launch green gate.",
    },
    {
        "slice_id": "2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox",
        "role": "checksum freeze and drift detector",
        "verifier": "artifact/verify_freeze_bundle.py",
        "primary_artifact": "artifact/evidence-chain-freeze-manifest.json",
        "readout": "readouts/evidence-chain-freeze-guide.md",
    },
    {
        "slice_id": "2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox",
        "role": "operator launch checklist and handoff start sequence",
        "verifier": "artifact/verify_operator_launch_checklist.py",
        "primary_artifact": "artifact/operator-launch-checklist.json",
        "readout": "readouts/operator-launch-checklist.md",
        "required_upstream_gate": "python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox\\artifact\\verify_operator_launch_checklist.py --final-gate",
    },
]

REQUEST_CATEGORIES = [
    {
        "request_id": "mainline_merge_review",
        "label": "User-approved mainline merge review",
        "current_status": "requires_separate_user_approval",
        "automatic_authority": False,
        "why": "Sandbox product-grade artifacts are candidates for review, not merge approval.",
    },
    {
        "request_id": "formal_vault_or_obsidian_write",
        "label": "Formal vault or Obsidian write/sync",
        "current_status": "requires_separate_user_approval",
        "automatic_authority": False,
        "why": "No sandbox PASS grants formal vault write, sync, or state authority.",
    },
    {
        "request_id": "reviewed_knowledge_or_evidence_support",
        "label": "Reviewed knowledge / evidence support / action basis",
        "current_status": "requires_separate_review_and_user_approval",
        "automatic_authority": False,
        "why": "Validators and receipts are process evidence, not reviewed truth or action support.",
    },
    {
        "request_id": "commit_push_or_release",
        "label": "Commit, push, release, or promotion",
        "current_status": "requires_separate_user_approval",
        "automatic_authority": False,
        "why": "This dossier records readiness to ask, not permission to execute.",
    },
    {
        "request_id": "template_or_tool_movement",
        "label": "Move sandbox logic into templates/tools",
        "current_status": "requires_separate_design_review_and_user_approval",
        "automatic_authority": False,
        "why": "Templates/tools are protected in this run and old dirty baseline is not part of this slice.",
    },
]

FORBIDDEN_CLAIMS = [
    "release approved",
    "promotion approved",
    "mainline ready",
    "enterprise production ready",
    "formal vault approved",
    "Obsidian sync approved",
    "commit authorized",
    "push authorized",
    "reviewed knowledge",
    "evidence support",
    "action basis",
    "user approval collected",
    "execution permission granted",
    "runtime certified",
    "re-accepted",
    "auto advance",
]

REQUIRED_NON_CLAIMS = [
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
    "not user approval",
    "not execution permission",
    "not runtime certification",
    "not re-acceptance",
    "not auto advance",
]

STOP_CONDITIONS = [
    "p2_49_final_gate_failed",
    "source_product_status_not_pass_product_grade",
    "protected_path_touched_by_current_slice",
    "dossier_claims_authority",
    "request_category_auto_authority_true",
    "p2_47_drift_hidden_as_green",
    "user_approval_required_before_any_execution",
]

READINESS_FALSE = [
    "release_approved",
    "promotion_approved",
    "mainline_ready",
    "enterprise_production_ready",
    "formal_vault_ready",
    "obsidian_sync_ready",
    "reviewed_knowledge_ready",
    "evidence_support_ready",
    "action_basis_ready",
    "commit_authorized",
    "push_authorized",
    "user_approval_collected",
    "execution_permission_granted",
    "auto_advance_allowed",
]

OPERATION_FALSE = [
    "old_slice_modified",
    "mainline_merge",
    "formal_vault_write",
    "obsidian_sync",
    "commit",
    "push",
    "promotion",
    "release",
    "dependency_install",
    "background_service",
    "hooks",
    "mcp_write_tool",
    "template_write",
    "tool_write",
    "reviewed_knowledge_write",
    "action_basis_creation",
]


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
        "sha256": sha256(path) if path.exists() else None,
        "size_bytes": path.stat().st_size if path.exists() else None,
        "frontmatter_status": frontmatter_status(path) if path.suffix.lower() == ".md" else None,
    }


def source_entry(item: dict) -> dict:
    base = repo_root() / "outputs" / "review" / "vaks-implementation-sandbox" / item["slice_id"]
    verifier_command_path = item["verifier"].replace("/", "\\")
    return {
        "slice_id": item["slice_id"],
        "role": item["role"],
        "source_root": rel(base),
        "product_acceptance_report": file_entry(base / "product-acceptance-report.md"),
        "verification_report": file_entry(base / "verification.md"),
        "reviewer_report": file_entry(base / "reviewer-report.md"),
        "boundary_audit": file_entry(base / "boundary-audit.md"),
        "primary_artifact": file_entry(base / item["primary_artifact"]),
        "readout": file_entry(base / item["readout"]),
        "verifier": file_entry(base / item["verifier"]),
        "manual_verifier_command": f"python -B .\\outputs\\review\\vaks-implementation-sandbox\\{item['slice_id']}\\{verifier_command_path}",
        "product_status_required": "pass_product_grade",
        "known_current_note": item.get("known_current_note", ""),
        "required_upstream_gate": item.get("required_upstream_gate", ""),
    }


def build_dossier() -> dict:
    sources = [source_entry(item) for item in SOURCE_SLICES]
    return {
        "record_kind": "final_sandbox_closeout_readiness_dossier",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "generated_at": date.today().isoformat(),
        "purpose": "package sandbox product-grade evidence for possible user decision without granting authority",
        "truth_boundary": "sandbox_closeout_readiness_not_promotion_or_action_authority",
        "write_scope": f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/",
        "source_chain": sources,
        "required_upstream_gate": SOURCE_SLICES[-1]["required_upstream_gate"],
        "closeout_verdict": {
            "sandbox_chain_product_grade": True,
            "ready_to_request_user_decision": True,
            "ready_to_execute": False,
            "ready_to_merge_mainline": False,
            "ready_for_formal_vault_write": False,
            "ready_as_action_basis": False,
        },
        "request_categories": REQUEST_CATEGORIES,
        "decision_table": [
            {
                "item": "Use as sandbox evidence",
                "status": "allowed_within_sandbox",
                "requires_user_approval": False,
                "notes": "Only for explaining sandbox state and planning the next user decision.",
            },
            {
                "item": "Ask user whether to review for promotion",
                "status": "ready_to_ask",
                "requires_user_approval": False,
                "notes": "The dossier can ask; it cannot decide or execute.",
            },
            {
                "item": "Merge, promote, sync, commit, push, or use as action basis",
                "status": "blocked_until_explicit_user_approval",
                "requires_user_approval": True,
                "notes": "Separate approval and likely separate review are required.",
            },
        ],
        "p2_47_current_handling": {
            "historical_product_pass": True,
            "current_dynamic_verifier_drift_sensitive": True,
            "allowed_use": "diagnostic_reference_only",
            "forbidden_use": "current_launch_green_gate",
        },
        "readiness_flags": {
            "closeout_dossier_ready": True,
            "ready_to_request_user_decision": True,
            **{key: False for key in READINESS_FALSE},
        },
        "operation_flags": {key: False for key in OPERATION_FALSE},
        "stop_conditions": STOP_CONDITIONS,
        "required_non_claims": REQUIRED_NON_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "acceptance_contract": {
            "requires_reviewer_pass": True,
            "requires_boundary_pass": True,
            "requires_gpt_5_5_extra_high_product_acceptance": True,
            "product_acceptance_is_only_pass_authority_for_this_slice": True,
            "p2_49_final_gate_must_pass": True,
        },
    }


def validate_config(data: dict) -> list[str]:
    errors: list[str] = []
    expected = {
        "record_kind": "final_sandbox_closeout_readiness_dossier",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": "sandbox_closeout_readiness_not_promotion_or_action_authority",
        "write_scope": f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"top_level_{key}")

    sources = data.get("source_chain")
    if not isinstance(sources, list) or len(sources) != len(SOURCE_SLICES):
        errors.append("source_chain_count")
        sources = []
    else:
        expected_ids = [item["slice_id"] for item in SOURCE_SLICES]
        actual_ids = [item.get("slice_id") for item in sources]
        if actual_ids != expected_ids:
            errors.append("source_chain_order")
        for source in sources:
            sid = source.get("slice_id", "unknown")
            for key in ["product_acceptance_report", "verification_report", "reviewer_report", "boundary_audit", "primary_artifact", "readout", "verifier"]:
                if source.get(key, {}).get("exists") is not True:
                    errors.append(f"source_missing_{sid}_{key}")
            if source.get("product_acceptance_report", {}).get("frontmatter_status") != "pass_product_grade":
                errors.append(f"source_product_status_{sid}")
            if source.get("product_status_required") != "pass_product_grade":
                errors.append(f"source_required_status_{sid}")
            command = source.get("manual_verifier_command", "")
            if "python -B" not in command or "verify_" not in command:
                errors.append(f"source_bad_manual_command_{sid}")
            if sid == "2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox":
                note = source.get("known_current_note", "")
                if "drift-sensitive" not in note or "not a launch green gate" not in note:
                    errors.append("p2_47_drift_note_missing")
            if sid == "2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox":
                gate = source.get("required_upstream_gate", "")
                if "verify_operator_launch_checklist.py --final-gate" not in gate:
                    errors.append("p2_49_required_gate_missing")

    if "verify_operator_launch_checklist.py --final-gate" not in data.get("required_upstream_gate", ""):
        errors.append("required_upstream_gate_missing")

    verdict = data.get("closeout_verdict", {})
    expected_verdict = {
        "sandbox_chain_product_grade": True,
        "ready_to_request_user_decision": True,
        "ready_to_execute": False,
        "ready_to_merge_mainline": False,
        "ready_for_formal_vault_write": False,
        "ready_as_action_basis": False,
    }
    for key, value in expected_verdict.items():
        if verdict.get(key) is not value:
            errors.append(f"closeout_verdict_{key}")

    requests = data.get("request_categories")
    if not isinstance(requests, list) or len(requests) != len(REQUEST_CATEGORIES):
        errors.append("request_category_count")
        requests = []
    for item in requests:
        rid = item.get("request_id", "unknown")
        if item.get("automatic_authority") is not False:
            errors.append(f"request_auto_authority_{rid}")
        if "requires_" not in item.get("current_status", ""):
            errors.append(f"request_status_not_requires_{rid}")

    p247 = data.get("p2_47_current_handling", {})
    if p247.get("current_dynamic_verifier_drift_sensitive") is not True:
        errors.append("p2_47_not_marked_drift_sensitive")
    if p247.get("forbidden_use") != "current_launch_green_gate":
        errors.append("p2_47_forbidden_use")

    readiness = data.get("readiness_flags", {})
    if readiness.get("closeout_dossier_ready") is not True:
        errors.append("closeout_dossier_not_ready")
    if readiness.get("ready_to_request_user_decision") is not True:
        errors.append("not_ready_to_request_user_decision")
    for key in READINESS_FALSE:
        if readiness.get(key) is not False:
            errors.append(f"readiness_{key}_not_false")

    ops = data.get("operation_flags", {})
    for key in OPERATION_FALSE:
        if ops.get(key) is not False:
            errors.append(f"operation_{key}_not_false")

    stop_conditions = data.get("stop_conditions", [])
    for condition in STOP_CONDITIONS:
        if condition not in stop_conditions:
            errors.append(f"missing_stop_condition_{condition}")

    non_claims = data.get("required_non_claims", [])
    for claim in REQUIRED_NON_CLAIMS:
        if claim not in non_claims:
            errors.append(f"missing_non_claim_{claim.replace(' ', '_')}")
    if any(claim not in REQUIRED_NON_CLAIMS for claim in non_claims):
        errors.append("extra_non_claim")

    forbidden = data.get("forbidden_claims", [])
    for claim in FORBIDDEN_CLAIMS:
        if claim not in forbidden:
            errors.append(f"missing_forbidden_claim_{claim.replace(' ', '_')}")

    contract = data.get("acceptance_contract", {})
    for key in [
        "requires_reviewer_pass",
        "requires_boundary_pass",
        "requires_gpt_5_5_extra_high_product_acceptance",
        "product_acceptance_is_only_pass_authority_for_this_slice",
        "p2_49_final_gate_must_pass",
    ]:
        if contract.get(key) is not True:
            errors.append(f"acceptance_contract_{key}")

    return sorted(set(errors))


def mutate(base: dict, name: str) -> dict:
    data = deepcopy(base)
    if name == "top-level-record-kind":
        data["record_kind"] = "closeout_dossier"
    elif name == "top-level-slice-id":
        data["slice_id"] = "wrong"
    elif name == "top-level-version":
        data["version"] = "0.0"
    elif name == "top-level-truth-boundary":
        data["truth_boundary"] = "promotion_authority"
    elif name == "top-level-write-scope":
        data["write_scope"] = "outputs/review/"
    elif name == "source-chain-count":
        data["source_chain"] = data["source_chain"][:-1]
    elif name == "source-chain-order":
        data["source_chain"][0], data["source_chain"][1] = data["source_chain"][1], data["source_chain"][0]
    elif name == "source-product-status":
        data["source_chain"][0]["product_acceptance_report"]["frontmatter_status"] = "pending"
    elif name == "source-missing-artifact":
        data["source_chain"][0]["primary_artifact"]["exists"] = False
    elif name == "source-bad-command":
        data["source_chain"][0]["manual_verifier_command"] = "python verifier.py"
    elif name == "p2-47-note-missing":
        data["source_chain"][3]["known_current_note"] = ""
    elif name == "p2-49-required-gate-missing":
        data["source_chain"][5]["required_upstream_gate"] = ""
    elif name == "required-upstream-gate-missing":
        data["required_upstream_gate"] = ""
    elif name.startswith("closeout-verdict-"):
        key = name.removeprefix("closeout-verdict-")
        data["closeout_verdict"][key] = not data["closeout_verdict"][key]
    elif name == "request-auto-authority":
        data["request_categories"][0]["automatic_authority"] = True
    elif name == "request-status-not-requires":
        data["request_categories"][0]["current_status"] = "approved"
    elif name == "p2-47-not-drift-sensitive":
        data["p2_47_current_handling"]["current_dynamic_verifier_drift_sensitive"] = False
    elif name == "p2-47-forbidden-use-green":
        data["p2_47_current_handling"]["forbidden_use"] = "allowed_green_gate"
    elif name == "closeout-dossier-not-ready":
        data["readiness_flags"]["closeout_dossier_ready"] = False
    elif name == "not-ready-to-request-user-decision":
        data["readiness_flags"]["ready_to_request_user_decision"] = False
    elif name.startswith("readiness-"):
        key = name.removeprefix("readiness-")
        data["readiness_flags"][key] = True
    elif name.startswith("operation-"):
        key = name.removeprefix("operation-")
        data["operation_flags"][key] = True
    elif name.startswith("missing-stop-"):
        condition = name.removeprefix("missing-stop-")
        data["stop_conditions"] = [c for c in data["stop_conditions"] if c != condition]
    elif name.startswith("missing-non-claim-"):
        claim = name.removeprefix("missing-non-claim-").replace("_", " ")
        data["required_non_claims"] = [c for c in data["required_non_claims"] if c != claim]
    elif name == "extra-non-claim":
        data["required_non_claims"].append("production approved")
    elif name.startswith("missing-forbidden-claim-"):
        claim = name.removeprefix("missing-forbidden-claim-").replace("_", " ")
        data["forbidden_claims"] = [c for c in data["forbidden_claims"] if c != claim]
    elif name.startswith("acceptance-contract-"):
        key = name.removeprefix("acceptance-contract-")
        data["acceptance_contract"][key] = False
    else:
        raise ValueError(name)
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
        "source-missing-artifact",
        "source-bad-command",
        "p2-47-note-missing",
        "p2-49-required-gate-missing",
        "required-upstream-gate-missing",
        "closeout-verdict-sandbox_chain_product_grade",
        "closeout-verdict-ready_to_request_user_decision",
        "closeout-verdict-ready_to_execute",
        "closeout-verdict-ready_to_merge_mainline",
        "closeout-verdict-ready_for_formal_vault_write",
        "closeout-verdict-ready_as_action_basis",
        "request-auto-authority",
        "request-status-not-requires",
        "p2-47-not-drift-sensitive",
        "p2-47-forbidden-use-green",
        "closeout-dossier-not-ready",
        "not-ready-to-request-user-decision",
        "extra-non-claim",
    ]
    names.extend(f"readiness-{key}" for key in READINESS_FALSE)
    names.extend(f"operation-{key}" for key in OPERATION_FALSE)
    names.extend(f"missing-stop-{key}" for key in STOP_CONDITIONS)
    names.extend(f"missing-non-claim-{key.replace(' ', '_')}" for key in REQUIRED_NON_CLAIMS)
    names.extend(f"missing-forbidden-claim-{key.replace(' ', '_')}" for key in FORBIDDEN_CLAIMS)
    names.extend(
        [
            "acceptance-contract-requires_reviewer_pass",
            "acceptance-contract-requires_boundary_pass",
            "acceptance-contract-requires_gpt_5_5_extra_high_product_acceptance",
            "acceptance-contract-product_acceptance_is_only_pass_authority_for_this_slice",
            "acceptance-contract-p2_49_final_gate_must_pass",
        ]
    )
    return names


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def report_text(report: str, status: str, body: str) -> str:
    return f"""---
record_kind: sandbox_report
slice_id: {SLICE_ID}
report: {report}
status: {status}
---

# {report.replace('-', ' ').title()}

{body}
"""


def contract_text(dossier: dict) -> str:
    return f"""---
record_kind: sandbox_contract
slice_id: {SLICE_ID}
status: built_pending_review
---

# Final Sandbox Closeout Readiness Contract

This dossier packages sandbox Product PASS evidence so a human can decide what to review next.

It is not release approval, promotion approval, mainline readiness, enterprise production readiness, formal vault approval, Obsidian sync, commit authorization, push authorization, reviewed knowledge, evidence support, action basis, user approval, execution permission, runtime certification, re-acceptance, or auto advance.

Required upstream gate:

```powershell
{dossier['required_upstream_gate']}
```

Permitted use:

- Explain sandbox status.
- Ask the user whether they want a separately approved promotion/review/merge path.
- Preserve stop conditions and non-claims.

Forbidden use:

- Execute merge, promotion, vault write/sync, commit, push, or action-basis creation.
- Treat p2-47 as a current green gate.
- Treat Product PASS as user approval.
"""


def readout_text(dossier: dict) -> str:
    requests = "\n".join(
        f"- `{item['request_id']}`: {item['current_status']} / automatic authority = {item['automatic_authority']}"
        for item in dossier["request_categories"]
    )
    return f"""---
record_kind: final_closeout_readout
slice_id: {SLICE_ID}
status: built_pending_review
---

# Final Sandbox Closeout Readiness Dossier

This is the closeout surface for p2-44 through p2-49. It is ready to ask for a user decision, not ready to execute.

## Plain Verdict

The sandbox chain is product-grade enough to ask the user what they want to review next. It is not approval to merge, promote, write the formal vault, sync Obsidian, commit, push, create reviewed knowledge, create evidence support, or use anything as action basis.

## Request Categories

{requests}

## Stop Conditions

{chr(10).join(f'- `{item}`' for item in STOP_CONDITIONS)}

## p2-47 Note

p2-47 is historical Product PASS and diagnostic reference. Its current dynamic verifier is drift-sensitive after later verifier files were added, so this dossier must not treat it as a current launch green gate.

## Required Upstream Gate

```powershell
{dossier['required_upstream_gate']}
```
"""


def oracle_text(oracle: dict[str, list[str]]) -> str:
    lines = [
        "---",
        "record_kind: failure_case_oracle_doc",
        f"slice_id: {SLICE_ID}",
        "status: built_pending_review",
        "---",
        "",
        "# Failure Case Oracle",
        "",
    ]
    for filename, errors in sorted(oracle.items()):
        lines.append(f"- `{filename}`: {', '.join(errors)}")
    lines.append("")
    return "\n".join(lines)


def prototype_files(dossier: dict) -> dict[str, str]:
    receipt = {
        "record_kind": "closeout_dossier_prototype_receipt",
        "slice_id": SLICE_ID,
        "source_slice_count": len(dossier["source_chain"]),
        "request_category_count": len(dossier["request_categories"]),
        "truth_boundary": dossier["truth_boundary"],
    }
    index = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>VAKS Closeout Readiness</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">Sandbox closeout</p>
      <h1>Readiness Dossier</h1>
      <p>Ready to ask. Not ready to execute.</p>
    </header>
    <section id="verdict"></section>
    <section id="requests"></section>
    <section id="stops"></section>
    <section id="nonclaims"></section>
  </main>
  <script src="app.js"></script>
</body>
</html>
"""
    style = """body{margin:0;font-family:Arial,sans-serif;background:#f6f7f2;color:#222}main{max-width:1040px;margin:0 auto;padding:32px 20px}header{border-bottom:2px solid #222;padding-bottom:16px}.eyebrow{text-transform:uppercase;font-size:12px;color:#666;letter-spacing:.08em}h1{font-size:34px;margin:6px 0 10px}.panel{background:#fff;border:1px solid #cfd2c5;border-radius:6px;margin:18px 0;padding:18px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.item{border-top:1px solid #ddd;padding-top:10px}.blocked{color:#8c3300;font-weight:700}.ok{color:#236b3b;font-weight:700}ul{padding-left:20px}code{background:#eee;padding:2px 4px;border-radius:3px}"""
    app = f"""const dossier = {json.dumps(dossier, indent=2, ensure_ascii=False)};
document.getElementById('verdict').innerHTML = `<div class="panel"><h2>Verdict</h2><p><span class="ok">Ready to ask for a user decision.</span> <span class="blocked">Not ready to execute.</span></p></div>`;
document.getElementById('requests').innerHTML = `<div class="panel"><h2>Request Categories</h2><div class="grid">${{dossier.request_categories.map(item => `<div class="item"><b>${{item.label}}</b><p><code>${{item.current_status}}</code></p><p>Automatic authority: ${{item.automatic_authority}}</p></div>`).join('')}}</div></div>`;
document.getElementById('stops').innerHTML = `<div class="panel"><h2>Stop Conditions</h2><ul>${{dossier.stop_conditions.map(item => `<li>${{item}}</li>`).join('')}}</ul></div>`;
document.getElementById('nonclaims').innerHTML = `<div class="panel"><h2>Non-Claims</h2><ul>${{dossier.required_non_claims.map(item => `<li>${{item}}</li>`).join('')}}</ul></div>`;
"""
    return {
        "prototype/final-closeout-readiness/receipt.json": json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        "prototype/final-closeout-readiness/index.html": index,
        "prototype/final-closeout-readiness/style.css": style,
        "prototype/final-closeout-readiness/app.js": app,
    }


def rebuild() -> dict:
    root = slice_root()
    for generated in ["fixtures", "failure-cases", "readouts", "prototype"]:
        target = root / generated
        if target.exists():
            shutil.rmtree(target)
    dossier = build_dossier()
    write_json(root / "artifact" / "final-sandbox-closeout-readiness-dossier.json", dossier)
    write_text(root / "artifact" / "closeout-readiness-contract.md", contract_text(dossier))
    write_text(root / "readouts" / "final-sandbox-closeout-readiness-dossier.md", readout_text(dossier))

    fixtures = {
        "valid-closeout-readiness-dossier.json": dossier,
        "valid-user-decision-request-table.json": {**dossier, "fixture_focus": "user_decision_request_table"},
        "valid-boundary-non-authority-closeout.json": {**dossier, "fixture_focus": "boundary_non_authority"},
    }
    for filename, data in fixtures.items():
        write_json(root / "fixtures" / filename, data)

    oracle: dict[str, list[str]] = {}
    for idx, name in enumerate(failure_mutations(), start=1):
        data = mutate(dossier, name)
        errors = validate_config(data)
        filename = f"{idx:03d}-{name}.json"
        write_json(root / "failure-cases" / filename, data)
        oracle[filename] = errors
    write_json(root / "artifact" / "failure-case-oracle.json", oracle)
    write_text(root / "artifact" / "failure-case-oracle.md", oracle_text(oracle))

    for path, text in prototype_files(dossier).items():
        write_text(root / path, text)

    write_text(
        root / "slice-plan.md",
        report_text(
            "slice-plan",
            "built_pending_review",
            "Build the final sandbox closeout readiness dossier for p2-44 through p2-49. The dossier can support a user decision request, but cannot grant promotion, merge, formal vault, or action authority.",
        ),
    )
    write_text(
        root / "source-map.md",
        report_text(
            "source-map",
            "built_pending_review",
            "Sources are p2-44 evidence ledger, p2-45 handoff, p2-46 status normalization, p2-47 portability diagnostic, p2-48 checksum freeze, and p2-49 operator launch checklist. This map is sandbox trace only.",
        ),
    )
    write_text(
        root / "verification.md",
        report_text(
            "verification",
            "local_verification_passed_pending_review",
            f"Run `python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_closeout_readiness_dossier.py`. Run `--final-gate` only after Reviewer, Boundary, and Product reports are written.",
        ),
    )
    write_text(root / "reviewer-report.md", report_text("reviewer-report", "pending_reviewer", "Pending independent Reviewer check."))
    write_text(root / "boundary-audit.md", report_text("boundary-audit", "pending_boundary_audit", "Pending Boundary Auditor check."))
    write_text(root / "product-acceptance-report.md", report_text("product-acceptance-report", "pending_product_acceptance", "Pending GPT-5.5 extra-high Product Acceptance."))
    write_text(
        root / "next-step.md",
        report_text(
            "next-step",
            "pending_product_acceptance",
            "If Product Acceptance passes, stop and ask the user before any promotion, mainline merge, formal vault write, commit, push, or action-basis use.",
        ),
    )
    return dossier


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    if args.rebuild:
        dossier = rebuild()
    else:
        dossier = json.loads((slice_root() / "artifact" / "final-sandbox-closeout-readiness-dossier.json").read_text(encoding="utf-8"))
    errors = validate_config(dossier)
    print(json.dumps({"slice_id": SLICE_ID, "rebuilt": args.rebuild, "errors": errors}, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
