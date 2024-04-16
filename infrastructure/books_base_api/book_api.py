from infrastructure.books_base_api.base import BaseClient


class BooksApi:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client
        self.endpoint = "/books"

    async def get_latest_article(
        self,
        **kwargs,
    ):
        """
        Get the latest article of the book

        :param kwargs: additional arguments
        :return:
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/latestArticle",
        )

        return status, result

    async def get_book(
        self,
        id_book: int,
        **kwargs,
    ):
        """
        Get a book by id with all the information

        :param id_book: unique book identifier
        :param kwargs: additional arguments
        :return:
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_book}",
        )

        return status, result
