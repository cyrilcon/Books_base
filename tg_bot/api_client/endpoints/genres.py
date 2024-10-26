from config import config
from tg_bot.api_client.base import BaseClient, ApiResponse
from api.api_v1.schemas import GenreSearchResponse, GenreSchema


class GenresApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}{config.api.v1.genres}"

    async def get_genres_with_pagination(
        self,
        max_results: int = 5,
        page: int | None = None,
    ) -> ApiResponse[GenreSchema]:
        """
        Get a list of genres with pagination.

        :param max_results: Maximum number of genres to return.
        :param page: Page number for pagination.
        """

        params = {"max_results": max_results}
        if page is not None:
            params["page"] = page

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}",
            params=params,
        )
        return ApiResponse(status, result, model=GenreSchema)

    async def get_genres_count(self) -> ApiResponse[int]:
        """
        Get the total number of genres.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/count",
        )
        return ApiResponse(status, result)

    async def search_genres(
        self,
        genre_name: str,
        max_results: int = 5,
        similarity_threshold: int = 75,
        page: int | None = None,
    ) -> ApiResponse[GenreSearchResponse]:
        """
        Search genres with Levenshtein distance.

        :param genre_name: Name of the genre to search for.
        :param max_results: Maximum number of genres to return.
        :param similarity_threshold: Minimum similarity threshold.
        :param page: Page number for pagination.
        """

        params = {
            "genre_name": genre_name,
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
        return ApiResponse(status, result, model=GenreSearchResponse)

    async def get_genre_by_id(self, id_genre: int) -> ApiResponse[GenreSchema]:
        """
        Get a genre by ID.

        :param id_genre: Unique genre identifier.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_genre}",
        )
        return ApiResponse(status, result, model=GenreSchema)
