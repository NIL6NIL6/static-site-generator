import unittest
from textnode import TextNode, TextType
from markdown import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold(self):
        nodes = [TextNode("This is **bold** text", TextType.PLAIN, None)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.PLAIN, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text", TextType.PLAIN, None),
        ]
        self.assertEqual(result, expected)

    def test_split_italic(self):
        nodes = [TextNode("This is _italic_ text", TextType.PLAIN, None)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.PLAIN, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" text", TextType.PLAIN, None),
        ]
        self.assertEqual(result, expected)

    def test_split_code(self):
        nodes = [TextNode("This is `code` text", TextType.PLAIN, None)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.PLAIN, None),
            TextNode("code", TextType.CODE, None),
            TextNode(" text", TextType.PLAIN, None),
        ]
        self.assertEqual(result, expected)

    def test_split_multiple(self):
        nodes = [TextNode("This is **bold** and _italic_ text", TextType.PLAIN, None)]
        result_bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        result = split_nodes_delimiter(result_bold, "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.PLAIN, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" and ", TextType.PLAIN, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" text", TextType.PLAIN, None),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()