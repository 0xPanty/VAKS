---
type: library_review
status: draft
library_name: "microsoft/markitdown"
repo_url: "https://github.com/microsoft/markitdown"
source_url: "https://github.com/microsoft/markitdown"
checked_commit: "e144e0a2be95b34df17433bac904e635f2c5e551"
commit_time: "2026-05-26T22:40:20Z"
source_status: active
reviewed_at: 2026-06-07
domain: document-to-markdown conversion
related_projects:
  - verified-action-knowledge-system
current_branch: source-intake / file-distillation
extracted_patterns:
  - file-to-markdown-adapter-before-comprehension
  - optional-dependency-format-router
  - converter-fixture-matrix
  - narrow-conversion-api-wrapper
fusion_decision: adapt
confidence: medium
evidence_count: 18
cross_validated_with:
  - "SOURCE_INTAKE.md"
  - "REFERENCE_REVIEW_PROTOCOL.md"
  - "raw/repos/2026-05-27-openkb-source.md"
negative_evidence:
  - "Broad URI/MCP conversion can read local files or network resources under current process privileges."
  - "Markdown output does not by itself provide reviewed source-span support."
extension_potential: high
relations: []
knowledge_status: candidate
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# 库分析：microsoft/markitdown

## 它解决什么问题

它解决的是“各种文件怎么先变成 LLM 好读的 Markdown”。

对 VAKS 来说，这正好卡在 Source Intake 的第一步：

```text
source file -> retained raw markdown -> candidate comprehension
```

它不解决 review、不解决 truth、不解决 evidence sufficiency、不解决 action basis。

## 核心设计

```text
MarkItDown
-> StreamInfo guesses
-> converter registry
-> format-specific converters
-> DocumentConverterResult(markdown)
```

关键设计点：

