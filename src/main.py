from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_blocks import markdown_to_blocks,block_to_block_type, strip_ordered_list_prefix, BlockType, strip_paragraph_newlines, strip_codeblock_backticks, extract_heading_level, extract_title
from markdown_inline import text_to_textnodes
import os
import shutil
import sys

def main():
    """Main entry point for the static site generator application.
    """
    basepath = '/'
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_directory('static', 'docs')
    generate_pages_recursive('content', basepath, 'template.html', 'docs')

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
                quote_lines = block.split('\n')
                quote_text = [l.strip('> ') for l in quote_lines]
                quote_text = '\n'.join(quote_text)
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

def copy_directory(source_dir, target_dir):
    """Recursively copy a directory and all its contents to a target location.
    
    Copies all files and subdirectories from the source directory to the target
    directory. If the target directory already exists, it is removed first before
    copying. The function recursively handles nested directory structures.
    
    Args:
        source_dir (str): The path to the source directory to copy from.
        target_dir (str): The path to the target directory to copy to. This directory
            will be created if it doesn't exist, or removed and recreated if it does.
    
    Note:
        If the source directory doesn't exist, the function will still create the
        target directory but it will be empty.
    """
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)
    if os.path.exists(source_dir):
        dir_list = os.listdir(source_dir)
        for file in dir_list:
            if os.path.isfile(os.path.join(source_dir, file)):
                shutil.copy(os.path.join(source_dir, file), os.path.join(target_dir, file))
            elif os.path.isdir(os.path.join(source_dir, file)):
                os.mkdir(os.path.join(target_dir, file))
                copy_directory(os.path.join(source_dir, file), os.path.join(target_dir, file))

def generate_page(from_path, basepath, template_path, dest_path):
    """Generate an HTML page from markdown content using a template.
    
    Reads markdown content from a source file, converts it to HTML, and injects
    it into an HTML template. The template should contain placeholders '{{ Title }}'
    and '{{ Content }}' which will be replaced with the extracted title and
    converted HTML content respectively. Absolute paths in href and src attributes
    are adjusted to use the provided basepath.
    
    Args:
        from_path (str): The file path to the markdown source file to convert.
        basepath (str): The base path prefix to use for absolute URLs in the
            generated HTML. All occurrences of 'href="/' and 'src="/' in the
            template will be replaced with 'href="{basepath}' and 'src="{basepath}'
            respectively.
        template_path (str): The file path to the HTML template file containing
            '{{ Title }}' and '{{ Content }}' placeholders.
        dest_path (str): The file path where the generated HTML page should be
            written. The parent directory will be created if it doesn't exist.
    
    Note:
        The function prints a message indicating which files are being used for
        generation. The title is extracted from the first heading in the markdown
        content.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    html_string = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)
    template = template.replace('{{ Title }}', page_title)
    template = template.replace('{{ Content }}', html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    with open(dest_path, 'w') as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, basepath, template_path, dest_dir_path):
    """Recursively generate HTML pages from markdown files in a directory.
    
    Traverses a directory structure containing markdown files and generates
    corresponding HTML pages using a template. Markdown files (`.md`) are
    converted to HTML files (`.html`) in the destination directory, preserving
    the directory structure. The basepath is passed to each page generation
    to ensure consistent URL path handling.
    
    Args:
        dir_path_content (str): The source directory path containing markdown
            files and subdirectories to process.
        basepath (str): The base path prefix to use for absolute URLs in the
            generated HTML pages. This is passed to `generate_page()` for each
            markdown file processed.
        template_path (str): The file path to the HTML template file containing
            '{{ Title }}' and '{{ Content }}' placeholders.
        dest_dir_path (str): The destination directory path where generated HTML
            files will be written. The directory structure will be preserved.
    
    Raises:
        ValueError: If `dir_path_content` is not a valid directory path.
    """
    if not os.path.isdir(dir_path_content):
        raise ValueError(f"Directory {dir_path_content} does not exist")
    if not os.path.isdir(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)
    for file in os.listdir(dir_path_content):
        path_src = os.path.join(dir_path_content, file)
        path_dest = os.path.join(dest_dir_path, file)
        if os.path.isfile(path_src) and file.endswith('.md'):
            generate_page(path_src, basepath, template_path, path_dest.replace('.md', '.html'))
        elif os.path.isdir(path_src):
            generate_pages_recursive(path_src, basepath, template_path, path_dest)

if __name__ == "__main__":
    main()