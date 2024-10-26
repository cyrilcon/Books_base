from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book import Book
    from .genre import Genre


class BookGenre(Base, TableNameMixin):
    id_book: Mapped[int] = mapped_column(
        ForeignKey("book.id_book", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    id_genre: Mapped[int] = mapped_column(
        ForeignKey("genre.id_genre"), primary_key=True
    )

    book: Mapped["Book"] = relationship(
        back_populates="genres",
    )
    genre: Mapped["Genre"] = relationship(
        back_populates="books",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_book={self.id_book}, "
            f"id_genre={self.id_genre})"
        )

    def __repr__(self):
        return str(self)
