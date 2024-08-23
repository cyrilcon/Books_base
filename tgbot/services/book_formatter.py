from typing import List, Dict, Any


class BookFormatter:
    """
    A class for formatting various book-related information.
    """

    @staticmethod
    def format_authors(authors: List[Dict[str, Any]]) -> str:
        """
        Converts a list of authors into a comma-separated string.

        :param authors: A list of dictionaries containing information about authors.
        :return: A string of author names separated by commas.
        """

        return ", ".join([author["author_name"] for author in authors])

    @staticmethod
    def format_file_formats(files: List[Dict[str, Any]]) -> str:
        """
        Converts a list of file formats into a comma-separated string.

        :param files: A list of dictionaries containing information about files.
        :return: A string of file formats separated by commas.
        """

        return ", ".join(f"{file['format']}" for file in files)

    @staticmethod
    def format_genres(genres: List[Dict[str, Any]]) -> str:
        """
        Converts a list of genres into a string of hashtags.

        :param genres: A list of dictionaries containing information about genres.
        :return: A string of genre hashtags separated by spaces.
        """

        return " ".join(
            [
                "#" + genre["genre_name"].strip().replace(" ", "_").lower()
                for genre in genres
            ]
        )

    @staticmethod
    def format_article(id_book: int) -> str:
        """
        Formats the book ID into an article with leading zeros.

        :param id_book: The ID of the book.
        :return: A formatted article in the form of a hashtag.
        """

        return "#{:04d}".format(id_book)
