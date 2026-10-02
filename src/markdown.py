from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        sub_texts = node.text.split(delimiter)
        if len(sub_texts) % 2 != 1:
            raise ValueError("Unmatched delimiter in text")

        for i, sub_text in enumerate(sub_texts):
            if i % 2 == 0:
                new_nodes.append(TextNode(sub_text, TextType.PLAIN, None))
            else:
                new_nodes.append(TextNode(sub_text, text_type, None))

    return new_nodes
