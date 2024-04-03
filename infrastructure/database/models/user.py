from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Text, func, BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin

if TYPE_CHECKING:
    from .discount import Discount


class User(Base, TableNameMixin):
    id_user: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    fullname: Mapped[str | None] = mapped_column(Text())
    username: Mapped[str | None] = mapped_column(Text())
    last_activity: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now(),
    )
    registration_date: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # ПОД ВОПРОСОМ
        default=datetime.now(),  # ТРЕБУЕТ ТЕСТА И ПРОВЕРКИ
    )
    base: Mapped[int] = mapped_column(default=0, server_default="0")
    id_discount: Mapped[int] = mapped_column(ForeignKey("discount.id_discount"))

    discount_rel: Mapped["Discount"] = relationship(
        back_populates="user_rel",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_user={self.id_user}, "
            f"fullname={self.fullname!r}, "
            f"username={self.username!r}, "
            f"last_activity={self.last_activity!r}, "
            f"registration_date={self.registration_date!r}, "
            f"base={self.base})"
        )

    def __repr__(self):
        return str(self)
