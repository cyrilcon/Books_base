from datetime import datetime

from environs import Env

from infrastructure.books_base_api.base import BaseClient


class BooksBaseApi(BaseClient):
    def __init__(self, env: Env, api_key: str = None, **kwargs):
        self.api_key = api_key
        self.base_url = env.str("API_URL")
        super().__init__(base_url=self.base_url)

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

        endpoint = "/users"

        data = {
            "id_user": id_user,
            "fullname": fullname,
            "username": username,
        }

        status, result = await self._make_request(
            method="POST",
            url=endpoint,
            json=data,
        )

        # await self.close()
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

        endpoint = f"/users/{id_user}"

        status, result = await self._make_request(
            method="GET",
            url=endpoint,
        )

        # await self.close()
        return status, result


env = Env()  # Создаётся объект Env
env.read_env(".env")  # Объект Env будет использоваться для чтения переменных окружения
api = BooksBaseApi(env)
