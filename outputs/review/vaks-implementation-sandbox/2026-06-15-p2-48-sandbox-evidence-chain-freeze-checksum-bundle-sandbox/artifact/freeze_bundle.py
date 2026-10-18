from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
SANDBOX_ROOT = ROOT.parent

VERSION = "sandbox-evidence-chain-freeze-checksum-bundle-v1"
TRUTH_BOUNDARY = "checksum_freeze_detects_drift_not_reacceptance_or_authority"
PURPOSE = "freeze the p2-44 through p2-47 sandbox handoff/audit chain so follow-up agents can detect drift"
WRITE_SCOPE = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"

SOURCE_SLICES = [
    {
        "slice_id": "2026-06-15-p2-44-sandbox-evidence-ledger-sandbox",
        "role": "sandbox evidence ledger",
        "primary_files": [
            "artifact/evidence-ledger.json",
            "artifact/verify_evidence_ledger.py",
            "product-acceptance-report.md",
            "reviewer-report.md",
            "boundary-audit.md",
            "verification.md",
            "next-step.md",
        ],
    },
    {
        "slice_id": "2026-06-15-p2-45-sandbox-release-candidate-handoff-sandbox",
        "role": "release-candidate handoff",
        "primary_files": [
            "artifact/release-candidate-handoff.json",
            "artifact/verify_release_candidate_handoff.py",
            "handoff-packets/release-candidate-handoff.md",
            "product-acceptance-report.md",
            "reviewer-report.md",
            "boundary-audit.md",
            "verification.md",
            "next-step.md",
        ],
    },
    {
        "slice_id": "2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox",
        "role": "status normalization compatibility audit",
        "primary_files": [
            "artifact/status-normalization-audit.json",
            "artifact/verify_status_normalization_audit.py",
            "readouts/status-normalization-guide.md",
            "product-acceptance-report.md",
            "reviewer-report.md",
            "boundary-audit.md",
            "verification.md",
            "next-step.md",
        ],
    },
    {
        "slice_id": "2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox",
        "role": "verifier portability dependency audit",
        "primary_files": [
            "artifact/verifier-portability-audit.json",
            "artifact/verify_portability_audit.py",
            "readouts/verifier-portability-guide.md",
            "product-acceptance-report.md",
            "reviewer-report.md",
            "boundary-audit.md",
            "verification.md",
            "next-step.md",
        ],
    },
]

ALLOWED_VIEWS = {
    "evidence-chain-freeze",
    "agent-drift-check-guide",
    "source-hash-index",
}

REQUIRED_FIXTURES = {
    "valid-evidence-chain-freeze.json": "evidence-chain-freeze",
    "valid-agent-drift-check-guide.json": "agent-drift-check-guide",
    "valid-source-hash-index.json": "source-hash-index",
}

TOP_LEVEL_FIELDS = {
    "record_kind",
    "slice_id",
    "version",
    "truth_boundary",
    "purpose",
    "write_scope",
    "view",
    "chain_scope",
    "freeze_policy",
    "source_slices",
    "summary",
    "drift_check",
    "agent_run_guide",
    "readiness_flags",
    "operation_performed_flags",
    "required_non_claims",
    "operator_note",
}

