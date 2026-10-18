from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox"
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


def source_paths() -> dict[str, Path]:
    src = sandbox_root() / SOURCE_SLICE_ID
    packet = sandbox_root() / PACKET_SLICE_ID
    proto = src / "prototype" / "formal-vault-write-decision-rehearsal"
    return {
        "source_next_step": src / "next-step.md",
        "source_product_acceptance": src / "product-acceptance-report.md",
        "source_verification": src / "verification.md",
        "source_reviewer_report": src / "reviewer-report.md",
        "source_boundary_audit": src / "boundary-audit.md",
        "source_map": src / "source-map.md",
        "source_rehearsal_config": src / "fixtures" / "valid-decision-rehearsal-config.json",
        "source_rehearsal_contract": src / "artifact" / "formal-vault-write-decision-rehearsal-contract.md",
        "source_rehearsal_receipt": proto / "Receipts" / "formal-vault-write-decision-rehearsal-receipt.json",
        "source_scenario_matrix": proto / "01 Scenario Matrix.md",
        "source_decision_rules": proto / "05 Decision Rules.md",
        "source_non_approval_receipt": proto / "06 Non Approval Receipt.md",
        "source_stop_conditions": proto / "07 Stop Conditions.md",
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


def scope_ids(packet: dict) -> list[str]:
    return [item["id"] for item in packet["approval_scope"]["items"]]


def approval_phrase_map(packet: dict) -> dict[str, str]:
    return {item["id"]: item["future_confirmation_phrase"] for item in packet["approval_questions"]}


def required_future_fields() -> list[str]:
    return [
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
    ]


def intake_contract(packet: dict, rehearsal: dict) -> dict:
    return {
        "contract_kind": "future_user_decision_intake_gate",
        "current_slice_collects_approval": False,
        "future_user_turn_required": True,
        "actual_user_input_disallowed_in_this_slice": True,
        "real_user_text_storage_disallowed_in_this_slice": True,
        "future_user_exact_text_reference_required": True,
        "exact_confirmation_phrases_required_for_approve": True,
        "hash_match_required": True,
        "deny_blocks_write": True,
        "revise_blocks_write": True,
        "extra_files_block_write": True,
        "sync_commit_push_promotion_blocked": True,
        "dirty_state_ack_required_for_approve": True,
        "rollback_and_hash_ack_required_for_approve": True,
        "approved_outcome_not_actionable_in_this_slice": True,
        "separate_future_execution_slice_required": True,
        "default_verdict": "NEEDS_REVISION",
        "allowed_verdict_values": ["APPROVED_BY_USER", "DENIED_BY_USER", "NEEDS_REVISION"],
        "required_future_fields": required_future_fields(),
        "required_packet_hash": packet["packet_hash"],
        "required_source_bundle_hash": packet["source_bundle_hash"],
        "required_scope_hash": packet["approval_scope"]["scope_hash"],
        "required_rehearsal_hash": rehearsal["rehearsal_hash"],
        "required_scope_ids": scope_ids(packet),
        "required_exclusions": ["obsidian_sync", "commit", "push", "promotion"],
        "required_confirmation_phrases": approval_phrase_map(packet),
    }


def common_hashes(packet: dict, rehearsal: dict) -> dict:
    return {
        "packet_hash": packet["packet_hash"],
        "source_bundle_hash": packet["source_bundle_hash"],
        "scope_hash": packet["approval_scope"]["scope_hash"],
        "rehearsal_hash": rehearsal["rehearsal_hash"],
    }


def common_decision_record(packet: dict, rehearsal: dict) -> dict:
    return {
        "synthetic_only": True,
        "actual_user_input": False,
        "approval_collected_now": False,
        "real_user_text_stored": False,
        "captured_user_text": "",
        "future_user_exact_text_reference": "future_turn_ref:REQUIRED_NOT_STORED_IN_THIS_SLICE",
        "user_turn_id": "future_user_turn_required",
        "timestamp_utc": "future_timestamp_required",
        "operator_or_agent_id": "future_operator_required",
        "scope_ids": scope_ids(packet),
        "hash_claims": common_hashes(packet, rehearsal),
        "explicit_exclusions_ack": ["obsidian_sync", "commit", "push", "promotion"],
        "extra_files_requested": False,
        "formal_vault_write_allowed_now": False,
        "formal_vault_accessed": False,
        "action_basis_created": False,
        "reviewed_knowledge_created": False,
        "sync_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "promotion_allowed": False,
    }


def synthetic_intake_samples(packet: dict, rehearsal: dict) -> list[dict]:
    common = common_decision_record(packet, rehearsal)
    phrases = approval_phrase_map(packet)
    return [
        {
            "id": "future_approve_reference_capture",
            "decision_id": "future_decision_id_required",
            "decision_verdict": "APPROVED_BY_USER",
            "phrase_claims": dict(phrases),
            "confirmed_question_ids": list(phrases.keys()),
            "rollback_ack": True,
            "hash_ack": True,
            "dirty_state_ack": True,
            "expected_gate_result": "VALID_FUTURE_APPROVAL_RECORD_BUT_NOT_ACTIONABLE_IN_THIS_SLICE",
            "next_gate": "future_separately_approved_execution_slice_required",
            **common,
        },
        {
            "id": "future_deny_reference_capture",
            "decision_id": "future_decision_id_required",
            "decision_verdict": "DENIED_BY_USER",
            "phrase_claims": {},
            "confirmed_question_ids": [],
            "rollback_ack": False,
            "hash_ack": False,
            "dirty_state_ack": False,
            "expected_gate_result": "BLOCKED_BY_FUTURE_DENIAL_RECORD",
            "next_gate": "stop_and_record_denial_only",
            **common,
        },
        {
            "id": "future_revision_reference_capture",
            "decision_id": "future_decision_id_required",
            "decision_verdict": "NEEDS_REVISION",
            "phrase_claims": {},
            "confirmed_question_ids": [],
            "rollback_ack": False,
            "hash_ack": False,
            "dirty_state_ack": False,
            "expected_gate_result": "BLOCKED_PENDING_PACKET_REVISION",
            "next_gate": "revise_packet_in_future_sandbox_only",
            **common,
        },
    ]


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


def attach_gate_hash(cfg: dict) -> dict:
    material = gate_material(cfg)
    cfg["intake_gate_hash_material"] = material
    cfg["intake_gate_hash"] = sha256_json(material)
    for sample in cfg["synthetic_intake_samples"]:
        sample["required_intake_gate_hash"] = cfg["intake_gate_hash"]
        sample["hash_claims"]["intake_gate_hash"] = cfg["intake_gate_hash"]
    cfg["intake_contract"]["required_intake_gate_hash"] = cfg["intake_gate_hash"]
    cfg["non_approval_receipt"]["intake_gate_hash"] = cfg["intake_gate_hash"]
    return cfg


def config() -> dict:
    paths = source_paths()
    inputs = [source_input(key, path) for key, path in paths.items()]
    packet = load_json(paths["source_packet_config"])
    rehearsal = load_json(paths["source_rehearsal_config"])
    cfg = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "packet_slice": PACKET_SLICE_ID,
        "intake_gate_version": "p2-27-user-decision-intake-gate-v1",
        "purpose": "Define a future explicit user-decision intake gate without collecting current approval, storing real user text, or executing formal vault operations.",
        "formal_vault_path_label": "formal Obsidian vault path is a label only; it is not accessed in this slice",
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": [item["source_path"] for item in inputs],
        "operations": {op: False for op in forbidden_operations()}
        | {"default_read_only": True, "rebuild_requires_explicit_flag": True},
        "boundary_phrases": [
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
        ],
        "source_inputs": inputs,
        "source_input_bundle_hash": sha256_json(inputs),
        "source_rehearsal_hash": rehearsal["rehearsal_hash"],
        "source_packet_hash": packet["packet_hash"],
        "source_packet_source_bundle_hash": packet["source_bundle_hash"],
        "source_packet_scope_hash": packet["approval_scope"]["scope_hash"],
        "source_packet_version": packet["packet_version"],
        "intake_contract": intake_contract(packet, rehearsal),
        "synthetic_intake_samples": synthetic_intake_samples(packet, rehearsal),
        "non_approval_receipt": {
            "approval_collected_now": False,
            "actual_user_input_used": False,
            "real_user_text_stored": False,
            "formal_vault_accessed": False,
            "current_status": "future_user_decision_intake_gate_defined_pending_review",
            "non_claims": [
                "not actual approval",
                "not formal vault approval",
                "not sync approval",
                "not commit approval",
                "not push approval",
                "not promotion approval",
                "not action basis",
                "not reviewed knowledge",
                "not evidence support",
                "not a user decision record",
            ],
        },
        "stop_conditions": [
            "actual user approval collection requested",
            "actual user decision collection requested",
            "real user text storage requested",
            "formal vault read requested",
            "formal vault scan requested",
            "formal vault write requested",
            "formal vault hash or snapshot requested",
            "absolute vault path requested",
            "Obsidian sync requested",
            "commit or push requested",
            "promotion requested",
            "decision inferred from silence or prior PASS",
            "future user exact text reference missing",
            "required confirmation phrase missing",
            "packet hash mismatch",
            "source bundle hash mismatch",
            "scope hash mismatch",
            "rehearsal hash mismatch",
            "intake gate hash mismatch",
            "approved record treated as action basis",
            "denied or revise record allows write",
            "extra files requested",
            "rollback, hash, or dirty-state acknowledgement missing for approval",
        ],
        "inspector_controls": {
            "inputs": [{"id": "q", "type": "search", "purpose": "filter"}],
            "buttons": [
                {"label": "All", "filter": "all"},
                {"label": "Contract", "filter": "contract"},
                {"label": "Approval Ref", "filter": "approve_reference"},
                {"label": "Blocks", "filter": "blocks"},
                {"label": "Receipt", "filter": "receipt"},
                {"label": "Stops", "filter": "stops"},
            ],
        },
        "product_metrics": {
            "required_positive_fixtures": 3,
            "minimum_failure_cases": 64,
            "required_intake_samples": 3,
            "required_future_fields": len(required_future_fields()),
            "max_journey_steps": 3,
        },
    }
    return attach_gate_hash(cfg)


