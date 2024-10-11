from aiogram.fsm.state import StatesGroup, State


class TestBroadcast(StatesGroup):
    """A class of states for test broadcasting."""

    write_message = State()
