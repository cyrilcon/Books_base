from infrastructure.books_base_api.base import BaseClient, ApiResponse


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
