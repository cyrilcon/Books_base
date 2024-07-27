from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter
from tgbot.services import ClearKeyboard

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("admin"))
async def admin(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    """
    Processing of the /admin command.
    :param message: /admin command.
    :param l10n: Language set by the user.
    :param state: FSM (For emergency discharge).
    :param storage: Storage for FSM.
    :return: A message with commands for the administrator.
    """

    await ClearKeyboard.clear(message, storage)

    await message.answer(l10n.format_value("admin-commands"))
    await state.clear()
