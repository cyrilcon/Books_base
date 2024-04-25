from aiogram.fsm.state import StatesGroup, State


class DeleteBook(StatesGroup):
    """Класс состояний для удаления книги."""

    delete_book = State()
