from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import get_user_language, find_user, get_url_user
from tgbot.states import GivePremium

give_premium_router = Router()
give_premium_router.message.filter(AdminFilter())


@give_premium_router.message(Command("give_premium"))
async def give_premium(message: Message, state: FSMContext):
    """
    Обработка команды /give_premium.
    :param message: Команда /give_premium.
    :param state: FSM (GivePremium).
    :return: Сообщение для выбора пользователя и переход в FSM (GivePremium).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("give-premium-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(GivePremium.select_user)


@give_premium_router.message(StateFilter(GivePremium.select_user))
async def give_premium_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор пользователя для выдачи статуса Books_Base Premium.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param bot: Экземпляр бота.
    :param state: FSM (GivePremium).
    :return: Выдача пользователю статуса Books_Base Premium.
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

        response = await api.users.give_premium(id_user)
        status = response.status

        if status == 201:
            await message.answer(
                l10n.format_value(
                    "give-premium-success",
                    {"url_user": url_user, "id_user": str(id_user)},
                )
            )
            await state.clear()
        else:
            await message.answer(
                l10n.format_value(
                    "give-premium-error",
                    {"url_user": url_user, "id_user": str(id_user)},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
    else:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
