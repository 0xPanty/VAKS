from __future__ import annotations

import hashlib
import shutil
import textwrap
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def clean_generated() -> None:
    for child in [
        SAMPLES / "sources",
        SAMPLES / "snapshots",
        SAMPLES / "annotations",
        SAMPLES / "mutations",
        SAMPLES / "projects",
        SAMPLES / "candidates",
        SAMPLES / "evidence",
    ]:
        if child.exists():
            shutil.rmtree(child)


def make_sources() -> dict[str, dict[str, str]]:
    sources = {
        "web-annotation-model": textwrap.dedent(
            """
            # Web Annotation Selector Notes

            A source annotation points to a source segment. The body explains why
            the segment matters, but the body is not evidence support.

            Text quote anchors work best when exact text is stored with a short
            prefix and suffix. Position anchors are useful, but position moves
            when the source changes.

            Selector is locator not evidence. Selector is locator not evidence.

            A repair queue is needed when a source changes, when a quote appears
            more than once, or when the original span cannot be found.

            A dense source should be summarized into a source digest before the
            annotation list becomes a new pile of unreviewed notes.
            """
        ).strip()
        + "\n",
        "obsidian-workbench": textwrap.dedent(
            """
            # Obsidian Workbench Notes

            Bases can show Markdown records as filtered tables. They are useful
            for inbox, project lens, source drilldown, and repair queues.

            A Base view is a surface for work. It is not a truth layer.

            Inline footnotes are comfortable because the reading mode can hide
            detail behind a small marker. The canonical record should still live
            in a sidecar file.

            Long selector text should stay out of the default table.
            """
        ).strip()
        + "\n",
        "rag-attribution-notes": textwrap.dedent(
            """
            # RAG Attribution Notes

            A citation can point to a source and still fail to support the final
            answer. Citation correctness is not the same as faithfulness.

            Context packs should separate review inputs from evidence support.
            A source annotation may help inspect a span, but an Evidence Packet
            must perform the support check.
            """
        ).strip()
        + "\n",
        "transcript-segment": textwrap.dedent(
            """
            # Transcript Segment

            [00:01:10] The speaker says the first useful moment is the simple
            ability to mark the exact sentence while staying in the reading flow.

            [00:03:20] The second moment is project filtering. A mark can be
            useful for VAKS without becoming a project decision.

            [00:05:45] The third moment is repair. A transcript can be re-cut or
            re-transcribed, so timestamps need nearby text as a cross-check.
            """
        ).strip()
        + "\n",
    }

    result = {}
    for slug, content in sources.items():
        source_path = SAMPLES / "sources" / f"{slug}.md"
        snapshot_path = SAMPLES / "snapshots" / f"{slug}-snapshot-v1.md"
        write_text(source_path, content)
        write_text(snapshot_path, content)
        result[slug] = {
            "source_ref": rel(source_path),
            "snapshot_ref": rel(snapshot_path),
            "hash": sha256_text(content),
            "content": content,
        }

    old_snapshot = sources["web-annotation-model"].replace(
        "A repair queue is needed",
        "A repair queue will be needed",
    )
    old_path = SAMPLES / "snapshots" / "web-annotation-model-old-snapshot.md"
    write_text(old_path, old_snapshot)
    result["web-annotation-model-old"] = {
        "source_ref": rel(SAMPLES / "sources" / "web-annotation-model.md"),
        "snapshot_ref": rel(old_path),
        "hash": sha256_text(old_snapshot),
        "content": old_snapshot,
    }
    return result


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_position(source_text: str, exact: str) -> tuple[int | None, int | None]:
    pos = source_text.find(exact)
    if pos == -1:
        return None, None
    return pos, pos + len(exact)


