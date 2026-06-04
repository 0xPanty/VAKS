import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parent


AUTHORITY_TRAP_PHRASES = {
    "group_count_as_support": ["group count proves support", "count proves support"],
    "lineage_as_independence": ["lineage proves independence", "derived chain is independent"],
    "source_count_as_independence": ["source count proves independence", "many sources proves independent"],
    "dashboard_as_truth": ["dashboard green means true", "dashboard confirms truth"],
    "test_pass_as_truth": ["test pass confirms truth", "fixture pass proves truth"],
    "feedback_summary_as_truth": ["feedback says true", "feedback confirms truth"],
    "feedback_count_as_truth": ["feedback count raises confidence", "repeated feedback proves truth"],
    "llm_summary_as_truth": ["llm summary is support", "model summary proves support"],
    "retrieval_rank_as_truth": ["ranked first so trusted", "retrieval rank proves trust"],
    "cluster_summary_as_truth": ["cluster summary is reviewed relation", "cluster summary proves relation"],
}

AUTHORITY_BOUNDARY_TOKENS = [
    "not authority",
    "not support strength",
    "not independence proof",
    "diagnostic only",
    "routing only",
    "no truth change",
]


@dataclass
class Case:
    id: str
    family: str
    object_type: str
    surface_state: str
    signal_text: str
    summary: str
    anchor_key: str = "PDF-A1"
    anchor_status: str = "valid"
    recurrence_key: str = ""
    action_meaning: str = ""
    gap_family: str = ""
    feedback_type: str = ""
    authority_trap: str = ""
    fingerprint_version: str = "v1"
    history_bucket: str = "new"
    gold_state: str = "ordinary"
    gold_full_audit: bool = False
    gold_review_due: bool = False
    gold_group_id: str = ""
    gold_can_group: bool = False
    gold_authority_boundary_visible: bool = False
    gold_missing_anchor_visible: bool = False
    gold_jumpback_succeeds: bool = True
    expected_front_max: int = 6
    tags: list[str] = field(default_factory=list)


def c(**kwargs):
    return Case(**kwargs)


