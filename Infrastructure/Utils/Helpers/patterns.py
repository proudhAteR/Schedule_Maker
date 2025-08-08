import re

REPS = [
    # Full days with modifiers
    {"label": "REPEAT", "pattern": [{"LOWER": {"IN": ["every", "on", "this", "next"]}}, {"LOWER": {"IN": [
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}}]},

    # Just day names (e.g., "Friday")
    {"label": "REPEAT", "pattern": [{"LOWER": {"IN": [
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}}]},

    # Abbreviated forms (e.g., "Mon", "Thurs")
    {"label": "REPEAT", "pattern": [{"LOWER": {"REGEX": r"^(mon|tue|tues|wed|weds|thu|thurs|fri|sat|sun)(day)?s?$"}}]},

]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december", "jan", "feb", "mar", "apr",
          "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
TIME_QUALIFIERS = ["sharp", "exactly", "approximately", "around", "about", "roughly",
                   "before", "after", "by", "no later than", "no earlier than"]
S_TIME_PATTERNS = [
    # 0. HIGHEST PRIORITY: Complete "between X and Y every DAY" pattern (NO trailing info)
    [
        {"LOWER": {"IN": ["between", "from"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # start time (accepts both : and .)
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},  # start meridiem
        {"LOWER": {"IN": ["and", "to", "until", "&", "-", "–", "—"]}},  # range separator
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # end time (accepts both : and .)
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},  # end meridiem
        {"LOWER": {"IN": ["every", "on", "each"]}},  # REQUIRED for complete pattern
        {"LOWER": {"IN": DAYS}}  # REQUIRED day - STOP HERE
    ],

    # 1. Complete "from X to Y every DAY" pattern (NO trailing info)
    [
        {"LOWER": {"IN": ["from", "starting"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},
        {"LOWER": {"IN": ["to", "until", "through", "thru", "till", "ending"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},
        {"LOWER": {"IN": ["every", "on", "each"]}},  # REQUIRED
        {"LOWER": {"IN": DAYS}}  # REQUIRED - STOP HERE
    ],

    # 2. Complete "every DAY from X to Y" pattern (NO trailing info)
    [
        {"LOWER": {"IN": ["every", "on", "each"]}},
        {"LOWER": {"IN": DAYS}},
        {"LOWER": {"IN": ["from", "between"]}, "OP": "?"},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},
        {"LOWER": {"IN": ["to", "and", "until", "-", "–", "—", "through", "thru", "till"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"}  # STOP HERE
    ],

    # NEW: Handle 24-hour format - "XX:XX-XX:XX every DAY" or "XX.XX-XX.XX every DAY"
    [
        {"TEXT": {"REGEX": r"^\d{1,2}$"}},  # First number (17)
        {"TEXT": {"IN": [":", "."]}},  # Colon or period
        {"TEXT": {"REGEX": r"^\d{2}$"}},  # Minutes (00)
        {"TEXT": {"IN": ["-", "–", "—", "to", "until"]}},  # Range separator
        {"TEXT": {"REGEX": r"^\d{1,2}$"}},  # End hour (19)
        {"TEXT": {"IN": [":", "."]}},  # Colon or period
        {"TEXT": {"REGEX": r"^\d{2}$"}},  # End minutes (15)
        {"LOWER": {"IN": ["every", "on", "each"]}},
        {"LOWER": {"IN": DAYS}}  # STOP HERE
    ],

    # NEW: Enhanced 24-hour format - more flexible (accepts both : and .)
    [
        {"TEXT": {"REGEX": r"^\d{1,2}[:.]\d{2}([:.]\d{2})?$"}},  # accepts both : and .
        {"TEXT": {"IN": ["to", "-", "–", "—", "through", "until"]}},
        {"TEXT": {"REGEX": r"^\d{1,2}[:.]\d{2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["every", "on", "each"]}},
        {"LOWER": {"IN": DAYS}}  # STOP HERE
    ],

    # 3. Complete "every DAY at X to Y" pattern (NO trailing info)
    [
        {"LOWER": {"IN": ["every", "on", "each"]}},
        {"LOWER": {"IN": DAYS}},
        {"LOWER": {"IN": ["at", "from"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},
        {"LOWER": {"IN": ["to", "until", "-", "–", "—", "through", "till"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"}  # STOP HERE
    ],

    # 4. Simple range with day: "X - Y every DAY" (NO trailing info)
    [
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},
        {"TEXT": {"IN": ["-", "–", "—", "to", "until"]}},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},
        {"LOWER": {"IN": ["every", "on", "each"]}},
        {"LOWER": {"IN": DAYS}}  # STOP HERE
    ],

    # 6. Cross-meridiem ranges: "11:30 am - 2:30 pm every Tuesday" (NO trailing info)
    [
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}},  # Required start meridiem
        {"TEXT": {"IN": ["to", "-", "–", "—", "through", "until"]}},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}},  # Required end meridiem
        {"LOWER": {"IN": ["every", "on", "each"]}},
        {"LOWER": {"IN": DAYS}}  # STOP HERE
    ],

    # 7. Hour-only ranges with day: "9 to 5 every weekday" (NO trailing info)
    [
        {"TEXT": {"REGEX": r"^\d{1,2}$"}},
        {"TEXT": {"IN": ["to", "until", "-", "–", "—", "through", "till"]}},
        {"TEXT": {"REGEX": r"^\d{1,2}$"}},
        {"LOWER": {"IN": ["every", "on", "each"]}},
        {"LOWER": {"IN": DAYS}}  # STOP HERE
    ],

    # --- LOWER PRIORITY: Single time patterns (only after range patterns fail) ---

    # 8. Single time with day: "every Tuesday at 3 pm" (NO trailing info)
    [
        {"LOWER": {"IN": ["every", "on", "each"]}},
        {"LOWER": {"IN": DAYS}},
        {"LOWER": {"IN": ["at", "from", "starting"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"}  # STOP HERE
    ],

    # 9. Day-first single time: "Tuesday at 3pm" (NO trailing info)
    [
        {"LOWER": {"IN": DAYS}},
        {"LOWER": {"IN": ["at", "from", "starting"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"}  # STOP HERE
    ],
    # NEW: Relative day + time range (e.g., "tomorrow from 2 p.m. to 3.30 p.m.")
    [
        {"LOWER": {"IN": ["tomorrow", "today", "tonight", "yesterday"]}},
        {"LOWER": {"IN": ["from", "at", "between", "starting"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},
        {"LOWER": {"IN": ["to", "until", "and", "-", "–", "—"]}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}, "OP": "?"},
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"}
    ],
    # NEW: Time range + relative day (e.g., "from 8 to noon tomorrow")
    [
        {"LOWER": {"IN": ["from", "between"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # Start time
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm", "noon", "midnight"]}, "OP": "?"},
        {"LOWER": {"IN": ["to", "until", "and", "-", "–", "—"]}},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # End time
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm", "noon", "midnight"]}, "OP": "?"},
        {"LOWER": {"IN": ["tomorrow", "today", "tonight", "yesterday"]}}  # Relative day
    ],

    # --- EVEN LOWER PRIORITY: Partial patterns ---

    # 10. Enhanced between pattern (without required day - for fallback)
    [
        {"LOWER": {"IN": ["between", "from"]}},
        {"LOWER": {"IN": TIME_QUALIFIERS}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},
        {"LOWER": {"IN": ["and", "to", "until", "&"]}},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"}
    ],

    # 11. Basic range pattern (fallback)
    [
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},
        {"TEXT": {"IN": ["to", "-", "–", "—", "through", "until"]}},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"}
    ],

    # 12. Single time patterns (lowest priority)
    [
        {"LOWER": {"IN": ["at", "by", "around", "about", "approximately", "roughly", "exactly"]}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"},
        {"LOWER": "sharp", "OP": "?"}
    ],

    # 13. Ordinal dates with times
    [
        {"LOWER": {"IN": MONTHS}},
        {"TEXT": {"REGEX": r"^\d{1,2}(st|nd|rd|th)?$"}},
        {"LOWER": {"IN": ["at", "from", "starting"]}, "OP": "?"},
        {"TEXT": {"REGEX": r"^\d{1,2}([:.]\d{2})?$"}},  # accepts both : and .
        {"LOWER": {"IN": ["a.m.", "am", "p.m.", "pm"]}, "OP": "?"}
    ],

    # 14. Meal times
    [
        {"LOWER": {"IN": ["lunch", "dinner", "breakfast", "brunch"]}},
        {"LOWER": {"IN": ["time", "hour", "break"]}}
    ],

    # 15. Business hours
    [
        {"LOWER": {"IN": ["business", "office", "working", "shop", "store"]}},
        {"LOWER": {"IN": ["hours", "time"]}}
    ],
    # 16. Relative date: Single words like "tomorrow", "today", "tonight"
    [
        {"LOWER": {"IN": ["tomorrow", "today", "tonight", "now", "yesterday"]}}
    ],

    # 17. Phrases like "day after tomorrow", "the day after tomorrow"
    [
        {"LOWER": {"IN": ["the", "day"]}, "OP": "?"},
        {"LOWER": "after"},
        {"LOWER": "tomorrow"}
    ],

    # 18. Relative future time like "in 2 days", "in a few weeks"
    [
        {"LOWER": "in"},
        {"LIKE_NUM": True, "OP": "?"},
        {"LOWER": {"IN": ["a", "an", "few"]}, "OP": "?"},
        {"LOWER": {"IN": ["minute", "minutes", "hour", "hours", "day", "days", "week", "weeks", "month", "months"]}}
    ],

    # 19. "Next/This/Coming [unit]" — e.g. "next week", "this weekend"
    [
        {"LOWER": {"IN": ["next", "this", "coming"]}},
        {"LOWER": {"IN": ["minute", "hour", "day", "week", "month", "weekend"]}}
    ]
]
LOCATION_PATTERNS = [
    [
        {"LOWER": {"IN": ["in", "at", "inside", "near"]}},
        {"LOWER": "the", "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "NUM", "X"]}, "OP": "+"}
    ],
]
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
TIME_EXPRESSIONS = {
    'noon': '12:00 pm',
    'midnight': '12:00 am',
    'morning': '9:00 am',
    'afternoon': '2:00 pm',
    'evening': '6:00 pm',
    'night': '9:00 pm'
}
TIME_PATTERNS = [
    # Natural language patterns first (higher priority)
    re.compile(
        r"\b(?:from|starting(?:\s+at)?|begins?(?:\s+at)?)\s+(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\s+(?:to|until|through|ending(?:\s+at)?|till)\s+(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\b",
        re.IGNORECASE),

    # Time ranges with meridiem
    re.compile(r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\s*(?:to|until|through|-|–|—)\s*(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
               re.IGNORECASE),

    # Single meridiem shared between times
    re.compile(r"\b(\d{1,2}(?::\d{2})?)\s*(?:to|until|through|-|–|—)\s*(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
               re.IGNORECASE),

    # 24-hour formats
    re.compile(r"\b([01]?\d|2[0-3]):([0-5]\d)\s*(?:to|until|through|-|–|—)\s*([01]?\d|2[0-3]):([0-5]\d)\b",
               re.IGNORECASE),
    re.compile(r"\b([01]?\d|2[0-3])\s*(?:to|until|through|-|–|—)\s*([01]?\d|2[0-3])\b", re.IGNORECASE),

    # Contextual patterns
    re.compile(
        r"\b(?:between|from)\s+(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\s+(?:and|to|until)\s+(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\b",
        re.IGNORECASE),
    # Matches "at 2:00 pm", "in 2:00 pm", "on 2:00 pm"
    re.compile(
        r"\b(?:at|in|on|around|about)?\s*(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
        re.IGNORECASE
    ),

]
DAY_PATTERNS = [
    re.compile(
        r"\b(?:every|on|this|next)?\s*"
        r"(?P<day>mon(?:day)?|tue(?:s|sday)?|wed(?:nesday)?|thu(?:rs|rsday)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?)s?\b",
        re.IGNORECASE
    ),
    re.compile(
        r"\b(?P<day>today|tomorrow|tonight|yesterday|day after tomorrow|day before yesterday|this weekend|next week|this week|next weekend)\b",
        re.IGNORECASE
    ),
]
DAY_MAPPINGS = {
    # Weekdays (lowercased for matching)
    'mon': 'Monday', 'monday': 'Monday',
    'tue': 'Tuesday', 'tues': 'Tuesday', 'tuesday': 'Tuesday',
    'wed': 'Wednesday', 'weds': 'Wednesday', 'wednesday': 'Wednesday',
    'thu': 'Thursday', 'thurs': 'Thursday', 'thursday': 'Thursday',
    'fri': 'Friday', 'friday': 'Friday',
    'sat': 'Saturday', 'saturday': 'Saturday',
    'sun': 'Sunday', 'sunday': 'Sunday',
}
