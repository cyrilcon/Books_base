from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import get_user_language, get_url_user, find_user
from tgbot.states import RemoveBlacklist

remove_blacklist_router = Router()
remove_blacklist_router.message.filter(AdminFilter())


@remove_blacklist_router.message(Command("remove_blacklist"))
async def remove_blacklist(message: Message, state: FSMContext):
    """
    Обработка команды /remove_blacklist.
    :param message: Команда /remove_blacklist.
    :param state: FSM (RemoveBlacklist).
    :return: Сообщение для удаления пользователя из чёрного списка и переход в FSM (RemoveBlacklist).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("remove-blacklist-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(RemoveBlacklist.select_user)


@remove_blacklist_router.message(StateFilter(RemoveBlacklist.select_user))
async def remove_blacklist_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор пользователя для удаления его из чёрного списка.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param bot: Экземпляр бота.
    :param state: FSM (AddToBlacklist).
    :return: Удаление пользователя из чёрного списка.
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

        response = await api.users.remove_blacklist(id_user)
        status = response.status

        if status == 204:
            await message.answer(
                l10n.format_value(
                    "remove-blacklist-user-was-removed",
                    {"url_user": url_user, "id_user": str(id_user)},
                )
            )
            await state.clear()
        else:
            await message.answer(
                l10n.format_value(
                    "remove-blacklist-user-is-not-already-in-blacklist",
                    {"url_user": url_user, "id_user": str(id_user)},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
    else:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
