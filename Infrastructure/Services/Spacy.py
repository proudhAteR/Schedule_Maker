import Infrastructure.Utils.Helpers.Imports as Imp
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.tokens.doc import Doc

from Core.Interface.Tokenizer import Tokenizer

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
TIME_PATTERNS = [
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
        {"IS_PUNCT": False, "IS_SPACE": False, "OP": "+"}
    ]
]


class Spacy(Tokenizer):

    def __init__(self, model: str = "en_core_web_sm"):
        self.core = Imp.ensure_spacy_model(model)
        self.matcher = Matcher(self.core.vocab)
        self.__add_patterns()

    def __add_patterns(self):
        ruler = EntityRuler(self.core)
        ruler.add_patterns(REPS)
        self._add_matcher_patterns()

    def _add_matcher_patterns(self):
        for i, pattern in enumerate(TIME_PATTERNS):
            self.matcher.add(f"time_{i}", [pattern])

        for i, p in enumerate(LOCATION_PATTERNS):
            self.matcher.add(f"location_{i}", [p])

        for i, p in enumerate(EXTRA_PATTERNS):
            self.matcher.add(f"extra_{i}", [p])

    def tokenize(self, sentence: str) -> dict:
        doc = self.core(sentence)
        tokens = self.__process_output(doc)
        return tokens

    def __match(self, doc: Doc, matched_token_ids: set) -> dict:
        res = {}
        matches = self.matcher(doc)

        for match_id, start, end in matches:
            match_range = range(start, end)

            label, span = self.__get_match_infos(doc, match_id, match_range)
            matched_token_ids.update(match_range)

            if label not in res or len(span.text) > len(res[label]):
                self.__update_res(label, res, span)

        return res

    def __get_match_infos(self, doc: Doc, match_id: int, match_range: range):
        label = self.core.vocab.strings[match_id]
        span = doc[match_range.start:match_range.stop]

        return label, span

    @staticmethod
    def __update_res(label, res, span):
        res[label] = span.text

    def __process_output(self, doc: Doc) -> dict:

        matched_token_ids = set()
        res = self.__match(doc, matched_token_ids)

        tokens = self.__sanitize_tokens(res)
        self.__adjust_time(doc, tokens)

        if "_matched_spans" in tokens:
            matched_token_ids.update(tokens.pop("_matched_spans"))

        tokens["title"] = self.__get_title(doc, matched_token_ids)
        return tokens

    @staticmethod
    def __adjust_time(doc: Doc, tokens: dict):
        if "time" not in tokens or not tokens["time"]:
            for ent in doc.ents:
                if ent.label_ in {"DATE", "TIME"}:
                    tokens["time"] = ent.text
                    tokens.setdefault("_matched_spans", set()).update(range(ent.start, ent.end))
                    break

        tokens['time'] = Spacy.quick_clean(
            tokens['time']
        )

    @staticmethod
    def quick_clean(time_str: str):
        return time_str.replace(": ", ":").replace(" :", ":").replace("- ", "-").replace(" -", "-")

    @staticmethod
    def __sanitize_tokens(raw_tokens: dict) -> dict:
        merged = {
            "location": [],
            "time": [],
            "extra": [],
        }

        for key, value in raw_tokens.items():
            if isinstance(value, str):
                value = [value]

            base_key = key.split("_")[0]
            if base_key in merged:
                merged[base_key].extend(value)

        result = {}
        for key, items in merged.items():
            unique_items = list(
                dict.fromkeys(items)
            )  # preserve order, remove duplicates

            if unique_items:
                result[key] = max(unique_items, key=len)

        return result

    @staticmethod
    def __get_title(doc, matched_token_ids: set):
        leftover_tokens = [token.text for i, token in enumerate(doc) if i not in matched_token_ids]
        return " ".join(leftover_tokens).strip()
