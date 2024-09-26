from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import find_user, create_user_link, ClearKeyboard
from tg_bot.states import RemoveBlacklist

remove_blacklist_router = Router()


@remove_blacklist_router.message(Command("remove_blacklist"))
async def remove_blacklist(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("remove-blacklist-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(RemoveBlacklist.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@remove_blacklist_router.message(StateFilter(RemoveBlacklist.select_user), F.text)
async def remove_blacklist_process(
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
    full_name = user.full_name
    username = user.username
    user_link = await create_user_link(full_name, username)

    if not user.is_blacklisted:
        sent_message = await message.answer(
            l10n.format_value(
                "remove-blacklist-error-already-removed",
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

    await api.users.blacklist.delete_blacklist(id_user)
    await message.answer(
        l10n.format_value(
            "remove-blacklist-success",
            {"user_link": user_link, "id_user": str(id_user)},
        )
    )
    await state.clear()
