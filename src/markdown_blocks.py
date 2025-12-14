from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    """Split markdown text into individual blocks.
    
    Separates markdown text by double newlines and returns a list of cleaned
    block strings. Empty blocks are filtered out.
    
    Args:
        markdown (str): The markdown text to split into blocks.
    
    Returns:
        list[str]: A list of block strings, each stripped of leading/trailing
            whitespace. Empty blocks are excluded.
    """
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        cleaned = block.strip()
        if cleaned:
            final_blocks.append(cleaned)
    return final_blocks

def extract_heading_level(block):
    """Extract the heading level (1-6) from a markdown header block.
    
    Parses the number of consecutive '#' characters at the start of a block
    to determine the heading level. Validates that the heading is properly
    formatted with a space after the hashes.
    
    Args:
        block (str): The markdown block to check for heading syntax.
    
    Returns:
        int or None: The heading level (1-6) if the block is a valid heading,
            None otherwise. Returns None if the block doesn't start with '#',
            has more than 6 '#' characters, or doesn't have a space after
            the hashes.
    """
    if not block or block[0] != '#':
        return None
    count = 0
    for char in block:
        if char == '#':
            count += 1
        else:
            break
    if 1 <= count <= 6 and count < len(block) and block[count] == ' ':
        return count
    return None

def block_to_block_type(block):
    """Determine the type of a markdown block.
    
    Analyzes the structure and syntax of a markdown block to classify it
    as one of the supported block types: heading, code, quote, unordered list,
    ordered list, or paragraph.
    
    Args:
        block (str): The markdown block to classify.
    
    Returns:
        BlockType: The type of the block. Possible values:
            - BlockType.HEADING: Block starts with 1-6 '#' characters
            - BlockType.CODE: Block starts and ends with '```'
            - BlockType.QUOTE: All lines start with '>'
            - BlockType.UNORDERED_LIST: All lines start with '- '
            - BlockType.ORDERED_LIST: Lines start with '1. ', '2. ', etc.
            - BlockType.PARAGRAPH: Default for blocks that don't match other types
    """
    if extract_heading_level(block) is not None:
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



def strip_ordered_list_prefix(text_list):
    """Remove ordered list number prefixes from a list of strings.
    
    Removes the numbered prefix (e.g., "1. ", "2. ", "3. ") from each string
    in the list, validating that the numbering is sequential and correct.
    
    Args:
        text_list (list[str]): A list of strings, each expected to start with
            a sequential number prefix (e.g., "1. text", "2. text", "3. text").
    
    Returns:
        list[str]: A list of strings with the number prefixes removed.
    
    Raises:
        Exception: If any item doesn't start with the expected sequential
            number prefix (e.g., if item 2 doesn't start with "2. ").
    """
    ordered_count = 1
    stripped_text_list = []
    for text in text_list:
        if text.startswith(f'{ordered_count}. '):
            stripped_text_list.append(text.strip(f'{ordered_count}. '))
            ordered_count += 1
        else:
            raise Exception(f"Ordered list item {text} does not start with {ordered_count}. ")
    return stripped_text_list

def strip_paragraph_newlines(text):
    """Remove newlines from paragraph text and join with spaces.
    
    Splits text by newlines, strips whitespace from each line, filters out
    empty lines, and joins the remaining lines with single spaces. This
    converts multi-line paragraph text into a single line suitable for
    HTML paragraph elements.
    
    Args:
        text (str): The paragraph text that may contain newlines.
    
    Returns:
        str: The text with newlines removed and lines joined with spaces.
            Empty lines are removed.
    """
    lines = text.split('\n')
    stripped_lines = []
    for line in lines:
        if line.strip():
            stripped_lines.append(line.strip())
    return ' '.join(stripped_lines)

def strip_codeblock_backticks(text):
    """Remove markdown code block delimiters from code block text.
    
    Removes the opening and closing triple backticks (```) from a markdown
    code block, returning only the code content. Handles both code blocks
    with and without newlines after the opening delimiter.
    
    Args:
        text (str): The markdown code block text including backticks.
    
    Returns:
        str: The code content with backticks removed. If the block starts
            with '```\n', removes both the opening and closing backticks.
            Otherwise, removes the first occurrence of '```' and everything
            before it.
    """
    if text.startswith('```\n'):
        return text.split('```\n')[1].strip('```')
    else:
        return text.split('```')[1]


def extract_title(markdown):
    """Extract the title from markdown content.
    
    Searches for the first line in the markdown that starts with '# ' (a level 1
    heading) and returns the text content of that heading as the title.
    
    Args:
        markdown (str): The markdown text to extract the title from.
    
    Returns:
        str: The title text with the '# ' prefix removed.
    
    Raises:
        Exception: If no level 1 heading (starting with '# ') is found in the
            markdown content.
    """
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.strip('# ')
    raise Exception("No title found in markdown")