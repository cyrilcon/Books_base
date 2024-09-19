from tg_bot.api.books_base_api.base import BaseClient, ApiResponse
from tg_bot.schemas import UserSchema


class PremiumApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/premium"

    async def create_premium(self, id_user: int) -> ApiResponse[UserSchema]:
        """
        Assign a user to premium.

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

    async def delete_premium(self, id_user: int) -> ApiResponse:
        """
        Remove a user from the list of premium users.

        :param id_user: Unique user identifier.
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_user}",
        )
        return ApiResponse(status, result)
