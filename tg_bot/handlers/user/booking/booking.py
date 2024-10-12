from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

command_booking_router = Router()


@command_booking_router.message(Command("booking"))
async def booking(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(l10n.format_value("booking"))
