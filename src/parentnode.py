from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Tag cannot be None for a ParentNode.")
        if self.children is None:
            raise ValueError("Children cannot be None for a ParentNode.")
        return (
            f"<{self.tag}{self.props_to_html()}>"
            + "".join(child.to_html() for child in self.children)
            + f"</{self.tag}>"
        )

    