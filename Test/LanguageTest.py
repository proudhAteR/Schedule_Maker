import pytest

from Infrastructure.Services.Language.LanguageService import LanguageService, language_factory


@pytest.mark.parametrize("sentence, expected_time, expected_location_contains, expected_title_contains", [
    ("Piano Lesson in Music Room from 16 to 17 every Sunday by Mr. Bennett",
     "from 16 to 17 every sunday", "in music room", "piano lesson"),

    ("Internship Info Session in Lecture Hall from 10:00 to 11:15 every Thursday by HR Rep",
     "from 10:00 to 11:15 every thursday", "in lecture hall", "internship info session"),

    ("Running in the park from 7 to 8 am on Sunday with Coach Mike",
     "from 7 to 8 am on sunday", "in the park", "running"),

    ("Dance class 9:00 - 10:30 every Wednesday with Emily",
     "9:00-10:30 every wednesday", "", "dance class"),

    ("Réunion d’équipe dans le 4B de 9h à 9h45 chaque lundi avec Marc",
     "from 9 a.m. to 9:45 a.m. every monday", "in 4b", "team meeting"),

    ("Atelier cuisine 17:00-19:15 chaque samedi par le Chef Louis",
     "17:00-19:15 every saturday", "", "kitchen workshop")
])
@pytest.mark.asyncio
async def test_processor(sentence: str, expected_time: str, expected_location_contains: str,
                         expected_title_contains: str):
    service = await language_factory()
    result = await service._process(sentence)

    time_val = result.get("time", "").lower()
    location_val = result.get("location", "").lower()
    title_val = result.get("title", "").lower()

    assert expected_time == time_val, f"Expected time snippet '{expected_time}' in '{time_val}'"

    if expected_location_contains:
        assert expected_location_contains == location_val, f"Expected location snippet '{expected_location_contains}' in '{location_val}'"

    assert expected_title_contains == title_val, f"Expected title snippet '{expected_title_contains}' in '{title_val}'"
