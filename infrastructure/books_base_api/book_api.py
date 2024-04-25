from infrastructure.books_base_api.base import BaseClient


class BooksApi:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client
        self.endpoint = "/books"

    async def add_book(self, data: dict, **kwargs):
        """
        Get the latest article of the book

        :param data: dictionary with book data
        :param kwargs: additional arguments
        :return: status code and result
        """

        data = {
            "id_book": data.get("id_book"),
            "title": data.get("title"),
            "description": data.get("description"),
            "cover": data.get("cover"),
            "price": data.get("price"),
            "authors": data.get("authors"),
            "genres": data.get("genres"),
            "files": data.get("files"),
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=self.endpoint,
            json=data,
        )

        return status, result

    async def get_latest_article(self, **kwargs):
        """
        Get the latest article of the book

        :param kwargs: additional arguments
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/latestArticle",
        )

        return status, result

    async def get_book(self, id_book: int, **kwargs):
        """
        Get a book by id with all the information

        :param id_book: unique book identifier
        :param kwargs: additional arguments
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_book}",
        )

        return status, result
