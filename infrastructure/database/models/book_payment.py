from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .payment import Payment


class BookPayment(Base):
    __tablename__ = "book_payment"
    __table_args__ = (
        UniqueConstraint(
            "id_book",
            "id_payment",
            name="idx_unique_book_payment",
        ),
    )

    id_book_payment: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(ForeignKey("book.id_book"))
    id_payment: Mapped[str] = mapped_column(ForeignKey("payment.id_payment"))

    book_rel: Mapped["Book"] = relationship(
        back_populates="book_payment_rel",
    )

    payment_rel: Mapped["Payment"] = relationship(
        back_populates="book_payment_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_book_payment={self.id_book_payment}, "
            f"id_book={self.id_book}, "
            f"id_payment={self.id_payment})"
        )

    def __repr__(self):
        return str(self)
