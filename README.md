# Markdown to HTML Converter API

A simple and experimental API that converts Markdown text into HTML using **regular expressions** — no Markdown library involved.
Built with [FastAPI](https://fastapi.tiangolo.com/) and configured with CORS support for local development and deployment.

> ⚠️ **Note:** This project is a regex-based exploration of Markdown parsing. It does **not** aim to support the full Markdown specification. Raw HTML in the input is escaped, and inline code spans are left untouched.

---

## 🚀 Getting Started

### Requirements

- Python 3.9–3.12 with the pinned dependencies in `requirements.txt`

### Installation

```bash
git clone https://github.com/luismarrer/markdown-regex.git
cd markdown-regex
pip install -r requirements.txt
```

With `uv`, you can create a compatible local environment with:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

### Running the server

```bash
.venv/bin/python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

### Running tests

```bash
.venv/bin/python -m unittest discover -s tests
```

---

## 📡 Endpoints

### `POST /parse`

Converts the provided Markdown text into its corresponding HTML representation.

#### 🔸 Request Body

```json
{
  "text": "# Hello World"
}
```

#### 🔸 Response Body

```json
{
  "html": "<h1>Hello World</h1>"
}
```

#### 🔸 Example

```bash
curl -X POST http://127.0.0.1:8000/parse \
  -H "Content-Type: application/json" \
  -d '{"text": "# Hello **World** with a [link](https://luismarrero.me)"}'
```

```json
{
  "html": "<h1>Hello <strong>World</strong> with a <a href=\"https://luismarrero.me\" target=\"_blank\" rel=\"noopener noreferrer\">link</a></h1>"
}
```

---

## ✅ Supported Syntax

| Markdown                | HTML                                  |
| ----------------------- | ------------------------------------- |
| `# … ###### `           | `<h1>` … `<h6>`                        |
| `**text**`              | `<strong>text</strong>`               |
| `*text*` / `_text_`     | `<em>text</em>`                        |
| `` `code` ``            | `<code>code</code>`                   |
| `[text](url)`           | `<a href="url">text</a>` (external links open in a new tab; protocol-less domains auto-prefixed with `https://`) |
| `![alt](url)`           | `<img src="url" alt="alt">`           |
| `- item` / `* item`     | `<ul><li>item</li></ul>`              |
| `1. item`               | `<ol><li>item</li></ol>`              |
| `> quote`               | `<blockquote><p>quote</p></blockquote>` |
| pipe tables             | `<table>` with `<thead>` and `<tbody>` |
| blank line              | new `<p>` paragraph                    |
| single newline          | `<br>` inside a paragraph              |

---

## 🛠️ Tech Stack

- Python
- FastAPI
- Regex

## 💻 Development & Testing

### Running the API

Start the development server:
```bash
uvicorn main:app --reload
```

### Running Tests

To run the test suite:
```bash
python -m pytest tests/ -v
```

## 📜 License

[MIT License](LICENSE)
