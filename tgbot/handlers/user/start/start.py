from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.services import ClearKeyboard

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message, l10n: FluentLocalization, storage: RedisStorage):
    """
    Processing of the /start command.
    :param message: /start command.
    :param l10n: Language set by the user.
    :param storage: Storage for FSM.
    :return: A welcome message or a found book.
    """

    await ClearKeyboard.clear(message, storage)

    fullname = message.from_user.full_name
    await message.answer(l10n.format_value("start", {"fullname": fullname}))
