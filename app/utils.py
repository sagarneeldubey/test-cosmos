import re
from .config import GPT_MODEL, OPENAI_API_KEY
from .schema import MetaDataPartial, MetaDataSummary
from openai import OpenAI

client = OpenAI()


def extract_year(text) -> int | None:
    """
    Given the text, finds the literal `pubication date` and extracts the year from it.
    Returns None if not found.
    """
    start_pos = -1
    match_pub = re.search(r"publication date", text, re.IGNORECASE)

    if match_pub:
        start_pos = match_pub.start()

    if start_pos == -1:
        return None

    match_year = re.search(
        r"\b(11\d{2}|12\d{2}|13\d{2}|14\d{2}|15\d{2}|16\d{2}|17\d{2}|18\d{2}|19\d{2}|20\d{2})\b",
        text[start_pos:],
    )

    if match_year:
        return int(match_year.group(1))
    else:
        return None


def extract_metadata_partial(text: str) -> MetaDataPartial:
    completion = client.beta.chat.completions.parse(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Extract author and title, and infer genre from the given text",
            },
            {"role": "user", "content": text},
        ],
        response_format=MetaDataPartial,
    )

    event = completion.choices[0].message.parsed

    return event


def extract_summary(text: str) -> str:
    completion = client.beta.chat.completions.parse(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Create a summary in fewer than 100 words form the given text",
            },
            {"role": "user", "content": text},
        ],
        response_format=MetaDataSummary,
    )

    event = completion.choices[0].message.parsed
    return event
