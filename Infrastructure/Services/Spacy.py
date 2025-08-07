from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.tokens.doc import Doc

import Infrastructure.Utils.Helpers.Imports as Imp
from Core.Interface.Tokenizer import Tokenizer
from Infrastructure.Utils.Helpers.spacy_patterns import *


class Spacy(Tokenizer):

    def __init__(self, model: str = "en_core_web_sm"):
        self.core = Imp.load_spacy_model(model)
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
        return self.__process_output(doc)

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
            )

            if unique_items:
                result[key] = max(unique_items, key=len)

        return result

    @staticmethod
    def __get_title(doc, matched_token_ids: set):
        leftover_tokens = [token.text for i, token in enumerate(doc) if i not in matched_token_ids]
        return " ".join(leftover_tokens).strip()
