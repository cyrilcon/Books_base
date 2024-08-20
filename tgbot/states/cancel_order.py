from aiogram.fsm.state import StatesGroup, State


class CancelOrder(StatesGroup):
    """A class of states for order cancellation."""

    select_order = State()