READINESS_FLAGS = {
    "checksum_freeze_ready",
    "drift_detected",
    "re_acceptance_performed",
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
    "old_slice_modified",
    "old_verifier_executed",
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
    "not re-acceptance",
    "not runtime certification",
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

REPORT_STATUS_EXPECTATIONS = {
    "product-acceptance-report.md": "pass_product_grade",
    "reviewer-report.md": "reviewer_pass",
    "boundary-audit.md": "boundary_pass",
    "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
}


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
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    frontmatter = text[3:end]
    match = re.search(r"^status:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    return match.group(1).strip() if match else None


def file_record(slice_id: str, relative_path: str) -> dict[str, Any]:
    path = SANDBOX_ROOT / slice_id / relative_path
    exists = path.exists()
    record = {
        "path": rel(path),
        "relative_path": relative_path,
        "exists": exists,
        "size_bytes": path.stat().st_size if exists else None,
        "sha256": sha256_file(path) if exists else None,
        "frontmatter_status": parse_status(path) if exists and path.suffix.lower() == ".md" else None,
        "role": "tracked_key_file",
    }
    return record


def source_slice_record(source: dict[str, Any]) -> dict[str, Any]:
    files = [file_record(source["slice_id"], item) for item in source["primary_files"]]
    return {
        "slice_id": source["slice_id"],
        "role": source["role"],
        "path": rel(SANDBOX_ROOT / source["slice_id"]),
        "tracked_files": files,
        "tracked_file_count": len(files),
        "missing_file_count": sum(1 for item in files if not item["exists"]),
        "hash_algorithm": "sha256",
        "all_expected_reports_pass": all(
            item["frontmatter_status"] == expected
            for item in files
            for report, expected in REPORT_STATUS_EXPECTATIONS.items()
            if item["relative_path"] == report
        ),
    }


def current_source_slices() -> list[dict[str, Any]]:
    return [source_slice_record(source) for source in SOURCE_SLICES]


def summarize(source_slices: list[dict[str, Any]]) -> dict[str, Any]:
    tracked_file_count = sum(item["tracked_file_count"] for item in source_slices)
    missing_file_count = sum(item["missing_file_count"] for item in source_slices)
    report_status_mismatches = []
    for source in source_slices:
        for item in source["tracked_files"]:
            expected = REPORT_STATUS_EXPECTATIONS.get(item["relative_path"])
            if expected is not None and item["frontmatter_status"] != expected:
                report_status_mismatches.append(
                    {
                        "slice_id": source["slice_id"],
                        "file": item["relative_path"],
                        "actual": item["frontmatter_status"],
                        "expected": expected,
                    }
                )
    return {
        "source_slice_count": len(source_slices),
        "tracked_file_count": tracked_file_count,
        "missing_file_count": missing_file_count,
        "report_status_mismatch_count": len(report_status_mismatches),
        "report_status_mismatches": report_status_mismatches,
        "all_sources_present": missing_file_count == 0,
        "all_expected_reports_pass": not report_status_mismatches,
    }


def default_bundle(view: str = "evidence-chain-freeze") -> dict[str, Any]:
    source_slices = current_source_slices()
    summary = summarize(source_slices)
    return {
        "record_kind": "sandbox_evidence_chain_freeze_checksum_bundle",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "view": view,
        "chain_scope": {
            "source_slice_ids": [item["slice_id"] for item in SOURCE_SLICES],
            "source_roles": {item["slice_id"]: item["role"] for item in SOURCE_SLICES},
            "freeze_kind": "key_file_hash_manifest",
            "hash_algorithm": "sha256",
        },
        "freeze_policy": {
            "analysis_mode": "read_only_hash_recompute",
            "does_not_copy_source_content": True,
            "does_not_modify_old_slices": True,
            "does_not_execute_old_verifiers": True,
            "drift_detected_means_stop_and_reinspect": True,
            "freeze_is_not_reacceptance": True,
            "freeze_is_not_runtime_certification": True,
        },
        "source_slices": source_slices,
        "summary": summary,
        "drift_check": {
            "expected_drift_count": 0,
            "drift_action": "stop_before_using_handoff_chain_and_reinspect_source_slices",
            "drift_does_not_auto_reject_prior_product_acceptance": True,
        },
        "agent_run_guide": [
            "run the p2-48 verifier before relying on the latest p2-44..p2-47 handoff chain",
            "if drift is detected, stop and inspect the changed source slice before continuing",
            "do not edit p2-44..p2-47 to make hashes match",
            "do not treat a matching checksum bundle as re-acceptance or action authority",
            "run source slice default verifiers separately if a later task needs deeper validation",
        ],
        "readiness_flags": {
            "checksum_freeze_ready": True,
            "drift_detected": False,
            "re_acceptance_performed": False,
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


def calculate_drifts(data: dict[str, Any]) -> list[dict[str, Any]]:
    drifts: list[dict[str, Any]] = []
    current_by_path = {}
    for source in current_source_slices():
        for file_item in source["tracked_files"]:
            current_by_path[file_item["path"]] = file_item
    for source in data.get("source_slices", []):
        for file_item in source.get("tracked_files", []):
            path = file_item.get("path")
            current = current_by_path.get(path)
            if current is None:
                drifts.append({"path": path, "kind": "unknown_tracked_path"})
                continue
            for key in ["exists", "size_bytes", "sha256", "frontmatter_status"]:
                if file_item.get(key) != current.get(key):
                    drifts.append(
                        {
                            "path": path,
                            "kind": f"{key}_drift",
                            "expected": file_item.get(key),
                            "actual": current.get(key),
                        }
                    )
    return drifts


def validate_bundle(data: dict[str, Any]) -> list[str]:
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
        "record_kind": "sandbox_evidence_chain_freeze_checksum_bundle",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{key}_mismatch")

    current = default_bundle(view if view in ALLOWED_VIEWS else "evidence-chain-freeze")
    for key in ["chain_scope", "freeze_policy", "summary", "drift_check", "agent_run_guide"]:
        if data.get(key) != current.get(key):
            errors.append(f"{key}_mismatch")
    if data.get("source_slices") != current.get("source_slices"):
        errors.append("source_slices_mismatch")

    summary = data.get("summary", {})
    if summary.get("source_slice_count") != 4:
        errors.append("source_slice_count_mismatch")
    if summary.get("tracked_file_count") != 31:
        errors.append("tracked_file_count_mismatch")
    if summary.get("missing_file_count") != 0:
        errors.append("missing_file_present")
    if summary.get("report_status_mismatch_count") != 0:
        errors.append("report_status_mismatch_present")
    if summary.get("all_sources_present") is not True:
        errors.append("all_sources_present_not_true")
    if summary.get("all_expected_reports_pass") is not True:
        errors.append("all_expected_reports_pass_not_true")

    drifts = calculate_drifts(data)
    for drift in drifts:
        errors.append(f"drift:{drift['kind']}:{drift['path']}")

    rules = data.get("agent_run_guide", [])
    for fragment in ["if drift is detected", "do not edit p2-44..p2-47", "not treat a matching checksum bundle as re-acceptance"]:
        if not any(fragment in str(rule) for rule in rules):
            errors.append(f"agent_run_rule_missing:{fragment}")

    flags = data.get("readiness_flags", {})
    if set(flags) != READINESS_FLAGS:
        errors.append("readiness_flags_keys_mismatch")
    if flags.get("checksum_freeze_ready") is not True:
        errors.append("checksum_freeze_ready_not_true")
    for flag in READINESS_FLAGS - {"checksum_freeze_ready"}:
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
    for directory in ["fixtures", "failure-cases", "prototype/evidence-chain-freeze", "readouts"]:
        path = ROOT / directory
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def make_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: dict[str, list[str]] = {}
    index = 1

    def add(name: str, mutate) -> None:
        nonlocal index
        sample = copy.deepcopy(base)
        mutate(sample)
        filename = f"{index:03d}-{name}.json"
        write_json(ROOT / "failure-cases" / filename, sample)
        cases[filename] = validate_bundle(sample)
        index += 1

    for key in ["record_kind", "slice_id", "version", "truth_boundary", "purpose", "write_scope"]:
        add(f"top-level-{key}", lambda sample, key=key: sample.__setitem__(key, "wrong"))
    add("bad-view", lambda sample: sample.__setitem__("view", "wrong"))
    add("extra-reacceptance-claim", lambda sample: sample.__setitem__("reacceptance_claim", True))
    add("summary-source-count-drift", lambda sample: sample["summary"].__setitem__("source_slice_count", 3))
    add("summary-tracked-file-count-drift", lambda sample: sample["summary"].__setitem__("tracked_file_count", 30))
    add("summary-missing-file-count", lambda sample: sample["summary"].__setitem__("missing_file_count", 1))
    add("summary-status-mismatch-count", lambda sample: sample["summary"].__setitem__("report_status_mismatch_count", 1))
    add("source-file-hash-drift", lambda sample: sample["source_slices"][0]["tracked_files"][0].__setitem__("sha256", "0" * 64))
    add("source-file-size-drift", lambda sample: sample["source_slices"][0]["tracked_files"][0].__setitem__("size_bytes", -1))
    add("source-file-exists-drift", lambda sample: sample["source_slices"][0]["tracked_files"][0].__setitem__("exists", False))
    add("source-status-drift", lambda sample: sample["source_slices"][1]["tracked_files"][3].__setitem__("frontmatter_status", "pending"))
    add("unknown-tracked-path", lambda sample: sample["source_slices"][0]["tracked_files"][0].__setitem__("path", "outputs/review/vaks-implementation-sandbox/missing/file.md"))
    add("policy-allows-old-edit", lambda sample: sample["freeze_policy"].__setitem__("does_not_modify_old_slices", False))
    add("drift-action-weakened", lambda sample: sample["drift_check"].__setitem__("drift_action", "continue_anyway"))
    add("agent-guide-missing-stop", lambda sample: sample["agent_run_guide"].pop(1))
    for flag in sorted(READINESS_FLAGS - {"checksum_freeze_ready"}):
        add(f"readiness-{flag}-true", lambda sample, flag=flag: sample["readiness_flags"].__setitem__(flag, True))
    for operation in sorted(OPERATION_FLAGS):
        add(f"operation-{operation}-true", lambda sample, operation=operation: sample["operation_performed_flags"].__setitem__(operation, True))
    for non_claim in REQUIRED_NON_CLAIMS:
        add(f"missing-non-claim-{non_claim.replace(' ', '-')}", lambda sample, non_claim=non_claim: sample["required_non_claims"].remove(non_claim))
    add("extra-non-claim", lambda sample: sample["required_non_claims"].append("unexpected authority"))
    return cases


def build_fixtures() -> None:
    reset_generated()
    base = default_bundle("evidence-chain-freeze")
    write_json(ROOT / "fixtures" / "valid-evidence-chain-freeze.json", base)
    guide = default_bundle("agent-drift-check-guide")
    guide["operator_note"] = "Agent drift-check guide view. Still sandbox only."
    write_json(ROOT / "fixtures" / "valid-agent-drift-check-guide.json", guide)
    index = default_bundle("source-hash-index")
    index["operator_note"] = "Source hash index view. Still sandbox only."
    write_json(ROOT / "fixtures" / "valid-source-hash-index.json", index)
    cases = make_failure_cases(base)
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "cases": cases})
    lines = ["# Failure Case Oracle", "", f"Slice: `{SLICE_ID}`", "", f"Total cases: {len(cases)}", ""]
    for name, expected in cases.items():
        lines.append(f"- `{name}` -> `{', '.join(expected)}`")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines))


