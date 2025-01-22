from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, CheckConstraint, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base, TableNameMixin

if TYPE_CHECKING:
    from .user import User


class Discount(Base, TableNameMixin):
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id_user"), primary_key=True)
    discount_value: Mapped[int] = mapped_column(
        CheckConstraint(
            "discount_value IN (15, 30, 50, 100)", name="check_discount_values"
        )
    )
    received_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="discount",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_user={self.id_user}, "
            f"discount_value={self.discount_value}, "
            f"received_datetime={self.received_datetime!r})"
        )

    def __repr__(self):
        return str(self)
