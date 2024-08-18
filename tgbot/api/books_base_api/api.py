from tgbot.config import config
from .base import BaseClient
from .endpoints import (
    AdminsApi,
    BlacklistApi,
    BooksApi,
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
        self.blacklist = BlacklistApi(self, self.prefix)
        self.books = BooksApi(self, self.prefix)
        self.orders = OrdersApi(self, self.prefix)
        self.premium = PremiumApi(self, self.prefix)
        self.users = UsersApi(self, self.prefix)

    async def close(self):
        await super().close()


api = BooksBaseApi()
