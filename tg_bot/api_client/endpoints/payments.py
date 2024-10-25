from typing import List

from tg_bot.api_client.base import BaseClient, ApiResponse
from tg_bot.api_client.schemas import PaymentSchema


class PaymentsApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/payments"

    async def create_payment(
        self,
        id_payment: int,
        id_user: int,
        price: int,
        currency: str,
        type: str,
        book_ids: List[int] | None = None,
    ) -> ApiResponse[PaymentSchema]:
        """
        Create a payment.

        :param id_payment: Unique payment identifier.
        :param id_user: Unique user identifier who made the payment.
        :param price: Price of payment.
        :param currency: Currency in which the payment was made.
        :param type: Payment type value (what was purchased).
        :param book_ids: Currency in which the payment was made.
        """

        data = {
            "id_payment": id_payment,
            "id_user": id_user,
            "price": price,
            "currency": currency,
            "type": type,
        }
        if book_ids is not None:
            data["book_ids"] = book_ids

        status, result = await self.base_client.make_request(
            method="POST",
            url=f"{self.endpoint}",
            json=data,
        )
        return ApiResponse(status, result, model=PaymentSchema)

    async def get_payment_by_id(self, id_payment: str) -> ApiResponse[PaymentSchema]:
        """
        Get an order by ID.

        :param id_payment: Unique payment identifier.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_payment}",
        )
        return ApiResponse(status, result, model=PaymentSchema)
