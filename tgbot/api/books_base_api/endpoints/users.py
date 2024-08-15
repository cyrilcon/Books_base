from datetime import datetime

from tgbot.api.books_base_api.base import BaseClient, ApiResponse


class UsersApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/users"

    async def create_user(
        self,
        id_user: int,
        language: str,
        fullname: str = None,
        username: str = None,
    ) -> ApiResponse:
        """
        Create a user.

        :param id_user: Unique user identifier.
        :param language: User's full name (first name and last name) | None.
        :param fullname: User's username (begins with the @ symbol) | None.
        :param username: User-selected language (ISO 639-1 code, e.g., "en" for English).
        """

        data = {
            "id_user": id_user,
            "fullname": fullname,
            "username": username,
            "language": language,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=self.endpoint,
            json=data,
        )

        return ApiResponse(status, result)

    async def get_user_by_username(self, username: str) -> ApiResponse:
        """
        Get a user by username.

        :param username: User's username.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/username/{username}",
        )
        return ApiResponse(status, result)

    async def get_user_by_id(self, id_user: int) -> ApiResponse:
        """
        Get a user by ID.

        :param id_user: Unique user identifier.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_user}",
        )
        return ApiResponse(status, result)

    async def update_user(self, id_user: int, **kwargs) -> ApiResponse:
        """
        Partially update user information.

        :param id_user: Unique user identifier.
        :param kwargs: Additional arguments.
        """

        data = {key: value for key, value in kwargs.items()}
        data["last_activity"] = datetime.now().isoformat()

        status, result = await self.base_client.make_request(
            method="PATCH",
            url=f"{self.endpoint}/{id_user}",
            json=data,
        )
        return ApiResponse(status, result)
