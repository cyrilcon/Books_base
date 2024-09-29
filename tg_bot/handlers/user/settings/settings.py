from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.services import get_fluent_localization, ClearKeyboard
from .keyboards import languages_keyboard

settings_router = Router()


@settings_router.message(Command("settings"))
async def settings(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)
    await state.clear()

    await message.answer(
        l10n.format_value("settings"),
        reply_markup=languages_keyboard(l10n),
    )


@settings_router.callback_query(F.data.startswith("set_language"))
async def settings_set_language(call: CallbackQuery, l10n: FluentLocalization):
    new_language_code = call.data.split(":")[-1]

    id_user = call.from_user.id
    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    if user.language_code == new_language_code:
        await call.answer(
            l10n.format_value("settings-error-language-already-set"),
            show_alert=True,
        )
        return

    response = await api.users.update_user(
        id_user=id_user,
        language_code=new_language_code,
    )
    user = response.get_model()
    l10n = get_fluent_localization(user.language_code)

    await call.message.edit_text(
        l10n.format_value("settings-success"),
        reply_markup=languages_keyboard(l10n),
    )
    await call.answer()
