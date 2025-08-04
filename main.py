from fastapi import FastAPI, Request
from pydantic import BaseModel
from parser import parse_markdown

app = FastAPI()

class MarkdownInput(BaseModel):
    text: str

@app.post("/parse")
def convert_md(md_input: MarkdownInput):
    html = parse_markdown(md_input.text)
    return {"html": html}