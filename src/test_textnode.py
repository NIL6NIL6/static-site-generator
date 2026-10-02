import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
