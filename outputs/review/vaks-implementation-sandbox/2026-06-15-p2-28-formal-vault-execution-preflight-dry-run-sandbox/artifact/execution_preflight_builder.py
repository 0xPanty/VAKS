from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-15-p2-28-formal-vault-execution-preflight-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox"
PACKET_SLICE_ID = "2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox"


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


def repo_relative(path: Path) -> str:
    return path.relative_to(workspace_root()).as_posix()


def safe_write(rel_path: str, content: str, *, overwrite: bool = True) -> None:
    base = root().resolve()
    target = (base / rel_path).resolve()
    if base != target and base not in target.parents:
        raise ValueError(f"Refusing to write outside slice root: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not overwrite:
        return
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def clear_json_files(rel_dir: str) -> None:
    base = root().resolve()
    target_dir = (base / rel_dir).resolve()
    if base != target_dir and base not in target_dir.parents:
        raise ValueError(f"Refusing to clear outside slice root: {target_dir}")
    if not target_dir.exists():
        return
    for path in target_dir.glob("*.json"):
        path.unlink()


def source_paths() -> dict[str, Path]:
    src = sandbox_root() / SOURCE_SLICE_ID
    packet = sandbox_root() / PACKET_SLICE_ID
    proto = src / "prototype" / "formal-vault-user-decision-intake-gate"
    return {
        "source_next_step": src / "next-step.md",
        "source_product_acceptance": src / "product-acceptance-report.md",
        "source_verification": src / "verification.md",
        "source_reviewer_report": src / "reviewer-report.md",
        "source_boundary_audit": src / "boundary-audit.md",
        "source_map": src / "source-map.md",
        "source_intake_config": src / "fixtures" / "valid-user-decision-intake-gate-config.json",
        "source_intake_contract": src / "artifact" / "formal-vault-user-decision-intake-gate-contract.md",
        "source_intake_receipt": proto / "Receipts" / "formal-vault-user-decision-intake-gate-receipt.json",
        "source_future_contract_page": proto / "01 Future Decision Contract.md",
        "source_capture_fields_page": proto / "02 Required Capture Fields.md",
        "source_approval_checklist_page": proto / "03 Future Approval Checklist.md",
        "source_stop_conditions_page": proto / "06 Stop Conditions.md",
        "source_packet_config": packet / "fixtures" / "valid-approval-packet-config.json",
    }


def source_input(key: str, path: Path) -> dict:
    return {
        "id": key,
        "source_path": repo_relative(path),
        "source_sha256": sha256(path) if path.exists() else "missing",
        "content_binding": "exact_source_sha256",
    }


def forbidden_operations() -> list[str]:
    return [
        "formal_vault_read",
        "formal_vault_scan",
        "formal_vault_write",
        "formal_vault_hash",
        "formal_vault_snapshot",
        "formal_vault_state_check",
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
        "real_user_text_storage",
        "real_user_text_capture",
        "write_gate_opening",
        "execution_performed",
        "snapshot_taken",
        "rollback_executed",
        "hash_before_collected",
        "hash_after_collected",
        "action_basis_creation",
        "reviewed_knowledge_creation",
        "external_notification",
    ]


def scope_ids(packet: dict) -> list[str]:
    return [item["id"] for item in packet["approval_scope"]["items"]]


def target_manifest(packet: dict) -> list[dict]:
    targets = []
    for item in packet["approval_scope"]["items"]:
        targets.append(
            {
                "id": item["id"],
                "relative_target": item["relative_target"],
                "source_path": item["p2_24_source_path"],
                "source_sha256": item["p2_24_source_sha256"],
                "content_binding": "exact_source_sha256",
                "target_path_relative_only": True,
                "formal_vault_target_resolved": False,
                "formal_vault_target_exists_checked": False,
                "snapshot_taken": False,
                "hash_before_collected": False,
                "hash_after_collected": False,
                "write_enabled_now": False,
                "dry_run_only": True,
            }
        )
    return targets


def preflight_contract(intake: dict, packet: dict) -> dict:
    return {
        "contract_kind": "formal_vault_execution_preflight_dry_run",
        "current_slice_executes": False,
        "current_slice_collects_approval": False,
        "formal_vault_access_disallowed": True,
        "formal_vault_state_inspection_disallowed": True,
        "real_user_text_storage_disallowed": True,
        "separate_future_execution_slice_required": True,
        "separate_final_user_confirmation_required": True,
        "approved_reference_not_executable_here": True,
        "deny_blocks_execution": True,
        "revise_blocks_execution": True,
        "dirty_state_blocks_execution": True,
        "extra_targets_block_execution": True,
        "sync_commit_push_promotion_blocked": True,
        "snapshot_plan_required_not_executed": True,
        "rollback_plan_required_not_executed": True,
        "hash_plan_required_not_executed": True,
        "default_result": "BLOCKED_NOT_EXECUTED",
        "required_source_intake_gate_hash": intake["intake_gate_hash"],
        "required_packet_hash": packet["packet_hash"],
        "required_source_bundle_hash": packet["source_bundle_hash"],
        "required_scope_hash": packet["approval_scope"]["scope_hash"],
        "required_scope_ids": scope_ids(packet),
        "required_exclusions": ["obsidian_sync", "commit", "push", "promotion"],
        "required_preflight_checks": [
            "source_product_passed",
            "intake_gate_hash_match",
            "packet_hash_match",
            "source_bundle_hash_match",
            "scope_hash_match",
            "target_scope_exact",
            "targets_relative_only",
            "no_extra_targets",
            "formal_vault_not_accessed",
            "formal_vault_state_not_inspected",
            "snapshot_plan_present_not_executed",
            "rollback_plan_present_not_executed",
            "hash_plan_present_not_executed",
            "no_sync_commit_push_promotion",
            "real_user_text_not_stored",
            "separate_execution_slice_required",
        ],
    }


def common_hashes(intake: dict, packet: dict) -> dict:
    return {
        "intake_gate_hash": intake["intake_gate_hash"],
        "packet_hash": packet["packet_hash"],
        "source_bundle_hash": packet["source_bundle_hash"],
        "scope_hash": packet["approval_scope"]["scope_hash"],
    }


def base_checks() -> dict:
    return {
        "source_product_passed": True,
        "intake_gate_hash_match": True,
        "packet_hash_match": True,
        "source_bundle_hash_match": True,
        "scope_hash_match": True,
        "target_scope_exact": True,
        "targets_relative_only": True,
        "no_extra_targets": True,
        "formal_vault_not_accessed": True,
        "formal_vault_state_not_inspected": True,
        "snapshot_plan_present_not_executed": True,
        "rollback_plan_present_not_executed": True,
        "hash_plan_present_not_executed": True,
        "no_sync_commit_push_promotion": True,
        "real_user_text_not_stored": True,
        "separate_execution_slice_required": True,
    }


def common_sample(intake: dict, packet: dict) -> dict:
    return {
        "synthetic_only": True,
        "actual_user_input": False,
        "approval_collected_now": False,
        "real_user_text_stored": False,
        "captured_user_text": "",
        "formal_vault_accessed": False,
        "formal_vault_state_inspected": False,
        "snapshot_taken": False,
        "rollback_executed": False,
        "hash_before_collected": False,
        "hash_after_collected": False,
        "execution_performed": False,
        "formal_vault_write_allowed_now": False,
        "action_basis_created": False,
        "reviewed_knowledge_created": False,
        "sync_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "promotion_allowed": False,
        "extra_targets_requested": False,
        "scope_ids": scope_ids(packet),
        "hash_claims": common_hashes(intake, packet),
        "explicit_exclusions_ack": ["obsidian_sync", "commit", "push", "promotion"],
        "preflight_checks": base_checks(),
    }


def preflight_samples(intake: dict, packet: dict) -> list[dict]:
    common = common_sample(intake, packet)
    return [
        {
            "id": "synthetic_approved_reference_preflight",
            "decision_verdict": "APPROVED_BY_USER",
            "decision_reference_kind": "synthetic_future_approval_reference",
            "decision_reference_present": True,
            "rollback_plan_present": True,
            "hash_plan_present": True,
            "snapshot_plan_present": True,
            "dirty_state_ack": True,
            "expected_preflight_result": "PREFLIGHT_DRY_RUN_COMPLETE_NOT_EXECUTABLE",
            "next_gate": "future_separately_approved_execution_slice_required",
            **common,
        },
        {
            "id": "synthetic_denied_reference_preflight",
            "decision_verdict": "DENIED_BY_USER",
            "decision_reference_kind": "synthetic_future_denial_reference",
            "decision_reference_present": True,
            "rollback_plan_present": False,
            "hash_plan_present": False,
            "snapshot_plan_present": False,
            "dirty_state_ack": False,
            "expected_preflight_result": "BLOCKED_BY_DENIAL_NOT_EXECUTED",
            "next_gate": "stop_and_record_denial_only",
            **common,
        },
        {
            "id": "synthetic_revision_reference_preflight",
            "decision_verdict": "NEEDS_REVISION",
            "decision_reference_kind": "synthetic_future_revision_reference",
            "decision_reference_present": True,
            "rollback_plan_present": False,
            "hash_plan_present": False,
            "snapshot_plan_present": False,
            "dirty_state_ack": False,
            "expected_preflight_result": "BLOCKED_PENDING_PACKET_REVISION_NOT_EXECUTED",
            "next_gate": "revise_packet_in_future_sandbox_only",
            **common,
        },
        {
            "id": "synthetic_dirty_state_preflight_block",
            "decision_verdict": "APPROVED_BY_USER",
            "decision_reference_kind": "synthetic_future_approval_reference",
            "decision_reference_present": True,
            "rollback_plan_present": True,
            "hash_plan_present": True,
            "snapshot_plan_present": True,
            "dirty_state_ack": False,
            "expected_preflight_result": "BLOCKED_BY_DIRTY_STATE_ACK_MISSING_NOT_EXECUTED",
            "next_gate": "stop_until_future_dirty_state_ack",
            **common,
        },
    ]


def material(cfg: dict) -> dict:
    contract = dict(cfg.get("preflight_contract", {}))
    contract.pop("required_preflight_hash", None)
    samples = []
    for sample in cfg.get("preflight_samples", []):
        item = dict(sample)
        item.pop("required_preflight_hash", None)
        hashes = dict(item.get("hash_claims", {}))
        hashes.pop("preflight_hash", None)
        item["hash_claims"] = hashes
        samples.append(item)
    receipt = dict(cfg.get("non_execution_receipt", {}))
    receipt.pop("preflight_hash", None)
    return {
        "preflight_version": cfg.get("preflight_version"),
        "source_slice": cfg.get("source_slice"),
        "source_input_bundle_hash": cfg.get("source_input_bundle_hash"),
        "source_intake_gate_hash": cfg.get("source_intake_gate_hash"),
        "source_packet_hash": cfg.get("source_packet_hash"),
        "source_packet_source_bundle_hash": cfg.get("source_packet_source_bundle_hash"),
        "source_packet_scope_hash": cfg.get("source_packet_scope_hash"),
        "target_manifest_hash": cfg.get("target_manifest_hash"),
        "preflight_contract": contract,
        "preflight_samples": samples,
        "non_execution_receipt": receipt,
        "stop_conditions": cfg.get("stop_conditions", []),
    }


def attach_preflight_hash(cfg: dict) -> dict:
    cfg["preflight_hash_material"] = material(cfg)
    cfg["preflight_hash"] = sha256_json(cfg["preflight_hash_material"])
    cfg["preflight_contract"]["required_preflight_hash"] = cfg["preflight_hash"]
    for sample in cfg["preflight_samples"]:
        sample["required_preflight_hash"] = cfg["preflight_hash"]
        sample["hash_claims"]["preflight_hash"] = cfg["preflight_hash"]
    cfg["non_execution_receipt"]["preflight_hash"] = cfg["preflight_hash"]
    return cfg


def config() -> dict:
    paths = source_paths()
    inputs = [source_input(key, path) for key, path in paths.items()]
    intake = load_json(paths["source_intake_config"])
    packet = load_json(paths["source_packet_config"])
    targets = target_manifest(packet)
    cfg = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "packet_slice": PACKET_SLICE_ID,
        "preflight_version": "p2-28-execution-preflight-dry-run-v1",
        "purpose": "Define the dry-run preflight checklist for a future formal-vault execution path without collecting approval, inspecting the formal vault, or executing any operation.",
        "formal_vault_path_label": "formal Obsidian vault path is a label only; it is not accessed in this slice",
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": [item["source_path"] for item in inputs],
        "operations": {op: False for op in forbidden_operations()}
        | {"default_read_only": True, "rebuild_requires_explicit_flag": True},
        "boundary_phrases": [
            "sandbox only",
            "execution preflight dry-run only",
            "not actual approval",
            "approval not collected",
            "real user text not stored",
            "formal vault not accessed",
            "formal vault state not inspected",
            "execution not performed",
            "snapshot not taken",
            "hashes not collected from formal vault",
            "dry-run only",
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "does not approve",
            "does not execute",
            "no formal vault write",
            "no formal vault read",
            "no sync",
            "no commit",
            "no push",
            "no promotion",
            "requires separate user approval",
            "requires separate execution slice",
        ],
        "source_inputs": inputs,
        "source_input_bundle_hash": sha256_json(inputs),
        "source_intake_gate_hash": intake["intake_gate_hash"],
        "source_packet_hash": packet["packet_hash"],
        "source_packet_source_bundle_hash": packet["source_bundle_hash"],
        "source_packet_scope_hash": packet["approval_scope"]["scope_hash"],
        "target_manifest": targets,
        "target_manifest_hash": sha256_json(targets),
        "preflight_contract": preflight_contract(intake, packet),
        "preflight_samples": preflight_samples(intake, packet),
        "non_execution_receipt": {
            "approval_collected_now": False,
            "actual_user_input_used": False,
            "real_user_text_stored": False,
            "formal_vault_accessed": False,
            "formal_vault_state_inspected": False,
            "execution_performed": False,
            "snapshot_taken": False,
            "hash_before_collected": False,
            "hash_after_collected": False,
            "current_status": "execution_preflight_dry_run_defined_pending_review",
            "non_claims": [
                "not actual approval",
                "not a user decision record",
                "not formal vault approval",
                "not execution readiness",
                "not sync approval",
                "not commit approval",
                "not push approval",
                "not promotion approval",
                "not action basis",
                "not reviewed knowledge",
                "not evidence support",
            ],
        },
        "stop_conditions": [
            "actual user approval collection requested",
            "actual user decision collection requested",
            "real user text storage requested",
            "formal vault read requested",
            "formal vault scan requested",
            "formal vault write requested",
            "formal vault state inspection requested",
            "formal vault hash or snapshot requested",
            "absolute vault path requested",
            "Obsidian sync requested",
            "commit or push requested",
            "promotion requested",
            "execution requested",
            "decision inferred from silence or prior PASS",
            "intake gate hash mismatch",
            "packet hash mismatch",
            "source bundle hash mismatch",
            "scope hash mismatch",
            "preflight hash mismatch",
            "target manifest mismatch",
            "extra targets requested",
            "target path is absolute or parent traversal",
            "approved reference treated as executable",
            "denied or revise reference allows execution",
            "dirty-state acknowledgement missing",
            "snapshot, rollback, or hash plan missing",
        ],
        "inspector_controls": {
            "inputs": [{"id": "q", "type": "search", "purpose": "filter"}],
            "buttons": [
                {"label": "All", "filter": "all"},
                {"label": "Checklist", "filter": "checklist"},
                {"label": "Targets", "filter": "targets"},
                {"label": "Blocks", "filter": "blocks"},
                {"label": "Receipt", "filter": "receipt"},
                {"label": "Stops", "filter": "stops"},
            ],
        },
        "product_metrics": {
            "required_positive_fixtures": 3,
            "minimum_failure_cases": 75,
            "required_preflight_samples": 4,
            "required_targets": len(targets),
            "max_journey_steps": 3,
        },
    }
    return attach_preflight_hash(cfg)


