from typing import List

from config import config
from tg_bot.api_client.base import BaseClient, ApiResponse
from api.api_v1.schemas import OrderSchema


class OrdersApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}{config.api.v1.orders}"

    async def get_order_ids(self) -> ApiResponse[List[int]]:
        """
        Get a list of order IDs.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}",
        )
        return ApiResponse(status, result)

    async def create_order(
        self,
        id_order: int,
        id_user: int,
        book_title: str,
        author_name: str,
    ) -> ApiResponse[OrderSchema]:
        """
        Create an order.

        :param id_order: Unique order identifier.
        :param id_user: Unique user identifier who made the order.
        :param book_title: Title of the book being ordered.
        :param author_name: The author of the book being ordered.

        """

        data = {
            "id_order": id_order,
            "id_user": id_user,
            "book_title": book_title,
            "author_name": author_name,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=f"{self.endpoint}",
            json=data,
        )
        return ApiResponse(status, result, model=OrderSchema)

    async def get_orders_count(self) -> ApiResponse[int]:
        """
        Get the total number of orders.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/count",
        )
        return ApiResponse(status, result)

    async def get_order_by_position(self, position: int) -> ApiResponse[OrderSchema]:
        """
        Get an order by position.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/position/{position}",
        )
        return ApiResponse(status, result, model=OrderSchema)

    async def get_order_by_id(self, id_order: int) -> ApiResponse[OrderSchema]:
        """
        Get an order by ID.

        :param id_order: Unique order identifier.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_order}",
        )
        return ApiResponse(status, result, model=OrderSchema)

    async def delete_order(self, id_order: int) -> ApiResponse:
        """
        Cancel an order.

        :param id_order: Unique order identifier.
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_order}",
        )
        return ApiResponse(status, result)
