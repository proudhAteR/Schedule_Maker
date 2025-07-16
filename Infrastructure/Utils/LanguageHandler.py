import re

import dateparser


class LanguageHandler:

    def pattern_match(self, sentence: str) -> tuple:
        sentence = sentence.strip()

        day_str, start, end = self.__temporal_match(sentence)

        by_match = re.search(r"by (.+)", sentence)
        more = by_match.group(1).strip() if by_match else ""

        name = sentence.split(" in ")[0].split(" from ")[0].split(" on ")[0]
        location_match = re.search(r"in (.*?) from", sentence)
        location = location_match.group(1).strip() if location_match else ""

        return name.strip(), location, start, end, day_str, more

    @staticmethod
    def __temporal_match(sentence: str):
        recurrence_match = re.search(r"every (\w+)", sentence, re.IGNORECASE)
        day_str = recurrence_match.group(1).strip() if recurrence_match else ""

        time_phrases = re.findall(r"from (.*?) to (.*?)(?= |$)", sentence)
        if not time_phrases:
            start = dateparser.parse(sentence)
            return day_str, start, start

        start_raw, end_raw = time_phrases[0]

        if day_str:
            start = dateparser.parse(f"{day_str} at {start_raw}")
            end = dateparser.parse(f"{day_str} at {end_raw}")
        else:
            start = dateparser.parse(start_raw)
            end = dateparser.parse(end_raw)

        return day_str, start, end
