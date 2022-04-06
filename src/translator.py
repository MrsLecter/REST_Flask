#!/usr/bin/python3
from deep_translator import GoogleTranslator

# input source_lang, target_lang in format 'en', 'ru' etc.
# output -> translated text
def getTranslation(source_text, source_lang, target_lang):
    text = source_text
    translated = GoogleTranslator(source=(source_lang.lower()), target=(
        target_lang.lower())).translate(text=text)
    return translated
