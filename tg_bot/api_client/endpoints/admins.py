from typing import List

from api.api_v1.schemas import UserSchema
from config import config
from tg_bot.api_client.base import BaseClient, ApiResponse


class AdminsApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}{config.api.v1.admins}"

    async def get_admin_ids(self) -> ApiResponse[List[int]]:
        """
        Get a list of admin user IDs.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}",
        )
        return ApiResponse(status, result)

    async def create_admin(self, id_user: int) -> ApiResponse[UserSchema]:
        """
        Create an admin.

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

    async def delete_admin(self, id_user: int) -> ApiResponse:
        """
        Remove a user from the list of admins.

        :param id_user: Unique user identifier.
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_user}",
        )
        return ApiResponse(status, result)
