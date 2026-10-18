---
record_kind: source_card
status: raw
knowledge_status: raw
processing_tier: medium
source_id: flexnote-docs-inspected-pages-2026-06-13
source_ref: raw/articles/2026-06-13-flexnote-docs-source.md
raw_location: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
title: FlexNote documentation inspected pages and extraction notes
why_saved: Preserve inspected source anchors and extraction notes for the FlexNote documentation source card.
captured_at: 2026-06-13
captured_by: Codex
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - flexnote
  - retained-source-notes
  - inspected-pages
---

# FlexNote Docs: Inspected Pages

This file preserves the inspected source anchors and extraction notes for the FlexNote documentation distillation. It is raw provenance support only, not reviewed knowledge.

## Pages Inspected

| Page | URL | Key anchors inspected |
|---|---|---|
| Introduction | https://wiki.myflexnote.com/docs/intro | what FlexNote is; core features; local-first; tags; Markdown links; cloud sync; video/PDF/web annotation; use cases |
| 中文简介 | https://wiki.myflexnote.com/zh/docs/intro | Chinese wording for the same feature model |
| Tutorial category | https://wiki.myflexnote.com/docs/category/tutorial---basics | page map for Card, Whiteboard, Tags, Highlighting, Tabs, Journal, Bidirectional Links, Shortcuts |
| Card System | https://wiki.myflexnote.com/docs/tutorial-basics/card | card as fundamental unit; multiple card types; global uniqueness; reuse; tag database |
| Whiteboard | https://wiki.myflexnote.com/docs/tutorial-basics/whiteboard | infinite canvas; nesting; arrows; thumbnails; auto layout; export |
| Tags | https://wiki.myflexnote.com/docs/tutorial-basics/tag | tags as extensible database with custom fields, relation fields, views, filtering |
| Highlighting | https://wiki.myflexnote.com/docs/tutorial-basics/Highlight | PDF/video highlights automatically become cards with source/location metadata |
| Tabs | https://wiki.myflexnote.com/docs/tutorial-basics/tab | auto-created tabs, pinning, nested folders, task/workspace switching |
| Journal | https://wiki.myflexnote.com/docs/tutorial-basics/daily-notes | daily card, date navigation, cross-module embedding, daily entry point |
| Bidirectional Links | https://wiki.myflexnote.com/docs/tutorial-basics/reference | `@` references, backlinks, visual arrows, info panel |
| Keyboard Shortcuts | https://wiki.myflexnote.com/docs/tutorial-basics/shortcuts | shortcut surface across search, card creation, sidebar, journal, whiteboard, editing |
| Import & Export | https://wiki.myflexnote.com/docs/export | md/txt/html import; md/pdf export; batch import/export; HTML cleaning claim |
| Third-Party Cloud Sync | https://wiki.myflexnote.com/docs/cloud-sync | local-first sync via S3/WebDAV/OneDrive/Baidu; incremental sync; hashes/timestamps; conflict advice |
| FAQ | https://wiki.myflexnote.com/docs/faq | Windows/macOS support; local-first security; mobile not yet; individual use; migration |

## Extracted Source Facts

- FlexNote presents itself as a local-first visual note-taking tool for creators and deep thinkers.
- Its feature cluster is: infinite canvas, Markdown editing, mind maps, bidirectional links, tag database, video/PDF/web annotations.
- The card is the main information atom. Cards can be text, PDF, video, web clip, image, audio, mind map, attachment, PDF highlight, or video annotation.
- Cards are globally unique and reusable: one card can appear in multiple whiteboards, and edits sync to all references.
- Whiteboards are visual workspaces. They can contain cards, nested cards, connections/arrows, nested whiteboards, thumbnails, navigation, auto layout, and export.
- Tags are described as an extensible database, not merely labels. Tags can have custom fields, relation fields, filters, and table/board/list views.
- PDF and video highlights can automatically generate cards, including source and location metadata such as page or timestamp.
- The journal is a date-based daily entry point; each daily entry is a card and can reference/embed other cards, tasks, highlights, and annotations.
- Bidirectional links are made through `@` mentions and visual arrows; cards expose incoming/outgoing links and whiteboard associations.
- FlexNote is local-first by default and supports optional third-party cloud sync through services including S3, WebDAV, OneDrive, and Baidu Netdisk.
- Sync is described as incremental and based on changed files; the docs warn users to edit on one primary device to avoid conflicts.
- Import/export supports Markdown and other common formats, with PDF export marked beta.

## Source-Window Limitations

- This is documentation-level inspection, not source-code inspection.
- The app was not run.
- Claims about sync correctness, HTML cleaning, and local storage were not independently tested.
- No repository, schema, or implementation internals were inspected in this run.
