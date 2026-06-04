import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "review_packet_operator_adjudication_narrow"


def read_csv(path):
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames=None):
    if not rows and not fieldnames:
        raise ValueError("fieldnames required for empty csv")
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames or list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def double_review_core_rows(core_gold):
    rows = []
    for item in core_gold:
        for reviewer in ["reviewer_A", "reviewer_B"]:
            rows.append(
                {
                    "reviewer_id": reviewer,
                    "sample_id": item["sample_id"],
                    "case_id": item["case_id"],
                    "packet": "core_24",
                    "time_to_triage_seconds": "",
                    "state_choice_ordinary_for_review_blocking_regressed_resolved": "",
                    "state_understood_y_n": "",
                    "risk_reason_understood_y_n": "",
                    "next_action_save_review_fix_anchor_full_audit_not_actionable": "",
                    "would_open_full_audit_y_n": "",
                    "wrong_actionability_y_n": "",
                    "serious_miss_y_n": "",
                    "source_entry_clicked_y_n": "",
                    "source_correct_quote_found_y_n": "",
                    "record_entry_clicked_y_n": "",
                    "evidence_entry_clicked_y_n": "",
                    "clickback_product_success_y_n": "",
                    "authority_misunderstanding_y_n": "",
                    "count_or_lineage_misread_y_n": "",
                    "burden_1_light_5_heavy": "",
                    "notes": "",
                }
            )
    return rows


def double_review_adversarial_rows(adv_gold):
    rows = []
    for item in adv_gold:
        for reviewer in ["reviewer_A", "reviewer_B"]:
            rows.append(
                {
                    "reviewer_id": reviewer,
                    "sample_id": item["sample_id"],
                    "case_id": item["case_id"],
                    "packet": "adversarial_12",
                    "adversarial_category": item["adversarial_category"],
                    "time_to_triage_seconds": "",
                    "trap_recognized_y_n": "",
                    "next_action": "",
                    "would_open_full_audit_y_n": "",
                    "wrong_actionability_y_n": "",
                    "source_entry_clicked_y_n": "",
                    "source_correct_quote_found_y_n": "",
                    "record_entry_clicked_y_n": "",
                    "evidence_entry_clicked_y_n": "",
                    "clickback_product_success_y_n": "",
                    "authority_misunderstanding_y_n": "",
                    "grouping_misread_y_n": "",
                    "notes": "",
                }
            )
    return rows


