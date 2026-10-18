#!/usr/bin/env python3
"""VAKS Adaptive Assurance Routing R0.6 dry-run.

This is a sandbox-only deterministic router. It produces runtime route
contracts and evidence-transition decisions; it does not run production
retrieval, does not assess truth, and does not grant action readiness.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CONTRACT_VERSION = "r0.6"
RUN_ID = "vaks-adaptive-assurance-routing-r0-6-2026-06-23"
DEFAULT_OUTPUT_DIR = Path("outputs/review") / RUN_ID

QUERY_MODES = {"orientation", "source_inspection", "review", "action"}
EXPERIENCE_PRESETS = {"auto", "fast", "standard", "strict"}
RISK_LEVELS = {"low", "medium", "high"}
COMPLEXITY_HINTS = {"simple", "complex", "deep", "unknown"}
RETRIEVAL_EFFORTS = {"minimal", "expanded", "deep"}
ASSURANCE_PROFILES = {"light", "grounded", "strict"}

PROFILE_ORDER = {"fast": 0, "standard": 1, "strict": 2}
ASSURANCE_ORDER = {"light": 0, "grounded": 1, "strict": 2}
ASSURANCE_BY_PROFILE = {"fast": "light", "standard": "grounded", "strict": "strict"}
PROFILE_BY_ASSURANCE = {"light": "fast", "grounded": "standard", "strict": "strict"}
QUERY_MODE_PROFILE_FLOOR = {
    "orientation": "fast",
    "source_inspection": "fast",
    "review": "standard",
    "action": "strict",
}

STRICT_DOMAINS = {"legal", "compliance", "finance", "hr", "security"}
GROUNDED_USES = {
    "internal_factual_answer",
    "technical_conclusion",
    "project_judgment",
    "enterprise_knowledge_answer",
    "research_comparison",
}
STRICT_FLAGS = {
    "explicit_challenge",
    "decision_use",
    "promotion_use",
    "strong_relation_use",
    "action_basis_requested",
    "action_use_requested",
    "high_impact_use",
}

RESPONSE_RULES = {
    "fully_supported": "direct",
    "partially_supported": "qualified",
    "scope_limited": "qualified",
    "missing_anchor": "abstain",
    "unresolved_conflict_low_risk": "qualified",
    "unresolved_conflict_high_risk": "review",
    "stale_or_superseded": "review",
    "candidate_only": "abstain",
}

NOT_PROVEN = [
    "routing_optimality",
    "production_latency",
    "production_runtime",
    "source_intake_p0",
    "reviewed_truth",
    "action_readiness",
]

AUTHORITY_BOUNDARY = {
    "runtime_only": True,
    "changes_truth": False,
    "changes_review_status": False,
    "changes_confidence": False,
    "grants_action_readiness": False,
}


@dataclass(frozen=True)
class RouteResult:
    case_id: str
    decision: dict[str, Any]
    error: dict[str, Any] | None = None


def profile_max(left: str, right: str) -> str:
    return left if PROFILE_ORDER[left] >= PROFILE_ORDER[right] else right


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def route_decision_hash(binding: dict[str, Any]) -> str:
    payload = {
        "contract_version": CONTRACT_VERSION,
        "route_decision_id": binding["route_decision_id"],
        "query_mode": binding["query_mode"],
        "assurance_profile": binding["assurance_profile"],
        "assurance_floor": binding["assurance_floor"],
        "retrieval_effort": binding["retrieval_effort"],
        "risk_level": binding["risk_level"],
        "max_auto_escalations": binding["max_auto_escalations"],
    }
    return sha256_text(stable_json(payload))


def route_binding(
    *,
    route_decision_id: str,
    query_mode: str,
    assurance_profile: str,
    assurance_floor: str,
    retrieval_effort: str,
    risk_level: str,
    max_auto_escalations: int = 1,
) -> dict[str, Any]:
    binding = {
        "route_decision_id": route_decision_id,
        "query_mode": query_mode,
        "assurance_profile": assurance_profile,
        "assurance_floor": assurance_floor,
        "retrieval_effort": retrieval_effort,
        "risk_level": risk_level,
        "max_auto_escalations": max_auto_escalations,
    }
    return {**binding, "route_decision_hash": route_decision_hash(binding)}


def contains_key(data: Any, key: str) -> bool:
    if isinstance(data, dict):
        return key in data or any(contains_key(value, key) for value in data.values())
    if isinstance(data, list):
        return any(contains_key(value, key) for value in data)
    return False


def validate_route_case(case: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ["case_id", "query", "query_mode", "intended_use", "risk_level"]:
        if field not in case or case[field] in (None, ""):
            errors.append(f"missing_required_field:{field}")
    query_mode = case.get("query_mode")
    if query_mode is not None and query_mode not in QUERY_MODES:
        errors.append(f"invalid_query_mode:{query_mode}")
    risk_level = case.get("risk_level")
    if risk_level is not None and risk_level not in RISK_LEVELS:
        errors.append(f"invalid_risk_level:{risk_level}")
    preset = case.get("experience_preset", "auto")
    if preset is not None and preset not in EXPERIENCE_PRESETS:
        errors.append(f"invalid_experience_preset:{preset}")
    complexity = case.get("complexity_hint", "unknown")
    if complexity is not None and complexity not in COMPLEXITY_HINTS:
        errors.append(f"invalid_complexity_hint:{complexity}")
    flags = case.get("flags", {})
    if flags is not None and not isinstance(flags, dict):
        errors.append("invalid_flags:not_object")
    return errors


def floor_profile(case: dict[str, Any]) -> tuple[str, list[str]]:
    query_mode = str(case["query_mode"])
    risk_level = str(case["risk_level"])
    intended_use = str(case.get("intended_use", ""))
    risk_domain = str(case.get("risk_domain", ""))
    flags = case.get("flags") or {}

    profile = QUERY_MODE_PROFILE_FLOOR[query_mode]
    reasons = [f"query_mode_{query_mode}_floor_{profile}"]

    if intended_use in GROUNDED_USES and PROFILE_ORDER[profile] < PROFILE_ORDER["standard"]:
        profile = "standard"
        reasons.append(f"intended_use_{intended_use}_requires_grounded")

    if risk_level == "high":
        profile = profile_max(profile, "strict")
        reasons.append("risk_high_requires_strict")
    elif risk_level == "medium" and profile == "fast" and intended_use in GROUNDED_USES:
        profile = "standard"
        reasons.append("risk_medium_grounded_answer")

    if risk_domain.lower() in STRICT_DOMAINS:
        profile = profile_max(profile, "strict")
        reasons.append(f"domain_{risk_domain.lower()}_requires_strict")

    for flag in sorted(STRICT_FLAGS):
        if bool(flags.get(flag)):
            profile = profile_max(profile, "strict")
            reasons.append(f"flag_{flag}_requires_strict")

    if bool(flags.get("classification_uncertain")) and PROFILE_ORDER[profile] < PROFILE_ORDER["standard"]:
        profile = "standard"
        reasons.append("classification_uncertain_defaults_standard")

    return profile, reasons


def apply_requested_profile(case: dict[str, Any], floor: str) -> tuple[str, dict[str, Any]]:
    requested = case.get("experience_preset", "auto") or "auto"
    if requested == "auto":
        return floor, {"value": "auto", "applied": False, "reason": "auto_uses_policy_floor"}
    if PROFILE_ORDER[requested] < PROFILE_ORDER[floor]:
        return floor, {
            "value": requested,
            "applied": False,
            "reason": "below_assurance_floor",
        }
    if PROFILE_ORDER[requested] > PROFILE_ORDER[floor]:
        return requested, {
            "value": requested,
            "applied": True,
            "reason": "user_requested_stricter_profile",
        }
    return floor, {
        "value": requested,
        "applied": True,
        "reason": "matches_assurance_floor",
    }


def retrieval_effort(case: dict[str, Any]) -> tuple[str, list[str]]:
    flags = case.get("flags") or {}
    complexity = case.get("complexity_hint", "unknown")
    reasons: list[str] = []

    deep_flags = [
        "conflict_expected",
        "multi_hop_required",
        "version_conflict_expected",
        "first_round_missing_anchor",
        "complex_scope_combo",
    ]
    expanded_flags = [
        "multi_condition",
        "comparison",
        "conversation_dependent",
        "query_rewrite_expected",
        "multi_source_required",
    ]

    if complexity == "deep" or any(bool(flags.get(flag)) for flag in deep_flags):
        reasons.append("complexity_deep_or_conflict_requires_deep")
        return "deep", reasons
    if complexity == "complex" or any(bool(flags.get(flag)) for flag in expanded_flags):
        reasons.append("complexity_complex_requires_expanded")
        return "expanded", reasons
    if complexity == "unknown":
        reasons.append("complexity_unknown_defaults_expanded")
        return "expanded", reasons

    reasons.append("query_shape_single_fact_minimal")
    return "minimal", reasons


def budget_for(assurance_profile: str, effort: str) -> dict[str, Any]:
    retrieval_budget = {
        "minimal": {"max_retrieval_rounds": 1, "max_subqueries": 1},
        "expanded": {"max_retrieval_rounds": 2, "max_subqueries": 2},
        "deep": {"max_retrieval_rounds": 2, "max_subqueries": 3},
    }[effort]
    assurance_budget = {
        "light": {"max_verifier_calls": 0, "max_repair_calls": 0, "estimated_cost_level": "low"},
        "grounded": {"max_verifier_calls": 1, "max_repair_calls": 1, "estimated_cost_level": "medium"},
        "strict": {"max_verifier_calls": 1, "max_repair_calls": 1, "estimated_cost_level": "high"},
    }[assurance_profile]
    return {
        **retrieval_budget,
        **assurance_budget,
        "max_auto_escalations": 1,
    }


def required_artifacts(assurance_profile: str) -> list[str]:
    base = ["query_policy", "retrieval_receipt", "context_pack"]
    if assurance_profile == "light":
        return base
    standard = base + ["claim_support_map", "sufficiency_summary", "answer_use", "guard_report"]
    if assurance_profile == "grounded":
        return standard
    return standard + ["evidence_gap_or_conflict_report", "review_handoff_if_needed"]


def guard_plan(assurance_profile: str, flags: dict[str, Any]) -> list[dict[str, str]]:
    guards = [
        {
            "guard": "retrieval_receipt",
            "trigger": "after_retrieval",
            "purpose": "retrieval receipt process contract",
        },
        {
            "guard": "runtime_artifacts",
            "trigger": "before_context_pack",
            "purpose": "runtime artifact exclusion contract",
        },
    ]
    if assurance_profile in {"grounded", "strict"}:
        guards.extend(
            [
                {
                    "guard": "support_boundary",
                    "trigger": "when_claim_support_map_exists",
                    "purpose": "support authority bucket contract",
                },
                {
                    "guard": "body_hash",
                    "trigger": "if_source_body_or_anchor_is_checked",
                    "purpose": "candidate body hash contract",
                },
            ]
        )
    if assurance_profile == "strict":
        guards.extend(
            [
                {
                    "guard": "support_boundary",
                    "trigger": "when_sufficiency_summary_exists",
                    "purpose": "evidence sufficiency boundary consistency via support boundary",
                },
            ]
        )
    if bool(flags.get("action_facing_object_exists")):
        guards.append(
            {
                "guard": "action_readiness",
                "trigger": "only_if_action_facing_object_exists",
                "purpose": "action readiness consistency contract",
            }
        )
    if bool(flags.get("operation_is_proposed")):
        guards.append(
            {
                "guard": "operation_receipt",
                "trigger": "only_if_operation_is_proposed",
                "purpose": "operation receipt process contract",
            }
        )
    return guards


def route_case(case: dict[str, Any]) -> RouteResult:
    errors = validate_route_case(case)
    case_id = str(case.get("case_id", "unknown-case"))
    if errors:
        return RouteResult(
            case_id=case_id,
            decision={
                "case_id": case_id,
                "contract_version": CONTRACT_VERSION,
                "status": "error",
                "errors": errors,
                "error_policy": "invalid_input_fail_closed",
            },
            error={"case_id": case_id, "errors": errors},
        )

    floor, floor_reasons = floor_profile(case)
    resolved_preset, requested = apply_requested_profile(case, floor)
    effort, effort_reasons = retrieval_effort(case)
    assurance_floor = ASSURANCE_BY_PROFILE[floor]
    assurance_profile = ASSURANCE_BY_PROFILE[resolved_preset]
    flags = case.get("flags") or {}

    reasons = floor_reasons + effort_reasons
    if requested["value"] != "auto":
        reasons.append(f"requested_profile_{requested['value']}_{requested['reason']}")

    decision = {
        "decision_id": f"route-{case_id}",
        "case_id": case_id,
        "contract_version": CONTRACT_VERSION,
        "status": "ok",
        "query": case["query"],
        "query_mode": case["query_mode"],
        "experience_preset": case.get("experience_preset", "auto") or "auto",
        "resolved_experience_preset": resolved_preset,
        "retrieval_effort": effort,
        "assurance_profile": assurance_profile,
        "assurance_floor": assurance_floor,
        "answer_policy": "pending_evidence",
        "reason_codes": reasons,
        "requested_profile": requested,
        "experience_floor": floor,
        "policy_floor_enforced": True,
        "downgrade_allowed": False,
        "budget": budget_for(assurance_profile, effort),
        "response_rules": RESPONSE_RULES,
        "required_artifacts": required_artifacts(assurance_profile),
        "guard_plan": guard_plan(assurance_profile, flags),
        "authority_boundary": AUTHORITY_BOUNDARY,
        "not_proven": NOT_PROVEN,
        "input_summary": {
            "intended_use": case["intended_use"],
            "risk_level": case["risk_level"],
            "risk_domain": case.get("risk_domain", "general"),
            "complexity_hint": case.get("complexity_hint", "unknown"),
            "flags": flags,
        },
    }
    return RouteResult(case_id=case_id, decision=decision)


def transition_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case.get("case_id", "unknown-transition"))
    route_id = str(case.get("route_decision_id", "missing-route-decision-id"))
    signals = case.get("evidence_signals", {})
    errors: list[str] = []

    for field in [
        "route_decision_id",
        "route_decision_hash",
        "query_mode",
        "assurance_profile",
        "assurance_floor",
        "retrieval_effort",
        "risk_level",
        "auto_escalations_used",
        "max_auto_escalations",
    ]:
        if field not in case:
            errors.append(f"missing_required_field:{field}")

    if not isinstance(signals, dict):
        errors.append("invalid_evidence_signals:not_object")
        signals = {}

    current_assurance = case.get("assurance_profile")
    current_effort = case.get("retrieval_effort")
    assurance_floor = case.get("assurance_floor")
    risk_level = case.get("risk_level")
    used = case.get("auto_escalations_used")
    max_escalations = case.get("max_auto_escalations")

    if case.get("query_mode") not in QUERY_MODES:
        errors.append(f"invalid_query_mode:{case.get('query_mode')}")
    if current_assurance not in ASSURANCE_PROFILES:
        errors.append(f"invalid_assurance_profile:{current_assurance}")
    if assurance_floor not in ASSURANCE_PROFILES:
        errors.append(f"invalid_assurance_floor:{assurance_floor}")
    if current_effort not in RETRIEVAL_EFFORTS:
        errors.append(f"invalid_retrieval_effort:{current_effort}")
    if risk_level not in RISK_LEVELS:
        errors.append(f"invalid_risk_level:{risk_level}")
    if not isinstance(used, int) or used not in {0, 1}:
        errors.append(f"invalid_auto_escalations_used:{used}")
    if not isinstance(max_escalations, int) or max_escalations != 1:
        errors.append(f"invalid_max_auto_escalations:{max_escalations}")
    if current_assurance in ASSURANCE_PROFILES and assurance_floor in ASSURANCE_PROFILES:
        if ASSURANCE_ORDER[current_assurance] < ASSURANCE_ORDER[assurance_floor]:
            errors.append("assurance_profile_below_floor")

    hash_fields_present = all(
        field in case
        for field in [
            "route_decision_id",
            "query_mode",
            "assurance_profile",
            "assurance_floor",
            "retrieval_effort",
            "risk_level",
            "max_auto_escalations",
        ]
    )
    if hash_fields_present:
        expected_hash = route_decision_hash(case)
        if case.get("route_decision_hash") != expected_hash:
            errors.append("route_decision_hash_mismatch")

    if errors:
        return {
            "transition_id": f"transition-{case_id}",
            "case_id": case_id,
            "contract_version": CONTRACT_VERSION,
            "status": "error",
            "route_decision_id": route_id,
            "route_decision_hash": case.get("route_decision_hash"),
            "errors": errors,
            "error_policy": "invalid_input_fail_closed",
            "authority_boundary": AUTHORITY_BOUNDARY,
            "not_proven": NOT_PROVEN,
        }

    # From this point, validation has proven the route binding and counters.
    current_assurance = str(current_assurance)
    current_effort = str(current_effort)
    risk_level = str(risk_level)
    used = int(used)
    max_escalations = int(max_escalations)
    remaining = max(0, max_escalations - used)

    independent_anchor = bool(
        signals.get("independent_anchor_present", signals.get("independent_anchor", False))
    )
    candidate_only = bool(signals.get("candidate_only"))
    authority_allowed = signals.get("authority_allowed")
    disallowed_authority = bool(signals.get("disallowed_authority"))
    support_result = signals.get("support_result")
    coverage_extent = signals.get("coverage_extent")
    conflict_state = signals.get("conflict_state")
    scope_fit = signals.get("scope_fit")
    temporal_fit = signals.get("temporal_fit")
    unresolved_conflict = bool(signals.get("unresolved_conflict")) or conflict_state == "unresolved"
    stale_or_superseded = bool(
        signals.get("stale_or_superseded") or signals.get("stale") or signals.get("superseded")
    ) or temporal_fit in {"stale", "superseded"}
    scope_limited = bool(signals.get("scope_limited")) or scope_fit == "limited" or support_result == "scope_limited"
    partial_support = bool(signals.get("partial_support")) or coverage_extent == "partial" or support_result == "weak"
    explicit_direct_fields = {
        "independent_anchor_present",
        "authority_allowed",
        "support_result",
        "coverage_extent",
        "conflict_state",
        "scope_fit",
        "temporal_fit",
    }
    missing_direct_fields = sorted(field for field in explicit_direct_fields if field not in signals)

    action = "keep"
    final_policy = "direct"
    to_effort = current_effort
    to_assurance = current_assurance
    assurance_changed = False
    reason_codes: list[str] = []

    contradictory_states = []
    if candidate_only and independent_anchor:
        contradictory_states.append("candidate_only_with_independent_anchor")
    if support_result == "supported" and not independent_anchor:
        contradictory_states.append("supported_without_independent_anchor")
    if coverage_extent == "full" and not independent_anchor:
        contradictory_states.append("full_coverage_without_independent_anchor")

    if contradictory_states:
        action = "error"
        final_policy = "abstain"
        reason_codes.extend(contradictory_states)
    elif candidate_only or disallowed_authority or authority_allowed is False:
        if remaining > 0 and current_effort == "minimal":
            action = "escalate_once"
            final_policy = "pending_evidence"
            to_effort = "expanded"
            reason_codes.append("candidate_or_disallowed_authority_escalate_once")
        else:
            action = "abstain"
            final_policy = "abstain"
            reason_codes.append("candidate_or_disallowed_authority_abstain")
    elif not independent_anchor:
        if remaining > 0 and current_effort == "minimal":
            action = "escalate_once"
            final_policy = "pending_evidence"
            to_effort = "expanded"
            reason_codes.append("missing_anchor_escalate_once")
        else:
            action = "abstain"
            final_policy = "abstain"
            reason_codes.append("missing_anchor_abstain")
    elif stale_or_superseded:
        action = "review"
        final_policy = "review"
        reason_codes.append("stale_or_superseded_review")
    elif unresolved_conflict:
        all_sides_anchored = bool(signals.get("conflict_all_sides_have_allowed_anchor"))
        if risk_level == "high":
            action = "review"
            final_policy = "review"
            reason_codes.append("unresolved_conflict_high_risk_review")
        elif all_sides_anchored:
            action = "qualify"
            final_policy = "qualified"
            reason_codes.append("unresolved_conflict_low_risk_anchored_qualified")
        else:
            action = "review"
            final_policy = "review"
            reason_codes.append("unresolved_conflict_without_full_anchors_review")
    elif scope_limited:
        action = "qualify"
        final_policy = "qualified"
        reason_codes.append("scope_limited_qualified")
    elif partial_support:
        action = "qualify"
        final_policy = "qualified"
        reason_codes.append("partial_support_qualified")
    elif missing_direct_fields:
        action = "assess_support"
        final_policy = "pending_evidence"
        reason_codes.append("direct_required_fields_missing:" + ",".join(missing_direct_fields))
    elif (
        support_result == "supported"
        and coverage_extent == "full"
        and conflict_state == "none"
        and scope_fit == "matched"
        and temporal_fit == "current"
        and authority_allowed is True
    ):
        action = "keep"
        final_policy = "direct"
        reason_codes.append("fully_supported_full_coverage_direct")
    else:
        action = "assess_support"
        final_policy = "pending_evidence"
        reason_codes.append("anchor_present_support_not_assessed")

    if action == "escalate_once":
        used_after = used + 1
    else:
        used_after = used
    remaining_after = max(0, max_escalations - used_after)

    return {
        "transition_id": f"transition-{case['case_id']}",
        "case_id": case["case_id"],
        "contract_version": CONTRACT_VERSION,
        "status": "error" if action == "error" else "ok",
        "route_decision_id": case["route_decision_id"],
        "route_decision_hash": case["route_decision_hash"],
        "query_mode": case["query_mode"],
        "assurance_floor": case["assurance_floor"],
        "evidence_signals": signals,
        "transition": {
            "action": action,
            "from_retrieval_effort": current_effort,
            "to_retrieval_effort": to_effort,
            "from_assurance_profile": current_assurance,
            "to_assurance_profile": to_assurance,
            "assurance_profile_changed": assurance_changed,
            "reason_codes": reason_codes,
        },
        "auto_escalations_used": used_after,
        "auto_escalations_remaining": remaining_after,
        **({"errors": reason_codes} if action == "error" else {}),
        "if_still_missing": {"final_answer_policy": "abstain"},
        "final_answer_policy": final_policy,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "not_proven": NOT_PROVEN,
    }


def routing_cases() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "R001",
            "query": "Where is the source anchor template?",
            "query_mode": "orientation",
            "intended_use": "casual_lookup",
            "risk_level": "low",
            "risk_domain": "general",
            "experience_preset": "auto",
            "complexity_hint": "simple",
            "flags": {},
            "expected_resolved_experience_preset": "fast",
            "expected_retrieval_effort": "minimal",
        },
        {
            "case_id": "R002",
            "query": "Compare GraphRAG, LightRAG, and HippoRAG for VAKS context activation.",
            "query_mode": "orientation",
            "intended_use": "research_comparison",
            "risk_level": "low",
            "risk_domain": "research",
            "experience_preset": "auto",
            "complexity_hint": "deep",
            "flags": {"comparison": True, "multi_source_required": True},
            "expected_resolved_experience_preset": "standard",
            "expected_retrieval_effort": "deep",
        },
        {
            "case_id": "R003",
            "query": "Inspect the raw W3C Web Annotation source anchor.",
            "query_mode": "source_inspection",
            "intended_use": "source_lookup",
            "risk_level": "low",
            "risk_domain": "general",
            "experience_preset": "auto",
            "complexity_hint": "simple",
            "flags": {},
            "expected_resolved_experience_preset": "fast",
            "expected_retrieval_effort": "minimal",
        },
        {
            "case_id": "R004",
            "query": "Can this raw anchor support the TextQuoteSelector source-anchor claim?",
            "query_mode": "review",
            "intended_use": "internal_factual_answer",
            "risk_level": "medium",
            "risk_domain": "general",
            "experience_preset": "auto",
            "complexity_hint": "simple",
            "flags": {},
            "expected_resolved_experience_preset": "standard",
            "expected_retrieval_effort": "minimal",
        },
        {
            "case_id": "R005",
            "query": "Challenge whether PROV traceability can be treated as evidence support.",
            "query_mode": "review",
            "intended_use": "technical_conclusion",
            "risk_level": "medium",
            "risk_domain": "general",
            "experience_preset": "auto",
            "complexity_hint": "simple",
            "flags": {"explicit_challenge": True},
            "expected_resolved_experience_preset": "strict",
            "expected_retrieval_effort": "minimal",
        },
        {
            "case_id": "R006",
            "query": "Can a China sales employee expense a client dinner under current policy?",
            "query_mode": "action",
            "intended_use": "action_basis_candidate",
            "risk_level": "high",
            "risk_domain": "finance",
            "experience_preset": "auto",
            "complexity_hint": "simple",
            "flags": {"action_basis_requested": True},
            "expected_resolved_experience_preset": "strict",
            "expected_retrieval_effort": "minimal",
        },
        {
            "case_id": "R007",
            "query": "Resolve conflicting HR policy versions for remote-work exceptions.",
            "query_mode": "action",
            "intended_use": "action_basis_candidate",
            "risk_level": "high",
            "risk_domain": "hr",
            "experience_preset": "auto",
            "complexity_hint": "deep",
            "flags": {"conflict_expected": True, "version_conflict_expected": True},
            "expected_resolved_experience_preset": "strict",
            "expected_retrieval_effort": "deep",
        },
        {
            "case_id": "R008",
            "query": "Give me the action-ready answer, but keep it fast.",
            "query_mode": "action",
            "intended_use": "action_basis_candidate",
            "risk_level": "high",
            "risk_domain": "legal",
            "experience_preset": "fast",
            "complexity_hint": "simple",
            "flags": {"action_basis_requested": True},
            "expected_resolved_experience_preset": "strict",
            "expected_retrieval_effort": "minimal",
            "expected_requested_applied": False,
        },
        {
            "case_id": "R009",
            "query": "Where did the fast/standard/strict idea come from?",
            "query_mode": "orientation",
            "intended_use": "casual_lookup",
            "risk_level": "low",
            "risk_domain": "general",
            "experience_preset": "strict",
            "complexity_hint": "simple",
            "flags": {},
            "expected_resolved_experience_preset": "strict",
            "expected_retrieval_effort": "minimal",
            "expected_requested_applied": True,
        },
        {
            "case_id": "R010",
            "query": "Classify this vague internal question.",
            "query_mode": "orientation",
            "intended_use": "unknown_internal_answer",
            "risk_level": "medium",
            "risk_domain": "general",
            "experience_preset": "auto",
            "complexity_hint": "unknown",
            "flags": {"classification_uncertain": True},
            "expected_resolved_experience_preset": "standard",
            "expected_retrieval_effort": "expanded",
        },
        {
            "case_id": "R011",
            "query": "Compare three local retrieval sidecar options for VAKS.",
            "query_mode": "orientation",
            "intended_use": "technical_conclusion",
            "risk_level": "low",
            "risk_domain": "research",
            "experience_preset": "auto",
            "complexity_hint": "deep",
            "flags": {"comparison": True, "multi_source_required": True},
            "expected_resolved_experience_preset": "standard",
            "expected_retrieval_effort": "deep",
        },
        {
            "case_id": "R012",
            "query": "Invalid query mode should fail closed.",
            "query_mode": "decide_now",
            "intended_use": "internal_factual_answer",
            "risk_level": "low",
            "risk_domain": "general",
            "experience_preset": "auto",
            "complexity_hint": "simple",
            "flags": {},
            "expected_error": True,
        },
    ]


def evidence_transition_cases() -> list[dict[str, Any]]:
    def bound(
        route_decision_id: str,
        *,
        query_mode: str = "review",
        assurance_profile: str = "grounded",
        assurance_floor: str = "grounded",
        retrieval_effort: str = "minimal",
        risk_level: str = "medium",
        auto_escalations_used: int = 0,
        max_auto_escalations: int = 1,
    ) -> dict[str, Any]:
        return {
            **route_binding(
                route_decision_id=route_decision_id,
                query_mode=query_mode,
                assurance_profile=assurance_profile,
                assurance_floor=assurance_floor,
                retrieval_effort=retrieval_effort,
                risk_level=risk_level,
                max_auto_escalations=max_auto_escalations,
            ),
            "auto_escalations_used": auto_escalations_used,
        }

    invalid_assurance = {
        "route_decision_id": "route-invalid-assurance",
        "query_mode": "review",
        "assurance_profile": "banana",
        "assurance_floor": "grounded",
        "retrieval_effort": "minimal",
        "risk_level": "medium",
        "max_auto_escalations": 1,
        "auto_escalations_used": 0,
    }
    invalid_assurance["route_decision_hash"] = route_decision_hash(invalid_assurance)
    invalid_effort = {
        "route_decision_id": "route-invalid-effort",
        "query_mode": "review",
        "assurance_profile": "grounded",
        "assurance_floor": "grounded",
        "retrieval_effort": "sideways",
        "risk_level": "medium",
        "max_auto_escalations": 1,
        "auto_escalations_used": 0,
    }
    invalid_effort["route_decision_hash"] = route_decision_hash(invalid_effort)
    negative_used = {
        **bound("route-negative-escalation-used"),
        "auto_escalations_used": -2,
    }
    hash_mismatch = {
        **bound("route-hash-mismatch"),
        "route_decision_hash": "0000badroutehash",
    }

    return [
        {
            "case_id": "E001",
            **bound("route-R0_5_direct_fixture"),
            "fixture_ref": "outputs/review/source-intake-real-readonly-evidence-loop-r0-5-2026-06-23/runs/run-001-direct-support",
            "evidence_signals": {
                "independent_anchor_present": True,
                "authority_allowed": True,
                "support_result": "supported",
                "coverage_extent": "full",
                "conflict_state": "none",
                "scope_fit": "matched",
                "temporal_fit": "current",
            },
            "expected_action": "keep",
            "expected_final_answer_policy": "direct",
        },
        {
            "case_id": "E002",
            **bound("route-R0_5_qualified_fixture"),
            "fixture_ref": "outputs/review/source-intake-real-readonly-evidence-loop-r0-5-2026-06-23/runs/run-002-qualified-partial",
            "evidence_signals": {
                "independent_anchor_present": True,
                "support_result": "weak",
                "coverage_extent": "partial",
                "conflict_state": "none",
                "scope_fit": "matched",
                "temporal_fit": "current",
            },
            "expected_action": "qualify",
            "expected_final_answer_policy": "qualified",
        },
        {
            "case_id": "E003",
            **bound(
                "route-missing-anchor-fast",
                query_mode="orientation",
                assurance_profile="light",
                assurance_floor="light",
                retrieval_effort="minimal",
                risk_level="low",
            ),
            "evidence_signals": {"independent_anchor_present": False},
            "expected_action": "escalate_once",
            "expected_if_still_missing_policy": "abstain",
        },
        {
            "case_id": "E004",
            **bound("route-scope-limited"),
            "evidence_signals": {
                "independent_anchor_present": True,
                "support_result": "scope_limited",
                "coverage_extent": "partial",
                "conflict_state": "none",
                "scope_fit": "limited",
                "temporal_fit": "current",
            },
            "expected_action": "qualify",
            "expected_final_answer_policy": "qualified",
        },
        {
            "case_id": "E005",
            **bound(
                "route-candidate-only",
                query_mode="orientation",
                assurance_profile="light",
                assurance_floor="light",
                retrieval_effort="minimal",
                risk_level="low",
            ),
            "evidence_signals": {"independent_anchor_present": False, "candidate_only": True},
            "expected_action": "escalate_once",
            "expected_if_still_missing_policy": "abstain",
        },
        {
            "case_id": "E006",
            **bound("route-stale"),
            "evidence_signals": {
                "independent_anchor_present": True,
                "support_result": "supported",
                "coverage_extent": "full",
                "conflict_state": "none",
                "scope_fit": "matched",
                "temporal_fit": "stale",
            },
            "expected_action": "review",
            "expected_final_answer_policy": "review",
        },
        {
            "case_id": "E007",
            **bound("route-superseded"),
            "evidence_signals": {
                "independent_anchor_present": True,
                "support_result": "supported",
                "coverage_extent": "full",
                "conflict_state": "none",
                "scope_fit": "matched",
                "temporal_fit": "superseded",
            },
            "expected_action": "review",
            "expected_final_answer_policy": "review",
        },
        {
            "case_id": "E008",
            **bound(
                "route-high-risk-conflict",
                assurance_profile="grounded",
                assurance_floor="grounded",
                retrieval_effort="expanded",
                risk_level="high",
            ),
            "evidence_signals": {
                "independent_anchor_present": True,
                "support_result": "supported",
                "coverage_extent": "full",
                "conflict_state": "unresolved",
                "conflict_all_sides_have_allowed_anchor": True,
                "scope_fit": "matched",
                "temporal_fit": "current",
            },
            "expected_action": "review",
            "expected_final_answer_policy": "review",
        },
        {
            "case_id": "E009",
            **bound("route-anchor-only-no-support-assessment"),
            "evidence_signals": {"independent_anchor_present": True},
            "expected_action": "assess_support",
            "expected_final_answer_policy": "pending_evidence",
        },
        {
            "case_id": "E010",
            **bound("route-partial-without-anchor"),
            "evidence_signals": {
                "independent_anchor_present": False,
                "support_result": "weak",
                "coverage_extent": "partial",
            },
            "expected_action": "escalate_once",
            "expected_if_still_missing_policy": "abstain",
        },
        {
            "case_id": "E011",
            **bound("route-scope-limited-without-anchor"),
            "evidence_signals": {
                "independent_anchor_present": False,
                "support_result": "scope_limited",
                "coverage_extent": "partial",
                "scope_fit": "limited",
            },
            "expected_action": "escalate_once",
            "expected_if_still_missing_policy": "abstain",
        },
        {
            "case_id": "E012",
            **bound("route-low-risk-conflict-without-anchor", risk_level="low"),
            "evidence_signals": {
                "independent_anchor_present": False,
                "conflict_state": "unresolved",
            },
            "expected_action": "escalate_once",
            "expected_if_still_missing_policy": "abstain",
        },
        {
            "case_id": "E013",
            **bound("route-candidate-only-partial"),
            "evidence_signals": {
                "independent_anchor_present": False,
                "candidate_only": True,
                "support_result": "weak",
                "coverage_extent": "partial",
            },
            "expected_action": "escalate_once",
            "expected_if_still_missing_policy": "abstain",
        },
        {
            "case_id": "E014",
            **bound("route-low-risk-conflict-with-all-anchors", risk_level="low"),
            "evidence_signals": {
                "independent_anchor_present": True,
                "support_result": "supported",
                "coverage_extent": "full",
                "conflict_state": "unresolved",
                "conflict_all_sides_have_allowed_anchor": True,
                "scope_fit": "matched",
                "temporal_fit": "current",
            },
            "expected_action": "qualify",
            "expected_final_answer_policy": "qualified",
        },
        {
            "case_id": "E015",
            **bound("route-supported-with-partial-coverage"),
            "evidence_signals": {
                "independent_anchor_present": True,
                "support_result": "supported",
                "coverage_extent": "partial",
                "conflict_state": "none",
                "scope_fit": "matched",
                "temporal_fit": "current",
            },
            "expected_action": "qualify",
            "expected_final_answer_policy": "qualified",
        },
        {
            "case_id": "E016",
            **bound("route-second-missing-anchor", auto_escalations_used=1),
            "evidence_signals": {"independent_anchor_present": False},
            "expected_action": "abstain",
            "expected_final_answer_policy": "abstain",
        },
        {
            "case_id": "E017",
            **invalid_assurance,
            "evidence_signals": {"independent_anchor_present": True},
            "expected_status": "error",
            "expected_error": True,
        },
        {
            "case_id": "E018",
            **invalid_effort,
            "evidence_signals": {"independent_anchor_present": True},
            "expected_status": "error",
            "expected_error": True,
        },
        {
            "case_id": "E019",
            **negative_used,
            "evidence_signals": {"independent_anchor_present": False},
            "expected_status": "error",
            "expected_error": True,
        },
        {
            "case_id": "E020",
            **hash_mismatch,
            "evidence_signals": {"independent_anchor_present": True},
            "expected_status": "error",
            "expected_error": True,
        },
        {
            "case_id": "E021",
            **bound("route-missing-conflict-state"),
            "evidence_signals": {
                "independent_anchor_present": True,
                "authority_allowed": True,
                "support_result": "supported",
                "coverage_extent": "full",
                "scope_fit": "matched",
                "temporal_fit": "current",
            },
            "expected_action": "assess_support",
            "expected_final_answer_policy": "pending_evidence",
        },
        {
            "case_id": "E022",
            **bound("route-missing-scope-fit"),
            "evidence_signals": {
                "independent_anchor_present": True,
                "authority_allowed": True,
                "support_result": "supported",
                "coverage_extent": "full",
                "conflict_state": "none",
                "temporal_fit": "current",
            },
            "expected_action": "assess_support",
            "expected_final_answer_policy": "pending_evidence",
        },
        {
            "case_id": "E023",
            **bound("route-missing-temporal-fit"),
            "evidence_signals": {
                "independent_anchor_present": True,
                "authority_allowed": True,
                "support_result": "supported",
                "coverage_extent": "full",
                "conflict_state": "none",
                "scope_fit": "matched",
            },
            "expected_action": "assess_support",
            "expected_final_answer_policy": "pending_evidence",
        },
        {
            "case_id": "E024",
            **bound("route-missing-authority-allowed"),
            "evidence_signals": {
                "independent_anchor_present": True,
                "support_result": "supported",
                "coverage_extent": "full",
                "conflict_state": "none",
                "scope_fit": "matched",
                "temporal_fit": "current",
            },
            "expected_action": "assess_support",
            "expected_final_answer_policy": "pending_evidence",
        },
    ]


def matrix_rows(route_results: list[RouteResult]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in route_results:
        decision = result.decision
        rows.append(
            {
                "case_id": result.case_id,
                "status": decision.get("status"),
                "query_mode": decision.get("query_mode"),
                "experience_preset": decision.get("experience_preset"),
                "resolved_experience_preset": decision.get("resolved_experience_preset"),
                "retrieval_effort": decision.get("retrieval_effort"),
                "assurance_profile": decision.get("assurance_profile"),
                "answer_policy": decision.get("answer_policy"),
                "experience_floor": decision.get("experience_floor"),
                "requested_profile_value": (decision.get("requested_profile") or {}).get("value"),
                "requested_profile_applied": (decision.get("requested_profile") or {}).get("applied"),
                "max_retrieval_rounds": (decision.get("budget") or {}).get("max_retrieval_rounds"),
                "max_subqueries": (decision.get("budget") or {}).get("max_subqueries"),
                "max_verifier_calls": (decision.get("budget") or {}).get("max_verifier_calls"),
                "max_repair_calls": (decision.get("budget") or {}).get("max_repair_calls"),
                "max_auto_escalations": (decision.get("budget") or {}).get("max_auto_escalations"),
                "error_codes": "|".join(decision.get("errors", [])),
                "reason_codes": "|".join(decision.get("reason_codes", [])),
            }
        )
    return rows


def assert_invariants(
    cases: list[dict[str, Any]],
    route_results: list[RouteResult],
    transition_cases: list[dict[str, Any]],
    transition_results: list[dict[str, Any]],
) -> dict[str, Any]:
    by_id = {result.case_id: result.decision for result in route_results}
    t_by_id = {result["case_id"]: result for result in transition_results}
    checks: dict[str, bool] = {}

    rerun = [route_case(case).decision for case in cases]
    checks["deterministic_route_decision"] = rerun == [result.decision for result in route_results]

    checks["query_mode_not_overwritten"] = all(
        result.error or result.decision.get("query_mode") == next(c for c in cases if c["case_id"] == result.case_id)["query_mode"]
        for result in route_results
    )
    checks["requested_profile_cannot_lower_floor"] = (
        by_id["R008"]["assurance_profile"] == "strict"
        and by_id["R008"]["requested_profile"]["applied"] is False
    )
    checks["action_query_minimum_strict"] = all(
        result.decision.get("assurance_profile") == "strict"
        for result in route_results
        if not result.error and result.decision.get("query_mode") == "action"
    )
    checks["simple_high_risk_minimal_strict"] = (
        by_id["R006"]["retrieval_effort"] == "minimal"
        and by_id["R006"]["assurance_profile"] == "strict"
    )
    checks["complex_low_risk_deep_grounded"] = (
        by_id["R011"]["retrieval_effort"] == "deep"
        and by_id["R011"]["assurance_profile"] == "grounded"
    )
    checks["unknown_classification_expanded_grounded"] = (
        by_id["R010"]["retrieval_effort"] == "expanded"
        and by_id["R010"]["assurance_profile"] == "grounded"
    )
    checks["invalid_input_returns_error"] = by_id["R012"]["status"] == "error"
    checks["answer_policy_pending_before_evidence"] = all(
        result.error or result.decision.get("answer_policy") == "pending_evidence"
        for result in route_results
    )
    checks["route_expected_fields_match"] = all(
        (
            result.decision.get("status") == "error"
            if case.get("expected_error") is True
            else (
                result.decision.get("resolved_experience_preset")
                == case.get("expected_resolved_experience_preset")
                and result.decision.get("retrieval_effort") == case.get("expected_retrieval_effort")
                and (
                    "expected_requested_applied" not in case
                    or result.decision.get("requested_profile", {}).get("applied")
                    == case.get("expected_requested_applied")
                )
            )
        )
        for case, result in zip(cases, route_results)
    )
    checks["partial_to_qualified"] = t_by_id["E002"]["final_answer_policy"] == "qualified"
    checks["missing_anchor_abstains_if_still_missing"] = (
        t_by_id["E003"]["transition"]["action"] == "escalate_once"
        and t_by_id["E003"]["if_still_missing"]["final_answer_policy"] == "abstain"
    )
    checks["high_risk_unresolved_conflict_review"] = t_by_id["E008"]["final_answer_policy"] == "review"
    checks["transition_expected_actions_match"] = all(
        "expected_action" not in case
        or t_by_id[case["case_id"]].get("status") == "error"
        or t_by_id[case["case_id"]]["transition"]["action"] == case["expected_action"]
        for case in transition_cases
    )
    checks["transition_expected_final_policies_match"] = all(
        "expected_final_answer_policy" not in case
        or t_by_id[case["case_id"]].get("status") == "error"
        or t_by_id[case["case_id"]]["final_answer_policy"] == case["expected_final_answer_policy"]
        for case in transition_cases
    )
    checks["transition_expected_still_missing_policies_match"] = all(
        "expected_if_still_missing_policy" not in case
        or t_by_id[case["case_id"]].get("status") == "error"
        or t_by_id[case["case_id"]]["if_still_missing"]["final_answer_policy"]
        == case["expected_if_still_missing_policy"]
        for case in transition_cases
    )
    checks["transition_expected_status_match"] = all(
        "expected_status" not in case or t_by_id[case["case_id"]]["status"] == case["expected_status"]
        for case in transition_cases
    )
    checks["transition_expected_error_match"] = all(
        "expected_error" not in case
        or (t_by_id[case["case_id"]]["status"] == "error") == bool(case["expected_error"])
        for case in transition_cases
    )
    checks["anchor_only_does_not_direct"] = (
        t_by_id["E009"]["transition"]["action"] == "assess_support"
        and t_by_id["E009"]["final_answer_policy"] == "pending_evidence"
    )
    checks["partial_without_anchor_does_not_qualify"] = (
        t_by_id["E010"]["final_answer_policy"] != "qualified"
        and t_by_id["E010"]["transition"]["action"] == "escalate_once"
    )
    checks["scope_without_anchor_does_not_qualify"] = (
        t_by_id["E011"]["final_answer_policy"] != "qualified"
        and t_by_id["E011"]["transition"]["action"] == "escalate_once"
    )
    checks["low_risk_conflict_without_anchor_does_not_qualify"] = (
        t_by_id["E012"]["final_answer_policy"] != "qualified"
        and t_by_id["E012"]["transition"]["action"] == "escalate_once"
    )
    checks["candidate_partial_does_not_qualify"] = (
        t_by_id["E013"]["final_answer_policy"] != "qualified"
        and t_by_id["E013"]["transition"]["action"] == "escalate_once"
    )
    checks["low_risk_conflict_requires_all_anchors_for_qualified"] = (
        t_by_id["E014"]["final_answer_policy"] == "qualified"
        and t_by_id["E014"]["transition"]["action"] == "qualify"
    )
    checks["direct_requires_supported_full_current_matched"] = (
        t_by_id["E001"]["final_answer_policy"] == "direct"
        and t_by_id["E001"]["transition"]["reason_codes"] == ["fully_supported_full_coverage_direct"]
    )
    checks["direct_requires_explicit_conflict_state"] = (
        t_by_id["E021"]["transition"]["action"] == "assess_support"
        and t_by_id["E021"]["final_answer_policy"] == "pending_evidence"
    )
    checks["direct_requires_explicit_scope_fit"] = (
        t_by_id["E022"]["transition"]["action"] == "assess_support"
        and t_by_id["E022"]["final_answer_policy"] == "pending_evidence"
    )
    checks["direct_requires_explicit_temporal_fit"] = (
        t_by_id["E023"]["transition"]["action"] == "assess_support"
        and t_by_id["E023"]["final_answer_policy"] == "pending_evidence"
    )
    checks["direct_requires_explicit_authority_allowed"] = (
        t_by_id["E024"]["transition"]["action"] == "assess_support"
        and t_by_id["E024"]["final_answer_policy"] == "pending_evidence"
    )
    checks["second_missing_anchor_abstains"] = (
        t_by_id["E016"]["transition"]["action"] == "abstain"
        and t_by_id["E016"]["final_answer_policy"] == "abstain"
    )
    checks["invalid_assurance_profile_errors"] = (
        t_by_id["E017"]["status"] == "error"
        and any("invalid_assurance_profile" in item for item in t_by_id["E017"]["errors"])
    )
    checks["invalid_retrieval_effort_errors"] = (
        t_by_id["E018"]["status"] == "error"
        and any("invalid_retrieval_effort" in item for item in t_by_id["E018"]["errors"])
    )
    checks["invalid_escalation_counter_errors"] = (
        t_by_id["E019"]["status"] == "error"
        and any("invalid_auto_escalations_used" in item for item in t_by_id["E019"]["errors"])
    )
    checks["route_hash_mismatch_errors"] = (
        t_by_id["E020"]["status"] == "error"
        and "route_decision_hash_mismatch" in t_by_id["E020"]["errors"]
    )
    checks["max_auto_escalations_one"] = all(
        result.get("status") == "error"
        or (result["auto_escalations_used"] <= 1 and result["auto_escalations_remaining"] in {0, 1})
        for result in transition_results
    )
    formal_guard_ids = {
        "body_hash",
        "support_boundary",
        "action_readiness",
        "feedback",
        "retrieval_receipt",
        "operation_receipt",
        "receipt",
        "failure_matrix",
        "runtime_artifacts",
    }
    checks["guard_plan_uses_formal_guard_ids"] = all(
        item.get("guard") in formal_guard_ids
        for result in route_results
        if not result.error
        for item in result.decision.get("guard_plan", [])
    )
    checks["strict_does_not_run_all_guards"] = all(
        not any(item["guard"] == "operation_receipt" for item in result.decision.get("guard_plan", []))
        for result in route_results
        if not result.error and result.decision.get("assurance_profile") == "strict"
    )
    checks["strict_does_not_grant_action_basis"] = all(
        result.error or result.decision.get("authority_boundary", {}).get("grants_action_readiness") is False
        for result in route_results
    )
    checks["no_truth_confidence_or_review_status_write"] = all(
        result.error
        or (
            result.decision["authority_boundary"]["changes_truth"] is False
            and result.decision["authority_boundary"]["changes_confidence"] is False
            and result.decision["authority_boundary"]["changes_review_status"] is False
        )
        for result in route_results
    )
    checks["no_production_or_p0_claims"] = all(
        result.error
        or (
            "production_runtime" in result.decision.get("not_proven", [])
            and "source_intake_p0" in result.decision.get("not_proven", [])
        )
        for result in route_results
    )
    checks["guard_plan_has_triggers"] = all(
        result.error or all("trigger" in item for item in result.decision.get("guard_plan", []))
        for result in route_results
    )
    checks["unknown_not_fast_or_strict"] = (
        by_id["R010"]["assurance_profile"] == "grounded"
        and by_id["R010"]["retrieval_effort"] == "expanded"
    )
    valid_assurance = {"light", "grounded", "strict"}
    checks["runtime_profile_field_absent"] = all(
        not contains_key(result.decision, "runtime_profile") for result in route_results
    ) and all(not contains_key(result, "runtime_profile") for result in transition_results)
    checks["assurance_profile_values_canonical"] = all(
        result.error
        or (
            result.decision.get("assurance_profile") in valid_assurance
            and result.decision.get("assurance_floor") in valid_assurance
        )
        for result in route_results
    ) and all(
        result.get("status") == "error"
        or (
            result["transition"]["from_assurance_profile"] in valid_assurance
            and result["transition"]["to_assurance_profile"] in valid_assurance
        )
        for result in transition_results
    )
    checks["transition_carries_authority_boundary"] = all(
        result.get("authority_boundary", {}).get("runtime_only") is True
        and result.get("authority_boundary", {}).get("changes_truth") is False
        and result.get("authority_boundary", {}).get("changes_review_status") is False
        and result.get("authority_boundary", {}).get("grants_action_readiness") is False
        for result in transition_results
    )

    return {
        "all_passed": all(checks.values()),
        "checks": checks,
        "failed": [name for name, passed in checks.items() if not passed],
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def contract_markdown() -> str:
    return """# VAKS Adaptive Assurance Routing R0.6 Contract

