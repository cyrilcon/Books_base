from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from api.api_v1.schemas import UserSchema
from tg_bot.keyboards.inline import languages_keyboard
from tg_bot.services.localization import get_fluent_localization

settings_process_router = Router()


@settings_process_router.callback_query(
    F.data.startswith("language"),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def settings_process(
    call: CallbackQuery,
    l10n: FluentLocalization,
    user: UserSchema,
):
    new_language_code = call.data.split(":")[-1]

    if user.language_code == new_language_code:
        await call.answer(
            l10n.format_value("settings-error-language-already-set"),
            show_alert=True,
        )
        return

    response = await api.users.update_user(
        id_user=call.from_user.id,
        language_code=new_language_code,
    )
    user = response.get_model()

    l10n = get_fluent_localization(user.language_code)
    await call.message.edit_text(
        l10n.format_value("settings-success"),
        reply_markup=languages_keyboard(l10n),
    )
    await call.answer()
