from pydantic import BaseModel, Field
from enum import Enum


class Output(BaseModel):
    url: str
    author: str | None
    title: str | None
    year: int | None
    genre: str | None
    summary: str | None


class Genre(str, Enum):
    nonfiction = "nonfiction"
    science_fiction = "science fiction"
    fantasy = "fantasy"
    mystery = "mystery"
    romance = "romance"
    horror = "horror"
    children = "children"
    thriller = "thriller"
    biography = "biography"


class MetaDataPartial(BaseModel):
    author: str = Field(description="The author of the book")
    title: str = Field(description="The title of the book")
    genre: Genre = Field(description="The genre of the book")


class MetaDataSummary(BaseModel):
    summary: str = Field(description="The summary of the book")
