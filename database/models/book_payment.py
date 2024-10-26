from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .book import Book
    from .payment import Payment


class BookPayment(Base, TableNameMixin):
    id_book: Mapped[int] = mapped_column(
        ForeignKey("book.id_book", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    id_payment: Mapped[str] = mapped_column(
        ForeignKey("payment.id_payment"), primary_key=True
    )

    book: Mapped["Book"] = relationship(
        back_populates="payments", cascade="all, delete"
    )
    payment: Mapped["Payment"] = relationship(
        back_populates="books",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_book={self.id_book}, "
            f"id_payment={self.id_payment})"
        )

    def __repr__(self):
        return str(self)
