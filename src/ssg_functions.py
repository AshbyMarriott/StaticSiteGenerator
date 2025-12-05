import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception(f"Invalid Markdown syntax: unclosed delimiter found in \"{node.text}\"")
            for i in range(0, len(split_text)):
                if i % 2 == 1:
                    new_node = TextNode(split_text[i], text_type)
                    new_nodes.append(new_node)
                else:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    pass

def split_nodes_link(old_nodes):
    pass
