from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book_genre import BookGenre


class Genre(Base, TableNameMixin):
    id_genre: Mapped[int] = mapped_column(primary_key=True)
    genre_name: Mapped[str] = mapped_column(String(255), unique=True)

    books: Mapped[list["BookGenre"]] = relationship(
        back_populates="genre",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_genre={self.id_genre}, "
            f"genre_name={self.genre_name!r})"
        )

    def __repr__(self):
        return str(self)
