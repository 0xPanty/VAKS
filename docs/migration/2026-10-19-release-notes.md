# VAKS Mac migration — 2026-10-19

完整工程、设计细节、研究、实验代码与进度从 `master` 克隆；本 Release 保存六个不纳入 Git 普通对象的大型第三方来源附件，合计 550647508 bytes。

从仓库根目录运行 `python tools/restore_migration_assets.py --download` 可下载、校验 SHA256 并恢复原相对路径。需要已登录 GitHub CLI。脚本不会解包或执行附件，不会覆盖不同的本地文件。

附件路径、尺寸和哈希见 `docs/migration/2026-10-19-release-assets.json`；Mac 环境与继续开发入口见 `START_HERE_MAC.md`。

附件仅是研究来源快照，保留上游权利和许可证；不代表 VAKS 已采纳这些工具，不构成生产能力证明。含凭据的其他原始资料已从上传范围隔离，脱敏记录见 `docs/migration/`。
