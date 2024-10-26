from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book import Book
    from .author import Author


class BookAuthor(Base, TableNameMixin):
    id_book: Mapped[int] = mapped_column(
        ForeignKey("book.id_book", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    id_author: Mapped[int] = mapped_column(
        ForeignKey("author.id_author"), primary_key=True
    )

    book: Mapped["Book"] = relationship(
        back_populates="authors",
    )
    author: Mapped["Author"] = relationship(
        back_populates="books",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_book={self.id_book}, "
            f"id_author={self.id_author})"
        )

    def __repr__(self):
        return str(self)
