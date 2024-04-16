from datetime import datetime

from infrastructure.books_base_api.base import BaseClient


class UsersApi:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client
        self.endpoint = "/users"

    async def add_user(
        self,
        id_user: int,
        fullname: str = None,
        username: str = None,
        **kwargs,
    ):
        """
        Add a user

        :param id_user: unique user identifier
        :param fullname: user's fullname (user's first name and last name)
        :param username: user's username (begins with the @ symbol)
        :param kwargs: additional arguments
        :return:
        """

        data = {
            "id_user": id_user,
            "fullname": fullname,
            "username": username,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=self.endpoint,
            json=data,
        )

        return status, result

    async def get_user(
        self,
        id_user: int,
        **kwargs,
    ):
        """
        Get a user by id with all the information

        :param id_user: unique user identifier
        :param kwargs: additional arguments
        :return:
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_user}",
        )

        return status, result

    async def update_user(
        self,
        id_user: int,
        **kwargs,
    ):
        """
        Update a user by id

        :param id_user: unique user identifier
        :param kwargs: additional arguments
        :return:
        """

        data = {key: value for key, value in kwargs.items()}
        data["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status, result = await self.base_client.make_request(
            method="PATCH",
            url=f"{self.endpoint}/{id_user}",
            json=data,
        )

        return status, result
