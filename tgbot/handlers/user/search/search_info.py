from aiogram import Router, F
from aiogram.types import CallbackQuery

from tgbot.services import get_user_language

search_info_router = Router()


@search_info_router.callback_query(F.data.startswith("pagination_info"))
async def search_info(call: CallbackQuery):
    """
    Краткое описание использования пагинации.
    :param call: Нажатая кнопка с нумерацией страницы.
    """

    page = call.data.split(":")[-2]
    all_pages = call.data.split(":")[-1]

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)
    text = l10n.format_value(
        "pagination-info",
        {
            "page": page,
            "all_pages": all_pages,
        },
    )

    await call.answer(text, show_alert=True)
