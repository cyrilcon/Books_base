from aiogram.fsm.state import StatesGroup, State


class AddBook(StatesGroup):
    """Класс состояний для добавления книги."""

    select_article = State()  # Артикула
    add_title = State()  # Название книги
    add_authors = State()  # Авторы
    add_description = State()  # Описание
    add_genres = State()  # Жанры
    add_cover = State()  # Обложка
