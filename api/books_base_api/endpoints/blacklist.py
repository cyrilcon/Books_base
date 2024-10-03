from typing import List

from api.books_base_api.base import BaseClient, ApiResponse
from api.books_base_api.schemas import UserSchema


class BlacklistApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/blacklist"

    async def get_blacklisted_user_ids(self) -> ApiResponse[List[int]]:
        """
        Get a list of blacklisted user IDs.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}",
        )
        return ApiResponse(status, result)

    async def create_blacklist(self, id_user: int) -> ApiResponse[UserSchema]:
        """
        Add a user to the blacklist.

        :param id_user: Unique user identifier.
        """

        data = {
            "id_user": id_user,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=f"{self.endpoint}",
            json=data,
        )
        return ApiResponse(status, result, model=UserSchema)

    async def delete_blacklist(self, id_user: int) -> ApiResponse:
        """
        Remove a user from the blacklist.

        :param id_user: Unique user identifier.
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_user}",
        )
        return ApiResponse(status, result)
