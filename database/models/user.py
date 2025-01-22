from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, BIGINT, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base, TableNameMixin

if TYPE_CHECKING:
    from .admin import Admin
    from .blacklist import Blacklist
    from .discount import Discount
    from .order import Order
    from .payment import Payment
    from .premium import Premium


class User(Base, TableNameMixin):
    id_user: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    full_name: Mapped[str | None] = mapped_column(String(225), index=True)
    username: Mapped[str | None] = mapped_column(String(32), unique=True)
    language_code: Mapped[str] = mapped_column(String(10))
    registration_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    last_activity_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    base_balance: Mapped[int] = mapped_column(default=0, server_default="0")
    referrer_id: Mapped[int | None] = mapped_column(default=None, server_default=None)

    admin: Mapped["Admin"] = relationship(
        back_populates="user",
    )
    blacklist: Mapped["Blacklist"] = relationship(
        back_populates="user",
    )
    discount: Mapped["Discount"] = relationship(
        back_populates="user",
    )
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
    )
    payments: Mapped[list["Payment"]] = relationship(
        back_populates="user",
    )
    premium: Mapped["Premium"] = relationship(
        back_populates="user",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id_user={self.id_user}, "
            f"full_name={self.full_name!r}, "
            f"username={self.username!r}, "
            f"language_code={self.language_code!r}, "
            f"registration_datetime={self.registration_datetime!r}, "
            f"last_activity_datetime={self.last_activity_datetime!r}, "
            f"base_balance={self.base_balance}, "
            f"referrer_id={self.referrer_id})"
        )

    def __repr__(self):
        return str(self)
