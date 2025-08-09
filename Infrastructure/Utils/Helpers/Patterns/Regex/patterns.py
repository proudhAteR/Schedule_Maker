import re

# Compiled regex patterns for better performance
TIME_PATTERNS = [
    # Natural language time ranges
    re.compile(
        r"\b(?:from|starting(?:\s+at)?|begins?(?:\s+at)?)\s+"
        r"(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\s+"
        r"(?:to|until|through|ending(?:\s+at)?|till)\s+"
        r"(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\b",
        re.IGNORECASE
    ),

    # Cross-meridiem ranges - "X am to Y pm"
    re.compile(
        r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\s*"
        r"(?:to|until|through|-|–|—)\s*"
        r"(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
        re.IGNORECASE
    ),

    # Shared meridiem - "X to Y am/pm"
    re.compile(
        r"\b(\d{1,2}(?::\d{2})?)\s*"
        r"(?:to|until|through|-|–|—)\s*"
        r"(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
        re.IGNORECASE
    ),

    # 24-hour format ranges
    re.compile(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\s*"
        r"(?:to|until|through|-|–|—)\s*"
        r"([01]?\d|2[0-3]):([0-5]\d)\b",
        re.IGNORECASE
    ),

    # Hour-only 24-hour ranges
    re.compile(
        r"\b([01]?\d|2[0-3])\s*"
        r"(?:to|until|through|-|–|—)\s*"
        r"([01]?\d|2[0-3])\b",
        re.IGNORECASE
    ),

    # Between/from patterns
    re.compile(
        r"\b(?:between|from)\s+"
        r"(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\s+"
        r"(?:and|to|until)\s+"
        r"(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\b",
        re.IGNORECASE
    ),

    # Single time with preposition
    re.compile(
        r"\b(?:at|by|around|about|approximately)?\s*"
        r"(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
        re.IGNORECASE
    ),

    # Special time expressions
    re.compile(
        r"\b(noon|midnight|morning|afternoon|evening|night|dawn|dusk)\b",
        re.IGNORECASE
    )
]

# Day patterns - optimized for better matching
DAY_PATTERNS = [
    # Standard weekday patterns with optional modifiers
    re.compile(
        r"\b(?:every|on|this|next|coming)?\s*"
        r"(?P<day>mon(?:day)?|tue(?:s|sday)?|wed(?:nesday)?|"
        r"thu(?:rs|rsday)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?)s?\b",
        re.IGNORECASE
    ),

    # Relative day expressions
    re.compile(
        r"\b(?P<day>today|tomorrow|tonight|yesterday|"
        r"day\s+after\s+tomorrow|day\s+before\s+yesterday|"
        r"this\s+weekend|next\s+week(?:end)?|this\s+week)\b",
        re.IGNORECASE
    ),

    # Weekday/weekend groups
    re.compile(
        r"\b(?:every\s+)?(?P<day>weekday|weekend|weeknight)s?\b",
        re.IGNORECASE
    )
]

# Enhanced day mappings with more variations
DAY_MAPPINGS = {
    # Standard weekdays
    'mon': 'Monday', 'monday': 'Monday',
    'tue': 'Tuesday', 'tues': 'Tuesday', 'tuesday': 'Tuesday',
    'wed': 'Wednesday', 'weds': 'Wednesday', 'wednesday': 'Wednesday',
    'thu': 'Thursday', 'thurs': 'Thursday', 'thursday': 'Thursday',
    'fri': 'Friday', 'friday': 'Friday',
    'sat': 'Saturday', 'saturday': 'Saturday',
    'sun': 'Sunday', 'sunday': 'Sunday',

    # Relative days
    'today': 'Today',
    'tomorrow': 'Tomorrow',
    'tonight': 'Tonight',
    'yesterday': 'Yesterday',
    'day after tomorrow': 'Day After Tomorrow',
    'day before yesterday': 'Day Before Yesterday',

    # Time periods
    'this weekend': 'This Weekend',
    'next weekend': 'Next Weekend',
    'this week': 'This Week',
    'next week': 'Next Week',
    'weekday': 'Weekdays',
    'weekend': 'Weekend',
    'weeknight': 'Weeknights'
}
