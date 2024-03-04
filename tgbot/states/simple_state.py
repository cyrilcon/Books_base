from aiogram.fsm.state import StatesGroup, State


class Simple(StatesGroup):
    """Класс состояний для простого состояния."""

    simple_state = State()  # Простое состояние
