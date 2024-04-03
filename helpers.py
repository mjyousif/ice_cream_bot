import langcodes


def get_language_code(language_input):
    # Assume that 2 characters inputs are language codes
    if len(language_input) == 2:
        return language_input

    try:
        language = langcodes.find(language_input)
        return language.language
    except NameError:
        # No matching language was found
        pass

    return ""
