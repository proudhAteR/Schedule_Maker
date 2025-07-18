from langdetect import detect, LangDetectException

from Core.Interface.APIs.TranslationAPI import TranslationAPI
from deep_translator import GoogleTranslator as Core


class GoogleTranslator(TranslationAPI):
    def __init__(self):
        super().__init__()

    @staticmethod
    def translate(text: str, from_lang: str, to_lang: str = 'en') -> str:
        t = Core(source=from_lang, target=to_lang)
        return t.translate(text)

    @staticmethod
    def detect_lang(text: str) -> str:
        try:
            return detect(text)
        except LangDetectException as e:
            raise KeyError(f"The language cannot be detected. Cause: {e}")
