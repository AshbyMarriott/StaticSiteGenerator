
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
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
        if self.tag is None:
            raise ValueError("Tag is None!")
        if self.children is None:
            raise ValueError("Children is None!")
        html_str = f"<{self.tag}{self.props_to_html()}>" + ''.join(f"{c.to_html()}" for c in self.children)
        html_str += f"</{self.tag}>"
        return html_str