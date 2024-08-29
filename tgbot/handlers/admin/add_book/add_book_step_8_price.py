from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline import (
    done_clear_back_cancel_keyboard,
    cancel_keyboard,
    post_cancel_keyboard,
)
from tgbot.services import ClearKeyboard, generate_book_caption, BookFormatter
from tgbot.states import AddBook

add_book_step_8_router = Router()


@add_book_step_8_router.callback_query(
    StateFilter(AddBook.select_price), F.data == "back"
)
async def back_to_add_book_step_7(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    data = await state.get_data()
    files = data.get("files")
    formats = BookFormatter.format_file_formats(files)

    await call.message.edit_text(
        l10n.format_value(
            "add-book-prompt-more-files",
            {"formats": formats},
        ),
        reply_markup=done_clear_back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_files)
    await call.answer()


@add_book_step_8_router.callback_query(
    StateFilter(AddBook.select_price),
    F.data.startswith("create_price")
    | F.data.startswith("not_from_user")
    | F.data.startswith("not_post"),
)
async def add_book_step_8(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    button_pressed = call.data.split(":")[0]
    price = int(call.data.split(":")[-1])

    from_user = False if button_pressed == "not_from_user" else True
    await state.update_data(price=price, from_user=from_user)

    is_post = False if button_pressed == "not_post" else True
    await state.update_data(is_post=is_post)

    data = await state.get_data()
    cover = data.get("cover")
    description = data.get("description")

    caption = await generate_book_caption(data, is_post=is_post, from_user=from_user)
    caption_length = len(caption)

    if caption_length > 1024:
        await call.message.edit_text(
            l10n.format_value(
                "add-book-error-caption-too-long",
                {
                    "description": description,
                    "caption_length": caption_length,
                },
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await state.set_state(AddBook.reduce_description)
        return

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
    await call.answer()


@add_book_step_8_router.message(StateFilter(AddBook.reduce_description), F.text)
async def add_book_step_8_abbreviation_of_description(
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
    is_post = data.get("is_post")
    from_user = data.get("from_user")

    caption = await generate_book_caption(data, is_post=is_post, from_user=from_user)
    caption_length = len(caption)

    if caption_length > 1024:
        sent_message = await message.answer(
            l10n.format_value(
                "add-book-error-caption-too-long",
                {
                    "description": abbreviated_description,
                    "caption_length": caption_length,
                },
            ),
            reply_markup=cancel_keyboard(l10n),
        )
    else:
        sent_message = await message.answer_photo(
            photo=cover,
            caption=caption,
            reply_markup=post_cancel_keyboard(l10n),
        )
        await state.update_data(caption=caption)
        await state.set_state(AddBook.preview)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
