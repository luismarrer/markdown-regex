import unittest

from parser import parse_markdown


class ParseMarkdownTest(unittest.TestCase):
    def test_headings_and_paragraphs(self):
        self.assertEqual(
            parse_markdown("# Title\n\nPlain text"),
            "<h1>Title</h1>\n<p>Plain text</p>",
        )

    def test_inline_markup_and_code(self):
        self.assertEqual(
            parse_markdown("**bold** *em* _em_ `**code**`"),
            "<p><strong>bold</strong> <em>em</em> <em>em</em> <code>**code**</code></p>",
        )

    def test_links_and_images(self):
        self.assertEqual(
            parse_markdown("[site](https://example.com) ![alt](image.png)"),
            '<p><a href="https://example.com">site</a> <img src="image.png" alt="alt"></p>',
        )

    def test_unordered_lists(self):
        self.assertEqual(
            parse_markdown("- one\n- **two**\n- `three`"),
            "<ul><li>one</li><li><strong>two</strong></li><li><code>three</code></li></ul>",
        )

    def test_ordered_lists(self):
        self.assertEqual(
            parse_markdown("1. one\n2. [two](https://example.com)"),
            '<ol><li>one</li><li><a href="https://example.com">two</a></li></ol>',
        )

    def test_blockquotes(self):
        self.assertEqual(
            parse_markdown("> hello\n> **world**"),
            "<blockquote><p>hello<br><strong>world</strong></p></blockquote>",
        )

    def test_tables(self):
        self.assertEqual(
            parse_markdown("| Name | Value |\n| --- | ---: |\n| One | **Two** |"),
            "<table><thead><tr><th>Name</th><th>Value</th></tr></thead><tbody><tr><td>One</td><td><strong>Two</strong></td></tr></tbody></table>",
        )

    def test_raw_html_is_escaped(self):
        self.assertEqual(
            parse_markdown("<script>alert(1)</script>"),
            "<p>&lt;script&gt;alert(1)&lt;/script&gt;</p>",
        )


if __name__ == "__main__":
    unittest.main()
