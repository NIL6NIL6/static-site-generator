class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        return " " + " ".join(
            f'{key}="{value}"' for key, value in self.props.items()
        ).strip()

    def __eq__(self, other: "HTMLNode") -> bool:
        return (
            isinstance(other, HTMLNode)
            and self.tag == other.tag
            and self.value == other.value
            and len(self.children) == len(other.children)
            and all(
                child1 == child2
                for child1, child2 in zip(self.children, other.children)
            )
            and len(self.props) == len(other.props)
            and all(
                key in other.props and self.props[key] == other.props[key]
                for key in self.props
            )
        )

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"