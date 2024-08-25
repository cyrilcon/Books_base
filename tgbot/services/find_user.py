from typing import Tuple

from tgbot.api.books_base_api import api
from tgbot.schemas import UserSchema
from tgbot.services import extract_username


async def find_user(identifier, l10n) -> Tuple[UserSchema | None, str | None]:
    """
    Search for a user by user ID or username.
    :param identifier: User ID or username.
    :param l10n: Language set by the user.
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
