"""Utility functions for the Static Site Generator.

This module provides helper functions for working with TextNodes and Markdown content.

Functions:
    split_nodes_delimiter(): Split text nodes on a delimiter and assign types to the resulting segments.
    extract_markdown_images(): Extract Markdown image tags from a string.
    extract_markdown_links(): Extract Markdown links from a string.
    split_nodes_image(): Split text nodes into text and image nodes based on Markdown image syntax.
    split_nodes_link(): Split text nodes into text and link nodes based on Markdown link syntax.

"""
import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Split text nodes on a delimiter and assign types to the resulting segments.

    Given a list of nodes, this function finds text nodes and splits their text
    on the provided delimiter (e.g., `**` for bold or `_` for italics). Text
    segments in even positions remain plain text, while segments in odd
    positions are wrapped with the provided `text_type`.

    Args:
        old_nodes (list[TextNode]): The list of existing text nodes.
        delimiter (str): The delimiter used to split the text (e.g. `"**"`).
        text_type (TextType): The text type to use for the delimited segments.

    Returns:
        list[TextNode]: A new list of nodes with text appropriately split and typed.

    Raises:
        Exception: If the split results in an even number of segments, indicating
            an unclosed or unmatched delimiter in the original text.
    """
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
    """Extract Markdown image tags from a string.

    Searches the provided text for Markdown image syntax of the form
    `![alt text](image_url)` and returns a list of tuples containing the
    extracted alt text and image URL.

    Args:
        text (str): The input string containing Markdown content.

    Returns:
        list[tuple[str, str]]: A list of `(alt_text, image_url)` pairs
        extracted from the Markdown image tags found in the text. If no
        image tags are present, an empty list is returned.
    """
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    """Extract Markdown links from a string.

    Searches the provided text for Markdown link syntax of the form
    `[link text](url)`—excluding image links (`![alt](url)`)—and returns a
    list of tuples containing the extracted link text and URL.

    Args:
        text (str): The input string containing Markdown content.

    Returns:
        list[tuple[str, str]]: A list of `(link_text, url)` pairs extracted
        from Markdown links found in the text. If no links are present,
        an empty list is returned.
    """
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    """Split text nodes into text and image nodes based on Markdown image syntax.

    Scans the given list of nodes for text nodes containing Markdown image
    syntax of the form `![alt](url)`. Each image occurrence is replaced with
    a `TextNode` of type `TextType.IMAGE`, and the surrounding text is
    preserved as `TextType.TEXT` nodes. Non-text nodes are passed through
    unchanged.

    Args:
        old_nodes (list[TextNode]): The list of existing nodes to process.

    Returns:
        list[TextNode]: A new list of nodes where any Markdown image syntax in
        text nodes has been converted into separate image and text nodes.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            matches = extract_markdown_images(text)
            
            while matches:
                alt, url = matches[0]

                full_match = f"![{alt}]({url})"
                before, after = text.split(full_match, 1)

                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))

                text = after
                matches = extract_markdown_images(text)
            
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    """Split text nodes into text and link nodes based on Markdown link syntax.

    Scans the given list of nodes for text nodes containing Markdown link
    syntax of the form `[text](url)`. Each link occurrence is replaced with
    a `TextNode` of type `TextType.LINK`, and the surrounding text is
    preserved as `TextType.TEXT` nodes. Non-text nodes are passed through
    unchanged.

    Args:
        old_nodes (list[TextNode]): The list of existing nodes to process.

    Returns:
        list[TextNode]: A new list of nodes where any Markdown link syntax in
        text nodes has been converted into separate link and text nodes.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            matches = extract_markdown_links(text)
            
            while matches:
                alt, url = matches[0]

                full_match = f"[{alt}]({url})"
                before, after = text.split(full_match, 1)

                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.LINK, url))

                text = after
                matches = extract_markdown_links(text)
            
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    textnodes = [TextNode(text, TextType.TEXT)]
    textnodes = split_nodes_delimiter(textnodes, '**', TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, '_', TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes, '`', TextType.CODE)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes

