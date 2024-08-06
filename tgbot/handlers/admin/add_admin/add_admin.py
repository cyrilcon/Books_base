from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import SuperAdminFilter
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import find_user, create_user_link, ClearKeyboard
from tgbot.states import AddAdmin

add_admin_router = Router()
add_admin_router.message.filter(SuperAdminFilter())


@add_admin_router.message(Command("add_admin"))
async def add_admin(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    """
    Processing of the /add_admin command.
    :param message: /add_admin command.
    :param l10n: Language set by the user.
    :param state: FSM (AddAdmin).
    :param storage: Storage for FSM.
    :return: Message to add a user to the admin list and go to FSM (AddAdmin).
    """

    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("add-admin-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddAdmin.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_admin_router.message(StateFilter(AddAdmin.select_user), F.text)
async def add_admin_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    """
    Selects the user to add to the admin list.
    :param message: A message with the expected username or user ID.
    :param l10n: Language set by the user.
    :param state: FSM (AddAdmin).
    :param storage: Storage for FSM.
    :return: Adding a user to the blacklist.
    """

    await ClearKeyboard.clear(message, storage)

    user, response_message = await find_user(message.text, l10n)

    if user:
        id_user = user["id_user"]
        fullname = user["fullname"]
        username = user["username"]
        user_link = await create_user_link(fullname, username)

        response = await api.admins.create_admin(id_user)
        status = response.status

        if status == 201:
            await message.answer(
                l10n.format_value(
                    "add-admin-success",
                    {"user_link": user_link, "id_user": str(id_user)},
                )
            )
            await state.clear()
        else:
            sent_message = await message.answer(
                l10n.format_value(
                    "add-admin-error",
                    {"user_link": user_link, "id_user": str(id_user)},
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
