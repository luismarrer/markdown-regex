# Repository Guidelines

## Project Structure

This is a small FastAPI Markdown-to-HTML parser experiment. `main.py` owns the API app, CORS configuration, and `POST /parse` endpoint. `parser.py` owns `parse_markdown(md_text) -> str` and the regex-based parsing pipeline. Keep the parser intentionally lightweight; do not add a Markdown library.

## Development Commands

Use Python 3.12 for local work with the pinned dependencies. The codebase expects Python 3.9+ syntax, and the current pinned dependencies are compatible through Python 3.12.

- `uv venv --python 3.12 .venv`: create a compatible local virtualenv.
- `uv pip install --python .venv/bin/python -r requirements.txt`: install dependencies.
- `.venv/bin/python -m uvicorn main:app --reload`: run the API at `http://127.0.0.1:8000`.
- `.venv/bin/python -m unittest discover -s tests`: run parser tests.

Exercise the API with:

```bash
curl -X POST http://127.0.0.1:8000/parse \
  -H "Content-Type: application/json" \
  -d '{"text":"# Hello"}'
```

## Parser Guidelines

This repo is a regex exploration, not a CommonMark implementation. Preserve the current safety model: stash inline code spans first, escape raw input with `html.escape`, emit parser-owned HTML tags after escaping, and restore code spans last.

Substitution order matters. Keep more specific rules before broad ones, such as images before links and bold before italic. Block-level helpers should run after inline formatting so list items, table cells, and blockquotes can contain simple inline markup.

## Testing Guidelines

For parser changes, run `.venv/bin/python -m unittest discover -s tests` and at least one `curl` request against `POST /parse`. Cover headings, inline code, links/images, lists, tables, blockquotes, paragraph wrapping, and raw HTML escaping when behavior changes.

## Security

Do not widen CORS to `*` unless explicitly requested. Do not allow raw input HTML to pass through unescaped. URL-bearing syntax such as links and images is emitted by the parser after input escaping; be careful when changing those regexes.
