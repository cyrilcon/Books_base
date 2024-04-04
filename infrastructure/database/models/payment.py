from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DECIMAL, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .user_payment import UserPayment


class Payment(Base, TableNameMixin):
    id_payment: Mapped[str] = mapped_column(String(255), primary_key=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    date_payment: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now(),
    )

    user_payment_rel: Mapped[list["UserPayment"]] = relationship(
        back_populates="payment_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_payment={self.id_payment}, "
            f"price={self.price}, "
            f"date_payment={self.date_payment!r})"
        )

    def __repr__(self):
        return str(self)