def refresh_source_input_bundle_hash(item: dict) -> None:
    item["source_input_bundle_hash"] = sha256_json(item["source_inputs"])


def refresh_gate_hash(item: dict) -> None:
    material = gate_material(item)
    item["intake_gate_hash_material"] = material
    item["intake_gate_hash"] = sha256_json(material)
    for sample in item["synthetic_intake_samples"]:
        sample["required_intake_gate_hash"] = item["intake_gate_hash"]
        sample.setdefault("hash_claims", {})["intake_gate_hash"] = item["intake_gate_hash"]
    item["intake_contract"]["required_intake_gate_hash"] = item["intake_gate_hash"]
    item["non_approval_receipt"]["intake_gate_hash"] = item["intake_gate_hash"]


def refresh_contract_hash_claims(item: dict) -> None:
    contract = item["intake_contract"]
    contract["required_packet_hash"] = item["source_packet_hash"]
    contract["required_source_bundle_hash"] = item["source_packet_source_bundle_hash"]
    contract["required_scope_hash"] = item["source_packet_scope_hash"]
    contract["required_rehearsal_hash"] = item["source_rehearsal_hash"]
    for sample in item["synthetic_intake_samples"]:
        hashes = sample["hash_claims"]
        hashes["packet_hash"] = item["source_packet_hash"]
        hashes["source_bundle_hash"] = item["source_packet_source_bundle_hash"]
        hashes["scope_hash"] = item["source_packet_scope_hash"]
        hashes["rehearsal_hash"] = item["source_rehearsal_hash"]


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
    mutate(f"{offset+1:02d}-source-input-path-missing.json", "source_input_path_missing:source_rehearsal_config", lambda c: (c["source_inputs"][6].__setitem__("source_path", ""), refresh_source_input_bundle_hash(c), refresh_gate_hash(c)))
    mutate(f"{offset+2:02d}-source-input-hash-mismatch.json", "source_input_hash_mismatch:source_rehearsal_config", lambda c: (c["source_inputs"][6].__setitem__("source_sha256", "deadbeef"), refresh_source_input_bundle_hash(c), refresh_gate_hash(c)))
    mutate(f"{offset+3:02d}-source-input-bundle-hash-mismatch.json", "source_input_bundle_hash_mismatch", lambda c: (c.__setitem__("source_input_bundle_hash", "deadbeef"), refresh_gate_hash(c)))
    mutate(f"{offset+4:02d}-source-rehearsal-hash-mismatch.json", "source_rehearsal_hash_mismatch", lambda c: (c.__setitem__("source_rehearsal_hash", "deadbeef"), refresh_contract_hash_claims(c), refresh_gate_hash(c)))
    mutate(f"{offset+5:02d}-source-packet-hash-mismatch.json", "source_packet_hash_mismatch", lambda c: (c.__setitem__("source_packet_hash", "deadbeef"), refresh_contract_hash_claims(c), refresh_gate_hash(c)))
    mutate(f"{offset+6:02d}-source-packet-source-bundle-hash-mismatch.json", "source_packet_source_bundle_hash_mismatch", lambda c: (c.__setitem__("source_packet_source_bundle_hash", "deadbeef"), refresh_contract_hash_claims(c), refresh_gate_hash(c)))
    mutate(f"{offset+7:02d}-source-packet-scope-hash-mismatch.json", "source_packet_scope_hash_mismatch", lambda c: (c.__setitem__("source_packet_scope_hash", "deadbeef"), refresh_contract_hash_claims(c), refresh_gate_hash(c)))
    gate_missing_expected = [
        "intake_gate_hash_missing",
        "contract_intake_gate_hash_mismatch",
        "sample_intake_gate_hash_mismatch:future_approve_reference_capture",
        "sample_intake_gate_hash_mismatch:future_deny_reference_capture",
        "sample_intake_gate_hash_mismatch:future_revision_reference_capture",
        "sample_required_intake_gate_hash_mismatch:future_approve_reference_capture",
        "sample_required_intake_gate_hash_mismatch:future_deny_reference_capture",
        "sample_required_intake_gate_hash_mismatch:future_revision_reference_capture",
    ]
    gate_mismatch_expected = [
        "intake_gate_hash_mismatch",
        "non_approval_receipt_intake_gate_hash_mismatch",
        "contract_intake_gate_hash_mismatch",
        "sample_intake_gate_hash_mismatch:future_approve_reference_capture",
        "sample_intake_gate_hash_mismatch:future_deny_reference_capture",
        "sample_intake_gate_hash_mismatch:future_revision_reference_capture",
        "sample_required_intake_gate_hash_mismatch:future_approve_reference_capture",
        "sample_required_intake_gate_hash_mismatch:future_deny_reference_capture",
        "sample_required_intake_gate_hash_mismatch:future_revision_reference_capture",
    ]
    mutate(f"{offset+8:02d}-intake-gate-hash-missing.json", gate_missing_expected, lambda c: c.__setitem__("intake_gate_hash", ""))
    mutate(f"{offset+9:02d}-intake-gate-hash-mismatch.json", gate_mismatch_expected, lambda c: c.__setitem__("intake_gate_hash", "deadbeef"))
    mutate(f"{offset+10:02d}-missing-approve-sample.json", ["missing_intake_sample:future_approve_reference_capture", "too_few_intake_samples"], lambda c: (c.__setitem__("synthetic_intake_samples", [s for s in c["synthetic_intake_samples"] if s["id"] != "future_approve_reference_capture"]), refresh_gate_hash(c)))
    mutate(f"{offset+11:02d}-sample-not-synthetic.json", "sample_not_synthetic:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0].__setitem__("synthetic_only", False), refresh_gate_hash(c)))
    mutate(f"{offset+12:02d}-sample-actual-user-input.json", "sample_uses_actual_user_input:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0].__setitem__("actual_user_input", True), refresh_gate_hash(c)))
    mutate(f"{offset+13:02d}-sample-real-user-text-stored.json", "sample_stores_real_user_text:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0].__setitem__("real_user_text_stored", True), refresh_gate_hash(c)))
    mutate(f"{offset+14:02d}-sample-captured-user-text-present.json", "sample_captures_user_text:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0].__setitem__("captured_user_text", "actual approval text"), refresh_gate_hash(c)))
    mutate(f"{offset+15:02d}-sample-missing-future-text-reference.json", "sample_missing_future_text_reference:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0].__setitem__("future_user_exact_text_reference", ""), refresh_gate_hash(c)))
    mutate(f"{offset+16:02d}-approve-missing-packet-hash.json", "sample_packet_hash_mismatch:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0]["hash_claims"].__setitem__("packet_hash", ""), refresh_gate_hash(c)))
    mutate(f"{offset+17:02d}-approve-wrong-source-bundle-hash.json", "sample_source_bundle_hash_mismatch:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0]["hash_claims"].__setitem__("source_bundle_hash", "deadbeef"), refresh_gate_hash(c)))
    mutate(f"{offset+18:02d}-approve-wrong-scope-hash.json", "sample_scope_hash_mismatch:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0]["hash_claims"].__setitem__("scope_hash", "deadbeef"), refresh_gate_hash(c)))
    mutate(f"{offset+19:02d}-approve-wrong-rehearsal-hash.json", "sample_rehearsal_hash_mismatch:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0]["hash_claims"].__setitem__("rehearsal_hash", "deadbeef"), refresh_gate_hash(c)))
    mutate(f"{offset+20:02d}-approve-missing-confirmation-phrase.json", "approved_missing_confirmation_phrase:future_approve_reference_capture:future_approve_exact_scope", lambda c: (c["synthetic_intake_samples"][0]["phrase_claims"].pop("future_approve_exact_scope"), refresh_gate_hash(c)))
    mutate(f"{offset+21:02d}-approve-missing-exclusion-ack.json", "approved_missing_exclusion_ack:future_approve_reference_capture:promotion", lambda c: (c["synthetic_intake_samples"][0].__setitem__("explicit_exclusions_ack", ["obsidian_sync", "commit", "push"]), refresh_gate_hash(c)))
    mutate(f"{offset+22:02d}-approve-missing-rollback-ack.json", "approved_missing_rollback_ack:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0].__setitem__("rollback_ack", False), refresh_gate_hash(c)))
    mutate(f"{offset+23:02d}-approve-missing-hash-ack.json", "approved_missing_hash_ack:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0].__setitem__("hash_ack", False), refresh_gate_hash(c)))
    mutate(f"{offset+24:02d}-approve-missing-dirty-state-ack.json", "approved_missing_dirty_state_ack:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0].__setitem__("dirty_state_ack", False), refresh_gate_hash(c)))
    mutate(f"{offset+25:02d}-approve-allows-write-now.json", "sample_allows_formal_vault_write_now:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0].__setitem__("formal_vault_write_allowed_now", True), refresh_gate_hash(c)))
    mutate(f"{offset+26:02d}-approve-creates-action-basis.json", "sample_creates_action_basis:future_approve_reference_capture", lambda c: (c["synthetic_intake_samples"][0].__setitem__("action_basis_created", True), refresh_gate_hash(c)))
    mutate(f"{offset+27:02d}-approve-actionable-result.json", ["approved_sample_result_actionable:future_approve_reference_capture", "approved_sample_result_bad:future_approve_reference_capture"], lambda c: (c["synthetic_intake_samples"][0].__setitem__("expected_gate_result", "READY_TO_WRITE"), refresh_gate_hash(c)))
    mutate(f"{offset+28:02d}-deny-allows-write.json", "denied_sample_allows_write:future_deny_reference_capture", lambda c: (c["synthetic_intake_samples"][1].__setitem__("formal_vault_write_allowed_now", True), refresh_gate_hash(c)))
    mutate(f"{offset+29:02d}-deny-wrong-result.json", "denied_sample_result_bad:future_deny_reference_capture", lambda c: (c["synthetic_intake_samples"][1].__setitem__("expected_gate_result", "READY_TO_WRITE"), refresh_gate_hash(c)))
    mutate(f"{offset+30:02d}-revise-allows-write.json", "revise_sample_allows_write:future_revision_reference_capture", lambda c: (c["synthetic_intake_samples"][2].__setitem__("formal_vault_write_allowed_now", True), refresh_gate_hash(c)))
    mutate(f"{offset+31:02d}-revise-wrong-result.json", "revise_sample_result_bad:future_revision_reference_capture", lambda c: (c["synthetic_intake_samples"][2].__setitem__("expected_gate_result", "READY_TO_WRITE"), refresh_gate_hash(c)))
    mutate(f"{offset+32:02d}-contract-missing-required-field.json", "contract_missing_required_future_field:intake_gate_hash", lambda c: (c["intake_contract"].__setitem__("required_future_fields", [f for f in c["intake_contract"]["required_future_fields"] if f != "intake_gate_hash"]), refresh_gate_hash(c)))
    mutate(f"{offset+33:02d}-rule-allows-current-approval-collection.json", "contract_allows_current_approval_collection", lambda c: (c["intake_contract"].__setitem__("current_slice_collects_approval", True), refresh_gate_hash(c)))
    mutate(f"{offset+34:02d}-rule-allows-real-user-text-storage.json", "contract_allows_real_user_text_storage", lambda c: (c["intake_contract"].__setitem__("real_user_text_storage_disallowed_in_this_slice", False), refresh_gate_hash(c)))
    mutate(f"{offset+35:02d}-rule-allows-approval-inference.json", "contract_missing_future_user_turn_required", lambda c: (c["intake_contract"].__setitem__("future_user_turn_required", False), refresh_gate_hash(c)))
    mutate(f"{offset+36:02d}-rule-approved-actionable.json", "contract_allows_approved_outcome_actionable", lambda c: (c["intake_contract"].__setitem__("approved_outcome_not_actionable_in_this_slice", False), refresh_gate_hash(c)))
    mutate(f"{offset+37:02d}-receipt-claims-approval.json", "non_approval_receipt_claims_approval", lambda c: (c["non_approval_receipt"].__setitem__("approval_collected_now", True), refresh_gate_hash(c)))
    mutate(f"{offset+38:02d}-receipt-real-user-text-stored.json", "non_approval_receipt_real_user_text_stored", lambda c: (c["non_approval_receipt"].__setitem__("real_user_text_stored", True), refresh_gate_hash(c)))
    mutate(f"{offset+39:02d}-receipt-formal-vault-accessed.json", "non_approval_receipt_formal_vault_accessed", lambda c: (c["non_approval_receipt"].__setitem__("formal_vault_accessed", True), refresh_gate_hash(c)))
    mutate(f"{offset+40:02d}-authority-confusing-text.json", "authority_confusing_text", lambda c: (c.__setitem__("purpose", "approval collected now and ready to write formal vault"), refresh_gate_hash(c)))
    mutate(f"{offset+41:02d}-too-few-failure-cases.json", "minimum_failure_cases_too_low", lambda c: (c["product_metrics"].__setitem__("minimum_failure_cases", 12), refresh_gate_hash(c)))
    mutate(f"{offset+42:02d}-inspector-approve-button.json", ["inspector_control_not_allowed:button:approve", "inspector_buttons_not_allowlisted"], lambda c: (c["inspector_controls"]["buttons"].append({"label": "Approve", "filter": "approve"}), refresh_gate_hash(c)))
    mutate(f"{offset+43:02d}-missing-stop-condition-real-user-text.json", "missing_stop_condition:real user text storage", lambda c: (c.__setitem__("stop_conditions", [s for s in c["stop_conditions"] if "real user text" not in s]), refresh_gate_hash(c)))
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

Define a sandbox-only gate for how a future explicit user decision would be
captured, validated, and classified before any later formal-vault write slice.

## Why Now

P2-26 proved synthetic approve/deny/revise classification. The next smallest
safe step is to define the future intake contract that prevents a later agent
from treating silence, prior Product Acceptance, or casual chat as formal write
approval.

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

- Contract states required future decision fields and exact hash bindings.
- Positive fixtures cover approve, deny, and revise reference records.
- Approval remains not actionable in this slice.
- Deny and revise block write.
- Real user text is not captured or stored.
- Formal vault is not read, scanned, written, hashed, snapshotted, or synced.
- Failure cases prove bad paths are caught.
- Reviewer, Boundary, and GPT-5.5 xhigh Product Acceptance pass.
- Final gate passes after Product Acceptance.

## Stop Conditions

Stop if the slice requires real user approval collection, real user text
storage, formal vault access, sync, commit, push, promotion, dependency
installation, background service, hook, or MCP write tool.

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

This slice reads P2-26 as the product-grade sandbox source and P2-25 packet
config for exact future confirmation phrases. It does not read or write the
formal Obsidian vault.

| Source | Path | Evidence |
| --- | --- | --- |
{chr(10).join(rows)}

## Hash Inputs

- source_input_bundle_hash: `{cfg['source_input_bundle_hash']}`
- source_rehearsal_hash: `{cfg['source_rehearsal_hash']}`
- source_packet_hash: `{cfg['source_packet_hash']}`
- source_packet_source_bundle_hash: `{cfg['source_packet_source_bundle_hash']}`
- source_packet_scope_hash: `{cfg['source_packet_scope_hash']}`
- intake_gate_hash: `{cfg['intake_gate_hash']}`

## Boundary

P2-26 `PASS_PRODUCT_GRADE` is a sandbox input only. It is not actual approval,
reviewed knowledge, evidence support, action basis, mainline approval, formal
vault approval, sync approval, commit approval, push approval, or promotion
approval.
"""


def render_contract(cfg: dict) -> str:
    fields = "\n".join(f"- `{field}`" for field in cfg["intake_contract"]["required_future_fields"])
    phrases = "\n".join(f"- `{qid}`: `{phrase}`" for qid, phrase in cfg["intake_contract"]["required_confirmation_phrases"].items())
    return f"""# Formal Vault User Decision Intake Gate Contract

## Input Contract

- P2-26 product-grade decision rehearsal and hashes.
- P2-25 approval packet confirmation phrases.
- No actual user approval, real user text storage, formal vault read, scan,
  write, sync, snapshot, hash, or mutation.

## Required Future Decision Fields

{fields}

## Required Approval Phrases

{phrases}

## Output Contract

- Future decision intake contract.
- Synthetic approve/deny/revise intake reference records.
- Non-approval receipt for this slice.
- Stop condition register.
- Static inspector with no approval, write, save, submit, network, or storage
  controls.

## Boundary Promise

This is a user-decision intake gate draft only. It defines what a later,
separately approved slice must validate. A separate future execution slice is
required. It is not actual approval, not a user decision record, not action
basis, and not permission to write the formal vault.

## Hashes

- source_input_bundle_hash: `{cfg['source_input_bundle_hash']}`
- source_rehearsal_hash: `{cfg['source_rehearsal_hash']}`
- source_packet_hash: `{cfg['source_packet_hash']}`
- source_packet_source_bundle_hash: `{cfg['source_packet_source_bundle_hash']}`
- source_packet_scope_hash: `{cfg['source_packet_scope_hash']}`
- intake_gate_hash: `{cfg['intake_gate_hash']}`
"""


def render_home(cfg: dict) -> str:
    return f"""{frontmatter("sandbox_user_decision_intake_gate_home", "sandbox_pilot")}

# User Decision Intake Gate Home

This sandbox defines how a future explicit user decision must be referenced and
validated before any later formal-vault write slice.

## Start

1. Open [[01 Future Decision Contract]].
2. Open [[02 Required Capture Fields]].
3. Open [[03 Future Approval Checklist]].
4. Open [[06 Stop Conditions]] before any action-facing move.

## Fast Links

- [[01 Future Decision Contract]]
- [[02 Required Capture Fields]]
- [[03 Future Approval Checklist]]
- [[04 Deny Or Revise Blocks]]
- [[05 Non Approval Receipt]]
- [[06 Stop Conditions]]
- [[07 Reviewer Packet]]
- `user-decision-intake-gate-inspector.html`
- {md_link("P2-26 next-step", "../../../" + SOURCE_SLICE_ID + "/next-step.md")}
- {md_link("P2-26 product acceptance", "../../../" + SOURCE_SLICE_ID + "/product-acceptance-report.md")}

## Boundary Rail

Sandbox only. User decision intake gate draft only. Future capture only. Not
actual approval. Approval not collected. Real user text not stored. Formal vault
not accessed. Dry-run only. Not reviewed knowledge. Not evidence support. Not
action basis. Does not approve. No formal vault read. No formal vault write. No
sync. No commit. No push. No promotion. Requires separate user approval.
Requires separate execution slice.
"""


def render_future_contract_page(cfg: dict) -> str:
    contract = cfg["intake_contract"]
    rows = "\n".join(f"| `{key}` | `{value}` |" for key, value in contract.items() if not isinstance(value, (list, dict)))
    return f"""{frontmatter("sandbox_future_decision_contract", "sandbox_pilot")}

# Future Decision Contract

| Rule | Value |
| --- | --- |
{rows}

## Required Hashes

- packet_hash: `{contract['required_packet_hash']}`
- source_bundle_hash: `{contract['required_source_bundle_hash']}`
- scope_hash: `{contract['required_scope_hash']}`
- rehearsal_hash: `{contract['required_rehearsal_hash']}`
- intake_gate_hash: `{contract['required_intake_gate_hash']}`

## Boundary

The contract is a gate definition only. It does not collect approval and does
not open any write path. A separate future execution slice is required before
any formal-vault write could be considered.
"""


def render_capture_fields(cfg: dict) -> str:
    fields = "\n".join(f"- `{field}`" for field in cfg["intake_contract"]["required_future_fields"])
    return f"""{frontmatter("sandbox_required_capture_fields", "sandbox_pilot")}

# Required Capture Fields

{fields}

## Storage Rule

This slice stores no real user text. A future decision record must point to the
future user turn or exact-text reference according to the future approved
execution protocol.

## Boundary

Future user exact text reference is required, but real user text is not captured
or stored in this sandbox.
"""


def render_approve_checklist(cfg: dict) -> str:
    sample = next(s for s in cfg["synthetic_intake_samples"] if s["id"] == "future_approve_reference_capture")
    phrases = "\n".join(f"- `{qid}`: `{phrase}`" for qid, phrase in sample["phrase_claims"].items())
    return f"""{frontmatter("sandbox_future_approval_checklist", "sandbox_pilot")}

# Future Approval Checklist

## Required Phrase Claims

{phrases}

## Required Acks

- rollback_ack: `{sample['rollback_ack']}`
- hash_ack: `{sample['hash_ack']}`
- dirty_state_ack: `{sample['dirty_state_ack']}`
- explicit_exclusions_ack: `{', '.join(sample['explicit_exclusions_ack'])}`

## Result

`{sample['expected_gate_result']}`

## Boundary

The approval reference is not actionable in this slice. A separate future
execution slice is still required.
"""


def render_blocks(cfg: dict) -> str:
    rows = ["| Sample | Verdict | Expected Gate Result | Write Allowed Now |", "| --- | --- | --- | --- |"]
    for sample in cfg["synthetic_intake_samples"]:
        rows.append(f"| `{sample['id']}` | `{sample['decision_verdict']}` | `{sample['expected_gate_result']}` | `{sample['formal_vault_write_allowed_now']}` |")
    return f"""{frontmatter("sandbox_deny_or_revise_blocks", "sandbox_pilot")}

# Deny Or Revise Blocks

{chr(10).join(rows)}

## Boundary

Deny and revise always block write. Approval also remains non-actionable inside
this slice.
"""


def render_receipt(cfg: dict) -> str:
    receipt = cfg["non_approval_receipt"]
    claims = "\n".join(f"- {item}" for item in receipt["non_claims"])
    return f"""{frontmatter("sandbox_non_approval_intake_gate_receipt", "sandbox_pilot")}

# Non Approval Receipt

| Field | Value |
| --- | --- |
| approval_collected_now | `{receipt['approval_collected_now']}` |
| actual_user_input_used | `{receipt['actual_user_input_used']}` |
| real_user_text_stored | `{receipt['real_user_text_stored']}` |
| formal_vault_accessed | `{receipt['formal_vault_accessed']}` |
| current_status | `{receipt['current_status']}` |
| intake_gate_hash | `{receipt['intake_gate_hash']}` |

## Non Claims

{claims}

## Next

- [[06 Stop Conditions]]
"""


def render_stops(cfg: dict) -> str:
    rows = "\n".join(f"- {item}" for item in cfg["stop_conditions"])
    return f"""{frontmatter("sandbox_user_decision_intake_gate_stop_conditions", "sandbox_pilot")}

# Stop Conditions

{rows}

## Safe Alternative

Record the requested move as a future user-decision intake issue or future
sandbox item and stop. Do not perform the operation in this slice.
"""


def render_reviewer_packet(cfg: dict) -> str:
    return f"""{frontmatter("sandbox_reviewer_packet", "sandbox_pilot")}

# Reviewer Packet

## Inspect First

- `artifact/formal-vault-user-decision-intake-gate-contract.md`
- `fixtures/valid-user-decision-intake-gate-config.json`
- `fixtures/valid-deny-user-decision-intake-config.json`
- `fixtures/valid-revise-user-decision-intake-config.json`
- `artifact/failure-case-oracle.md`
- `prototype/formal-vault-user-decision-intake-gate/`
- `artifact/verify_user_decision_intake_gate.py`

## Review Questions

- Does this define a future intake gate rather than collecting approval now?
- Is real user text blocked from storage in this sandbox?
- Do hashes bind to P2-26/P2-25 source material?
- Does approval remain non-actionable here?
- Do deny and revise block write?
- Does the inspector remain read-only and non-approval-collecting?
"""


def render_inspector_html(cfg: dict) -> str:
    cards = [
        f"""<article class=\"card\" data-kind=\"contract\" data-search=\"contract future user turn required no approval no write hash required\">
  <p class=\"eyebrow\">contract</p>
  <h3>Future Decision Contract</h3>
  <p>Requires future user turn, exact-text reference, packet/source/scope/rehearsal/intake hashes, and explicit exclusions.</p>
  <strong>{cfg['intake_gate_hash']}</strong>
</article>""",
        """<article class=\"card\" data-kind=\"approve_reference\" data-search=\"approve reference valid but not actionable separate execution slice\">
  <p class=\"eyebrow\">approve reference</p>
  <h3>Approval Reference</h3>
  <p>A synthetically valid approval record stays non-actionable in this slice.</p>
  <strong>separate execution slice required</strong>
</article>""",
        """<article class=\"card\" data-kind=\"blocks\" data-search=\"deny revise block write no action basis\">
  <p class=\"eyebrow\">blocks</p>
  <h3>Deny / Revise</h3>
  <p>Deny and revise records block write and do not create action basis.</p>
  <strong>write_allowed_now=false</strong>
</article>""",
        """<article class=\"card\" data-kind=\"receipt\" data-search=\"non approval receipt real user text not stored formal vault not accessed\">
  <p class=\"eyebrow\">receipt</p>
  <h3>Non Approval Receipt</h3>
  <p>Approval is not collected, real user text is not stored, and the formal vault is not accessed.</p>
  <strong>not actual approval</strong>
</article>""",
        """<article class=\"card\" data-kind=\"stops\" data-search=\"stop conditions no sync no commit no push no promotion no formal vault write\">
  <p class=\"eyebrow\">stops</p>
  <h3>Stop Conditions</h3>
  <p>Stop on approval collection, real user text storage, formal vault access, hash mismatch, action basis, sync, commit, push, or promotion.</p>
  <strong>does not approve</strong>
</article>""",
    ]
    buttons = []
    for control in cfg["inspector_controls"]["buttons"]:
        active = ' class="active"' if control["filter"] == "all" else ""
        buttons.append(f"<button type=\"button\"{active} data-filter=\"{control['filter']}\">{control['label']}</button>")
    data = {
        "intake_contract": cfg["intake_contract"],
        "synthetic_intake_samples": cfg["synthetic_intake_samples"],
        "non_approval_receipt": cfg["non_approval_receipt"],
        "stop_conditions": cfg["stop_conditions"],
    }
    return f"""<!doctype html>
<html lang=\"en\" data-sandbox-only=\"true\" data-user-decision-intake-gate-only=\"true\" data-future-capture-only=\"true\" data-no-approval=\"true\" data-no-real-user-text-storage=\"true\" data-no-write=\"true\" data-no-sync=\"true\" data-no-authority=\"true\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Formal Vault User Decision Intake Gate</title>
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
    <h1>Formal Vault User Decision Intake Gate</h1>
    <p>Sandbox-only future capture gate. It cannot collect approval, store real user text, write, sync, approve, or execute commands.</p>
  </header>
  <div class=\"layout\">
    <main>
      <div class=\"toolbar\" data-role=\"intake-filter\">
        <input id=\"q\" type=\"search\" placeholder=\"Search contract, approve reference, blocks, receipt, stops\">
        {' '.join(buttons)}
      </div>
      <div class=\"grid\" data-role=\"intake-cards\">
        {chr(10).join(cards)}
      </div>
    </main>
    <aside data-role=\"boundary-rail\">
      <h2>Boundary Rail</h2>
      <ul>
        <li>sandbox only</li>
        <li>user decision intake gate draft only</li>
        <li>future capture only</li>
        <li>not actual approval</li>
        <li>approval not collected</li>
        <li>real user text not stored</li>
        <li>formal vault not accessed</li>
        <li>not evidence support / not action basis</li>
        <li>no formal vault read / no formal vault write</li>
        <li>no sync / no commit / no push / no promotion</li>
      </ul>
    </aside>
  </div>
  <script type=\"application/json\" id=\"intake-data\">
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
    source_hashes = {}
    for key, path in paths.items():
        source_hashes[key] = sha256(path) if path.exists() else "missing"
    return {
        "record_kind": "sandbox_formal_vault_user_decision_intake_gate_receipt",
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "formal_vault_accessed": False,
        "approval_collected_now": False,
        "actual_user_input_used": False,
        "real_user_text_stored": False,
        "write_scope": cfg["write_scope"],
        "source_hashes": source_hashes,
        "source_input_bundle_hash": cfg["source_input_bundle_hash"],
        "source_rehearsal_hash": cfg["source_rehearsal_hash"],
        "source_packet_hash": cfg["source_packet_hash"],
        "intake_gate_hash": cfg["intake_gate_hash"],
        "sample_count": len(cfg["synthetic_intake_samples"]),
        "forbidden_operations": {op: False for op in forbidden_operations()},
        "non_claims": cfg["non_approval_receipt"]["non_claims"],
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


def render_verification_pending() -> str:
    return f"""---
record_kind: sandbox_verification
slice_id: {SLICE_ID}
status: pending
truth_boundary: sandbox_verification_only
---

# Verification

Pending.
"""


def variant_config(base: dict, focus: str) -> dict:
    variant = json.loads(json.dumps(base))
    variant["fixture_focus"] = focus
    if focus == "deny":
        variant["purpose"] = "Variant fixture focused on future denial intake blocking."
    elif focus == "revise":
        variant["purpose"] = "Variant fixture focused on future revision-request intake blocking."
    return attach_gate_hash(variant)


def build() -> None:
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required source files: " + "; ".join(missing))
    cfg = config()
    git_status_summary = "pre-existing dirty tree recorded before build; final audit scoped to this slice path"

    safe_write("slice-plan.md", render_slice_plan(git_status_summary))
    safe_write("source-map.md", render_source_map(paths, cfg))
    safe_write("artifact/formal-vault-user-decision-intake-gate-contract.md", render_contract(cfg))
    safe_write("fixtures/valid-user-decision-intake-gate-config.json", json.dumps(cfg, indent=2, ensure_ascii=False))
    safe_write("fixtures/valid-deny-user-decision-intake-config.json", json.dumps(variant_config(cfg, "deny"), indent=2, ensure_ascii=False))
    safe_write("fixtures/valid-revise-user-decision-intake-config.json", json.dumps(variant_config(cfg, "revise"), indent=2, ensure_ascii=False))

    cases = failure_cases(cfg)
    for name, item in cases:
        safe_write(f"failure-cases/{name}", json.dumps(item, indent=2, ensure_ascii=False))
    safe_write("artifact/failure-case-oracle.json", json.dumps([{"file": name, "expected_failures": item["expected_failures"]} for name, item in cases], indent=2, ensure_ascii=False))
    safe_write("artifact/failure-case-oracle.md", render_failure_oracle_md(cases))

    proto = "prototype/formal-vault-user-decision-intake-gate"
    safe_write(f"{proto}/00 User Decision Intake Gate Home.md", render_home(cfg))
    safe_write(f"{proto}/01 Future Decision Contract.md", render_future_contract_page(cfg))
    safe_write(f"{proto}/02 Required Capture Fields.md", render_capture_fields(cfg))
    safe_write(f"{proto}/03 Future Approval Checklist.md", render_approve_checklist(cfg))
    safe_write(f"{proto}/04 Deny Or Revise Blocks.md", render_blocks(cfg))
    safe_write(f"{proto}/05 Non Approval Receipt.md", render_receipt(cfg))
    safe_write(f"{proto}/06 Stop Conditions.md", render_stops(cfg))
    safe_write(f"{proto}/07 Reviewer Packet.md", render_reviewer_packet(cfg))
    safe_write(f"{proto}/user-decision-intake-gate-inspector.html", render_inspector_html(cfg))
    safe_write(f"{proto}/Receipts/formal-vault-user-decision-intake-gate-receipt.json", json.dumps(render_receipt_json(cfg, paths), indent=2, ensure_ascii=False))

    safe_write("verification.md", render_verification_pending(), overwrite=False)
    safe_write("reviewer-report.md", render_pending("sandbox_reviewer_report", "Reviewer Report"), overwrite=False)
    safe_write("boundary-audit.md", render_pending("sandbox_boundary_audit", "Boundary Audit"), overwrite=False)
    safe_write("product-acceptance-report.md", render_pending("sandbox_product_acceptance_report", "Product Acceptance Report"), overwrite=False)
    safe_write("next-step.md", render_pending("sandbox_next_step", "Next Step"), overwrite=False)


if __name__ == "__main__":
    build()
