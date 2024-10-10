from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import find_user, create_user_link, set_user_commands
from tg_bot.states import RemoveAdmin

remove_admin_process_router = Router()


@remove_admin_process_router.message(
    StateFilter(RemoveAdmin.select_admin),
    F.text,
)
async def remove_admin_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    user, response_message = await find_user(l10n, message.text)

    if not user:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
        return

    id_user = user.id_user

    if id_user == message.from_user.id:
        await message.answer(
            l10n.format_value(
                "remove-admin-error-self-remove",
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    user_link = create_user_link(user.full_name, user.username)

    if not user.is_admin:
        await message.answer(
            l10n.format_value(
                "remove-admin-error-user-already-not-admin",
                {"user_link": user_link, "id_user": str(id_user)},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    await api.users.admins.delete_admin(id_user=id_user)
    await set_user_commands(bot=bot, id_user=id_user, is_admin=False)
    await message.answer(
        l10n.format_value(
            "remove-admin-success",
            {"user_link": user_link, "id_user": str(id_user)},
        )
    )
    await state.clear()
