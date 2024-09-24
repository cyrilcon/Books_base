from aiogram.fsm.state import StatesGroup, State


class GiveBook(StatesGroup):
    """A class of states for giving book."""

    select_user = State()
    select_book = State()
