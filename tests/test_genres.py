import pytest
from httpx import AsyncClient

from config import config
from test_books import create_book_1, create_book_2

prefix = config.api.prefix + config.api.v1.prefix + config.api.v1.genres


class TestGenresSuccess:
    @pytest.mark.asyncio
    async def test_get_genres_with_pagination(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test getting genres with pagination.
        """

        max_results = 5
        response = await client.get(f"{prefix}?max_results={max_results}")
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0]["genre_name"] == "classic"

    @pytest.mark.asyncio
    async def test_get_genres_count(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test getting the total number of genres.
        """

        response = await client.get(f"{prefix}/count")
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result, int)
        assert result == 3

    @pytest.mark.asyncio
    async def test_search_genres(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching genres.
        """

        genre_name = "fiction"

        response = await client.get(f"{prefix}/search?genre_name={genre_name}")
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["genres"]) == 1
        assert result["genres"][0]["genre"]["genre_name"] == genre_name

        # Test pagination
        max_results = 1
        page = 1

        response = await client.get(
            f"{prefix}/search?genre_name={genre_name}&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["genres"]) == 1

        page = 2
        response = await client.get(
            f"{prefix}/search?genre_name={genre_name}&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["genres"]) == 0

    @pytest.mark.asyncio
    async def test_get_genre_by_id(self, client: AsyncClient, create_book_1):
        """
        Test getting a genre by ID.
        """

        id_genre = create_book_1["genres"][0]["id_genre"]

        response = await client.get(f"{prefix}/{id_genre}")
        assert response.status_code == 200
        assert response.json()["id_genre"] == id_genre


class TestGenresFailure:
    @pytest.mark.asyncio
    async def test_get_genres_with_pagination_without_books(self, client: AsyncClient):
        """
        Test getting genres with pagination when no books are in the database.
        """

        max_results = 5
        response = await client.get(f"{prefix}?max_results={max_results}")
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_genres_with_pagination_invalid_page(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test getting genres with pagination with an invalid page number.
        """

        max_results = 5
        page = 999

        response = await client.get(f"{prefix}?max_results={max_results}&page={page}")
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_genres_with_pagination_invalid_max_results(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test getting genres with pagination with invalid max_results parameter.
        """

        max_results = 50
        response = await client.get(f"{prefix}?max_results={max_results}")
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_genres_count_without_books(self, client: AsyncClient):
        """
        Test getting the total number of genres when no books are in the database.
        """

        response = await client.get(f"{prefix}/count")
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result, int)
        assert result == 0

    @pytest.mark.asyncio
    async def test_search_genres_without_books(self, client: AsyncClient):
        """
        Test searching genres when no books are in the database.
        """

        genre_name = "Nonexistent"
        max_results = 5

        response = await client.get(
            f"{prefix}/search?genre_name={genre_name}&max_results={max_results}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 0
        assert len(result["genres"]) == 0

    @pytest.mark.asyncio
    async def test_search_genres_without_matching_names(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching genres when no genre names match the search query.
        """

        genre_name = "Nonexistent"
        max_results = 5

        response = await client.get(
            f"{prefix}/search?genre_name={genre_name}&max_results={max_results}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 0
        assert len(result["genres"]) == 0

    @pytest.mark.asyncio
    async def test_search_genres_invalid_page(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching genres with an invalid page number.
        """

        genre_name = "Fiction"
        max_results = 5
        page = 999

        response = await client.get(
            f"{prefix}/search?genre_name={genre_name}&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["genres"]) == 0

    async def test_search_genres_invalid_max_results(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching genres with invalid max_results parameter.
        """

        genre_name = "Fiction"
        max_results = 50

        response = await client.get(
            f"{prefix}/search?genre_name={genre_name}&max_results={max_results}"
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_search_genres_invalid_similarity_threshold(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching genres with invalid similarity_threshold parameter.
        """

        genre_name = "Fiction"
        similarity_threshold = 200

        response = await client.get(
            f"{prefix}/search?genre_name={genre_name}&similarity_threshold={similarity_threshold}"
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_genre_by_id_not_found(self, client: AsyncClient):
        """
        Test getting a genre by a non-existent ID.
        """

        non_existent_id_genre = 999

        response = await client.get(f"{prefix}/{non_existent_id_genre}")
        assert response.status_code == 404

        error_text = f"Genre with ID {non_existent_id_genre} not found!!"
        assert response.json()["detail"] == error_text
