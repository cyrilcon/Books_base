from enum import Enum


class SearchBy(str, Enum):
    AUTHOR: str = "author"
    TITLE: str = "title"
    GENRE: str = "genre"