def base_record(
    *,
    ann_id: str,
    source: dict[str, str],
    selector_type: str,
    exact: str,
    role: str,
    note: str,
    anchor_status: str = "exact_verified",
    lifecycle_state: str = "triaged",
    review_pressure: str = "none",
    project: bool = False,
    candidate: bool = False,
    support_checked: bool = False,
    evidence_packet: bool = False,
    evidence_status: str = "not_checked",
    source_changed: bool = False,
    archived: bool = False,
    digest_required: bool = False,
    timestamp_start: str | None = None,
    timestamp_end: str | None = None,
    line_start: int | None = None,
    line_end: int | None = None,
    page: int | None = None,
    rect: str | None = None,
    anchor_checked_at: str = "2026-06-14",
    anchor_stale: bool = False,
) -> dict:
    start, end = source_position(source["content"], exact)
    if source_changed:
        source_hash = source["hash"]
    else:
        current = (ROOT / source["source_ref"]).read_text(encoding="utf-8")
        source_hash = sha256_text(current)

    record = {
        "record_kind": "source_annotation",
        "status": "captured",
        "knowledge_status": "candidate",
        "processing_tier": "light",
        "lifecycle_state": "archived" if archived else lifecycle_state,
        "overlay_state": "none",
        "review_pressure": review_pressure,
        "annotation_scope": "source_local_anchor",
        "annotation_id": ann_id,
        "source_ref": source["source_ref"],
        "working_copy_ref": source["source_ref"],
        "source_snapshot_ref": source["snapshot_ref"],
        "source_hash": source_hash,
        "external_annotation_id": "",
        "selector_type": selector_type,
        "selector_exact": exact,
        "selector_prefix": "short prefix around the source span",
        "selector_suffix": "short suffix around the source span",
        "selector_position_start": start,
        "selector_position_end": end,
        "selector_timestamp_start": timestamp_start,
        "selector_timestamp_end": timestamp_end,
        "selector_line_start": line_start,
        "selector_line_end": line_end,
        "selector_page": page,
        "selector_rect": rect,
        "content_hash": sha256_text(exact),
        "anchor_status": anchor_status,
        "anchor_checked_at": anchor_checked_at,
        "anchor_check_method": "context_fuzzy"
        if anchor_status == "fuzzy_recovered"
        else "exact_quote",
        "anchor_match_count": 2 if anchor_status == "ambiguous" else 0 if anchor_status == "broken" else 1,
        "anchor_stale": anchor_stale,
        "annotation_role": role,
        "body_note": note,
        "support_checked": support_checked,
        "evidence_support_status": evidence_status,
        "evidence_packet_ref": "samples/evidence/evidence-packet-001.md" if evidence_packet else "",
        "candidate_refs": [f"samples/candidates/{ann_id}-candidate.md"] if candidate else [],
        "project_overlay_refs": ["samples/projects/vaks-source-annotation-overlay.md"] if project else [],
        "source_digest_required": digest_required,
        "repair_note": "closed or intentionally ignored"
        if archived
        else "needs human repair"
        if anchor_status in {"ambiguous", "broken", "source_changed"}
        else "",
        "retrieval_policy": {
            "policy_kind": "archive_only" if archived else "orientation_only",
            "pack_allowed": "blocked" if archived else "review_input_only",
            "action_basis_allowed": False,
            "warning_code": "annotation_not_support",
        },
        "promotion_gate": "sandbox_required",
        "action_basis_allowed": False,
        "truth_mutation_allowed": False,
        "tags": ["source-annotation", "review-input"],
    }
    return record


def write_annotation(record: dict, root: Path) -> None:
    path = root / f"{record['annotation_id']}.md"
    frontmatter = yaml.safe_dump(record, sort_keys=False, allow_unicode=False)
    body = textwrap.dedent(
        f"""
        # Source Annotation {record['annotation_id']}

        This sandbox fixture says: inspect this source span.

        It does not grant evidence support, project adoption, truth confidence,
        or action readiness.
        """
    ).strip()
    write_text(path, f"---\n{frontmatter}---\n\n{body}\n")


