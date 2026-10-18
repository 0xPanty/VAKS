import csv
import json
from datetime import datetime, timezone
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

SYNTHESIS_PATH = RESULTS_DIR / "phase_b_keep_stop_synthesis.json"
PACKET_PATH = SANDBOX_DIR / "PHASE_B_KEEP_STOP_SYNTHESIS_PACKET.md"
DECISION_PATH = SANDBOX_DIR / "PHASE_B_KEEP_STOP_SYNTHESIS_DECISION.md"

APPROVED_DOC_SCOPE = [
    "SOURCE_INTAKE.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(rows: list[dict], corpus: str, mode: str) -> dict:
    for row in rows:
        if row.get("corpus") == corpus and row.get("mode") == mode:
            return row
    raise KeyError(f"missing row: {corpus} / {mode}")


def ratio_value(value: str) -> float:
    left, right = value.split("/", 1)
    return float(left) / float(right)


def float_value(value: str) -> float:
    return float(value)


def row_slice(row: dict) -> dict:
    return {
        "hit_at_5": row["hit_at_5"],
        "hit_at_10": row["hit_at_10"],
        "mrr": row["mrr"],
        "action_leakage_rate": row["action_leakage_rate"],
        "forbidden_top1_rate": row["forbidden_top1_rate"],
        "cross_bucket_violation_rate": row["cross_bucket_violation_rate"],
        "warning_coverage_risk": row["warning_coverage_risk"],
        "clickback_coverage": row["clickback_coverage"],
        "hash_coverage": row["hash_coverage"],
        "adapter_coverage": row["adapter_coverage"],
        "receipt_coverage": row["receipt_coverage"],
    }


def compare_rows(old: dict, new: dict) -> dict:
    return {
        "hit_at_5_delta": ratio_value(new["hit_at_5"]) - ratio_value(old["hit_at_5"]),
        "hit_at_10_delta": ratio_value(new["hit_at_10"]) - ratio_value(old["hit_at_10"]),
        "mrr_delta": float_value(new["mrr"]) - float_value(old["mrr"]),
        "action_leakage_delta": float_value(new["action_leakage_rate"]) - float_value(old["action_leakage_rate"]),
        "forbidden_top1_delta": float_value(new["forbidden_top1_rate"]) - float_value(old["forbidden_top1_rate"]),
        "cross_bucket_delta": float_value(new["cross_bucket_violation_rate"]) - float_value(old["cross_bucket_violation_rate"]),
    }


def gate_status(path_name: str, status_key: str) -> dict:
    payload = read_json(RESULTS_DIR / path_name)
    return {
        "status": payload.get(status_key),
        "errors": payload.get("error_count"),
    }


def build_retrieval_evidence() -> dict:
    main_rows = read_csv(RESULTS_DIR / "phase_b_summary.csv")
    holdout_rows = read_csv(RESULTS_DIR / "phase_b_holdout_summary.csv")
    evidence = {
        "main_pressure": {},
        "holdout_pressure": {},
        "positive_checks": {},
    }
    for corpus in ["primary", "full"]:
        baseline = find_row(main_rows, corpus, "baseline_file_lexical")
        skeleton = find_row(main_rows, corpus, "vaks_b_adapter_skeleton")
        yuxi_native = find_row(main_rows, corpus, "yuxi_native_profile")
        evidence["main_pressure"][corpus] = {
            "baseline_file_lexical": row_slice(baseline),
            "vaks_b_adapter_skeleton": row_slice(skeleton),
            "yuxi_native_profile": row_slice(yuxi_native),
            "skeleton_vs_baseline": compare_rows(baseline, skeleton),
            "skeleton_vs_yuxi_native": compare_rows(yuxi_native, skeleton),
        }
    for corpus in ["primary", "full"]:
        baseline = find_row(holdout_rows, corpus, "baseline_file_lexical")
        skeleton = find_row(holdout_rows, corpus, "vaks_b_adapter_skeleton")
        yuxi_native = find_row(holdout_rows, corpus, "yuxi_native_profile")
        evidence["holdout_pressure"][corpus] = {
            "baseline_file_lexical": row_slice(baseline),
            "vaks_b_adapter_skeleton": row_slice(skeleton),
            "yuxi_native_profile": row_slice(yuxi_native),
            "skeleton_vs_baseline": compare_rows(baseline, skeleton),
            "skeleton_vs_yuxi_native": compare_rows(yuxi_native, skeleton),
        }
    main_primary = evidence["main_pressure"]["primary"]["skeleton_vs_baseline"]
    main_full = evidence["main_pressure"]["full"]["skeleton_vs_baseline"]
    holdout_primary = evidence["holdout_pressure"]["primary"]["skeleton_vs_baseline"]
    holdout_full = evidence["holdout_pressure"]["full"]["skeleton_vs_baseline"]
    yuxi_main_primary = evidence["main_pressure"]["primary"]["skeleton_vs_yuxi_native"]
    yuxi_main_full = evidence["main_pressure"]["full"]["skeleton_vs_yuxi_native"]
    yuxi_holdout_primary = evidence["holdout_pressure"]["primary"]["skeleton_vs_yuxi_native"]
    yuxi_holdout_full = evidence["holdout_pressure"]["full"]["skeleton_vs_yuxi_native"]
    evidence["positive_checks"] = {
        "main_primary_hit_mrr_improved_over_baseline": main_primary["hit_at_5_delta"] > 0 and main_primary["mrr_delta"] > 0,
        "main_full_hit_mrr_improved_over_baseline": main_full["hit_at_5_delta"] > 0 and main_full["mrr_delta"] > 0,
        "main_action_leakage_improved_over_baseline": main_primary["action_leakage_delta"] < 0 and main_full["action_leakage_delta"] < 0,
        "holdout_primary_hit_mrr_improved_over_baseline": holdout_primary["hit_at_5_delta"] > 0 and holdout_primary["mrr_delta"] > 0,
        "holdout_full_mrr_improved_and_hit_not_regressed_over_baseline": holdout_full["hit_at_5_delta"] >= 0 and holdout_full["mrr_delta"] > 0,
        "holdout_action_leakage_improved_over_baseline": holdout_primary["action_leakage_delta"] < 0 and holdout_full["action_leakage_delta"] < 0,
        "governance_beats_yuxi_native_main": yuxi_main_primary["action_leakage_delta"] < 0 and yuxi_main_full["action_leakage_delta"] < 0,
        "governance_beats_yuxi_native_holdout": yuxi_holdout_primary["action_leakage_delta"] < 0 and yuxi_holdout_full["action_leakage_delta"] < 0,
        "holdout_retrieval_beats_or_ties_yuxi_native": yuxi_holdout_primary["hit_at_5_delta"] >= 0 and yuxi_holdout_full["hit_at_5_delta"] >= 0,
    }
    return evidence


def build_synthesis() -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    promotion = read_json(RESULTS_DIR / "phase_b_promotion_gate_evaluation_summary.json")
    simulated = read_json(RESULTS_DIR / "phase_b_simulated_reviewer_outcome_summary.json")
    review_queue = read_json(RESULTS_DIR / "phase_b_review_queue_packet_summary.json")
    refreshed = read_json(RESULTS_DIR / "phase_b_refreshed_support_check_candidate_summary.json")
    source_refresh = read_json(RESULTS_DIR / "phase_b_source_refresh_candidate_summary.json")
    support = read_json(RESULTS_DIR / "phase_b_evidence_support_check_candidate_summary.json")
    envelope = read_json(RESULTS_DIR / "phase_b_evidence_envelope_candidate_summary.json")
    context_pack = read_json(RESULTS_DIR / "phase_b_context_pack_candidate_summary.json")
    runtime = read_json(RESULTS_DIR / "phase_b_runtime_feasibility_check.json")
    minimal_doc = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    retrieval = build_retrieval_evidence()
    prior_gates = {
        "promotion_gate": gate_status("phase_b_promotion_gate_check.json", "promotion_gate_status"),
        "simulated_reviewer_outcome": gate_status("phase_b_simulated_reviewer_outcome_check.json", "simulated_reviewer_outcome_status"),
        "review_queue_packet": gate_status("phase_b_review_queue_packet_check.json", "review_queue_packet_status"),
        "refreshed_support_check": gate_status("phase_b_refreshed_support_check_candidate_check.json", "refreshed_support_check_status"),
        "source_refresh": gate_status("phase_b_source_refresh_candidate_check.json", "source_refresh_status"),
        "evidence_support_check": gate_status("phase_b_evidence_support_check_candidate_check.json", "evidence_support_check_status"),
        "evidence_envelope": gate_status("phase_b_evidence_envelope_candidate_check.json", "evidence_envelope_status"),
        "context_pack": gate_status("phase_b_context_pack_candidate_check.json", "context_pack_status"),
        "runtime_feasibility": gate_status("phase_b_runtime_feasibility_check.json", "runtime_feasibility_status"),
        "minimal_doc_patch": gate_status("phase_b_minimal_doc_patch_check.json", "minimal_doc_patch_status"),
        "adapter_contract": gate_status("phase_b_adapter_contract_test.json", "contract_status"),
        "integration_readiness": gate_status("phase_b_integration_readiness_check.json", "readiness_status"),
        "mainline_readiness": gate_status("phase_b_mainline_readiness_check.json", "mainline_readiness_status"),
        "external_review_result": gate_status("phase_b_external_review_result_check.json", "external_review_status"),
        "pro_review_prompt": gate_status("phase_b_pro_review_prompt_check.json", "prompt_status"),
    }
    positive_value_confirmed = all(retrieval["positive_checks"].values())
    no_boundary_leak = (
        int(promotion.get("promotion_allowed_count") or 0) == 0
        and int(promotion.get("action_basis_allowed_count") or 0) == 0
        and int(promotion.get("evidence_sufficiency_passed_count") or 0) == 0
        and int(promotion.get("formal_writeback_allowed_count") or 0) == 0
        and int(promotion.get("truth_confidence_change_allowed_count") or 0) == 0
        and int(promotion.get("reviewed_relation_creation_allowed_count") or 0) == 0
        and int(promotion.get("blocked_gate_count") or -1) == int(promotion.get("gate_record_count") or -2)
    )
    return {
        "artifact_kind": "vaks_phase_b_keep_stop_synthesis",
        "built_at": built_at,
        "compared_against_previous_version": "phase_b_promotion_gate_sufficiency_block",
        "keep_stop_decision": "keep_phase_b_as_sandbox_candidate",
        "positive_value_confirmed": positive_value_confirmed,
        "no_boundary_leak_confirmed": no_boundary_leak,
        "plain_language_decision": (
            "Keep the VAKS-wrapped Yuxi-like retrieval adapter as a sandbox and documentation candidate; "
            "do not promote original Yuxi runtime, C-lite, writeback, or action use yet."
        ),
        "documentation_patch_scope": APPROVED_DOC_SCOPE,
        "changed_core_docs_observed": minimal_doc.get("changed_core_docs"),
        "mainline_status": "documentation_only_patch_validated_not_committed",
        "runtime_status": "original_yuxi_full_stack_unvalidated_docker_unavailable",
        "original_yuxi_runtime_validated": False,
        "reject_full_runtime_adoption": True,
        "runtime_adoption_allowed": False,
        "c_lite_allowed": False,
        "skills_mcp_subagents_allowed": False,
        "formal_writeback_allowed": False,
        "promotion_allowed_count": int(promotion.get("promotion_allowed_count") or 0),
        "action_basis_allowed_count": int(promotion.get("action_basis_allowed_count") or 0),
        "action_ready_count": int(promotion.get("action_ready_count") or 0),
        "evidence_packet_created_count": int(promotion.get("evidence_packet_created_count") or 0),
        "evidence_packet_allowed_count": int(promotion.get("evidence_packet_allowed_count") or 0),
        "evidence_sufficiency_passed_count": int(promotion.get("evidence_sufficiency_passed_count") or 0),
        "automatic_promotion_allowed_count": int(promotion.get("automatic_promotion_allowed_count") or 0),
        "truth_confidence_change_allowed_count": int(promotion.get("truth_confidence_change_allowed_count") or 0),
        "reviewed_relation_creation_allowed_count": int(promotion.get("reviewed_relation_creation_allowed_count") or 0),
        "retrieval_evidence": retrieval,
        "pipeline_counts": {
            "context_pack_count": context_pack.get("pack_count"),
            "context_pack_action_basis_allowed_count": context_pack.get("action_basis_allowed_count"),
            "evidence_envelope_count": envelope.get("envelope_count"),
            "support_check_count": support.get("support_check_count"),
            "evidence_item_count": support.get("evidence_item_count"),
            "source_span_available_count": support.get("source_span_available_count"),
            "pre_refresh_needed_count": support.get("source_refresh_needed_count"),
            "post_refresh_needed_count": refreshed.get("source_refresh_needed_count"),
            "pre_refresh_mismatch_count": source_refresh.get("pre_refresh_mismatch_count"),
            "post_refresh_mismatch_count": source_refresh.get("post_refresh_mismatch_count"),
            "refreshed_item_count": source_refresh.get("refreshed_item_count"),
            "current_source_hash_match_count": refreshed.get("current_source_hash_match_count"),
            "review_packet_count": review_queue.get("review_packet_count"),
            "open_packet_count": review_queue.get("open_packet_count"),
            "blocked_no_source_anchor_count": review_queue.get("blocked_no_source_anchor_count"),
            "simulated_packet_count": simulated.get("simulated_packet_count"),
            "simulated_support_like_count": promotion.get("simulated_support_like_count"),
            "blocked_gate_count": promotion.get("blocked_gate_count"),
            "gate_record_count": promotion.get("gate_record_count"),
        },
        "runtime_environment": {
            "docker_path": (runtime.get("environment") or {}).get("docker_path"),
            "runtime_feasibility_status": runtime.get("runtime_feasibility_status"),
        },
        "prior_gates": prior_gates,
        "allowed_next_steps": [
            "commit_validated_four_file_documentation_patch_after_user_approval",
            "run_original_yuxi_full_stack_only_after_docker_or_remote_runner_exists",
            "design_next_sandbox_gate_before_any_c_lite_or_runtime_default",
        ],
        "hard_stops": [
            "do_not_claim_original_yuxi_runtime_validated",
            "do_not_promote_to_c_lite",
            "do_not_attach_skills_mcp_subagents_or_writeback",
            "do_not_create_evidence_packet_or_action_basis_from_simulation",
            "do_not_treat_graph_or_vector_rank_as_evidence_support",
            "do_not_change_truth_confidence_or_reviewed_relations",
        ],
    }


def write_packet(synthesis: dict) -> None:
    main_primary = synthesis["retrieval_evidence"]["main_pressure"]["primary"]
    main_full = synthesis["retrieval_evidence"]["main_pressure"]["full"]
    holdout_primary = synthesis["retrieval_evidence"]["holdout_pressure"]["primary"]
    holdout_full = synthesis["retrieval_evidence"]["holdout_pressure"]["full"]
    counts = synthesis["pipeline_counts"]
    lines = [
        "---",
        "record_kind: sandbox_keep_stop_synthesis_packet",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: keep_stop_synthesis_not_runtime_adoption",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Keep / Stop Synthesis Packet",
        "",
        "## Decision",
        "",
        "```text",
        f"keep_stop_decision: {synthesis['keep_stop_decision']}",
        f"positive_value_confirmed: {str(synthesis['positive_value_confirmed']).lower()}",
        f"no_boundary_leak_confirmed: {str(synthesis['no_boundary_leak_confirmed']).lower()}",
        f"mainline_status: {synthesis['mainline_status']}",
        f"runtime_status: {synthesis['runtime_status']}",
        "```",
        "",
        "Plain language:",
        "",
        "```text",
        synthesis["plain_language_decision"],
        "```",
        "",
        "## Compared Against Previous Version",
        "",
        "Previous version:",
        "",
        "```text",
        "promotion-gate / sufficiency-block sandbox",
        "```",
        "",
        "This synthesis adds:",
        "",
        "```text",
        "whole-chain keep/stop judgment",
        "retrieval value + governance safety in one decision",
        "explicit stop list for runtime, C-lite, writeback, and action basis",
        "```",
        "",
        "It preserves:",
        "",
        "```text",
        f"promotion_allowed_count: {synthesis['promotion_allowed_count']}",
        f"action_basis_allowed_count: {synthesis['action_basis_allowed_count']}",
        f"evidence_packet_created_count: {synthesis['evidence_packet_created_count']}",
        f"evidence_sufficiency_passed_count: {synthesis['evidence_sufficiency_passed_count']}",
        f"formal_writeback_allowed: {str(synthesis['formal_writeback_allowed']).lower()}",
        f"truth_confidence_change_allowed_count: {synthesis['truth_confidence_change_allowed_count']}",
        f"reviewed_relation_creation_allowed_count: {synthesis['reviewed_relation_creation_allowed_count']}",
        "```",
        "",
        "## Retrieval Value",
        "",
        "Main pressure set:",
        "",
        "```text",
        f"primary baseline hit@5: {main_primary['baseline_file_lexical']['hit_at_5']}",
        f"primary VAKS+B skeleton hit@5: {main_primary['vaks_b_adapter_skeleton']['hit_at_5']}",
        f"primary baseline MRR: {main_primary['baseline_file_lexical']['mrr']}",
        f"primary VAKS+B skeleton MRR: {main_primary['vaks_b_adapter_skeleton']['mrr']}",
        f"full baseline hit@5: {main_full['baseline_file_lexical']['hit_at_5']}",
        f"full VAKS+B skeleton hit@5: {main_full['vaks_b_adapter_skeleton']['hit_at_5']}",
        f"full baseline MRR: {main_full['baseline_file_lexical']['mrr']}",
        f"full VAKS+B skeleton MRR: {main_full['vaks_b_adapter_skeleton']['mrr']}",
        "```",
        "",
        "Holdout pressure set:",
        "",
        "```text",
        f"primary baseline hit@5: {holdout_primary['baseline_file_lexical']['hit_at_5']}",
        f"primary VAKS+B skeleton hit@5: {holdout_primary['vaks_b_adapter_skeleton']['hit_at_5']}",
        f"primary baseline MRR: {holdout_primary['baseline_file_lexical']['mrr']}",
        f"primary VAKS+B skeleton MRR: {holdout_primary['vaks_b_adapter_skeleton']['mrr']}",
        f"full baseline hit@5: {holdout_full['baseline_file_lexical']['hit_at_5']}",
        f"full VAKS+B skeleton hit@5: {holdout_full['vaks_b_adapter_skeleton']['hit_at_5']}",
        f"full baseline MRR: {holdout_full['baseline_file_lexical']['mrr']}",
        f"full VAKS+B skeleton MRR: {holdout_full['vaks_b_adapter_skeleton']['mrr']}",
        "```",
        "",
        "## Governance Value",
        "",
        "```text",
        "main primary Yuxi-native action leakage: "
        f"{main_primary['yuxi_native_profile']['action_leakage_rate']}",
        "main primary VAKS+B action leakage: "
        f"{main_primary['vaks_b_adapter_skeleton']['action_leakage_rate']}",
        "main full Yuxi-native action leakage: "
        f"{main_full['yuxi_native_profile']['action_leakage_rate']}",
        "main full VAKS+B action leakage: "
        f"{main_full['vaks_b_adapter_skeleton']['action_leakage_rate']}",
        "holdout primary Yuxi-native action leakage: "
        f"{holdout_primary['yuxi_native_profile']['action_leakage_rate']}",
        "holdout primary VAKS+B action leakage: "
        f"{holdout_primary['vaks_b_adapter_skeleton']['action_leakage_rate']}",
        "holdout full Yuxi-native action leakage: "
        f"{holdout_full['yuxi_native_profile']['action_leakage_rate']}",
        "holdout full VAKS+B action leakage: "
        f"{holdout_full['vaks_b_adapter_skeleton']['action_leakage_rate']}",
        "```",
        "",
        "## Chain Evidence",
        "",
        "```text",
        f"context packs: {counts['context_pack_count']}",
        f"evidence envelopes: {counts['evidence_envelope_count']}",
        f"support checks: {counts['support_check_count']}",
        f"evidence items: {counts['evidence_item_count']}",
        f"source spans available: {counts['source_span_available_count']}",
        f"source refresh needed before refresh: {counts['pre_refresh_needed_count']}",
        f"source refresh needed after refresh: {counts['post_refresh_needed_count']}",
        f"hash mismatches before refresh: {counts['pre_refresh_mismatch_count']}",
        f"hash mismatches after refresh: {counts['post_refresh_mismatch_count']}",
        f"review packets: {counts['review_packet_count']}",
        f"open review packets: {counts['open_packet_count']}",
        f"blocked no-anchor packets: {counts['blocked_no_source_anchor_count']}",
        f"simulated support-like item outcomes: {counts['simulated_support_like_count']}",
        f"blocked promotion gates: {counts['blocked_gate_count']} / {counts['gate_record_count']}",
        "```",
        "",
        "## Hard Stops",
        "",
        "```text",
        *synthesis["hard_stops"],
        "```",
        "",
        "## Next Step",
        "",
        "```text",
        "Either commit the validated four-file documentation patch with user approval,",
        "or provide a Docker/remote runner for original Yuxi full-stack testing.",
        "Do not start C-lite or runtime adoption from this packet alone.",
        "```",
        "",
    ]
    PACKET_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_decision(synthesis: dict) -> None:
    counts = synthesis["pipeline_counts"]
    lines = [
        "---",
        "record_kind: sandbox_iteration_decision",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: keep_stop_synthesis_not_runtime_adoption",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Keep / Stop Synthesis Decision",
        "",
        "## Decision",
        "",
        "Keep Phase B as a positive sandbox and documentation candidate only.",
        "",
        "Do not promote it to runtime/default adoption, C-lite, original Yuxi parity,",
        "Skills/MCP/subagent execution, formal writeback, Evidence Packet, or action basis.",
        "",
        "## Compared Against Previous Version",
        "",
        "Previous version: promotion-gate / sufficiency-block sandbox.",
        "",
        "This step adds whole-chain synthesis and does not add any new authority.",
        "",
        "## Result",
        "",
        "```text",
        f"positive_value_confirmed: {str(synthesis['positive_value_confirmed']).lower()}",
        f"no_boundary_leak_confirmed: {str(synthesis['no_boundary_leak_confirmed']).lower()}",
        f"promotion_allowed_count: {synthesis['promotion_allowed_count']}",
        f"action_basis_allowed_count: {synthesis['action_basis_allowed_count']}",
        f"evidence_sufficiency_passed_count: {synthesis['evidence_sufficiency_passed_count']}",
        f"formal_writeback_allowed: {str(synthesis['formal_writeback_allowed']).lower()}",
        f"original_yuxi_runtime_validated: {str(synthesis['original_yuxi_runtime_validated']).lower()}",
        f"runtime_adoption_allowed: {str(synthesis['runtime_adoption_allowed']).lower()}",
        f"c_lite_allowed: {str(synthesis['c_lite_allowed']).lower()}",
        f"blocked promotion gates: {counts['blocked_gate_count']} / {counts['gate_record_count']}",
        f"source refresh needed: {counts['pre_refresh_needed_count']} -> {counts['post_refresh_needed_count']}",
        f"current source hash matches: {counts['current_source_hash_match_count']}",
        "```",
        "",
        "## Next Step",
        "",
        "The next safe step is a user-approved commit of the validated four-file",
        "documentation patch, or a separate original-Yuxi runtime test once Docker",
        "or a remote runner exists.",
        "",
    ]
    DECISION_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    synthesis = build_synthesis()
    SYNTHESIS_PATH.write_text(json.dumps(synthesis, ensure_ascii=False, indent=2), encoding="utf-8")
    write_packet(synthesis)
    write_decision(synthesis)
    print(f"keep_stop_decision: {synthesis['keep_stop_decision']}")
    print(f"positive_value_confirmed: {synthesis['positive_value_confirmed']}")
    print(f"no_boundary_leak_confirmed: {synthesis['no_boundary_leak_confirmed']}")


if __name__ == "__main__":
    main()