- core package 默认轻量，格式能力通过 optional dependencies 打开。
- built-in converters 覆盖 PDF, Office docs, HTML, text formats, ZIP, image/audio metadata/transcription, YouTube 等。
- plugins 默认关闭，需要显式启用。
- cloud analyzers 需要显式参数。
- MCP 包提供 `convert_to_markdown(uri)`，方便但需要强安全边界。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:8-12` | Security warning + lightweight file-to-Markdown purpose | Good fit as pre-intake converter | Not truth support |
| `README.md:14-24` | Supported formats | Broad source coverage | Quality varies by format |
| `README.md:91-112` | Optional dependency groups | Install only needed capabilities | Avoid `[all]` default |
| `README.md:342-348` | Narrow conversion API warning | Use `convert_local` / stream wrapper | Do not expose broad URI |
| `packages/markitdown/pyproject.toml:18-51` | Dependencies and extras | Dependency surface is controllable | Cloud extras must be opt-in |
| `_base_converter.py:5-42` | Result + converter base classes | Simple adapter interface | No VAKS metadata by default |
| `_markitdown.py:94-139` | `MarkItDown` class and plugin toggle | Central router | Needs wrapper policy |
| `_markitdown.py:182-205` | Built-in converter registration | Multi-format routing pattern | Built-in order is not VAKS routing |
| `_markitdown.py:428-497` | URI / response conversion | Flexible input modes | Unsafe without allowlists |
| `_markitdown.py:569-578` | Sorted conversion attempts | Fallback design | Need warning capture |
| `_pdf_converter.py:495-584` | PDF table / text fallback | Useful default PDF path | Not page-span enough alone |
| `__main__.py:57-66` | Output file and extension hints | CLI contract idea | VAKS should own output path |
| `__main__.py:90-130` | CU and plugin CLI flags | Explicit capability switches | Keep off by default |
| `markitdown-mcp/__main__.py:20-23` | MCP tool converts URI to Markdown | Useful agent tool shape | Too broad as-is |
| `markitdown-mcp/README.md:132-134` | No auth + current user privilege warning | Strong risk anchor | Sandbox / localhost not enough for VAKS |
| `markitdown-ocr/_plugin.py:19-68` | OCR plugin registers priority converters | Extension design | LLM vision OCR is later-stage |
| `tests/_test_vectors.py:16-260` | Multi-format vectors | Borrow fixture matrix | Tests are not proof for VAKS data |
| `tests/test_module_vectors.py:57-147` | local/stream/http/file/data URI tests | Borrow input-mode matrix | VAKS should forbid several modes by default |

## 当前支线价值

当前支线：

```text
file distillation skill / VAKS source intake
```

它对当前支线：

```text
supports
```

具体价值：

- 给文件蒸馏入口提供现成、活跃、MIT 的转换器候选。
- 能减少 VAKS 自己维护 PDF/DOCX/XLSX/PPTX/HTML/ZIP 解析器的负担。
- optional dependency 和 plugin 结构适合做轻重分级。
- 安全文档能直接转成 VAKS wrapper 的运行边界。

风险：

- 默认宽 API 容易让 agent 读到不该读的本机文件或远程资源。
- 转换 Markdown 容易被误当成 source support。
- OCR / Azure / MCP 会扩大成本、网络、权限和 provenance 风险。
- 对 scanned PDF、复杂表格、页码/行号/单元格定位仍需二次验证。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Very good raw-to-markdown utility for simple wiki/source intake | adapt |
| Dusk workbench | Can feed project workbench with normalized source previews | watch |
| source ingest | Strong value as file adapter | adapt |
| review queue | Can produce candidate text, not review items by itself | adapt |
| schema / reviewed knowledge | No direct fit; no claim/pattern/decision schema | reject direct |
| memory / dev context | Can produce Support/Cold source text for context packs | adapt |
| feedback | Conversion failures can become workflow feedback | watch |
| retrieval / cache | Markdown output can feed BM25/FTS/vector as derived cache | adapt |
| API / MCP / agent access | MCP shape is useful but dangerous without wrapper | design-only |
| viewer / workbench | Markdown previews are useful for human review | adapt |
| publishing | Possible source-to-draft helper, later | watch |
| risk / anti-pattern | Broad local/URI conversion is a strong source-hygiene risk | adapt as warning |

## 值得提炼的模式

### Pattern: file-to-Markdown adapter before candidate comprehension

人话：

```text
先把各种文件洗成 Markdown，再让 VAKS 蒸馏；不要让 parser 同时当 reviewer。
```

Smallest VAKS version:

```text
input file
-> path allowlist
-> source hash
-> MarkItDown local/stream conversion
-> retained raw markdown
-> conversion metadata
-> candidate distillation shell
```

### Pattern: optional dependency by source type

Default install should be small:

```text
markitdown[pdf,docx,xlsx,pptx]
```

Add only when needed:

```text
audio-transcription
youtube-transcription
az-doc-intel
az-content-understanding
markitdown-ocr
```

### Pattern: fixture matrix for converter safety

Borrow test shape:

```text
format
input mode
expected output file
conversion metadata
forbidden side effect
warning capture
```

## 标签与量化

- domain: source ingest
- problem: file content conversion before distillation
- pattern: file-to-markdown-adapter-before-comprehension
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 4
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似设计来源：OpenKB already used MarkItDown for short document conversion; VAKS already treats MarkItDown + manual sections as an alternative in long-document adapter notes.
- 用户历史项目里的相似问题/影子：VAKS needs source cards, transcripts, repo snapshots, and future file intake without turning raw conversion into truth.
- 支持证据：source snapshot shows converter registry, optional extras, CLI, MCP package, OCR plugin, and test vectors.
- 反例或失败边界：MCP read-any-URI design conflicts with VAKS path-scoped and action-basis boundaries.
- 最小验证方式：install a narrow optional subset in a sandbox and run local fixtures through a wrapper that records hashes and metadata.

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| MarkItDown can normalize many file types before LLM distillation | SOURCE_INTAKE says source cards are provenance and candidate material is not action basis | candidate_relation | Should VAKS define a formal file-conversion raw artifact? |
| Converted Markdown can feed candidate distillation | Evidence Support Check lives on evidence items, not URLs or generated summaries | missing_evidence | What source locator survives conversion? |
| MCP can expose conversion as an agent tool | Agent memory/tool writes must be quarantined and path-scoped | risk_of | Can a wrapper prove path/network/plugin policy before tool use? |
| Optional dependencies allow light/heavy intake | Processing tier is not authority | candidate_relation | How to record enabled dependency set in provenance? |

边界：

- 相似不是支持。
- 冲突不是自动推翻。
- 重复出现不是自动真理。
- 校准输出是 review input，不是 reviewed relation。

## Support / Challenge Review

- What supports it: README, pyproject extras, converter registry, CLI, test vectors, MCP/OCR packages.
- What challenges it: broad I/O privilege, weak source-span preservation, MCP auth warning, cloud/OCR cost and provenance.
- Challenge severity: major if exposed to agents without wrapper; minor if used as a local one-shot converter.
- Scope limits: source conversion only, not claim review or evidence support.
- Known risks: private file access, remote URI fetches, ZIP recursion, plugin priority replacement, silent OCR/cloud drift.
- Review again when: implementing real VAKS file intake or enabling MCP/OCR/cloud.
- Action readiness: needs_review.

边界：

- provenance 不是 support。
- 有引用不等于有证据。
- 支持变多不自动提高 confidence。

## 关系边 / 关联强度

```yaml
relations:
  - target: "[[source-intake-file-to-markdown-adapter]]"
    type: derived_from
    relation_state: candidate
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-06-07-microsoft-markitdown-source]]"
    rationale: "MarkItDown provides a concrete multi-format conversion adapter that can precede VAKS candidate distillation."
    created: 2026-06-07
    last_verified: 2026-06-07
