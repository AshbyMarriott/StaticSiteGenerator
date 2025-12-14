
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        """Convert the HTML node to its HTML string representation.
        
        This is an abstract method that must be implemented by subclasses.
        Each subclass provides its own implementation based on whether it's a
        leaf node (with content) or a parent node (with children).
        
        Raises:
            NotImplementedError: Always, as this is an abstract method.
        """
        raise NotImplementedError
    
    def props_to_html(self):
        """Convert the node's properties dictionary to HTML attribute string.
        
        Converts a dictionary of HTML attributes (props) into a formatted
        string suitable for insertion into an HTML tag. The attributes are
        formatted as `key="value"` pairs separated by spaces.
        
        Returns:
            str: A string containing HTML attributes formatted as ` key="value"`.
                Returns an empty string if props is None. The leading space
                is included to allow direct concatenation with tag names.
        
        Example:
            If props = {"href": "https://example.com", "target": "_blank"},
            returns ' href="https://example.com" target="_blank"'.
        """
        props_str = ""
        if self.props is not None:
            props_str += ' ' + ' '.join(f"{k}=\"{v}\"" for k, v in self.props.items())
        return props_str
    
    def __repr__(self):
        return f"Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        """Convert the leaf node to its HTML string representation.
        
        Generates an HTML string for a leaf node, which contains content but
        no children. If the node has no tag, returns the value as plain text.
        Otherwise, returns a properly formatted HTML tag with the value as content.
        
        Returns:
            str: The HTML string representation of the leaf node. If tag is None,
                returns the value as plain text. Otherwise, returns a formatted
                HTML tag with attributes and content (e.g., '<p>content</p>').
        
        Raises:
            ValueError: If the value is None, as leaf nodes must have content.
        """
        if self.value is None:
            raise ValueError("Value is None!")
        if self.tag is None:
            return self.value
        html_str = f"<{self.tag}"
        if self.props is not None:
            html_str += self.props_to_html()
        html_str += f">{self.value}</{self.tag}>"
        return html_str

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props = props)
    
    def to_html(self):
        """Convert the parent node to its HTML string representation.
        
        Generates an HTML string for a parent node, which contains child nodes
        but no direct content. Recursively converts all child nodes to HTML and
        wraps them in the parent's tag.
        
        Returns:
            str: The HTML string representation of the parent node and all its
                children. The format is '<tag>child1_htmlchild2_html...</tag>'.
        
        Raises:
            ValueError: If the tag is None, as parent nodes must have a tag.
            ValueError: If children is None, as parent nodes must have children.
        """
        if self.tag is None:
            raise ValueError("Tag is None!")
        if self.children is None:
            raise ValueError("Children is None!")
        html_str = f"<{self.tag}{self.props_to_html()}>" + ''.join(f"{c.to_html()}" for c in self.children)
        html_str += f"</{self.tag}>"
        return html_str