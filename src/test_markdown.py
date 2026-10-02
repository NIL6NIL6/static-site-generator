import unittest

from markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


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

class TestSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
        nodes = [TextNode("This is an image ![alt text](image.jpg) in text", TextType.PLAIN, None)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is an image ", TextType.PLAIN, None),
            TextNode("alt text", TextType.IMAGE, "image.jpg"),
            TextNode(" in text", TextType.PLAIN, None),
        ]
        self.assertEqual(result, expected)

    def test_split_image_last(self):
        nodes = [TextNode("This is an image at the end ![alt text](image.jpg)", TextType.PLAIN, None)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is an image at the end ", TextType.PLAIN, None),
            TextNode("alt text", TextType.IMAGE, "image.jpg"),
        ]
        self.assertEqual(result, expected)

    def test_split_images(self):
        nodes = [TextNode("This is an image ![alt text](image.jpg) and another ![another image](another.jpg) in text", TextType.PLAIN, None)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is an image ", TextType.PLAIN, None),
            TextNode("alt text", TextType.IMAGE, "image.jpg"),
            TextNode(" and another ", TextType.PLAIN, None),
            TextNode("another image", TextType.IMAGE, "another.jpg"),
            TextNode(" in text", TextType.PLAIN, None),
        ]
        self.assertEqual(result, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_link(self):
        nodes = [TextNode("This is a link [link text](link.html) in text", TextType.PLAIN, None)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("This is a link ", TextType.PLAIN, None),
            TextNode("link text", TextType.LINK, "link.html"),
            TextNode(" in text", TextType.PLAIN, None),
        ]
        self.assertEqual(result, expected)

    def test_split_link_last(self):
        nodes = [TextNode("This is a link at the end [link text](link.html)", TextType.PLAIN, None)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("This is a link at the end ", TextType.PLAIN, None),
            TextNode("link text", TextType.LINK, "link.html"),
        ]
        self.assertEqual(result, expected)

    def test_split_links(self):
        nodes = [TextNode("This is a link [link text](link.html) and another [another link](another.html) in text", TextType.PLAIN, None)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("This is a link ", TextType.PLAIN, None),
            TextNode("link text", TextType.LINK, "link.html"),
            TextNode(" and another ", TextType.PLAIN, None),
            TextNode("another link", TextType.LINK, "another.html"),
            TextNode(" in text", TextType.PLAIN, None),
        ]
        self.assertEqual(result, expected)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "garbage garbage ![alt text](image.jpg) garbage garbage"
        result = extract_markdown_images(text)
        expected = [("alt text", "image.jpg")]
        self.assertEqual(result, expected)

    def test_extract_multiple_markdown_images(self):
        text = "garbage garbage ![alt text](image.jpg) garbage ![another image](another.jpg) garbage garbage"
        result = extract_markdown_images(text)
        expected = [("alt text", "image.jpg"), ("another image", "another.jpg")]
        self.assertEqual(result, expected)

    def test_avoid_markdown_links(self):
        text = "garbage garbage [alt text](image.jpg) garbage garbage"
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

    def test_mix_images_and_links(self):
        text = "garbage garbage ![alt text](image.jpg) garbage garbage [link text](link.html) garbage garbage ![another image](another.jpg) garbage garbage [another link](another.html) garbage garbage"
        result_images = extract_markdown_images(text)
        expected_images = [("alt text", "image.jpg"), ("another image", "another.jpg")]
        self.assertEqual(result_images, expected_images)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "[link text](link.html)"
        result = extract_markdown_links(text)
        expected = [("link text", "link.html")]
        self.assertEqual(result, expected)

    def test_extract_multiple_markdown_links(self):
        text = "[link text](link.html) [another link](another.html)"
        result = extract_markdown_links(text)
        expected = [("link text", "link.html"), ("another link", "another.html")]
        self.assertEqual(result, expected)

    def test_avoid_markdown_images(self):
        text = "garbage garbage ![alt text](image.jpg) [link text](link.html) garbage garbage"
        result = extract_markdown_links(text)
        expected = [("link text", "link.html")]
        self.assertEqual(result, expected)

    def test_mix_images_and_links(self):
        text = "garbage garbage ![alt text](image.jpg) garbage garbage [link text](link.html) garbage garbage ![another image](another.jpg) garbage garbage [another link](another.html) garbage garbage"
        result_links = extract_markdown_links(text)
        expected_links = [("link text", "link.html"), ("another link", "another.html")]
        self.assertEqual(result_links, expected_links)


if __name__ == "__main__":
    unittest.main()
