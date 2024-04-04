from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .payment import Payment


class UserPayment(Base):
    __tablename__ = "user_payment"
    __table_args__ = (
        UniqueConstraint(
            "id_user",
            "id_payment",
            name="idx_unique_user_payment",
        ),
    )

    id_user_payment: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id_user"))
    id_payment: Mapped[int] = mapped_column(ForeignKey("payment.id_payment"))

    user_rel: Mapped["User"] = relationship(
        back_populates="user_payment_rel",
    )

    payment_rel: Mapped["Payment"] = relationship(
        back_populates="user_payment_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_user_payment={self.id_user_payment}, "
            f"id_user={self.id_user}, "
            f"id_payment={self.id_payment})"
        )

    def __repr__(self):
        return str(self)
