from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import find_user, create_user_link, ClearKeyboard
from tg_bot.states import TakeDiscount

take_discount_router = Router()


@take_discount_router.message(Command("take_discount"))
async def take_discount(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("take-discount-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(TakeDiscount.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@take_discount_router.message(
    StateFilter(TakeDiscount.select_user),
    F.text,
)
async def take_discount_process(
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

    if not user.has_discount:
        sent_message = await message.answer(
            l10n.format_value(
                "take-discount-error-user-already-has-not-discount",
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

    await api.users.discounts.delete_discount(id_user=id_user)
    await message.answer(
        l10n.format_value(
            "take-discount-success",
            {
                "discount": user.has_discount,
                "user_link": user_link,
                "id_user": str(id_user),
            },
        )
    )
    await state.clear()
