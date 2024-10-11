from aiogram.fsm.state import StatesGroup, State


class GetToken(StatesGroup):
    """A class of states for getting token of a photo."""

    send_photo = State()
