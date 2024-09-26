from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import find_user, create_user_link, ClearKeyboard
from tg_bot.states import RemoveAdmin

remove_admin_router = Router()


@remove_admin_router.message(Command("remove_admin"))
async def remove_admin(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("remove-admin-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(RemoveAdmin.select_admin)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@remove_admin_router.message(StateFilter(RemoveAdmin.select_admin), F.text)
async def remove_admin_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    user, response_message = await find_user(l10n, message.text)

    if not user:
        sent_message = await message.answer(
            response_message, reply_markup=cancel_keyboard(l10n)
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_user = user.id_user

    if id_user == message.from_user.id:
        sent_message = await message.answer(
            l10n.format_value(
                "remove-admin-error-self-remove",
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    full_name = user.full_name
    username = user.username
    user_link = await create_user_link(full_name, username)

    if not user.is_admin:
        sent_message = await message.answer(
            l10n.format_value(
                "remove-admin-error-already-not-admin",
                {"user_link": user_link, "id_user": str(id_user)},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    await api.users.admins.delete_admin(id_user)
    await message.answer(
        l10n.format_value(
            "remove-admin-success",
            {"user_link": user_link, "id_user": str(id_user)},
        )
    )
    await state.clear()