This sandbox defines a deterministic runtime routing contract. It is not a new
truth layer, not a production runtime, and not a Source Intake P0 result.

## Core Invariant

```text
query_mode controls use and authority scope.
retrieval_effort controls retrieval complexity.
assurance_profile controls verification cost.
answer_policy is decided after evidence/sufficiency signals.
```

These four fields must not replace each other.

## Canonical Fields

- `query_mode`: `orientation | source_inspection | review | action`
- `experience_preset`: `auto | fast | standard | strict`
- `resolved_experience_preset`: resolved product preset only; it is not an
  assurance state and does not change truth/review/action authority.
- `retrieval_effort`: `minimal | expanded | deep`
- `assurance_profile`: `light | grounded | strict`
- `answer_policy`: `pending_evidence` before evidence is inspected, then
  `direct | qualified | abstain | review` after evidence transition.

## Experience Floors And Assurance Mapping

```yaml
orientation: fast
source_inspection: fast
review: standard
action: strict
```

Requested presets can raise the resolved experience preset but cannot lower the
policy floor. Budgets, artifacts, and Guard plans are computed from the mapped
`assurance_profile` value: `light`, `grounded`, or `strict`.

## Response Rules

```yaml
fully_supported: direct
partially_supported: qualified
scope_limited: qualified
missing_anchor: abstain
unresolved_conflict_low_risk: qualified
unresolved_conflict_high_risk: review
stale_or_superseded: review
candidate_only: abstain
```

