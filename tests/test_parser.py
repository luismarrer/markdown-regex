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
            '<p><a href="https://example.com" target="_blank" rel="noopener noreferrer">site</a> <img src="image.png" alt="alt"></p>',
        )

    def test_unordered_lists(self):
        self.assertEqual(
            parse_markdown("- one\n- **two**\n- `three`"),
            "<ul><li>one</li><li><strong>two</strong></li><li><code>three</code></li></ul>",
        )

    def test_ordered_lists(self):
        self.assertEqual(
            parse_markdown("1. one\n2. [two](https://example.com)"),
            '<ol><li>one</li><li><a href="https://example.com" target="_blank" rel="noopener noreferrer">two</a></li></ol>',
        )

    def test_links_absolute(self):
        # Absolute link should open in new tab and retain its URL
        expected = '<p>Click <a href="https://google.com" target="_blank" rel="noopener noreferrer">Google</a></p>'
        self.assertEqual(parse_markdown("Click [Google](https://google.com)"), expected)

    def test_links_protocolless(self):
        # Protocol-less link should get https:// prepended and open in new tab
        expected = '<p>Check <a href="https://hola.com" target="_blank" rel="noopener noreferrer">hola</a></p>'
        self.assertEqual(parse_markdown("Check [hola](hola.com)"), expected)
        
        expected_sub = '<p>Check <a href="https://www.luismarrero.me" target="_blank" rel="noopener noreferrer">portfolio</a></p>'
        self.assertEqual(parse_markdown("Check [portfolio](www.luismarrero.me)"), expected_sub)

    def test_links_relative(self):
        # Relative paths and anchors should not get protocol or target="_blank"
        self.assertEqual(parse_markdown("Go to [About](/about)"), '<p>Go to <a href="/about">About</a></p>')
        self.assertEqual(parse_markdown("Go to [Top](#top)"), '<p>Go to <a href="#top">Top</a></p>')
        self.assertEqual(parse_markdown("Download [Resume](resume.pdf)"), '<p>Download <a href="resume.pdf">Resume</a></p>')

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
    def test_link_redos_safety(self):
        import time
        # Testing ReDoS safety for links
        input_str = "([a](" * 500
        start = time.perf_counter()
        parse_markdown(input_str)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 0.05, f"ReDoS vulnerability detected in links: took {elapsed:.4f} seconds")

        # Testing ReDoS safety for images
        input_str_img = "(![a](" * 500
        start = time.perf_counter()
        parse_markdown(input_str_img)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 0.05, f"ReDoS vulnerability detected in images: took {elapsed:.4f} seconds")


if __name__ == "__main__":
    unittest.main()
