from infrastructure.books_base_api.api_response import ApiResponse
from infrastructure.books_base_api.base import BaseClient


class BooksApi:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client
        self.endpoint = "/books"

    async def add_book(self, data: dict) -> ApiResponse:
        """
        Get the latest article of the book

        :param data: dictionary with book data
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

        return ApiResponse(status, result)

    async def get_latest_article(self) -> ApiResponse:
        """
        Get the latest article of the book

        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/latest-article",
        )

        return ApiResponse(status, result)

    async def get_all_titles(self) -> ApiResponse:
        """
        Get all titles

        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/titles",
        )

        return ApiResponse(status, result)

    async def get_books_by_titles(self, titles) -> ApiResponse:
        """
        Get articles, titles, authors of books, by the titles

        :param titles: list of titles
        :return: status code and result
        """

        data = {"titles": titles}

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/books-by-titles",
            json=data,
        )

        return ApiResponse(status, result)

    async def get_book_by_title(self, title: str) -> ApiResponse:
        """
        Get a book by title with all the information

        :param title: book title
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/title/{title}",
        )

        return ApiResponse(status, result)

    async def get_book(self, id_book: int) -> ApiResponse:
        """
        Get a book by id with all the information

        :param id_book: unique book identifier
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_book}",
        )

        return ApiResponse(status, result)

    async def update_book(self, id_edit_book: int, **kwargs) -> ApiResponse:
        """
        Update a book by id

        :param id_edit_book: unique edit book identifier
        :param kwargs: additional arguments
        :return:
        """

        data = {key: value for key, value in kwargs.items()}

        status, result = await self.base_client.make_request(
            method="PATCH",
            url=f"{self.endpoint}/{id_edit_book}",
            json=data,
        )

        return ApiResponse(status, result)

    async def delete_book(self, id_book: int) -> ApiResponse:
        """
        Delete a book

        :param id_book: unique book identifier
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_book}",
        )

        return ApiResponse(status, result)
