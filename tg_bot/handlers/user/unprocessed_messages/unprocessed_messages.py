from aiogram import Router
from aiogram.types import Message
from fluent.runtime import FluentLocalization

unprocessed_messages_router = Router()


@unprocessed_messages_router.message(
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def unprocessed_messages(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(l10n.format_value("error-unprocessed-messages"))
