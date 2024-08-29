from aiogram.fsm.state import StatesGroup, State


class Order(StatesGroup):
    """A class of states for book ordering."""

    book_title = State()
    author_name = State()
