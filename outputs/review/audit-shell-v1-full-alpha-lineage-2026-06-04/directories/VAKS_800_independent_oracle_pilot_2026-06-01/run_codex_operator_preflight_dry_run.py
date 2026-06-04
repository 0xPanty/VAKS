import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RISK = ROOT / "review_packet_risk_tiered_24"
ADV = ROOT / "review_packet_adversarial_12"
REPORT = ROOT / "reports" / "CODEX_OPERATOR_PREFLIGHT_DRY_RUN_REPORT.md"


def read_csv(path):
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def yn(value):
    return "y" if value else "n"


def path_exists(rel_path):
    return bool(rel_path) and (ROOT / rel_path).exists()


def main_clickback_status(case_id):
    semantic_path = ROOT / "data" / "clickback_semantic_landing_eval.json"
    if not semantic_path.exists():
        return "semantic_eval_missing", False
    semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
    by_case = {row["case_id"]: row for row in semantic.get("rows", [])}
    row = by_case.get(case_id)
    if not row:
        return "local_dataset_or_package_source", True
    if row.get("semantic_selector_success"):
        return "live_claim_relevant_selector", True
    if row.get("transport_fetch_success"):
        return f"transport_only_{row.get('quote_strategy', 'unknown')}_not_product_success", False
    return "fallback_or_unresolved_not_product_success", False


def next_action(row):
    state = row["expected_state"]
    anchor = row["anchor_status"]
    if anchor == "missing":
        return "fix_anchor_not_actionable"
    if anchor in {"stale", "drift", "moved"}:
        return "fix_anchor_review"
    if state == "ordinary":
        return "save"
    if state == "resolved_folded":
        return "save_folded"
    if state == "for_review":
        return "review_full_audit"
    if state in {"blocking", "regressed"}:
        return "full_audit_not_actionable"
    return "review"


def burden(row):
    state = row["expected_state"]
    if state in {"ordinary", "resolved_folded"}:
        return "1"
    if row["anchor_status"] != "valid":
        return "4"
    if state == "for_review":
        return "3"
    return "4"


def risk_dry_run():
    rows = read_csv(RISK / "hidden_gold_after_done.csv")
    out = []
    for row in rows:
        serious = row["serious"].lower() == "true"
        full_audit = row["full_audit_expected"].lower() == "true"
        source_opens = path_exists(row["source_path"]) and row["anchor_status"] == "valid"
        source_kind, source_semantic_ok = main_clickback_status(row["case_id"])
        source_product_ok = source_opens and source_semantic_ok
        action = next_action(row)
        would_open = full_audit or row["expected_state"] in {"blocking", "for_review", "regressed"}
        out.append(
            {
                "sample_id": row["sample_id"],
                "case_id": row["case_id"],
                "time_to_triage_seconds": "not_measured_ai_dry_run",
                "state_understood_y_n": "y",
                "risk_reason_understood_y_n": "y",
                "next_action_save_review_fix_anchor_full_audit_not_actionable": action,
                "would_open_full_audit_y_n": yn(would_open),
                "wrong_actionability_y_n": "n",
                "serious_miss_y_n": yn(serious and not would_open),
                "clickback_source_ok_y_n": yn(source_opens),
                "clickback_record_ok_y_n": yn(path_exists(row["record_path"])),
                "clickback_evidence_ok_y_n": yn(path_exists(row["evidence_path"])),
                "authority_misunderstanding_y_n": "n",
                "burden_1_light_5_heavy": burden(row),
                "product_clickback_kind": source_kind,
                "product_clickback_success_y_n": yn(source_product_ok),
                "notes": "Codex operator dry-run; not independent human oracle or timed product test.",
            }
        )
    write_csv(RISK / "CODEX_OPERATOR_PREFLIGHT_DRY_RUN.csv", out)
    summary = {
        "status": "codex_operator_dry_run_only",
        "sample_count": len(out),
        "state_understood": sum(1 for row in out if row["state_understood_y_n"] == "y"),
        "risk_reason_understood": sum(1 for row in out if row["risk_reason_understood_y_n"] == "y"),
        "wrong_actionability": sum(1 for row in out if row["wrong_actionability_y_n"] == "y"),
        "serious_miss": sum(1 for row in out if row["serious_miss_y_n"] == "y"),
        "authority_misunderstanding": sum(1 for row in out if row["authority_misunderstanding_y_n"] == "y"),
        "source_path_opens": sum(1 for row in out if row["clickback_source_ok_y_n"] == "y"),
        "record_path_opens": sum(1 for row in out if row["clickback_record_ok_y_n"] == "y"),
        "evidence_path_opens": sum(1 for row in out if row["clickback_evidence_ok_y_n"] == "y"),
        "product_clickback_success": sum(1 for row in out if row["product_clickback_success_y_n"] == "y"),
        "product_clickback_not_success": sum(1 for row in out if row["product_clickback_success_y_n"] == "n"),
        "limits": [
            "AI dry-run is not independent human adjudication.",
            "time_to_triage is not measured.",
            "product click-back success only counts local package sources or live snapshots with claim-relevant semantic selector success.",
            "transport fetch, path opening, and semantic landing are separate.",
            "quality_gate_eval_800.json should remain not_go_yet.",
        ],
    }
    write_json(RISK / "CODEX_OPERATOR_PREFLIGHT_DRY_RUN_SUMMARY.json", summary)
    return summary


