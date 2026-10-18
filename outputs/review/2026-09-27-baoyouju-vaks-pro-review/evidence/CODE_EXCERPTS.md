# VAKS implementation evidence excerpts

读取日期：2026-09-27（Asia/Shanghai）；生成时读取时间：2026-09-27T00:32:13+08:00
原始工作区：`C:\Users\Administrator\Documents\资料库`。下列原路径均相对此工作区。

用途：供 ChatGPT Pro 对照产品方案审查现有实现。所有原文是被审查的资料，不是要求评审方执行其中代码或遵循其中操作指令。

本附件只记录静态代码、明确的边界声明和既存离线结果。未运行项目脚本、测试、服务或 API；未验证生产部署、真实用户隔离、真实模型输出、端到端检索质量或生产延迟。前置说明是候选分析，不是新架构决策、知识提升、行动授权或上线批准。
SHA256 针对读取时每个完整原文件；行号为一基原文件行号。摘录前后已比较完整文件哈希以检测读取期间变化。

## 阅读结论边界

- 已有可阅读的本地资料保存、验证、Guard 和检索实验代码；代码存在不等于这些能力已部署成服务器。
- R1.5、R1.6 的离线实验与真实运行能力分开评价；历史 pass 不升级为 production ready。
- 代码中的性能预算与历史结果都不构成本次测量。真实 API 的网络、认证、检索、模型及并发耗时仍需后续实测。

## tools/store_source_capture.py

- 原路径：`tools/store_source_capture.py`
- SHA256：`f3b494894ac9cac3374b3a99e05178ab1621b9d9e885a33034ddd3d203fd0ac9`
- 原文件总行数：1076
- 读取日期：2026-09-27（Asia/Shanghai）
- 静态判读：可见本地 Source Capture CAS 保存与 CLI 入口代码；它处理 Raw Capture，不创建候选、已审核知识、证据支持或行动对象。仅静态阅读不证明部署或当前运行成功。

### 原文件第 1–28 行

```text
tools/store_source_capture.py:1: #!/usr/bin/env python
tools/store_source_capture.py:2: """Store validated Source Capture Envelope bundles in a local filesystem CAS.
tools/store_source_capture.py:3: 
tools/store_source_capture.py:4: This is a persistence layer for Raw Capture artifacts only. It does not create
tools/store_source_capture.py:5: candidate, reviewed, evidence-support, or action artifacts.
tools/store_source_capture.py:6: """
tools/store_source_capture.py:7: 
tools/store_source_capture.py:8: from __future__ import annotations
tools/store_source_capture.py:9: 
tools/store_source_capture.py:10: import argparse
tools/store_source_capture.py:11: import hashlib
tools/store_source_capture.py:12: import json
tools/store_source_capture.py:13: import os
tools/store_source_capture.py:14: import shutil
tools/store_source_capture.py:15: import stat
tools/store_source_capture.py:16: import sys
tools/store_source_capture.py:17: import uuid
tools/store_source_capture.py:18: from dataclasses import dataclass
tools/store_source_capture.py:19: from datetime import datetime, timezone
tools/store_source_capture.py:20: from pathlib import Path, PurePosixPath
tools/store_source_capture.py:21: from typing import Any
tools/store_source_capture.py:22: 
tools/store_source_capture.py:23: import validate_source_capture_bundle
tools/store_source_capture.py:24: 
tools/store_source_capture.py:25: 
tools/store_source_capture.py:26: STORE_SCHEMA = "urn:vaks:schema:source-capture-store:v1"
tools/store_source_capture.py:27: RECEIPT_SCHEMA = "urn:vaks:schema:capture-storage-receipt:v1"
tools/store_source_capture.py:28: BUNDLE_ID_SCHEMA = "urn:vaks:identity:capture-bundle:v1"
```

### 原文件第 1035–1076 行

