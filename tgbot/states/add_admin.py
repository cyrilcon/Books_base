from aiogram.fsm.state import StatesGroup, State


class AddAdmin(StatesGroup):
    """A state class for adding a user to the list of administrators."""

    select_user = State()
