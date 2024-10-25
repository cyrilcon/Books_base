from datetime import datetime, timezone
from typing import List

from tg_bot.api_client.base import BaseClient, ApiResponse
from tg_bot.api_client.endpoints import (
    AdminsApi,
    BlacklistApi,
    DiscountsApi,
    PremiumApi,
)
from tg_bot.api_client.schemas import UserSchema, UserStats


class UsersApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/users"

        self.admins = AdminsApi(self.base_client, self.endpoint)
        self.blacklist = BlacklistApi(self.base_client, self.endpoint)
        self.discounts = DiscountsApi(self.base_client, self.endpoint)
        self.premium = PremiumApi(self.base_client, self.endpoint)

    async def get_user_ids(self) -> ApiResponse[List[int]]:
        """
        Get a list of user IDs.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}",
        )
        return ApiResponse(status, result)

    async def create_user(
        self,
        id_user: int,
        language_code: str,
        full_name: str = None,
        username: str = None,
    ) -> ApiResponse[UserSchema]:
        """
        Create a user.

        :param id_user: Unique user identifier.
        :param language_code: IETF language tag of the user's language.
        :param full_name: User's full name (first name and last name). | None.
        :param username: User's username. | None.
        """

        data = {
            "id_user": id_user,
            "full_name": full_name,
            "username": username,
            "language_code": language_code,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=self.endpoint,
            json=data,
        )

        return ApiResponse(status, result, model=UserSchema)

    async def get_user_statistics(self) -> ApiResponse[UserStats]:
        """
        Get user activity statistics.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/stats",
        )
        return ApiResponse(status, result, model=UserStats)

    async def get_user_by_username(self, username: str) -> ApiResponse[UserSchema]:
        """
        Get a user by username.

        :param username: User's username.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/username/{username}",
        )
        return ApiResponse(status, result, model=UserSchema)

    async def get_book_ids(self, id_user: int) -> ApiResponse[List[int]]:
        """
        Get a list of book purchased IDs by the user.

        :param id_user: Unique user identifier.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_user}/books",
        )
        return ApiResponse(status, result)

    async def get_order_ids_by_user(self, id_user: int) -> ApiResponse[List[int]]:
        """
        Get a list of order IDs by the user.

        :param id_user: Unique user identifier.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_user}/orders",
        )
        return ApiResponse(status, result)

    async def get_user_by_id(self, id_user: int) -> ApiResponse[UserSchema]:
        """
        Get a user by ID.

        :param id_user: Unique user identifier.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_user}",
        )
        return ApiResponse(status, result, model=UserSchema)

    async def update_user(self, id_user: int, **kwargs) -> ApiResponse[UserSchema]:
        """
        Partially update user information.

        :param id_user: Unique user identifier.
        :param kwargs: Additional arguments.
        """

        data = {key: value for key, value in kwargs.items()}
        data["last_activity_datetime"] = datetime.now(timezone.utc).isoformat()

        status, result = await self.base_client.make_request(
            method="PATCH",
            url=f"{self.endpoint}/{id_user}",
            json=data,
        )
        return ApiResponse(status, result, model=UserSchema)
