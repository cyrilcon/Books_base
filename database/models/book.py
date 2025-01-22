from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Text, String, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book_author import BookAuthor
    from .book_genre import BookGenre
    from .book_file import BookFile
    from .book_payment import BookPayment


class Book(Base, TableNameMixin):
    id_book: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text())
    cover: Mapped[str] = mapped_column(String(255), unique=True)
    price: Mapped[int]
    added_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    authors: Mapped[list["BookAuthor"]] = relationship(
        back_populates="book",
        cascade="all, delete",
        passive_deletes=True,
    )
    genres: Mapped[list["BookGenre"]] = relationship(
        back_populates="book",
        cascade="all, delete",
        passive_deletes=True,
    )
    files: Mapped[list["BookFile"]] = relationship(
        back_populates="book",
        cascade="all, delete",
        passive_deletes=True,
    )
    payments: Mapped[list["BookPayment"]] = relationship(
        back_populates="book",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_book={self.id_book}, "
            f"title={self.title!r}, "
            f"cover={self.cover!r}, "
            f"description={self.description!r}, "
            f"price={self.price}, "
            f"added_datetime={self.added_datetime!r})"
        )

    def __repr__(self):
        return str(self)