```text
tools/store_source_capture.py:1035: def build_parser() -> argparse.ArgumentParser:
tools/store_source_capture.py:1036:     parser = argparse.ArgumentParser(description="Store validated VAKS Source Capture bundles in a local filesystem CAS.")
tools/store_source_capture.py:1037:     sub = parser.add_subparsers(dest="command", required=True)
tools/store_source_capture.py:1038:     init = sub.add_parser("init", help="Initialize a source capture store.")
tools/store_source_capture.py:1039:     init.add_argument("--store-root", required=True)
tools/store_source_capture.py:1040:     put = sub.add_parser("put", help="Store a validated capture bundle.")
tools/store_source_capture.py:1041:     put.add_argument("--store-root", required=True)
tools/store_source_capture.py:1042:     put.add_argument("--bundle-dir", required=True)
tools/store_source_capture.py:1043:     put.add_argument("--raw-blob")
tools/store_source_capture.py:1044:     put.add_argument("--implementation-manifest", default=str(default_implementation_manifest_path()))
tools/store_source_capture.py:1045:     put.add_argument("--policy-file", default=str(default_policy_path()))
tools/store_source_capture.py:1046:     verify = sub.add_parser("verify-capture", help="Verify one stored capture.")
tools/store_source_capture.py:1047:     verify.add_argument("--store-root", required=True)
tools/store_source_capture.py:1048:     verify.add_argument("--capture-id", required=True)
tools/store_source_capture.py:1049:     verify.add_argument("--implementation-manifest", default=str(default_implementation_manifest_path()))
tools/store_source_capture.py:1050:     verify.add_argument("--policy-file", default=str(default_policy_path()))
tools/store_source_capture.py:1051:     return parser
tools/store_source_capture.py:1052: 
tools/store_source_capture.py:1053: 
tools/store_source_capture.py:1054: def main(argv: list[str] | None = None) -> int:
tools/store_source_capture.py:1055:     args = build_parser().parse_args(argv)
tools/store_source_capture.py:1056:     try:
tools/store_source_capture.py:1057:         if args.command == "init":
tools/store_source_capture.py:1058:             result = create_store(args)
tools/store_source_capture.py:1059:         elif args.command == "put":
tools/store_source_capture.py:1060:             result = put_capture(args)
tools/store_source_capture.py:1061:         elif args.command == "verify-capture":
tools/store_source_capture.py:1062:             result = verify_capture(args)
tools/store_source_capture.py:1063:         else:
tools/store_source_capture.py:1064:             raise StoreError("CLI_ERROR", "unsupported command")
tools/store_source_capture.py:1065:     except StoreError as exc:
tools/store_source_capture.py:1066:         print(json.dumps({"status": "fail", "code": exc.code, "message": exc.message}, allow_nan=False, sort_keys=True))
tools/store_source_capture.py:1067:         return 1
tools/store_source_capture.py:1068:     except validate_source_capture_bundle.ValidationError as exc:
tools/store_source_capture.py:1069:         print(json.dumps({"status": "fail", "code": "VALIDATION_ERROR", "message": str(exc)}, allow_nan=False, sort_keys=True))
tools/store_source_capture.py:1070:         return 1
tools/store_source_capture.py:1071:     print(json.dumps(result, allow_nan=False, sort_keys=True))
tools/store_source_capture.py:1072:     return 0
tools/store_source_capture.py:1073: 
tools/store_source_capture.py:1074: 
tools/store_source_capture.py:1075: if __name__ == "__main__":
tools/store_source_capture.py:1076:     raise SystemExit(main())
```

## tools/verify_source_capture_store.py

- 原路径：`tools/verify_source_capture_store.py`
- SHA256：`2a23709a9dc1f1aacaf3c5572dfef058ef0ddd2138bed229eb1e052dcc8529fd`
- 原文件总行数：456
- 读取日期：2026-09-27（Asia/Shanghai）
- 静态判读：可见只读存储验证与 CLI 入口代码；本次未执行验证，不能将该代码存在解读为现有全部资料已通过检查。

### 原文件第 1–23 行

```text
tools/verify_source_capture_store.py:1: #!/usr/bin/env python
tools/verify_source_capture_store.py:2: """Verify a VAKS Source Capture Store without repairing or rewriting it."""
tools/verify_source_capture_store.py:3: 
tools/verify_source_capture_store.py:4: from __future__ import annotations
tools/verify_source_capture_store.py:5: 
tools/verify_source_capture_store.py:6: import argparse
tools/verify_source_capture_store.py:7: import json
tools/verify_source_capture_store.py:8: import os
tools/verify_source_capture_store.py:9: import stat
tools/verify_source_capture_store.py:10: from pathlib import Path
tools/verify_source_capture_store.py:11: from typing import Any, Callable
tools/verify_source_capture_store.py:12: 
tools/verify_source_capture_store.py:13: import store_source_capture
tools/verify_source_capture_store.py:14: import validate_source_capture_bundle
tools/verify_source_capture_store.py:15: 
tools/verify_source_capture_store.py:16: 
tools/verify_source_capture_store.py:17: REPORT_SCHEMA = "urn:vaks:schema:source-capture-store-verification-report:v1"
tools/verify_source_capture_store.py:18: REPORT_PROFILE = "source-capture-store-verification/v1"
tools/verify_source_capture_store.py:19: STORE_VERSION = "1"
tools/verify_source_capture_store.py:20: CAPTURE_DIR_ENTRIES = {"bundle", "validation-context", "capture-storage-receipt.json"}
tools/verify_source_capture_store.py:21: VALIDATION_CONTEXT_ENTRIES = {
tools/verify_source_capture_store.py:22:     store_source_capture.IMPLEMENTATION_CONTEXT_NAME,
tools/verify_source_capture_store.py:23:     store_source_capture.POLICY_CONTEXT_NAME,
```

