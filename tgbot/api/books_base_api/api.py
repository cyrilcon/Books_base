from tgbot.config import config
from .base import BaseClient
from .endpoints import (
    AdminsApi,
    ArticlesApi,
    AuthorsApi,
    BlacklistApi,
    BooksApi,
    DiscountsApi,
    GenresApi,
    OrdersApi,
    PremiumApi,
    UsersApi,
)


class BooksBaseApi(BaseClient):
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = config.api.url
        self.prefix = config.api.prefix
        super().__init__(base_url=self.base_url)

        self.admins = AdminsApi(self, self.prefix)
        self.articles = ArticlesApi(self, self.prefix)
        self.authors = AuthorsApi(self, self.prefix)
        self.blacklist = BlacklistApi(self, self.prefix)
        self.books = BooksApi(self, self.prefix)
        self.discounts = DiscountsApi(self, self.prefix)
        self.genres = GenresApi(self, self.prefix)
        self.orders = OrdersApi(self, self.prefix)
        self.premium = PremiumApi(self, self.prefix)
        self.users = UsersApi(self, self.prefix)

    async def close(self):
        await super().close()


api = BooksBaseApi()
