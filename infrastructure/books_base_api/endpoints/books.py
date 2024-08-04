from infrastructure.books_base_api.base import BaseClient, ApiResponse


class BooksApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/books"

    async def create_book(self, data: dict) -> ApiResponse:
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
        return ApiResponse(status, result)

    async def search_books_by_title(
        self,
        title: str,
        max_results: int = 5,
        similarity_threshold: int = 75,
        page: int | None = None,
    ) -> ApiResponse:
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
            url=f"{self.endpoint}/search",
            params=params,
        )
        return ApiResponse(status, result)

    async def get_latest_article(self) -> ApiResponse:
        """
        Get the latest article of books.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/latest-article",
        )
        return ApiResponse(status, result)

    async def get_book_by_id(self, id_book: int) -> ApiResponse:
        """
        Get a book by ID.

        :param id_book: Unique book identifier (article of the book).
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_book}",
        )
        return ApiResponse(status, result)
