from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import find_user, create_user_link, ClearKeyboard
from tg_bot.states import AddBlacklist

add_blacklist_router = Router()


@add_blacklist_router.message(Command("add_blacklist"))
async def add_blacklist(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("add-blacklist-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddBlacklist.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_blacklist_router.message(
    StateFilter(AddBlacklist.select_user),
    F.text,
)
async def add_blacklist_process(
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
    user_link = await create_user_link(user.full_name, user.username)

    if user.is_blacklisted:
        sent_message = await message.answer(
            l10n.format_value(
                "add-blacklist-error-user-already-blacklisted",
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

    await api.users.blacklist.create_blacklist(id_user=id_user)
    await message.answer(
        l10n.format_value(
            "add-blacklist-success",
            {"user_link": user_link, "id_user": str(id_user)},
        )
    )
    await state.clear()