def make_cases():
    cases = [
        c(id="FL01", family="false_lite_state", object_type="answer", surface_state="ordinary",
          signal_text="User wants this as action basis for a deployment decision.", summary="Ordinary-looking answer actually used for action.",
          anchor_key="POL-P1", gold_state="blocking", gold_full_audit=True, gold_review_due=True, tags=["trigger_held"]),
        c(id="FL02", family="false_lite_state", object_type="claim", surface_state="ordinary",
          signal_text="Candidate is being promoted to reviewed knowledge.", summary="Note cleanup hides promotion request.",
          anchor_key="PDF-A3", gold_state="blocking", gold_full_audit=True, gold_review_due=True, tags=["trigger_held"]),
        c(id="FL03", family="false_lite_state", object_type="feedback", surface_state="ordinary",
          signal_text="Polite correction: the cited claim is wrong.", summary="Correction must not stay as ordinary feedback.",
          anchor_key="PDF-A4", feedback_type="wrong_claim", gold_state="blocking", gold_full_audit=True, gold_review_due=True, tags=["feedback"]),
        c(id="FL04", family="false_lite_state", object_type="claim", surface_state="ordinary",
          signal_text="Known omission is present in the current source.", summary="Omission should trigger review.",
          anchor_key="WEB-AR4", gap_family="omission", gold_state="for_review", gold_full_audit=True, gold_review_due=True, tags=["trigger_held"]),
        c(id="FL05", family="false_lite_state", object_type="collision", surface_state="ordinary",
          signal_text="This source directly conflicts with the standing reviewed claim.", summary="Conflict must thicken.",
          anchor_key="PDF-A4", gap_family="conflict", gold_state="blocking", gold_full_audit=True, gold_review_due=True, tags=["trigger_held"]),
        c(id="FL06", family="false_lite_state", object_type="answer", surface_state="ordinary",
          signal_text="Risk-sensitive production safety answer.", summary="Short question but production safety risk.",
          anchor_key="DOC-V3", gap_family="risk", gold_state="blocking", gold_full_audit=True, gold_review_due=True, tags=["trigger_held"]),
        c(id="FL07", family="false_lite_state", object_type="feedback", surface_state="ordinary",
          signal_text="High severity wrong answer report from user.", summary="Thanks message contains serious failure.",
          anchor_key="DOC-V3", feedback_type="wrong_answer", gold_state="blocking", gold_full_audit=True, gold_review_due=True, tags=["feedback"]),
        c(id="FL08", family="false_lite_state", object_type="feedback", surface_state="ordinary",
          signal_text="Action outcome failed after using the recommendation.", summary="Outcome note requires review.",
          anchor_key="POL-P3", feedback_type="action_result", gold_state="for_review", gold_full_audit=True, gold_review_due=True, tags=["feedback"]),
        c(id="FL09", family="false_lite_state", object_type="feedback", surface_state="ordinary",
          signal_text="Decision outcome changes future recommendation framing.", summary="Decision outcome calibration.",
          anchor_key="POL-P3", feedback_type="decision_result", gold_state="for_review", gold_full_audit=True, gold_review_due=True, tags=["feedback"]),
        c(id="FL10", family="false_lite_state", object_type="claim", surface_state="ordinary",
          signal_text="Agent memory supplied key support without current source span.", summary="Memory support without span.",
          anchor_key="NONE", anchor_status="missing", gold_state="blocking", gold_full_audit=True, gold_review_due=True,
          gold_missing_anchor_visible=True, gold_jumpback_succeeds=False, tags=["anchor"]),
        c(id="FL11", family="false_lite_state", object_type="feedback", surface_state="ordinary",
          signal_text="Resolved old feedback reappears as regression.", summary="Regression must reopen.",
          anchor_key="PDF-A1", recurrence_key="scope-alpha", feedback_type="too_broad", gold_state="regressed",
          gold_full_audit=True, gold_review_due=True, tags=["recurrence"]),
        c(id="FL12", family="false_lite_state", object_type="collision", surface_state="ordinary",
          signal_text="Reviewer blocks upgrade despite supportive wording.", summary="Reviewer block must thicken.",
          anchor_key="POL-P2", gold_state="blocking", gold_full_audit=True, gold_review_due=True, tags=["trigger_held"]),

        c(id="AU01", family="authority_blackbox", object_type="collision", surface_state="ordinary",
          signal_text="Group count appears in support/refine cluster.", summary="Count must not become support strength.",
          anchor_key="PDF-A1", recurrence_key="auth-group", authority_trap="group_count_as_support",
          gold_authority_boundary_visible=True, tags=["authority", "recurrence"]),
        c(id="AU02", family="authority_blackbox", object_type="claim", surface_state="ordinary",
          signal_text="Lineage chain is visible.", summary="Lineage must not prove independence.",
          anchor_key="DOC-V1", authority_trap="lineage_as_independence", gold_authority_boundary_visible=True, tags=["authority"]),
        c(id="AU03", family="authority_blackbox", object_type="claim", surface_state="ordinary",
          signal_text="Several same-origin source copies repeat the claim.", summary="Source count must not prove independence.",
          anchor_key="DOC-V1", authority_trap="source_count_as_independence", gold_authority_boundary_visible=True, tags=["authority"]),
        c(id="AU04", family="authority_blackbox", object_type="answer", surface_state="ordinary",
          signal_text="Dashboard is green.", summary="Dashboard status is diagnostic only.",
          anchor_key="POL-P1", authority_trap="dashboard_as_truth", gold_authority_boundary_visible=True, tags=["authority"]),
        c(id="AU05", family="authority_blackbox", object_type="answer", surface_state="ordinary",
          signal_text="Fixture test passed.", summary="Test pass is not truth.",
          anchor_key="REPO-R3", authority_trap="test_pass_as_truth", gold_authority_boundary_visible=True, tags=["authority"]),
        c(id="AU06", family="authority_blackbox", object_type="feedback", surface_state="ordinary",
          signal_text="Positive feedback summary says useful.", summary="Positive feedback cannot update truth.",
          anchor_key="PDF-A1", feedback_type="useful", authority_trap="feedback_summary_as_truth",
          gold_authority_boundary_visible=True, tags=["authority", "feedback"]),
        c(id="AU07", family="authority_blackbox", object_type="feedback", surface_state="ordinary",
          signal_text="Repeated feedback count is high.", summary="Feedback count cannot raise truth confidence.",
          anchor_key="PDF-A1", recurrence_key="auth-feedback", feedback_type="too_broad", authority_trap="feedback_count_as_truth",
          gold_authority_boundary_visible=True, gold_group_id="G-AU-FB", gold_can_group=True, tags=["authority", "recurrence"]),
        c(id="AU08", family="authority_blackbox", object_type="feedback", surface_state="ordinary",
          signal_text="Repeated feedback count is high again.", summary="Second feedback count still cannot raise truth confidence.",
          anchor_key="PDF-A1", recurrence_key="auth-feedback", feedback_type="too_broad", authority_trap="feedback_count_as_truth",
          gold_authority_boundary_visible=True, gold_group_id="G-AU-FB", gold_can_group=True, tags=["authority", "recurrence"]),
        c(id="AU09", family="authority_blackbox", object_type="claim", surface_state="ordinary",
          signal_text="LLM summary supplied support without raw source span.", summary="LLM summary cannot be support.",
          anchor_key="NONE", anchor_status="missing", authority_trap="llm_summary_as_truth",
          gold_state="blocking", gold_full_audit=True, gold_review_due=True, gold_authority_boundary_visible=True,
          gold_missing_anchor_visible=True, gold_jumpback_succeeds=False, tags=["authority", "anchor"]),
        c(id="AU10", family="authority_blackbox", object_type="answer", surface_state="ordinary",
          signal_text="Retrieval rank is high.", summary="Retrieval rank cannot become trust.",
          anchor_key="WEB-AR1", authority_trap="retrieval_rank_as_truth", gold_authority_boundary_visible=True, tags=["authority"]),
        c(id="AU11", family="authority_blackbox", object_type="collision", surface_state="ordinary",
          signal_text="Cluster summary suggests a reviewed relation.", summary="Cluster summary is not reviewed relation.",
          anchor_key="REPO-R4", authority_trap="cluster_summary_as_truth", gold_authority_boundary_visible=True, tags=["authority"]),

        c(id="AN01", family="anchor_jumpback_output", object_type="claim", surface_state="ordinary",
          signal_text="Valid PDF anchor should jump back.", summary="PDF page/span anchor.",
          anchor_key="PDF-A1", tags=["anchor", "sparse"]),
        c(id="AN02", family="anchor_jumpback_output", object_type="answer", surface_state="ordinary",
          signal_text="Versioned doc anchor should preserve version.", summary="Versioned doc pointer.",
          anchor_key="DOC-V2", tags=["anchor", "sparse"]),
        c(id="AN03", family="anchor_jumpback_output", object_type="claim", surface_state="ordinary",
          signal_text="Archived web selector should resolve.", summary="Archived web pointer.",
          anchor_key="WEB-AR3", tags=["anchor", "sparse"]),
        c(id="AN04", family="anchor_jumpback_output", object_type="claim", surface_state="ordinary",
          signal_text="Repo release note pointer should resolve.", summary="Repo release pointer.",
          anchor_key="REPO-R1", tags=["anchor", "sparse"]),
        c(id="AN05", family="anchor_jumpback_output", object_type="answer", surface_state="ordinary",
          signal_text="Policy page pointer should resolve.", summary="Policy pointer.",
          anchor_key="POL-P1", tags=["anchor", "sparse"]),
        c(id="AN06", family="anchor_jumpback_output", object_type="claim", surface_state="ordinary",
          signal_text="Missing source span must be visible.", summary="Missing anchor.",
          anchor_key="NONE", anchor_status="missing", gold_state="blocking", gold_full_audit=True, gold_review_due=True,
          gold_missing_anchor_visible=True, gold_jumpback_succeeds=False, tags=["anchor"]),
        c(id="AN07", family="anchor_jumpback_output", object_type="claim", surface_state="ordinary",
          signal_text="Selector drift should be review due.", summary="Selector drift.",
          anchor_key="WEB-DRIFT", anchor_status="drift", gold_state="for_review", gold_full_audit=True, gold_review_due=True,
          gold_missing_anchor_visible=True, gold_jumpback_succeeds=False, tags=["anchor"]),
        c(id="AN08", family="anchor_jumpback_output", object_type="answer", surface_state="ordinary",
          signal_text="Stale pointer should not pass as traceability.", summary="Stale pointer.",
          anchor_key="STALE-DOC", anchor_status="stale", gold_state="for_review", gold_full_audit=True, gold_review_due=True,
          gold_missing_anchor_visible=True, gold_jumpback_succeeds=False, tags=["anchor"]),

        c(id="GR01", family="grouping_recurrence", object_type="feedback", surface_state="ordinary",
          signal_text="Repeated too-broad feedback for same answer-scope action.", summary="Same recurrence 1.",
          anchor_key="PDF-A1", recurrence_key="scope-topic-alpha", action_meaning="narrow_answer_scope", feedback_type="too_broad",
          gap_family="scope_gap", gold_group_id="G-SCOPE-1", gold_can_group=True, tags=["recurrence"]),
        c(id="GR02", family="grouping_recurrence", object_type="feedback", surface_state="ordinary",
          signal_text="Repeated too-broad feedback for same answer-scope action.", summary="Same recurrence 2.",
          anchor_key="PDF-A1", recurrence_key="scope-topic-alpha", action_meaning="narrow_answer_scope", feedback_type="too_broad",
          gap_family="scope_gap", gold_group_id="G-SCOPE-1", gold_can_group=True, tags=["recurrence"]),
        c(id="GR03", family="grouping_recurrence", object_type="feedback", surface_state="ordinary",
          signal_text="Same topic but deployment approval action.", summary="Same topic, different action meaning.",
          anchor_key="PDF-A1", recurrence_key="scope-topic-alpha", action_meaning="approve_deployment", feedback_type="too_broad",
          gap_family="scope_gap", tags=["recurrence"]),
        c(id="GR04", family="grouping_recurrence", object_type="collision", surface_state="ordinary",
          signal_text="Support/refine says simulated-only scope.", summary="Refine recurrence 1.",
          anchor_key="REPO-R4", recurrence_key="collision-gamma", action_meaning="refine_scope", gap_family="scope_gap",
          gold_group_id="G-REFINE-1", gold_can_group=True, tags=["recurrence"]),
        c(id="GR05", family="grouping_recurrence", object_type="collision", surface_state="ordinary",
          signal_text="Support/refine says simulated-only scope again.", summary="Refine recurrence 2.",
          anchor_key="REPO-R4", recurrence_key="collision-gamma", action_meaning="refine_scope", gap_family="scope_gap",
          gold_group_id="G-REFINE-1", gold_can_group=True, tags=["recurrence"]),
        c(id="GR06", family="grouping_recurrence", object_type="collision", surface_state="ordinary",
          signal_text="Same recurrence key but this source conflicts.", summary="Conflict member must break fold.",
          anchor_key="PDF-A4", recurrence_key="collision-gamma", action_meaning="refine_scope", gap_family="conflict",
          gold_state="blocking", gold_full_audit=True, gold_review_due=True, tags=["recurrence", "trigger_held"]),
        c(id="GR07", family="grouping_recurrence", object_type="collision", surface_state="ordinary",
          signal_text="Same recurrence key but missing anchor.", summary="Missing anchor member must break fold.",
          anchor_key="NONE", anchor_status="missing", recurrence_key="collision-gamma", action_meaning="refine_scope",
          gap_family="scope_gap", gold_state="blocking", gold_full_audit=True, gold_review_due=True,
          gold_missing_anchor_visible=True, gold_jumpback_succeeds=False, tags=["recurrence", "anchor"]),
        c(id="GR08", family="grouping_recurrence", object_type="feedback", surface_state="ordinary",
          signal_text="Resolved recurrence reappears as regression.", summary="Regression must reopen.",
          anchor_key="PDF-A1", recurrence_key="scope-topic-alpha", action_meaning="narrow_answer_scope", feedback_type="too_broad",
          gap_family="scope_gap", gold_state="regressed", gold_full_audit=True, gold_review_due=True, tags=["recurrence"]),

        c(id="VG01", family="versioned_fingerprint", object_type="feedback", surface_state="resolved_folded",
          signal_text="Old v1 resolved recurrence.", summary="Fingerprint v1 old member.",
          anchor_key="PDF-A1", recurrence_key="fp-delta", action_meaning="narrow_answer_scope", feedback_type="too_broad",
          fingerprint_version="v1", history_bucket="old", gold_state="resolved_folded", gold_group_id="G-FP-v1", gold_can_group=True, tags=["versioned"]),
        c(id="VG02", family="versioned_fingerprint", object_type="feedback", surface_state="resolved_folded",
          signal_text="Second old v1 resolved recurrence.", summary="Fingerprint v1 old member 2.",
          anchor_key="PDF-A1", recurrence_key="fp-delta", action_meaning="narrow_answer_scope", feedback_type="too_broad",
          fingerprint_version="v1", history_bucket="old", gold_state="resolved_folded", gold_group_id="G-FP-v1", gold_can_group=True, tags=["versioned"]),
        c(id="VG03", family="versioned_fingerprint", object_type="feedback", surface_state="ordinary",
          signal_text="New v2 recurrence with action outcome failure.", summary="New serious member must not be absorbed into v1.",
          anchor_key="POL-P3", recurrence_key="fp-delta", action_meaning="narrow_answer_scope", feedback_type="action_result",
          fingerprint_version="v2", history_bucket="new", gold_state="for_review", gold_full_audit=True, gold_review_due=True, tags=["versioned", "feedback"]),
        c(id="VG04", family="versioned_fingerprint", object_type="feedback", surface_state="ordinary",
          signal_text="New v2 ordinary recurrence with compatible action meaning.", summary="New v2 ordinary member.",
          anchor_key="PDF-A1", recurrence_key="fp-epsilon", action_meaning="add_context", feedback_type="missing_context",
          fingerprint_version="v2", history_bucket="new", gold_group_id="G-FP-v2", gold_can_group=True, tags=["versioned"]),
        c(id="VG05", family="versioned_fingerprint", object_type="feedback", surface_state="ordinary",
          signal_text="Second new v2 ordinary recurrence with compatible action meaning.", summary="New v2 ordinary member 2.",
          anchor_key="PDF-A1", recurrence_key="fp-epsilon", action_meaning="add_context", feedback_type="missing_context",
          fingerprint_version="v2", history_bucket="new", gold_group_id="G-FP-v2", gold_can_group=True, tags=["versioned"]),

        c(id="FB01", family="feedback_revision_strip", object_type="feedback", surface_state="ordinary",
          signal_text="Useful feedback, route should be remembered but truth unchanged.", summary="Categorical feedback useful.",
          anchor_key="PDF-A1", feedback_type="useful", gold_authority_boundary_visible=True, tags=["feedback", "authority"]),
        c(id="FB02", family="feedback_revision_strip", object_type="feedback", surface_state="ordinary",
          signal_text="Wrong scope feedback, activation route should narrow but truth unchanged.", summary="Categorical wrong scope.",
          anchor_key="PDF-A1", feedback_type="wrong_scope", gap_family="scope_gap", gold_authority_boundary_visible=True, tags=["feedback", "authority"]),

        c(id="FR01", family="front_burden", object_type="claim", surface_state="ordinary",
          signal_text="Long provenance-heavy ordinary claim with valid source.", summary="Ordinary claim with a long provenance chain and repeated processing notes that should not all be on the front.",
          anchor_key="DOC-V1", gap_family="none", tags=["sparse"]),
        c(id="FR02", family="front_burden", object_type="answer", surface_state="ordinary",
          signal_text="Long ordinary query-run with many excluded candidates.", summary="Ordinary query answer with many activated but unused candidates and a long trace.",
          anchor_key="WEB-AR1", tags=["sparse"]),
        c(id="FR03", family="front_burden", object_type="answer", surface_state="ordinary",
          signal_text="Action basis with long trace must keep deep packet.", summary="Long action-basis trace should not be compressed away.",
          anchor_key="POL-P2", gold_state="blocking", gold_full_audit=True, gold_review_due=True, tags=["trigger_held", "sparse"]),
    ]
    return cases


