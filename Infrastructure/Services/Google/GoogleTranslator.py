from deep_translator import GoogleTranslator as Core

from Core.Interface.APIs.TranslationAPI import TranslationAPI


class GoogleTranslator(TranslationAPI):
    def __init__(self):
        super().__init__()

    @staticmethod
    def translate(text: str, to_lang: str = 'en') -> str:
        t = Core(source='auto', target=to_lang)
        return t.translate(text)

    @staticmethod
    def detect_lang(text: str) -> str:
        pass
