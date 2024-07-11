from datetime import datetime

from infrastructure.books_base_api.api_response import ApiResponse
from infrastructure.books_base_api.base import BaseClient


class UsersApi:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client
        self.endpoint = "/users"

    async def add_user(
        self,
        id_user: int,
        language: str,
        fullname: str = None,
        username: str = None,
    ) -> ApiResponse:
        """
        Add a user

        :param id_user: unique user identifier
        :param language: user selected language
        :param fullname: user's fullname (user's first name and last name)
        :param username: user's username (begins with the @ symbol)
        :return: status code and result
        """

        data = {
            "id_user": id_user,
            "fullname": fullname,
            "username": username,
            "language": language,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=self.endpoint,
            json=data,
        )

        return ApiResponse(status, result)

    async def get_admins(self) -> ApiResponse:
        """
        Get a list of admins id

        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/admins",
        )

        return ApiResponse(status, result)

    async def get_user_by_username(self, username: str) -> ApiResponse:
        """
        Get a user by username with all the information

        :param username: unique user identifier
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/username/{username}",
        )

        return ApiResponse(status, result)

    async def get_user(self, id_user: int) -> ApiResponse:
        """
        Get a user by id with all the information

        :param id_user: unique user identifier
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_user}",
        )

        return ApiResponse(status, result)

    async def update_user(self, id_user: int, **kwargs) -> ApiResponse:
        """
        Update a user by id

        :param id_user: unique user identifier
        :param kwargs: additional arguments
        :return: status code and result
        """

        data = {key: value for key, value in kwargs.items()}
        data["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status, result = await self.base_client.make_request(
            method="PATCH",
            url=f"{self.endpoint}/{id_user}",
            json=data,
        )

        return ApiResponse(status, result)

    async def set_discount(self, id_user: int, discount: int) -> ApiResponse:
        """
        Set a discount for a user

        :param id_user: unique user identifier
        :param discount: discount value
        :return: status code and result
        """

        data = {
            "discount": discount,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=f"{self.endpoint}/{id_user}/discount",
            json=data,
        )

        return ApiResponse(status, result)

    async def add_blacklist(self, id_user: int) -> ApiResponse:
        """
        Add user to blacklist

        :param id_user: unique user identifier
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="POST",
            url=f"{self.endpoint}/{id_user}/blacklist",
        )

        return ApiResponse(status, result)

    async def remove_blacklist(self, id_user: int) -> ApiResponse:
        """
        Remove user from blacklist

        :param id_user: unique user identifier
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_user}/blacklist",
        )

        return ApiResponse(status, result)