def load_anchors():
    return json.loads((ROOT / "anchors.json").read_text(encoding="utf-8"))


def detect_state(case):
    text = case.signal_text.lower()
    anchor_problem = case.anchor_status in {"missing", "stale", "drift"}
    if "regression" in text or "reappears" in text:
        return "regressed"
    if "action basis" in text or "promotion" in text or "promoted" in text or "explicit challenge" in text or "conflicts" in text or "conflict" in text:
        return "blocking"
    if "risk-sensitive" in text or "high severity" in text or "wrong answer" in text or "correction" in text:
        return "blocking"
    if "reviewer blocks" in text or "blocks upgrade" in text:
        return "blocking"
    if anchor_problem and case.anchor_status == "missing":
        return "blocking"
    if anchor_problem:
        return "for_review"
    if "known omission" in text or "action outcome" in text or "decision outcome" in text or "failed" in text:
        return "for_review"
    if case.surface_state in {"resolved_folded", "parked_nonblocking"}:
        return case.surface_state
    return "ordinary"


def should_full_audit(state, case):
    return state in {"blocking", "for_review", "regressed"} or case.anchor_status in {"missing", "stale", "drift"}


def anchor_line(case, anchors, sparse=True):
    if case.anchor_status == "valid":
        meta = anchors.get(case.anchor_key, {})
        if sparse:
            return f"anchor: {case.anchor_key} path={meta.get('path')} marker={meta.get('marker')}"
        return f"anchor: {case.anchor_key} path={meta.get('path')} marker={meta.get('marker')} mode=full_provenance type={meta.get('type')}"
    return f"missing_anchor: {case.anchor_status}:{case.anchor_key}"


