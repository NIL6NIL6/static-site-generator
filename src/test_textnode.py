import unittest

from src.leafnode import LeafNode
from src.textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr_plain(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node_str = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), node_str)

    def test_repr_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://example.com")
        node_str = "TextNode(This is a link node, link, https://example.com)"
        self.assertEqual(repr(node), node_str)

    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_diff_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_diff_none_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a link node", TextType.LINK, None)
        self.assertNotEqual(node, node2)

class TestTextNodeToLeafNode(unittest.TestCase):
    def test_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode(None, "This is a text node"))

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("b", "This is a text node"))

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("i", "This is a text node"))

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("code", "This is a text node"))

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://example.com")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("a", "This is a link node", {"href": "https://example.com"}))

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://example.com/image.png")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("img", None, {"src": "https://example.com/image.png", "alt": "This is an image node"}))


if __name__ == "__main__":
    unittest.main()
