from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    done_clear_back_cancel_keyboard,
    cancel_keyboard,
    post_cancel_keyboard,
)
from tgbot.services import ClearKeyboard, generate_book_caption
from tgbot.states import AddBook

add_book_router_8 = Router()
add_book_router_8.message.filter(AdminFilter())


@add_book_router_8.callback_query(StateFilter(AddBook.select_price), F.data == "back")
async def back_to_add_book_7(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)

    data = await state.get_data()
    files = data.get("files")
    formats = ", ".join(f"{file['format']}" for file in files)

    await call.message.edit_text(
        l10n.format_value(
            "add-book-files-send-more",
            {"formats": formats},
        ),
        reply_markup=done_clear_back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_files)


@add_book_router_8.callback_query(
    StateFilter(AddBook.select_price),
    F.data.in_({"price_post_85", "price_post_50", "do_not_publish", "not_from_user"}),
)
async def add_book_8(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await call.answer(cache_time=1)

    button_pressed = call.data

    price = 50 if button_pressed == "price_post_50" else 85
    from_user = False if button_pressed == "not_from_user" else True
    await state.update_data(price=price, from_user=from_user)

    post = False if button_pressed == "do_not_publish" else True
    await state.update_data(post=post)

    data = await state.get_data()
    cover = data.get("cover")
    description = data.get("description")

    caption = await generate_book_caption(data, post=True, from_user=from_user)
    caption_length = len(caption)

    if caption_length <= 1024:
        await call.message.delete()
        sent_message = await call.message.answer_photo(
            photo=cover,
            caption=caption,
            reply_markup=post_cancel_keyboard(l10n),
        )
        await state.update_data(caption=caption)
        await state.set_state(AddBook.preview)
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=call.from_user.id,
            sent_message_id=sent_message.message_id,
        )
    else:
        await call.message.edit_text(
            l10n.format_value(
                "add-book-caption-too-long",
                {
                    "description": description,
                    "caption_length": caption_length,
                },
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await state.set_state(AddBook.reduce_description)


@add_book_router_8.message(StateFilter(AddBook.reduce_description), F.text)
async def abbreviation_of_description(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    abbreviated_description = message.text
    await state.update_data(description=abbreviated_description)

    data = await state.get_data()
    cover = data.get("cover")
    from_user = data.get("from_user")

    caption = await generate_book_caption(data, post=True, from_user=from_user)
    caption_length = len(caption)

    if caption_length < 1024:
        sent_message = await message.answer_photo(
            photo=cover,
            caption=caption,
            reply_markup=post_cancel_keyboard(l10n),
        )
        await state.update_data(caption=caption)
        await state.set_state(AddBook.preview)
    else:
        sent_message = await message.answer(
            l10n.format_value(
                "add-book-caption-too-long",
                {
                    "description": abbreviated_description,
                    "caption_length": caption_length,
                },
            ),
            reply_markup=cancel_keyboard(l10n),
        )

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