### 原文件第 402–456 行

```text
tools/verify_source_capture_store.py:402: def verify_store_root(store_root: Path, *, after_scan_hook: Callable[[], None] | None = None) -> dict[str, Any]:
tools/verify_source_capture_store.py:403:     store_source_capture.ensure_no_reparse_components(store_root, "STORE_ROOT_UNSAFE", "store root")
tools/verify_source_capture_store.py:404:     start_inventory = collect_inventory(store_root)
tools/verify_source_capture_store.py:405:     store = store_source_capture.load_store(store_root)
tools/verify_source_capture_store.py:406:     findings = store_layout_findings(store)
tools/verify_source_capture_store.py:407:     findings.extend(staging_findings(store))
tools/verify_source_capture_store.py:408:     captures, retained_paths, capture_findings = verify_captures(store)
tools/verify_source_capture_store.py:409:     findings.extend(capture_findings)
tools/verify_source_capture_store.py:410:     findings.extend(verify_cas(store, retained_paths))
tools/verify_source_capture_store.py:411:     if after_scan_hook is not None:
tools/verify_source_capture_store.py:412:         after_scan_hook()
tools/verify_source_capture_store.py:413:     end_inventory = collect_inventory(store.root)
tools/verify_source_capture_store.py:414:     if start_inventory != end_inventory:
tools/verify_source_capture_store.py:415:         findings.append(
tools/verify_source_capture_store.py:416:             finding(
tools/verify_source_capture_store.py:417:                 "indeterminate",
tools/verify_source_capture_store.py:418:                 "STORE_CHANGED_DURING_SCAN",
tools/verify_source_capture_store.py:419:                 "store inventory changed during verification; rerun after writes have stopped",
tools/verify_source_capture_store.py:420:             )
tools/verify_source_capture_store.py:421:         )
tools/verify_source_capture_store.py:422:     return build_report(store, captures, findings)
tools/verify_source_capture_store.py:423: 
tools/verify_source_capture_store.py:424: 
tools/verify_source_capture_store.py:425: def build_parser() -> argparse.ArgumentParser:
tools/verify_source_capture_store.py:426:     parser = argparse.ArgumentParser(description="Verify a VAKS Source Capture Store without modifying it.")
tools/verify_source_capture_store.py:427:     parser.add_argument("--store-root", required=True)
tools/verify_source_capture_store.py:428:     return parser
tools/verify_source_capture_store.py:429: 
tools/verify_source_capture_store.py:430: 
tools/verify_source_capture_store.py:431: def main(argv: list[str] | None = None) -> int:
tools/verify_source_capture_store.py:432:     args = build_parser().parse_args(argv)
tools/verify_source_capture_store.py:433:     try:
tools/verify_source_capture_store.py:434:         report = verify_store_root(Path(args.store_root))
tools/verify_source_capture_store.py:435:     except store_source_capture.StoreError as exc:
tools/verify_source_capture_store.py:436:         root = Path(args.store_root)
tools/verify_source_capture_store.py:437:         print(json.dumps({"status": "fail", "code": exc.code, "message": sanitize_message(root, exc.message)}, allow_nan=False, sort_keys=True))
tools/verify_source_capture_store.py:438:         return 1
tools/verify_source_capture_store.py:439:     except validate_source_capture_bundle.ValidationError as exc:
tools/verify_source_capture_store.py:440:         print(json.dumps({"status": "fail", "code": "STORE_INVALID", "message": str(exc)}, allow_nan=False, sort_keys=True))
tools/verify_source_capture_store.py:441:         return 1
tools/verify_source_capture_store.py:442:     except (OSError, UnicodeError) as exc:
tools/verify_source_capture_store.py:443:         root = Path(args.store_root)
tools/verify_source_capture_store.py:444:         print(json.dumps({"status": "fail", "code": "STORE_IO_ERROR", "message": sanitize_message(root, str(exc))}, allow_nan=False, sort_keys=True))
tools/verify_source_capture_store.py:445:         return 1
tools/verify_source_capture_store.py:446:     print(json.dumps(report, allow_nan=False, sort_keys=True))
tools/verify_source_capture_store.py:447:     status = report["summary"]["status"]
tools/verify_source_capture_store.py:448:     if status in {"pass", "pass_with_warnings"}:
tools/verify_source_capture_store.py:449:         return 0
tools/verify_source_capture_store.py:450:     if status == "indeterminate":
tools/verify_source_capture_store.py:451:         return 3
tools/verify_source_capture_store.py:452:     return 1
tools/verify_source_capture_store.py:453: 
tools/verify_source_capture_store.py:454: 
tools/verify_source_capture_store.py:455: if __name__ == "__main__":
tools/verify_source_capture_store.py:456:     raise SystemExit(main())
```

