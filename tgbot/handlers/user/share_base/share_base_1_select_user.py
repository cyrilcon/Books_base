from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LinkPreviewOptions

from infrastructure.books_base_api import api
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    cancel_keyboard,
    share_base_keyboard,
)
from tgbot.keyboards.inline.share_base import share_our_store_keyboard
from tgbot.services import (
    get_user_language,
    check_username,
)
from tgbot.states import ShareBase

share_base_router_1 = Router()


@share_base_router_1.message(Command("share_base"))
async def share_base_1(message: Message, state: FSMContext):
    """
    Обработка команды /share_base.
    :param message: Команда /share_base.
    :param state: FSM (ShareBase).
    :return: Сообщение для написания ника пользователя и переход в FSM (select_user).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("share-base-select-user"),
        reply_markup=cancel_keyboard(l10n),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await state.set_state(ShareBase.select_user)


@share_base_router_1.message(StateFilter(ShareBase.select_user))
async def share_base_1_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор пользователя, которому будут отправлены base.
    :param message: Сообщение с ожидаемым username.
    :param bot: Экземпляр бота.
    :param state: FSM (ShareBase).
    :return: Сообщение для указания количества base и переход в FSM (add_description).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    username = message.from_user.username
    l10n = await get_user_language(id_user)

    message_text = message.text
    selected_user = check_username(message_text)

    if selected_user:
        if selected_user == username:
            await message.answer(
                l10n.format_value("share-base-cannot-yourself"),
                reply_markup=cancel_keyboard(l10n),
            )
        else:
            response = await api.users.get_user_by_username(selected_user)
            status = response.status

            if status == 200:
                response = await api.users.get_user(id_user)
                bases = response.result["base"]

                amount_base = l10n.format_value(
                    "base-store-account-amount-base",
                    {"bases": bases},
                )

                await message.answer(
                    l10n.format_value(
                        "share-base-select-amount-base",
                        {"username": selected_user, "amount_base": amount_base},
                    ),
                    reply_markup=share_base_keyboard(l10n),
                )
                await state.clear()

            else:
                await message.answer(
                    l10n.format_value(
                        "share-base-username-not-found", {"username": selected_user}
                    ),
                    reply_markup=share_our_store_keyboard(l10n),
                )
    else:
        await message.answer(
            l10n.format_value("share-base-username-incorrect"),
            reply_markup=cancel_keyboard(l10n),
        )
