from typing import Tuple

from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from api.api_v1.schemas import UserSchema
from tg_bot.services.extract_username import extract_username


async def find_user(
    l10n: FluentLocalization,
    identifier: str,
) -> Tuple[UserSchema | None, str | None]:
    """
    Search for a user by user ID or username.
    :param l10n: Language set by the user.
    :param identifier: User ID or username.
    :return: Tuple (user, message).
    """

    if identifier.isdigit():
        id_user = int(identifier)
        response = await api.users.get_user_by_id(id_user)
        status = response.status

        if status != 200:
            response_message = l10n.format_value(
                "error-user-not-found-by-id",
                {"id_user": str(id_user)},
            )
            return None, response_message

        user = response.get_model()
        return user, None

    username = extract_username(identifier)

    if not username:
        response_message = l10n.format_value("error-invalid-username")
        return None, response_message

    response = await api.users.get_user_by_username(username)
    status = response.status

    if status != 200:
        response_message = l10n.format_value(
            "error-user-not-found-by-username",
            {"username": username},
        )
        return None, response_message

    user = response.get_model()
    return user, None
