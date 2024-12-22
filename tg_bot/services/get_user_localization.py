from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.services.fluent_loader import get_fluent_localization


async def get_user_localization(id_user: int) -> FluentLocalization:
    """
    Returns the set language of the user.
    :param id_user: Unique user identifier.
    :return: Selected user language.
    """

    response = await api.users.get_user_by_id(id_user)

    if response.status == 200:
        user = response.get_model()
        language_code = user.language_code
        l10n = get_fluent_localization(language_code)
        return l10n

    l10n = get_fluent_localization("ru")
    return l10n
