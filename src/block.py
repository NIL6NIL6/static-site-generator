import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^```\n.*\n```$", block, re.DOTALL):
        return BlockType.CODE
    elif all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^\d+\. ", line) for line in block.split("\n")):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH