from tgbot.api.books_base_api.base import BaseClient, ApiResponse
from tgbot.schemas import ArticleSchema


class ArticlesApi:
    def __init__(self, base_client: BaseClient, prefix: str):
        self.base_client = base_client
        self.endpoint = f"{prefix}/articles"

    async def create_article(
        self,
        link: str,
        title: str,
        language_code: str,
    ) -> ApiResponse[ArticleSchema]:
        """
        Create an article.

        :param link: Link to the Telegraph article.
        :param title: Title of the article.
        :param language_code: IETF language tag of the article.
        """

        data = {
            "link": link,
            "title": title,
            "language_code": language_code,
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=f"{self.endpoint}",
            json=data,
        )
        return ApiResponse(status, result, model=ArticleSchema)

    async def get_article_by_link(self, link: str) -> ApiResponse[ArticleSchema]:
        """
        Get an article by link.

        :param link: Link to the Telegraph article.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/link/{link}",
        )
        return ApiResponse(status, result, model=ArticleSchema)

    async def get_article_by_position(
        self, position: int
    ) -> ApiResponse[ArticleSchema]:
        """
        Get an article by position.
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/position/{position}",
        )
        return ApiResponse(status, result, model=ArticleSchema)

    async def delete_article(self, id_article: int) -> ApiResponse:
        """
        Delete an article.

        :param id_article: Unique article identifier.
        """

        status, result = await self.base_client.make_request(
            method="DELETE",
            url=f"{self.endpoint}/{id_article}",
        )
        return ApiResponse(status, result)