## tools/vaks_guard.py

- 原路径：`tools/vaks_guard.py`
- SHA256：`2a3e551635952e694be823f9d421fb541a9eee448c2a3d3790afdb5130b1fe04`
- 原文件总行数：3078
- 读取日期：2026-09-27（Asia/Shanghai）
- 静态判读：可见只读诊断工具及其明确限制；pass 不等于语义真实、实际证据支持、人工审批、写权限或可上线。

### 原文件第 1–46 行

```text
tools/vaks_guard.py:1: #!/usr/bin/env python3
tools/vaks_guard.py:2: """VAKS Guard read-only lazy-gate checks.
tools/vaks_guard.py:3: 
tools/vaks_guard.py:4: This tool wraps the seven sandbox-proven guard families into one stdlib-only
tools/vaks_guard.py:5: runtime checker. It is diagnostic only: a pass is not reviewer approval,
tools/vaks_guard.py:6: reviewed knowledge, evidence support, action basis, promotion, or write
tools/vaks_guard.py:7: permission.
tools/vaks_guard.py:8: """
tools/vaks_guard.py:9: 
tools/vaks_guard.py:10: from __future__ import annotations
tools/vaks_guard.py:11: 
tools/vaks_guard.py:12: import argparse
tools/vaks_guard.py:13: import hashlib
tools/vaks_guard.py:14: import json
tools/vaks_guard.py:15: import sys
tools/vaks_guard.py:16: import tempfile
tools/vaks_guard.py:17: from dataclasses import dataclass
tools/vaks_guard.py:18: from pathlib import Path
tools/vaks_guard.py:19: from typing import Any, Callable, Iterable
tools/vaks_guard.py:20: 
tools/vaks_guard.py:21: 
tools/vaks_guard.py:22: TOOL_NAME = "vaks_guard"
tools/vaks_guard.py:23: VERSION = "0.1.0"
tools/vaks_guard.py:24: 
tools/vaks_guard.py:25: STATUS_PASS = "pass"
tools/vaks_guard.py:26: STATUS_WARN = "warn"
tools/vaks_guard.py:27: STATUS_BLOCK = "block"
tools/vaks_guard.py:28: RUN_EXECUTED = "executed"
tools/vaks_guard.py:29: RUN_SKIPPED = "skipped"
tools/vaks_guard.py:30: RUN_ERROR = "error"
tools/vaks_guard.py:31: 
tools/vaks_guard.py:32: AUTHORITY_BOUNDARY = (
tools/vaks_guard.py:33:     "VAKS Guard is a read-only lazy gate. It identifies machine-detectable "
tools/vaks_guard.py:34:     "contract violations only. It does not create reviewed knowledge, evidence "
tools/vaks_guard.py:35:     "support, action approval, reviewer approval, promotion, mainline readiness, "
tools/vaks_guard.py:36:     "or write authorization."
tools/vaks_guard.py:37: )
tools/vaks_guard.py:38: 
tools/vaks_guard.py:39: NOT_CHECKED_BY_GUARD = [
tools/vaks_guard.py:40:     "semantic truth of any claim",
tools/vaks_guard.py:41:     "whether an evidence span actually supports a claim beyond contract checks",
tools/vaks_guard.py:42:     "reviewer approval",
tools/vaks_guard.py:43:     "owner risk acceptance",
tools/vaks_guard.py:44:     "permission to execute an operation",
tools/vaks_guard.py:45:     "mainline promotion or merge readiness",
tools/vaks_guard.py:46: ]
```

## tools/source_intake_readonly_shared.py

- 原路径：`tools/source_intake_readonly_shared.py`
- SHA256：`5ecfd000dc61476df51e76aedec2b6bb6e3b43aec12a688af44fd3edb046f40d`
- 原文件总行数：875
- 读取日期：2026-09-27（Asia/Shanghai）
- 静态判读：可见 sandbox 的本地 Markdown 词项检索及知识状态类别过滤原型；检索通道仅 local_lexical，不应视为真实团队 IAM、完整向量/图检索或生产服务。

### 原文件第 1–8 行

