import unittest

from htmlnode import HTMLNode

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
        node_props_str = f" href=https://boot.dev target=_blank"
        self.assertEqual(node.props_to_html(), node_props_str)
    
    def test_all_none(self):
        none_node = HTMLNode()
        self.assertEqual(str(none_node), f'Tag: None\nValue: None\nChildren: None\nProps: None')
        self.assertEqual(none_node.props_to_html(), '')

if __name__ == "__main__":
    unittest.main()