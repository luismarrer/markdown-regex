# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An experimental FastAPI service that converts a subset of Markdown to HTML using only regular expressions (no Markdown library). It deliberately does **not** target the full CommonMark/Markdown spec — it's a regex exploration. See the README's "Future Ideas" checklist for which features are implemented vs. planned (lists, images, tables, blockquotes are not yet done).

## Commands

```bash
pip install -r requirements.txt   # install deps (fastapi, uvicorn, pydantic)
uvicorn main:app --reload         # run dev server at http://127.0.0.1:8000
```

- Interactive API docs: http://127.0.0.1:8000/docs
- There is no test suite, linter config, or build step. To exercise the API: `POST /parse` with body `{"text": "# Hello"}` → `{"html": "<h1>Hello</h1>"}`.

## Architecture

Two files:
- `main.py` — FastAPI app, CORS config, and the single `POST /parse` endpoint. It validates input via the `MarkdownInput` Pydantic model and delegates to `parse_markdown`.
- `parser.py` — `parse_markdown(md_text) -> str`, a sequence of `re.sub` passes applied to the whole string.

### Things to know when editing the parser

- **Substitution order is load-bearing.** Headings run `######` → `#` (longest first) so that `###` isn't prematurely consumed by the `#` rule. Bold (`**`) runs before italic (`*`) for the same reason. Preserve this descending/specific-first ordering when adding rules.
- **Inline code is stashed first, then restored last.** `` `code` `` spans are pulled out into placeholders (`\x00N\x00`) before any other rule runs and re-inserted at the end, so Markdown inside code is never parsed. Their contents are escaped individually.
- **Input is HTML-escaped** via `html.escape` after code is stashed, so raw `<`/`>`/`&` in the input cannot inject HTML. The tags the parser emits are added after escaping, so they survive.
- **Headings are anchored** with `^...$` under `re.MULTILINE`, so a `#` mid-line is not treated as a heading.
- **Block wrapping is last (`_wrap_blocks`)**, after inline rules but before code is restored: blank-line-separated blocks become `<p>`, single newlines become `<br>`, and lines already rendered as `<h1>`–`<h6>` are emitted as-is (never wrapped in `<p>`).
- Each rule is an independent regex over the whole string; there is no tokenizer or AST.
- Adding a feature means adding a `re.sub` line in the right position and ticking the box in the README's Future Ideas list.

### CORS

`allow_origins` in `main.py` is an explicit allowlist of `luismarrero.me` origins (plus a local dev origin). Update this list when adding new frontends rather than widening to `*`.
