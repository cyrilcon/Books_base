from aiogram.fsm.state import StatesGroup, State


class AddBlacklist(StatesGroup):
    """Класс состояний для добавления пользователя в чёрный список."""

    select_user = State()
