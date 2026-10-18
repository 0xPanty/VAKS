#!/usr/bin/env python3
"""
Sandbox-only P1.5-14 raw intake parser router validator.

This prototype validates synthetic raw-intake parser routing manifests. It
proves the contract shape for modality routing, parser configuration capture,
retained extraction bundles, source anchors, and VAKS authority boundaries.

It is read-only, uses only the Python standard library, does not parse real
sources, does not install parser dependencies, and does not write raw/wiki/vault
artifacts.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

RECORD_KIND = "raw_intake_parser_router_manifest"

KNOWN_SOURCE_TYPES = {
    "document",
    "pdf",
    "ppt",
    "word",
    "image",
    "screenshot",
    "audio",
    "video",
    "web_page",
    "repo_snapshot",
    "chat_export",
    "other",
}

SOURCE_MODALITY = {
    "document": "document",
    "pdf": "document",
    "ppt": "document",
    "word": "document",
    "image": "image",
    "screenshot": "image",
    "audio": "audio",
    "video": "video",
    "web_page": "web",
    "repo_snapshot": "repo",
    "chat_export": "chat",
    "other": "other",
}

ROUTE_MODALITY = {
    "document_parse": "document",
    "image_ocr": "image",
    "audio_transcript": "audio",
    "video_transcript": "video",
    "public_web_capture": "web",
    "repo_snapshot_parse": "repo",
    "chat_export_parse": "chat",
    "generic_manual_capture": "other",
}

ALLOWED_KNOWLEDGE_STATUS = {"raw", "candidate"}

FORBIDDEN_AUTHORITY_CLAIMS = {
    "support",
    "direct_support",
    "inferential_support",
    "reviewed_support",
    "truth",
    "truth_confidence",
    "reviewed_knowledge",
    "reviewed_relation",
    "reviewer_approval",
    "evidence_support",
    "action_basis",
    "ready_action_basis",
    "action_ready",
    "promotion",
    "promotion_ready",
    "mainline_ready",
    "mainline_readiness",
    "source_of_record",
}

CLAIM_FIELDS = {
    "claims",
    "artifact_claims",
    "output_claims",
    "route_claims",
    "parser_claims",
    "source_card_claims",
    "evidence_claims",
    "receipt_claims",
}

AUTHORITY_BOOL_FIELDS = {
    "parser_output_is_support",
    "parser_markdown_as_reviewed_knowledge",
    "parser_markdown_is_reviewed",
    "ocr_as_evidence_support",
    "transcript_as_support",
    "crawler_text_as_support",
    "output_as_support",
    "output_claims_support",
    "evidence_support_created",
    "reviewed_knowledge_created",
    "reviewed_relation_created",
    "reviewer_approval_claimed",
    "action_basis_allowed",
    "truth_mutation_allowed",
    "promotion_ready",
    "mainline_ready",
    "support_ready",
}

PROTECTED_TARGET_PREFIXES = {
    "h:/obsidian/",
    "h:\\obsidian\\",
    "wiki/claims/",
    "wiki/patterns/",
    "wiki/decisions/",
    "templates/",
    "tools/",
}

PROTECTED_TARGET_EXACTS = {
    "h:/obsidian",
    "wiki/claims",
    "wiki/patterns",
    "wiki/decisions",
    "templates",
    "tools",
}

PROTECTED_TARGET_FILES = {
    "schema.md",
    "architecture_principles.md",
    "fusion_architecture_v0_2_draft.md",
    "readme.md",
}

SOURCE_CARD_FORBIDDEN_FIELDS = {
    "relations",
    "confidence",
    "freshness",
    "relevance",
    "source_quality",
    "cross_source_count",
    "truth_score",
    "truth_confidence",
    "adopted",
    "rejected",
    "must_use",
    "universal_ban",
    "review_verdict",
    "decision_outcome",
    "accepted",
}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    item_id: str = ""

    def as_dict(self) -> dict[str, str]:
        result = {"code": self.code, "message": self.message}
        if self.item_id:
            result["item_id"] = self.item_id
        return result


def norm(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip().lower().replace("\\", "/").replace(" ", "_").replace("-", "_")


def path_norm(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/").lower()


def raw_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return norm(value) in {"true", "yes", "1"}


def as_list(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [norm(item) for item in value if norm(item)]
    return [norm(item) for item in str(value).split(",") if norm(item)]


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, list):
        return any(has_value(item) for item in value)
    if isinstance(value, dict):
        return bool(value)
    return str(value).strip() != ""


def add_once(issues: list[Issue], code: str, message: str, item_id: str = "") -> None:
    key = (code, item_id)
    if key not in {(issue.code, issue.item_id) for issue in issues}:
        issues.append(Issue(code, message, item_id))


def item_id(item: dict[str, Any]) -> str:
    return raw_text(item.get("id")) or raw_text(item.get("path")) or raw_text(item.get("kind")) or "<unknown>"


def sha256_like(value: Any) -> bool:
    text = raw_text(value).lower()
    return text.startswith("sha256:") and len(text.split("sha256:", 1)[1]) >= 16


def md5_like(value: Any) -> bool:
    text = raw_text(value).lower()
    return text.startswith("md5:") or norm(value) == "md5"


def deep_merge(base: Any, patch: Any) -> Any:
    if isinstance(base, dict) and isinstance(patch, dict):
        result = dict(base)
        for key, value in patch.items():
            result[key] = deep_merge(result.get(key), value)
        return result
    return patch


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"manifest must be a JSON object: {path}")
    return data


def load_manifest(path: Path) -> dict[str, Any]:
    path = path.resolve()
    root = Path(__file__).resolve().parents[1]
    data = load_json(path)
    if not has_value(data.get("extends")):
        return data

    base_path = (root / raw_text(data["extends"])).resolve()
    if root.resolve() not in base_path.parents and base_path != root.resolve():
        raise ValueError(f"extends path escapes sandbox root: {data['extends']}")

    base = load_manifest(base_path)
    patched = deep_merge(base, data.get("patch", {}))
    overlay = {key: value for key, value in data.items() if key not in {"extends", "patch"}}
    return deep_merge(patched, overlay)


def collect_claims(item: dict[str, Any]) -> set[str]:
    claims: set[str] = set()
    for field in CLAIM_FIELDS:
        claims.update(as_list(item.get(field)))
    return claims


def protected_target(value: Any) -> bool:
    text = path_norm(value)
    if not text:
        return False
    trimmed = text.lstrip("./")
    if ".codex/" in trimmed or trimmed.startswith(".codex/"):
        return True
    if trimmed.rstrip("/") in PROTECTED_TARGET_EXACTS:
        return True
    if trimmed in PROTECTED_TARGET_FILES:
        return True
    return any(trimmed.startswith(prefix) for prefix in PROTECTED_TARGET_PREFIXES)


def scan_authority_confusion(value: Any, issues: list[Issue], path: str = "$") -> None:
    if isinstance(value, dict):
        claims = collect_claims(value)
        if claims.intersection(FORBIDDEN_AUTHORITY_CLAIMS):
            add_once(
                issues,
                "RP_AUTHORITY_CLAIM_FORBIDDEN",
                "raw parser routing artifacts cannot claim support, truth, review approval, action basis, or mainline readiness.",
                path,
            )

        for key, field_value in value.items():
            field_name = norm(key)
            if field_name in FORBIDDEN_AUTHORITY_CLAIMS and (
                as_bool(field_value) or (not isinstance(field_value, bool) and has_value(field_value))
            ):
                add_once(
                    issues,
                    "RP_AUTHORITY_CLAIM_FORBIDDEN",
                    "direct authority fields are forbidden in raw parser routing artifacts.",
                    f"{path}.{key}",
                )
            if field_name in AUTHORITY_BOOL_FIELDS and as_bool(field_value):
                add_once(
                    issues,
                    "RP_AUTHORITY_CONFUSION",
                    "raw parser routing fields cannot assert support, truth mutation, action basis, promotion, or mainline readiness.",
                    f"{path}.{key}",
                )
            scan_authority_confusion(field_value, issues, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_authority_confusion(item, issues, f"{path}[{index}]")


def validate_original(original: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(original, dict):
        add_once(issues, "RP_MISSING_ORIGINAL", "original block is required.")
        return issues

    if not has_value(original.get("path")):
        add_once(issues, "RP_ORIGINAL_PATH_MISSING", "original.path is required.")

    if not has_value(original.get("sha256")) or not sha256_like(original.get("sha256")):
        add_once(issues, "RP_ORIGINAL_HASH_MISSING", "original.sha256 must be sha256-like.")

    if md5_like(original.get("sha256")) or norm(original.get("hash_algorithm")) == "md5":
        add_once(issues, "RP_WEAK_HASH", "MD5 cannot be used as the preserved original hash.")

    source_type = norm(original.get("source_type"))
    if source_type not in KNOWN_SOURCE_TYPES:
        add_once(issues, "RP_UNKNOWN_SOURCE_TYPE", "source_type must be a known raw intake type.")

    if (
        as_bool(original.get("private_or_account_content"))
        or as_bool(original.get("uses_cookies"))
        or norm(original.get("access_mode")) in {"private", "private_account", "account"}
    ) and not as_bool(original.get("explicit_user_authorization")):
        add_once(
            issues,
            "RP_PRIVATE_ACCESS_UNAUTHORIZED",
            "private/account/cookie-based capture requires explicit user authorization.",
        )

    return issues


def validate_router(router: Any, original: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(router, dict):
        add_once(issues, "RP_MISSING_ROUTER", "router block is required.")
        return issues

    modality = norm(router.get("modality"))
    route = norm(router.get("route"))
    source_type = norm(original.get("source_type")) if isinstance(original, dict) else ""
    expected_modality = SOURCE_MODALITY.get(source_type)
    route_modality = ROUTE_MODALITY.get(route)

    if modality not in set(SOURCE_MODALITY.values()):
        add_once(issues, "RP_UNKNOWN_MODALITY", "router.modality must be known.")

    if route not in ROUTE_MODALITY:
        add_once(issues, "RP_UNKNOWN_ROUTE", "router.route must be known.")

    if expected_modality and modality and modality != expected_modality:
        add_once(issues, "RP_ROUTE_MODALITY_MISMATCH", "router.modality must match original.source_type.")

    if route_modality and modality and route_modality != modality:
        add_once(issues, "RP_ROUTE_MODALITY_MISMATCH", "router.route must match router.modality.")

    if not as_bool(router.get("lazy_routing")):
        add_once(issues, "RP_LAZY_ROUTING_REQUIRED", "parser routing must be lazy, not always-on.")

    if as_bool(router.get("heavy_parser_always_on")):
        add_once(issues, "RP_HEAVY_PARSER_ALWAYS_ON", "heavy parsers cannot run by default for ordinary capture.")

    if not has_value(router.get("selected_adapter")):
        add_once(issues, "RP_SELECTED_ADAPTER_MISSING", "router.selected_adapter is required.")

    if not has_value(router.get("selected_by")):
        add_once(issues, "RP_SELECTED_BY_MISSING", "router.selected_by must record route trace metadata.")

    if as_bool(router.get("classifier_confidence_claims_truth")) or as_bool(router.get("route_confidence_claims_truth")):
        add_once(issues, "RP_ROUTER_CONFIDENCE_AS_TRUTH", "router/classifier confidence is routing metadata, not truth.")

    return issues


def validate_parser(parser: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(parser, dict):
        add_once(issues, "RP_MISSING_PARSER", "parser block is required.")
        return issues

    required = {"adapter_name", "adapter_version", "runtime", "parser_config_hash", "known_limits"}
    missing = sorted(field for field in required if not has_value(parser.get(field)))
    if missing:
        add_once(issues, "RP_PARSER_CONFIG_MISSING", f"parser config missing fields: {missing}.")

    if has_value(parser.get("parser_config_hash")) and not sha256_like(parser.get("parser_config_hash")):
        add_once(issues, "RP_PARSER_CONFIG_MISSING", "parser_config_hash must be sha256-like.")

    if as_bool(parser.get("installed_dependency")) or as_bool(parser.get("dependency_install_requested")):
        add_once(issues, "RP_DEPENDENCY_INSTALL_FORBIDDEN", "this sandbox cannot install parser dependencies.")

    if as_bool(parser.get("full_runtime_core_dependency")) or as_bool(parser.get("core_dependency")):
        add_once(issues, "RP_RUNTIME_CORE_DEPENDENCY_FORBIDDEN", "full parser runtime cannot become a core VAKS dependency here.")

    license_family = norm(parser.get("license_family"))
    if license_family in {"gpl", "agpl", "marker_derived", "unknown"} and not as_bool(parser.get("license_reviewed")):
        add_once(issues, "RP_LICENSE_REVIEW_REQUIRED", "GPL/AGPL/unknown parser lineage requires license review before product import.")

    if norm(parser.get("model_locality")) in {"cloud_default", "unknown"} and not as_bool(parser.get("locality_reviewed")):
        add_once(issues, "RP_MODEL_LOCALITY_UNREVIEWED", "cloud/default/unknown model locality requires review.")

    if as_bool(parser.get("parser_confidence_claims_truth")) or as_bool(parser.get("extraction_confidence_claims_truth")):
        add_once(issues, "RP_PARSER_CONFIDENCE_AS_TRUTH", "parser confidence is extraction quality metadata, not truth confidence.")

    return issues


def output_items(outputs: dict[str, Any]) -> list[dict[str, Any]]:
    retained = outputs.get("retained_outputs", [])
    if isinstance(retained, list):
        return [item for item in retained if isinstance(item, dict)]
    return []


def validate_outputs(outputs: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(outputs, dict):
        add_once(issues, "RP_MISSING_OUTPUTS", "outputs block is required.")
        return issues

    retained = output_items(outputs)
    if not retained:
        add_once(issues, "RP_RETAINED_OUTPUTS_MISSING", "at least one retained output object is required.")

    if not has_value(outputs.get("metadata_path")):
        add_once(issues, "RP_RETAINED_OUTPUTS_MISSING", "metadata_path is required for the extraction bundle.")

    if as_bool(outputs.get("scratch_only")):
        add_once(issues, "RP_OUTPUT_SCRATCH_ONLY", "parser output cannot live only in scratch.")

    for field in ("markdown_path", "json_path", "metadata_path", "chunks_path", "images_dir"):
        if has_value(outputs.get(field)) and protected_target(outputs.get(field)):
            add_once(issues, "RP_PROTECTED_PATH_TARGET", "extraction output targets a protected or scratch path.", field)

    for item in retained:
        current_id = item_id(item)
        if not has_value(item.get("path")) or not has_value(item.get("kind")):
            add_once(issues, "RP_RETAINED_OUTPUTS_MISSING", "retained output needs kind and path.", current_id)
        if has_value(item.get("path")) and protected_target(item.get("path")):
            add_once(issues, "RP_PROTECTED_PATH_TARGET", "retained output targets a protected or scratch path.", current_id)
        if not sha256_like(item.get("output_hash")):
            add_once(issues, "RP_OUTPUT_HASH_MISSING", "retained output needs sha256 output_hash.", current_id)
        if norm(item.get("knowledge_status")) not in ALLOWED_KNOWLEDGE_STATUS:
            add_once(issues, "RP_OUTPUT_STATUS_NOT_RAW_OR_CANDIDATE", "retained parser output must stay raw or candidate.", current_id)

    return issues


def validate_anchors(anchors: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(anchors, dict):
        add_once(issues, "RP_MISSING_ANCHORS", "anchors block is required.")
        return issues

    anchor_lists = []
    for field in ("page_refs", "timestamp_refs", "region_refs", "url_refs"):
        value = anchors.get(field, [])
        if isinstance(value, list):
            anchor_lists.extend(item for item in value if isinstance(item, dict))

    if not anchor_lists:
        add_once(issues, "RP_ANCHORS_MISSING", "at least one page/timestamp/region/url anchor is required.")

    if not as_bool(anchors.get("source_hash_on_anchors")):
        add_once(issues, "RP_ANCHOR_HASH_MISSING", "anchors must carry source_hash_on_anchors: true.")

    for anchor in anchor_lists:
        current_id = item_id(anchor)
        if not has_value(anchor.get("selector")):
            add_once(issues, "RP_ANCHOR_SELECTOR_MISSING", "anchor selector is required.", current_id)
        if not sha256_like(anchor.get("source_hash")):
            add_once(issues, "RP_ANCHOR_HASH_MISSING", "anchor needs sha256 source_hash.", current_id)

    return issues


def validate_boundary(boundary: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(boundary, dict):
        add_once(issues, "RP_MISSING_BOUNDARY", "boundary block is required.")
        return issues

    if norm(boundary.get("knowledge_status")) not in ALLOWED_KNOWLEDGE_STATUS:
        add_once(issues, "RP_OUTPUT_CLAIMS_AUTHORITY", "boundary.knowledge_status must stay raw or candidate.")

    if as_bool(boundary.get("action_basis_allowed")):
        add_once(issues, "RP_ACTION_BASIS_FORBIDDEN", "raw parser output cannot be action basis.")

    if as_bool(boundary.get("truth_mutation_allowed")):
        add_once(issues, "RP_TRUTH_MUTATION_FORBIDDEN", "raw parser output cannot mutate truth.")

    if (
        as_bool(boundary.get("parser_output_is_support"))
        or as_bool(boundary.get("reviewed_knowledge_created"))
        or as_bool(boundary.get("reviewed_relation_created"))
        or as_bool(boundary.get("evidence_support_created"))
        or as_bool(boundary.get("promotion_ready"))
        or as_bool(boundary.get("mainline_ready"))
    ):
        add_once(issues, "RP_OUTPUT_CLAIMS_AUTHORITY", "parser output cannot create support, review, promotion, or readiness.")

    return issues


def validate_source_card(card: Any) -> list[Issue]:
    issues: list[Issue] = []
    if card is None:
        return issues
    if not isinstance(card, dict):
        add_once(issues, "RP_INVALID_SOURCE_CARD", "source_card must be an object when present.")
        return issues

    if norm(card.get("record_kind")) not in {"source_card", "proposed_source_card"}:
        add_once(issues, "RP_INVALID_SOURCE_CARD", "source_card.record_kind must stay source-card shaped.")

    if norm(card.get("knowledge_status")) != "raw":
        add_once(issues, "RP_SOURCE_CARD_NOT_RAW", "source cards are provenance-only raw records.")

    if has_value(card.get("target_path")) and protected_target(card.get("target_path")):
        add_once(issues, "RP_PROTECTED_PATH_TARGET", "source card target path is protected or scratch.")

    forbidden = sorted(field for field in SOURCE_CARD_FORBIDDEN_FIELDS if field in card)
    if forbidden:
        add_once(issues, "RP_SOURCE_CARD_AUTHORITY_FIELD", f"source card contains forbidden authority fields: {forbidden}.")

    retrieval_policy = card.get("retrieval_policy", {})
    if isinstance(retrieval_policy, dict) and as_bool(retrieval_policy.get("action_basis_allowed")):
        add_once(issues, "RP_ACTION_BASIS_FORBIDDEN", "source card retrieval policy cannot allow action basis.")

    return issues


def validate_candidate(candidate: Any) -> list[Issue]:
    issues: list[Issue] = []
    if candidate is None:
        return issues
    if not isinstance(candidate, dict):
        add_once(issues, "RP_INVALID_CANDIDATE_DISTILLATION", "candidate_distillation must be an object when present.")
        return issues

    if norm(candidate.get("knowledge_status")) != "candidate":
        add_once(issues, "RP_CANDIDATE_NOT_CANDIDATE", "candidate distillation must stay candidate.")

    if not as_bool(candidate.get("provisional")):
        add_once(issues, "RP_CANDIDATE_NOT_PROVISIONAL", "candidate distillation must be provisional.")

    retrieval_policy = candidate.get("retrieval_policy", {})
    if isinstance(retrieval_policy, dict) and as_bool(retrieval_policy.get("action_basis_allowed")):
        add_once(issues, "RP_ACTION_BASIS_FORBIDDEN", "candidate distillation cannot allow action basis.")

    return issues


def validate_manifest(manifest: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    if norm(manifest.get("record_kind")) != RECORD_KIND:
        add_once(issues, "RP_INVALID_RECORD_KIND", f"record_kind must be {RECORD_KIND}.")

    if not has_value(manifest.get("scenario_id")):
        add_once(issues, "RP_MISSING_SCENARIO_ID", "scenario_id is required.")

    scan_authority_confusion(manifest, issues)

    original = manifest.get("original", {})
    issues.extend(validate_original(original))
    issues.extend(validate_router(manifest.get("router", {}), original if isinstance(original, dict) else {}))
    issues.extend(validate_parser(manifest.get("parser", {})))
    issues.extend(validate_outputs(manifest.get("outputs", {})))
    issues.extend(validate_anchors(manifest.get("anchors", {})))
    issues.extend(validate_boundary(manifest.get("boundary", {})))
    issues.extend(validate_source_card(manifest.get("source_card")))
    issues.extend(validate_candidate(manifest.get("candidate_distillation")))

    return issues


def summarize(manifest: dict[str, Any], issues: list[Issue]) -> dict[str, Any]:
    return {
        "scenario_id": manifest.get("scenario_id", "<missing>"),
        "valid": not issues,
        "issue_codes": sorted({issue.code for issue in issues}),
        "issues": [issue.as_dict() for issue in issues],
        "non_claims": {
            "parser_pass_not_reviewed_knowledge": True,
            "parser_pass_not_evidence_support": True,
            "parser_pass_not_action_basis": True,
            "parser_pass_not_promotion": True,
            "parser_pass_not_mainline_readiness": True,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="path to a raw parser router manifest JSON file")
    args = parser.parse_args(argv)
    manifest = load_manifest(args.manifest)
    issues = validate_manifest(manifest)
    print(json.dumps(summarize(manifest, issues), indent=2, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
