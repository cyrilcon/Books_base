from aiogram.fsm.state import StatesGroup, State


class Broadcast(StatesGroup):
    """A class of states for broadcasting."""

    write_message = State()
