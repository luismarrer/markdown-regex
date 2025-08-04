from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from parser import parse_markdown

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321", "https://luismarrero.me"],
    allow_methods=["POST"],
    allow_headers=["*"])

class MarkdownInput(BaseModel):
    text: str

@app.post("/parse")
def convert_md(md_input: MarkdownInput):
    html = parse_markdown(md_input.text)
    return {"html": html}