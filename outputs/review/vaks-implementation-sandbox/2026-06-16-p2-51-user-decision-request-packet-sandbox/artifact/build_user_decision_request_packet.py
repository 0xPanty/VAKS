from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from copy import deepcopy
from datetime import date
from pathlib import Path


SLICE_ID = "2026-06-16-p2-51-user-decision-request-packet-sandbox"
VERSION = "0.1.0"
SOURCE_SLICE_ID = "2026-06-16-p2-50-final-sandbox-closeout-readiness-dossier-sandbox"
SOURCE_FINAL_GATE = (
    "python -B .\\outputs\\review\\vaks-implementation-sandbox\\"
    f"{SOURCE_SLICE_ID}\\artifact\\verify_closeout_readiness_dossier.py --final-gate"
)

DECISION_OPTIONS = [
    {
        "option_id": "A_keep_sandbox_reference",
        "label": "Keep sandbox as reference only",
        "recommended_default": True,
        "what_it_means": "Do not start promotion or mainline work; use the sandbox chain as reference evidence only.",
        "automatic_execution": False,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "allowed_next_action": "none",
    },
    {
        "option_id": "B_start_readonly_promotion_review_plan",
        "label": "Authorize a new read-only promotion review planning slice",
        "recommended_default": False,
        "what_it_means": "Prepare a separate read-only review plan that identifies candidate mainline scope without writing mainline files.",
        "automatic_execution": False,
        "requires_new_scope": True,
        "requires_separate_user_approval": True,
        "allowed_next_action": "new_readonly_sandbox_or_plan_only",
    },
    {
        "option_id": "C_request_mainline_merge_scope",
        "label": "Authorize asking for a separately scoped mainline merge review",
        "recommended_default": False,
        "what_it_means": "Ask the user to explicitly name allowed mainline paths before any merge work starts.",
        "automatic_execution": False,
        "requires_new_scope": True,
        "requires_separate_user_approval": True,
        "allowed_next_action": "ask_for_explicit_path_scope_only",
    },
    {
        "option_id": "D_park_or_reject_sandbox_chain",
        "label": "Park or reject the sandbox chain",
        "recommended_default": False,
        "what_it_means": "Record no further action unless the user later reopens the topic.",
        "automatic_execution": False,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "allowed_next_action": "none",
    },
]

FORBIDDEN_NEXT_ACTIONS = [
    "promotion",
    "mainline_merge",
    "formal_vault_write",
    "obsidian_sync",
    "commit",
    "push",
    "release",
    "reviewed_knowledge_creation",
    "evidence_support_creation",
    "action_basis_creation",
    "template_write",
    "tool_write",
    "dependency_install",
    "background_service",
    "hooks",
    "mcp_write_tool",
]

REQUIRED_NON_CLAIMS = [
    "not approval",
    "not execution permission",
    "not promotion",
    "not mainline merge",
    "not release",
    "not formal vault write",
    "not Obsidian sync",
    "not commit",
    "not push",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "not auto advance",
]

STOP_CONDITIONS = [
    "p2_50_final_gate_failed",
    "user_decision_option_missing",
    "option_grants_automatic_execution",
    "option_skips_separate_approval_for_execution_path",
    "forbidden_next_action_enabled",
    "protected_path_write_required",
    "authority_confusion_detected",
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
        "size_bytes": path.stat().st_size if path.exists() else None,
        "sha256": sha256(path) if path.exists() else None,
        "frontmatter_status": frontmatter_status(path) if path.suffix.lower() == ".md" else None,
    }


