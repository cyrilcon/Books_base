from config import config
from tg_bot.api_client.base import BaseClient
from tg_bot.api_client.endpoints import (
    ArticlesApi,
    AuthorsApi,
    BooksApi,
    GenresApi,
    OrdersApi,
    PaymentsApi,
    UsersApi,
)


class BooksBaseApi(BaseClient):
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = config.api.url
        self.prefix = config.api.prefix
        super().__init__(base_url=self.base_url)

        self.articles = ArticlesApi(self, self.prefix)
        self.authors = AuthorsApi(self, self.prefix)
        self.books = BooksApi(self, self.prefix)
        self.genres = GenresApi(self, self.prefix)
        self.orders = OrdersApi(self, self.prefix)
        self.payments = PaymentsApi(self, self.prefix)
        self.users = UsersApi(self, self.prefix)

    async def close(self):
        await super().close()


api = BooksBaseApi()
