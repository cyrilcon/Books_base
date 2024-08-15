from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.services.fluent_loader import get_fluent_localization


async def get_user_language(id_user: int) -> FluentLocalization:
    """
    Returns the set language of the user.
    :param id_user: User identifier.
    :return: Selected user language.
    """

    response = await api.users.get_user_by_id(id_user)
    status = response.status
    user = response.result

    if status == 200:
        language = user["language"]
        l10n = get_fluent_localization(language)
        return l10n

    l10n = get_fluent_localization("ru")
    return l10n
