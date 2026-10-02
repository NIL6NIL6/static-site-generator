import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("tag", "value")
        node2 = HTMLNode("tag", "value")
        self.assertEqual(node1, node2)

    def test_diff_tag(self):
        node1 = HTMLNode("tag1", "value")
        node2 = HTMLNode("tag2", "value")
        self.assertNotEqual(node1, node2)

    def test_diff_value(self):
        node1 = HTMLNode("tag", "value1")
        node2 = HTMLNode("tag", "value2")
        self.assertNotEqual(node1, node2)

    def test_eq_children(self):
        child = HTMLNode("child", "value")
        node1 = HTMLNode("tag", "value", children=[child])
        node2 = HTMLNode("tag", "value", children=[child])
        self.assertEqual(node1, node2)

    def test_diff_children(self):
        child1 = HTMLNode("child", "value1")
        child2 = HTMLNode("child", "value2")
        node1 = HTMLNode("tag", "value", children=[child1])
        node2 = HTMLNode("tag", "value", children=[child2])
        self.assertNotEqual(node1, node2)

    def test_eq_props(self):
        props = {"key": "value"}
        node1 = HTMLNode("tag", "value", props=props)
        node2 = HTMLNode("tag", "value", props=props)
        self.assertEqual(node1, node2)

    def test_diff_props(self):
        props1 = {"key": "value1"}
        props2 = {"key": "value2"}
        node1 = HTMLNode("tag", "value", props=props1)
        node2 = HTMLNode("tag", "value", props=props2)
        self.assertNotEqual(node1, node2)

    def test_diff_prop_keys(self):
        props1 = {"key1": "value"}
        props2 = {"key2": "value"}
        node1 = HTMLNode("tag", "value", props=props1)
        node2 = HTMLNode("tag", "value", props=props2)
        self.assertNotEqual(node1, node2)

    def test_no_props_to_html(self):
        node = HTMLNode("tag", "value")
        self.assertEqual(node.props_to_html(), "")

    def test_prop_to_html(self):
        props = {"key": "value"}
        props_html = ' key="value"'
        node = HTMLNode("tag", "value", props=props)
        self.assertEqual(node.props_to_html(), props_html)

    def test_props_to_html(self):
        props = {"key1": "value", "key2": "value"}
        props_html = ' key1="value" key2="value"'
        node = HTMLNode("tag", "value", props=props)
        self.assertEqual(node.props_to_html(), props_html)
