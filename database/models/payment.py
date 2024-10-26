from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DECIMAL, func, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .user import User
    from .book_payment import BookPayment
    from .premium import Premium


class Payment(Base, TableNameMixin):
    id_payment: Mapped[str] = mapped_column(String(255), primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id_user"))
    price: Mapped[int]
    currency: Mapped[str] = mapped_column(
        String(3),
        CheckConstraint("currency IN ('XTR', 'RUB')", name="check_currency_values"),
    )
    payment_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=datetime.now(),
    )

    user: Mapped[list["User"]] = relationship(
        back_populates="payments",
    )
    books: Mapped[list["BookPayment"]] = relationship(
        back_populates="payment",
    )
    premium: Mapped["Premium"] = relationship(
        back_populates="payment",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_payment={self.id_payment}, "
            f"id_user={self.id_user}, "
            f"price={self.price}, "
            f"currency={self.currency!r}, "
            f"payment_datetime={self.payment_datetime!r})"
        )

    def __repr__(self):
        return str(self)
