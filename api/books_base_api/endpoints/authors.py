from api.books_base_api.base import BaseClient, ApiResponse
from api.books_base_api.schemas import AuthorSearchResponse, AuthorSchema


class AuthorsApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/authors"

    async def search_authors(
        self,
        author_name: str,
        max_results: int = 5,
        similarity_threshold: int = 75,
        page: int | None = None,
    ) -> ApiResponse[AuthorSearchResponse]:
        """
        Search authors with Levenshtein distance.

        :param author_name: Name of the author to search for.
        :param max_results: Maximum number of authors to return.
        :param similarity_threshold: Minimum similarity threshold.
        :param page: Page number for pagination.
        """

        params = {
            "author_name": author_name,
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
        return ApiResponse(status, result, model=AuthorSearchResponse)

    async def get_author_by_id(self, id_author: int) -> ApiResponse[AuthorSchema]:
        """
        Get an author by ID.

        :param id_author: Unique author identifier.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_author}",
        )
        return ApiResponse(status, result, model=AuthorSchema)
