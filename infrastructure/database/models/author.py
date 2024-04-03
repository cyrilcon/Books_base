from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book_author import BookAuthor


class Author(Base, TableNameMixin):
    id_author: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(255))

    book_author_rel: Mapped[list["BookAuthor"]] = relationship(
        back_populates="author_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_author={self.id_author}, "
            f"author={self.author!r})"
        )

    def __repr__(self):
        return str(self)
