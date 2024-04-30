from aiogram.fsm.state import StatesGroup, State


class EditBook(StatesGroup):
    """Класс состояний для изменения данных о книге."""

    select_book = State()
    edit_article = State()
    edit_title = State()
    edit_authors = State()
    edit_description = State()
    edit_genres = State()
    edit_cover = State()
    edit_files = State()
    edit_price = State()
