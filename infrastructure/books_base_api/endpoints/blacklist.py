from infrastructure.books_base_api.base import BaseClient, ApiResponse


class BlacklistApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/blacklist"

    async def create_blacklist(self, id_user: int) -> ApiResponse:
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
        return ApiResponse(status, result)
