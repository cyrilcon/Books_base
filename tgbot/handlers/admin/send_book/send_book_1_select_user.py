from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tgbot.services import find_user, ClearKeyboard, create_user_link
from tgbot.states import SendBook

send_book_router_1 = Router()
send_book_router_1.message.filter(AdminFilter())


@send_book_router_1.message(Command("send_book"))
async def send_book_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("send-book-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendBook.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@send_book_router_1.message(StateFilter(SendBook.select_user), F.text)
async def send_book_1_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    user, response_message = await find_user(message.text, l10n)

    if user:
        id_user = user["id_user"]
        fullname = user["fullname"]
        username = user["username"]
        user_link = await create_user_link(fullname, username)

        sent_message = await message.answer(
            l10n.format_value(
                "send-book-select-book",
                {"user_link": user_link, "id_user": str(id_user)},
            ),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await state.update_data(id_user_recipient=id_user)
        await state.set_state(SendBook.select_book)
    else:
        sent_message = await message.answer(
            response_message, reply_markup=cancel_keyboard(l10n)
        )

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
