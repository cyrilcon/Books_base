from infrastructure.books_base_api.base import BaseClient, ApiResponse


class AdminsApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/admins"

    async def get_admin_ids(self) -> ApiResponse:
        """
        Get a list of admin user IDs.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}",
        )
        return ApiResponse(status, result)

    async def create_admin(self, id_user: int) -> ApiResponse:
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
        return ApiResponse(status, result)
