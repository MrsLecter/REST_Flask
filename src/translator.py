#!/usr/bin/python3
import typing
import deep_translator
from deep_translator import GoogleTranslator

# input source_lang, target_lang in format 'en', 'ru' etc.
# output -> translated text
def getTranslation(source_text: str, source_lang: str, target_lang: str) -> str:
    text = source_text
    translated = GoogleTranslator(source=(source_lang.lower()), target=(
        target_lang.lower())).translate(text=text)
    return translated
