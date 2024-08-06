from aiogram.fsm.state import StatesGroup, State


class Serve(StatesGroup):
    """A class of states for order service."""

    select_booking = State()
    send_book = State()
