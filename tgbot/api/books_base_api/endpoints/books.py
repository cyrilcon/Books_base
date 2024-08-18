from tgbot.api.books_base_api.base import BaseClient, ApiResponse
from tgbot.schemas import (
    BookSchema,
    BookAuthorSearchResponse,
    BookGenreSearchResponse,
    BookTitleSearchResponse,
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

    async def search_books_by_author(
        self,
        author_name: str,
        max_results: int = 5,
        page: int | None = None,
    ) -> ApiResponse[BookAuthorSearchResponse]:
        """
        Search books by author.

        :param author_name: Author of the book to search for.
        :param max_results: Maximum number of books to return.
        :param page: Page number for pagination.
        """

        params = {
            "author_name": author_name,
            "max_results": max_results,
        }
        if page is not None:
            params["page"] = page

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/search-by-author",
            params=params,
        )
        return ApiResponse(status, result, model=BookAuthorSearchResponse)

    async def search_books_by_genre(
        self,
        genre_name: str,
        max_results: int = 5,
        page: int | None = None,
    ) -> ApiResponse[BookGenreSearchResponse]:
        """
        Search books by genre.

        :param genre_name: Genre of the book to search for.
        :param max_results: Maximum number of books to return.
        :param page: Page number for pagination.
        """

        params = {
            "genre_name": genre_name,
            "max_results": max_results,
        }
        if page is not None:
            params["page"] = page

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/search-by-genre",
            params=params,
        )
        return ApiResponse(status, result, model=BookGenreSearchResponse)

    async def search_books_by_title(
        self,
        title: str,
        max_results: int = 5,
        similarity_threshold: int = 75,
        page: int | None = None,
    ) -> ApiResponse[BookTitleSearchResponse]:
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
        if page is not None:
            params["page"] = page

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/search-by-title",
            params=params,
        )
        return ApiResponse(status, result, model=BookTitleSearchResponse)

    async def get_latest_article(self) -> ApiResponse[int]:
        """
        Get the latest article of books.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/latest-article",
        )
        return ApiResponse(status, result)

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

    async def update_book(self, **kwargs) -> ApiResponse[BookSchema]:
        """
        Partially update book information.

        :param kwargs: Additional arguments.
        """

        id_book = kwargs.pop("id_book", None)
        if id_book is None:
            raise ValueError("id_book is required to update a book!!")

        data = {key: value for key, value in kwargs.items()}

        status, result = await self.base_client.make_request(
            method="PATCH",
            url=f"{self.endpoint}/{id_book}",
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
