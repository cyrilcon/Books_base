from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book_author import BookAuthor


class Author(Base, TableNameMixin):
    id_author: Mapped[int] = mapped_column(primary_key=True)
    author_name: Mapped[str] = mapped_column(String(255), unique=True)

    books: Mapped[list["BookAuthor"]] = relationship(
        back_populates="author",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_author={self.id_author}, "
            f"author_name={self.author_name!r})"
        )

    def __repr__(self):
        return str(self)
