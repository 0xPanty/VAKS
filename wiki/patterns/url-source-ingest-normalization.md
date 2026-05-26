---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - OpenKB
related_concepts:
  - "[[source-adapter-ingest-contract]]"
  - "[[2026-05-27-openkb-architecture-review]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt-candidate
tags:
  - pattern/source-adapter
  - url-ingest
  - normalization
evidence_count: 1
confidence: high
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[source-adapter-ingest-contract]]"
    type: refines
    strength: 4
    confidence: high
    evidence:
      - "[[url-source-ingest-normalization]]"
    rationale: "URL sources need safe fetch, content-type sniffing, filename normalization, and clean extraction before compilation."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - source adapters
---

# 设计模式：URL Source Ingest Normalization

## 一句话定义

远程 URL 入库时，先安全下载、识别真实内容类型、清洗正文、生成唯一 raw 文件，再交给普通本地文件 ingest 流程。

## 解决的问题

网页和 PDF URL 很脏：

- server Content-Type 可能错。
- DOI/短链接会跳转。
- HTML 可能有导航、cookie、footer 噪音。
- 两个页面标题可能相同，保存时互相覆盖。
- 大 PDF 不能一次性读进内存。

OpenKB 的 URL ingest 有几个好细节：

```text
magic bytes beat declared content type
PDF chunked download
Content-Disposition filename priority
HTML trafilatura main-content extraction
short extraction warning
unique filename suffix
then pass local raw file to normal ingest
```

## 适用场景

- 用户丢 URL 进资料库。
- 需要把网页/PDF 统一变成 raw source。
- 后续需要保留 raw 文件和 provenance。

## 不适用场景

- 需要浏览器登录/cookie 的页面。
- JS-heavy 页面，trafilatura 抽不出正文。
- 需要完整网页归档而非正文抽取。

## 反例与避坑

- 失败条件：把 URL 文本直接交给 LLM。
- 相似反模式：保存整页 HTML，导致导航和广告进入 summary。
- 复杂度风险：抓取器变成浏览器自动化产品。
- 替代方案：用户手动保存 PDF/Markdown 到 raw。

## 来源证据

OpenKB `url_ingest.py` 先 sniff PDF/HTML，再分别走 chunked PDF download 或 trafilatura HTML extraction，并用 `_unique_path` 避免 raw 文件覆盖。

## 标签与量化

- domain: source ingest
- problem: remote source acquisition
- maturity: proven
- complexity: medium
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：OpenKB、一般 web clipping/source adapter。
- 历史项目影子：资料库会持续收网页、GitHub、论文 PDF。
- 支持证据：OpenKB 把 URL ingest 独立成 input-acquisition layer。
- 反例：高度动态页面仍需要手动或浏览器采集。

## 最小实现方式

v0.1 先不自动抓网页，但定义记录字段：

```yaml
source_url:
fetch_method: manual | url-fetch | browser-export
content_type_declared:
content_type_detected:
raw_path:
extraction_warning:
```

未来 source adapter 再实现：

```text
url -> raw file -> source record -> candidate compile
```

## 项目融合建议

作为 source adapter 候选进入 blueprint。优先级低于 review queue 和 lint，但高于重型检索。

## 可拓展性

- 可以通过什么接口/适配层接入：source adapter。
- 未来可能被什么替代：browser clipper、readability、Firecrawl、Jina Reader、Playwright。
- 替换或升级成本：低，只要 raw/source record contract 不变。
- 回退方式：手动保存原文到 raw。

## 验证指标

- PDF/HTML 是否识别正确。
- 失败时是否不写半成品 formal node。
- raw 文件是否不覆盖。
- extraction warning 是否进入 review。
