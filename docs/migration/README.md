# 2026-10-19 Windows → GitHub → Mac 迁移

目标：[私有仓库 0xPanty/VAKS](https://github.com/0xPanty/VAKS)。Mac 首先阅读根目录 `START_HERE_MAC.md`。

## 完整性与恢复材料

| 文件 | 用途 |
|---|---|
| `2026-10-19-vault-comparison.json` | 同步前两个位置的完整项目文件比对，含路径、尺寸、SHA256 与排除项；快照时间早于新增迁移文件 |
| `2026-10-19-vault-transfer.json` | 1026 次复制收据：891 个缺失路径补齐、135 个不同版本／旧路径存档；每份复制核对 SHA256 |
| `2026-10-19-release-assets.json` | 六个大型来源附件的原相对路径、Release 名称、字节数与 SHA256；总计 550647508 bytes |
| `2026-10-19-redactions.json` | 两份含 JWT 的公开来源下载文件处理记录；原件留在本地，提供脱敏参考副本 |
| `2026-10-19-ragflow-redaction.json` | 第三方 RAGFlow 源码归档中凭据／私钥内容的剔除记录及安全副本哈希 |
| `sanitized-reference-files/` | 脱敏参考副本，不是原始证据；原来源 hash 不适用于这些副本 |

源文件和归档副本的候选／历史状态保持不变。正式 vault 与工程都有独有材料；此次迁移不是把正式 vault 宣布为唯一当前代码来源。历史评审 ZIP 保留当时内容，不重写其 manifest。

## 纳入 Git

根架构与开发说明，全部 handoff、docs、schemas、policies、templates、tests、tools，wiki 知识与索引，raw 来源与文本、图像及普通快照，outputs 下研究、评审、实验代码／fixtures／结果、产品方案和 Pro 原文，以及正式 vault 的补充文件与不同版本存档。原有 Git 历史随 `master` 保留。

`.gitattributes` 默认禁用自动文本换行转换，保留来源、证据和归档的实际字节；既有七项 LF 规则仍生效。本次不批量转换文件内容。Windows 本仓库启用了 `core.longpaths` 以纳入较深的实验路径。

## 附件恢复

六个大文件保存到同一私有仓库的 `migration-2026-10-19` Release。克隆后，在已登录 GitHub CLI 的环境运行：

```bash
python tools/restore_migration_assets.py --download
```

不带参数时只检查本地六个文件。工具验证大小与 SHA256，拒绝覆盖不同内容，不解包、不执行。

## 明确没有上传的东西

- 根目录个人陈述和三张证件照：与 VAKS 无关。
- `.git` 的本机配置和凭据、`.obsidian` 配置／插件／布局、空 `.codex` / `.agents` 本机目录、系统依赖。
- `temp/`、Python 缓存、一次性 `_disposable_vault_workspace/` 和运行锁。实验代码、结果、契约、fixtures 和 r218 未见完成结果这一事实仍保存。
- 两个含 JWT 的原始下载文件，以及含未确认凭据与私钥的原始 RAGFlow ZIP。保留其本地原件与原 SHA256；上传可阅读的脱敏副本，避免改变原始证据后伪装成原件。

六个大文件属于“在 Release 单独保存”，不属于遗漏。基础源文件、候选笔记和实验报告没有因文件数量多而整体排除。

## 验证含义

本次在 Windows / Python 3.12.14 通过 implementation manifest check（6 组件）、Guard self-test（7 类检查）、Source Capture 99 项及 Store 62 项测试。对仓库历史、当前资料、压缩包及正式 vault 增量做了凭据格式和路径检查，并复核测试向量误报。格式扫描不是绝对无秘密保证。

Mac 上需要再跑实际环境检查；本次没有把历史 sandbox 通过计作生产能力，没有执行第三方归档中的代码，也没有调用付费模型 API。
