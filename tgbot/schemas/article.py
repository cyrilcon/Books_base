from datetime import datetime

from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    """
    Base article model with common attributes.
    """

    link: str = Field(..., max_length=255, description="Link to the Telegraph article")
    title: str = Field(..., max_length=255, description="Title of the article")
    language_code: str = Field(
        ..., max_length=3, description="IETF language tag of the article"
    )


class ArticleCreate(ArticleBase):
    """
    Schema for creating a new article.
    """

    pass


class ArticleSchema(BaseModel):
    """
    Detailed article schema.
    """

    id_article: int = Field(..., description="Unique article identifier")
    link: str = Field(..., max_length=255, description="Link to the Telegraph article")
    title: str = Field(..., max_length=255, description="Title of the article")
    language_code: str = Field(
        ..., max_length=3, description="IETF language tag of the article"
    )
    added_datetime: datetime = Field(..., description="Time of article addition")
