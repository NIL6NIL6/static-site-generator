import re

from src.block import BlockType, block_to_block_type
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.markdown_helpers import markdown_to_blocks, text_to_textnodes
from src.parentnode import ParentNode
from src.textnode import text_node_to_html_node


def text_to_children(text: str) -> list[HTMLNode]:
    text = text.replace("\n", " ")
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]


def paragraph_to_html_node(paragraph: str) -> HTMLNode:
    return ParentNode("p", text_to_children(paragraph), None)


def heading_to_html_node(heading: str) -> HTMLNode:
    level = len(re.match(r"^(#+)", heading).group(0))
    text = heading[level:].strip()
    return ParentNode(f"h{level}", text_to_children(text), None)


def code_to_html_node(code: str) -> HTMLNode:
    return ParentNode("pre", [LeafNode("code", code[4:-3], None)], None)


def quote_to_html_node(quote: str) -> HTMLNode:
    return ParentNode("blockquote", text_to_children(quote[1:].strip()), None)


def unordered_list_to_html_node(unordered_list: str) -> HTMLNode:
    return ParentNode(
        "ul",
        [
            ParentNode("li", text_to_children(list_item[1:].strip()), None)
            for list_item in unordered_list.split("\n")
        ],
    )


def ordered_list_to_html_node(ordered_list: str) -> HTMLNode:
    return ParentNode(
        "ol",
        [
            ParentNode(
                "li",
                text_to_children(re.match(r"\d+\.\s+(.*)", list_item).group(1).strip()),
                None,
            )
            for list_item in ordered_list.split("\n")
        ],
    )


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block, block_type in zip(blocks, map(block_to_block_type, blocks)):
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.CODE:
                children.append(code_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                children.append(ordered_list_to_html_node(block))
    return ParentNode("div", children, None)
