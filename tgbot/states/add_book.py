from aiogram.fsm.state import StatesGroup, State


class AddBook(StatesGroup):
    """Класс состояний для добавления книги."""

    select_article = State()  # Выбор артикула
