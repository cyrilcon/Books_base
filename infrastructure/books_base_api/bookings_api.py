from infrastructure.books_base_api.api_response import ApiResponse
from infrastructure.books_base_api.base import BaseClient


class BookingsApi:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client
        self.endpoint = "/booking"

    async def create_booking(
        self, id_user: int, id_booking: int, title: str, author: str
    ) -> ApiResponse:
        """
        Add a booking

        :param id_user: unique user identifier
        :param id_booking: unique booking identifier
        :param title: book title
        :param author: author title
        :return: status code and result
        """

        data = {
            "id_user": id_user,
            "id_booking": id_booking,
            "title": title,
            "author": author,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=self.endpoint,
            json=data,
        )

        return ApiResponse(status, result)

    async def get_booking_count(self) -> ApiResponse:
        """
        Get booking count

        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/count",
        )

        return ApiResponse(status, result)

    async def get_booking_by_position(self, position: int) -> ApiResponse:
        """
        Get a booking by position

        :param position: booking position in the database
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/position/{position}",
        )

        return ApiResponse(status, result)

    async def get_booking(self, id_booking: int) -> ApiResponse:
        """
        Get a booking by id

        :param id_booking: unique booking identifier
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_booking}",
        )

        return ApiResponse(status, result)

    async def delete_booking(self, id_booking: int) -> ApiResponse:
        """
        Delete a booking

        :param id_booking: unique booking identifier
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_booking}",
        )

        return ApiResponse(status, result)
