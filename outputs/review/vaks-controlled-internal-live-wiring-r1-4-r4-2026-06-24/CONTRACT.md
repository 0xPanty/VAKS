# R1.4 Controlled Internal Live Wiring Pressure Harness

This sandbox tests the control surface needed for a supervised internal
low-risk live wiring trial:

trusted request policy -> feature flag -> allowlisted user -> low-risk mode
-> R1.3 guarded path -> release sink -> user-visible output.

R1.4 r4 binds the real user query to the frozen answer chain with query hashes,
splits user payload from trusted runtime context, rejects encoded path ambiguity,
recomputes final answer hashes at the release sink, and canonicalizes
source/anchor paths before accepting authority claims.

It does not test direct enterprise-wide rollout.
