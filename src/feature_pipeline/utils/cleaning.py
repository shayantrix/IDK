import re

from unstructured.cleaners.core import (
    clean,
    clean_non_ascii_chars,
    replace_unicode_quotes,
)


def remove_whitespace(text):
    text = text.strip()
    return text


def unbold_text(text):
    # Mapping of bold numbers to their regular equivalents
    bold_numbers = {
        "𝟬": "0",
        "𝟭": "1",
        "𝟮": "2",
        "𝟯": "3",
        "𝟰": "4",
        "𝟱": "5",
        "𝟲": "6",
        "𝟳": "7",
        "𝟴": "8",
        "𝟵": "9",
    }

    # Function to convert bold characters (letters and numbers)
    def convert_bold_char(match):
        char = match.group(0)
        # Convert bold numbers
        if char in bold_numbers:
            return bold_numbers[char]
        # Convert bold uppercase letters
        elif "\U0001d5d4" <= char <= "\U0001d5ed":
            return chr(ord(char) - 0x1D5D4 + ord("A"))
        # Convert bold lowercase letters
        elif "\U0001d5ee" <= char <= "\U0001d607":
            return chr(ord(char) - 0x1D5EE + ord("a"))
        else:
            return char  # Return the character unchanged if it's not a bold number or letter

    # Regex for bold characters (numbers, uppercase, and lowercase letters)
    bold_pattern = re.compile(
        r"[\U0001D5D4-\U0001D5ED\U0001D5EE-\U0001D607\U0001D7CE-\U0001D7FF]"
    )
    text = bold_pattern.sub(convert_bold_char, text)

    return text

def unitalic_text(text):
    def convert_italic_char(match):
        char = match.group(0)
        # unicode range for italic letters
        if "\U0001d608" <= char <= "\U0001d621":
            return chr(ord(char) - 0x1D608 + ord("A"))
        elif "\U0001d622" <= char <= "\U0001d63b":
            return chr(ord(char) - 0x1D622 + ord("a"))
        else:
            return char
    # Regex for italic characters (uppercase and lowercase letters)
    italic_pattern = re.compile(
        r"[\U0001D608-\U0001D621\U0001D622-\U0001D63B]"
    )
    text = italic_pattern.sub(convert_italic_char, text)
    return text


def clean_text(text_content: str | None) -> str:
    if text_content is None:
        return ""

    cleaned_text = remove_whitespace(text_content)
    cleaned_text = unbold_text(text_content)
    cleaned_text = unitalic_text(cleaned_text)
    cleaned_text = clean(cleaned_text)
    cleaned_text = replace_unicode_quotes(cleaned_text)

    return cleaned_text
