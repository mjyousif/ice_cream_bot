import os
import langcodes
from translate import Translator
from gtts import gTTS, lang
from models.zao_response import Zao_Response


def get_language_code(language_input):
    """Converts a language name or abbreviation into a standard two-letter language code.

    Args:
        language_input (str): The input language name or abbreviation.

    Returns:
        str: The corresponding two-letter language code, or an empty string if no match is found.
    """

    # Assume that 2 characters inputs are language codes
    if len(language_input) == 2:
        return language_input

    try:
        language = langcodes.find(language_input)
        assert isinstance(language.language, str)
        return language.language
    except LookupError:
        # No matching language was found
        pass

    return ""


def generate_zao_response(language: str):
    """Generates a Zao_Response object containing translated text and audio path for a given language.

    Args:
        language (str): The language for translation.

    Returns:
        Zao_Response: An object with the translated text and audio path.
    """

    language_code = get_language_code(language)

    # Easter egg
    if language == "taiwanese":
        return Zao_Response(text="🇨🇳 🇨🇳  🇨🇳 🇨🇳", audio_path=f"audio/tts-nan.mp3")

    # Check for language support
    supported_languages = lang.tts_langs()
    if language_code not in supported_languages:
        text = f"{language} is not supported"
        return Zao_Response(text=text)

    # Translate the text
    text_to_translate = "Good morning China, now I have ice cream."
    translator = Translator(to_lang=language_code)
    translated_text = translator.translate(text=text_to_translate)

    # Check for existing audio file
    tts_audio = f"audio/tts-{language_code}.mp3"
    if not os.path.isfile(tts_audio):
        # Generate text-to-speech
        tts = gTTS(text=translated_text, lang=language_code)
        tts.save(tts_audio)

    return Zao_Response(text=translated_text, audio_path=tts_audio)
