from aiogram.fsm.state import StatesGroup, State


class SendMessage(StatesGroup):
    """A class of states for sending a message to the user."""

    select_user = State()
    write_message = State()