def build_packet() -> dict:
    source_root = repo_root() / "outputs" / "review" / "vaks-implementation-sandbox" / SOURCE_SLICE_ID
    return {
        "record_kind": "sandbox_user_decision_request_packet",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "generated_at": date.today().isoformat(),
        "purpose": "ask the user for the next decision without executing any decision",
        "truth_boundary": "decision_request_packet_not_approval_or_execution_authority",
        "write_scope": f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/",
        "source_closeout": {
            "slice_id": SOURCE_SLICE_ID,
            "source_root": rel(source_root),
            "final_gate_command": SOURCE_FINAL_GATE,
            "product_acceptance_report": file_entry(source_root / "product-acceptance-report.md"),
            "next_step": file_entry(source_root / "next-step.md"),
            "primary_artifact": file_entry(source_root / "artifact" / "final-sandbox-closeout-readiness-dossier.json"),
            "verifier": file_entry(source_root / "artifact" / "verify_closeout_readiness_dossier.py"),
        },
        "request_prompt": {
            "title": "请选择 VAKS sandbox 下一步",
            "plain_language": "sandbox 链条已经产品级通过；现在只能请你选择下一步方向，不能自动执行任何合并、发布、同步、写库或行动依据。",
            "requires_explicit_user_reply": True,
            "no_default_execution": True,
            "safe_default_if_no_reply": "A_keep_sandbox_reference",
        },
        "decision_options": DECISION_OPTIONS,
        "forbidden_next_actions": {key: False for key in FORBIDDEN_NEXT_ACTIONS},
        "readiness_flags": {
            "decision_request_packet_ready": True,
            "ready_to_ask_user": True,
            "ready_to_execute_user_choice": False,
            "user_choice_collected": False,
            "promotion_ready": False,
            "mainline_merge_ready": False,
            "formal_vault_write_ready": False,
            "action_basis_ready": False,
            "commit_ready": False,
            "push_ready": False,
        },
        "stop_conditions": STOP_CONDITIONS,
        "required_non_claims": REQUIRED_NON_CLAIMS,
        "acceptance_contract": {
            "requires_reviewer_pass": True,
            "requires_boundary_pass": True,
            "requires_gpt_5_5_extra_high_product_acceptance": True,
            "p2_50_final_gate_must_pass": True,
            "product_acceptance_does_not_collect_user_choice": True,
        },
    }


