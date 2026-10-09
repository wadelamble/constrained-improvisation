"""Check section-local footnotes without building or writing the public site."""
from html.parser import HTMLParser
import unittest

from build_site import render_markdown


class Links(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.ids = []
        self.targets = []
        self.references = []
        self.backlinks = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.targets.append(attrs["href"][1:])
            if attrs.get("role") == "doc-noteref":
                self.references.append(attrs)
            if attrs.get("role") == "doc-backlink":
                self.backlinks.append(attrs)


class FootnoteChecks(unittest.TestCase):
    def assert_links(self, markup):
        links = Links(markup)
        self.assertEqual(len(links.ids), len(set(links.ids)))
        self.assertTrue(set(links.targets) <= set(links.ids))
        self.assertTrue(all(link.get("aria-label") for link in links.references + links.backlinks))
        self.assertNotIn("\x00", markup)
        return links

    def test_local_groups_multiline_math_and_repeated_reference(self):
        markup, toc = render_markdown("""### First
Text[^first], again[^first].

[^first]: First paragraph.

    Second paragraph with **weight**.

    ```math
    \\mathcal A[\\Psi] = \\int dt\\,\\mathcal L
    \\delta\\mathcal A = 0.
    ```

### Second
Text[^second] and a later return[^first].

[^second]: Second note.
""")
        self.assertEqual(markup.count('class="footnotes"'), 2)
        self.assertLess(markup.index('class="footnotes"'), markup.index('<h3 id="second">'))
        self.assertGreater(markup.rindex('class="footnotes"'), markup.index('<h3 id="second">'))
        self.assertIn('<p>Second paragraph with <strong>weight</strong>.</p>', markup)
        self.assertIn('<div class="math-block">$$\n\\mathcal A[\\Psi]', markup)
        self.assertIn('\\delta\\mathcal A = 0.\n$$</div>', markup)
        self.assertEqual(toc, [(3, "First", "first"), (3, "Second", "second")])
        links = self.assert_links(markup)
        self.assertEqual(len(links.references), 4)
        self.assertEqual(len(links.backlinks), 4)
        self.assertEqual(links.references[0]["href"], links.references[3]["href"])

    def test_literal_code_math_and_unknown_references(self):
        markup, _ = render_markdown(r"""`[^note]` and ``literal ` [^note]`` and $x[^note]$ and \[^note].

```text
[^fake]: Literal definition.
[^note]
```

```math
[^fake]: Still literal.
```

Real[^note] and unknown[^missing].

[^note]: Actual note.
""")
        links = self.assert_links(markup)
        self.assertEqual(len(links.references), 1)
        self.assertIn('<code>[^note]</code>', markup)
        self.assertIn('<code>literal ` [^note]</code>', markup)
        self.assertIn('$x[^note]$', markup)
        self.assertIn('[^fake]: Literal definition.', markup)
        self.assertIn('unknown[^missing]', markup)

    def test_escaping_and_id_collisions(self):
        markup, _ = render_markdown("""# fn 1
### fnref 1
Reference[^a&<b>\"'].

[^a&<b>\"']: <script>alert("unsafe")</script> & ordinary text.
""")
        links = self.assert_links(markup)
        self.assertEqual(len(links.references), 1)
        self.assertIn('&lt;script&gt;', markup)
        self.assertNotIn('<script>', markup)
        self.assertNotIn('id="a&', markup)

    def test_definitions_before_references_and_first_reference_numbering(self):
        markup, _ = render_markdown("""[^first]: Defined first.
[^second]: Defined second.

Second[^second], first[^first].
""")
        links = self.assert_links(markup)
        self.assertEqual(links.references[0]["aria-label"], "Footnote 1")
        self.assertEqual(len(links.backlinks), 2)
        self.assertIn('<li id="fn-2" value="2"><p>Defined first.', markup)

    def test_existing_markdown(self):
        markup, toc = render_markdown("## Title\n\nPlain **bold**, *italic*, `code`, $x$ and [link](target).")
        self.assertEqual(markup, '<h2 id="title">Title</h2>\n<p>Plain <strong>bold</strong>, <em>italic</em>, <code>code</code>, $x$ and <a href="target">link</a>.</p>')
        self.assertEqual(toc, [(2, "Title", "title")])

    def test_shared_links_in_sidebars_and_details(self):
        markup, _ = render_markdown("""Text[^note].

::: sidebar
Sidebar[^note].
:::

::: details More
Details[^note].
:::

[^note]: Shared note.
""")
        links = self.assert_links(markup)
        self.assertEqual(len(links.references), 3)
        self.assertEqual(len(links.backlinks), 3)


if __name__ == "__main__":
    unittest.main()
