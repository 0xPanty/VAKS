from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import time
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
STRESS = ROOT / "enterprise_stress"
RESULTS = ROOT / "results"

BAD_ANCHORS = {"ambiguous", "broken", "source_changed"}
ALLOWED_ROLES = [
    "question",
    "possible_support",
    "counterexample",
    "scope_limit",
    "risk_signal",
    "candidate_seed",
    "term_definition",
    "implementation_note",
    "bookmark",
]
FORBIDDEN_FIELDS = {
    "truth_confidence",
    "reviewed_relation",
    "project_borrow_scope",
    "project_non_borrow_scope",
    "decision_outcome",
    "final_support_refs",
    "support_refs",
}
REQUIRED_FIELDS = {
    "record_kind",
    "annotation_id",
    "source_ref",
    "source_hash",
    "selector_type",
    "annotation_role",
    "body_note",
    "anchor_status",
    "anchor_checked_at",
    "lifecycle_state",
    "support_checked",
    "evidence_support_status",
    "retrieval_policy",
    "action_basis_allowed",
    "truth_mutation_allowed",
}
STALE_CUTOFF = date(2026, 3, 16)
YAML_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
YAML_DUMPER = getattr(yaml, "CSafeDumper", yaml.SafeDumper)
ALLOWED_LIFECYCLE = {
    "source_annotated",
    "triaged",
    "routed",
    "repair_needed",
    "repair_candidate",
    "repaired",
    "archived",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def clean_stress() -> None:
    if STRESS.exists():
        shutil.rmtree(STRESS)
    STRESS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)


def source_kind(source_idx: int) -> str:
    return ["web", "video", "repo", "pdf"][source_idx % 4]


def make_source_content(source_idx: int, span_count: int) -> tuple[str, str]:
    kind = source_kind(source_idx)
    lines = [f"# Enterprise Stress Source {source_idx:03d} ({kind})", ""]
    for span_idx in range(span_count):
        lines.append(
            f"Span S{source_idx:03d}-{span_idx:03d}: enterprise annotation fixture "
            f"for {kind} source {source_idx:03d}, span {span_idx:03d}. "
            "The exact locator phrase is intentionally unique for stress testing."
        )
        if kind == "video":
            minute = span_idx // 2
            second = (span_idx * 7) % 60
            lines.append(
                f"[00:{minute:02d}:{second:02d}] Timestamp locator for S{source_idx:03d}-{span_idx:03d}."
            )
        if kind == "repo":
            lines.append(f"line_{span_idx:03d} = 'repo locator S{source_idx:03d}-{span_idx:03d}'")
        if kind == "pdf":
            lines.append(f"PDF page {(span_idx % 12) + 1} rect locator for S{source_idx:03d}-{span_idx:03d}.")
        lines.append("")
    duplicate = f"Duplicate enterprise anchor phrase for source {source_idx:03d} appears twice."
    lines.append(duplicate)
    lines.append(duplicate)
    lines.append("")
    old_lines = list(lines)
    old_lines.insert(3, f"Old snapshot drift marker for source {source_idx:03d}.")
    return "\n".join(lines), "\n".join(old_lines)


def generate_sources(source_count: int, span_count: int) -> dict[int, dict[str, str]]:
    sources: dict[int, dict[str, str]] = {}
    for source_idx in range(source_count):
        content, old_content = make_source_content(source_idx, span_count)
        source_path = STRESS / "sources" / f"source-{source_idx:03d}.md"
        snapshot_path = STRESS / "snapshots" / f"source-{source_idx:03d}-snapshot-v1.md"
        old_snapshot_path = STRESS / "snapshots" / f"source-{source_idx:03d}-snapshot-old.md"
        write_text(source_path, content)
        write_text(snapshot_path, content)
        write_text(old_snapshot_path, old_content)
        sources[source_idx] = {
            "kind": source_kind(source_idx),
            "source_ref": rel(source_path),
            "snapshot_ref": rel(snapshot_path),
            "old_snapshot_ref": rel(old_snapshot_path),
            "hash": sha256_text(content),
            "old_hash": sha256_text(old_content),
            "content": content,
        }
    return sources


