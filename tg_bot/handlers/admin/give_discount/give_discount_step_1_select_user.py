from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard, discounts_back_cancel_keyboard
from tg_bot.services import find_user, ClearKeyboard, create_user_link
from tg_bot.states import GiveDiscount

give_discount_step_1_router = Router()


@give_discount_step_1_router.message(Command("give_discount"))
async def give_discount(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("give-discount-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveDiscount.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@give_discount_step_1_router.message(StateFilter(GiveDiscount.select_user), F.text)
async def give_discount_step_1(
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

    discount = user.has_discount
    if discount:
        sent_message = await message.answer(
            l10n.format_value(
                "give-discount-error-user-already-has-discount",
                {"discount": discount},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_user = user.id_user
    full_name = user.full_name
    username = user.username
    user_link = await create_user_link(full_name, username)

    sent_message = await message.answer(
        l10n.format_value(
            "give-discount-prompt-select-discount",
            {"user_link": user_link, "id_user": str(id_user)},
        ),
        reply_markup=discounts_back_cancel_keyboard(l10n),
    )
    await state.update_data(id_user_recipient=id_user, user_link=user_link)
    await state.set_state(GiveDiscount.select_discount)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