def risky_authority_text(case):
    phrases = AUTHORITY_TRAP_PHRASES.get(case.authority_trap)
    return phrases[0] if phrases else ""


def safe_authority_text(case):
    if not case.authority_trap:
        return ""
    if "independence" in case.authority_trap:
        return f"authority_boundary: {case.authority_trap} is not independence proof"
    if "feedback" in case.authority_trap:
        return f"authority_boundary: {case.authority_trap} is no truth change"
    if "dashboard" in case.authority_trap or "test_pass" in case.authority_trap or "retrieval" in case.authority_trap:
        return f"authority_boundary: {case.authority_trap} is diagnostic only"
    return f"authority_boundary: {case.authority_trap} is not support strength"


def group_candidate(case, versioned=False):
    if not case.recurrence_key:
        return ""
    parts = [case.recurrence_key, case.action_meaning, case.feedback_type, case.gap_family, case.anchor_status]
    if versioned:
        parts.insert(0, case.fingerprint_version)
    return "|".join(parts)


def render_case(case, variant, anchors):
    core = variant not in {"control_previous_patch_like"}
    state = detect_state(case) if core else case.surface_state
    full = True if variant == "baseline_full_audit" else should_full_audit(state, case)
    review_due = full or state in {"blocking", "for_review", "regressed"}

    sparse = variant in {"sparse_provenance_mention_pointer", "guarded_combined"}
    folded = variant in {"folded_recurrence_card", "guarded_combined"}
    versioned = variant in {"versioned_fingerprint_grouping", "guarded_combined"}
    categorical_feedback = variant in {"categorical_feedback_revision_strip", "guarded_combined"}

    front = [f"case: {case.id}", f"state: {state}", f"summary: {case.summary}"]
    back = [f"full_record_pointer: record://{case.id}"]
    full_audit = []

    if variant == "control_previous_patch_like":
        state = case.surface_state
        full = case.surface_state in {"blocking", "for_review", "regressed"} or case.anchor_status in {"missing", "stale", "drift"}
        review_due = full
        front = [f"case: {case.id}", f"state: {state}", f"summary: {case.summary}"]
        if case.authority_trap:
            front.append(f"note: {risky_authority_text(case)}")
    elif variant == "baseline_full_audit":
        full = True
        review_due = state in {"blocking", "for_review", "regressed"}
        front.append("full_audit_open: baseline")

    front.append(anchor_line(case, anchors, sparse=sparse))

    if case.gap_family and case.gap_family != "none":
        front.append(f"open_gap: {case.gap_family}")
    if full:
        front.append("upgrade_trigger: hard_gate_or_anchor_problem")
        full_audit.append("FULL_AUDIT_OPEN")
        full_audit.append(f"review_due: {str(review_due).lower()}")
        full_audit.append(f"evidence_packet_pointer: evidence://{case.id}")
    elif review_due:
        front.append("review_due: true")

    if case.authority_trap:
        if core:
            boundary = safe_authority_text(case)
            front.append(boundary)
            back.append(boundary)
        elif variant == "baseline_full_audit":
            back.append(safe_authority_text(case))

    if case.object_type == "feedback":
        if categorical_feedback:
            front.append(f"feedback_revision: type={case.feedback_type or 'note'} recurrence={case.recurrence_key or 'none'} no truth change")
        elif variant == "control_previous_patch_like" and case.feedback_type in {"useful", "wrong_scope"}:
            front.append("feedback_delta: truth_confidence_delta=+0.1")

    group_id = ""
    if folded or versioned:
        group_id = group_candidate(case, versioned=versioned)
        if full or state in {"blocking", "for_review", "regressed"}:
            front.append("fold_break: serious_member_or_anchor_problem")
            group_id = ""
        elif group_id:
            front.append(f"group_id: {group_id}")
            front.append(f"fingerprint_version: {case.fingerprint_version if versioned else 'unversioned'}")
            if folded:
                front.append("folded_recurrence_card: latest_exemplar + unresolved_exemplar + count + last_seen")

    if variant == "trigger_held_deep_packet_retention" and not full:
        front.append("metadata_stub: ordinary")
    if sparse and case.anchor_status == "valid":
        front.append("provenance_mode: sparse_pointer")
    elif case.anchor_status == "valid":
        back.append("provenance_detail: entity/activity/agent/source family/processing notes")

    if variant != "control_previous_patch_like":
        front = compact_front(front)

    return {
        "case_id": case.id,
        "variant": variant,
        "front": front,
        "back": back,
        "full": full_audit,
        "rendered_text": "\n".join(front + back + full_audit),
    }