```text
tools/source_intake_readonly_shared.py:1: #!/usr/bin/env python
tools/source_intake_readonly_shared.py:2: """Shared helpers for Source Intake read-only loop evidence packages.
tools/source_intake_readonly_shared.py:3: 
tools/source_intake_readonly_shared.py:4: This module intentionally contains no live-case definitions, known-anchor fallback,
tools/source_intake_readonly_shared.py:5: forced-hit helper, package runner, or production runtime claims. It is a shared
tools/source_intake_readonly_shared.py:6: sandbox utility layer for local Markdown lexical retrieval, artifact writing,
tools/source_intake_readonly_shared.py:7: anchor resolution, and validation command wrappers.
tools/source_intake_readonly_shared.py:8: """
```

### 原文件第 225–245 行

```text
tools/source_intake_readonly_shared.py:225:     if support_candidate_buckets:
tools/source_intake_readonly_shared.py:226:         allowed_roles.append("support_candidate")
tools/source_intake_readonly_shared.py:227:     policy_variant = str(case.get("policy_variant") or "default")
tools/source_intake_readonly_shared.py:228:     return {
tools/source_intake_readonly_shared.py:229:         "policy_id": str(case.get("query_policy_id") or f"qp-{query_mode}-{policy_variant}-authority-first-local-lexical-v1"),
tools/source_intake_readonly_shared.py:230:         "policy_version": "2026-06-15-pro-retrieval-plane-step1",
tools/source_intake_readonly_shared.py:231:         "use_mode": query_mode,
tools/source_intake_readonly_shared.py:232:         "risk_tier": risk_tier,
tools/source_intake_readonly_shared.py:233:         "intent": case.get("intent", ""),
tools/source_intake_readonly_shared.py:234:         "authority_filter_mode": "bucket_first_before_ranking",
tools/source_intake_readonly_shared.py:235:         "allowed_authority_buckets": allowed_buckets,
tools/source_intake_readonly_shared.py:236:         "support_candidate_authority_buckets": support_candidate_buckets,
tools/source_intake_readonly_shared.py:237:         "allowed_roles": allowed_roles,
tools/source_intake_readonly_shared.py:238:         "retrieval_channels": ["local_lexical"],
tools/source_intake_readonly_shared.py:239:         "disabled_channels": ["dense_vector", "sparse_semantic", "graph_overlay", "rrf_hybrid_fusion", "second_stage_rerank"],
tools/source_intake_readonly_shared.py:240:         "fusion_method": "none_single_local_lexical_channel",
tools/source_intake_readonly_shared.py:241:         "fusion_scope": "within_authority_bucket_only_when_multiple_channels_exist",
tools/source_intake_readonly_shared.py:242:         "rerank_method": "none",
tools/source_intake_readonly_shared.py:243:         "max_hops": 0,
tools/source_intake_readonly_shared.py:244:         "enable_graph": False,
tools/source_intake_readonly_shared.py:245:         "enable_expansion": False,
```

### 原文件第 278–298 行

```text
tools/source_intake_readonly_shared.py:278: def retrieve_with_query_policy(
tools/source_intake_readonly_shared.py:279:     case: dict[str, Any],
tools/source_intake_readonly_shared.py:280:     corpus: list[CorpusDoc],
tools/source_intake_readonly_shared.py:281:     *,
tools/source_intake_readonly_shared.py:282:     top_k: int = 12,
tools/source_intake_readonly_shared.py:283: ) -> tuple[dict[str, Any], dict[str, Any], list[SearchHit]]:
tools/source_intake_readonly_shared.py:284:     policy = query_policy_for_case(case)
tools/source_intake_readonly_shared.py:285:     filtered, receipt = filter_corpus_by_query_policy(corpus, policy)
tools/source_intake_readonly_shared.py:286:     hits = retrieve(str(case["query"]), filtered, top_k=top_k)
tools/source_intake_readonly_shared.py:287:     receipt.update(
tools/source_intake_readonly_shared.py:288:         {
tools/source_intake_readonly_shared.py:289:             "query_policy_id": policy["policy_id"],
tools/source_intake_readonly_shared.py:290:             "retrieval_channels": policy["retrieval_channels"],
tools/source_intake_readonly_shared.py:291:             "fusion_method": policy["fusion_method"],
tools/source_intake_readonly_shared.py:292:             "rerank_method": policy["rerank_method"],
tools/source_intake_readonly_shared.py:293:             "returned_hit_count": len(hits),
tools/source_intake_readonly_shared.py:294:         }
tools/source_intake_readonly_shared.py:295:     )
tools/source_intake_readonly_shared.py:296:     return policy, receipt, hits
tools/source_intake_readonly_shared.py:297: 
tools/source_intake_readonly_shared.py:298: 
```

