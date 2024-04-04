from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book_file import BookFile


class File(Base, TableNameMixin):
    id_file: Mapped[int] = mapped_column(primary_key=True)
    format: Mapped[str] = mapped_column(String(10))
    file: Mapped[str] = mapped_column(String(255))

    book_file_rel: Mapped[list["BookFile"]] = relationship(
        back_populates="file_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_file={self.id_file}, "
            f"format={self.format!r}, "
            f"file={self.file!r})"
        )

    def __repr__(self):
        return str(self)
