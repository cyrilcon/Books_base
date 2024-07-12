from aiogram.fsm.state import StatesGroup, State


class GivePremium(StatesGroup):
    """Класс состояний для выдачи статуса Books_base Premium."""

    select_user = State()
