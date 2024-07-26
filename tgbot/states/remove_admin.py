from aiogram.fsm.state import StatesGroup, State


class RemoveAdmin(StatesGroup):
    """A state class for demoting an administrator."""

    select_admin = State()
