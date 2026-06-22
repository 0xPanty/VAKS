# Semantic Support Judgment Instructions

Status: packet generated, not judged.

Judge only the visible query, answer/use claim, anchor ref, source hash / frozen snapshot ref, and anchor excerpt.

The `row_id` column is opaque. The judge-only packet intentionally excludes case IDs, expected outcomes, internal self-check results, and row-to-case mapping.

Fill `judge_a_id` / `judge_b_id` and `judge_a_judged_at` / `judge_b_judged_at` when judging. Use stable pseudonymous IDs if real names should not be exposed. The arbiter should fill `arbiter_id` and `arbiter_judged_at` only after comparing both independent judgments.

The judge-only zip is excerpt-based and should be judged from the visible `query`, `answer_use_claim`, and `anchor_excerpt` only. If the excerpt is insufficient or truncated, score relevance/sufficiency as 0 or 1 and explain in notes. Do not request or use the full Pro review package. `anchor_source_hash` and `frozen_snapshot_ref` are return-side audit fields, not judge-side evidence expansion instructions.

Scores:

- relevance: 0 = not relevant, 1 = partially relevant, 2 = directly relevant.
- sufficiency: 0 = does not support the claim, 1 = weak/partial support, 2 = sufficient support for this read-only answer/use claim.

Two independent judges should fill judge A and judge B columns before any arbitration.
This packet does not prove independent/external semantic support until judgments are filled and adjudicated.
