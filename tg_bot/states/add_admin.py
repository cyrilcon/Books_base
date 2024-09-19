from aiogram.fsm.state import StatesGroup, State


class AddAdmin(StatesGroup):
    """A class of states adding a user to the list of administrators."""

    select_user = State()
