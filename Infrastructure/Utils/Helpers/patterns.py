import re

# Core constants - optimized for better coverage and maintainability
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"]
WEEKENDS = ["saturday", "sunday"]

MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december", "jan", "feb", "mar", "apr",
          "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

# Time qualifiers and connectors
TIME_QUALIFIERS = ["sharp", "exactly", "approximately", "around", "about", "roughly",
                   "before", "after", "by", "no later than", "no earlier than"]
TIME_CONNECTORS = ["to", "until", "through", "thru", "till", "and", "-", "–", "—"]
TIME_PREPOSITIONS = ["at", "from", "between", "starting", "beginning"]

# Meridiem indicators
MERIDIEM = ["a.m.", "am", "p.m.", "pm"]
SPECIAL_TIMES = ["noon", "midnight", "morning", "afternoon", "evening", "night"]

# Day modifiers
DAY_MODIFIERS = ["every", "on", "each", "this", "next", "coming"]
RELATIVE_DAYS = ["today", "tomorrow", "tonight", "yesterday", "weekend"]

# Optimized regex patterns - compiled once for better performance
TIME_REGEX = r"^\d{1,2}([:.]\d{2})?$"
HOUR_REGEX = r"^\d{1,2}$"
MINUTES_REGEX = r"^\d{2}$"
ORDINAL_REGEX = r"^\d{1,2}(st|nd|rd|th)?$"
DAY_ABBREV_REGEX = r"^(mon|tue|tues|wed|weds|thu|thurs|fri|sat|sun)(day)?s?$"

# Repeat patterns - simplified and more maintainable
REPS = [
    {"label": "REPEAT", "pattern": [
        {"LOWER": {"IN": DAY_MODIFIERS}},
        {"LOWER": {"IN": DAYS}}
    ]},
    {"label": "REPEAT", "pattern": [
        {"LOWER": {"IN": DAYS}}
    ]},
    {"label": "REPEAT", "pattern": [
        {"LOWER": {"REGEX": DAY_ABBREV_REGEX}}
    ]},
]

