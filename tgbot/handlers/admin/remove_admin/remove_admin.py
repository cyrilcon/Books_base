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
from tgbot.states import RemoveAdmin

remove_admin_router = Router()
remove_admin_router.message.filter(SuperAdminFilter())


@remove_admin_router.message(Command("remove_admin"))
async def remove_admin(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    """
    Processing of the /remove_admin command.
    :param message: /remove_admin command.
    :param l10n: Language set by the user.
    :param state: FSM (RemoveAdmin).
    :param storage: Storage for FSM.
    :return: Message to demote the administrator and go to FSM (RemoveAdmin).
    """

    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("remove-admin-select"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(RemoveAdmin.select_admin)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@remove_admin_router.message(StateFilter(RemoveAdmin.select_admin), F.text)
async def remove_admin_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    """
    Selecting an administrator for demotion.
    :param message: A message with the expected username or user ID.
    :param l10n: Language set by the user.
    :param state: FSM (RemoveAdmin).
    :param storage: Storage for FSM.
    :return: Administrator demotion.
    """

    await ClearKeyboard.clear(message, storage)

    user, response_message = await find_user(message.text, l10n)

    if user:
        id_user = user["id_user"]

        if id_user == message.from_user.id:
            sent_message = await message.answer(
                l10n.format_value(
                    "remove-admin-error-self-remove",
                ),
                reply_markup=cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                user_id=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
        else:
            fullname = user["fullname"]
            username = user["username"]
            user_link = await create_user_link(fullname, username)

            response = await api.admins.delete_admin(id_user)
            status = response.status

            if status == 204:
                await message.answer(
                    l10n.format_value(
                        "remove-admin-success",
                        {"user_link": user_link, "id_user": str(id_user)},
                    )
                )
                await state.clear()
            else:
                sent_message = await message.answer(
                    l10n.format_value(
                        "remove-admin-error-not-admin",
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
