from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import languages_keyboard
from tgbot.services import get_user_language

settings_router = Router()


@settings_router.message(Command("settings"))
async def settings(message: Message, l10n: FluentLocalization):
    await message.answer(
        l10n.format_value("settings"),
        reply_markup=languages_keyboard(l10n),
    )


@settings_router.callback_query(F.data.startswith("language"))
async def settings_set_language(
    call: CallbackQuery,
    l10n: FluentLocalization,
):
    id_user = call.from_user.id
    response = await api.users.get_user_by_id(id_user)
    user = response.result

    user_language_code = user["language"]
    new_language_code = call.data.split(":")[-1]

    if user_language_code != new_language_code:
        await call.answer(cache_time=1)

        await api.users.update_user(id_user, language=new_language_code)
        l10n = await get_user_language(id_user)

        await call.message.edit_text(
            l10n.format_value("settings-success"),
            reply_markup=languages_keyboard(l10n),
        )
    else:
        await call.answer(l10n.format_value("settings-error"), show_alert=True)
