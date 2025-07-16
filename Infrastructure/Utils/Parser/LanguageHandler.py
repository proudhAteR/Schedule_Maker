import re

from Infrastructure.Utils.Parser.Matcher.ExtraMatcher import ExtraMatcher
from Infrastructure.Utils.Parser.Matcher.LocationMatcher import LocationMatcher
from Infrastructure.Utils.Parser.Matcher.TemporalMatcher import TemporalMatcher
from Infrastructure.Utils.Parser.Matcher.TitleMatcher import TitleMatcher


class LanguageHandler:

    def __init__(self):
        self.__l_matcher = LocationMatcher()
        self.__e_matcher = ExtraMatcher()
        self.__n_matcher = TitleMatcher()
        self.__t_matcher = TemporalMatcher()

    def pattern_match(self, sentence: str) -> tuple:
        day_str, start, end = self.__t_matcher.match(sentence)
        extra = self.__e_matcher.match(sentence)
        name = self.__n_matcher.match(sentence)
        location = self.__l_matcher.match(sentence)

        return name, location, start, end, day_str, extra
