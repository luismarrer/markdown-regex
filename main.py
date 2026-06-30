from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from parser import parse_markdown

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://luismarrero-me.localhost:1355", "https://luismarrero.me", "https://www.luismarrero.me"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

class MarkdownInput(BaseModel):
    text: str = Field(..., max_length=100_000)

@app.post("/parse")
def convert_md(md_input: MarkdownInput):
    html = parse_markdown(md_input.text)
    return {"html": html}

