from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.services import get_fluent_localization


async def get_user_language(id_user: int) -> FluentLocalization:
    """
    Возвращает установленный язык пользователя.
    :param id_user: ID пользователя.
    :return: Выбранный язык пользователя.
    """
    response = await api.users.get_user(id_user)
    status = response.status
    user = response.result

    if status == 200:
        language = user["language"]
        l10n = get_fluent_localization(language)
        return l10n

    l10n = get_fluent_localization("ru")
    return l10n
