from aiogram.fsm.state import StatesGroup, State


class RemoveAdmin(StatesGroup):
    """A class of states for demoting an administrator."""

    select_admin = State()
