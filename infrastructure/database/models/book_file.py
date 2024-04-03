from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .file import File


class BookFile(Base):
    __tablename__ = "book_file"
    __table_args__ = (
        UniqueConstraint(
            "id_book",
            "id_file",
            name="idx_unique_book_file",
        ),
    )

    id_book_file: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(ForeignKey("book.id_book"))
    id_file: Mapped[int] = mapped_column(ForeignKey("file.id_file"))

    book_rel: Mapped["Book"] = relationship(
        back_populates="book_file_rel",
    )

    file_rel: Mapped["File"] = relationship(
        back_populates="book_file_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_book_file={self.id_book_file}, "
            f"id_book={self.id_book}, "
            f"id_file={self.id_file})"
        )

    def __repr__(self):
        return str(self)
