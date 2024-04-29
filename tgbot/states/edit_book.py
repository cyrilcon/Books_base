from aiogram.fsm.state import StatesGroup, State


class EditBook(StatesGroup):
    """Класс состояний для изменения данных о книге."""

    select_book = State()