def refresh_source_input_bundle_hash(item: dict) -> None:
    item["source_input_bundle_hash"] = sha256_json(item["source_inputs"])


def refresh_target_hash(item: dict) -> None:
    item["target_manifest_hash"] = sha256_json(item["target_manifest"])


def refresh_contract_hash_claims(item: dict) -> None:
    c = item["preflight_contract"]
    c["required_source_intake_gate_hash"] = item["source_intake_gate_hash"]
    c["required_packet_hash"] = item["source_packet_hash"]
    c["required_source_bundle_hash"] = item["source_packet_source_bundle_hash"]
    c["required_scope_hash"] = item["source_packet_scope_hash"]
    for sample in item["preflight_samples"]:
        sample["hash_claims"]["intake_gate_hash"] = item["source_intake_gate_hash"]
        sample["hash_claims"]["packet_hash"] = item["source_packet_hash"]
        sample["hash_claims"]["source_bundle_hash"] = item["source_packet_source_bundle_hash"]
        sample["hash_claims"]["scope_hash"] = item["source_packet_scope_hash"]


def refresh_preflight_hash(item: dict) -> None:
    item["preflight_hash_material"] = material(item)
    item["preflight_hash"] = sha256_json(item["preflight_hash_material"])
    item["preflight_contract"]["required_preflight_hash"] = item["preflight_hash"]
    for sample in item["preflight_samples"]:
        sample["required_preflight_hash"] = item["preflight_hash"]
        sample["hash_claims"]["preflight_hash"] = item["preflight_hash"]
    item["non_execution_receipt"]["preflight_hash"] = item["preflight_hash"]