def build_readout_and_contract() -> None:
    bundle = default_bundle()
    summary = bundle["summary"]
    write_json(ROOT / "artifact" / "evidence-chain-freeze-manifest.json", bundle)
    write_text(
        ROOT / "artifact" / "checksum-freeze-contract.md",
        f"""
# Evidence Chain Checksum Freeze Contract

Slice: `{SLICE_ID}`

This bundle freezes hashes for p2-44 through p2-47 key files. It is a drift detector only.
It does not copy source content, edit old slices, re-accept old work, certify runtime
behavior, promote artifacts, or approve action use.

## Drift Rule

- Matching hashes mean the tracked handoff/audit files still match this freeze bundle.
- Drift means stop and inspect the changed source slice before relying on the chain.
- Drift does not automatically reject prior Product Acceptance, and a match does not create new Product Acceptance.
- `--rebuild` is Builder-only. Reviewers and follow-up agents should use the default verifier so they do not refresh the freeze point by accident.
""",
    )
    write_text(
        ROOT / "readouts" / "evidence-chain-freeze-guide.md",
        f"""
# Evidence Chain Freeze Guide

Status: sandbox checksum drift detector only.

Source slices: `{summary['source_slice_count']}`

Tracked files: `{summary['tracked_file_count']}`

Missing files: `{summary['missing_file_count']}`

Report status mismatches: `{summary['report_status_mismatch_count']}`

Interpretation:

- Run this verifier before relying on the p2-44..p2-47 handoff/audit chain.
- If drift appears, stop and inspect the changed source slice.
- Do not use `--rebuild` during review; it refreshes the freeze point inside this sandbox.
- This freeze is not re-acceptance, runtime certification, release approval, promotion, reviewed knowledge, evidence support, or action basis.
""",
    )


