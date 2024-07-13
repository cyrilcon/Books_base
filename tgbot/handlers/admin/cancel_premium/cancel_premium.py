from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import get_user_language, find_user, get_url_user
from tgbot.states import CancelPremium

cancel_premium_router = Router()
cancel_premium_router.message.filter(AdminFilter())


@cancel_premium_router.message(Command("cancel_premium"))
async def cancel_premium(message: Message, state: FSMContext):
    """
    Обработка команды /cancel_premium.
    :param message: Команда /cancel_premium.
    :param state: FSM (CancelPremium).
    :return: Сообщение для выбора пользователя и переход в FSM (CancelPremium).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("cancel-premium-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(CancelPremium.select_user)


@cancel_premium_router.message(StateFilter(CancelPremium.select_user))
async def cancel_premium_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор пользователя для отмены статуса Books_Base Premium.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param bot: Экземпляр бота.
    :param state: FSM (CancelPremium).
    :return: Отмена статуса Books_Base Premium у пользователя.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    status, user, response_message = await find_user(message.text, l10n)

    if status == 200:
        id_user = user["id_user"]
        fullname = user["fullname"]
        username = user["username"]
        url_user = await get_url_user(fullname, username)

        response = await api.users.cancel_premium(id_user)
        status = response.status

        if status == 204:
            await message.answer(
                l10n.format_value(
                    "cancel-premium-success",
                    {"url_user": url_user, "id_user": str(id_user)},
                )
            )
            await state.clear()
        else:
            await message.answer(
                l10n.format_value(
                    "cancel-premium-error",
                    {"url_user": url_user, "id_user": str(id_user)},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
    else:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
