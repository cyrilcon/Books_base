from aiogram.fsm.state import StatesGroup, State


class AddBook(StatesGroup):
    """A class of states for adding a book."""

    select_article = State()
    add_title = State()
    add_authors = State()
    add_description = State()
    add_genres = State()
    add_cover = State()
    add_files = State()
    select_price = State()
    reduce_description = State()
    preview = State()
