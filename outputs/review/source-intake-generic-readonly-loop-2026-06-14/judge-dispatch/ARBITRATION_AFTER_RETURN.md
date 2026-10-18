# Arbitration After Judge Return

Use this only after Judge A and Judge B have returned filled copies.

Minimum arbitration process:

1. Merge Judge A and Judge B scores by `row_id`.
2. For rows where both relevance and sufficiency match, copy the shared score to the arbiter columns.
3. For rows with disagreement, inspect only the visible query, answer/use claim, anchor ref, source hash, frozen snapshot ref, anchor excerpt, and judge notes.
4. Fill:
   - `arbiter_id`
   - `arbiter_judged_at`
   - `arbiter_final_relevance_0_2`
   - `arbiter_final_sufficiency_0_2`
   - `arbiter_notes`

Do not treat arbitration as P0 approval, production runtime validation, or reviewed truth promotion. It only completes independent semantic support judgment for the allowed read-only support rows in this sandbox package.