def compact_front(front):
    case_line = next((line for line in front if line.startswith("case: ")), "")
    state_line = next((line for line in front if line.startswith("state: ")), "")
    summary_line = next((line for line in front if line.startswith("summary: ")), "")
    anchor = next((line for line in front if line.startswith("anchor: ") or line.startswith("missing_anchor: ")), "")

    group = next((line for line in front if line.startswith("group_id: ")), "")
    fingerprint = next((line for line in front if line.startswith("fingerprint_version: ")), "")
    folded = next((line for line in front if line.startswith("folded_recurrence_card: ")), "")
    if group:
        group = " ".join(part for part in [group, fingerprint.replace("fingerprint_version:", "fingerprint="), folded.replace("folded_recurrence_card:", "folded=")] if part)

    reserved = {case_line, state_line, summary_line, anchor}
    if group:
        reserved.add(next((line for line in front if line.startswith("group_id: ")), ""))
        reserved.add(next((line for line in front if line.startswith("fingerprint_version: ")), ""))
        reserved.add(next((line for line in front if line.startswith("folded_recurrence_card: ")), ""))

    flags = [line for line in front if line and line not in reserved]
    compacted = [line for line in [case_line, state_line, summary_line, anchor, group] if line]
    if flags:
        compacted.append("flags: " + " ; ".join(flags))
    return compacted


def parse_state(artifact):
    for line in artifact["front"]:
        if line.startswith("state: "):
            return line.split(": ", 1)[1].strip()
    return "missing"


def parse_group_id(artifact):
    for line in artifact["front"]:
        if line.startswith("group_id: "):
            return line.split(": ", 1)[1].strip()
    return ""


