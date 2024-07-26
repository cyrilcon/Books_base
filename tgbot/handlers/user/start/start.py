from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from fluent.runtime import FluentLocalization

start_router = Router()


@start_router.message(CommandStart())
async def start(
    message: Message,
    l10n: FluentLocalization,
):
    """
    Processing of the /start command.
    :param message: /start command.
    :param l10n: Language set by the user.
    :return: A welcome message or a found book.
    """

    fullname = message.from_user.full_name
    await message.answer(l10n.format_value("start", {"fullname": fullname}))
