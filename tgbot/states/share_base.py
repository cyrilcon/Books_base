from aiogram.fsm.state import StatesGroup, State


class ShareBase(StatesGroup):
    """Класс состояний для отправки base пользователю."""

    select_recipient = State()
