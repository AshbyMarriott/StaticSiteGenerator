import unittest

from ssg_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

    def test_split_images(self):
        """Test provided by Boot.dev course Ch3L5"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_nodes_images_no_opening_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_images_no_dividing_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_nodes_images_only_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )
    
    def test_split_nodes_images_no_link_text(self):
        node = TextNode(
            "![](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_nodes_images_no_url_text(self):
        node = TextNode(
            "![image]()![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, ""),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://github.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://github.com"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_no_link(self):
        node = TextNode(
            "This is text with no links!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links!", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        """Example io provided by Boot.dev course"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertEqual(
            textnodes,
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
            ]
        )
    
    def test_text_to_textnodes_repeated_image(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and another ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        textnodes = text_to_textnodes(text)
        self.assertEqual(
            textnodes,
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

if __name__ == "__main__":
    unittest.main()