def failure_cases(base: dict) -> list[tuple[str, dict]]:
    cases: list[tuple[str, dict]] = []

    def expected_list(codes: str | list[str]) -> list[str]:
        return [codes] if isinstance(codes, str) else codes

    def mutate(name: str, codes: str | list[str], fn) -> None:
        item = json.loads(json.dumps(base))
        fn(item)
        item["expected_failures"] = expected_list(codes)
        cases.append((name, item))

    for idx, op in enumerate(forbidden_operations(), start=1):
        mutate(f"{idx:02d}-forbidden-{op}.json", f"forbidden_operation:{op}", lambda c, op=op: c["operations"].__setitem__(op, True))

    offset = len(forbidden_operations())
    mutate(f"{offset+1:02d}-source-input-path-missing.json", "source_input_path_missing:source_intake_config", lambda c: (c["source_inputs"][6].__setitem__("source_path", ""), refresh_source_input_bundle_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+2:02d}-source-input-hash-mismatch.json", "source_input_hash_mismatch:source_intake_config", lambda c: (c["source_inputs"][6].__setitem__("source_sha256", "deadbeef"), refresh_source_input_bundle_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+3:02d}-source-input-bundle-hash-mismatch.json", "source_input_bundle_hash_mismatch", lambda c: (c.__setitem__("source_input_bundle_hash", "deadbeef"), refresh_preflight_hash(c)))
    mutate(f"{offset+4:02d}-source-intake-gate-hash-mismatch.json", "source_intake_gate_hash_mismatch", lambda c: (c.__setitem__("source_intake_gate_hash", "deadbeef"), refresh_contract_hash_claims(c), refresh_preflight_hash(c)))
    mutate(f"{offset+5:02d}-source-packet-hash-mismatch.json", "source_packet_hash_mismatch", lambda c: (c.__setitem__("source_packet_hash", "deadbeef"), refresh_contract_hash_claims(c), refresh_preflight_hash(c)))
    mutate(f"{offset+6:02d}-source-bundle-hash-mismatch.json", "source_packet_source_bundle_hash_mismatch", lambda c: (c.__setitem__("source_packet_source_bundle_hash", "deadbeef"), refresh_contract_hash_claims(c), refresh_preflight_hash(c)))
    mutate(f"{offset+7:02d}-source-scope-hash-mismatch.json", "source_packet_scope_hash_mismatch", lambda c: (c.__setitem__("source_packet_scope_hash", "deadbeef"), refresh_contract_hash_claims(c), refresh_preflight_hash(c)))
    hash_missing_expected = [
        "preflight_hash_missing",
        "contract_preflight_hash_mismatch",
        "sample_preflight_hash_mismatch:synthetic_approved_reference_preflight",
        "sample_preflight_hash_mismatch:synthetic_denied_reference_preflight",
        "sample_preflight_hash_mismatch:synthetic_dirty_state_preflight_block",
        "sample_preflight_hash_mismatch:synthetic_revision_reference_preflight",
        "sample_required_preflight_hash_mismatch:synthetic_approved_reference_preflight",
        "sample_required_preflight_hash_mismatch:synthetic_denied_reference_preflight",
        "sample_required_preflight_hash_mismatch:synthetic_dirty_state_preflight_block",
        "sample_required_preflight_hash_mismatch:synthetic_revision_reference_preflight",
    ]
    hash_mismatch_expected = [
        "preflight_hash_mismatch",
        "non_execution_receipt_preflight_hash_mismatch",
        "contract_preflight_hash_mismatch",
        "sample_preflight_hash_mismatch:synthetic_approved_reference_preflight",
        "sample_preflight_hash_mismatch:synthetic_denied_reference_preflight",
        "sample_preflight_hash_mismatch:synthetic_dirty_state_preflight_block",
        "sample_preflight_hash_mismatch:synthetic_revision_reference_preflight",
        "sample_required_preflight_hash_mismatch:synthetic_approved_reference_preflight",
        "sample_required_preflight_hash_mismatch:synthetic_denied_reference_preflight",
        "sample_required_preflight_hash_mismatch:synthetic_dirty_state_preflight_block",
        "sample_required_preflight_hash_mismatch:synthetic_revision_reference_preflight",
    ]
    mutate(f"{offset+8:02d}-preflight-hash-missing.json", hash_missing_expected, lambda c: c.__setitem__("preflight_hash", ""))
    mutate(f"{offset+9:02d}-preflight-hash-mismatch.json", hash_mismatch_expected, lambda c: c.__setitem__("preflight_hash", "deadbeef"))
    mutate(f"{offset+10:02d}-target-absolute-path.json", ["target_path_not_relative:native_home", "target_relative_target_mismatch:native_home"], lambda c: (c["target_manifest"][0].__setitem__("relative_target", "H:/Obsidian/VAKS.md"), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+11:02d}-target-parent-traversal.json", ["target_path_not_relative:native_home", "target_relative_target_mismatch:native_home"], lambda c: (c["target_manifest"][0].__setitem__("relative_target", "../VAKS.md"), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+12:02d}-extra-target-requested.json", ["target_manifest_scope_mismatch", "target_not_in_packet_scope:extra_target", "too_many_targets"], lambda c: (c["target_manifest"].append(dict(c["target_manifest"][0], id="extra_target")), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+13:02d}-target-source-hash-missing.json", ["target_source_hash_missing:native_home", "target_source_hash_mismatch:native_home"], lambda c: (c["target_manifest"][0].__setitem__("source_sha256", ""), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+14:02d}-target-state-checked.json", "target_formal_vault_state_checked:native_home", lambda c: (c["target_manifest"][0].__setitem__("formal_vault_target_exists_checked", True), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+15:02d}-target-snapshot-taken.json", "target_snapshot_taken:native_home", lambda c: (c["target_manifest"][0].__setitem__("snapshot_taken", True), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+16:02d}-target-hash-before-collected.json", "target_hash_before_collected:native_home", lambda c: (c["target_manifest"][0].__setitem__("hash_before_collected", True), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+17:02d}-target-write-enabled.json", "target_write_enabled_now:native_home", lambda c: (c["target_manifest"][0].__setitem__("write_enabled_now", True), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+18:02d}-target-relative-drift.json", "target_relative_target_mismatch:native_home", lambda c: (c["target_manifest"][0].__setitem__("relative_target", "VAKS-Workbench-Draft/99 Wrong But Relative.md"), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+19:02d}-target-source-path-drift.json", "target_source_path_mismatch:native_home", lambda c: (c["target_manifest"][0].__setitem__("source_path", "outputs/review/vaks-implementation-sandbox/wrong/source.md"), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+20:02d}-target-source-sha-drift.json", "target_source_hash_mismatch:native_home", lambda c: (c["target_manifest"][0].__setitem__("source_sha256", "deadbeef"), refresh_target_hash(c), refresh_preflight_hash(c)))
    mutate(f"{offset+21:02d}-sample-not-synthetic.json", "sample_not_synthetic:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("synthetic_only", False), refresh_preflight_hash(c)))
    mutate(f"{offset+22:02d}-sample-actual-user-input.json", "sample_uses_actual_user_input:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("actual_user_input", True), refresh_preflight_hash(c)))
    mutate(f"{offset+23:02d}-sample-real-user-text-stored.json", "sample_stores_real_user_text:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("real_user_text_stored", True), refresh_preflight_hash(c)))
    mutate(f"{offset+24:02d}-sample-captured-user-text.json", "sample_captures_user_text:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("captured_user_text", "actual approval text"), refresh_preflight_hash(c)))
    mutate(f"{offset+25:02d}-sample-missing-decision-reference.json", "sample_missing_decision_reference:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("decision_reference_present", False), refresh_preflight_hash(c)))
    mutate(f"{offset+26:02d}-sample-intake-hash-mismatch.json", "sample_intake_gate_hash_mismatch:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0]["hash_claims"].__setitem__("intake_gate_hash", "deadbeef"), refresh_preflight_hash(c)))
    mutate(f"{offset+27:02d}-sample-packet-hash-mismatch.json", "sample_packet_hash_mismatch:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0]["hash_claims"].__setitem__("packet_hash", "deadbeef"), refresh_preflight_hash(c)))
    mutate(f"{offset+28:02d}-sample-scope-hash-mismatch.json", "sample_scope_hash_mismatch:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0]["hash_claims"].__setitem__("scope_hash", "deadbeef"), refresh_preflight_hash(c)))
    mutate(f"{offset+29:02d}-sample-check-false.json", "sample_preflight_check_failed:synthetic_approved_reference_preflight:formal_vault_not_accessed", lambda c: (c["preflight_samples"][0]["preflight_checks"].__setitem__("formal_vault_not_accessed", False), refresh_preflight_hash(c)))
    mutate(f"{offset+30:02d}-sample-execution-performed.json", "sample_execution_performed:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("execution_performed", True), refresh_preflight_hash(c)))
    mutate(f"{offset+31:02d}-sample-formal-vault-accessed.json", "sample_accesses_formal_vault:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("formal_vault_accessed", True), refresh_preflight_hash(c)))
    mutate(f"{offset+32:02d}-sample-state-inspected.json", "sample_inspects_formal_vault_state:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("formal_vault_state_inspected", True), refresh_preflight_hash(c)))
    mutate(f"{offset+33:02d}-sample-snapshot-taken.json", "sample_snapshot_taken:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("snapshot_taken", True), refresh_preflight_hash(c)))
    mutate(f"{offset+34:02d}-sample-hash-before-collected.json", "sample_hash_before_collected:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("hash_before_collected", True), refresh_preflight_hash(c)))
    mutate(f"{offset+35:02d}-sample-allows-write.json", "sample_allows_formal_vault_write_now:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("formal_vault_write_allowed_now", True), refresh_preflight_hash(c)))
    mutate(f"{offset+36:02d}-sample-creates-action-basis.json", "sample_creates_action_basis:synthetic_approved_reference_preflight", lambda c: (c["preflight_samples"][0].__setitem__("action_basis_created", True), refresh_preflight_hash(c)))
    mutate(f"{offset+37:02d}-approved-actionable-result.json", ["approved_sample_result_actionable:synthetic_approved_reference_preflight", "approved_sample_result_bad:synthetic_approved_reference_preflight"], lambda c: (c["preflight_samples"][0].__setitem__("expected_preflight_result", "READY_TO_WRITE"), refresh_preflight_hash(c)))
    mutate(f"{offset+38:02d}-deny-allows-execution.json", "denied_sample_executes:synthetic_denied_reference_preflight", lambda c: (c["preflight_samples"][1].__setitem__("execution_performed", True), refresh_preflight_hash(c)))
    mutate(f"{offset+39:02d}-deny-wrong-result.json", "denied_sample_result_bad:synthetic_denied_reference_preflight", lambda c: (c["preflight_samples"][1].__setitem__("expected_preflight_result", "READY_TO_WRITE"), refresh_preflight_hash(c)))
    mutate(f"{offset+40:02d}-revise-allows-execution.json", "revise_sample_executes:synthetic_revision_reference_preflight", lambda c: (c["preflight_samples"][2].__setitem__("execution_performed", True), refresh_preflight_hash(c)))
    mutate(f"{offset+41:02d}-revise-wrong-result.json", "revise_sample_result_bad:synthetic_revision_reference_preflight", lambda c: (c["preflight_samples"][2].__setitem__("expected_preflight_result", "READY_TO_WRITE"), refresh_preflight_hash(c)))
    mutate(f"{offset+42:02d}-dirty-state-does-not-block.json", "dirty_sample_result_bad:synthetic_dirty_state_preflight_block", lambda c: (c["preflight_samples"][3].__setitem__("expected_preflight_result", "PREFLIGHT_DRY_RUN_COMPLETE_NOT_EXECUTABLE"), refresh_preflight_hash(c)))
    mutate(f"{offset+43:02d}-contract-allows-execution.json", "contract_allows_execution", lambda c: (c["preflight_contract"].__setitem__("current_slice_executes", True), refresh_preflight_hash(c)))
    mutate(f"{offset+44:02d}-contract-allows-vault-access.json", "contract_allows_formal_vault_access", lambda c: (c["preflight_contract"].__setitem__("formal_vault_access_disallowed", False), refresh_preflight_hash(c)))
    mutate(f"{offset+45:02d}-contract-missing-separate-execution.json", "contract_missing_separate_execution_slice", lambda c: (c["preflight_contract"].__setitem__("separate_future_execution_slice_required", False), refresh_preflight_hash(c)))
    mutate(f"{offset+46:02d}-contract-missing-check.json", "contract_missing_required_preflight_check:formal_vault_not_accessed", lambda c: (c["preflight_contract"].__setitem__("required_preflight_checks", [x for x in c["preflight_contract"]["required_preflight_checks"] if x != "formal_vault_not_accessed"]), refresh_preflight_hash(c)))
    mutate(f"{offset+47:02d}-receipt-claims-execution.json", "non_execution_receipt_claims_execution", lambda c: (c["non_execution_receipt"].__setitem__("execution_performed", True), refresh_preflight_hash(c)))
    mutate(f"{offset+48:02d}-receipt-formal-vault-accessed.json", "non_execution_receipt_formal_vault_accessed", lambda c: (c["non_execution_receipt"].__setitem__("formal_vault_accessed", True), refresh_preflight_hash(c)))
    mutate(f"{offset+49:02d}-receipt-hash-collected.json", "non_execution_receipt_hash_before_collected", lambda c: (c["non_execution_receipt"].__setitem__("hash_before_collected", True), refresh_preflight_hash(c)))
    mutate(f"{offset+50:02d}-authority-confusing-text.json", "authority_confusing_text", lambda c: (c.__setitem__("purpose", "ready to write formal vault after this preflight"), refresh_preflight_hash(c)))
    mutate(f"{offset+51:02d}-too-few-failure-cases.json", "minimum_failure_cases_too_low", lambda c: (c["product_metrics"].__setitem__("minimum_failure_cases", 12), refresh_preflight_hash(c)))
    mutate(f"{offset+52:02d}-inspector-execute-button.json", ["inspector_buttons_not_allowlisted", "inspector_control_not_allowed:button:execute"], lambda c: (c["inspector_controls"]["buttons"].append({"label": "Execute", "filter": "execute"}), refresh_preflight_hash(c)))
    mutate(f"{offset+53:02d}-missing-stop-condition-execution.json", "missing_stop_condition:execution requested", lambda c: (c.__setitem__("stop_conditions", [s for s in c["stop_conditions"] if s != "execution requested"]), refresh_preflight_hash(c)))
    return cases


def frontmatter(record_kind: str, status: str) -> str:
    return f"""---
record_kind: {record_kind}
slice_id: {SLICE_ID}
status: {status}
truth_boundary: sandbox_only
---"""


def md_link(label: str, target: str) -> str:
    return f"[{label}]({target.replace(' ', '%20')})"


def render_slice_plan(git_status_summary: str) -> str:
    return f"""---
record_kind: sandbox_slice_plan
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Slice Plan

## Slice

`{SLICE_ID}`

## Goal

Define a sandbox-only execution preflight dry-run for a future formal-vault
write path. This slice checks that the future execution checklist is complete,
but it does not inspect the formal vault and does not execute anything.

## Why Now

P2-27 defined how a future user decision must be referenced and validated. The
next safe step is to prevent a valid decision reference from becoming an
immediate write by requiring a separate preflight and a separate execution
slice.

## Write Scope

Only:

```text
outputs/review/vaks-implementation-sandbox/{SLICE_ID}/
```

## Non-Touched Paths

- `SCHEMA.md`
- `ARCHITECTURE_PRINCIPLES.md`
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
- `README.md`
- `wiki/claims/`
- `wiki/patterns/`
- `wiki/decisions/`
- `templates/`
- `tools/`
- Obsidian vault

## Acceptance Criteria

- Contract separates preflight completeness from execution permission.
- Target manifest is relative-path only and dry-run only.
- Positive fixtures cover approved-reference dry-run, denial block, and revision
  block.
- Failure cases prove bad paths are caught.
- No formal vault read, scan, state check, write, hash, snapshot, or sync.
- No actual approval collection or real user text storage.
- Reviewer, Boundary, and GPT-5.5 xhigh Product Acceptance pass.
- Final gate passes after Product Acceptance.

## Stop Conditions

Stop if the slice requires real user approval collection, real user text
storage, formal vault access, formal vault state inspection, sync, commit, push,
promotion, dependency installation, background service, hook, or MCP write tool.

## Start Git Status Summary

```text
{git_status_summary}
```

The dirty tree is treated as pre-existing baseline. Final audit is scoped to
this slice path only.
"""


def render_source_map(paths: dict[str, Path], cfg: dict) -> str:
    rows = []
    for key, path in paths.items():
        rel = path.relative_to(sandbox_root())
        rows.append(f"| `{key}` | `../{rel.as_posix()}` | exists: `{path.exists()}` | sha256: `{sha256(path) if path.exists() else 'missing'}` |")
    return f"""---
record_kind: sandbox_source_map
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Source Map

This slice reads P2-27 as the product-grade sandbox source and P2-25 packet
config for exact target scope. It does not read or write the formal Obsidian
vault.

| Source | Path | Evidence |
| --- | --- | --- |
{chr(10).join(rows)}

## Hash Inputs

- source_input_bundle_hash: `{cfg['source_input_bundle_hash']}`
- source_intake_gate_hash: `{cfg['source_intake_gate_hash']}`
- source_packet_hash: `{cfg['source_packet_hash']}`
- source_packet_source_bundle_hash: `{cfg['source_packet_source_bundle_hash']}`
- source_packet_scope_hash: `{cfg['source_packet_scope_hash']}`
- target_manifest_hash: `{cfg['target_manifest_hash']}`
- preflight_hash: `{cfg['preflight_hash']}`

## Boundary

P2-27 `PASS_PRODUCT_GRADE` is a sandbox input only. It is not actual approval,
reviewed knowledge, evidence support, action basis, mainline approval, formal
vault approval, sync approval, commit approval, push approval, promotion
approval, or execution approval.
"""


def render_contract(cfg: dict) -> str:
    checks = "\n".join(f"- `{item}`" for item in cfg["preflight_contract"]["required_preflight_checks"])
    targets = "\n".join(f"- `{item['id']}` -> `{item['relative_target']}`" for item in cfg["target_manifest"])
    return f"""# Formal Vault Execution Preflight Dry-Run Contract

## Input Contract

- P2-27 product-grade user-decision intake gate and hashes.
- P2-25 approval packet target scope.
- No actual approval collection, real user text storage, formal vault read,
  scan, state inspection, write, snapshot, hash, sync, or mutation.

## Required Preflight Checks

{checks}

## Dry-Run Target Manifest

{targets}

## Output Contract

- Execution preflight contract.
- Dry-run target manifest.
- Synthetic approved/denied/revision preflight samples.
- Non-execution receipt.
- Stop condition register.
- Static inspector with no execute, approval, write, save, submit, network, or
  storage controls.

## Boundary Promise

This is an execution preflight dry-run only. It proves checklist shape, not
execution readiness. It does not approve, execute, inspect, write, sync, commit,
push, or promote.

## Hashes

- source_input_bundle_hash: `{cfg['source_input_bundle_hash']}`
- source_intake_gate_hash: `{cfg['source_intake_gate_hash']}`
- source_packet_hash: `{cfg['source_packet_hash']}`
- source_packet_source_bundle_hash: `{cfg['source_packet_source_bundle_hash']}`
- source_packet_scope_hash: `{cfg['source_packet_scope_hash']}`
- target_manifest_hash: `{cfg['target_manifest_hash']}`
- preflight_hash: `{cfg['preflight_hash']}`
"""


def render_home(cfg: dict) -> str:
    return f"""{frontmatter("sandbox_execution_preflight_home", "sandbox_pilot")}

# Execution Preflight Dry-Run Home

This sandbox defines the preflight checks a future execution slice would need
before any formal-vault write could even be requested.

## Start

1. Open [[01 Preflight Checklist]].
2. Open [[02 Dry Run Target Manifest]].
3. Open [[03 Approved Reference Dry Run]].
4. Open [[06 Stop Conditions]] before any action-facing move.

## Fast Links

- [[01 Preflight Checklist]]
- [[02 Dry Run Target Manifest]]
- [[03 Approved Reference Dry Run]]
- [[04 Deny Or Revise Blocks]]
- [[05 Non Execution Receipt]]
- [[06 Stop Conditions]]
- [[07 Reviewer Packet]]
- `execution-preflight-inspector.html`
- {md_link("P2-27 next-step", "../../../" + SOURCE_SLICE_ID + "/next-step.md")}
- {md_link("P2-27 product acceptance", "../../../" + SOURCE_SLICE_ID + "/product-acceptance-report.md")}

## Boundary Rail

Sandbox only. Execution preflight dry-run only. Not actual approval. Approval
not collected. Real user text not stored. Formal vault not accessed. Formal
vault state not inspected. Execution not performed. Snapshot not taken. Hashes
not collected from formal vault. Dry-run only. Not reviewed knowledge. Not
evidence support. Not action basis. Does not approve. Does not execute. No
formal vault read. No formal vault write. No sync. No commit. No push. No
promotion. Requires separate user approval. Requires separate execution slice.
"""


def render_checklist(cfg: dict) -> str:
    checks = "\n".join(f"- `{item}`" for item in cfg["preflight_contract"]["required_preflight_checks"])
    return f"""{frontmatter("sandbox_preflight_checklist", "sandbox_pilot")}

# Preflight Checklist

{checks}

## Result Meaning

Completing this checklist would only mean the dry-run shape is complete. It is
not execution readiness and does not open any write path.
"""


def render_targets(cfg: dict) -> str:
    rows = ["| ID | Relative Target | Write Enabled Now | State Checked | Snapshot Taken |", "| --- | --- | --- | --- | --- |"]
    for item in cfg["target_manifest"]:
        rows.append(f"| `{item['id']}` | `{item['relative_target']}` | `{item['write_enabled_now']}` | `{item['formal_vault_target_exists_checked']}` | `{item['snapshot_taken']}` |")
    return f"""{frontmatter("sandbox_dry_run_target_manifest", "sandbox_pilot")}

# Dry Run Target Manifest

{chr(10).join(rows)}

## Boundary

Targets are relative labels only. Formal vault target state is not inspected and
no snapshot, hash, or write is performed.
"""


def render_approved(cfg: dict) -> str:
    sample = next(s for s in cfg["preflight_samples"] if s["id"] == "synthetic_approved_reference_preflight")
    checks = "\n".join(f"- `{key}`: `{value}`" for key, value in sample["preflight_checks"].items())
    return f"""{frontmatter("sandbox_approved_reference_preflight", "sandbox_pilot")}

# Approved Reference Dry Run

## Sample

- decision_verdict: `{sample['decision_verdict']}`
- decision_reference_kind: `{sample['decision_reference_kind']}`
- expected_preflight_result: `{sample['expected_preflight_result']}`
- execution_performed: `{sample['execution_performed']}`
- formal_vault_write_allowed_now: `{sample['formal_vault_write_allowed_now']}`
- next_gate: `{sample['next_gate']}`

## Checks

{checks}

## Boundary

The approved reference dry-run is not executable in this slice. A separate
future execution slice and separate user approval are still required.
"""


def render_blocks(cfg: dict) -> str:
    rows = ["| Sample | Verdict | Expected Result | Executed |", "| --- | --- | --- | --- |"]
    for sample in cfg["preflight_samples"]:
        rows.append(f"| `{sample['id']}` | `{sample['decision_verdict']}` | `{sample['expected_preflight_result']}` | `{sample['execution_performed']}` |")
    return f"""{frontmatter("sandbox_preflight_blocks", "sandbox_pilot")}

# Deny Or Revise Blocks

{chr(10).join(rows)}

## Boundary

Deny and revise block execution. Dirty-state acknowledgement gaps block
execution. Approved references also remain non-executable inside this slice.
"""


def render_receipt(cfg: dict) -> str:
    r = cfg["non_execution_receipt"]
    claims = "\n".join(f"- {item}" for item in r["non_claims"])
    return f"""{frontmatter("sandbox_non_execution_receipt", "sandbox_pilot")}

# Non Execution Receipt

| Field | Value |
| --- | --- |
| approval_collected_now | `{r['approval_collected_now']}` |
| actual_user_input_used | `{r['actual_user_input_used']}` |
| real_user_text_stored | `{r['real_user_text_stored']}` |
| formal_vault_accessed | `{r['formal_vault_accessed']}` |
| formal_vault_state_inspected | `{r['formal_vault_state_inspected']}` |
| execution_performed | `{r['execution_performed']}` |
| snapshot_taken | `{r['snapshot_taken']}` |
| hash_before_collected | `{r['hash_before_collected']}` |
| hash_after_collected | `{r['hash_after_collected']}` |
| current_status | `{r['current_status']}` |
| preflight_hash | `{r['preflight_hash']}` |

## Non Claims

{claims}

## Next

- [[06 Stop Conditions]]
"""


def render_stops(cfg: dict) -> str:
    rows = "\n".join(f"- {item}" for item in cfg["stop_conditions"])
    return f"""{frontmatter("sandbox_execution_preflight_stop_conditions", "sandbox_pilot")}

# Stop Conditions

{rows}

## Safe Alternative

Record the requested move as a future sandbox item and stop. Do not perform the
operation in this slice.
"""


def render_reviewer_packet(cfg: dict) -> str:
    return f"""{frontmatter("sandbox_reviewer_packet", "sandbox_pilot")}

# Reviewer Packet

## Inspect First

- `artifact/formal-vault-execution-preflight-dry-run-contract.md`
- `fixtures/valid-execution-preflight-config.json`
- `fixtures/valid-deny-execution-preflight-config.json`
- `fixtures/valid-revise-execution-preflight-config.json`
- `artifact/failure-case-oracle.md`
- `prototype/formal-vault-execution-preflight-dry-run/`
- `artifact/verify_execution_preflight.py`

## Review Questions

- Does preflight completeness stay separate from execution permission?
- Does any sample inspect or write the formal vault?
- Are targets relative and dry-run only?
- Do deny, revise, and dirty-state gaps block execution?
- Does the inspector remain read-only and non-executing?
"""


def render_inspector_html(cfg: dict) -> str:
    cards = [
        f"""<article class=\"card\" data-kind=\"checklist\" data-search=\"checklist preflight dry run no execution\">
  <p class=\"eyebrow\">checklist</p>
  <h3>Preflight Checklist</h3>
  <p>Checklist shape is complete only as a dry-run.</p>
  <strong>{cfg['preflight_hash']}</strong>
</article>""",
        """<article class=\"card\" data-kind=\"targets\" data-search=\"targets relative manifest no formal vault state inspection\">
  <p class=\"eyebrow\">targets</p>
  <h3>Dry Run Target Manifest</h3>
  <p>Targets are relative labels; formal vault target state is not inspected.</p>
  <strong>write_enabled_now=false</strong>
</article>""",
        """<article class=\"card\" data-kind=\"blocks\" data-search=\"deny revise dirty state block execution\">
  <p class=\"eyebrow\">blocks</p>
  <h3>Blocking Outcomes</h3>
  <p>Deny, revise, and missing dirty-state acknowledgement block execution.</p>
  <strong>execution_performed=false</strong>
</article>""",
        """<article class=\"card\" data-kind=\"receipt\" data-search=\"non execution receipt formal vault not accessed hash not collected\">
  <p class=\"eyebrow\">receipt</p>
  <h3>Non Execution Receipt</h3>
  <p>No approval, user text, vault access, state check, snapshot, hash, or write happened.</p>
  <strong>not execution readiness</strong>
</article>""",
        """<article class=\"card\" data-kind=\"stops\" data-search=\"stop conditions no sync no commit no push no promotion no execution\">
  <p class=\"eyebrow\">stops</p>
  <h3>Stop Conditions</h3>
  <p>Stop on execution request, formal vault access, hash/snapshot request, sync, commit, push, or promotion.</p>
  <strong>does not execute</strong>
</article>""",
    ]
    buttons = []
    for control in cfg["inspector_controls"]["buttons"]:
        active = ' class="active"' if control["filter"] == "all" else ""
        buttons.append(f"<button type=\"button\"{active} data-filter=\"{control['filter']}\">{control['label']}</button>")
    data = {
        "preflight_contract": cfg["preflight_contract"],
        "target_manifest": cfg["target_manifest"],
        "preflight_samples": cfg["preflight_samples"],
        "non_execution_receipt": cfg["non_execution_receipt"],
        "stop_conditions": cfg["stop_conditions"],
    }
    return f"""<!doctype html>
<html lang=\"en\" data-sandbox-only=\"true\" data-execution-preflight-only=\"true\" data-dry-run-only=\"true\" data-no-approval=\"true\" data-no-real-user-text-storage=\"true\" data-no-formal-vault-access=\"true\" data-no-execution=\"true\" data-no-write=\"true\" data-no-sync=\"true\" data-no-authority=\"true\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Formal Vault Execution Preflight Dry-Run</title>
  <style>
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: #172026; background: #f7faf8; }}
    header {{ padding: 24px 28px 16px; background: #fff; border-bottom: 1px solid #d8dee4; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; letter-spacing: 0; }}
    .layout {{ display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 18px; padding: 18px 28px 32px; }}
    .toolbar {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 14px; }}
    input {{ min-width: 280px; height: 40px; padding: 0 12px; border: 1px solid #d8dee4; border-radius: 6px; }}
    button {{ height: 40px; border: 1px solid #d8dee4; background: #fff; border-radius: 6px; padding: 0 12px; font-weight: 700; }}
    button.active {{ border-color: #256f68; color: #256f68; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; }}
    .card, aside {{ background: #fff; border: 1px solid #d8dee4; border-radius: 8px; padding: 14px; }}
    .card h3 {{ margin: 4px 0 8px; font-size: 18px; }}
    .card p, aside li {{ color: #52616b; line-height: 1.45; }}
    .eyebrow {{ margin: 0; color: #256f68; text-transform: uppercase; font-size: 12px; font-weight: 700; }}
    aside {{ align-self: start; position: sticky; top: 16px; }}
    @media (max-width: 860px) {{ .layout {{ grid-template-columns: 1fr; padding: 16px; }} input {{ min-width: 100%; }} }}
  </style>
</head>
<body>
  <header>
    <h1>Formal Vault Execution Preflight Dry-Run</h1>
    <p>Sandbox-only preflight. Approval not collected. It cannot approve, inspect the formal vault, execute, write, sync, read the formal vault, write the formal vault, or collect hashes from the vault.</p>
  </header>
  <div class=\"layout\">
    <main>
      <div class=\"toolbar\" data-role=\"preflight-filter\">
        <input id=\"q\" type=\"search\" placeholder=\"Search checklist, targets, blocks, receipt, stops\">
        {' '.join(buttons)}
      </div>
      <div class=\"grid\" data-role=\"preflight-cards\">
        {chr(10).join(cards)}
      </div>
    </main>
    <aside data-role=\"boundary-rail\">
      <h2>Boundary Rail</h2>
      <ul>
        <li>sandbox only</li>
        <li>execution preflight dry-run only</li>
        <li>not actual approval</li>
        <li>approval not collected</li>
        <li>formal vault not accessed</li>
        <li>formal vault state not inspected</li>
        <li>execution not performed</li>
        <li>snapshot not taken</li>
        <li>hashes not collected from formal vault</li>
        <li>no formal vault read / no formal vault write</li>
        <li>not evidence support / not action basis</li>
        <li>no sync / no commit / no push / no promotion</li>
      </ul>
    </aside>
  </div>
  <script type=\"application/json\" id=\"preflight-data\">
{json.dumps(data, indent=2, ensure_ascii=False)}
  </script>
  <script>
    const input = document.getElementById('q');
    const cards = Array.from(document.querySelectorAll('.card'));
    const buttons = Array.from(document.querySelectorAll('button[data-filter]'));
    let filter = 'all';
    function applyFilter() {{
      const query = input.value.toLowerCase();
      cards.forEach(card => {{
        const okFilter = filter === 'all' || card.dataset.kind === filter;
        const okQuery = !query || card.dataset.search.toLowerCase().includes(query) || card.textContent.toLowerCase().includes(query);
        card.hidden = !(okFilter && okQuery);
      }});
    }}
    buttons.forEach(btn => btn.addEventListener('click', () => {{
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filter = btn.dataset.filter;
      applyFilter();
    }}));
    input.addEventListener('input', applyFilter);
  </script>
</body>
</html>
"""


def render_receipt_json(cfg: dict, paths: dict[str, Path]) -> dict:
    return {
        "record_kind": "sandbox_formal_vault_execution_preflight_receipt",
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "formal_vault_accessed": False,
        "formal_vault_state_inspected": False,
        "approval_collected_now": False,
        "actual_user_input_used": False,
        "real_user_text_stored": False,
        "execution_performed": False,
        "snapshot_taken": False,
        "hash_before_collected": False,
        "hash_after_collected": False,
        "write_scope": cfg["write_scope"],
        "source_hashes": {key: sha256(path) if path.exists() else "missing" for key, path in paths.items()},
        "source_input_bundle_hash": cfg["source_input_bundle_hash"],
        "source_intake_gate_hash": cfg["source_intake_gate_hash"],
        "source_packet_hash": cfg["source_packet_hash"],
        "target_manifest_hash": cfg["target_manifest_hash"],
        "preflight_hash": cfg["preflight_hash"],
        "target_count": len(cfg["target_manifest"]),
        "sample_count": len(cfg["preflight_samples"]),
        "forbidden_operations": {op: False for op in forbidden_operations()},
        "non_claims": cfg["non_execution_receipt"]["non_claims"],
    }


def render_failure_oracle_md(cases: list[tuple[str, dict]]) -> str:
    rows = ["# Failure Case Oracle", "", "| File | Expected failure |", "| --- | --- |"]
    for name, item in cases:
        rows.append(f"| `{name}` | `{', '.join(item['expected_failures'])}` |")
    return "\n".join(rows)


def render_pending(kind: str, title: str) -> str:
    return f"""---
record_kind: {kind}
slice_id: {SLICE_ID}
status: pending
truth_boundary: sandbox_only
---

# {title}

Pending.
"""


def variant_config(base: dict, focus: str) -> dict:
    variant = json.loads(json.dumps(base))
    variant["fixture_focus"] = focus
    if focus == "deny":
        keep = {"synthetic_denied_reference_preflight"}
        variant["purpose"] = "Variant fixture focused on denial blocking preflight."
    elif focus == "revise":
        keep = {"synthetic_revision_reference_preflight"}
        variant["purpose"] = "Variant fixture focused on revision blocking preflight."
    else:
        keep = {sample["id"] for sample in variant["preflight_samples"]}
    variant["preflight_samples"] = [sample for sample in variant["preflight_samples"] if sample["id"] in keep]
    variant["product_metrics"]["required_preflight_samples"] = len(variant["preflight_samples"])
    return attach_preflight_hash(variant)


def build() -> None:
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required source files: " + "; ".join(missing))
    cfg = config()
    git_status_summary = "pre-existing dirty tree recorded before build; final audit scoped to this slice path"

    safe_write("slice-plan.md", render_slice_plan(git_status_summary))
    safe_write("source-map.md", render_source_map(paths, cfg))
    safe_write("artifact/formal-vault-execution-preflight-dry-run-contract.md", render_contract(cfg))
    safe_write("fixtures/valid-execution-preflight-config.json", json.dumps(cfg, indent=2, ensure_ascii=False))
    safe_write("fixtures/valid-deny-execution-preflight-config.json", json.dumps(variant_config(cfg, "deny"), indent=2, ensure_ascii=False))
    safe_write("fixtures/valid-revise-execution-preflight-config.json", json.dumps(variant_config(cfg, "revise"), indent=2, ensure_ascii=False))

    clear_json_files("failure-cases")
    cases = failure_cases(cfg)
    for name, item in cases:
        safe_write(f"failure-cases/{name}", json.dumps(item, indent=2, ensure_ascii=False))
    safe_write("artifact/failure-case-oracle.json", json.dumps([{"file": name, "expected_failures": item["expected_failures"]} for name, item in cases], indent=2, ensure_ascii=False))
    safe_write("artifact/failure-case-oracle.md", render_failure_oracle_md(cases))

    proto = "prototype/formal-vault-execution-preflight-dry-run"
    safe_write(f"{proto}/00 Execution Preflight Home.md", render_home(cfg))
    safe_write(f"{proto}/01 Preflight Checklist.md", render_checklist(cfg))
    safe_write(f"{proto}/02 Dry Run Target Manifest.md", render_targets(cfg))
    safe_write(f"{proto}/03 Approved Reference Dry Run.md", render_approved(cfg))
    safe_write(f"{proto}/04 Deny Or Revise Blocks.md", render_blocks(cfg))
    safe_write(f"{proto}/05 Non Execution Receipt.md", render_receipt(cfg))
    safe_write(f"{proto}/06 Stop Conditions.md", render_stops(cfg))
    safe_write(f"{proto}/07 Reviewer Packet.md", render_reviewer_packet(cfg))
    safe_write(f"{proto}/execution-preflight-inspector.html", render_inspector_html(cfg))
    safe_write(f"{proto}/Receipts/formal-vault-execution-preflight-receipt.json", json.dumps(render_receipt_json(cfg, paths), indent=2, ensure_ascii=False))

    safe_write("verification.md", render_pending("sandbox_verification", "Verification"), overwrite=False)
    safe_write("reviewer-report.md", render_pending("sandbox_reviewer_report", "Reviewer Report"), overwrite=False)
    safe_write("boundary-audit.md", render_pending("sandbox_boundary_audit", "Boundary Audit"), overwrite=False)
    safe_write("product-acceptance-report.md", render_pending("sandbox_product_acceptance_report", "Product Acceptance Report"), overwrite=False)
    safe_write("next-step.md", render_pending("sandbox_next_step", "Next Step"), overwrite=False)


if __name__ == "__main__":
    build()
