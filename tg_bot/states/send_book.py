from aiogram.fsm.state import StatesGroup, State


class SendBook(StatesGroup):
    """A class of states for sending a book to the user."""

    select_user = State()
    select_book = State()
