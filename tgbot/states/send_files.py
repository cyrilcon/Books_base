from aiogram.fsm.state import StatesGroup, State


class SendFiles(StatesGroup):
    """A class of states for sending files to the user."""

    select_user = State()
    upload_files = State()
    write_caption = State()