`fully_supported` requires an independent allowed anchor plus explicit
ClaimSupportMap-style signals: `support_result: supported`,
`coverage_extent: full`, `conflict_state: none`, `scope_fit: matched`, and
`temporal_fit: current`. Anchor presence alone only permits support assessment;
it does not permit `direct`.

The positive direct-answer fields must be explicit. Missing `authority_allowed`,
`conflict_state`, `scope_fit`, or `temporal_fit` means not assessed yet, so the
transition remains `assess_support` / `pending_evidence` instead of `direct`.

## Route-Bound Evidence Transition

Post-retrieval transition must be bound to a pre-route decision slice. Each
transition input carries `route_decision_id`, `route_decision_hash`,
`query_mode`, `assurance_profile`, `assurance_floor`, `retrieval_effort`,
`risk_level`, `max_auto_escalations`, and `auto_escalations_used`.

The transition fails closed if the hash does not match, an enum is illegal,
`auto_escalations_used` is outside `0 | 1`, or `assurance_profile` is below
`assurance_floor`.

## Guard Planning

Guard checks follow the actual exit, not the profile name. A strict question does
not automatically run operation preflight unless an operation is proposed or an
action-facing object exists.

## Out of Scope

This R0.6 dry-run does not implement production retrieval, vector search, graph
retrieval, semantic routing, LLM classification, UI, database storage, API/MCP,
review approval, truth promotion, or action readiness.

