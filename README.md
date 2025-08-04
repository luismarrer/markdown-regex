# Markdown to HTML Converter API

This is a simple and experimental API that converts Markdown text into HTML using regular expressions.  
Built with [FastAPI](https://fastapi.tiangolo.com/) and configured with CORS support for local development and deployment.

> ⚠️ **Note:** This project is a regex-based exploration of Markdown parsing. It does **not** aim to support the full Markdown specification.

---

## 🚀 Endpoints

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

## 🛠️ Tech Stack

- Python
- FastAPI
- Regex
  
## 🧪 Future Ideas

[ ] Support for more Markdown features (lists, code blocks, bold/italic, etc.)

## 📜 License

MIT License
