import pytest
from httpx import AsyncClient

from config import config
from test_books import create_book_1, create_book_2

prefix = config.api.prefix + config.api.v1.prefix + config.api.v1.authors


class TestAuthorsSuccess:
    @pytest.mark.asyncio
    async def test_search_authors(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching authors.
        """

        response = await client.get(f"{prefix}/search?author_name=F. Scott Fitzgerald")
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["authors"]) == 1
        assert result["authors"][0]["author"]["author_name"] == "F. Scott Fitzgerald"

        # Test pagination
        author_name = "F. Scott Fitzgerald"
        max_results = 1
        page = 1

        response = await client.get(
            f"{prefix}/search?author_name={author_name}&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["authors"]) == 1

        page = 2
        response = await client.get(
            f"{prefix}/search?author_name={author_name}&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["authors"]) == 0

    @pytest.mark.asyncio
    async def test_get_author_by_id(self, client: AsyncClient, create_book_1):
        """
        Test getting an author by ID.
        """

        id_author = create_book_1["authors"][0]["id_author"]
        response = await client.get(f"{prefix}/{id_author}")
        assert response.status_code == 200
        assert response.json()["id_author"] == id_author


class TestAuthorsFailure:
    @pytest.mark.asyncio
    async def test_search_authors_without_books(self, client: AsyncClient):
        """
        Test searching authors when no books are in the database.
        """

        author_name = "Nonexistent"
        max_results = 5

        response = await client.get(
            f"{prefix}/search?author_name={author_name}&max_results={max_results}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 0
        assert len(result["authors"]) == 0

    @pytest.mark.asyncio
    async def test_search_authors_without_matching_titles(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching authors when no author names match the search query.
        """

        author_name = "Nonexistent"
        max_results = 5

        response = await client.get(
            f"{prefix}/search?author_name={author_name}&max_results={max_results}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 0
        assert len(result["authors"]) == 0

    @pytest.mark.asyncio
    async def test_search_authors_invalid_page(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching authors with an invalid page number.
        """

        author_name = "F"
        max_results = 5
        page = 999

        response = await client.get(
            f"{prefix}/search?author_name={author_name}&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["authors"]) == 0

    @pytest.mark.asyncio
    async def test_search_authors_invalid_max_results(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching authors with invalid max_results parameter.
        """

        author_name = "F"
        max_results = 50

        response = await client.get(
            f"{prefix}/search?author_name={author_name}&max_results={max_results}"
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_search_authors_invalid_similarity_threshold(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching authors with invalid similarity_threshold parameter.
        """

        author_name = "F"
        similarity_threshold = 200

        response = await client.get(
            f"{prefix}/search?author_name={author_name}&similarity_threshold={similarity_threshold}"
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_author_by_id_not_found(self, client: AsyncClient):
        """
        Test getting an author by a non-existent ID.
        """

        non_existent_id_author = 9999

        response = await client.get(f"{prefix}/{non_existent_id_author}")
        assert response.status_code == 404

        error_text = f"Author with ID {non_existent_id_author} not found!!"
        assert response.json()["detail"] == error_text
