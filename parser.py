import html
import re


BLOCK_TAG_RE = re.compile(r"^<(?:h[1-6]|ul|ol|blockquote|table)\b")


def _split_cells(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]

    return [cell.strip() for cell in line.split("|")]


def _is_table_separator(line: str) -> bool:
    cells = _split_cells(line)
    if not cells:
        return False

    return all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _render_tables(text: str) -> str:
    rendered_blocks: list[str] = []

    for block in re.split(r"\n\s*\n", text):
        lines = [line.strip() for line in block.split("\n") if line.strip()]

        if len(lines) >= 2 and "|" in lines[0] and _is_table_separator(lines[1]):
            headers = _split_cells(lines[0])
            rows = [_split_cells(line) for line in lines[2:] if "|" in line]

            header_html = "".join(f"<th>{cell}</th>" for cell in headers)
            body_html = "".join(
                "<tr>"
                + "".join(f"<td>{row[index] if index < len(row) else ''}</td>" for index in range(len(headers)))
                + "</tr>"
                for row in rows
            )

            rendered_blocks.append(
                f"<table><thead><tr>{header_html}</tr></thead><tbody>{body_html}</tbody></table>"
            )
        else:
            rendered_blocks.append(block)

    return "\n\n".join(rendered_blocks)


def _render_blockquotes(text: str) -> str:
    def render(match: re.Match) -> str:
        lines = [
            re.sub(r"^&gt;\s?", "", line).strip()
            for line in match.group(0).strip().split("\n")
        ]
        content = "<br>".join(line for line in lines if line)
        return f"<blockquote><p>{content}</p></blockquote>"

    return re.sub(r"(?m)(?:^&gt;\s?.+(?:\n|$))+", render, text)


def _render_lists(text: str) -> str:
    def render_unordered(match: re.Match) -> str:
        items = re.findall(r"(?m)^[-+*]\s+(.+)$", match.group(0))
        return "<ul>" + "".join(f"<li>{item.strip()}</li>" for item in items) + "</ul>"

    def render_ordered(match: re.Match) -> str:
        items = re.findall(r"(?m)^\d+\.\s+(.+)$", match.group(0))
        return "<ol>" + "".join(f"<li>{item.strip()}</li>" for item in items) + "</ol>"

    text = re.sub(r"(?m)(?:^[-+*]\s+.+(?:\n|$))+", render_unordered, text)
    return re.sub(r"(?m)(?:^\d+\.\s+.+(?:\n|$))+", render_ordered, text)


def _wrap_blocks(text: str) -> str:
    """Group lines into <p> blocks (split on blank lines), joining single
    newlines with <br>. Already-rendered block tags are passed through."""
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
            if BLOCK_TAG_RE.match(line):
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

    # 5. Images before links, so the link rule does not consume image syntax.
    text = re.sub(r"!\[([^\]]*?)\]\(([^)]*?)\)", r'<img src="\2" alt="\1">', text)

    # 6. Links: [text](url)
    def replace_link(match):
        link_text = match.group(1)
        url = match.group(2).strip()
        
        # Check if it already has a protocol, or is relative/anchor
        if re.match(r'^(https?://|mailto:|tel:|javascript:|/|#|\.\.?/)', url, re.IGNORECASE):
            fixed_url = url
        else:
            first_part = url.split('/')[0]
            if '.' in first_part:
                file_exts = {'.html', '.htm', '.php', '.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.json', '.md', '.txt', '.xml'}
                if any(first_part.lower().endswith(ext) for ext in file_exts):
                    fixed_url = url
                elif re.match(r'^[a-zA-Z0-9][-a-zA-Z0-9.]*\.[a-zA-Z]{2,}$', first_part):
                    fixed_url = f"https://{url}"
                else:
                    fixed_url = url
            else:
                fixed_url = url
                
        is_external = fixed_url.startswith(('http://', 'https://'))
        if is_external:
            return f'<a href="{fixed_url}" target="_blank" rel="noopener noreferrer">{link_text}</a>'
        return f'<a href="{fixed_url}">{link_text}</a>'

    text = re.sub(r"\[([^\]]*?)\]\(([^)]*?)\)", replace_link, text)

    # 7. Block-level structures. These run after inline formatting so list
    #    items, table cells, and blockquotes can contain simple inline markup.
    text = _render_tables(text)
    text = _render_blockquotes(text)
    text = _render_lists(text)

    # 8. Wrap blocks: paragraphs (blank-line separated) and <br> for single
    #    newlines. Rendered block tags are emitted as-is, never wrapped in <p>.
    text = _wrap_blocks(text)

    # 9. Restore the stashed code spans.
    text = re.sub(
        r"\x00(\d+)\x00",
        lambda m: f"<code>{code_spans[int(m.group(1))]}</code>",
        text,
    )

    return text
