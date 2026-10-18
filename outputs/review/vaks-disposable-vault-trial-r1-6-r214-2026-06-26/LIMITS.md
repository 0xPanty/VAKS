# R1.6 Limits

This is still a bounded sandbox. It proves the local disposable-vault release
boundary for frozen R1.5 adapter outputs, adversarial paths, and
Obsidian-shaped vault objects inside a disposable shadow vault.

It does not prove:

- production runtime readiness;
- real Obsidian plugin behavior;
- real Obsidian Markdown rendering behavior;
- live LLM or retrieval behavior;
- real IAM or feature-flag provider integration;
- real user traffic quality;
- reviewed truth, promotion, or action readiness.

The formal Obsidian vault is only used as a rejected path probe. No file is
created there.

Quick or partial bundles are probe evidence only. Formal closeout evidence must
carry `evidence_profile: formal`, all four self-tests passing, and formal-scale
coverage floors; a self-consistent downgrade to `not_run` self-tests is not
accepted as closeout evidence.

On Windows, the junction escape case uses a local WinAPI reparse-point helper
to construct a filesystem attack shape inside the disposable workspace. This is
not a shell command, network, service, database, LLM, retrieval, or formal-vault
write.