### 原文件第 358–397 行

```text
tools/source_intake_readonly_shared.py:358: def retrieve(query: str, corpus: list[CorpusDoc], *, top_k: int = 12) -> list[SearchHit]:
tools/source_intake_readonly_shared.py:359:     terms = set(tokenize(query))
tools/source_intake_readonly_shared.py:360:     hits: list[SearchHit] = []
tools/source_intake_readonly_shared.py:361:     for doc in corpus:
tools/source_intake_readonly_shared.py:362:         path_tokens = Counter(tokenize(doc.rel_path))
tools/source_intake_readonly_shared.py:363:         title_tokens = Counter(tokenize(doc.title))
tools/source_intake_readonly_shared.py:364:         heading_tokens = Counter(tokenize(headings(doc.body)))
tools/source_intake_readonly_shared.py:365:         body_tokens = Counter(tokenize(doc.body[:20000]))
tools/source_intake_readonly_shared.py:366:         score = 0.0
tools/source_intake_readonly_shared.py:367:         matched: set[str] = set()
tools/source_intake_readonly_shared.py:368:         for term in terms:
tools/source_intake_readonly_shared.py:369:             path_count = path_tokens.get(term, 0)
tools/source_intake_readonly_shared.py:370:             title_count = title_tokens.get(term, 0)
tools/source_intake_readonly_shared.py:371:             heading_count = heading_tokens.get(term, 0)
tools/source_intake_readonly_shared.py:372:             body_count = body_tokens.get(term, 0)
tools/source_intake_readonly_shared.py:373:             if path_count or title_count or heading_count or body_count:
tools/source_intake_readonly_shared.py:374:                 matched.add(term)
tools/source_intake_readonly_shared.py:375:             score += path_count * 6.0 + title_count * 4.0 + heading_count * 2.5 + min(body_count, 6) * 1.0
tools/source_intake_readonly_shared.py:376:         if score <= 0:
tools/source_intake_readonly_shared.py:377:             continue
tools/source_intake_readonly_shared.py:378:         if doc.record_kind == "source_card" and "source" in terms:
tools/source_intake_readonly_shared.py:379:             score += 1.5
tools/source_intake_readonly_shared.py:380:         if doc.record_kind == "candidate_distillation" and "candidate" in terms:
tools/source_intake_readonly_shared.py:381:             score += 4.0
tools/source_intake_readonly_shared.py:382:         if doc.record_kind == "project_overlay" and "overlay" in terms:
tools/source_intake_readonly_shared.py:383:             score += 4.0
tools/source_intake_readonly_shared.py:384:         selected_by = {
tools/source_intake_readonly_shared.py:385:             "lexical": bool(matched),
tools/source_intake_readonly_shared.py:386:             "semantic": False,
tools/source_intake_readonly_shared.py:387:             "graph": False,
tools/source_intake_readonly_shared.py:388:             "metadata": any(term in tokenize(doc.rel_path + " " + doc.title) for term in terms),
tools/source_intake_readonly_shared.py:389:             "rank": False,
tools/source_intake_readonly_shared.py:390:             "dashboard": False,
tools/source_intake_readonly_shared.py:391:             "legacy_raw_metadata": False,
tools/source_intake_readonly_shared.py:392:         }
tools/source_intake_readonly_shared.py:393:         hits.append(
tools/source_intake_readonly_shared.py:394:             SearchHit(
tools/source_intake_readonly_shared.py:395:                 doc=doc,
tools/source_intake_readonly_shared.py:396:                 score=score,
tools/source_intake_readonly_shared.py:397:                 rank=0,
```

## tools/vaks_supervised_trial_adapter_r1_5.py

- 原路径：`tools/vaks_supervised_trial_adapter_r1_5.py`
- SHA256：`310f7453eddfecbe050b7499995ed23c535c06f23dca42073ee5757127f88e21`
- 原文件总行数：4248
- 读取日期：2026-09-27（Asia/Shanghai）
- 静态判读：离线、确定性 adapter 沙箱。150ms 是代码中的本地 adapter p95 预算，既不是本次测量结果，也不是实际 API 端到端速度承诺；真实 IAM、模型质量、检索质量、生产运行时和生产延迟未证明。

### 原文件第 1–10 行