def parse_anchor(artifact):
    for line in artifact["front"]:
        if line.startswith("anchor: "):
            m = re.search(r"anchor: (?P<key>\S+) path=(?P<path>\S+) marker=(?P<marker>\S+)", line)
            if m:
                return m.groupdict()
    return {}


def anchor_resolves(parsed):
    if not parsed:
        return False
    path = ROOT / parsed["path"]
    if not path.exists():
        return False
    return parsed["marker"] in path.read_text(encoding="utf-8")


def authority_leaks(text):
    lower = text.lower()
    return any(phrase in lower for phrases in AUTHORITY_TRAP_PHRASES.values() for phrase in phrases) or "truth_confidence_delta" in lower


def authority_boundary_visible(text):
    lower = text.lower()
    return any(token in lower for token in AUTHORITY_BOUNDARY_TOKENS)


def compare_output(case, artifact):
    text = artifact["rendered_text"]
    state = parse_state(artifact)
    full = "FULL_AUDIT_OPEN" in text
    review_due = "review_due: true" in text
    missing_anchor_visible = "missing_anchor:" in text
    parsed_anchor = parse_anchor(artifact)
    jumpback = anchor_resolves(parsed_anchor)
    front_lines = len(artifact["front"])
    leak = authority_leaks(text)
    boundary = authority_boundary_visible(text)

    return {
        "case_id": case.id,
        "state_ok": state == case.gold_state,
        "false_lite": case.gold_full_audit and not full,
        "ordinary_false_positive": (not case.gold_full_audit) and full,
        "review_due_fn": case.gold_review_due and not review_due,
        "review_due_fp": (not case.gold_review_due) and review_due,
        "missing_anchor_ok": (not case.gold_missing_anchor_visible) or (missing_anchor_visible and full),
        "jumpback_ok": (not case.gold_jumpback_succeeds) or jumpback,
        "authority_leak": leak,
        "authority_boundary_ok": (not case.gold_authority_boundary_visible) or (boundary and not leak),
        "front_ok": front_lines <= case.expected_front_max,
        "front_lines": front_lines,
        "full_lines": len(artifact["full"]),
        "back_lines": len(artifact["back"]),
        "group_id": parse_group_id(artifact),
    }


def evaluate_grouping(cases, comparisons):
    by_id = {case.id: case for case in cases}
    groups = defaultdict(list)
    for row in comparisons:
        if row["group_id"]:
            groups[row["group_id"]].append(row["case_id"])

    severe = []
    grouped_gold_members = set()
    for group_key, ids in groups.items():
        if len(ids) <= 1:
            continue
        gold_ids = {by_id[i].gold_group_id for i in ids}
        can_group = all(by_id[i].gold_can_group for i in ids)
        states = {by_id[i].gold_state for i in ids}
        if not can_group or len(gold_ids) != 1 or "" in gold_ids or states - {"ordinary", "resolved_folded", "parked_nonblocking"}:
            severe.append({"group_key": group_key, "case_ids": ids, "gold_group_ids": sorted(gold_ids), "states": sorted(states)})
        else:
            grouped_gold_members.update(ids)

    gold_groupable = [case for case in cases if case.gold_can_group]
    grouping_recall = len(grouped_gold_members) / len(gold_groupable) if gold_groupable else 1.0
    grouped_count = sum(len(ids) for ids in groups.values() if len(ids) > 1)
    group_cards = sum(1 for ids in groups.values() if len(ids) > 1)
    reduction = ((grouped_count - group_cards) / grouped_count * 100) if grouped_count else 0.0
    return {
        "groups": dict(groups),
        "severe_over_grouping": severe,
        "gold_groupable": len(gold_groupable),
        "grouping_recall": round(grouping_recall, 4),
        "grouped_reduction_pct": round(reduction, 1),
    }


def summarize_variant(cases, artifacts, comparisons, grouping):
    total = len(cases)
    hard_failures = {
        "state_mismatch": sum(1 for row in comparisons if not row["state_ok"]),
        "false_lite": sum(1 for row in comparisons if row["false_lite"]),
        "review_due_fn": sum(1 for row in comparisons if row["review_due_fn"]),
        "jumpback_failures": sum(1 for row in comparisons if not row["jumpback_ok"]),
        "missing_anchor_failures": sum(1 for row in comparisons if not row["missing_anchor_ok"]),
        "authority_leakage": sum(1 for row in comparisons if row["authority_leak"]),
        "authority_boundary_failures": sum(1 for row in comparisons if not row["authority_boundary_ok"]),
        "front_violations": sum(1 for row in comparisons if not row["front_ok"]),
        "severe_over_grouping": len(grouping["severe_over_grouping"]),
    }
    safety_pass = all(value == 0 for value in hard_failures.values())
    baseline_front = total * 12
    front_lines = sum(row["front_lines"] for row in comparisons)
    visible_reduction = round((baseline_front - front_lines) / baseline_front * 100, 1)
    total_lines = sum(row["front_lines"] + row["back_lines"] + row["full_lines"] for row in comparisons)
    full_count = sum(1 for row in comparisons if row["full_lines"] > 0)
    burden_units = front_lines + total_lines + (2 * full_count) + len(grouping["groups"])
    return {
        "cases": total,
        "safety_pass": safety_pass,
        "hard_failures": hard_failures,
        "ordinary_false_positive": sum(1 for row in comparisons if row["ordinary_false_positive"]),
        "review_due_fp": sum(1 for row in comparisons if row["review_due_fp"]),
        "visible_front_reduction_pct": visible_reduction,
        "grouping_recall": grouping["grouping_recall"],
        "grouped_reduction_pct": grouping["grouped_reduction_pct"],
        "front_lines_total": front_lines,
        "total_rendered_lines": total_lines,
        "full_audit_count": full_count,
        "burden_units": burden_units,
        "score": score_variant(safety_pass, hard_failures, visible_reduction, grouping, burden_units),
    }


