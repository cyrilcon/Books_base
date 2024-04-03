from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .user import User


class Discount(Base, TableNameMixin):
    id_discount: Mapped[int] = mapped_column(primary_key=True)
    discount: Mapped[int]

    user_rel: Mapped[list["User"]] = relationship(
        back_populates="discount_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_discount={self.id_discount}, "
            f"discount={self.discount})"
        )

    def __repr__(self):
        return str(self)
