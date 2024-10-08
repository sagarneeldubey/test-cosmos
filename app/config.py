import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATA_URL = (
    "hf://datasets/AlekseyKorshuk/fiction-books/data/train-00000-of-00001.parquet"
)
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o-mini")
YEAR_CHAR_CUTOFF = 125
PARTIAL_CHAR_CUTOFF = 1000
SUMMARY_CHAR_CUTOFF = 5000
