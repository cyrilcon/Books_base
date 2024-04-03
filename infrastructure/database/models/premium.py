from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .user import User


class Premium(Base, TableNameMixin):
    id_premium: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id_user"), unique=True)
    reading_limit: Mapped[int | None]
    date_limit: Mapped[datetime | None]

    user_rel: Mapped["User"] = relationship(
        back_populates="premium_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_premium={self.id_premium}, "
            f"id_user={self.id_user})"
        )

    def __repr__(self):
        return str(self)