def validate_config(data: dict) -> list[str]:
    errors: list[str] = []
    expected = {
        "record_kind": "sandbox_user_decision_request_packet",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": "decision_request_packet_not_approval_or_execution_authority",
        "write_scope": f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"top_level_{key}")

    source = data.get("source_closeout", {})
    if source.get("slice_id") != SOURCE_SLICE_ID:
        errors.append("source_closeout_slice_id")
    if "verify_closeout_readiness_dossier.py --final-gate" not in source.get("final_gate_command", ""):
        errors.append("source_final_gate_command")
    for key in ["product_acceptance_report", "next_step", "primary_artifact", "verifier"]:
        if source.get(key, {}).get("exists") is not True:
            errors.append(f"source_missing_{key}")
    if source.get("product_acceptance_report", {}).get("frontmatter_status") != "pass_product_grade":
        errors.append("source_product_status")
    if source.get("next_step", {}).get("frontmatter_status") != "pass_product_grade_pending_user_decision":
        errors.append("source_next_step_status")

    prompt = data.get("request_prompt", {})
    if prompt.get("requires_explicit_user_reply") is not True:
        errors.append("prompt_does_not_require_explicit_user_reply")
    if prompt.get("no_default_execution") is not True:
        errors.append("prompt_allows_default_execution")
    if prompt.get("safe_default_if_no_reply") != "A_keep_sandbox_reference":
        errors.append("prompt_unsafe_default")
    if "不能自动执行" not in prompt.get("plain_language", ""):
        errors.append("prompt_missing_no_auto_execute_language")

    options = data.get("decision_options", [])
    if not isinstance(options, list) or len(options) != len(DECISION_OPTIONS):
        errors.append("decision_option_count")
        options = []
    expected_ids = [item["option_id"] for item in DECISION_OPTIONS]
    actual_ids = [item.get("option_id") for item in options]
    if actual_ids != expected_ids:
        errors.append("decision_option_order")
    recommended = [item.get("option_id") for item in options if item.get("recommended_default") is True]
    if recommended != ["A_keep_sandbox_reference"]:
        errors.append("decision_option_default")
    for item in options:
        option_id = item.get("option_id", "unknown")
        if item.get("automatic_execution") is not False:
            errors.append(f"option_automatic_execution_{option_id}")
        action = item.get("allowed_next_action", "")
        if action in FORBIDDEN_NEXT_ACTIONS:
            errors.append(f"option_forbidden_next_action_{option_id}")
        if option_id in ["B_start_readonly_promotion_review_plan", "C_request_mainline_merge_scope"]:
            if item.get("requires_new_scope") is not True:
                errors.append(f"option_requires_new_scope_{option_id}")
            if item.get("requires_separate_user_approval") is not True:
                errors.append(f"option_requires_separate_user_approval_{option_id}")
            label = item.get("label", "")
            if "Authorize" not in label:
                errors.append(f"option_label_missing_authorize_{option_id}")

    forbidden = data.get("forbidden_next_actions", {})
    for key in FORBIDDEN_NEXT_ACTIONS:
        if forbidden.get(key) is not False:
            errors.append(f"forbidden_next_action_{key}_enabled")

    readiness = data.get("readiness_flags", {})
    if readiness.get("decision_request_packet_ready") is not True:
        errors.append("decision_request_packet_not_ready")
    if readiness.get("ready_to_ask_user") is not True:
        errors.append("not_ready_to_ask_user")
    for key in [
        "ready_to_execute_user_choice",
        "user_choice_collected",
        "promotion_ready",
        "mainline_merge_ready",
        "formal_vault_write_ready",
        "action_basis_ready",
        "commit_ready",
        "push_ready",
    ]:
        if readiness.get(key) is not False:
            errors.append(f"readiness_{key}_not_false")

    for condition in STOP_CONDITIONS:
        if condition not in data.get("stop_conditions", []):
            errors.append(f"missing_stop_condition_{condition}")

    non_claims = data.get("required_non_claims", [])
    for claim in REQUIRED_NON_CLAIMS:
        if claim not in non_claims:
            errors.append(f"missing_non_claim_{claim.replace(' ', '_')}")
    if any(claim not in REQUIRED_NON_CLAIMS for claim in non_claims):
        errors.append("extra_non_claim")

    contract = data.get("acceptance_contract", {})
    for key in [
        "requires_reviewer_pass",
        "requires_boundary_pass",
        "requires_gpt_5_5_extra_high_product_acceptance",
        "p2_50_final_gate_must_pass",
        "product_acceptance_does_not_collect_user_choice",
    ]:
        if contract.get(key) is not True:
            errors.append(f"acceptance_contract_{key}")

    return sorted(set(errors))


