from infrastructure.books_base_api import api
from tgbot.services import check_username


async def find_user(identifier, l10n):
    """
    Поиск пользователя по его ID или username.
    :param identifier: ID или username пользователя.
    :param l10n: Объект для локализации сообщений.
    :return: Кортеж (status, user, message).
    """

    if identifier.isdigit():
        id_user = int(identifier)
        response = await api.users.get_user(id_user)
        status = response.status

        if status == 200:
            user = response.result
            return status, user, None

        else:
            response_message = l10n.format_value(
                "user-not-found-by-id",
                {"id_user": str(id_user)},
            )
            return status, None, response_message

    else:
        selected_user = check_username(identifier)

        if selected_user:
            response = await api.users.get_user_by_username(selected_user)
            status = response.status

            if status == 200:
                user = response.result
                return status, user, None

            else:
                response_message = l10n.format_value(
                    "user-not-found-by-username",
                    {"username": selected_user},
                )
                return status, None, response_message

        else:
            response_message = l10n.format_value("username-incorrect")
            return None, None, response_message