def adjudication_rows(core_gold, adv_gold):
    rows = []
    for item in core_gold:
        rows.append(
            {
                "sample_id": item["sample_id"],
                "case_id": item["case_id"],
                "packet": "core_24",
                "reviewer_disagreement_y_n": "",
                "adjudicated_state": "",
                "adjudicated_next_action": "",
                "adjudicated_wrong_actionability_y_n": "",
                "adjudicated_serious_miss_y_n": "",
                "adjudicated_clickback_product_success_y_n": "",
                "adjudicated_authority_misunderstanding_y_n": "",
                "adjudicator_notes": "",
            }
        )
    for item in adv_gold:
        rows.append(
            {
                "sample_id": item["sample_id"],
                "case_id": item["case_id"],
                "packet": "adversarial_12",
                "reviewer_disagreement_y_n": "",
                "adjudicated_state": "",
                "adjudicated_next_action": "",
                "adjudicated_wrong_actionability_y_n": "",
                "adjudicated_serious_miss_y_n": "",
                "adjudicated_clickback_product_success_y_n": "",
                "adjudicated_authority_misunderstanding_y_n": "",
                "adjudicator_notes": "",
            }
        )
    return rows


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    core_gold = read_csv(ROOT / "review_packet_risk_tiered_24" / "hidden_gold_after_done.csv")
    adv_gold = read_csv(ROOT / "review_packet_adversarial_12" / "hidden_gold_after_done.csv")

    write_csv(OUT / "CORE_24_DOUBLE_REVIEW_SHEET_BLANK.csv", double_review_core_rows(core_gold))
    write_csv(OUT / "ADVERSARIAL_12_DOUBLE_REVIEW_SHEET_BLANK.csv", double_review_adversarial_rows(adv_gold))
    write_csv(OUT / "ADJUDICATION_RESOLUTION_SHEET_BLANK.csv", adjudication_rows(core_gold, adv_gold))

    manifest = {
        "status": "blank_human_operator_adjudication_packet",
        "scope": "narrow_real_human_operator_adjudication_only",
        "core_samples": len(core_gold),
        "adversarial_samples": len(adv_gold),
        "reviewers_required": 2,
        "adjudicator_required": True,
        "result_status": "blank_not_run",
        "source_materials": [
            "review_packet_risk_tiered_24/RISK_TIERED_REVIEWER_CARDS_ZH.md",
            "review_packet_adversarial_12/ADVERSARIAL_OPERATOR_CARDS_ZH.md",
        ],
        "hidden_gold_files": [
            "review_packet_risk_tiered_24/hidden_gold_after_done.csv",
            "review_packet_adversarial_12/hidden_gold_after_done.csv",
        ],
        "do_not_claim": [
            "main-vault operation convention readiness",
            "independent human oracle before sheets are filled",
            "product click-back success without reviewer click logs",
            "human timing without measured timestamps",
        ],
    }
    write_json(OUT / "packet_manifest.json", manifest)
    write_json(
        OUT / "GATE_SUMMARY_BLANK.json",
        {
            "status": "blank",
            "go_meaning": "eligible for candidate operation-convention discussion only, not adoption",
            "hard_gates": {
                "wrong_actionability": "blank",
                "serious_miss": "blank",
                "source_record_evidence_clickback_success": "blank",
                "authority_misunderstanding": "blank",
            },
            "product_gates": {
                "triage_time": "blank",
                "full_audit_open_rate": "blank",
            },
            "note": "Fill from double-review and adjudication sheets only. Do not use Codex dry-run as human evidence.",
        },
    )

    (OUT / "README_OPERATOR_ADJUDICATION_NARROW.md").write_text(
        """# Narrow Operator Adjudication Packet

Status: blank human/operator adjudication packet. Sandbox only. No main-vault
writeback, no `SCHEMA.md` change, and no operation-convention promotion.

## Purpose

This is the next step recommended by Pro: a narrow but hard operator
adjudication stage. It tests whether real reviewers/operators can use the
operator surface without misreading actionability, authority, or click-back.

This is not another automatic patch and not a Codex dry-run.

## Source Materials

Reviewers should read these first:

```text
review_packet_risk_tiered_24/RISK_TIERED_REVIEWER_CARDS_ZH.md
review_packet_adversarial_12/ADVERSARIAL_OPERATOR_CARDS_ZH.md
```

Do not open hidden gold before finishing reviewer sheets.

## Sheets To Fill

```text
CORE_24_DOUBLE_REVIEW_SHEET_BLANK.csv
ADVERSARIAL_12_DOUBLE_REVIEW_SHEET_BLANK.csv
ADJUDICATION_RESOLUTION_SHEET_BLANK.csv
GATE_SUMMARY_BLANK.json
```

Use two independent reviewers/operators first. Then one adjudicator resolves
disagreements and records gate outcomes.

## What Counts

- wrong actionability
- serious miss
- authority misunderstanding
- source / record / evidence click-back success
- whether the reviewer found the correct quote/context, not merely a path
- triage time
- whether full audit was opened when needed

## What Does Not Count

- Codex dry-run
- lint pass
- test/report/dashboard pass
- source count, URL count, lineage count
- group count or recurrence count
- local wrapper-only click-back
- path existence without correct quote/context

## Current Boundary

The project remains `not_go_yet` until real reviewer/operator sheets and
adjudication are filled.
""",
        encoding="utf-8",
    )

    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
