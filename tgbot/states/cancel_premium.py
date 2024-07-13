from aiogram.fsm.state import StatesGroup, State


class CancelPremium(StatesGroup):
    """Класс состояний для отмены статуса Books_base Premium."""

    select_user = State()
