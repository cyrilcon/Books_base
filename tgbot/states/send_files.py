from aiogram.fsm.state import StatesGroup, State


class SendFiles(StatesGroup):
    """Класс состояний для отправки файлов пользователю."""

    select_user = State()
    load_files = State()