def build_good_annotations(sources: dict[str, dict[str, str]]) -> list[dict]:
    web = sources["web-annotation-model"]
    old = sources["web-annotation-model-old"]
    obsidian = sources["obsidian-workbench"]
    rag = sources["rag-attribution-notes"]
    transcript = sources["transcript-segment"]

    records: list[dict] = []
    web_exact = "Selector is locator not evidence."
    roles = [
        "candidate_seed",
        "possible_support",
        "question",
        "implementation_note",
        "term_definition",
        "risk_signal",
        "scope_limit",
        "bookmark",
        "counterexample",
        "candidate_seed",
        "possible_support",
        "question",
        "implementation_note",
        "term_definition",
        "risk_signal",
        "scope_limit",
        "bookmark",
        "possible_support",
    ]
    for idx, role in enumerate(roles, start=1):
        status = "exact_verified"
        lifecycle = "triaged"
        pressure = "none"
        exact = "A source annotation points to a source segment."
        if idx == 2:
            exact = "Text quote anchors work best when exact text is stored with a short"
        if idx == 11:
            exact = "A dense source should be summarized into a source digest"
        if idx == 4:
            status = "ambiguous"
            pressure = "high"
            lifecycle = "repair_needed"
            exact = web_exact
        if idx == 5:
            status = "broken"
            pressure = "blocked"
            lifecycle = "repair_needed"
            exact = "This text is no longer present in the current source."
        if idx == 6:
            status = "source_changed"
            pressure = "high"
            lifecycle = "repair_needed"
            exact = "A repair queue will be needed"
        if idx == 7:
            status = "fuzzy_recovered"
            pressure = "medium"
            exact = "Text quote anchors work best when exact text is stored"
        stale = idx == 16
        if stale:
            pressure = "medium"
        if idx == 17:
            lifecycle = "archived"
        record_source = old if status == "source_changed" else web
        records.append(
            base_record(
                ann_id=f"ann-web-{idx:03d}",
                source=record_source,
                selector_type="TextQuoteSelector",
                exact=exact,
                role=role,
                note=f"Sandbox web annotation fixture {idx}.",
                anchor_status=status,
                lifecycle_state=lifecycle,
                review_pressure=pressure,
                project=idx in {1, 2, 3, 8, 9, 10},
                candidate=idx in {1, 3, 10, 14},
                digest_required=True,
                source_changed=status == "source_changed",
                archived=lifecycle == "archived",
                anchor_checked_at="2026-01-15" if stale else "2026-06-14",
                anchor_stale=stale,
            )
        )

    obsidian_exact = "A Base view is a surface for work."
    for idx in range(1, 9):
        records.append(
            base_record(
                ann_id=f"ann-obsidian-{idx:03d}",
                source=obsidian,
                selector_type="TextQuoteSelector",
                exact=obsidian_exact if idx != 5 else "Long selector text should stay out of the default table.",
                role=["candidate_seed", "possible_support", "bookmark", "implementation_note"][idx % 4],
                note=f"Workbench fixture {idx}.",
                anchor_status="fuzzy_recovered" if idx == 4 else "exact_verified",
                lifecycle_state="routed" if idx in {2, 4} else "triaged",
                review_pressure="medium" if idx in {2, 4} else "none",
                project=idx in {2, 4, 6},
                candidate=idx in {1, 2},
            )
        )

    rag_exact = "Citation correctness is not the same as faithfulness."
    for idx in range(1, 6):
        records.append(
            base_record(
                ann_id=f"ann-rag-{idx:03d}",
                source=rag,
                selector_type="TextQuoteSelector",
                exact=rag_exact,
                role=["scope_limit", "risk_signal", "possible_support", "counterexample", "question"][idx - 1],
                note=f"Attribution boundary fixture {idx}.",
                anchor_status="exact_verified",
                lifecycle_state="routed",
                review_pressure="high" if idx in {1, 2} else "medium",
                project=idx in {1, 2, 3},
                support_checked=idx == 3,
                evidence_packet=idx == 3,
                evidence_status="checked_in_packet" if idx == 3 else "not_checked",
            )
        )

    records.extend(
        [
            base_record(
                ann_id="ann-video-001",
                source=transcript,
                selector_type="timestamp",
                exact="ability to mark the exact sentence",
                role="candidate_seed",
                note="Capture should preserve reading flow.",
                timestamp_start="00:01:10",
                timestamp_end="00:01:28",
                project=True,
                candidate=True,
            ),
            base_record(
                ann_id="ann-video-002",
                source=transcript,
                selector_type="timestamp",
                exact="A mark can be useful for VAKS without becoming a project decision.",
                role="scope_limit",
                note="Project relevance is not project verdict.",
                timestamp_start="00:03:20",
                timestamp_end="00:03:42",
                project=True,
            ),
            base_record(
                ann_id="ann-video-003",
                source=transcript,
                selector_type="timestamp",
                exact="timestamps need nearby text as a cross-check",
                role="risk_signal",
                note="Transcript re-cut risk.",
                timestamp_start="00:05:45",
                timestamp_end="00:06:00",
                anchor_status="fuzzy_recovered",
                review_pressure="medium",
            ),
            base_record(
                ann_id="ann-video-004",
                source=transcript,
                selector_type="line_range",
                exact="The second moment is project filtering.",
                role="bookmark",
                note="Line-range navigation fixture.",
                line_start=5,
                line_end=7,
            ),
        ]
    )
    return records


