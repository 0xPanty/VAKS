# VAKS：Mac 开发接续入口

本次迁移基准：2026-10-19。目标仓库：`0xPanty/VAKS`（私有）。此文件用于恢复设计和开发进度；上传不改变候选、实验、已审知识之间的权威边界。

## 先取代码，再恢复上下文

```bash
git clone https://github.com/0xPanty/VAKS.git
cd VAKS
git status
```

私有仓库需要先登录自己的 GitHub 账号。已有克隆时先检查本地修改，再 `git pull --ff-only`，不要覆盖未提交内容。保留原有 `master` 分支及历史；不要默认切到不存在的 `main`。

请依次阅读：

1. [本次迁移与当前进度](00_handoff/2026-10-19-github-mac-continuation.md)。
2. [项目约定](AGENTS.md)、[README](README.md)、[架构主线](FUSION_ARCHITECTURE_V0_2_DRAFT.md)、[第二大脑解释模型](SECOND_BRAIN_MODEL.md)。
3. [实现顺序](IMPLEMENTATION_BLUEPRINT.md)、[Schema](SCHEMA.md)、[源码捕获存储](docs/source-capture-store-v1.md)。
4. [保险团队产品方案 draft-2](outputs/review/2026-09-26-vaks-insurance-team-plan-candidate.md)、[Pro 原文评审](outputs/review/2026-09-27-baoyouju-vaks-pro-review-response.md)。

给 Mac 上的新 Agent 的恢复提示：

> 这是 VAKS 的跨机开发恢复。先读 START_HERE_MAC.md 和最新 handoff，再按 AGENTS.md 阅读当前架构。核实当前分支、修改和实现状态。outputs/review 中的实验、评审、通过记录不是生产能力或自动采纳决议。先给出当前状态和一个最小开发切口，不重新堆一套架构；后续实施以我当前要求为准。Windows 盘符是历史环境，不是 Mac 上可执行的默认配置。

## Python 工具的最小环境

当前主体是 Markdown / JSON / Python CLI，没有统一 Web 服务启动入口。Source Capture manifest 声明 Python >= 3.10；完整工具中有 PyYAML 依赖，尚无覆盖所有实验的锁文件。

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install PyYAML
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$(python -c 'import pathlib,tempfile; print(pathlib.Path(tempfile.gettempdir()).resolve())')"

python tools/build_source_capture_implementation_manifest.py --check
python tools/vaks_guard.py self-test
python tools/selftest_source_capture.py
python tools/selftest_source_capture_store.py
```

这些自检使用本地 fixture / 临时目录，不连接收费模型 API，不写正式知识库。`--check` 不可省略，否则 manifest 工具会写文件。macOS 的 `/var` 常经符号链接，先解析 TMPDIR 是为避免 Store 的祖先符号链接检查拒绝临时路径。这里的命令经过静态检查及 Windows 基础自检；尚未在真实 Mac 验证。

不要把 `normalize_*`、`relocate_*`、视频 finalize、大规模运行时试验或所有 `validate_*` 批量执行当作环境检查：部分命令会写报告、调整文件或需要单独配置。

## 正式知识库、历史副本和大附件

- 原 Windows 工程：`C:\Users\Administrator\Documents\资料库`；正式 Obsidian vault：`H:\Obsidian\资料库`。两者原本就不完全相同。
- 本次补入正式 vault 的项目缺失文件，并保留不同版本的迁移快照及比对记录；不按修改时间覆盖当前仓库。详见 [迁移清单目录](docs/migration/)。
- 可用 Obsidian 打开克隆目录浏览。`.obsidian` 配置、插件、登录状态、工作区布局未迁移；Mac 的正式 vault 路径由你本机选择，不能继续使用 H 盘路径。
- 六个大型来源下载按清单作为私有 GitHub Release 附件保存。运行下面的恢复工具前先安装并登录 GitHub CLI；普通代码阅读和开发不依赖这些附件。

```bash
python tools/restore_migration_assets.py --download
```

该工具只下载清单指定附件、验证 SHA256 并恢复原相对路径，不解包、不运行其中内容；遇到已存在但哈希不同的文件会停止。

## 已知平台差异

- `tools/new-video-source-card.ps1` 调用 Windows `powershell`；`tools/finalize-video-intake.ps1` 默认写 H 盘。Mac 不能原样运行这条流程，先显式适配调用与目标路径。
- R1.4 / R1.6 实验仍含 `H:/Obsidian/资料库`，且 R1.6 含 Windows 属性 / junction 检查。在 Mac 上该字符串不等同于 Windows 绝对路径；先适配再运行。
- 不为迁移全库转换编码、换行或重写历史路径：现有来源锚点、hash、实验记录依赖原始字节。仅将当前工作配置改为 Mac 路径。
- Git 同步项目内容与历史，不同步浏览器会话、API 密钥、系统 Python 或其他机器环境。Mac 上的运行结果必须重新验证。
