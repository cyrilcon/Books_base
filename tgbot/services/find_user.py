from typing import Any

from tgbot.api.books_base_api import api
from tgbot.services import check_username


async def find_user(identifier, l10n) -> tuple[dict[str, Any] | None, str | None]:
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

        if status == 200:
            user = response.result
            return user, None

        else:
            response_message = l10n.format_value(
                "user-not-found-id",
                {"id_user": str(id_user)},
            )
            return None, response_message

    else:
        selected_user = check_username(identifier)

        if selected_user:
            response = await api.users.get_user_by_username(selected_user)
            status = response.status

            if status == 200:
                user = response.result
                return user, None

            else:
                response_message = l10n.format_value(
                    "user-not-found-username",
                    {"username": selected_user},
                )
                return None, response_message

        else:
            response_message = l10n.format_value("username-incorrect")
            return None, response_message