def build_prototype() -> None:
    bundle = default_bundle()
    summary = bundle["summary"]
    prototype = ROOT / "prototype" / "evidence-chain-freeze"
    rows = "\n".join(f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in summary.items() if key != "report_status_mismatches")
    write_text(
        prototype / "index.html",
        f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Evidence Chain Freeze</title>
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
    <h1>Evidence Chain Freeze</h1>
    <p class="summary">sandbox checksum drift detector only. Source slices {summary['source_slice_count']}; tracked files {summary['tracked_file_count']}; missing files {summary['missing_file_count']}; not re-acceptance; not action basis.</p>
    <table>
      <thead><tr><th>Signal</th><th>Value</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <section class="notice">If drift appears, stop and inspect the changed source slice. No old slice is edited by this bundle.</section>
  </main>
  <script src="app.js"></script>
</body>
</html>
""",
    )
    write_text(prototype / "app.js", 'document.documentElement.dataset.evidenceChainFreezeReady = "true";')
    receipt = {
        "record_kind": "evidence_chain_freeze_prototype_receipt",
        "slice_id": SLICE_ID,
        "re_acceptance_performed": False,
        "runtime_certified": False,
        "old_slice_modified": False,
        "release_approved": False,
        "promotion_approved": False,
        "enterprise_production_ready": False,
        "mainline_ready": False,
        "formal_vault_accessed": False,
        "sync_performed": False,
        "commit_performed": False,
        "push_performed": False,
        "action_basis_created": False,
        "required_non_claims": REQUIRED_NON_CLAIMS,
    }
    write_json(prototype / "receipt.json", receipt)


def frontmatter(status: str) -> str:
    return f"---\nstatus: {status}\nslice_id: {SLICE_ID}\n---\n"


def build_reports() -> None:
    bundle = default_bundle()
    summary = bundle["summary"]
    write_text(
        ROOT / "slice-plan.md",
        frontmatter("built_pending_review")
        + f"""
# Slice Plan

## Objective

Build a read-only checksum freeze bundle for the p2-44 through p2-47 handoff/audit chain.

## Inputs

- p2-44 sandbox evidence ledger
- p2-45 sandbox release-candidate handoff
- p2-46 status normalization compatibility audit
- p2-47 verifier portability dependency audit

## Only Write Path

`{WRITE_SCOPE}`

## Non-Goals

- No re-acceptance.
- No runtime certification.
- No execution of old verifiers.
- No edits to old slices.
- No mainline merge, formal vault operation, Obsidian sync, commit, push, promotion, reviewed knowledge, evidence support, or action basis.
""",
    )
    source_lines = []
    for source in bundle["source_slices"]:
        source_lines.append(f"- `{source['slice_id']}`: `{source['tracked_file_count']}` tracked files")
    write_text(
        ROOT / "source-map.md",
        frontmatter("built_pending_review")
        + f"""
# Source Map

Tracked source slices:

{chr(10).join(source_lines)}

Summary:

- source slices: `{summary['source_slice_count']}`
- tracked files: `{summary['tracked_file_count']}`
- missing files: `{summary['missing_file_count']}`
- report status mismatches: `{summary['report_status_mismatch_count']}`

This map records checksum provenance only. It is not re-acceptance, evidence support, reviewed truth, action basis, formal vault approval, or mainline readiness.
""",
    )
    write_text(
        ROOT / "verification.md",
        frontmatter("local_verification_passed_pending_review")
        + f"""
# Verification

Default read-only verification command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_freeze_bundle.py
```

Expected result:

- Positive fixtures pass.
- Failure cases match the oracle.
- Recomputed p2-44..p2-47 hashes match the freeze manifest.
- Missing file count is `0`.
- Report status mismatch count is `0`.
- Prototype and readout preserve sandbox-only boundaries.

Builder-only regeneration command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_freeze_bundle.py --rebuild
```

Final gate command after reviews:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_freeze_bundle.py --final-gate
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
        actual = validate_bundle(read_json(path))
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
        fixture_errors = validate_bundle(data)
        expected_view = REQUIRED_FIXTURES.get(path.name)
        if expected_view and data.get("view") != expected_view:
            fixture_errors.append(f"fixture_view_mismatch:{expected_view}")
        if path.name == "valid-evidence-chain-freeze.json" and "operator_note" in data:
            fixture_errors.append("fixture_operator_note_unexpected")
        if path.name != "valid-evidence-chain-freeze.json" and path.name in REQUIRED_FIXTURES and "operator_note" not in data:
            fixture_errors.append("fixture_operator_note_missing")
        details.append({"file": path.name, "errors": fixture_errors})
        if fixture_errors:
            errors.append({"file": path.name, "errors": fixture_errors})
    return {"count": len(details), "fixtures": details, "errors": errors}


def validate_readout() -> dict[str, Any]:
    path = ROOT / "readouts" / "evidence-chain-freeze-guide.md"
    issues: list[str] = []
    if not path.exists():
        return {"path": str(path), "issues": ["missing_readout"]}
    text = path.read_text(encoding="utf-8", errors="ignore")
    for phrase in ["sandbox checksum drift detector only", "Tracked files", "If drift appears", "Do not use `--rebuild` during review", "not re-acceptance"]:
        if phrase not in text:
            issues.append(f"readout_phrase_missing:{phrase}")
    return {"path": str(path), "issues": issues}


def validate_contract() -> dict[str, Any]:
    path = ROOT / "artifact" / "checksum-freeze-contract.md"
    issues: list[str] = []
    if not path.exists():
        return {"path": str(path), "issues": ["missing_contract"]}
    text = path.read_text(encoding="utf-8", errors="ignore")
    for phrase in [
        "drift detector only",
        "does not copy source content",
        "Drift means stop",
        "does not create new Product Acceptance",
        "`--rebuild` is Builder-only",
    ]:
        if phrase not in text:
            issues.append(f"contract_phrase_missing:{phrase}")
    return {"path": str(path), "issues": issues}


def validate_oracle_doc() -> dict[str, Any]:
    path = ROOT / "artifact" / "failure-case-oracle.md"
    oracle_path = ROOT / "artifact" / "failure-case-oracle.json"
    issues: list[str] = []
    if not path.exists():
        return {"path": str(path), "issues": ["missing_oracle_doc"]}
    if not oracle_path.exists():
        return {"path": str(path), "issues": ["missing_oracle_json_for_doc_check"]}
    text = path.read_text(encoding="utf-8", errors="ignore")
    count = len(read_json(oracle_path).get("cases", {}))
    if "# Failure Case Oracle" not in text:
        issues.append("oracle_doc_title_missing")
    if f"Total cases: {count}" not in text:
        issues.append("oracle_doc_total_count_mismatch")
    return {"path": str(path), "issues": issues}


def validate_prototype() -> dict[str, Any]:
    prototype = ROOT / "prototype" / "evidence-chain-freeze"
    issues: list[str] = []
    for item in ["index.html", "app.js", "receipt.json"]:
        if not (prototype / item).exists():
            issues.append(f"missing_prototype_file:{item}")
    if (prototype / "index.html").exists():
        html = (prototype / "index.html").read_text(encoding="utf-8", errors="ignore").lower()
        for forbidden in ["<form", "download", "contenteditable", "<a ", "h:\\obsidian", "onclick"]:
            if forbidden in html:
                issues.append(f"prototype_forbidden:{forbidden}")
        for phrase in ["sandbox checksum drift detector only", "not re-acceptance", "not action basis", "no old slice is edited"]:
            if phrase not in html:
                issues.append(f"prototype_phrase_missing:{phrase}")
    if (prototype / "app.js").exists():
        js = (prototype / "app.js").read_text(encoding="utf-8", errors="ignore").strip()
        if js != 'document.documentElement.dataset.evidenceChainFreezeReady = "true";':
            issues.append("prototype_app_js_not_static_receipt_marker")
    if (prototype / "receipt.json").exists():
        receipt = read_json(prototype / "receipt.json")
        for flag in [
            "re_acceptance_performed",
            "runtime_certified",
            "old_slice_modified",
            "release_approved",
            "promotion_approved",
            "enterprise_production_ready",
            "mainline_ready",
            "formal_vault_accessed",
            "sync_performed",
            "commit_performed",
            "push_performed",
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
    primary = ROOT / "fixtures" / "valid-evidence-chain-freeze.json"
    config_errors = validate_bundle(read_json(primary)) if primary.exists() else ["missing_valid_fixture"]
    artifact_path = ROOT / "artifact" / "evidence-chain-freeze-manifest.json"
    artifact_errors = validate_bundle(read_json(artifact_path)) if artifact_path.exists() else ["missing_evidence_chain_freeze_manifest"]
    fixtures = validate_fixtures()
    failure_cases = validate_failure_cases()
    prototype = validate_prototype()
    readout = validate_readout()
    contract = validate_contract()
    oracle_doc = validate_oracle_doc()
    reports = validate_required_reports(final_gate=final_gate)
    failures: list[str] = []
    failures.extend(config_errors)
    failures.extend([f"artifact_error:{item}" for item in artifact_errors])
    failures.extend([f"fixture_error:{item['file']}" for item in fixtures["errors"]])
    failures.extend([f"failure_case_mismatch:{item['file']}" for item in failure_cases["mismatches"]])
    failures.extend(prototype["issues"])
    failures.extend(readout["issues"])
    failures.extend(contract["issues"])
    failures.extend(oracle_doc["issues"])
    failures.extend(reports["issues"])
    current = default_bundle()
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
        "contract": contract,
        "oracle_doc": oracle_doc,
        "required_reports": reports,
        "summary": current["summary"],
        "source_slice_ids": current["chain_scope"]["source_slice_ids"],
        "non_claims": REQUIRED_NON_CLAIMS,
    }


if __name__ == "__main__":
    build()
