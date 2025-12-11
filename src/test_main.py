import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node, markdown_to_html_node
from htmlnode import *

class TestMain(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_codeblock2(self):
        md = """
```This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_codeblock3(self):
        md = """
```This is text that _should_ remain
the **same** even with inline stuff```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
    
    def test_unordered_list(self):
        md = """
- Here is a list item
- Here is another list item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Here is a list item</li><li>Here is another list item</li></ul></div>"
        )
    
    def test_ordered_list(self):
        md = """
1. Here is a list item
2. Here is another list item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Here is a list item</li><li>Here is another list item</li></ol></div>"
        )
    
    def test_heading(self):
        md = """
# This is a h1 heading

## This is a h2 heading

###### This is a h6 heading"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a h1 heading</h1><h2>This is a h2 heading</h2><h6>This is a h6 heading</h6></div>"
        )
        
    def test_quote(self):
        md = """>This is a quote

> This is another quote with `code` in **it**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote><blockquote>This is another quote with <code>code</code> in <b>it</b></blockquote></div>"
        )
    
        
if __name__ == "__main__":
    unittest.main()