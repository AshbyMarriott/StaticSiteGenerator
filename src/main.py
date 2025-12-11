from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_blocks import markdown_to_blocks,block_to_block_type, strip_ordered_list_prefix, BlockType, strip_paragraph_newlines, strip_codeblock_backticks, extract_heading_level
from markdown_inline import text_to_textnodes

def main():
    """Main entry point for the static site generator application.
    
    Currently serves as a simple test/demo function that creates a TextNode
    and prints it. This function is executed when the script is run directly.
    """
    aNode = TextNode('some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(aNode)

def text_node_to_html_node(text_node):
    """Convert a TextNode to its corresponding HTML node representation.
    
    Maps a TextNode to an appropriate HTML LeafNode based on its text type.
    Each text type corresponds to a specific HTML tag or structure.
    
    Args:
        text_node (TextNode): The TextNode to convert to HTML. Must have a valid
            text_type from the TextType enum.
    
    Returns:
        LeafNode: An HTML node representing the text node:
            - TEXT: LeafNode with no tag (plain text)
            - BOLD: LeafNode with 'b' tag
            - ITALIC: LeafNode with 'i' tag
            - CODE: LeafNode with 'code' tag
            - LINK: LeafNode with 'a' tag and href property
            - IMAGE: LeafNode with 'img' tag, src and alt properties
    
    Raises:
        Exception: If the text_node.text_type doesn't match any allowed TextType
            values.
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None,value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag='i', value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag='code', value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag='a', value=text_node.text, props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag='img', value='', props = {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("TextType doesn't match allowed values")

def markdown_to_html_node(markdown):
    """Convert markdown text to an HTML node structure.
    
    Parses markdown text into blocks and converts each block type to its
    corresponding HTML representation. Supports headings, paragraphs, code blocks,
    blockquotes, and ordered/unordered lists.
    
    Args:
        markdown (str): The markdown text to convert to HTML.
    
    Returns:
        ParentNode: A div element containing all converted HTML blocks as children.
            Each block is converted according to its type:
            - HEADING: h1-h6 elements
            - PARAGRAPH: p elements
            - CODE: pre > code elements
            - QUOTE: blockquote elements
            - UNORDERED_LIST: ul > li elements
            - ORDERED_LIST: ol > li elements
    
    Raises:
        Exception: If an unsupported block type is encountered.
    """
    blocks = markdown_to_blocks(markdown)
    html_parent_node = ParentNode(tag="div", children=[])
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                heading_level = extract_heading_level(block)
                heading_text = block.strip('# ')
                heading_node = ParentNode(tag=f'h{heading_level}', children=text_to_children(heading_text))
                html_parent_node.children.append(heading_node)
            case BlockType.QUOTE:
                quote_text = block.strip('> ')
                quote_node = ParentNode(tag='blockquote', children = text_to_children(quote_text))
                html_parent_node.children.append(quote_node)
            case BlockType.UNORDERED_LIST:
                list_items = block.split('\n')
                list_text = [l.strip('- ') for l in list_items]
                children = [ParentNode(tag='li', children=text_to_children(text)) for text in list_text]
                list_node = ParentNode(tag='ul', children=children)
                html_parent_node.children.append(list_node)
            case BlockType.ORDERED_LIST:
                list_items = block.split('\n')
                list_text = strip_ordered_list_prefix(list_items)
                children = [ParentNode(tag='li', children=text_to_children(text)) for text in list_text]
                list_node = ParentNode(tag='ol', children=children)
                html_parent_node.children.append(list_node)
            case BlockType.CODE:
                code_text = strip_codeblock_backticks(block)
                code_text_node = TextNode(code_text, TextType.TEXT)
                code_node = ParentNode(tag='code', children =[text_node_to_html_node(code_text_node)])
                pre_node = ParentNode(tag='pre', children=[code_node])
                html_parent_node.children.append(pre_node)
            case BlockType.PARAGRAPH:
                paragraph_text = strip_paragraph_newlines(block)
                text_nodes = text_to_textnodes(paragraph_text)
                children = [text_node_to_html_node(text_node) for text_node in text_nodes]
                paragraph_node = ParentNode(tag='p', children=children)
                html_parent_node.children.append(paragraph_node)
            case _:
                raise Exception(f"Block type {block_type} not supported")
    return html_parent_node

def text_to_children(text):
    """Convert text with inline markdown to a list of HTML nodes.
    
    Parses text containing inline markdown syntax (bold, italic, code, links, images)
    and converts it into a list of HTML nodes. The text is first parsed into TextNodes
    and then each TextNode is converted to its corresponding HTML representation.
    
    Args:
        text (str): The text string that may contain inline markdown syntax.
    
    Returns:
        list[HTMLNode]: A list of HTML nodes (LeafNode objects) representing the
            parsed text. Each node corresponds to a segment of the text with its
            appropriate HTML tag (e.g., <b> for bold, <i> for italic, <code> for code,
            <a> for links, <img> for images).
    """
    textnodes = text_to_textnodes(text)
    children = []
    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))
    return children

        
if __name__ == "__main__":
    main()