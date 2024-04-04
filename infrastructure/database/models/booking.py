from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .user_booking import UserBooking


class Booking(Base, TableNameMixin):
    id_booking: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    author: Mapped[str] = mapped_column(String(255))
    name_book: Mapped[str] = mapped_column(String(255))
    booking_date: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now(),
    )

    user_booking_rel: Mapped[list["UserBooking"]] = relationship(
        back_populates="booking_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_booking={self.id_booking}, "
            f"author={self.author!r}, "
            f"name_book={self.name_book!r}, "
            f"booking_date={self.booking_date!r})"
        )

    def __repr__(self):
        return str(self)
