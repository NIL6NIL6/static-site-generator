import re

from src.textnode import TextNode, TextType


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
            if i % 2 == 0 and sub_text != "":
                new_nodes.append(TextNode(sub_text, TextType.PLAIN, None))
            else:
                new_nodes.append(TextNode(sub_text, text_type, None))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        sub_texts = extract_markdown_images(node.text)
        if len(sub_texts) == 0:
            new_nodes.append(node)
            continue

        start_index = 0
        for alt_text, url in sub_texts:
            image_text = f"![{alt_text}]({url})"
            image_index = node.text.find(image_text, start_index)
            if image_index != start_index:
                new_nodes.append(
                    TextNode(
                        node.text[start_index:image_index],
                        TextType.PLAIN,
                        None,
                    )
                )
            start_index = image_index + len(image_text)
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
        if start_index != len(node.text):
            new_nodes.append(
                TextNode(node.text[start_index:], TextType.PLAIN, None)
            )
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        sub_texts = extract_markdown_links(node.text)
        if len(sub_texts) == 0:
            new_nodes.append(node)
            continue

        start_index = 0
        for alt_text, url in sub_texts:
            link_text = f"[{alt_text}]({url})"
            link_index = node.text.find(link_text, start_index)
            if link_index != start_index:
                new_nodes.append(
                    TextNode(
                        node.text[start_index:link_index], TextType.PLAIN, None
                    )
                )
            start_index = link_index + len(link_text)
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
        if start_index != len(node.text):
            new_nodes.append(
                TextNode(node.text[start_index:], TextType.PLAIN, None)
            )
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = split_nodes_image([TextNode(text, TextType.PLAIN, None)])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    return [
        stripped_block
        for block in markdown.split("\n\n")
        if len(stripped_block := block.strip()) > 0
    ]
