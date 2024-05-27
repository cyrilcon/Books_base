from aiogram.fsm.state import StatesGroup, State


class Support(StatesGroup):
    """Класс состояний для тех-поддержки."""

    message_to_admin = State()
    message_to_user = State()
