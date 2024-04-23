from infrastructure.books_base_api.base import BaseClient


class BooksApi:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client
        self.endpoint = "/books"

    async def add_book(
        self,
        id_book: int,
        title: str,
        cover: str,
        description: str,
        price: int,
        authors: list,
        genres: list,
        files: dict,
        **kwargs,
    ):
        """
        Get the latest article of the book

        :param id_book: unique book identifier
        :param title: book title
        :param cover: cover of the book is in the form of a telegram token
        :param description: book description
        :param price: book price
        :param authors: list of authors of the book
        :param genres: list of genres of the book
        :param files: dict of files of the book
        :param kwargs: additional arguments
        :return: status code and result
        """

        data = {
            "id_book": id_book,
            "title": title,
            "cover": cover,
            "description": description,
            "price": price,
            "authors": [{"author": author} for author in authors],
            "genres": [{"genre": genre} for genre in genres],
            "files": [{"format": key, "file": value} for key, value in files.items()],
        }

        status, result = await self.base_client.make_request(
            method="POST",
            url=self.endpoint,
            json=data,
        )

        return status, result

    async def get_latest_article(
        self,
        **kwargs,
    ):
        """
        Get the latest article of the book

        :param kwargs: additional arguments
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/latestArticle",
        )

        return status, result

    async def get_book(
        self,
        id_book: int,
        **kwargs,
    ):
        """
        Get a book by id with all the information

        :param id_book: unique book identifier
        :param kwargs: additional arguments
        :return: status code and result
        """

        status, result = await self.base_client.make_request(
            method="GET",
            url=f"{self.endpoint}/{id_book}",
        )

        return status, result
