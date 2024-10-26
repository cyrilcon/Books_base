from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .user import User
    from .payment import Payment


class Premium(Base, TableNameMixin):
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id_user"), primary_key=True)
    id_payment: Mapped[str | None] = mapped_column(
        ForeignKey("payment.id_payment"), nullable=True
    )
    received_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=datetime.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="premium",
    )
    payment: Mapped["Payment"] = relationship(
        back_populates="premium",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_user={self.id_user}, "
            f"id_payment={self.id_payment}, "
            f"received_datetime={self.received_datetime!r})"
        )

    def __repr__(self):
        return str(self)
