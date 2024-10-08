import logging
from fastapi import FastAPI
from typing import Dict
from .config import (
    LOG_LEVEL,
    YEAR_CHAR_CUTOFF,
    PARTIAL_CHAR_CUTOFF,
    SUMMARY_CHAR_CUTOFF,
    DATA_URL,
)
from .schema import Output
from .utils import extract_metadata_partial, extract_summary, extract_year
import polars as pl
import pandas as pd

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger("structured")
logging.getLogger("structured").setLevel(LOG_LEVEL)

app = FastAPI()


@app.get("/meta-data")
def meta_data(url: str) -> Output | None:
    if not url:
        return None

    df = pl.read_parquet(DATA_URL)
    df_filtered = df.filter(pl.col("url").str.contains(url.lower().strip()))

    if not len(df_filtered):
        return None

    url_text = df_filtered.select("url").to_series().to_list()[0]
    text = df_filtered.select("text").to_series().to_list()[0]
    year = extract_year(text[-YEAR_CHAR_CUTOFF:])
    meta_data_partial = extract_metadata_partial(text[:PARTIAL_CHAR_CUTOFF])
    summary = extract_summary(text[:SUMMARY_CHAR_CUTOFF]).summary

    return Output(
        url=url_text,
        author=meta_data_partial.author,
        title=meta_data_partial.title,
        year=year,
        genre=meta_data_partial.genre,
        summary=summary,
    )
