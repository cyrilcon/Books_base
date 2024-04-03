from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .booking import Booking


class UserBooking(Base):
    __tablename__ = "user_booking"
    __table_args__ = (
        UniqueConstraint(
            "id_user",
            "id_booking",
            name="idx_unique_user_booking",
        ),
    )

    id_user_booking: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id_user"))
    id_booking: Mapped[int] = mapped_column(ForeignKey("booking.id_booking"))

    user_rel: Mapped["User"] = relationship(
        back_populates="user_booking_rel",
    )

    booking_rel: Mapped["Booking"] = relationship(
        back_populates="user_booking_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_user_booking={self.id_user_booking}, "
            f"id_user={self.id_user}, "
            f"id_booking={self.id_booking})"
        )

    def __repr__(self):
        return str(self)