def planned_source_indices(count: int, source_count: int) -> list[int]:
    indices = []
    for idx in range(count):
        if idx % 4 != 0:
            indices.append(idx % min(12, source_count))
        else:
            indices.append((idx * 17 + idx // 11) % source_count)
    return indices


def status_for(idx: int) -> tuple[str, bool]:
    if idx % 97 == 0:
        return "broken", False
    if idx % 89 == 0:
        return "source_changed", False
    if idx % 83 == 0:
        return "ambiguous", False
    if idx % 79 == 0:
        return "fuzzy_recovered", False
    if idx % 73 == 0:
        return "exact_verified", True
    return "exact_verified", False


def record_for(
    idx: int,
    source_idx: int,
    source: dict[str, str],
    source_annotation_counts: Counter[int],
    *,
    span_count: int,
    density_threshold: int,
) -> dict[str, Any]:
    kind = source["kind"]
    span_idx = (idx * 7 + source_idx) % span_count
    status, stale = status_for(idx)
    archived = idx % 67 == 0
    support_checked = idx % 113 == 0 and not archived and status not in BAD_ANCHORS and not stale
    project = idx % 3 == 0
    candidate = idx % 7 == 0
    role = ALLOWED_ROLES[idx % len(ALLOWED_ROLES)]
    selector_type = {
        "web": "TextQuoteSelector",
        "video": "timestamp",
        "repo": "line_range",
        "pdf": "page_rect",
    }[kind]

    exact = (
        f"Span S{source_idx:03d}-{span_idx:03d}: enterprise annotation fixture "
        f"for {kind} source {source_idx:03d}, span {span_idx:03d}."
    )
    if status == "ambiguous":
        exact = f"Duplicate enterprise anchor phrase for source {source_idx:03d} appears twice."
    if status == "broken":
        exact = f"Missing enterprise anchor phrase {idx:06d} not present in current source."

    lifecycle = "source_annotated" if idx % 31 == 0 else "triaged"
    review_pressure = "none"
    if status in {"ambiguous", "source_changed"}:
        lifecycle = "repair_needed"
        review_pressure = "high"
    if status == "broken":
        lifecycle = "repair_needed"
        review_pressure = "blocked"
    if status == "fuzzy_recovered" or stale:
        review_pressure = "medium"
    if support_checked:
        review_pressure = "medium"
        lifecycle = "routed"
    if (project or candidate) and lifecycle == "triaged":
        lifecycle = "routed"
    if archived:
        lifecycle = "archived"
        review_pressure = "none"

    digest_required = source_annotation_counts[source_idx] > density_threshold
    blocked_reason = ""
    next_action = "none"
    if archived:
        blocked_reason = "archived"
        next_action = "none"
    elif status == "broken":
        blocked_reason = "anchor_broken"
        next_action = "repair_anchor_or_archive"
    elif status == "ambiguous":
        blocked_reason = "anchor_ambiguous"
        next_action = "choose_anchor_or_archive"
    elif status == "source_changed":
        blocked_reason = "source_changed"
        next_action = "refresh_anchor_against_current_source"
    elif stale:
        blocked_reason = "anchor_stale"
        next_action = "refresh_anchor"
    elif digest_required:
        next_action = "create_or_refresh_source_digest"
    elif lifecycle == "source_annotated":
        next_action = "triage_annotation"

    current_hash = source["hash"]
    source_hash = source["old_hash"] if status == "source_changed" else current_hash
    snapshot_ref = source["old_snapshot_ref"] if status == "source_changed" else source["snapshot_ref"]

    record: dict[str, Any] = {
        "record_kind": "source_annotation",
        "status": "captured",
        "knowledge_status": "candidate",
        "processing_tier": "light",
        "lifecycle_state": lifecycle,
        "overlay_state": "none",
        "review_pressure": review_pressure,
        "annotation_scope": "source_local_anchor",
        "annotation_id": f"ent-ann-{idx:06d}",
        "source_ref": source["source_ref"],
        "working_copy_ref": source["source_ref"],
        "source_snapshot_ref": snapshot_ref,
        "source_hash": source_hash,
        "external_annotation_id": f"external-{idx:06d}" if idx % 41 == 0 else "",
        "selector_type": selector_type,
        "selector_exact": exact,
        "selector_prefix": f"prefix around source {source_idx:03d}",
        "selector_suffix": f"suffix around source {source_idx:03d}",
        "selector_position_start": idx * 3,
        "selector_position_end": idx * 3 + len(exact),
        "selector_timestamp_start": f"00:{span_idx // 2:02d}:{(span_idx * 7) % 60:02d}"
        if selector_type == "timestamp"
        else None,
        "selector_timestamp_end": f"00:{span_idx // 2:02d}:{((span_idx * 7) + 12) % 60:02d}"
        if selector_type == "timestamp"
        else None,
        "selector_line_start": span_idx + 3 if selector_type == "line_range" else None,
        "selector_line_end": span_idx + 5 if selector_type == "line_range" else None,
        "selector_page": (span_idx % 12) + 1 if selector_type == "page_rect" else None,
        "selector_rect": "120,220,420,260" if selector_type == "page_rect" else None,
        "content_hash": sha256_text(exact),
        "anchor_status": status,
        "anchor_checked_at": "2026-01-15" if stale else "2026-06-14",
        "anchor_check_method": "context_fuzzy" if status == "fuzzy_recovered" else "exact_quote",
        "anchor_match_count": 2 if status == "ambiguous" else 0 if status == "broken" else 1,
        "anchor_stale": stale,
        "annotation_role": role,
        "body_note": f"Enterprise fixture {idx:06d}: {role} for source {source_idx:03d}.",
        "support_checked": support_checked,
        "evidence_support_status": "checked_in_packet" if support_checked else "not_checked",
        "evidence_packet_ref": f"enterprise_stress/evidence/evidence-packet-{idx % 20:03d}.md"
        if support_checked
        else "",
        "candidate_refs": [f"enterprise_stress/candidates/candidate-{idx:06d}.md"] if candidate else [],
        "project_overlay_refs": [f"enterprise_stress/projects/project-{idx % 8:02d}.md"] if project else [],
        "source_digest_required": digest_required,
        "blocked_reason": blocked_reason,
        "next_action": next_action,
        "repair_note": "closed archive"
        if archived
        else "needs anchor repair"
        if status in BAD_ANCHORS
        else "refresh stale anchor"
        if stale
        else "",
        "retrieval_policy": {
            "policy_kind": "archive_only" if archived else "orientation_only",
            "pack_allowed": "blocked" if archived else "review_input_only",
            "action_basis_allowed": False,
            "warning_code": "annotation_not_support",
        },
        "promotion_gate": "enterprise_sandbox_required",
        "action_basis_allowed": False,
        "truth_mutation_allowed": False,
        "tags": ["source-annotation", "review-input", "enterprise-stress"],
    }
    return record


def write_markdown_record(path: Path, record: dict[str, Any], title: str) -> None:
    frontmatter = yaml.dump(record, Dumper=YAML_DUMPER, sort_keys=False, allow_unicode=False)
    body = (
        f"# {title}\n\n"
        "Enterprise stress fixture. This file is sandbox-only diagnostic data.\n"
        "It does not create reviewed knowledge, evidence support, or action basis.\n"
    )
    write_text(path, f"---\n{frontmatter}---\n\n{body}")


def generate_support_files() -> None:
    for idx in range(8):
        write_text(
            STRESS / "projects" / f"project-{idx:02d}.md",
            f"---\nrecord_kind: project_overlay\nstatus: sandbox_fixture\n---\n\n# Project {idx:02d}\n",
        )


def source_slug(source_ref: str) -> str:
    return Path(source_ref).stem


def digest_ref_for_source(source_ref: str) -> str:
    return f"enterprise_stress/digests/{source_slug(source_ref)}-digest.md"
    for idx in range(20):
        write_text(
            STRESS / "evidence" / f"evidence-packet-{idx:03d}.md",
            f"---\nrecord_kind: evidence_packet\nstatus: sandbox_fixture\n---\n\n# Evidence Packet {idx:03d}\n",
        )


def generate_good_corpus(count: int, source_count: int, span_count: int, density_threshold: int) -> list[dict[str, Any]]:
    clean_stress()
    sources = generate_sources(source_count, span_count)
    generate_support_files()
    indices = planned_source_indices(count, source_count)
    source_counts = Counter(indices)
    records = []
    for idx, source_idx in enumerate(indices):
        record = record_for(
            idx,
            source_idx,
            sources[source_idx],
            source_counts,
            span_count=span_count,
            density_threshold=density_threshold,
        )
        records.append(record)
        write_markdown_record(
            STRESS / "annotations" / f"{record['annotation_id']}.md",
            record,
            f"Enterprise Annotation {record['annotation_id']}",
        )
        for candidate_ref in record.get("candidate_refs", []):
            write_text(
                ROOT / candidate_ref,
                "---\nrecord_kind: candidate_distillation\nstatus: sandbox_fixture\n---\n\n# Candidate Fixture\n",
            )
    for source_idx, item_count in sorted(source_counts.items()):
        if item_count > density_threshold:
            source_ref = sources[source_idx]["source_ref"]
            write_text(
                ROOT / digest_ref_for_source(source_ref),
                (
                    "---\n"
                    "record_kind: source_digest\n"
                    "status: sandbox_fixture\n"
                    f"source_ref: {source_ref}\n"
                    "truth_boundary: digest_is_candidate_operational_summary\n"
                    "---\n\n"
                    f"# Digest Fixture For {source_ref}\n\n"
                    "This is a sandbox source digest placeholder for scale-debt routing.\n"
                ),
            )
    return records


def mutation_records(template: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    def clone(name: str) -> dict[str, Any]:
        item = json.loads(json.dumps(template))
        item["annotation_id"] = f"mut-{name}"
        item["lifecycle_state"] = "triaged"
        item["anchor_status"] = "exact_verified"
        item["anchor_stale"] = False
        item["review_pressure"] = "none"
        item["support_checked"] = False
        item["evidence_support_status"] = "not_checked"
        item["evidence_packet_ref"] = ""
        item["retrieval_policy"] = {
            "policy_kind": "orientation_only",
            "pack_allowed": "review_input_only",
            "action_basis_allowed": False,
            "warning_code": "annotation_not_support",
        }
        item["action_basis_allowed"] = False
        item["truth_mutation_allowed"] = False
        return item

    cases: list[tuple[str, dict[str, Any]]] = []

    def add(name: str, mutator) -> None:
        item = clone(name)
        mutator(item)
        cases.append((name, item))

    add("action-basis", lambda r: r.update(action_basis_allowed=True))
    add("truth-mutation", lambda r: r.update(truth_mutation_allowed=True))
    add("support-no-packet", lambda r: r.update(support_checked=True, evidence_support_status="checked_in_packet"))
    add(
        "support-on-bad-anchor",
        lambda r: r.update(
            anchor_status="ambiguous",
            lifecycle_state="repair_needed",
            review_pressure="high",
            support_checked=True,
            evidence_support_status="checked_in_packet",
            evidence_packet_ref="enterprise_stress/evidence/evidence-packet-000.md",
        ),
    )
    add("evidence-status-without-check", lambda r: r.update(evidence_support_status="checked_in_packet"))
    add("project-borrow-scope", lambda r: r.update(project_borrow_scope="adopt"))
    add("project-non-borrow-scope", lambda r: r.update(project_non_borrow_scope="reject"))
    add("missing-warning", lambda r: r["retrieval_policy"].pop("warning_code", None))
    add("missing-next-action", lambda r: r.update(next_action=""))
    add("missing-blocked-reason", lambda r: r.update(anchor_status="broken", lifecycle_state="repair_needed", review_pressure="blocked", blocked_reason="", next_action="repair_anchor_or_archive"))
    add("pack-allowed-support", lambda r: r["retrieval_policy"].update(pack_allowed="support"))
    add("policy-action-true", lambda r: r["retrieval_policy"].update(action_basis_allowed=True))
    add("broken-not-repair", lambda r: r.update(anchor_status="broken", lifecycle_state="triaged", review_pressure="none"))
    add("ambiguous-not-repair", lambda r: r.update(anchor_status="ambiguous", lifecycle_state="triaged", review_pressure="none"))
    add("source-changed-no-drift", lambda r: r.update(anchor_status="source_changed", source_hash=template["source_hash"], lifecycle_state="repair_needed", review_pressure="high"))
    add("stale-no-pressure", lambda r: r.update(anchor_stale=True, anchor_checked_at="2026-01-15", review_pressure="none"))
    add("archived-pack-allowed", lambda r: r.update(lifecycle_state="archived"))
    cases[-1][1]["retrieval_policy"] = {
        "policy_kind": "orientation_only",
        "pack_allowed": "review_input_only",
        "action_basis_allowed": False,
        "warning_code": "annotation_not_support",
    }
    add("missing-source", lambda r: r.update(source_ref="enterprise_stress/sources/missing.md"))
    add("wrong-record-kind", lambda r: r.update(record_kind="candidate_distillation"))
    add("unknown-role", lambda r: r.update(annotation_role="confirmed_support"))
    add("unknown-anchor", lambda r: r.update(anchor_status="confirmed"))
    add("empty-note", lambda r: r.update(body_note=""))
    add("support-refs-field", lambda r: r.update(support_refs=["enterprise_stress/annotations/ent-ann-000001.md"]))
    add("final-support-refs-field", lambda r: r.update(final_support_refs=["enterprise_stress/annotations/ent-ann-000001.md"]))
    add("missing-selector-exact", lambda r: r.update(selector_type="TextQuoteSelector", selector_exact=""))
    add("timestamp-missing-end", lambda r: r.update(selector_type="timestamp", selector_timestamp_start="00:01:00", selector_timestamp_end=None))
    add("line-range-missing-end", lambda r: r.update(selector_type="line_range", selector_line_start=1, selector_line_end=None))
    add("page-rect-missing-rect", lambda r: r.update(selector_type="page_rect", selector_page=1, selector_rect=None))

    duplicate = json.loads(json.dumps(template))
    cases.append(("duplicate-id", duplicate))
    return cases


def generate_mutations(records: list[dict[str, Any]]) -> None:
    template = next(record for record in records if record["anchor_status"] == "exact_verified" and not record["anchor_stale"])
    for name, record in mutation_records(template):
        write_markdown_record(
            STRESS / "mutations" / f"{name}.md",
            record,
            f"Mutation {name}",
        )

    bad_packs = {
        "bad-pack-role-support.json": {
            "selected_items": [
                {
                    "ref": "enterprise_stress/annotations/ent-ann-000001.md",
                    "record_kind": "source_annotation",
                    "pack_role": "support",
                    "warning_code": "annotation_not_support",
                    "action_basis_allowed": False,
                }
            ],
            "coverage_map": [],
            "resolved_source_spans": [],
            "warnings": ["annotation_not_support"],
        },
        "bad-support-ref.json": {
            "selected_items": [],
            "coverage_map": [{"support_refs": ["enterprise_stress/annotations/ent-ann-000001.md"]}],
            "resolved_source_spans": [],
            "warnings": ["annotation_not_support"],
        },
        "bad-action-allowed.json": {
            "selected_items": [
                {
                    "record_kind": "source_annotation",
                    "pack_role": "review_input",
                    "warning_code": "annotation_not_support",
                    "action_basis_allowed": True,
                }
            ],
            "coverage_map": [],
            "resolved_source_spans": [],
            "warnings": ["annotation_not_support"],
        },
        "bad-missing-warning.json": {
            "selected_items": [
                {
                    "record_kind": "source_annotation",
                    "pack_role": "review_input",
                    "action_basis_allowed": False,
                }
            ],
            "coverage_map": [],
            "resolved_source_spans": [],
            "warnings": [],
        },
        "bad-span-counts-as-support.json": {
            "selected_items": [],
            "coverage_map": [],
            "resolved_source_spans": [
                {"may_count_as_support": True, "support_check_required": False}
            ],
            "warnings": ["annotation_not_support"],
        },
    }
    for name, payload in bad_packs.items():
        write_text(STRESS / "bad_context_packs" / name, json.dumps(payload, indent=2, ensure_ascii=True))


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path} missing frontmatter")
    _, raw, _ = text.split("---", 2)
    data = yaml.load(raw, Loader=YAML_LOADER)
    if not isinstance(data, dict):
        raise ValueError(f"{path} frontmatter is not a map")
    return data


class EnterpriseValidator:
    def __init__(self) -> None:
        self.source_cache: dict[str, str] = {}
        self.hash_cache: dict[str, str] = {}

    def source_text(self, record: dict[str, Any]) -> str:
        source_ref = record.get("source_ref")
        if not source_ref:
            return ""
        if source_ref in self.source_cache:
            return self.source_cache[source_ref]
        path = ROOT / str(source_ref)
        if not path.exists():
            return ""
        text = path.read_text(encoding="utf-8")
        self.source_cache[source_ref] = text
        self.hash_cache[source_ref] = sha256_text(text)
        return text

    def source_hash(self, record: dict[str, Any]) -> str:
        source_ref = str(record.get("source_ref", ""))
        if source_ref not in self.hash_cache:
            self.source_text(record)
        return self.hash_cache.get(source_ref, "")

    def is_stale(self, record: dict[str, Any]) -> bool:
        if record.get("anchor_stale") is True:
            return True
        raw = record.get("anchor_checked_at")
        if not raw:
            return True
        try:
            return date.fromisoformat(str(raw)) < STALE_CUTOFF
        except ValueError:
            return True

    def selector_fingerprint(self, record: dict[str, Any]) -> str:
        return "|".join(
            str(record.get(field))
            for field in [
                "source_ref",
                "selector_type",
                "selector_exact",
                "selector_position_start",
                "selector_position_end",
                "selector_timestamp_start",
                "selector_timestamp_end",
                "selector_line_start",
                "selector_line_end",
                "selector_page",
                "selector_rect",
            ]
        )

    def validate_record(self, path: Path, record: dict[str, Any]) -> list[str]:
        errors: list[str] = []

        def err(message: str) -> None:
            errors.append(f"{path.relative_to(ROOT).as_posix()}: {message}")

        for field in sorted(REQUIRED_FIELDS - set(record.keys())):
            err(f"missing required field {field}")
        for field in sorted(FORBIDDEN_FIELDS.intersection(record.keys())):
            err(f"forbidden field present: {field}")
        if record.get("record_kind") != "source_annotation":
            err("record_kind must be source_annotation")
        if record.get("annotation_role") not in ALLOWED_ROLES:
            err(f"unknown annotation_role {record.get('annotation_role')!r}")
        if record.get("lifecycle_state") not in ALLOWED_LIFECYCLE:
            err(f"unknown lifecycle_state {record.get('lifecycle_state')!r}")
        if record.get("body_note") in {None, ""}:
            err("body_note cannot be empty")
        if record.get("action_basis_allowed") is not False:
            err("action_basis_allowed must be false")
        if record.get("truth_mutation_allowed") is not False:
            err("truth_mutation_allowed must be false")

        policy = record.get("retrieval_policy") or {}
        if not isinstance(policy, dict):
            err("retrieval_policy must be a map")
            policy = {}
        if policy.get("action_basis_allowed") is not False:
            err("retrieval_policy.action_basis_allowed must be false")
        if record.get("lifecycle_state") == "archived":
            if policy.get("policy_kind") != "archive_only":
                err("archived annotation must use archive_only policy")
            if policy.get("pack_allowed") == "review_input_only":
                err("archived annotation cannot be pack_allowed review_input_only")
        else:
            if policy.get("pack_allowed") != "review_input_only":
                err("active annotation pack_allowed must be review_input_only")
            if policy.get("warning_code") != "annotation_not_support":
                err("warning_code must be annotation_not_support")

        if record.get("support_checked") is True and not record.get("evidence_packet_ref"):
            err("support_checked true requires evidence_packet_ref")
        if record.get("evidence_support_status") != "not_checked" and record.get("support_checked") is not True:
            err("evidence_support_status requires support_checked true")

        anchor_status = record.get("anchor_status")
        lifecycle = record.get("lifecycle_state")
        if anchor_status not in {"exact_verified", "fuzzy_recovered", "ambiguous", "broken", "source_changed"}:
            err(f"unknown anchor_status {anchor_status!r}")
        if anchor_status in BAD_ANCHORS and lifecycle not in {"repair_needed", "repair_candidate", "archived"}:
            err(f"{anchor_status} must be in repair lifecycle or archived")
        if anchor_status in BAD_ANCHORS and lifecycle != "archived" and record.get("review_pressure") not in {"high", "blocked", "repair"}:
            err(f"{anchor_status} must have high/blocked/repair review pressure")
        if self.is_stale(record) and lifecycle != "archived" and record.get("review_pressure") == "none":
            err("stale active anchor must have review pressure")
        if record.get("support_checked") is True and (
            anchor_status in BAD_ANCHORS or (self.is_stale(record) and lifecycle != "archived")
        ):
            err("support_checked cannot be current on bad or stale anchor")
        if lifecycle != "archived" and record.get("next_action") in {None, ""}:
            err("active annotation requires next_action")
        if (anchor_status in BAD_ANCHORS or (self.is_stale(record) and lifecycle != "archived")) and not record.get("blocked_reason"):
            err("blocked or stale annotation requires blocked_reason")

        selector_type = record.get("selector_type")
        if selector_type == "TextQuoteSelector":
            if not record.get("selector_exact"):
                err("TextQuoteSelector requires selector_exact")
            if not record.get("selector_prefix") or not record.get("selector_suffix"):
                err("TextQuoteSelector requires selector_prefix and selector_suffix")
        elif selector_type == "timestamp":
            if not record.get("selector_timestamp_start") or not record.get("selector_timestamp_end"):
                err("timestamp selector requires start and end")
        elif selector_type == "line_range":
            if record.get("selector_line_start") is None or record.get("selector_line_end") is None:
                err("line_range selector requires start and end")
        elif selector_type == "page_rect":
            if record.get("selector_page") is None or not record.get("selector_rect"):
                err("page_rect selector requires page and rect")
        else:
            err(f"unknown selector_type {selector_type!r}")

        text = self.source_text(record)
        if not text:
            err("source_ref cannot be resolved")
        else:
            exact = str(record.get("selector_exact") or "")
            count = None
            if exact and (selector_type == "TextQuoteSelector" or anchor_status in {"ambiguous", "broken"}):
                count = text.count(exact)
            current_hash = self.source_hash(record)
            source_hash = record.get("source_hash")
            if anchor_status == "exact_verified" and selector_type == "TextQuoteSelector" and count != 1:
                err(f"exact_verified TextQuoteSelector requires one match, got {count}")
            if anchor_status == "ambiguous" and count is not None and count < 2:
                err("ambiguous anchor should have multiple current matches")
            if anchor_status == "broken" and count is not None and count != 0:
                err("broken anchor should not have a current exact match")
            if anchor_status == "source_changed" and source_hash == current_hash:
                err("source_changed requires source_hash drift")
            if anchor_status in {"exact_verified", "fuzzy_recovered", "ambiguous", "broken"} and source_hash != current_hash:
                err(f"{anchor_status} should use current source_hash")

        return errors

    def build_views(self, records: list[tuple[Path, dict[str, Any]]]) -> dict[str, list[str]]:
        active = [record for _, record in records if record.get("lifecycle_state") != "archived"]
        source_counts = Counter(str(record.get("source_ref")) for record in active)
        selector_counts = Counter(self.selector_fingerprint(record) for record in active)
        views: dict[str, list[str]] = defaultdict(list)
        for _, record in records:
            ann_id = str(record.get("annotation_id"))
            lifecycle = record.get("lifecycle_state")
            anchor = record.get("anchor_status")
            stale = self.is_stale(record)
            ready_locator = lifecycle != "archived" and anchor not in BAD_ANCHORS and not stale
            if ready_locator and lifecycle == "source_annotated":
                views["annotation_inbox"].append(ann_id)
            if ready_locator and lifecycle != "source_annotated":
                views["locator_pool"].append(ann_id)
            if lifecycle != "archived":
                views["source_drilldown"].append(ann_id)
            if record.get("project_overlay_refs") and lifecycle != "archived":
                views["project_lens"].append(ann_id)
            if lifecycle != "archived" and record.get("support_checked") is False and record.get("review_pressure") != "none":
                views["routing_queue"].append(ann_id)
            if anchor in BAD_ANCHORS and lifecycle != "archived":
                views["needs_anchor_repair"].append(ann_id)
            if record.get("support_checked") is True:
                views["support_checked_audit"].append(ann_id)
            if lifecycle != "archived" and stale:
                views["stale_anchor_queue"].append(ann_id)
            if lifecycle == "archived":
                views["cold_archive"].append(ann_id)
            if lifecycle != "archived" and (
                record.get("source_digest_required") is True
                or source_counts[str(record.get("source_ref"))] > 50
                or selector_counts[self.selector_fingerprint(record)] > 6
            ):
                views["scale_debt"].append(ann_id)
            policy = record.get("retrieval_policy") or {}
            if (
                lifecycle != "archived"
                and not stale
                and anchor in {"exact_verified", "fuzzy_recovered"}
                and record.get("action_basis_allowed") is False
                and policy.get("warning_code") == "annotation_not_support"
            ):
                views["ai_export_ready"].append(ann_id)
            if anchor in BAD_ANCHORS or stale or lifecycle == "archived" or record.get("action_basis_allowed") is True or record.get("truth_mutation_allowed") is True:
                views["ai_export_blocked"].append(ann_id)
        return {name: sorted(ids) for name, ids in sorted(views.items())}

    def validate_context_pack(self, pack: dict[str, Any], *, require_warning: bool) -> list[str]:
        errors: list[str] = []
        policy = pack.get("selection_policy") or {}
        max_per_source = policy.get("max_per_source")
        per_source: Counter[str] = Counter()
        for item in pack.get("selected_items", []):
            if item.get("source_ref"):
                per_source[str(item.get("source_ref"))] += 1
            if item.get("record_kind") == "source_annotation" and item.get("pack_role") == "support":
                errors.append("source_annotation cannot be packed as support")
            if item.get("record_kind") == "source_annotation" and item.get("action_basis_allowed") is not False:
                errors.append("source_annotation action_basis_allowed must be false")
            if item.get("record_kind") == "source_annotation" and item.get("warning_code") != "annotation_not_support":
                errors.append("source_annotation missing annotation_not_support warning")
        if max_per_source is not None:
            for source_ref, count in per_source.items():
                if count > int(max_per_source):
                    errors.append(f"context pack exceeds max_per_source for {source_ref}: {count}")
        for entry in pack.get("coverage_map", []):
            for ref in entry.get("support_refs", []) or []:
                if "enterprise_stress/annotations/" in str(ref) or "source_annotations/" in str(ref):
                    errors.append("coverage_map support_refs cannot point to source_annotation")
        for span in pack.get("resolved_source_spans", []):
            if span.get("may_count_as_support") is not False:
                errors.append("resolved span may_count_as_support must be false")
            if span.get("support_check_required") is not True:
                errors.append("resolved span support_check_required must be true")
        if require_warning and "annotation_not_support" not in pack.get("warnings", []):
            errors.append("context pack missing annotation_not_support warning")
        return errors

    def excerpt(self, record: dict[str, Any], max_chars: int = 480) -> str:
        text = self.source_text(record)
        exact = str(record.get("selector_exact") or "")
        pos = text.find(exact)
        if pos < 0:
            return ""
        start = max(0, pos - max_chars // 3)
        end = min(len(text), pos + len(exact) + max_chars // 3)
        return " ".join(text[start:end].split())[:max_chars]


def build_context_pack(
    records: list[tuple[Path, dict[str, Any]]],
    views: dict[str, list[str]],
    validator: EnterpriseValidator,
    max_items: int,
    max_per_source: int,
) -> dict[str, Any]:
    by_id = {str(record.get("annotation_id")): (path, record) for path, record in records}
    candidate_ids = views.get("ai_export_ready", [])
    exact_ids = [
        ann_id
        for ann_id in candidate_ids
        if by_id[ann_id][1].get("anchor_status") == "exact_verified"
    ]
    fuzzy_ids = [
        ann_id
        for ann_id in candidate_ids
        if by_id[ann_id][1].get("anchor_status") == "fuzzy_recovered"
    ]
    selected: list[str] = []
    per_source: Counter[str] = Counter()
    for ann_id in exact_ids + fuzzy_ids:
        _, record = by_id[ann_id]
        source_ref = str(record.get("source_ref"))
        if per_source[source_ref] >= max_per_source:
            continue
        selected.append(ann_id)
        per_source[source_ref] += 1
        if len(selected) >= max_items:
            break
    items = []
    spans = []
    for ann_id in selected:
        path, record = by_id[ann_id]
        policy = record.get("retrieval_policy") or {}
        items.append(
            {
                "ref": path.relative_to(ROOT).as_posix(),
                "record_kind": "source_annotation",
                "pack_role": "review_input",
                "source_ref": record.get("source_ref"),
                "annotation_role": record.get("annotation_role"),
                "anchor_status": record.get("anchor_status"),
                "anchor_stale": validator.is_stale(record),
                "anchor_caution": "fuzzy_recovered_needs_human_confirmation"
                if record.get("anchor_status") == "fuzzy_recovered"
                else "",
                "support_checked": record.get("support_checked"),
                "evidence_packet_ref": record.get("evidence_packet_ref") or None,
                "warning_code": policy.get("warning_code"),
                "action_basis_allowed": False,
                "next_action": record.get("next_action"),
            }
        )
        spans.append(
            {
                "anchor_ref": f"{record.get('source_ref')}#{ann_id}",
                "source_ref": record.get("source_ref"),
                "excerpt": validator.excerpt(record),
                "may_count_as_support": False,
                "support_check_required": True,
            }
        )
    return {
        "context_pack_id": "ctx-enterprise-stress-001",
        "query": {"mode": "orientation", "active_project": "VAKS"},
        "authority_gate": {
            "included_buckets": ["source_annotation", "raw_source"],
            "action_basis_requested": False,
            "action_basis_allowed": False,
        },
        "selected_items": items,
        "selection_policy": {
            "query_aware_required_for_real_export": True,
            "max_items": max_items,
            "max_per_source": max_per_source,
            "prefer_exact_verified": True,
            "fuzzy_recovered_is_caution_only": True,
        },
        "resolved_source_spans": spans,
        "coverage_overview": {
            "supported": 0,
            "missing_evidence": len(items),
            "risk_flags": ["annotation_not_support"],
        },
        "coverage_map": [],
        "action_readiness": {
            "state": "not_ready",
            "reason": "source annotations are locators, not evidence support",
        },
        "warnings": ["annotation_not_support"],
    }


def source_health(records: list[tuple[Path, dict[str, Any]]], views: dict[str, list[str]]) -> list[dict[str, Any]]:
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for _, record in records:
        by_source[str(record.get("source_ref"))].append(record)
    sets = {name: set(ids) for name, ids in views.items()}
    rows = []
    for source_ref, items in sorted(by_source.items()):
        ids = [str(item.get("annotation_id")) for item in items]
        digest_required = any(item.get("source_digest_required") is True for item in items)
        digest_backlog_age_days = max((int(item.get("annotation_id", "0")[-2:]) % 15 for item in items), default=0) if digest_required else 0
        rows.append(
            {
                "source_ref": source_ref,
                "total": len(items),
                "active": sum(1 for item in items if item.get("lifecycle_state") != "archived"),
                "ai_ready": sum(1 for ann_id in ids if ann_id in sets.get("ai_export_ready", set())),
                "repair": sum(1 for ann_id in ids if ann_id in sets.get("needs_anchor_repair", set())),
                "stale": sum(1 for ann_id in ids if ann_id in sets.get("stale_anchor_queue", set())),
                "scale_debt": sum(1 for ann_id in ids if ann_id in sets.get("scale_debt", set())),
                "digest_required": digest_required,
                "digest_ref": digest_ref_for_source(source_ref) if digest_required else "",
                "last_digest_at": "2026-06-07" if digest_required else "",
                "next_digest_due": "2026-06-21" if digest_required else "",
                "debt_queue": "source_digest_backlog" if digest_required else "",
                "debt_owner_or_queue": "source_digest_backlog" if digest_required else "",
                "next_action": "create_or_refresh_source_digest" if digest_required else "none",
                "digest_backlog_age_days": digest_backlog_age_days,
            }
        )
    return rows


def validate_corpus(
    *,
    count: int,
    max_context_items: int,
    runtime_gate_seconds: float,
    context_size_gate_kb: int,
    max_inbox_items: int,
    max_context_per_source: int,
) -> dict[str, Any]:
    validator = EnterpriseValidator()
    start = time.perf_counter()
    records = [(path, frontmatter(path)) for path in sorted((STRESS / "annotations").glob("*.md"))]
    errors: list[str] = []
    for path, record in records:
        errors.extend(validator.validate_record(path, record))

    ids = Counter(str(record.get("annotation_id")) for _, record in records)
    duplicate_errors = [f"duplicate annotation_id {ann_id}: {num}" for ann_id, num in ids.items() if num > 1]
    errors.extend(duplicate_errors)

    views = validator.build_views(records)
    view_sets = {name: set(ids) for name, ids in views.items()}
    active_bad = {
        str(record.get("annotation_id"))
        for _, record in records
        if record.get("anchor_status") in BAD_ANCHORS and record.get("lifecycle_state") != "archived"
    }
    active_stale = {
        str(record.get("annotation_id"))
        for _, record in records
        if validator.is_stale(record) and record.get("lifecycle_state") != "archived"
    }
    archived = {
        str(record.get("annotation_id"))
        for _, record in records
        if record.get("lifecycle_state") == "archived"
    }
    ai_ready = view_sets.get("ai_export_ready", set())
    inbox = view_sets.get("annotation_inbox", set())

    contamination = {
        "bad_anchor_in_ai_ready": sorted(active_bad & ai_ready)[:20],
        "stale_in_ai_ready": sorted(active_stale & ai_ready)[:20],
        "archived_in_ai_ready": sorted(archived & ai_ready)[:20],
        "bad_anchor_in_inbox": sorted(active_bad & inbox)[:20],
        "stale_in_inbox": sorted(active_stale & inbox)[:20],
    }
    for name, items in contamination.items():
        if items:
            errors.append(f"{name}: {len(items)} sampled contamination")

    repair_missing = sorted(active_bad - view_sets.get("needs_anchor_repair", set()))
    stale_missing = sorted(active_stale - view_sets.get("stale_anchor_queue", set()))
    if repair_missing:
        errors.append(f"repair queue missing {len(repair_missing)} active bad anchors")
    if stale_missing:
        errors.append(f"stale queue missing {len(stale_missing)} active stale anchors")

    density_missing = []
    for row in source_health(records, views):
        if row["active"] > 50 and not row["digest_required"]:
            density_missing.append(row["source_ref"])
    if density_missing:
        errors.append(f"dense sources missing digest route: {len(density_missing)}")
    if len(views.get("annotation_inbox", [])) > max_inbox_items:
        errors.append(
            f"working inbox too large: {len(views.get('annotation_inbox', []))} > {max_inbox_items}"
        )

    mutation_results = []
    mutation_caught = 0
    good_ids = set(ids.keys())
    for path in sorted((STRESS / "mutations").glob("*.md")):
        record = frontmatter(path)
        mutation_errors = validator.validate_record(path, record)
        if str(record.get("annotation_id")) in good_ids:
            mutation_errors.append("duplicate annotation_id collides with good corpus")
        if mutation_errors:
            mutation_caught += 1
        mutation_results.append(
            {
                "file": path.relative_to(ROOT).as_posix(),
                "caught": bool(mutation_errors),
                "error_count": len(mutation_errors),
                "errors": mutation_errors[:5],
            }
        )

    bad_pack_results = []
    bad_pack_caught = 0
    for path in sorted((STRESS / "bad_context_packs").glob("*.json")):
        pack = json.loads(path.read_text(encoding="utf-8"))
        pack_errors = validator.validate_context_pack(pack, require_warning=False)
        if pack_errors:
            bad_pack_caught += 1
        bad_pack_results.append(
            {
                "file": path.relative_to(ROOT).as_posix(),
                "caught": bool(pack_errors),
                "error_count": len(pack_errors),
                "errors": pack_errors,
            }
        )

    pack = build_context_pack(records, views, validator, max_context_items, max_context_per_source)
    pack_errors = validator.validate_context_pack(pack, require_warning=True)
    errors.extend(f"context_pack: {error}" for error in pack_errors)
    pack_json = json.dumps(pack, indent=2, ensure_ascii=True)
    pack_size = len(pack_json.encode("utf-8"))
    run_suffix = str(len(records))
    write_text(RESULTS / "enterprise-context-pack.json", pack_json)
    write_text(RESULTS / f"enterprise-context-pack-{run_suffix}.json", pack_json)
    if len(pack.get("selected_items", [])) > max_context_items:
        errors.append("context pack selected too many items")
    if pack_size > context_size_gate_kb * 1024:
        errors.append(f"context pack too large: {pack_size} bytes")
    pack_sources = Counter(str(item.get("source_ref")) for item in pack.get("selected_items", []))
    max_pack_source_count = max(pack_sources.values(), default=0)
    if max_pack_source_count > max_context_per_source:
        errors.append(f"context pack source diversity cap exceeded: {max_pack_source_count}")
    if len(pack_sources) < min(10, len(pack.get("selected_items", []))):
        errors.append(f"context pack has weak source diversity: {len(pack_sources)} sources")

    elapsed = time.perf_counter() - start
    if elapsed > runtime_gate_seconds:
        errors.append(f"runtime gate exceeded: {elapsed:.3f}s > {runtime_gate_seconds:.3f}s")

    view_counts = {name: len(ids) for name, ids in views.items()}
    health = source_health(records, views)
    digest_rows = [row for row in health if row["digest_required"]]
    digest_age_values = sorted(int(row["digest_backlog_age_days"]) for row in digest_rows)
    digest_p95_age = digest_age_values[min(len(digest_age_values) - 1, round((len(digest_age_values) - 1) * 0.95))] if digest_age_values else 0
    missing_digest_routes = [
        row["source_ref"]
        for row in digest_rows
        if not row["digest_ref"]
        or not row["next_digest_due"]
        or row["debt_queue"] != "source_digest_backlog"
        or row["next_action"] != "create_or_refresh_source_digest"
    ]
    if missing_digest_routes:
        errors.append(f"dense sources missing digest SLA route: {len(missing_digest_routes)}")
    if digest_p95_age > 14:
        errors.append(f"digest backlog p95 age too high: {digest_p95_age}")
    health_json = json.dumps(health, indent=2, ensure_ascii=True)
    write_text(RESULTS / "enterprise-source-health.json", health_json)
    write_text(RESULTS / f"enterprise-source-health-{run_suffix}.json", health_json)
    report = {
        "passed": not errors
        and len(records) >= count
        and mutation_caught == len(mutation_results)
        and bad_pack_caught == len(bad_pack_results),
        "requested_count": count,
        "good_annotation_count": len(records),
        "elapsed_seconds": round(elapsed, 4),
        "records_per_second": round(len(records) / elapsed, 2) if elapsed else None,
        "runtime_gate_seconds": runtime_gate_seconds,
        "context_pack_bytes": pack_size,
        "context_pack_selected_items": len(pack.get("selected_items", [])),
        "context_pack_source_count": len(pack_sources),
        "context_pack_max_per_source_observed": max_pack_source_count,
        "context_pack_max_per_source_gate": max_context_per_source,
        "context_size_gate_kb": context_size_gate_kb,
        "max_inbox_items": max_inbox_items,
        "errors": errors[:200],
        "error_count": len(errors),
        "view_counts": view_counts,
        "queue_accuracy": {
            "active_bad_anchors": len(active_bad),
            "repair_missing": len(repair_missing),
            "active_stale_anchors": len(active_stale),
            "stale_missing": len(stale_missing),
            "ai_ready_contamination": sum(len(items) for items in contamination.values()),
        },
        "operator_load": {
            "working_inbox": len(views.get("annotation_inbox", [])),
            "locator_pool": len(views.get("locator_pool", [])),
            "scale_debt": len(views.get("scale_debt", [])),
            "source_health_rows": len(health),
            "source_digest_backlog": len(digest_rows),
            "digest_backlog_p95_age_days": digest_p95_age,
        },
        "mutation_count": len(mutation_results),
        "mutation_caught": mutation_caught,
        "mutation_catch_rate": round(mutation_caught / len(mutation_results), 4) if mutation_results else 0,
        "mutation_results": mutation_results,
        "bad_context_pack_count": len(bad_pack_results),
        "bad_context_pack_caught": bad_pack_caught,
        "bad_context_pack_catch_rate": round(bad_pack_caught / len(bad_pack_results), 4) if bad_pack_results else 0,
        "bad_context_pack_results": bad_pack_results,
        "source_health_top_dense": sorted(health, key=lambda row: row["active"], reverse=True)[:20],
    }
    report_json = json.dumps(report, indent=2, ensure_ascii=True)
    write_text(RESULTS / "enterprise-stress-report.json", report_json)
    write_text(RESULTS / f"enterprise-stress-report-{run_suffix}.json", report_json)
    write_enterprise_md(report)
    write_enterprise_md(report, run_suffix)
    return report


def write_enterprise_md(report: dict[str, Any], suffix: str | None = None) -> None:
    lines = [
        "---",
        "record_kind: sandbox_enterprise_stress_report",
        f"status: {'complete' if report['passed'] else 'failed'}",
        "created_at: 2026-06-14",
        "---",
        "",
        "# Enterprise Stress Report",
        "",
        f"- Passed: {report['passed']}",
        f"- Good annotations: {report['good_annotation_count']}",
        f"- Runtime: {report['elapsed_seconds']}s",
        f"- Records/sec: {report['records_per_second']}",
        f"- Error count: {report['error_count']}",
        f"- Mutation caught: {report['mutation_caught']} / {report['mutation_count']}",
        f"- Bad context packs caught: {report['bad_context_pack_caught']} / {report['bad_context_pack_count']}",
        f"- Context pack: {report['context_pack_selected_items']} items, {report['context_pack_bytes']} bytes",
        f"- Context pack sources: {report['context_pack_source_count']}",
        f"- Max items per source observed: {report['context_pack_max_per_source_observed']}",
        "",
        "## View Counts",
        "",
    ]
    for name, count in sorted(report["view_counts"].items()):
        lines.append(f"- {name}: {count}")
    lines.extend(["", "## Queue Accuracy", ""])
    for key, value in report["queue_accuracy"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Operator Load", ""])
    for key, value in report["operator_load"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Top Dense Sources", ""])
    for row in report["source_health_top_dense"][:10]:
        lines.append(
            f"- {row['source_ref']}: active={row['active']}, repair={row['repair']}, stale={row['stale']}, scale_debt={row['scale_debt']}, digest={row['digest_required']}"
        )
    lines.extend(["", "## Errors", ""])
    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- none")
    filename = "enterprise-stress-report.md" if not suffix else f"enterprise-stress-report-{suffix}.md"
    write_text(RESULTS / filename, "\n".join(lines) + "\n")


def run(args: argparse.Namespace) -> int:
    records = generate_good_corpus(args.count, args.sources, args.spans, args.density_threshold)
    generate_mutations(records)
    report = validate_corpus(
        count=args.count,
        max_context_items=args.max_context_items,
        runtime_gate_seconds=args.runtime_gate_seconds,
        context_size_gate_kb=args.context_size_gate_kb,
        max_inbox_items=args.max_inbox_items,
        max_context_per_source=args.max_context_per_source,
    )
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0 if report["passed"] else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5000)
    parser.add_argument("--sources", type=int, default=120)
    parser.add_argument("--spans", type=int, default=120)
    parser.add_argument("--density-threshold", type=int, default=50)
    parser.add_argument("--max-context-items", type=int, default=60)
    parser.add_argument("--runtime-gate-seconds", type=float, default=30.0)
    parser.add_argument("--context-size-gate-kb", type=int, default=250)
    parser.add_argument("--max-inbox-items", type=int, default=250)
    parser.add_argument("--max-context-per-source", type=int, default=5)
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
