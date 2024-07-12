from aiogram.fsm.state import StatesGroup, State


class RemoveAdmin(StatesGroup):
    """Класс состояний для разжалования администратора."""

    select_admin = State()
