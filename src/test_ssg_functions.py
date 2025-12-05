import unittest

from ssg_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestSSGFunctions(unittest.TestCase):
    def test_split_nodes_code1(self):
        node = TextNode("Here is a `code block` in a string", TextType.TEXT)
        node_split = split_nodes_delimiter([node],'`', TextType.CODE)
        node_code_split = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in a string", TextType.TEXT)
        ]
        
        self.assertEqual(node_split, node_code_split)

    def test_split_nodes_code2(self):
        node = TextNode("Here is a `code block` in a `string", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], '`', TextType.CODE)
    
    def test_split_nodes_code3(self):
        node = TextNode("Here is a `code block` in a string`", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], '`', TextType.CODE)
    
    def test_split_nodes_code4(self):
        node = TextNode("Here is a `code block` in a `string`", TextType.TEXT)
        node_split = split_nodes_delimiter([node],'`', TextType.CODE)
        node_code_split = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in a ", TextType.TEXT),
            TextNode("string", TextType.CODE),
            TextNode("", TextType.TEXT)
        ]
        
        self.assertEqual(node_split, node_code_split)
    
    def test_split_nodes_code5(self):
        node = TextNode("Here is a `code block` in a `string```", TextType.TEXT)
        node_split = split_nodes_delimiter([node],'`', TextType.CODE)
        node_code_split = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in a ", TextType.TEXT),
            TextNode("string", TextType.CODE),
            TextNode("", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode("", TextType.TEXT)
        ]
        
        self.assertEqual(node_split, node_code_split)
    
    def test_split_nodes_code6(self):
        node = TextNode("Here is a `code block` in a `string``", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], '`', TextType.CODE)
    
    def test_split_nodes_bold1(self):
        node = TextNode("How about something **bold**?", TextType.TEXT)
        node_split = split_nodes_delimiter([node], '**', TextType.BOLD)
        node_bold_split = [
            TextNode("How about something ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("?", TextType.TEXT)
        ]
        self.assertEqual(node_split, node_bold_split)
    
    def test_split_nodes_italic1(self):
        node = TextNode("How about something _italic_?", TextType.TEXT)
        node_split = split_nodes_delimiter([node], '_', TextType.ITALIC)
        node_italic_split = [
            TextNode("How about something ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("?", TextType.TEXT)
        ]
        self.assertEqual(node_split, node_italic_split)
    
    def test_split_nodes_italic_no_delim(self):
        node = TextNode("No delimiters here", TextType.TEXT)
        node_split = split_nodes_delimiter([node], '_', TextType.ITALIC)
        node_italic_split = [
            TextNode("No delimiters here", TextType.TEXT)
        ]
        self.assertEqual(node_split, node_italic_split)
    
    def test_split_nodes_only_delim(self):
        node = TextNode("**bold**", TextType.TEXT)
        node_split = split_nodes_delimiter([node], '**', TextType.BOLD)
        node_bold_split = [
            TextNode("", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT)
        ]
        self.assertEqual(node_split, node_bold_split)

    def test_extract_markdown_images1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        correct_matches = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(matches, correct_matches)

    def test_extract_markdown_links1(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        correct_matches = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(matches, correct_matches)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()