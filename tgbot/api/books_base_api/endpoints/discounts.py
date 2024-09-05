from tgbot.api.books_base_api.base import BaseClient, ApiResponse
from tgbot.schemas import UserSchema, DiscountEnum


class DiscountsApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/discounts"

    async def create_discount(
        self, id_user: int, discount: DiscountEnum
    ) -> ApiResponse[UserSchema]:
        """
        Give a discount to the user.

        :param id_user: Unique user identifier.
        :param discount: Discount value.
        """

        data = {
            "id_user": id_user,
            "discount": discount,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=f"{self.endpoint}",
            json=data,
        )
        return ApiResponse(status, result, model=UserSchema)

    async def delete_discount(self, id_user: int) -> ApiResponse:
        """
        Remove a discount from the user.

        :param id_user: Unique user identifier.
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_user}",
        )
        return ApiResponse(status, result)