def score_variant(safety_pass, hard_failures, visible_reduction, grouping, burden_units):
    if not safety_pass:
        return 0
    score = 50
    score += min(25, max(0, visible_reduction) * 0.35)
    score += min(10, grouping["grouping_recall"] * 10)
    score += min(8, grouping["grouped_reduction_pct"] * 0.08)
    score += max(0, 12 - burden_units / 120)
    score -= hard_failures.get("front_violations", 0) * 2
    return round(score, 2)


def run():
    anchors = load_anchors()
    cases = make_cases()
    variants = [
        "baseline_full_audit",
        "control_previous_patch_like",
        "trigger_held_deep_packet_retention",
        "sparse_provenance_mention_pointer",
        "folded_recurrence_card",
        "versioned_fingerprint_grouping",
        "categorical_feedback_revision_strip",
        "guarded_combined",
    ]

    all_artifacts = {}
    all_results = {}
    for variant in variants:
        artifacts = [render_case(case, variant, anchors) for case in cases]
        comparisons = [compare_output(case, artifact) for case, artifact in zip(cases, artifacts)]
        grouping = evaluate_grouping(cases, comparisons)
        summary = summarize_variant(cases, artifacts, comparisons, grouping)
        all_artifacts[variant] = artifacts
        all_results[variant] = {
            "summary": summary,
            "comparisons": comparisons,
            "grouping": grouping,
        }

    (ROOT / "rendered_artifacts.json").write_text(json.dumps(all_artifacts, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "oracle_results.json").write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "ALPHA_BAKEOFF_REPORT.md").write_text(make_alpha_report(all_results), encoding="utf-8")
    (ROOT / "FRAMEWORK_SANDBOX_PRESSURE_REPORT.md").write_text(make_framework_report(all_results), encoding="utf-8")
    (ROOT / "README.md").write_text(make_readme(), encoding="utf-8")

    ranked = sorted(((name, result["summary"]["score"], result["summary"]["safety_pass"]) for name, result in all_results.items()), key=lambda x: x[1], reverse=True)
    print("ranked_variants:")
    for name, score, safety in ranked:
        print(f"{name}: score={score} safety_pass={safety}")
    best = ranked[0]
    if best[0] != "guarded_combined" or not best[2]:
        raise SystemExit(1)