Existing output directories are append-only by default. Regeneration requires
both `--replace-existing` and `--confirm-replace-existing
vaks-adaptive-assurance-routing-r0-6-2026-06-23`.
"""


def limits_markdown() -> str:
    return """# R0.6 Limits

This package can show only that the current routing and escalation matrix
produces deterministic runtime plans under the R0.6 contract.

The runner is append-only by default. `--replace-existing` is protected by a
run-id confirmation token and should be used only to regenerate this sandbox
artifact intentionally.

It does not prove:

- Source Intake P0
- production runtime validation
- routing optimality on real traffic
- production latency or cost
- hybrid/vector/graph retrieval
- reviewed truth
- reviewer approval
- promotion
- action basis approval
- action readiness

`fast`, `standard`, and `strict` are product experience presets only. The
formal runtime contract is `retrieval_effort` plus `assurance_profile`,
constrained by the existing `query_mode`. This package intentionally does not
emit a `runtime_profile` field.
"""


def pro_prompt() -> str:
    return """# Pro Review Prompt: VAKS Adaptive Assurance Routing R0.6

Please audit this sandbox package only within its declared scope.

Questions:

1. Does the R0.6 contract preserve existing `query_mode` semantics instead of
   replacing them with fast/standard/strict?
2. Does the router enforce assurance floors and prevent requested presets from
   lowering them?
