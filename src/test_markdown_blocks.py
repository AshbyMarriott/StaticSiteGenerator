import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        """Test provided by Boot.dev lesson"""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_excessive_newlines1(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading1(self):
        block = """# This is a heading block
This is the heading continued on the next line"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    
    def test_block_to_block_type_heading2(self):
        block = """## This is a heading block
This is the heading continued on the next line"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading6(self):
        block = """###### This is a heading block
This is the heading continued on the next line"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_paragraph1(self):
        block = """ This is a paragraph block
This is the heading continued on the next line"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph2(self):
        block = """1. This is a paragraph block
2. That wants to be an ordered list block
3 . but due to a typo is not"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list1(self):
        block = """1. This is a block
2. That wants to be an ordered list block
3. and is!"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
