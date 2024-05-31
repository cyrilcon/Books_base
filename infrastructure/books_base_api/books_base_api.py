from environs import Env

from infrastructure.books_base_api.base import BaseClient
from .book_api import BooksApi
from .bookings_api import BookingsApi
from .user_api import UsersApi


class BooksBaseApi(BaseClient):
    def __init__(self, env: Env, api_key: str = None, **kwargs):
        self.api_key = api_key
        self.base_url = env.str("API_URL")
        super().__init__(base_url=self.base_url)

        self.books = BooksApi(self)
        self.bookings = BookingsApi(self)
        self.users = UsersApi(self)


env = Env()  # Создаётся объект Env
env.read_env(".env")  # Объект Env будет использоваться для чтения переменных окружения
api = BooksBaseApi(env)