```text
tools/vaks_supervised_trial_adapter_r1_5.py:1: """R1.5 supervised internal trial adapter preflight for VAKS guarded answers.
tools/vaks_supervised_trial_adapter_r1_5.py:2: 
tools/vaks_supervised_trial_adapter_r1_5.py:3: This sandbox tests the layer above the R1.4 gate: server-built request
tools/vaks_supervised_trial_adapter_r1_5.py:4: envelopes, feature-flag off behavior, answer relevance gating, pre-Guard output
tools/vaks_supervised_trial_adapter_r1_5.py:5: blocking, fallback safety, log redaction, and local latency.
tools/vaks_supervised_trial_adapter_r1_5.py:6: 
tools/vaks_supervised_trial_adapter_r1_5.py:7: It is offline, deterministic, and sandbox-only. It does not call a network, DB,
tools/vaks_supervised_trial_adapter_r1_5.py:8: API, service, LLM, live retrieval system, Obsidian, wiki, raw source writer, or
tools/vaks_supervised_trial_adapter_r1_5.py:9: Truth Core.
tools/vaks_supervised_trial_adapter_r1_5.py:10: """
```

### 原文件第 2872–2890 行

```text
tools/vaks_supervised_trial_adapter_r1_5.py:2872: def run_latency(stack: dict[str, Any], trial_case: dict[str, Any], output_dir: Path, *, count: int) -> dict[str, Any]:
tools/vaks_supervised_trial_adapter_r1_5.py:2873:     elapsed: list[float] = []
tools/vaks_supervised_trial_adapter_r1_5.py:2874:     failures = 0
tools/vaks_supervised_trial_adapter_r1_5.py:2875:     for index in range(count):
tools/vaks_supervised_trial_adapter_r1_5.py:2876:         case = copy.deepcopy(trial_case)
tools/vaks_supervised_trial_adapter_r1_5.py:2877:         case["case_id"] = f"latency-{index:05d}"
tools/vaks_supervised_trial_adapter_r1_5.py:2878:         result = process_adapter_case(stack, case, output_dir)
tools/vaks_supervised_trial_adapter_r1_5.py:2879:         elapsed.append(result["elapsed_ms"])
tools/vaks_supervised_trial_adapter_r1_5.py:2880:         if result.get("final_answer", {}).get("release_state") != "released":
tools/vaks_supervised_trial_adapter_r1_5.py:2881:             failures += 1
tools/vaks_supervised_trial_adapter_r1_5.py:2882:     return {
tools/vaks_supervised_trial_adapter_r1_5.py:2883:         "sample_count": count,
tools/vaks_supervised_trial_adapter_r1_5.py:2884:         "failure_count": failures,
tools/vaks_supervised_trial_adapter_r1_5.py:2885:         "samples_ms": [round(value, 6) for value in elapsed],
tools/vaks_supervised_trial_adapter_r1_5.py:2886:         "avg_ms": round(sum(elapsed) / len(elapsed), 6) if elapsed else 0.0,
tools/vaks_supervised_trial_adapter_r1_5.py:2887:         "p95_ms": round(percentile(elapsed, 95), 6),
tools/vaks_supervised_trial_adapter_r1_5.py:2888:         "p99_ms": round(percentile(elapsed, 99), 6),
tools/vaks_supervised_trial_adapter_r1_5.py:2889:         "budget": "local adapter p95 <= 150ms; not production end-to-end SLO",
tools/vaks_supervised_trial_adapter_r1_5.py:2890:     }
```

### 原文件第 3395–3408 行

```text
tools/vaks_supervised_trial_adapter_r1_5.py:3395:         "not_proven": [
tools/vaks_supervised_trial_adapter_r1_5.py:3396:             "production_runtime",
tools/vaks_supervised_trial_adapter_r1_5.py:3397:             "canary_ready",
tools/vaks_supervised_trial_adapter_r1_5.py:3398:             "enterprise_full_enforce",
tools/vaks_supervised_trial_adapter_r1_5.py:3399:             "real_iam_provider",
tools/vaks_supervised_trial_adapter_r1_5.py:3400:             "real_feature_flag_provider",
tools/vaks_supervised_trial_adapter_r1_5.py:3401:             "live_llm_quality",
tools/vaks_supervised_trial_adapter_r1_5.py:3402:             "live_retrieval_quality",
tools/vaks_supervised_trial_adapter_r1_5.py:3403:             "general_natural_language_semantic_relevance",
tools/vaks_supervised_trial_adapter_r1_5.py:3404:             "production_latency_slo",
tools/vaks_supervised_trial_adapter_r1_5.py:3405:             "reviewed_truth",
tools/vaks_supervised_trial_adapter_r1_5.py:3406:             "promotion",
tools/vaks_supervised_trial_adapter_r1_5.py:3407:             "action_readiness",
tools/vaks_supervised_trial_adapter_r1_5.py:3408:         ],
```

### 原文件第 3551–3554 行

