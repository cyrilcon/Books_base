from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard, back_and_cancel_keyboard
from tgbot.services import get_user_language, check_username, get_url_user


async def search_user(message: Message, bot: Bot, state: FSMContext, state_class, text):
    """
    Выбор пользователя для дальнейшей с ним коммуникацией.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param bot: Экземпляр бота.
    :param state: FSMContext.
    :param state_class: Класс состояния для FSM.
    :param text: Текст отправляемы пользователю при ответе.
    :return: Обновление состояния FSM.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    message_text = message.text

    if message_text.isdigit():
        id_user = int(message_text)

        response = await api.users.get_user(id_user)
        status = response.status

        if status == 200:
            await user_found(response, message, l10n, state, state_class, text)
        else:
            await message.answer(
                l10n.format_value("user-not-found-by-id", {"id_user": str(id_user)}),
                reply_markup=cancel_keyboard(l10n),
            )
    else:
        selected_user = check_username(message_text)

        if selected_user:
            response = await api.users.get_user_by_username(selected_user)
            status = response.status

            if status == 200:
                await user_found(response, message, l10n, state, state_class, text)
            else:
                await message.answer(
                    l10n.format_value(
                        "user-not-found-by-username", {"username": selected_user}
                    ),
                    reply_markup=cancel_keyboard(l10n),
                )
        else:
            await message.answer(
                l10n.format_value("username-incorrect"),
                reply_markup=cancel_keyboard(l10n),
            )


async def user_found(response, message, l10n, state, state_class, text):
    """
    Сценарий, если пользователь найден.
    :param response: Полученный ответ от api.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param l10n: Язык установленный у пользователя.
    :param state: FSMContext.
    :param state_class: Класс состояния для FSM.
    :param text: Текст отправляемы пользователю при ответе.
    :return: Обновление состояния FSM.
    """

    user = response.result
    id_user_recipient = user["id_user"]
    fullname = user["fullname"]
    username = user["username"]

    url_user = await get_url_user(fullname, username)

    await message.answer(
        l10n.format_value(
            text, {"url_user": url_user, "id_user": str(id_user_recipient)}
        ),
        reply_markup=back_and_cancel_keyboard(l10n),
    )

    await state.update_data(id_user_recipient=id_user_recipient)
    await state.set_state(state_class)
