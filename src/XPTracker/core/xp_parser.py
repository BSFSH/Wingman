import re


def parse_xp_message(text_block: str) -> int:
    # Use finditer to find ALL occurrences in the block, not just the first
    xp_pattern = re.compile(r'You gain\s+(\d+)(?:\s+\(\+(\d+)\))?.*experience', re.IGNORECASE)

    total_xp = 0
    # This loop ensures we catch the Mummy AND the Sphinx in the same block
    for match in xp_pattern.finditer(text_block):
        base = int(match.group(1))
        bonus = int(match.group(2)) if match.group(2) else 0
        total_xp += (base + bonus)

    return total_xp