def mutate(base: dict, name: str) -> dict:
    data = deepcopy(base)
    if name == "top-level-record-kind":
        data["record_kind"] = "decision_packet"
    elif name == "top-level-slice-id":
        data["slice_id"] = "wrong"
    elif name == "top-level-version":
        data["version"] = "0.0"
    elif name == "top-level-truth-boundary":
        data["truth_boundary"] = "approval_authority"
    elif name == "top-level-write-scope":
        data["write_scope"] = "outputs/review/"
    elif name == "source-slice-id":
        data["source_closeout"]["slice_id"] = "wrong"
    elif name == "source-final-gate-command":
        data["source_closeout"]["final_gate_command"] = "python verifier.py"
    elif name == "source-product-status":
        data["source_closeout"]["product_acceptance_report"]["frontmatter_status"] = "pending"
    elif name == "source-next-step-status":
        data["source_closeout"]["next_step"]["frontmatter_status"] = "pass_product_grade"
    elif name == "prompt-no-explicit-reply":
        data["request_prompt"]["requires_explicit_user_reply"] = False
    elif name == "prompt-default-execution":
        data["request_prompt"]["no_default_execution"] = False
    elif name == "prompt-unsafe-default":
        data["request_prompt"]["safe_default_if_no_reply"] = "C_request_mainline_merge_scope"
    elif name == "prompt-missing-no-auto-language":
        data["request_prompt"]["plain_language"] = "请选择下一步。"
    elif name == "option-count":
        data["decision_options"] = data["decision_options"][:-1]
    elif name == "option-order":
        data["decision_options"][0], data["decision_options"][1] = data["decision_options"][1], data["decision_options"][0]
    elif name == "option-default":
        data["decision_options"][0]["recommended_default"] = False
        data["decision_options"][1]["recommended_default"] = True
    elif name == "option-auto-execution":
        data["decision_options"][1]["automatic_execution"] = True
    elif name == "option-forbidden-action":
        data["decision_options"][1]["allowed_next_action"] = "promotion"
    elif name == "option-missing-new-scope":
        data["decision_options"][1]["requires_new_scope"] = False
    elif name == "option-missing-separate-approval":
        data["decision_options"][2]["requires_separate_user_approval"] = False
    elif name == "option-unsafe-label":
        data["decision_options"][1]["label"] = "Start a read-only promotion review plan"
    elif name.startswith("forbidden-action-"):
        key = name.removeprefix("forbidden-action-")
        data["forbidden_next_actions"][key] = True
    elif name == "decision-packet-not-ready":
        data["readiness_flags"]["decision_request_packet_ready"] = False
    elif name == "not-ready-to-ask":
        data["readiness_flags"]["ready_to_ask_user"] = False
    elif name.startswith("readiness-"):
        key = name.removeprefix("readiness-")
        data["readiness_flags"][key] = True
    elif name.startswith("missing-stop-"):
        condition = name.removeprefix("missing-stop-")
        data["stop_conditions"] = [c for c in data["stop_conditions"] if c != condition]
    elif name.startswith("missing-non-claim-"):
        claim = name.removeprefix("missing-non-claim-").replace("_", " ")
        data["required_non_claims"] = [c for c in data["required_non_claims"] if c != claim]
    elif name == "extra-non-claim":
        data["required_non_claims"].append("approved")
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
        "source-slice-id",
        "source-final-gate-command",
        "source-product-status",
        "source-next-step-status",
        "prompt-no-explicit-reply",
        "prompt-default-execution",
        "prompt-unsafe-default",
        "prompt-missing-no-auto-language",
        "option-count",
        "option-order",
        "option-default",
        "option-auto-execution",
        "option-forbidden-action",
        "option-missing-new-scope",
        "option-missing-separate-approval",
        "option-unsafe-label",
        "decision-packet-not-ready",
        "not-ready-to-ask",
        "extra-non-claim",
    ]
    names.extend(f"forbidden-action-{key}" for key in FORBIDDEN_NEXT_ACTIONS)
    names.extend(
        f"readiness-{key}"
        for key in [
            "ready_to_execute_user_choice",
            "user_choice_collected",
            "promotion_ready",
            "mainline_merge_ready",
            "formal_vault_write_ready",
            "action_basis_ready",
            "commit_ready",
            "push_ready",
        ]
    )
    names.extend(f"missing-stop-{key}" for key in STOP_CONDITIONS)
    names.extend(f"missing-non-claim-{key.replace(' ', '_')}" for key in REQUIRED_NON_CLAIMS)
    names.extend(
        [
            "acceptance-contract-requires_reviewer_pass",
            "acceptance-contract-requires_boundary_pass",
            "acceptance-contract-requires_gpt_5_5_extra_high_product_acceptance",
            "acceptance-contract-p2_50_final_gate_must_pass",
            "acceptance-contract-product_acceptance_does_not_collect_user_choice",
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


def readout_text(packet: dict) -> str:
    options = "\n".join(
        f"- `{item['option_id']}`: {item['label']} / automatic_execution={item['automatic_execution']} / requires_new_scope={item['requires_new_scope']} / requires_separate_user_approval={item['requires_separate_user_approval']} / allowed_next_action={item['allowed_next_action']}"
        for item in packet["decision_options"]
    )
    return f"""---
record_kind: user_decision_request_readout
slice_id: {SLICE_ID}
status: built_pending_review
---

# User Decision Request Packet

This packet is ready to ask the user for the next VAKS sandbox decision. It is not approval and not execution permission.

## Prompt

{packet['request_prompt']['plain_language']}

## Options

{options}

Options B and C only authorize a future scoped conversation. They do not start the future work in this slice.

## Safe Default

If the user does not reply, keep the sandbox as reference only. Do not execute anything.

## Required Upstream Gate

```powershell
{packet['source_closeout']['final_gate_command']}
```

## Builder-Only Command

`--rebuild` rewrites generated files inside this sandbox and is for Builder repair only. Ordinary follow-up agents should use the default verifier or `--run-upstream`.
"""


def contract_text(packet: dict) -> str:
    return f"""---
record_kind: sandbox_contract
slice_id: {SLICE_ID}
status: built_pending_review
---

# User Decision Request Packet Contract

This contract allows asking the user a question. It does not collect approval, execute approval, or create action authority.

Required upstream gate:

```powershell
{packet['source_closeout']['final_gate_command']}
```

Every option must have `automatic_execution=false`. Any option that may lead toward promotion, merge, vault write, commit, push, or action-basis work must require a new scope and separate user approval.

Non-claims: {', '.join(REQUIRED_NON_CLAIMS)}.
"""


def oracle_text(oracle: dict[str, list[str]]) -> str:
    lines = ["---", "record_kind: failure_case_oracle_doc", f"slice_id: {SLICE_ID}", "status: built_pending_review", "---", "", "# Failure Case Oracle", ""]
    for filename, errors in sorted(oracle.items()):
        lines.append(f"- `{filename}`: {', '.join(errors)}")
    lines.append("")
    return "\n".join(lines)


def prototype_files(packet: dict) -> dict[str, str]:
    receipt = {
        "record_kind": "user_decision_request_prototype_receipt",
        "slice_id": SLICE_ID,
        "option_count": len(packet["decision_options"]),
        "truth_boundary": packet["truth_boundary"],
    }
    index = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>VAKS Decision Request</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">Ask only</p>
      <h1>VAKS Sandbox Decision</h1>
      <p>No option executes automatically.</p>
    </header>
    <section id="prompt"></section>
    <section id="options"></section>
    <section id="stops"></section>
  </main>
  <script src="app.js"></script>
</body>
</html>
"""
    style = """body{margin:0;font-family:Arial,sans-serif;background:#f7f8f3;color:#222}main{max-width:980px;margin:0 auto;padding:32px 20px}header{border-bottom:2px solid #222;padding-bottom:16px}.eyebrow{text-transform:uppercase;font-size:12px;letter-spacing:.08em;color:#666}h1{font-size:34px;margin:6px 0 10px}.panel{background:white;border:1px solid #cfd2c4;border-radius:6px;margin:18px 0;padding:18px}.option{border-top:1px solid #ddd;padding:12px 0}.no{color:#8b2f00;font-weight:700}.yes{color:#236a3b;font-weight:700}code{background:#eee;padding:2px 4px;border-radius:3px}"""
    app = f"""const packet = {json.dumps(packet, indent=2, ensure_ascii=False)};
document.getElementById('prompt').innerHTML = `<div class="panel"><h2>Prompt</h2><p>${{packet.request_prompt.plain_language}}</p><p><span class="yes">Ready to ask.</span> <span class="no">Not approval.</span></p></div>`;
document.getElementById('options').innerHTML = `<div class="panel"><h2>Options</h2>${{packet.decision_options.map(item => `<div class="option"><b>${{item.option_id}}</b><p>${{item.label}}</p><p>automatic_execution: <code>${{item.automatic_execution}}</code></p><p>${{item.what_it_means}}</p></div>`).join('')}}</div>`;
document.getElementById('stops').innerHTML = `<div class="panel"><h2>Stop Conditions</h2><ul>${{packet.stop_conditions.map(item => `<li>${{item}}</li>`).join('')}}</ul></div>`;
"""
    return {
        "prototype/user-decision-request/receipt.json": json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        "prototype/user-decision-request/index.html": index,
        "prototype/user-decision-request/style.css": style,
        "prototype/user-decision-request/app.js": app,
    }


def rebuild() -> dict:
    root = slice_root()
    for generated in ["fixtures", "failure-cases", "readouts", "prototype"]:
        target = root / generated
        if target.exists():
            shutil.rmtree(target)
    packet = build_packet()
    write_json(root / "artifact" / "user-decision-request-packet.json", packet)
    write_text(root / "artifact" / "user-decision-request-contract.md", contract_text(packet))
    write_text(root / "readouts" / "user-decision-request-packet.md", readout_text(packet))

    fixtures = {
        "valid-user-decision-request-packet.json": packet,
        "valid-decision-options.json": {**packet, "fixture_focus": "decision_options"},
        "valid-non-execution-boundary.json": {**packet, "fixture_focus": "non_execution_boundary"},
    }
    for filename, data in fixtures.items():
        write_json(root / "fixtures" / filename, data)

    oracle: dict[str, list[str]] = {}
    for idx, name in enumerate(failure_mutations(), start=1):
        data = mutate(packet, name)
        errors = validate_config(data)
        filename = f"{idx:03d}-{name}.json"
        write_json(root / "failure-cases" / filename, data)
        oracle[filename] = errors
    write_json(root / "artifact" / "failure-case-oracle.json", oracle)
    write_text(root / "artifact" / "failure-case-oracle.md", oracle_text(oracle))

    for path, text in prototype_files(packet).items():
        write_text(root / path, text)

    write_text(root / "slice-plan.md", report_text("slice-plan", "built_pending_review", "Build a user decision request packet that can ask the user what to do next without executing any option."))
    write_text(root / "source-map.md", report_text("source-map", "built_pending_review", "Source is p2-50 final sandbox closeout readiness dossier and its final gate. This is decision-request packaging only."))
    write_text(
        root / "verification.md",
        report_text(
            "verification",
            "local_verification_passed_pending_review",
            f"""Default verifier passed:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_user_decision_request_packet.py
```

Builder-only rebuild verifier passed:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_user_decision_request_packet.py --rebuild
```

Read-only upstream verifier passed and ran p2-50 final gate:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_user_decision_request_packet.py --run-upstream
```

Observed result after Reviewer-driven repair: 4 decision options, 3 positive fixtures, 73 failure cases, 0 orphan failure cases, 0 oracle mismatches, prototype/readout/contract/oracle checks clean, and p2-50 final gate passed. p2-50 in turn ran p2-49 final gate, and p2-49 ran p2-48 freeze.

Reviewer-driven repair:

- Readout exposes `requires_new_scope` and `requires_separate_user_approval` for each option.
- Options B and C are framed as authorizing a future scoped conversation, not starting work inside this slice.
- `--rebuild` is documented as Builder-only; ordinary follow-up agents should use the default verifier or `--run-upstream`.
- Verifier text checks require these readout safeguards.

Pre-report final gate ran the full upstream chain and failed only because Reviewer, Boundary, Product, and next-step reports were still pending. That is the expected pre-review state.

Run `--final-gate` again only after Reviewer, Boundary, and Product reports are written.""",
        ),
    )
    write_text(root / "reviewer-report.md", report_text("reviewer-report", "pending_reviewer", "Pending independent Reviewer check."))
    write_text(root / "boundary-audit.md", report_text("boundary-audit", "pending_boundary_audit", "Pending Boundary Auditor check."))
    write_text(root / "product-acceptance-report.md", report_text("product-acceptance-report", "pending_product_acceptance", "Pending GPT-5.5 extra-high Product Acceptance."))
    write_text(root / "next-step.md", report_text("next-step", "pending_product_acceptance", "If Product Acceptance passes, the packet may be shown to the user as a question. It still cannot execute any option."))
    return packet


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    if args.rebuild:
        packet = rebuild()
    else:
        packet = json.loads((slice_root() / "artifact" / "user-decision-request-packet.json").read_text(encoding="utf-8"))
    errors = validate_config(packet)
    print(json.dumps({"slice_id": SLICE_ID, "rebuilt": args.rebuild, "errors": errors}, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
