import re
import html
import unicodedata
import pandas as pd


def clean_customer_text(text):
    """
    Conservative cleaning for AppleSupport customer tweets.

    Keeps:
    - technical terms
    - numbers
    - product names
    - error messages
    - hashtags as words

    Removes:
    - URLs
    - @mentions
    - emojis / symbols
    - unnecessary Unicode artifacts
    - excessive whitespace
    """

    if pd.isna(text):
        return ""

    text = str(text)

    # Decode HTML entities
    text = html.unescape(text)

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # Remove @mentions
    text = re.sub(
        r"@\w+",
        " ",
        text
    )

    # Keep hashtag word, remove '#'
    text = re.sub(
        r"#(\w+)",
        r"\1",
        text
    )

    # Unicode normalization
    text = unicodedata.normalize(
        "NFKC",
        text
    )

    # Remove variation selectors and zero-width characters
    text = re.sub(
        r"[\u200b-\u200f\u202a-\u202e\ufeff\ufe0e\ufe0f]",
        "",
        text
    )

    # Remove emoji / symbol characters
    cleaned_chars = []

    for char in text:
        category = unicodedata.category(char)

        if category.startswith("So"):
            continue

        if category.startswith("Sk"):
            continue

        cleaned_chars.append(char)

    text = "".join(cleaned_chars)

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def add_clean_text(df):
    """
    Add text_raw and text_clean columns.
    """

    df = df.copy()

    df["text_raw"] = (
        df["text"]
        .fillna("")
        .astype(str)
    )

    df["text_clean"] = (
        df["text_raw"]
        .apply(clean_customer_text)
    )

    return df