from aiogram.fsm.state import StatesGroup, State


class Refund(StatesGroup):
    """A class of states for refunding."""

    select_payment = State()