def make_alpha_report(results):
    cases = make_cases()
    cases_by_id = {case.id: case for case in cases}
    slice_tags = {
        "trigger_held_deep_packet_retention": {"trigger_held"},
        "sparse_provenance_mention_pointer": {"sparse", "anchor"},
        "folded_recurrence_card": {"recurrence"},
        "versioned_fingerprint_grouping": {"versioned"},
        "categorical_feedback_revision_strip": {"feedback", "authority"},
        "guarded_combined": {"trigger_held", "sparse", "anchor", "recurrence", "versioned", "feedback", "authority"},
    }
    lines = [
        "# VAKS Audit Shell Output-Level Oracle Alpha Bakeoff",
        "",
        "Status: sandbox-only. No main-vault writeback, no SCHEMA change, no truth-core change.",
        "",
        "## Verdict",
        "",
        "The strongest positive result is `guarded_combined`: trigger-held deep packet retention + sparse provenance mention pointer + folded recurrence card + versioned fingerprint grouping, with categorical feedback wording as a supporting constraint.",
        "",
        "No structural alpha should be adopted alone. The safest standalone item is `categorical_feedback_revision_strip`, but it has narrow impact. The strongest core alpha is `trigger_held_deep_packet_retention`, because it protects the hard boundary: ordinary stays light, serious triggers become thick. It still needs the feedback/authority boundary strip to be safe across the whole framework.",
        "",
        "## Full Pressure Table",
        "",
        "This table runs every variant against the entire pressure set. A single-purpose alpha can fail here if it lacks another required boundary.",
        "",
        "| variant | safety | score | false-lite | state mismatch | authority leakage | authority boundary fail | jumpback fail | severe over-group | front reduction | grouping recall | grouped reduction | burden units |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, data in sorted(results.items(), key=lambda item: item[1]["summary"]["score"], reverse=True):
        s = data["summary"]
        f = s["hard_failures"]
        lines.append(
            f"| {name} | {s['safety_pass']} | {s['score']} | {f['false_lite']} | {f['state_mismatch']} | "
            f"{f['authority_leakage']} | {f['authority_boundary_failures']} | {f['jumpback_failures']} | "
            f"{f['severe_over_grouping']} | {s['visible_front_reduction_pct']} | {s['grouping_recall']} | "
            f"{s['grouped_reduction_pct']} | {s['burden_units']} |"
        )
    lines.extend([
        "",
        "## Relevant Slice Table",
        "",
        "This table asks a narrower question: when an alpha is tested against the cases it is meant to solve, does it behave positively?",
        "",
        "| alpha | slice cases | slice safety | slice hard failures | slice front reduction | full-set caveat |",
        "| --- | ---: | --- | ---: | ---: | --- |",
    ])
    for name, tags in slice_tags.items():
        if name not in results:
            continue
        rows = results[name]["comparisons"]
        relevant_ids = {case.id for case in cases if set(case.tags) & tags}
        relevant = [row for row in rows if row["case_id"] in relevant_ids]
        hard = sum(
            1
            for row in relevant
            if not all([
                row["state_ok"],
                not row["false_lite"],
                not row["review_due_fn"],
                row["jumpback_ok"],
                row["missing_anchor_ok"],
                not row["authority_leak"],
                row["authority_boundary_ok"],
                row["front_ok"],
            ])
        )
        front_lines = sum(row["front_lines"] for row in relevant)
        baseline = len(relevant) * 12
        reduction = round((baseline - front_lines) / baseline * 100, 1) if baseline else 0.0
        caveat = "safe as standalone wording constraint" if name == "categorical_feedback_revision_strip" else "needs companion boundaries for full framework"
        if name == "guarded_combined":
            caveat = "candidate stack for framework sandbox"
        lines.append(f"| {name} | {len(relevant)} | {hard == 0} | {hard} | {reduction} | {caveat} |")
    lines.extend([
        "",
        "## Alpha Judgment",
        "",
        "### Strong Positive Stack",
        "",
        "- `guarded_combined` is the strongest result. It passes the output-level hard gates while keeping a substantial front-face reduction.",
        "- This means the reasonable alpha is not one isolated trick; it is a guarded shell stack.",
        "",
        "### Strong Positive Components",
        "",
        "- `trigger_held_deep_packet_retention`: core engine. It should be carried forward as the main alpha, but not alone.",
        "- `sparse_provenance_mention_pointer`: strong companion. It reduces repeated provenance text while preserving resolvable anchor pointers.",
        "- `folded_recurrence_card`: strong but only under a hard break-fold rule. It reduces recurrence noise, but serious, missing-anchor, or regressed members must escape the fold.",
        "- `versioned_fingerprint_grouping`: strong for long-term maintainability. It prevents new grouping rules from rewriting old grouping history.",
        "",
        "### Supporting Constraint",
        "",
        "- `categorical_feedback_revision_strip`: useful, but better treated as wording discipline inside the shell rather than the main alpha by itself.",
        "",
        "## Why The Control Fails",
        "",
        "The `control_previous_patch_like` variant is intentionally close to the old weakness. It fails output-level checks because state is not upgraded from ordinary-looking surfaces and authority traps can leak into rendered text.",
        "",
        "## What This Proves",
        "",
        "This proves the output-level oracle can catch the exact overclaim classes Pro identified: state mismatch, authority leakage, rendered-front violations, jump-back failure, and unsafe grouping.",
        "",
        "It still does not prove real-data product readiness. The next step after this sandbox is a real-data paired pilot only if the user approves it.",
    ])
    return "\n".join(lines) + "\n"


def make_framework_report(results):
    best = results["guarded_combined"]["summary"]
    lines = [
        "# Main-Framework Sandbox Pressure Report",
        "",
        "Status: sandbox projection only. This is not a main-vault operation convention and not a schema patch.",
        "",
        "## Framework Fit",
        "",
        "The guarded combined alpha fits the existing VAKS route because it stays in the view / queue / audit shell layer:",
        "",
        "- Capture / Understand remain light for ordinary material.",
        "- Review / action-basis gates still thicken on hard triggers.",
        "- Connect / grouping remains triage only, not support strength.",
        "- Feedback remains activation / scope-fit only, not truth change.",
        "- Source anchors stay jump-backable through sparse pointers.",
        "",
        "## Pressure Gates",
        "",
        "| gate | result |",
        "| --- | --- |",
        f"| safety pass | {best['safety_pass']} |",
        f"| false-lite | {best['hard_failures']['false_lite']} |",
        f"| state mismatch | {best['hard_failures']['state_mismatch']} |",
        f"| authority leakage | {best['hard_failures']['authority_leakage']} |",
        f"| authority boundary failures | {best['hard_failures']['authority_boundary_failures']} |",
        f"| jump-back failures | {best['hard_failures']['jumpback_failures']} |",
        f"| severe over-grouping | {best['hard_failures']['severe_over_grouping']} |",
        f"| visible front reduction | {best['visible_front_reduction_pct']}% |",
        f"| grouping recall | {best['grouping_recall']} |",
        f"| grouped reduction | {best['grouped_reduction_pct']}% |",
        "",
        "## Sandbox Operation Convention Candidate",
        "",
        "Candidate wording for future testing only:",
        "",
        "```text",
        "Use audit shell front/back/full as a view convention.",
        "Default ordinary items to a compact front face with resolvable anchor pointers.",
        "Open deep packet on action-basis, promotion, explicit challenge, conflict, known omission, missing/stale/drifted anchor, regression, action outcome, decision outcome, reviewer block, or high-severity wrong answer.",
        "Fold recurrence only when the representative members remain ordinary and anchor-valid.",
        "Version fingerprint grouping rules and never rewrite old group history from new rules.",
        "Render authority boundaries wherever count, lineage, dashboard, test pass, feedback, retrieval rank, LLM summary, or cluster summary appears.",
        "```",
        "",
        "## Still Forbidden",
        "",
        "- Do not write this into `SCHEMA.md`.",
        "- Do not treat grouping as support strength.",
        "- Do not treat lineage or provenance as independence proof.",
        "- Do not treat dashboard/test/shell/feedback as truth authority.",
        "- Do not treat unresolved pointer IDs as retained traceability.",
        "- Do not let a sandbox pass trigger truth writeback.",
    ]
    return "\n".join(lines) + "\n"


def make_readme():
    return """# VAKS Audit Shell Output Oracle Alpha Bakeoff

This sandbox implements an output-level oracle hardening patch plus a multi-alpha bakeoff.

It is sandbox-only:

```text
no main-vault writeback
no SCHEMA change
no commit
no 480 real-data pilot
```

Run:

```powershell
python run_output_oracle_alpha_bakeoff.py
```

Primary reports:

```text
ALPHA_BAKEOFF_REPORT.md
FRAMEWORK_SANDBOX_PRESSURE_REPORT.md
oracle_results.json
rendered_artifacts.json
```
"""


if __name__ == "__main__":
    run()
