from datetime import datetime

from sqlalchemy import func, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TableNameMixin


class Article(Base, TableNameMixin):
    id_article: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String(255), unique=True)
    title: Mapped[str] = mapped_column(String(255))
    language_code: Mapped[str] = mapped_column(String(3))
    added_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_user={self.id_article}, "
            f"link={self.link!r}, "
            f"title={self.title!r}, "
            f"language_code={self.language_code!r}, "
            f"added_datetime={self.added_datetime!r})"
        )

    def __repr__(self):
        return str(self)
