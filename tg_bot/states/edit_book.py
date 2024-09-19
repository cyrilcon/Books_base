from aiogram.fsm.state import StatesGroup, State


class EditBook(StatesGroup):
    """A class of states for changing book data."""

    select_book = State()
    edit_article = State()
    edit_title = State()
    edit_authors = State()
    edit_description = State()
    edit_genres = State()
    edit_cover = State()
    edit_files = State()
