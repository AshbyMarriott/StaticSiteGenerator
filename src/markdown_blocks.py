from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        cleaned = block.strip()
        if cleaned:
            final_blocks.append(cleaned)
    return final_blocks

def block_to_block_type(block):
    if block.startswith(('# ', '## ', '### ', '#### ', '##### ', '###### ')):
        return BlockType.HEADING
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    block_lines = block.split('\n')
    starts_with_quote = True
    starts_with_unordered = True
    starts_with_ordered = True
    ordered_count = 1
    for i in block_lines:
        if not i.startswith('>'):
            starts_with_quote = False
        if not i.startswith('- '):
            starts_with_unordered = False
        if not i.startswith(f'{ordered_count}. '):
            starts_with_ordered = False
        ordered_count += 1
    if starts_with_quote:
        return BlockType.QUOTE
    if starts_with_unordered:
        return BlockType.UNORDERED_LIST
    if starts_with_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH