from aiogram.fsm.state import StatesGroup, State


class Booking(StatesGroup):
    """A class of states for book ordering."""

    send_title = State()
    send_author = State()
