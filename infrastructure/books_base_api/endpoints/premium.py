from infrastructure.books_base_api.base import BaseClient, ApiResponse


class PremiumApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/premium"

    async def create_premium(self, id_user: int) -> ApiResponse:
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
        return ApiResponse(status, result)
