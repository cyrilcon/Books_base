from aiogram.fsm.state import StatesGroup, State


class CancelBooking(StatesGroup):
    """A class of states for order cancellation."""

    select_booking = State()
