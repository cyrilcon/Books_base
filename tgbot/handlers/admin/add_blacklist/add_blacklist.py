from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import find_user, create_user_link, ClearKeyboard
from tgbot.states import AddBlacklist

add_blacklist_router = Router()
add_blacklist_router.message.filter(AdminFilter())


@add_blacklist_router.message(Command("add_blacklist"))
async def add_blacklist(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    """
    Processing of the /add_blacklist command.
    :param message: /add_blacklist command.
    :param l10n: Language set by the user.
    :param state: FSM (AddBlacklist).
    :param storage: Storage for FSM.
    :return: Message to add a user to the blacklist and go to FSM (AddBlacklist).
    """

    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("add-blacklist-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddBlacklist.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_blacklist_router.message(StateFilter(AddBlacklist.select_user), F.text)
async def add_blacklist_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    """
    Selects a user to add to the blacklist.
    :param message: A message with the expected username or user ID.
    :param l10n: Language set by the user.
    :param state: FSM (AddBlacklist).
    :param storage: Storage for FSM.
    :return: Adding a user to the blacklist.
    """

    await ClearKeyboard.clear(message, storage)

    user, response_message = await find_user(message.text, l10n)

    if user:
        id_user = user["id_user"]
        fullname = user["fullname"]
        username = user["username"]
        url_user = await create_user_link(fullname, username)

        response = await api.blacklist.create_blacklist(id_user)
        status = response.status

        if status == 201:
            await message.answer(
                l10n.format_value(
                    "add-blacklist-success",
                    {"url_user": url_user, "id_user": str(id_user)},
                )
            )
            await state.clear()
        else:
            sent_message = await message.answer(
                l10n.format_value(
                    "add-blacklist-error",
                    {"url_user": url_user, "id_user": str(id_user)},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                user_id=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
    else:
        sent_message = await message.answer(
            response_message, reply_markup=cancel_keyboard(l10n)
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            user_id=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
