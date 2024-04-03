from typing import TYPE_CHECKING

from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book_author import BookAuthor
    from .book_genre import BookGenre
    from .book_file import BookFile


class Book(Base, TableNameMixin):
    id_book: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(255))
    cover: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())
    price: Mapped[int]

    book_author_rel: Mapped[list["BookAuthor"]] = relationship(
        back_populates="book_rel",
    )

    book_genre_rel: Mapped[list["BookGenre"]] = relationship(
        back_populates="book_rel",
    )

    book_file_rel: Mapped[list["BookFile"]] = relationship(
        back_populates="book_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_book={self.id_book}, "
            f"name={self.name!r}, "
            f"cover={self.cover!r}, "
            f"description={self.description!r}, "
            f"price={self.price})"
        )

    def __repr__(self):
        return str(self)
