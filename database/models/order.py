from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, String, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .user import User


class Order(Base, TableNameMixin):
    id_order: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id_user"))
    book_title: Mapped[str] = mapped_column(String(255))
    author_name: Mapped[str] = mapped_column(String(255))
    order_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(back_populates="orders")

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_order={self.id_order}, "
            f"id_user={self.id_user}, "
            f"book_title={self.book_title!r}, "
            f"author_name={self.author_name!r}, "
            f"order_datetime={self.order_datetime!r})"
        )

    def __repr__(self):
        return str(self)