def build_mutations(good: list[dict]) -> list[dict]:
    def clone(base: dict, ann_id: str) -> dict:
        record = dict(base)
        record["annotation_id"] = ann_id
        return record

    mutations = []

    bad = clone(good[0], "mut-action-basis")
    bad["action_basis_allowed"] = True
    mutations.append(bad)

    bad = clone(good[1], "mut-truth-mutation")
    bad["truth_mutation_allowed"] = True
    mutations.append(bad)

    bad = clone(good[2], "mut-support-no-packet")
    bad["support_checked"] = True
    bad["evidence_support_status"] = "checked_in_packet"
    bad["evidence_packet_ref"] = ""
    mutations.append(bad)

    bad = clone(good[3], "mut-project-borrow-scope")
    bad["project_borrow_scope"] = "adopt this for VAKS"
    mutations.append(bad)

    bad = clone(good[4], "mut-missing-warning")
    bad["retrieval_policy"] = {
        "policy_kind": "orientation_only",
        "pack_allowed": "review_input_only",
        "action_basis_allowed": False,
    }
    mutations.append(bad)

    bad = clone(good[5], "mut-broken-ready")
    bad["anchor_status"] = "broken"
    bad["lifecycle_state"] = "triaged"
    bad["review_pressure"] = "none"
    mutations.append(bad)

    bad = clone(good[6], "mut-duplicate-id")
    bad["annotation_id"] = good[6]["annotation_id"]
    mutations.append(bad)

    return mutations


def write_support_files() -> None:
    write_text(
        SAMPLES / "projects" / "vaks-source-annotation-overlay.md",
        textwrap.dedent(
            """
            ---
            record_kind: project_overlay
            status: sandbox_fixture
            ---

            # VAKS Source Annotation Overlay

            This sandbox overlay is only used to test project lens filtering.
            """
        ).strip()
        + "\n",
    )
    write_text(
        SAMPLES / "evidence" / "evidence-packet-001.md",
        textwrap.dedent(
            """
            ---
            record_kind: evidence_packet
            status: sandbox_fixture
            ---

            # Evidence Packet Fixture

            This file exists so support_checked annotations can point to a
            review object. It is not a real reviewed evidence packet.
            """
        ).strip()
        + "\n",
    )


def main() -> None:
    clean_generated()
    sources = make_sources()
    write_support_files()
    good = build_good_annotations(sources)
    good_root = SAMPLES / "annotations"
    for record in good:
        write_annotation(record, good_root)
        for candidate_ref in record.get("candidate_refs", []):
            write_text(
                ROOT / candidate_ref,
                f"---\nrecord_kind: candidate_distillation\nstatus: sandbox_fixture\n---\n\n# {record['annotation_id']} Candidate Fixture\n",
            )

    mutation_root = SAMPLES / "mutations"
    for record in build_mutations(good):
        write_annotation(record, mutation_root)

    bad_context = {
        "context_pack_id": "ctx-mut-bad-support-ref",
        "selected_items": [
            {
                "ref": "samples/annotations/ann-web-001.md",
                "record_kind": "source_annotation",
                "pack_role": "support",
                "warning_code": "annotation_not_support",
                "action_basis_allowed": False,
            }
        ],
        "coverage_map": [
            {
                "claim": "annotations can prove support",
                "support_refs": ["samples/annotations/ann-web-001.md"],
            }
        ],
        "warnings": [],
    }
    write_text(
        SAMPLES / "mutations" / "bad-context-pack.json",
        yaml.safe_dump(bad_context, sort_keys=False, allow_unicode=False),
    )
    print(f"generated {len(good)} good annotations and 7 mutation annotations")


if __name__ == "__main__":
    main()
