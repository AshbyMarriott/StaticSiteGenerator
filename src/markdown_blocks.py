def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        cleaned = block.strip()
        if cleaned:
            final_blocks.append(cleaned)
    return final_blocks