# Core building blocks for complex patterns
TIME_COMPONENT = {"TEXT": {"REGEX": TIME_REGEX}}
MERIDIEM_COMPONENT = {"LOWER": {"IN": MERIDIEM}, "OP": "?"}
QUALIFIER_COMPONENT = {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"}
CONNECTOR_COMPONENT = {"LOWER": {"IN": TIME_CONNECTORS}}
DAY_COMPONENT = {"LOWER": {"IN": DAYS}}
DAY_MODIFIER_COMPONENT = {"LOWER": {"IN": DAY_MODIFIERS}}

# Optimized time patterns - prioritized by complexity and frequency
S_TIME_PATTERNS = [
    # High Priority: Complete recurring patterns with days

    # Pattern 1: "every DAY from X to Y" / "every DAY X to Y"
    [
        DAY_MODIFIER_COMPONENT,
        DAY_COMPONENT,
        {"LOWER": {"IN": ["from", "at"]}, "OP": "?"},
        QUALIFIER_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT,
        CONNECTOR_COMPONENT,
        QUALIFIER_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT
    ],

    # Pattern 2: "from X to Y every DAY"
    [
        {"LOWER": {"IN": ["from", "between"]}},
        QUALIFIER_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT,
        CONNECTOR_COMPONENT,
        QUALIFIER_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT,
        DAY_MODIFIER_COMPONENT,
        DAY_COMPONENT
    ],

    # Pattern 3: 24-hour format with days - "HH:MM-HH:MM every DAY"
    [
        {"TEXT": {"REGEX": r"^\d{1,2}[:.]\d{2}$"}},
        {"TEXT": {"IN": ["-", "–", "—", "to"]}},
        {"TEXT": {"REGEX": r"^\d{1,2}[:.]\d{2}$"}},
        DAY_MODIFIER_COMPONENT,
        DAY_COMPONENT
    ],

    # Pattern 4: Cross-meridiem ranges - "X am to Y pm every DAY"
    [
        TIME_COMPONENT,
        {"LOWER": {"IN": MERIDIEM}},  # Required
        CONNECTOR_COMPONENT,
        TIME_COMPONENT,
        {"LOWER": {"IN": MERIDIEM}},  # Required
        DAY_MODIFIER_COMPONENT,
        DAY_COMPONENT
    ],

    # Pattern 5: Simple time ranges - "X-Y every DAY"
    [
        TIME_COMPONENT,
        MERIDIEM_COMPONENT,
        CONNECTOR_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT,
        DAY_MODIFIER_COMPONENT,
        DAY_COMPONENT
    ],

    # Medium Priority: Single time patterns

    # Pattern 6: "every DAY at X"
    [
        DAY_MODIFIER_COMPONENT,
        DAY_COMPONENT,
        {"LOWER": {"IN": TIME_PREPOSITIONS}},
        QUALIFIER_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT
    ],

    # Pattern 7: "DAY at X"
    [
        DAY_COMPONENT,
        {"LOWER": {"IN": TIME_PREPOSITIONS}},
        QUALIFIER_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT
    ],

    # Relative time patterns

    # Pattern 8: Relative single days with times - "tomorrow at X"
    [
        {"LOWER": {"IN": RELATIVE_DAYS}},
        {"LOWER": {"IN": TIME_PREPOSITIONS}},
        QUALIFIER_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT
    ],

    # Pattern 9: Relative multi-word - "next week at X"
    [
        {"LOWER": {"IN": ["next", "this", "coming"]}},
        {"LOWER": {"IN": ["week", "month", "weekend"]}},
        {"LOWER": {"IN": TIME_PREPOSITIONS}},
        QUALIFIER_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT
    ],

    # Lower Priority: Fallback patterns

    # Pattern 10: Generic time ranges (no day specified)
    [
        {"LOWER": {"IN": ["from", "between"]}},
        QUALIFIER_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT,
        CONNECTOR_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT
    ],

    # Pattern 11: Simple range fallback
    [
        TIME_COMPONENT,
        MERIDIEM_COMPONENT,
        CONNECTOR_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT
    ],

    # Pattern 12: Single time fallback
    [
        {"LOWER": {"IN": TIME_PREPOSITIONS}, "OP": "?"},
        QUALIFIER_COMPONENT,
        TIME_COMPONENT,
        MERIDIEM_COMPONENT,
        {"LOWER": "sharp", "OP": "?"}
    ],

    # Specialized patterns

    # Pattern 13: Date with time - "January 15th at 3pm"
    [
        {"LOWER": {"IN": MONTHS}},
        {"TEXT": {"REGEX": ORDINAL_REGEX}},
        {"LOWER": {"IN": TIME_PREPOSITIONS}, "OP": "?"},
        TIME_COMPONENT,
        MERIDIEM_COMPONENT
    ],
    # Pattern 14: Relative future - "in 2 days"
    [
        {"LOWER": "in"},
        {"LIKE_NUM": True, "OP": "?"},
        {"LOWER": {"IN": ["a", "an", "few", "couple"]}, "OP": "?"},
        {"LOWER": {"IN": ["minute", "minutes", "hour", "hours", "day", "days",
                          "week", "weeks", "month", "months", "year", "years"]}}
    ]
]

# Location patterns - simplified
LOCATION_PATTERNS = [
    [
        {"LOWER": {"IN": ["in", "at", "inside", "near"]}},
        {"LOWER": "the", "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "+"}
    ],
]

# Extra context patterns
EXTRA_PATTERNS = [
    [
        {"LOWER": {"IN": ["by", "with", "for"]}},
        {"LOWER": "the", "OP": "?"},
        # Match word, optional period, more words
        {"IS_ALPHA": True},  # Required first word
        {"TEXT": ".", "OP": "?"},  # Optional period
        {"IS_ALPHA": True, "OP": "*"}  # Optional additional words
    ]
]

# Time expressions mapping
TIME_EXPRESSIONS = {
    'noon': '12:00 pm',
    'midnight': '12:00 am',
    'morning': '9:00 am',
    'afternoon': '2:00 pm',
    'evening': '6:00 pm',
    'night': '9:00 pm',
    'dawn': '6:00 am',
    'dusk': '7:00 pm'
}

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
