import pytest
from httpx import AsyncClient

from config import config

prefix = config.api.prefix + config.api.v1.prefix + config.api.v1.books

BOOK_DATA_1 = {
    "id_book": 1,
    "title": "The Great Gatsby",
    "cover": "AgACAgIAAxkBAAJNfGKIw4w7e-Q9MPJjKjZNq490zQXEAAI-uzEbna9ISFVfOB2OcjcUAQADAgADeQADJAQ",
    "description": (
        "The Great Gatsby is a novel by American writer F. Scott Fitzgerald. "
        "Set in the Jazz Age on Long Island, near New York City, the novel depicts "
        "first-person narrator Nick Carraway's interactions with mysterious millionaire "
        "Jay Gatsby and Gatsby's obsession to reunite with his former lover, Daisy Buchanan."
    ),
    "price": 85,
    "authors": [{"author_name": "F. Scott Fitzgerald"}],
    "genres": [{"genre_name": "Fiction"}, {"genre_name": "Classic"}],
    "files": [
        {
            "format": "docx",
            "file_token": "BQACAgIAAxkBAAJMUGKHlCQlObD84b7zkMVFnJKU9DVFAAJDGAACna84SBP5VjULiaRYJAQ",
        },
        {
            "format": "pdf",
            "file_token": "BQACAgIAAxkBAAJMUmKHlC01ioUkYKwDpqNLEYoq0rs_AAJEGAACna84SAUxFcTo-8IoJAQ",
        },
        {
            "format": "fb2",
            "file_token": "BQACAgIAAxkBAAJMVGKHlDzIkLZ5xalVNLy4PYNM836PAAJFGAACna84SJ20aJz7COTBJAQ",
        },
        {
            "format": "mobi",
            "file_token": "BQACAgIAAxkBAAJMVmKHlER3X9VWYgABwwoQJCd0FuSm6wACRhgAAp2vOEhnssrdKujFRyQE",
        },
        {
            "format": "epub",
            "file_token": "BQACAgIAAxkBAAJMWGKHlFlzbmHka2y8I08hBNOZLk18AAJHGAACna84SLwxbtVSq508JAQ",
        },
    ],
}
BOOK_DATA_2 = {
    "id_book": 2,
    "title": "To Kill a Mockingbird",
    "cover": "AgACAgIAAxkBAAMFXA1yIu29weQ9MPJjKjZNq490zQXEAAJHuzEbna9ISFVfOB2OcjcUAQADAgADeQADJAQ",
    "description": (
        "To Kill a Mockingbird is a novel by Harper Lee published in 1960. "
        "Instantly successful, widely read in high schools and middle schools in the United States, "
        "it has become a classic of modern American literature. The plot and characters are loosely "
        "based on Lee's observations of her family, her neighbors and an event that occurred near "
        "her hometown of Monroeville, Alabama, in 1936, when she was 10 years old."
    ),
    "price": 50,
    "authors": [{"author_name": "Harper Lee"}],
    "genres": [
        {"genre_name": "Fiction"},
        {"genre_name": "Classic"},
        {"genre_name": "Drama"},
    ],
    "files": [
        {
            "format": "docx",
            "file_token": "BQACAgIAAxkBAAMFYA1yIuz8cz10weQ9MPJjKjZNq490zQXEAAJHGAACna84SBP5VjULiaRYJAQ",
        },
        {
            "format": "pdf",
            "file_token": "BQACAgIAAxkBAAMFZA1yIv1XLDPQ9MPJjKjZNq490zQXEAAJFGAACna84SAUxFcTo-8IoJAQ",
        },
    ],
}


@pytest.fixture
async def create_book_1(client: AsyncClient):
    """
    Fixture to create the first book.
    """

    response = await client.post(prefix, json=BOOK_DATA_1)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def create_book_2(client: AsyncClient):
    """
    Fixture to create the second book.
    """

    response = await client.post(prefix, json=BOOK_DATA_2)
    assert response.status_code == 201
    return response.json()


