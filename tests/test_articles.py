import pytest
from httpx import AsyncClient

from config import config

prefix = config.api.prefix + config.api.v1.prefix + config.api.v1.articles

ARTICLE_DATA = {
    "link": "https://telegra.ph/Books-base-20-05-24",
    "title": "Books_base Version 2.0",
    "language_code": "en",
}


@pytest.fixture
async def create_article(client: AsyncClient):
    """
    Fixture to create an article.
    """

    response = await client.post(prefix, json=ARTICLE_DATA)
    assert response.status_code == 201
    return response.json()


class TestArticlesSuccess:
    @pytest.mark.asyncio
    async def test_create_article(self, client: AsyncClient):
        """
        Test creating a new article.
        """

        response = await client.post(prefix, json=ARTICLE_DATA)
        assert response.status_code == 201
        assert response.json()["link"] == ARTICLE_DATA["link"]

    @pytest.mark.asyncio
    async def test_get_article_by_link(self, client: AsyncClient, create_article):
        """
        Test getting an article by link.
        """

        link = ARTICLE_DATA["link"]
        response = await client.get(f"{prefix}/link/{link}")
        assert response.status_code == 200
        assert response.json()["title"] == ARTICLE_DATA["title"]

    @pytest.mark.asyncio
    async def test_get_articles_count_by_language_code(
        self, client: AsyncClient, create_article
    ):
        """
        Test getting the total number of articles by language_code.
        """

        language_code = create_article["language_code"]
        response = await client.get(f"{prefix}/{language_code}/count")
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result, int)
        assert result == 1

    @pytest.mark.asyncio
    async def test_get_article_by_language_code_and_position(
        self, client: AsyncClient, create_article
    ):
        """
        Test getting an article by language_code and position in the database.
        """

        language_code = "en"
        position = 1

        response = await client.get(f"{prefix}/{language_code}/position/{position}")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_article(self, client: AsyncClient, create_article):
        """
        Test deleting an article by ID.
        """

        id_article = create_article["id_article"]
        response = await client.delete(f"{prefix}/{id_article}")
        assert response.status_code == 204


class TestArticlesFailure:
    @pytest.mark.asyncio
    async def test_create_article_invalid_link(self, client: AsyncClient):
        """
        Test creating an article with an invalid link.
        """

        incomplete_article_data = ARTICLE_DATA.copy()
        incomplete_article_data["link"] = "example.com"

        response = await client.post(prefix, json=incomplete_article_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_article_link_already_exists(
        self, client: AsyncClient, create_article
    ):
        """
        Test creating an article with a duplicate link.
        """

        response = await client.post(prefix, json=ARTICLE_DATA)
        assert response.status_code == 409

        error_text = "Article with such a link already exists!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_article_language_code_too_long(self, client: AsyncClient):
        """
        Test creating an article with too long language_code.
        """

        article_with_too_long_language_code_data = ARTICLE_DATA.copy()
        article_with_too_long_language_code_data["language_code"] = "english"

        response = await client.post(
            prefix, json=article_with_too_long_language_code_data
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_article_by_link_not_found(self, client: AsyncClient):
        """
        Test getting an article by a non-existent link.
        """

        non_existent_link = "https://example.com"

        response = await client.get(f"{prefix}/link/{non_existent_link}")
        assert response.status_code == 404

        error_text = "Article with such a link not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_get_articles_count_by_language_code_without_articles(
        self, client: AsyncClient
    ):
        """
        Test getting the total number of articles by language_code when no articles are in the database.
        """

        language_code = "en"
        response = await client.get(f"{prefix}/{language_code}/count")
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result, int)
        assert result == 0

    @pytest.mark.asyncio
    async def test_get_articles_count_by_language_code_non_existent_language_code(
        self, client: AsyncClient
    ):
        """
        Test getting the total number of articles by a non-existent language_code.
        """

        non_existent_language_code = "english"

        response = await client.get(f"{prefix}/{non_existent_language_code}/count")
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result, int)
        assert result == 0

    @pytest.mark.asyncio
    async def test_get_article_by_language_code_and_position_not_found(
        self, client: AsyncClient
    ):
        """
        Test getting an article by a non-existent language_code and a non-existent position in the database.
        """

        non_existent_language_code = "english"
        position = 1
        non_existent_position = 9999

        response = await client.get(
            f"{prefix}/{non_existent_language_code}/position/{position}"
        )
        assert response.status_code == 404

        error_text = f"Article with language code '{non_existent_language_code}' at position {position} in the database not found!!"
        assert response.json()["detail"] == error_text

        language_code = "en"
        response = await client.get(
            f"{prefix}/{language_code}/position/{non_existent_position}"
        )
        assert response.status_code == 404

        error_text = f"Article with language code '{language_code}' at position {non_existent_position} in the database not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_article_not_found(self, client: AsyncClient):
        """
        Test deleting a non-existent order.
        """

        non_existent_id_article = 9999

        response = await client.delete(f"{prefix}/{non_existent_id_article}")
        assert response.status_code == 404

        error_text = f"Article with ID {non_existent_id_article} not found!!"
        assert response.json()["detail"] == error_text
