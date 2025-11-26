from textnode import TextNode, TextType

def main():
    aNode = TextNode('some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(aNode)

if __name__ == "__main__":
    main()