3. Do the routing and evidence-transition matrices cover the required
   invariants: simple high-risk minimal+strict, complex low-risk deep+grounded,
   unknown expanded+grounded, invalid input error, missing anchor abstain,
   partial qualified, high-risk conflict review, and max one escalation?
4. Is Guard planning tied to actual exits rather than strict profile names?
5. Does evidence transition use only canonical `assurance_profile` values
   (`light`, `grounded`, `strict`) and avoid any `runtime_profile` field?
6. Does evidence transition require explicit support result + full coverage
   before `direct`, instead of treating anchor presence as support?
7. Do candidate-only, missing-anchor, and no-anchor partial/scope/conflict
   combinations fail safe instead of becoming `qualified`?
8. Is every evidence transition bound to a route decision hash and protected
   against illegal assurance profiles, retrieval efforts, bad escalation
   counters, and hash mismatch?
9. Does `direct` require explicit positive values for authority, conflict,
   scope, and temporal fields instead of treating missing values as pass?
10. Does the runner protect existing output directories unless both
   `--replace-existing` and the matching `--confirm-replace-existing` token are
   supplied?
11. Are overclaims avoided: no P0, no production runtime, no routing optimality,
   no reviewed truth, no action readiness?

Expected verdict format:

```text
overall verdict:
can keep as bounded sandbox evidence:
does it prove P0:
does it prove production runtime:
remaining blockers:
minimum next action:
```
"""


def build_summary(
    output_dir: Path,
    cases: list[dict[str, Any]],
    route_results: list[RouteResult],
    transition_cases_: list[dict[str, Any]],
    transition_results: list[dict[str, Any]],
    invariant_report: dict[str, Any],
) -> dict[str, Any]:
    artifact_hashes: dict[str, str] = {}
    for path in sorted(output_dir.iterdir()):
        if path.is_file():
            artifact_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "status": "pass" if invariant_report["all_passed"] else "fail",
        "contract_version": CONTRACT_VERSION,
        "run_id": RUN_ID,
        "routing_case_count": len(cases),
        "routing_error_count": sum(1 for result in route_results if result.error),
        "route_decision_count": len(route_results),
        "evidence_transition_case_count": len(transition_cases_),
        "evidence_transition_decision_count": len(transition_results),
        "invariant_report": invariant_report,
        "not_proven": NOT_PROVEN,
        "artifact_hashes": artifact_hashes,
    }


def run(
    output_dir: Path,
    replace_existing: bool = False,
    confirm_replace_existing: str | None = None,
) -> dict[str, Any]:
    if output_dir.exists():
        if not replace_existing:
            raise FileExistsError(
                f"{output_dir} already exists; use a new --out-dir or pass protected replacement flags"
            )
        if confirm_replace_existing != RUN_ID:
            raise PermissionError(
                "--replace-existing requires --confirm-replace-existing "
                f"{RUN_ID}; this prevents accidental sandbox deletion"
            )
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)

    cases = routing_cases()
    route_results = [route_case(case) for case in cases]
    transitions = evidence_transition_cases()
    transition_results = [transition_case(case) for case in transitions]
    invariant_report = assert_invariants(cases, route_results, transitions, transition_results)

    (output_dir / "CONTRACT.md").write_text(contract_markdown(), encoding="utf-8")
    write_jsonl(output_dir / "routing_cases.jsonl", cases)
    write_jsonl(output_dir / "routing_decisions.jsonl", [result.decision for result in route_results])
    write_jsonl(output_dir / "evidence_transition_cases.jsonl", transitions)
    write_jsonl(output_dir / "evidence_transition_decisions.jsonl", transition_results)
    write_csv(output_dir / "routing_matrix.csv", matrix_rows(route_results))
    (output_dir / "LIMITS.md").write_text(limits_markdown(), encoding="utf-8")
    (output_dir / "PRO_REVIEW_PROMPT.md").write_text(pro_prompt(), encoding="utf-8")

    summary = build_summary(output_dir, cases, route_results, transitions, transition_results, invariant_report)
    summary_text = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    (output_dir / "routing_summary.json").write_text(summary_text, encoding="utf-8")
    summary["artifact_hashes"]["routing_summary.json"] = sha256_text(summary_text)

    # Rewrite summary after including its own stable content hash placeholder is
    # intentionally avoided; the manifest covers other artifacts and the status.
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--replace-existing", action="store_true")
    parser.add_argument("--confirm-replace-existing")
    args = parser.parse_args()

    summary = run(
        args.out_dir,
        replace_existing=args.replace_existing,
        confirm_replace_existing=args.confirm_replace_existing,
    )
    print(json.dumps({
        "status": summary["status"],
        "run_id": summary["run_id"],
        "output_dir": str(args.out_dir),
        "routing_case_count": summary["routing_case_count"],
        "evidence_transition_case_count": summary["evidence_transition_case_count"],
        "failed_invariants": summary["invariant_report"]["failed"],
    }, ensure_ascii=False, sort_keys=True))
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
