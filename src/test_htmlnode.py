import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_repr_1(self):
        node = HTMLNode(tag='p', value="This is some text in a paragraph.")
        node_str = f"Tag: p\nValue: This is some text in a paragraph.\nChildren: None\nProps: None"
        self.assertEqual(str(node), node_str)
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html(self):
        node = HTMLNode(
            tag='a',
             value="Boot.dev",
              props={
                  "href":"https://boot.dev",
                  "target":"_blank"
              } )
        node_props_str = f" href=\"https://boot.dev\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), node_props_str)
    
    def test_all_none(self):
        none_node = HTMLNode()
        self.assertEqual(str(none_node), f'Tag: None\nValue: None\nChildren: None\nProps: None')
        self.assertEqual(none_node.props_to_html(), '')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here", {"href":"https://boot.dev"})
        self.assertEqual(node.to_html(), "<a href=\"https://boot.dev\">Click here</a>")
    
    def test_leaf_to_html_a_w_target(self):
        node = LeafNode("a", "Click here", {"href":"https://boot.dev", "target":"_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://boot.dev\" target=\"_blank\">Click here</a>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")

if __name__ == "__main__":
    unittest.main()