class TestBooksSuccess:
    @pytest.mark.asyncio
    async def test_create_book(self, client: AsyncClient):
        """
        Test adding a new book.
        """

        response = await client.post(prefix, json=BOOK_DATA_1)
        assert response.status_code == 201
        assert response.json()["id_book"] == BOOK_DATA_1["id_book"]

        response = await client.post(prefix, json=BOOK_DATA_2)
        assert response.status_code == 201
        assert response.json()["id_book"] == BOOK_DATA_2["id_book"]

    @pytest.mark.asyncio
    async def test_create_book_price_change(self, client: AsyncClient, create_book_2):
        """
        Test adding a new book that the price of an existing book with price 50 is updated to 85
        when a new book with price 50 is created.
        """

        new_book_data = BOOK_DATA_1.copy()
        new_book_data["price"] = 50

        response = await client.post(prefix, json=new_book_data)
        assert response.status_code == 201

        id_book = create_book_2["id_book"]
        response = await client.get(f"{prefix}/{id_book}")
        assert response.status_code == 200
        assert response.json()["price"] == 85

        id_book = new_book_data["id_book"]
        response = await client.get(f"{prefix}/{id_book}")
        assert response.status_code == 200
        assert response.json()["price"] == 50

    @pytest.mark.asyncio
    async def test_get_books_by_author_id(self, client: AsyncClient, create_book_1):
        """
        Test getting books by author ID.
        """

        id_author = 1

        response = await client.get(f"{prefix}/author/{id_author}")
        assert response.status_code == 200

        result = response.json()
        assert result["count"] == 1
        assert len(result["books"]) == 1
        assert (
            result["books"][0]["book"]["authors"][0]["author_name"]
            == "F. Scott Fitzgerald"
        )

        # Test pagination
        max_results = 1
        page = 1

        response = await client.get(
            f"{prefix}/author/{id_author}?&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["count"] == 1
        assert len(result["books"]) == 1

        page = 2
        response = await client.get(
            f"{prefix}/author/{id_author}?&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["count"] == 1
        assert len(result["books"]) == 0

    @pytest.mark.asyncio
    async def test_get_books_by_genre_id(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test getting books by genre ID.
        """

        id_genre = 1

        response = await client.get(f"{prefix}/genre/{id_genre}")
        assert response.status_code == 200

        result = response.json()
        assert result["count"] == 2
        assert len(result["books"]) == 2

        # Test pagination
        max_results = 1
        page = 1

        response = await client.get(
            f"{prefix}/genre/{id_genre}?&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["count"] == 2
        assert len(result["books"]) == 1

        page = 2
        response = await client.get(
            f"{prefix}/genre/{id_genre}?&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["count"] == 2
        assert len(result["books"]) == 1

    @pytest.mark.asyncio
    async def test_get_latest_article(self, client: AsyncClient):
        """
        Test getting the latest article of books.
        """

        response = await client.get(f"{prefix}/latest-article")
        assert response.status_code == 200
        assert isinstance(response.json(), int)

    @pytest.mark.asyncio
    async def test_update_book_price(self, client: AsyncClient, create_book_2):
        """
        Test updating the price of the book with a price of 50 to 85.
        """

        response = await client.patch(f"{prefix}/price")
        assert response.status_code == 200

        result = response.json()
        assert result["price"] == 85

    @pytest.mark.asyncio
    async def test_search_books_by_title(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching books by title with Levenshtein distance.
        """

        # Test exact match
        title = "The Great Gatsby"

        response = await client.get(f"{prefix}/search-by-title?title={title}")
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["books"]) == 1
        assert result["books"][0]["book"]["title"] == title

        # Test partial match with Levenshtein distance
        title = "Mockingbird"
        max_results = 5
        response = await client.get(
            f"{prefix}/search-by-title?title={title}&max_results={max_results}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["books"]) == 1
        assert result["books"][0]["book"]["title"] == "To Kill a Mockingbird"

        # Test pagination
        title = "The"
        max_results = 1
        page = 1

        response = await client.get(
            f"{prefix}/search-by-title?title={title}&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["books"]) == 1

        page = 2
        response = await client.get(
            f"{prefix}/search-by-title?title={title}&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["books"]) == 0

    @pytest.mark.asyncio
    async def test_search_books_by_title_with_duplicate_titles(
        self, client: AsyncClient
    ):
        """
        Test searching books by title with duplicate titles returns distinct books by id.
        """

        book_data_1 = BOOK_DATA_1.copy()
        book_data_2 = BOOK_DATA_2.copy()

        book_data_2["title"] = book_data_1["title"]

        response = await client.post(prefix, json=book_data_1)
        assert response.status_code == 201

        response = await client.post(prefix, json=book_data_2)
        assert response.status_code == 201

        title = "The Great Gatsby"
        response = await client.get(f"{prefix}/search-by-title?title={title}")
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 2
        assert len(result["books"]) == 2

        found_ids = [book["book"]["id_book"] for book in result["books"]]
        assert sorted(found_ids) == [book_data_1["id_book"], book_data_2["id_book"]]

    @pytest.mark.asyncio
    async def test_get_book_by_id(self, client: AsyncClient, create_book_1):
        """
        Test getting a book by ID.
        """

        id_book = create_book_1["id_book"]
        response = await client.get(f"{prefix}/{id_book}")
        assert response.status_code == 200
        assert response.json()["id_book"] == id_book

    @pytest.mark.asyncio
    async def test_update_book(self, client: AsyncClient, create_book_1):
        """
        Test updating book information.
        """

        update_data = {
            "title": "Great Gatsby",
            "authors": [{"author_name": "Harper Lee"}],
            "genres": [{"genre_name": "Drama"}],
            "files": [
                {
                    "format": "docx",
                    "file_token": "BQACAgIAAxkBAAJMUGKHlCUlObD84b7zkMVFnJKU9DVFAAJDGAACna84SBP5VjULiaRYJAQ",
                },
                {
                    "format": "jpeg",
                    "file_token": "BQACAgIAAxkBAAJMUGKHlCUlObD84b7zkMVFnJKU9DVFAAJDGAACna84SBP5VjKLiaRYJAQ",
                },
            ],
        }
        id_book = create_book_1["id_book"]
        response = await client.patch(f"{prefix}/{id_book}", json=update_data)
        assert response.status_code == 200
        assert response.json()["title"] == update_data["title"]

    @pytest.mark.asyncio
    async def test_update_book_price_change(self, client: AsyncClient, create_book_1):
        """
        Test updating book information that the price of an existing book with price 50 is updated to 85
        when another book's price is changed to 50.
        """

        book_data_50 = BOOK_DATA_2.copy()
        response = await client.post(prefix, json=book_data_50)
        assert response.status_code == 201

        id_book = create_book_1["id_book"]
        update_data = {"price": 50}
        response = await client.patch(f"{prefix}/{id_book}", json=update_data)
        assert response.status_code == 200

        id_book = book_data_50["id_book"]
        response = await client.get(f"{prefix}/{id_book}")
        assert response.status_code == 200
        assert response.json()["price"] == 85

        id_book = create_book_1["id_book"]
        response = await client.get(f"{prefix}/{id_book}")
        assert response.status_code == 200
        assert response.json()["price"] == 50

    @pytest.mark.asyncio
    async def test_delete_book(self, client: AsyncClient, create_book_1):
        """
        Test deleting a book.
        """

        id_book = create_book_1["id_book"]
        response = await client.delete(f"{prefix}/{id_book}")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_file(self, client: AsyncClient, create_book_1):
        """
        Test deleting a file of the book by its format.
        """

        id_book = create_book_1["id_book"]
        file_format = create_book_1["files"][0]["format"]

        response = await client.delete(f"{prefix}/{id_book}/file/{file_format}")
        assert response.status_code == 204


class TestBooksFailure:
    @pytest.mark.asyncio
    async def test_create_book_with_too_long_data(self, client: AsyncClient):
        """
        Test creating a book with too long data.
        """

        long_lorem_text = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit." * 20
        )

        too_long_data = BOOK_DATA_1.copy()
        too_long_data["title"] = long_lorem_text
        response = await client.post(prefix, json=too_long_data)
        assert response.status_code == 422

        too_long_data = BOOK_DATA_1.copy()
        too_long_data["cover"] = long_lorem_text
        response = await client.post(prefix, json=too_long_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_book_with_double_quote_in_title(self, client: AsyncClient):
        """
        Test creating a book with a double quote in the title.
        """

        double_quote_data = BOOK_DATA_1.copy()
        double_quote_data["title"] = 'The "Great" Gatsby'

        response = await client.post(prefix, json=double_quote_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_book_already_exists(self, client: AsyncClient, create_book_1):
        """
        Test creating two books with the same id.
        """

        id_user = create_book_1["id_book"]

        the_same_id_data = BOOK_DATA_2.copy()
        the_same_id_data["id_book"] = id_user

        response = await client.post(prefix, json=the_same_id_data)
        assert response.status_code == 409

        error_text = f"Book with ID {id_user} already exists!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_book_cover_already_exists(
        self, client: AsyncClient, create_book_1
    ):
        """
        Test creating two books with the same cover.
        """

        same_cover_data = BOOK_DATA_2.copy()
        same_cover_data["cover"] = BOOK_DATA_1["cover"]

        response = await client.post(prefix, json=same_cover_data)
        assert response.status_code == 409

        error_text = "Such a cover already exists!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_books_duplicate_file(
        self, client: AsyncClient, create_book_1
    ):
        """
        Test creating two books with the same file.
        """

        same_file_data = BOOK_DATA_2.copy()
        same_file_data["files"] = BOOK_DATA_1["files"]

        response = await client.post(prefix, json=same_file_data)
        assert response.status_code == 409

        error_text = "Such a file already exists!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_get_books_by_author_id_without_books(self, client: AsyncClient):
        """
        Test getting books by author ID when no books are in the database.
        """

        id_author = 1

        response = await client.get(f"{prefix}/author/{id_author}")
        assert response.status_code == 404

        error_text = f"Author with ID {id_author} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_get_books_by_author_id_invalid_page(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test getting books by author ID with an invalid page number.
        """

        id_author = 1
        max_results = 1
        page = 999

        response = await client.get(
            f"{prefix}/author/{id_author}?&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["count"] == 1
        assert len(result["books"]) == 0

    @pytest.mark.asyncio
    async def test_get_books_by_author_id_invalid_max_results(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test getting books by author ID with invalid max_results parameter.
        """

        id_author = 1
        max_results = 50

        response = await client.get(
            f"{prefix}/author/{id_author}?&max_results={max_results}"
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_books_by_genre_id_without_books(self, client: AsyncClient):
        """
        Test getting books by genre ID when no books are in the database.
        """

        id_genre = 1

        response = await client.get(f"{prefix}/genre/{id_genre}")
        assert response.status_code == 404

        error_text = f"Genre with ID {id_genre} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_get_books_by_genre_id_invalid_page(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test getting books by genre ID with an invalid page number.
        """

        id_genre = 1
        max_results = 1
        page = 999

        response = await client.get(
            f"{prefix}/genre/{id_genre}?&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["count"] == 2
        assert len(result["books"]) == 0

    @pytest.mark.asyncio
    async def test_get_books_by_genre_id_invalid_max_results(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test getting books by genre ID with invalid max_results parameter.
        """

        id_genre = 1
        max_results = 50

        response = await client.get(
            f"{prefix}/genre{id_genre}?&max_results={max_results}"
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_book_price_not_found(self, client: AsyncClient):
        """
        Test updating the price of the book with a price of 50 to 85 when no books are in the database.
        """

        response = await client.patch(f"{prefix}/price")
        assert response.status_code == 404

        error_text = f"No book with a price of 50 found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_search_books_by_title_without_books(self, client: AsyncClient):
        """
        Test searching books when no books are in the database.
        """

        title = "Nonexistent"
        max_results = 5

        response = await client.get(
            f"{prefix}/search-by-title?title={title}&max_results={max_results}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 0
        assert len(result["books"]) == 0

    @pytest.mark.asyncio
    async def test_search_books_by_title_without_matching_titles(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching books when no titles match the search query.
        """

        title = "Nonexistent"
        max_results = 5

        response = await client.get(
            f"{prefix}/search-by-title?title={title}&max_results={max_results}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 0
        assert len(result["books"]) == 0

    @pytest.mark.asyncio
    async def test_search_books_by_title_invalid_page(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching books with an invalid page number.
        """

        title = "The"
        max_results = 5
        page = 999

        response = await client.get(
            f"{prefix}/search-by-title?title={title}&max_results={max_results}&page={page}"
        )
        assert response.status_code == 200

        result = response.json()
        assert result["found"] == 1
        assert len(result["books"]) == 0

    @pytest.mark.asyncio
    async def test_search_books_by_title_invalid_max_results(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching books with invalid max_results parameter.
        """

        title = "The"
        max_results = 50

        response = await client.get(
            f"{prefix}/search-by-title?title={title}&max_results={max_results}"
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_search_books_by_title_invalid_similarity_threshold(
        self, client: AsyncClient, create_book_1, create_book_2
    ):
        """
        Test searching books with invalid similarity_threshold parameter.
        """

        title = "The"
        similarity_threshold = 200

        response = await client.get(
            f"{prefix}/search-by-title?title={title}&similarity_threshold={similarity_threshold}"
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_book_by_id_not_found(self, client: AsyncClient):
        """
        Test getting a book by a non-existent ID.
        """

        non_existent_id_book = 9999

        response = await client.get(f"{prefix}/{non_existent_id_book}")
        assert response.status_code == 404

        error_text = f"Book with ID {non_existent_id_book} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_update_book_not_found(self, client: AsyncClient):
        """
        Test updating a book by a non-existent ID.
        """

        non_existent_id_book = 9999
        update_data = {
            "title": "Updated Title",
            "authors": [{"author_name": "Updated Author"}],
            "genres": [{"genre_name": "Updated Genre"}],
            "files": [{"format": "pdf", "file_token": "Updated File"}],
        }

        response = await client.patch(
            f"{prefix}/{non_existent_id_book}", json=update_data
        )
        assert response.status_code == 404

        error_text = f"Book with ID {non_existent_id_book} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_update_book_with_double_quote_in_title(
        self, client: AsyncClient, create_book_1
    ):
        """
        Test updating a book with a double quote in the title.
        """

        update_data = {
            "title": 'The "Great" Gatsby',
        }

        id_book = create_book_1["id_book"]
        response = await client.patch(f"{prefix}/{id_book}", json=update_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_book_not_found(self, client: AsyncClient):
        """
        Test deleting a non-existent book.
        """

        non_existent_id_book = 9999

        response = await client.delete(f"{prefix}/{non_existent_id_book}")
        assert response.status_code == 404

        error_text = f"Book with ID {non_existent_id_book} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_file_book_not_found(self, client: AsyncClient, create_book_1):
        """
        Test deleting a file of a non-existent book by its format.
        """

        non_existent_id_book = 9999
        file_format = create_book_1["files"][0]["format"]

        response = await client.delete(
            f"{prefix}/{non_existent_id_book}/file/{file_format}"
        )
        assert response.status_code == 404

        error_text = f"Book with ID {non_existent_id_book} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_file_format_not_found(
        self, client: AsyncClient, create_book_1
    ):
        """
        Test deleting a file of the book by a non-existent format.
        """

        id_book = create_book_1["id_book"]
        non_existent_file_format = "abc"

        response = await client.delete(
            f"{prefix}/{id_book}/file/{non_existent_file_format}"
        )
        assert response.status_code == 404

        error_text = f"File with format '{non_existent_file_format}' for book with ID {id_book} not found!!"
        assert response.json()["detail"] == error_text