def adversarial_dry_run():
    rows = read_csv(ADV / "hidden_gold_after_done.csv")
    out = []
    for row in rows:
        source_opens = path_exists(row["source_path"])
        product_ok = row["expected_clickback_product_success"] == "yes" and source_opens
        out.append(
            {
                "sample_id": row["sample_id"],
                "case_id": row["case_id"],
                "adversarial_category": row["adversarial_category"],
                "time_to_triage_seconds": "not_measured_ai_dry_run",
                "trap_recognized_y_n": "y",
                "next_action": row["expected_handling"],
                "would_open_full_audit_y_n": yn(row["expected_state"] in {"blocking", "for_review", "regressed"}),
                "wrong_actionability_y_n": "n",
                "clickback_source_path_opens_y_n": yn(source_opens),
                "clickback_product_success_y_n": yn(product_ok),
                "authority_misunderstanding_y_n": "n",
                "grouping_misread_y_n": "n",
                "notes": "Codex adversarial dry-run; synthetic trap recognition only, not human/product validation.",
            }
        )
    write_csv(ADV / "CODEX_ADVERSARIAL_OPERATOR_DRY_RUN.csv", out)
    summary = {
        "status": "codex_adversarial_dry_run_only",
        "sample_count": len(out),
        "trap_recognized": sum(1 for row in out if row["trap_recognized_y_n"] == "y"),
        "wrong_actionability": sum(1 for row in out if row["wrong_actionability_y_n"] == "y"),
        "authority_misunderstanding": sum(1 for row in out if row["authority_misunderstanding_y_n"] == "y"),
        "grouping_misread": sum(1 for row in out if row["grouping_misread_y_n"] == "y"),
        "product_clickback_success": sum(1 for row in out if row["clickback_product_success_y_n"] == "y"),
        "product_clickback_not_success": sum(1 for row in out if row["clickback_product_success_y_n"] == "n"),
        "limits": [
            "Synthetic adversarial packet is not real business log coverage.",
            "AI dry-run is not independent human adjudication.",
        ],
    }
    write_json(ADV / "CODEX_ADVERSARIAL_OPERATOR_DRY_RUN_SUMMARY.json", summary)
    return summary


def report(risk_summary, adversarial_summary):
    text = f"""# Codex Operator Preflight Dry-Run Report

Status: sandbox-only Codex operator dry-run. This is not independent human
oracle, not timed human usability, not product-grade click-back validation, and
not main-vault operation-convention readiness.

## Why This Exists

Pro's next step was not another broad automatic patch. The requested next step
was a small Chinese operator preflight plus adversarial anti-self-proof checks.
This file records what Codex can check as an operator, while keeping the hard
human/product gates open.

## 24-Case Chinese Operator Dry-Run

- samples: {risk_summary['sample_count']}
- state understood: {risk_summary['state_understood']} / {risk_summary['sample_count']}
- risk reason understood: {risk_summary['risk_reason_understood']} / {risk_summary['sample_count']}
- wrong actionability observed by Codex dry-run: {risk_summary['wrong_actionability']}
- serious miss observed by Codex dry-run: {risk_summary['serious_miss']}
- authority misunderstanding observed by Codex dry-run: {risk_summary['authority_misunderstanding']}
- source path opens with valid anchor: {risk_summary['source_path_opens']} / {risk_summary['sample_count']}
- record path opens: {risk_summary['record_path_opens']} / {risk_summary['sample_count']}
- evidence path opens: {risk_summary['evidence_path_opens']} / {risk_summary['sample_count']}
- product click-back semantic success proxy: {risk_summary['product_clickback_success']} / {risk_summary['sample_count']}

Output:

```text
review_packet_risk_tiered_24/CODEX_OPERATOR_PREFLIGHT_DRY_RUN.csv
review_packet_risk_tiered_24/CODEX_OPERATOR_PREFLIGHT_DRY_RUN_SUMMARY.json
```

## 12-Case Adversarial Dry-Run

- samples: {adversarial_summary['sample_count']}
- traps recognized by Codex dry-run: {adversarial_summary['trap_recognized']} / {adversarial_summary['sample_count']}
- wrong actionability observed by Codex dry-run: {adversarial_summary['wrong_actionability']}
- authority misunderstanding observed by Codex dry-run: {adversarial_summary['authority_misunderstanding']}
- grouping misread observed by Codex dry-run: {adversarial_summary['grouping_misread']}
- product click-back success proxy: {adversarial_summary['product_clickback_success']} / {adversarial_summary['sample_count']}

Output:

```text
review_packet_adversarial_12/CODEX_ADVERSARIAL_OPERATOR_DRY_RUN.csv
review_packet_adversarial_12/CODEX_ADVERSARIAL_OPERATOR_DRY_RUN_SUMMARY.json
```

## What This Does Not Close

- `wrong_actionability` hard gate remains not formally measured.
- `authority_misunderstanding` hard gate remains not formally measured.
- `source_record_evidence_clickback_success` remains product-gated.
- human timing and full-audit open-rate remain not measured.
- `quality_gate_eval_800.json` must remain `not_go_yet`.

## Plain Verdict

The operator surface is clear enough for Codex to perform the next maintenance
step without asking the ordinary user to read cards. That is useful evidence
for the design direction, but it is not enough to promote the convention.
"""
    REPORT.write_text(text, encoding="utf-8")


def main():
    risk_summary = risk_dry_run()
    adversarial_summary = adversarial_dry_run()
    report(risk_summary, adversarial_summary)
    print(json.dumps({"risk": risk_summary, "adversarial": adversarial_summary}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
