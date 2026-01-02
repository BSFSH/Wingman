import re
from typing import List, Dict, Any


def parse_xp_message(text_block: str) -> int:
    """Parses text for XP gains."""
    # Use finditer to find ALL occurrences in the block
    xp_pattern = re.compile(r'You gain\s+(\d+)(?:\s+\(\+(\d+)\))?.*experience', re.IGNORECASE)

    total_xp = 0
    for match in xp_pattern.finditer(text_block):
        base = int(match.group(1))
        bonus = int(match.group(2)) if match.group(2) else 0
        total_xp += (base + bonus)

    return total_xp


def parse_group_status(text_block: str, includePets: bool = False) -> List[Dict[str, Any]]:
    """
    Parses a text block for group member status.
    Returns a list of dictionaries for valid rows found.
    """
    members = []

    # Regex Breakdown:
    classAndLevel = r"\[\s*(?P<cls>[A-Za-z]+)\s+(?P<lvl>\d+)\s*\]"
    spaceAfterBracket = r"\s+"
    statusIndicators = r"(?P<status>(?:[BPDS]\s)*)"
    characterName = r"(?P<name>.+?)"
    health = r"\s+(?P<hp>\d+/\s*\d+)"
    skipPercentIndicators = r".*?"
    fatigue = r"\s+(?P<fat>\d+/\s*\d+)"
    power = r"\s+(?P<pwr>\d+/\s*\d+)"

    currentPartyMember = classAndLevel + spaceAfterBracket + statusIndicators + characterName \
                        + health + skipPercentIndicators \
                        + fatigue + skipPercentIndicators \
                        + power

    newFollowersName = r"(?P<NewGroupMember>.+)"
    followsYou = r"\s{1}follows you"
    newFollower = f"{newFollowersName}{followsYou}"


    groupParserString = f"({currentPartyMember}|{newFollower})"

    pattern = re.compile(groupParserString,
        re.DOTALL
    )
    
    def isCurrentPartyMember(line: str) -> bool:
        return ']' in line and '/' in line

    def isNewFollower(line: str) -> bool:
        return 'follows you' in line

    for line in text_block.splitlines():
        if isCurrentPartyMember(line):
            match = pattern.search(line)
            if match:
                data = match.groupdict()

                # NEW: Exclude pets/mobs immediately
                if not includePets and data['cls'].lower() == 'mob':
                    continue

                data['status'] = data['status'].strip()
                data['name'] = data['name'].strip()
                members.append(data)

        elif isNewFollower(line):
            match = pattern.search(line)
            if match:
                data = match.groupdict()

                data['NewGroupMember'] = match.group('NewGroupMember').strip()
                members.append(data)

    return members
