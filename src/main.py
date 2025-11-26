from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    aNode = TextNode('some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(aNode)

def text_node_to_html_node(text_node):
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

if __name__ == "__main__":
    main()