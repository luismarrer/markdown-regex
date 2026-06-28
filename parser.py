import html
import re


def _wrap_blocks(text: str) -> str:
    """Group lines into <p> blocks (split on blank lines), joining single
    newlines with <br>. Heading lines are passed through untouched."""
    rendered: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        if not block.strip():
            continue

        paragraph: list[str] = []

        def flush() -> None:
            if paragraph:
                rendered.append("<p>" + "<br>".join(paragraph) + "</p>")
                paragraph.clear()

        for line in block.split("\n"):
            line = line.strip()
            if not line:
                continue
            if re.match(r"<h[1-6]>", line):
                flush()
                rendered.append(line)
            else:
                paragraph.append(line)
        flush()

    return "\n".join(rendered)


def parse_markdown(md_text: str) -> str:
    # 1. Stash inline code spans so their contents are never parsed as Markdown.
    code_spans: list[str] = []

    def _stash_code(match: re.Match) -> str:
        code_spans.append(html.escape(match.group(1)))
        return f"\x00{len(code_spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", _stash_code, md_text)

    # 2. Escape the rest so raw HTML in the input can't be injected.
    text = html.escape(text)

    # 3. Headings: longest marker first, anchored to the start of a line.
    for level in range(6, 0, -1):
        text = re.sub(
            rf"^{'#' * level} (.*)$",
            rf"<h{level}>\1</h{level}>",
            text,
            flags=re.MULTILINE,
        )

    # 4. Bold before italic, so ** isn't consumed by the * rule.
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)

    # 5. Links: [text](url)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', text)

    # 6. Wrap blocks: paragraphs (blank-line separated) and <br> for single
    #    newlines. Heading lines are emitted as-is, never wrapped in <p>.
    text = _wrap_blocks(text)

    # 7. Restore the stashed code spans.
    text = re.sub(
        r"\x00(\d+)\x00",
        lambda m: f"<code>{code_spans[int(m.group(1))]}</code>",
        text,
    )

    return text
