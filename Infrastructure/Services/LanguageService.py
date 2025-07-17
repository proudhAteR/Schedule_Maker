from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field
from Core.Models.LanguageMatch import LanguageMatch


class LanguageService:
    def __init__(self):
        self.__matchers: list[Matcher] = [
            matcher() for matcher in Matcher.all_subclasses()
        ]

    def pattern_match(self, sentence: str) -> LanguageMatch:
        data = {}

        for matcher in self.__matchers:
            data.update(
                matcher.match(sentence)
            )

        return LanguageMatch(
            name=data.get(Field.NAME, "").strip(),
            location=data.get(Field.LOCATION, "").strip(),
            start=data.get(Field.START),
            end=data.get(Field.END),
            day_str=data.get(Field.DAY, ""),
            more=data.get(Field.EXTRA, "")
        )
