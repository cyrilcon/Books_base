from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book_file import BookFile


class File(Base, TableNameMixin):
    id_file: Mapped[int] = mapped_column(primary_key=True)
    format: Mapped[str] = mapped_column(String(10))
    file_token: Mapped[str] = mapped_column(String(255), unique=True)

    books: Mapped[list["BookFile"]] = relationship(
        back_populates="file",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_file={self.id_file}, "
            f"format={self.format!r}, "
            f"file_token={self.file_token!r})"
        )

    def __repr__(self):
        return str(self)
