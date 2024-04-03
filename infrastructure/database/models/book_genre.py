from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .genre import Genre


class BookGenre(Base):
    __tablename__ = "book_genre"
    __table_args__ = (
        UniqueConstraint(
            "id_book",
            "id_genre",
            name="idx_unique_book_genre",
        ),
    )

    id_book_genre: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(ForeignKey("book.id_book"))
    id_genre: Mapped[int] = mapped_column(ForeignKey("genre.id_genre"))

    book_rel: Mapped["Book"] = relationship(
        back_populates="book_genre_rel",
    )

    genre_rel: Mapped["Genre"] = relationship(
        back_populates="book_genre_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_book_genre={self.id_book_genre}, "
            f"id_book={self.id_book}, "
            f"id_genre={self.id_genre})"
        )

    def __repr__(self):
        return str(self)
