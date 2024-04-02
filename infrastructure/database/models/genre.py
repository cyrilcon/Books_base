from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book_genre import BookGenre


class Genre(Base, TableNameMixin):
    id_genre: Mapped[int] = mapped_column(primary_key=True)
    genre: Mapped[str] = mapped_column(String(255))

    book_genre_rel: Mapped["BookGenre"] = relationship(
        back_populates="genre_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_genre={self.id_genre}, "
            f"genre={self.genre!r})"
        )

    def __repr__(self):
        return str(self)
