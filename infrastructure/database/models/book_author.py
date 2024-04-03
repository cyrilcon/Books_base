from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .author import Author


class BookAuthor(Base):
    __tablename__ = "book_author"
    __table_args__ = (
        UniqueConstraint(
            "id_book",
            "id_author",
            name="idx_unique_book_author",
        ),
    )

    id_book_author: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(ForeignKey("book.id_book"))
    id_author: Mapped[int] = mapped_column(ForeignKey("author.id_author"))

    book_rel: Mapped["Book"] = relationship(
        back_populates="book_author_rel",
    )

    author_rel: Mapped["Author"] = relationship(
        back_populates="book_author_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_book_author={self.id_book_author}, "
            f"id_book={self.id_book}, "
            f"id_author={self.id_author})"
        )

    def __repr__(self):
        return str(self)
