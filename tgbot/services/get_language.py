from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.services import get_fluent_localization


async def get_user_language(id_user: int) -> FluentLocalization:
    """
    Возвращает установленный язык пользователя.
    :param id_user: id пользователя.
    :return: Выбранный язык пользователя.
    """
    status, user = await api.users.get_user(id_user)
    language = user["language"]
    l10n = get_fluent_localization(language)
    return l10n
