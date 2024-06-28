from aiogram.fsm.state import StatesGroup, State


class SendFiles(StatesGroup):
    """Класс состояний для отправки файлов пользователю."""

    select_recipient = State()
    load_files = State()
