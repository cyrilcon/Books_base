from aiogram.fsm.state import StatesGroup, State


class RemoveFromBlacklist(StatesGroup):
    """Класс состояний для удаления пользователя из чёрного списка."""

    select_user = State()
