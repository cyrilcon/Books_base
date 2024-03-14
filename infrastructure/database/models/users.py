import datetime
from typing import Optional

from sqlalchemy import String, BIGINT
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base, TimestampMixin, TableNameMixin


class Telegram_Chat(Base, TimestampMixin, TableNameMixin):
    """
    Описание таблицы Telegram_Chat.

    Attributes:
        id_chat (Mapped[int]): id чата.
        group_name (Mapped[Optional[str]]): Название группы.
        activity (Mapped[datetime]): Время последнего использования бота.
        schedule_time (Mapped[Optional[str]]): Время автоматической отправки расписания.

    Methods:
        __repr__(): Возвращает строковое представление объекта Chat_Group_Telegram.

    Inherited Attributes:
        Наследует классы Base, TimestampMixin и TableNameMixin, которые предоставляют дополнительные атрибуты и функциональность.

    Inherited Methods:
        Наследует методы классов Base, TimestampMixin и TableNameMixin,
        которые предоставляют дополнительную функциональность.

    """

    # """
    # CREATE TABLE IF NOT EXISTS Chat_Group_Telegram(
    # id_chat TEXT NOT NULL,
    # group_name VARCHAR(20) NOT NULL,
    # recent_use TIMESTAMP(0) NOT NULL,
    # schedule_time VARCHAR(5),
    # PRIMARY KEY (id_chat));
    # """

    id_chat: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    group_name: Mapped[Optional[str]] = mapped_column(String(20))
    activity: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), nullable=False
    )
    schedule_time: Mapped[Optional[str]] = mapped_column(String(5))

    def __repr__(self):
        return f"<Chat_Group_Telegram {self.id_chat} {self.group_name} {self.activity} {self.schedule_time}>"
