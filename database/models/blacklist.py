from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .user import User


class Blacklist(Base, TableNameMixin):
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id_user"), primary_key=True)
    added_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=datetime.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="blacklist",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_user={self.id_user}, "
            f"added_datetime={self.added_datetime!r})"
        )

    def __repr__(self):
        return str(self)
