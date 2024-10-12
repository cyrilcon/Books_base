from api.books_base_api.base import BaseClient, ApiResponse
from api.books_base_api.schemas import (
    BookSchema,
    BooksResponse,
    BookTitleSimilarityResponse,
)


class BooksApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/books"

    async def create_book(self, data: dict) -> ApiResponse[BookSchema]:
        """
        Create a book.

        :param data: Dictionary with book data.
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
        return ApiResponse(status, result, model=BookSchema)

    async def get_books_by_author_id(
        self,
        id_author: int,
        max_results: int = 5,
        page: int | None = None,
    ) -> ApiResponse[BooksResponse]:
        """
        Get books by author ID.

        :param id_author: Unique author identifier.
        :param max_results: Maximum number of books to return.
        :param page: Page number for pagination.
        """

        params = {"max_results": max_results}
        if page:
            params["page"] = page

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/author/{id_author}",
            params=params,
        )
        return ApiResponse(status, result, model=BooksResponse)

    async def get_books_by_genre_id(
        self,
        id_genre: int,
        max_results: int = 5,
        page: int | None = None,
    ) -> ApiResponse[BooksResponse]:
        """
        Get books by genre ID.

        :param id_genre: Unique genre identifier.
        :param max_results: Maximum number of books to return.
        :param page: Page number for pagination.
        """

        params = {"max_results": max_results}
        if page:
            params["page"] = page

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/genre/{id_genre}",
            params=params,
        )
        return ApiResponse(status, result, model=BooksResponse)

    async def get_latest_article(self) -> ApiResponse[int]:
        """
        Get the latest article of books.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/latest-article",
        )
        return ApiResponse(status, result)

    async def update_book_price(self) -> ApiResponse[BookSchema]:
        """
        Update the price of the book with a price of 50 to 85
        """

        status, result = await self.base_client.make_request(
            method="PATCH",
            url=f"{self.endpoint}/price",
        )
        return ApiResponse(status, result, model=BookSchema)

    async def search_books_by_title(
        self,
        title: str,
        max_results: int = 5,
        similarity_threshold: int = 75,
        page: int | None = None,
    ) -> ApiResponse[BookTitleSimilarityResponse]:
        """
        Search books by title with Levenshtein distance.

        :param title: Title of the book to search for.
        :param max_results: Maximum number of books to return.
        :param similarity_threshold: Minimum similarity threshold.
        :param page: Page number for pagination.
        """

        params = {
            "title": title,
            "max_results": max_results,
            "similarity_threshold": similarity_threshold,
        }
        if page:
            params["page"] = page

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/search-by-title",
            params=params,
        )
        return ApiResponse(status, result, model=BookTitleSimilarityResponse)

    async def get_book_by_id(self, id_book: int) -> ApiResponse[BookSchema]:
        """
        Get a book by ID.

        :param id_book: Unique book identifier (article of the book).
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_book}",
        )
        return ApiResponse(status, result, model=BookSchema)

    async def update_book(
        self, id_book_edited: int, **kwargs
    ) -> ApiResponse[BookSchema]:
        """
        Partially update book information.

        :param id_book_edited: Unique book edited identifier (article of the book).
        :param kwargs: Additional arguments.
        """

        data = {key: value for key, value in kwargs.items()}

        status, result = await self.base_client.make_request(
            method="PATCH",
            url=f"{self.endpoint}/{id_book_edited}",
            json=data,
        )
        return ApiResponse(status, result, model=BookSchema)

    async def delete_book(self, id_book: int) -> ApiResponse:
        """
        Delete a book.

        :param id_book: Unique book identifier (article of the book).
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_book}",
        )
        return ApiResponse(status, result)

    async def delete_file(self, id_book: int, file_format: str) -> ApiResponse:
        """
        Delete a file of the book by its format.

        :param id_book: Unique book identifier (article of the book).
        :param file_format: Format of the file.
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_book}/file/{file_format}",
        )
        return ApiResponse(status, result)
