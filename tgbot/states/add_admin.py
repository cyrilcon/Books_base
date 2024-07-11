from aiogram.fsm.state import StatesGroup, State


class AddAdmin(StatesGroup):
    """Класс состояний для добавления пользователя в список администраторов."""

    select_user = State()
