from tgbot.api.books_base_api.base import BaseClient, ApiResponse


class BookingsApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/bookings"

    async def create_booking(
        self,
        id_booking: int,
        id_user: int,
        title: str,
        author: str,
    ) -> ApiResponse:
        """
        Create a user.

        :param id_booking: Unique booking identifier.
        :param id_user: Unique user identifier who made the booking.
        :param title: Title of the book being booked.
        :param author: The author of the book being booked.

        """

        data = {
            "id_booking": id_booking,
            "id_user": id_user,
            "title": title,
            "author": author,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=f"{self.endpoint}",
            json=data,
        )
        return ApiResponse(status, result)

    async def get_booking_count(self) -> ApiResponse:
        """
        Get the total number of bookings.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/count",
        )
        return ApiResponse(status, result)

    async def get_booking_by_position(self, position: int) -> ApiResponse:
        """
        Get a booking by position.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/position/{position}",
        )
        return ApiResponse(status, result)

    async def get_booking_by_id(self, id_booking: int) -> ApiResponse:
        """
        Get a booking by ID.

        :param id_booking: Unique booking identifier.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_booking}",
        )
        return ApiResponse(status, result)

    async def delete_booking(self, id_booking: int) -> ApiResponse:
        """
        Cancel a booking.

        :param id_booking: Unique booking identifier.
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_booking}",
        )
        return ApiResponse(status, result)
