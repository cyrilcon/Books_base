from aiogram.fsm.state import StatesGroup, State


class DeleteBook(StatesGroup):
    """A class of states for deleting a book."""

    select_book = State()
