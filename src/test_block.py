import unittest

from src.block import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph_to_block_type(self):
        markdown_block = "Text line"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading_to_block_type(self):
        for i in range(1, 7):
            markdown_block = "#" * i + " Heading"
            block_type = block_to_block_type(markdown_block)
            self.assertEqual(block_type, BlockType.HEADING)

    def test_code_to_block_type(self):
        markdown_block = "```\ncode line\n```"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote_to_block_type(self):
        markdown_block = "> Quote line 1\n>Quote line 2\n> Quote line 3"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_without_lt(self):
        markdown_block = "> Quote line 1\nQuote line 2\n>Quote line 3"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_list_to_block_type(self):
        markdown_block = "- List item \n- List item 2\n- List item 3"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unordered_list_without_dash(self):
        markdown_block = "- List item 1\nList item 2\n- List item 3"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_to_block_type(self):
        markdown_block = "1. List item\n2. List item 2\n3. List item 3"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_without_numbers(self):
        markdown_block = "1. List item 1\nList item 2\n3. List item 3"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_with_unordered_numbers(self):
        markdown_block = "1. List item 1\n3. List item 2\n2. List item 3"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)