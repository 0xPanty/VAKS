# Judge Dispatch Ready To Send

Status: ready_not_judged

Send only the relevant subfolder to each judge.

Judge A gets only:

- `judge-a/semantic-support-judge-a.zip`
- `judge-a/semantic-support-judge-a.zip.sha256`
- `judge-a/MESSAGE_TO_JUDGE_A.md`

Judge B gets only:

- `judge-b/semantic-support-judge-b.zip`
- `judge-b/semantic-support-judge-b.zip.sha256`
- `judge-b/MESSAGE_TO_JUDGE_B.md`

Do not send either judge mapping, expected outcomes, author-side self-check,
the other judge result, arbiter files, the combined ready-to-send zip, or the
full Pro review package.

After each judge returns only their filled CSV, save the files under
`judge-return-results/` and run the merge command in `../JUDGE_RETURN_WORKFLOW.md`.
