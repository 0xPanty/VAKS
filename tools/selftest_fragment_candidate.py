#!/usr/bin/env python
"""Self-test fragment_candidate validation behavior."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path
from typing import Any, Callable

import yaml

import validate_fragment_candidate
import validate_source_intake_contract


BODY = "## Fragment\n\nA source-missing fragment can preserve a useful idea without becoming evidence.\n"
ROOT = Path(__file__).resolve().parent.parent


def base_record() -> dict[str, Any]:
    return {
        "schema": validate_fragment_candidate.SCHEMA,
        "record_kind": "fragment_candidate",
        "fragment_id": "urn:uuid:123e4567-e89b-42d3-a456-426614174000",
        "created_at": "2026-07-01T00:00:00+00:00",
        "created_by": "user",
        "knowledge_status": "candidate",
        "candidate_class": "fragment_only",
        "processing_tier": "light",
        "fragment": {
            "kind": "idea",
            "language": "en",
            "content_digest": validate_fragment_candidate.sha256_text(BODY),
            "quote_exactness": "not_applicable",
            "literal_quote_allowed": False,
        },
        "provenance": {
            "status": "self_authored",
            "source_hint": {
                "hint_text": None,
                "possible_title": None,
                "possible_author": None,
                "possible_url": None,
                "possible_platform": None,
                "possible_timeframe": None,
                "hint_confidence": "none",
            },
            "source_recovery": {
                "status": "not_attempted",
                "recovered_source_ref": None,
                "attempts": [],
            },
        },
        "retrieval_policy": {
            "policy_kind": "orientation_only",
            "pack_allowed": "activation_only",
            "action_basis_allowed": False,
            "warning_code": "missing_source_provenance",
        },
        "usage_policy": {
            "pack_content_allowed": False,
            "pack_pointer_allowed": True,
            "action_basis_allowed": False,
            "evidence_support_allowed": False,
            "reviewed_knowledge_allowed": False,
        },
        "state": {
            "fragment_state": "inbox",
            "merged_into": None,
            "discarded_reason": None,
        },
        "tags": ["fragment", "source-missing"],
    }


def write_record(path: Path, data: dict[str, Any], body: str = BODY) -> None:
    frontmatter = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    path.write_text(f"---\n{frontmatter}---\n{body}", encoding="utf-8", newline="\n")


def assert_case(name: str, mutate: Callable[[dict[str, Any]], None] | None, should_pass: bool) -> None:
    data = copy.deepcopy(base_record())
    if mutate is not None:
        mutate(data)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / f"{name}.md"
        write_record(path, data)
        report = validate_fragment_candidate.validate_paths([path])
        passed = report["status"] == "pass"
        if passed != should_pass:
            raise AssertionError(f"{name}: expected pass={should_pass}, got {json.dumps(report, ensure_ascii=False, indent=2)}")


def assert_contract_case(name: str, mutate: Callable[[dict[str, Any]], None] | None, should_pass: bool) -> None:
    data = copy.deepcopy(base_record())
    if mutate is not None:
        mutate(data)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        rel = Path("fragments") / f"{name}.md"
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        write_record(path, data)
        registry = validate_source_intake_contract.load_registry(ROOT)
        issues: list[dict[str, Any]] = []
        validate_source_intake_contract.validate_file(root, rel, registry, issues)
        passed = not [issue for issue in issues if issue["severity"] == "error"]
        if passed != should_pass:
            raise AssertionError(f"{name}: expected contract pass={should_pass}, got {json.dumps(issues, ensure_ascii=False, indent=2)}")


def assert_both_case(name: str, mutate: Callable[[dict[str, Any]], None] | None, should_pass: bool) -> None:
    assert_case(f"{name}-dedicated", mutate, should_pass)
    assert_contract_case(f"{name}-contract", mutate, should_pass)


def test_valid_self_authored_idea() -> None:
    assert_case("valid-self-authored-idea", None, True)


def test_valid_source_hint_claim_like() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["fragment"]["kind"] = "claim_like"
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Maybe from a provenance design paper."
        data["provenance"]["source_hint"]["hint_confidence"] = "low"
        data["provenance"]["source_recovery"]["status"] = "needed"
        data["state"]["fragment_state"] = "source_recovery_needed"

    assert_case("valid-source-hint-claim-like", mutate, True)


def test_valid_quote_like_unverified() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["fragment"]["kind"] = "quote_like"
        data["fragment"]["quote_exactness"] = "unverified"

    assert_case("valid-quote-like-unverified", mutate, True)


def test_invalid_fragment_with_source_id() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["source_id"] = "vsrc:1:repo:github.com/example/example"

    assert_case("invalid-source-id", mutate, False)


def test_invalid_evidence_support_allowed() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["usage_policy"]["evidence_support_allowed"] = True

    assert_case("invalid-evidence-support", mutate, False)


def test_invalid_action_basis_allowed() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["retrieval_policy"]["action_basis_allowed"] = True

    assert_case("invalid-action-basis", mutate, False)


def test_invalid_quote_like_literal_without_source() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["fragment"]["kind"] = "quote_like"
        data["fragment"]["quote_exactness"] = "not_applicable"
        data["fragment"]["literal_quote_allowed"] = True

    assert_case("invalid-quote-like-literal", mutate, False)


def test_invalid_merged_without_target() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["state"]["fragment_state"] = "merged"

    assert_case("invalid-merged-without-target", mutate, False)


def test_invalid_digest_mismatch() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["fragment"]["content_digest"] = "sha256:" + "0" * 64

    assert_case("invalid-digest", mutate, False)


def test_invalid_source_unknown_with_hint() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_unknown"
        data["provenance"]["source_hint"]["hint_text"] = "I remember a title."

    assert_case("invalid-source-unknown-with-hint", mutate, False)


def test_invalid_recovered_source_ref_when_not_found() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Maybe from a paper."
        data["provenance"]["source_hint"]["hint_confidence"] = "low"
        data["provenance"]["source_recovery"]["status"] = "needed"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "source_card:abc"

    assert_case("invalid-recovered-ref-when-not-found", mutate, False)


def test_invalid_source_unknown_with_found_source_ref() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_unknown"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "source_card:abc"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": "source_card:abc"}

    assert_case("invalid-source-unknown-with-found-ref", mutate, False)


def test_invalid_found_source_not_merged() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Maybe from a paper."
        data["provenance"]["source_hint"]["hint_confidence"] = "low"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "source_card:abc"

    assert_case("invalid-found-source-not-merged", mutate, False)


def test_invalid_non_merged_with_merged_into() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["state"]["merged_into"] = {"kind": "source_card", "ref": "source_card:abc"}

    assert_case("invalid-non-merged-with-target", mutate, False)


def test_valid_merged_source_card_target() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered from a source card."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "raw/articles/example-source.md"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": "raw/articles/example-source.md"}

    assert_case("valid-merged-source-card", mutate, True)


def test_valid_merged_source_annotation_target() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "memory_trace"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered a matching source span."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "outputs/review/source_annotations/example/ann-001.md"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_annotation", "ref": "outputs/review/source_annotations/example/ann-001.md"}

    assert_case("valid-merged-source-annotation", mutate, True)


def test_valid_merged_candidate_distillation_target() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "candidate_distillation", "ref": "outputs/review/example-candidate-distillation.md"}

    assert_case("valid-merged-candidate-distillation", mutate, True)


def test_invalid_recovered_source_ref_object() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = {"ref": "raw/articles/example-source.md"}
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": "raw/articles/example-source.md"}

    assert_case("invalid-recovered-ref-object", mutate, False)


def test_invalid_recovered_source_ref_list() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = ["raw/articles/example-source.md"]
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": "raw/articles/example-source.md"}

    assert_case("invalid-recovered-ref-list", mutate, False)


def test_invalid_merged_into_ref_object() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "raw/articles/example-source.md"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": {"path": "raw/articles/example-source.md"}}

    assert_case("invalid-merged-ref-object", mutate, False)


def test_invalid_merged_into_ref_list() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "raw/articles/example-source.md"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": ["raw/articles/example-source.md"]}

    assert_case("invalid-merged-ref-list", mutate, False)


def test_contract_rejects_nested_source_id_in_recovery_attempt() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_recovery"]["attempts"] = [
            {"source_id": "vsrc:1:repo:github.com/example/example"}
        ]

    assert_contract_case("contract-rejects-nested-source-id", mutate, False)


def test_contract_rejects_nested_source_ref_in_recovery_attempt() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_recovery"]["attempts"] = [
            {"source_ref": "raw/articles/example.md"}
        ]

    assert_contract_case("contract-rejects-nested-source-ref", mutate, False)


def test_contract_rejects_nested_evidence_packet_ref() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_recovery"]["attempts"] = [
            {"evidence_packet_ref": "wiki/evidence/example.md"}
        ]

    assert_contract_case("contract-rejects-evidence-packet-ref", mutate, False)


def test_contract_allows_state_merged_into_ref() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "raw/articles/example-source.md"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": "raw/articles/example-source.md"}

    assert_contract_case("contract-allows-merged-ref", mutate, True)


def test_contract_allows_recovered_source_ref_under_state_rules() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "memory_trace"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source span."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "outputs/review/source_annotations/example/ann-001.md"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_annotation", "ref": "outputs/review/source_annotations/example/ann-001.md"}

    assert_contract_case("contract-allows-recovered-source-ref", mutate, True)


def test_contract_rejects_recovered_source_ref_object() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = {"ref": "raw/articles/example-source.md"}
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": "raw/articles/example-source.md"}

    assert_contract_case("contract-rejects-recovered-ref-object", mutate, False)


def test_contract_rejects_recovered_source_ref_list() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = ["raw/articles/example-source.md"]
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": "raw/articles/example-source.md"}

    assert_contract_case("contract-rejects-recovered-ref-list", mutate, False)


def test_contract_rejects_merged_into_ref_object() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "raw/articles/example-source.md"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": {"path": "raw/articles/example-source.md"}}

    assert_contract_case("contract-rejects-merged-ref-object", mutate, False)


def test_contract_rejects_merged_into_ref_list() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "raw/articles/example-source.md"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": ["raw/articles/example-source.md"]}

    assert_contract_case("contract-rejects-merged-ref-list", mutate, False)


def test_invalid_extra_fragment_evidence_support_status() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["fragment"]["evidence_support_status"] = "supported"

    assert_both_case("invalid-extra-fragment-evidence-support-status", mutate, False)


def test_invalid_extra_fragment_action_basis_allowed() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["fragment"]["action_basis_allowed"] = True

    assert_both_case("invalid-extra-fragment-action-basis-allowed", mutate, False)


def test_invalid_extra_retrieval_pack_content_allowed() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["retrieval_policy"]["pack_content_allowed"] = True

    assert_both_case("invalid-extra-retrieval-pack-content-allowed", mutate, False)


def test_invalid_extra_usage_evidence_support_status() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["usage_policy"]["evidence_support_status"] = "supported"

    assert_both_case("invalid-extra-usage-evidence-support-status", mutate, False)


def test_invalid_extra_source_hint_source_url() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_hint"]["source_url"] = "https://example.com"

    assert_both_case("invalid-extra-source-hint-source-url", mutate, False)


def test_valid_source_hint_possible_url() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "May come from this page."
        data["provenance"]["source_hint"]["possible_url"] = "https://example.com/source"
        data["provenance"]["source_hint"]["hint_confidence"] = "low"

    assert_both_case("valid-source-hint-possible-url", mutate, True)


def test_invalid_extra_provenance_source_url() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_url"] = "https://example.com"

    assert_both_case("invalid-extra-provenance-source-url", mutate, False)


def test_valid_recovery_attempt_with_neutral_query_field() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_recovery"]["attempts"] = [
            {
                "method": "manual_memory",
                "query": "remembered paper title",
                "outcome": "not_found",
                "result_ref": "search-log:abc",
            }
        ]

    assert_both_case("valid-recovery-attempt-neutral-query", mutate, True)


def test_invalid_recovery_attempt_with_source_id() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_recovery"]["attempts"] = [
            {"source_id": "vsrc:1:repo:github.com/example/example"}
        ]

    assert_both_case("invalid-recovery-attempt-source-id", mutate, False)


def test_invalid_recovery_attempt_with_evidence_support_status() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_recovery"]["attempts"] = [
            {"evidence_support_status": "supported"}
        ]

    assert_both_case("invalid-recovery-attempt-evidence-support-status", mutate, False)


def test_invalid_attempt_recovered_source_ref() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_recovery"]["attempts"] = [
            {"recovered_source_ref": "source_card:abc"}
        ]

    assert_both_case("invalid-attempt-recovered-source-ref", mutate, False)


def test_invalid_attempt_merged_into() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_recovery"]["attempts"] = [
            {"merged_into": {"kind": "source_card", "ref": "raw/articles/x.md"}}
        ]

    assert_both_case("invalid-attempt-merged-into", mutate, False)


def assert_invalid_attempt_formal_ref(field: str, value: Any | None = None) -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_recovery"]["attempts"] = [
            {field: value if value is not None else "formal-ref:x"}
        ]

    assert_both_case(f"invalid-attempt-{field.replace('_', '-')}", mutate, False)


def test_invalid_attempt_source_anchor_ref() -> None:
    assert_invalid_attempt_formal_ref("source_anchor_ref", "outputs/review/source_annotations/example/ann-001.md")


def test_invalid_attempt_source_anchor() -> None:
    assert_invalid_attempt_formal_ref("source_anchor", "outputs/review/source_annotations/example/ann-001.md")


def test_invalid_attempt_source_card_ref() -> None:
    assert_invalid_attempt_formal_ref("source_card_ref", "raw/articles/example.md")


def test_invalid_attempt_source_capture_ref() -> None:
    assert_invalid_attempt_formal_ref("source_capture_ref", "raw/captures/example/capture-envelope.json")


def test_invalid_attempt_capture_ref() -> None:
    assert_invalid_attempt_formal_ref("capture_ref", "urn:uuid:00000000-0000-4000-8000-000000000001")


def test_invalid_attempt_annotation_ref() -> None:
    assert_invalid_attempt_formal_ref("annotation_ref", "outputs/review/source_annotations/example/ann-001.md")


def test_invalid_attempt_evidence_ref() -> None:
    assert_invalid_attempt_formal_ref("evidence_ref", "outputs/review/evidence-packet-x.md")


def test_invalid_attempt_evidence_support_ref() -> None:
    assert_invalid_attempt_formal_ref("evidence_support_ref", "outputs/review/evidence-packet-x.md")


def test_invalid_attempt_review_ref() -> None:
    assert_invalid_attempt_formal_ref("review_ref", "wiki/reviews/example.md")


def test_invalid_attempt_reviewed_knowledge_ref() -> None:
    assert_invalid_attempt_formal_ref("reviewed_knowledge_ref", "wiki/claims/example.md")


def test_invalid_attempt_action_ref() -> None:
    assert_invalid_attempt_formal_ref("action_ref", "outputs/actions/action-x.md")


def test_invalid_attempt_action_basis_ref() -> None:
    assert_invalid_attempt_formal_ref("action_basis_ref", "outputs/actions/action-x.md")


def test_invalid_attempt_source() -> None:
    assert_invalid_attempt_formal_ref("source", "raw/articles/example.md")


def test_invalid_attempt_evidence() -> None:
    assert_invalid_attempt_formal_ref("evidence", "outputs/review/evidence-packet-x.md")


def test_invalid_attempt_review() -> None:
    assert_invalid_attempt_formal_ref("review", "wiki/reviews/example.md")


def test_invalid_attempt_action() -> None:
    assert_invalid_attempt_formal_ref("action", "outputs/actions/action-x.md")


def test_invalid_attempt_target() -> None:
    assert_invalid_attempt_formal_ref("target", "wiki/claims/example.md")


def test_invalid_attempt_citation() -> None:
    assert_invalid_attempt_formal_ref("citation", "https://example.com/source")


def test_invalid_attempt_source_url() -> None:
    assert_invalid_attempt_formal_ref("source_url", "https://example.com/source")


def test_invalid_attempt_source_locator() -> None:
    assert_invalid_attempt_formal_ref("source_locator", "raw/articles/example.md")


def test_invalid_attempt_authority() -> None:
    assert_invalid_attempt_formal_ref("authority", "source")


def test_invalid_attempt_support() -> None:
    assert_invalid_attempt_formal_ref("support", "supported")


def test_invalid_attempt_claim_support() -> None:
    assert_invalid_attempt_formal_ref("claim_support", "supported")


def test_invalid_attempt_item_reviewed() -> None:
    assert_invalid_attempt_formal_ref("itemReviewed", "raw/articles/example.md")


def test_invalid_attempt_sources() -> None:
    assert_invalid_attempt_formal_ref("sources", ["raw/articles/example.md"])


def test_invalid_attempt_source_uri() -> None:
    assert_invalid_attempt_formal_ref("source_uri", "raw/articles/example.md")


def test_invalid_attempt_source_urls() -> None:
    assert_invalid_attempt_formal_ref("source_urls", ["https://example.com/source"])


def test_invalid_attempt_source_reference() -> None:
    assert_invalid_attempt_formal_ref("sourceReference", "raw/articles/example.md")


def test_invalid_attempt_evidence_support_camel_case() -> None:
    assert_invalid_attempt_formal_ref("evidenceSupport", "outputs/review/evidence-packet-x.md")


def test_invalid_attempt_action_basis_camel_case() -> None:
    assert_invalid_attempt_formal_ref("actionBasis", "outputs/actions/action-x.md")


def test_invalid_attempt_reviewed_knowledge_camel_case() -> None:
    assert_invalid_attempt_formal_ref("reviewedKnowledge", "wiki/claims/example.md")


def test_invalid_attempt_authority_aliases() -> None:
    aliases = [
        "source_uris",
        "sourceUrl",
        "evidences",
        "reviews",
        "actions",
        "targets",
        "citations",
        "authorities",
        "supports",
        "claimSupport",
        "item_reviewed",
    ]
    for alias in aliases:
        assert_invalid_attempt_formal_ref(alias, "formal-ref:x")


def test_invalid_attempt_non_object() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["source_recovery"]["attempts"] = ["remembered phrase"]

    assert_both_case("invalid-attempt-non-object", mutate, False)


def test_valid_state_merged_into_still_allowed() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "source_hint_only"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "raw/articles/example-source.md"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_card", "ref": "raw/articles/example-source.md"}

    assert_both_case("valid-state-merged-into-still-allowed", mutate, True)


def test_valid_source_recovery_recovered_source_ref_when_found() -> None:
    def mutate(data: dict[str, Any]) -> None:
        data["provenance"]["status"] = "memory_trace"
        data["provenance"]["source_hint"]["hint_text"] = "Recovered source span."
        data["provenance"]["source_hint"]["hint_confidence"] = "medium"
        data["provenance"]["source_recovery"]["status"] = "found"
        data["provenance"]["source_recovery"]["recovered_source_ref"] = "outputs/review/source_annotations/example/ann-001.md"
        data["state"]["fragment_state"] = "merged"
        data["state"]["merged_into"] = {"kind": "source_annotation", "ref": "outputs/review/source_annotations/example/ann-001.md"}

    assert_both_case("valid-source-recovery-recovered-ref-when-found", mutate, True)


def test_directory_scan_ignores_readme() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "README.md").write_text("# Fragment docs\n", encoding="utf-8")
        write_record(root / "valid.fragment.md", base_record())
        report = validate_fragment_candidate.validate_paths([root])
        if report["status"] != "pass" or report["files_scanned"] != 1:
            raise AssertionError(f"directory scan should ignore README.md: {json.dumps(report, ensure_ascii=False, indent=2)}")


def run() -> None:
    tests = [
        test_valid_self_authored_idea,
        test_valid_source_hint_claim_like,
        test_valid_quote_like_unverified,
        test_invalid_fragment_with_source_id,
        test_invalid_evidence_support_allowed,
        test_invalid_action_basis_allowed,
        test_invalid_quote_like_literal_without_source,
        test_invalid_merged_without_target,
        test_invalid_digest_mismatch,
        test_invalid_source_unknown_with_hint,
        test_invalid_recovered_source_ref_when_not_found,
        test_invalid_source_unknown_with_found_source_ref,
        test_invalid_found_source_not_merged,
        test_invalid_non_merged_with_merged_into,
        test_valid_merged_source_card_target,
        test_valid_merged_source_annotation_target,
        test_valid_merged_candidate_distillation_target,
        test_invalid_recovered_source_ref_object,
        test_invalid_recovered_source_ref_list,
        test_invalid_merged_into_ref_object,
        test_invalid_merged_into_ref_list,
        test_contract_rejects_nested_source_id_in_recovery_attempt,
        test_contract_rejects_nested_source_ref_in_recovery_attempt,
        test_contract_rejects_nested_evidence_packet_ref,
        test_contract_allows_state_merged_into_ref,
        test_contract_allows_recovered_source_ref_under_state_rules,
        test_contract_rejects_recovered_source_ref_object,
        test_contract_rejects_recovered_source_ref_list,
        test_contract_rejects_merged_into_ref_object,
        test_contract_rejects_merged_into_ref_list,
        test_invalid_extra_fragment_evidence_support_status,
        test_invalid_extra_fragment_action_basis_allowed,
        test_invalid_extra_retrieval_pack_content_allowed,
        test_invalid_extra_usage_evidence_support_status,
        test_invalid_extra_source_hint_source_url,
        test_valid_source_hint_possible_url,
        test_invalid_extra_provenance_source_url,
        test_valid_recovery_attempt_with_neutral_query_field,
        test_invalid_recovery_attempt_with_source_id,
        test_invalid_recovery_attempt_with_evidence_support_status,
        test_invalid_attempt_recovered_source_ref,
        test_invalid_attempt_merged_into,
        test_invalid_attempt_source_anchor_ref,
        test_invalid_attempt_source_anchor,
        test_invalid_attempt_source_card_ref,
        test_invalid_attempt_source_capture_ref,
        test_invalid_attempt_capture_ref,
        test_invalid_attempt_annotation_ref,
        test_invalid_attempt_evidence_ref,
        test_invalid_attempt_evidence_support_ref,
        test_invalid_attempt_review_ref,
        test_invalid_attempt_reviewed_knowledge_ref,
        test_invalid_attempt_action_ref,
        test_invalid_attempt_action_basis_ref,
        test_invalid_attempt_source,
        test_invalid_attempt_evidence,
        test_invalid_attempt_review,
        test_invalid_attempt_action,
        test_invalid_attempt_target,
        test_invalid_attempt_citation,
        test_invalid_attempt_source_url,
        test_invalid_attempt_source_locator,
        test_invalid_attempt_authority,
        test_invalid_attempt_support,
        test_invalid_attempt_claim_support,
        test_invalid_attempt_item_reviewed,
        test_invalid_attempt_sources,
        test_invalid_attempt_source_uri,
        test_invalid_attempt_source_urls,
        test_invalid_attempt_source_reference,
        test_invalid_attempt_evidence_support_camel_case,
        test_invalid_attempt_action_basis_camel_case,
        test_invalid_attempt_reviewed_knowledge_camel_case,
        test_invalid_attempt_authority_aliases,
        test_invalid_attempt_non_object,
        test_valid_state_merged_into_still_allowed,
        test_valid_source_recovery_recovered_source_ref_when_found,
        test_directory_scan_ignores_readme,
    ]
    for test in tests:
        test()
    print(json.dumps({"status": "pass", "tests": len(tests)}, indent=2))


if __name__ == "__main__":
    run()