```

## 对当前项目的适配点

Best fit:

```text
VAKS file distillation skill
```

Minimal local contract:

```yaml
input:
  allowed_path_root:
  file_path:
  source_url:
  processing_tier: light | medium | heavy
policy:
  network_allowed: false
  plugins_enabled: false
  cloud_allowed: false
  max_file_size_mb:
output:
  raw_source_card:
  retained_markdown:
  conversion_metadata:
  candidate_distillation:
```

## 可拓展性

- 是否适合作为插件/适配层：是，适合作为 source adapter。
- 是否会绑定核心结构：不应该；应包在 VAKS wrapper 后面。
- 未来替换成本：低，只要 wrapper contract 稳定，可替换为 pandoc, pymupdf, unstructured, Azure, or custom parser。
- 可迁移路径：先 local wrapper，后 fixture matrix，再按文件类型补专业 adapter。

## 复杂度和风险

Complexity:

- Low for local DOCX/PDF/PPTX/XLSX conversion.
- Medium for reliable PDF tables/scanned docs.
- High for MCP, arbitrary URI, OCR, cloud analyzers, ZIP recursion.

Risks:

- Permission overreach.
- Generated Markdown treated as raw source support.
- Missing page/line/cell locators.
- Optional dependency sprawl.
- Cloud/API use without provenance.

## 不可行点 / 避坑

- 可能失败的条件：complex scanned PDFs, heavy tables, handwritten content, private docs with embedded media, malformed files.
- 已知反例：MCP tool can read current user's accessible files unless sandboxed.
- 相似踩坑：OpenKB-style auto-compile into wiki concepts is not VAKS truth-compatible.
- 应该避开的实现方式：`markitdown[all]` + broad `convert(uri)` + write straight to `wiki/claims`.
- 更稳的替代方案：narrow local wrapper + retained markdown + metadata + candidate-only output.

## 融合判断

- 结论：adapt
- 理由：它精准补 Source Intake 的文件转换缺口，但不能进入 review/truth/action 层。
- 验证方式：sandbox fixture run with real VAKS sample files; compare output quality, metadata completeness, and forbidden side effects.

## 直接判断

- Direct use: yes, as a local converter candidate behind VAKS wrapper.
- Fork: not now.
- Design-only: MCP/OCR/cloud/plugin priority model for now.
- Reject: broad URI/MCP/default cloud/default plugins.
- Current branch value: strong for file distillation skill.
- Whole architecture value: strong for source ingest; medium for retrieval/cache; risk reference for agent access.
- Risk: permission, network, locator loss, generated text authority confusion.
- Next action: keep as candidate-only; if implementing, write wrapper contract and fixtures before running on real user files.

## 后续行动

- Add a VAKS file-distillation wrapper design note only after user asks for implementation.
- Start with local files only: PDF/DOCX/XLSX/PPTX/HTML/TXT/MD.
- Record original hash, converted markdown hash, converter version, source path, warnings, and policy flags.
- Require explicit approval for network, OCR, Azure, plugins, MCP, or ZIP recursion.