```text
tools/vaks_supervised_trial_adapter_r1_5.py:3551: - The local stress self-test is still an in-process sandbox test. It does not
tools/vaks_supervised_trial_adapter_r1_5.py:3552:   represent real IAM, network, live retrieval, live LLM, or production load.
tools/vaks_supervised_trial_adapter_r1_5.py:3553: - Source import audit is static and import-level. It can catch direct banned
tools/vaks_supervised_trial_adapter_r1_5.py:3554:   imports, but it is not a runtime firewall or production egress control.
```

### 原文件第 3588–3593 行

```text
tools/vaks_supervised_trial_adapter_r1_5.py:3588: - Candidate final, visible claim ids, expected claim ids, and marker groups must
tools/vaks_supervised_trial_adapter_r1_5.py:3589:   be structurally valid before relevance can pass.
tools/vaks_supervised_trial_adapter_r1_5.py:3590: - Claim ids must be unique, trimmed, non-empty strings without control
tools/vaks_supervised_trial_adapter_r1_5.py:3591:   characters.
tools/vaks_supervised_trial_adapter_r1_5.py:3592: - Latency is local adapter path latency, not production end-to-end latency.
tools/vaks_supervised_trial_adapter_r1_5.py:3593: - Review bundle output paths, ZIP paths, SHA256 sidecar paths, and individual
```

## tools/vaks_disposable_vault_trial_r1_6.py

- 原路径：`tools/vaks_disposable_vault_trial_r1_6.py`
- SHA256：`3b9bd5b2f1f8b86e754dc3072d101de32556f4c0f6bfcf3c3bc601bc4746f810`
- 原文件总行数：15048
- 读取日期：2026-09-27（Asia/Shanghai）
- 静态判读：离线、确定性、临时 vault 沙箱；不调用网络、数据库、API、LLM、真实检索或正式 Obsidian vault。

### 原文件第 1–10 行

```text
tools/vaks_disposable_vault_trial_r1_6.py:1: """R1.6 disposable vault trial for VAKS guarded-answer release wiring.
tools/vaks_disposable_vault_trial_r1_6.py:2: 
tools/vaks_disposable_vault_trial_r1_6.py:3: This sandbox tests the last file-output boundary before a real supervised
tools/vaks_disposable_vault_trial_r1_6.py:4: trial: a guarded answer may be written to an Obsidian-like vault only after the
tools/vaks_disposable_vault_trial_r1_6.py:5: adapter sink has committed it, and only inside a disposable temporary vault.
tools/vaks_disposable_vault_trial_r1_6.py:6: 
tools/vaks_disposable_vault_trial_r1_6.py:7: It is offline, deterministic, and sandbox-only. It does not call a network, DB,
tools/vaks_disposable_vault_trial_r1_6.py:8: API, service, LLM, live retrieval system, real Obsidian vault, wiki writer, raw
tools/vaks_disposable_vault_trial_r1_6.py:9: source writer, or Truth Core.
tools/vaks_disposable_vault_trial_r1_6.py:10: """
```

## outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json

- 原路径：`outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json`
- SHA256：`b6c11c362e114924df792e56997a3a37afd2c4cc0ef012c947aaf0d47a200ec2`
- 原文件总行数：254
- 读取日期：2026-09-27（Asia/Shanghai）
- 静态判读：历史结果文件自报 pass；推荐范围仅为单账户、低风险、有监督且不写正式 vault 的试用。not_proven 原文必须与 pass 一起阅读，本次没有重跑或复现该结果。

### 原文件第 1–4 行

```text
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:1: {
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:2:   "append_only_self_test_status": "pass",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:3:   "disposable_vault_trial_recommendation": "eligible_for_one_account_low_risk_supervised_trial_without_formal_vault_write",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:4:   "failed_bundle_cleanup_self_test_status": "pass",
```

### 原文件第 235–254 行

```text
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:235:   "not_proven": [
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:236:     "action_readiness",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:237:     "canary_ready",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:238:     "enterprise_full_enforce",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:239:     "formal_obsidian_vault_write",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:240:     "live_llm_quality",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:241:     "live_retrieval_quality",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:242:     "production_runtime",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:243:     "promotion",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:244:     "real_feature_flag_provider",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:245:     "real_iam_provider",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:246:     "real_obsidian_markdown_rendering",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:247:     "real_obsidian_plugin_runtime",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:248:     "reviewed_truth"
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:249:   ],
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:250:   "positive_gate_pass": true,
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:251:   "reproducibility_self_test_status": "pass",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:252:   "schema_version": "r1.6-disposable-vault-trial",
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:253:   "status": "pass"
outputs/review/vaks-disposable-vault-trial-r1-6-r217-2026-06-26/summary.json:254: }
```

