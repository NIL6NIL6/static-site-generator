import re

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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"\!\[(.*?)\]\((.*?)\)"
    matches: list[tuple[str, str]] = []
    for match in re.findall(pattern, text):
        matches.append((str(match[0]), str(match[1])))
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches: list[tuple[str, str]] = []
    for match in re.findall(pattern, text):
        matches.append((str(match[0]), str(match[1])))
    return matches

