from typing import List, Dict, Any, Union

from pydantic import BaseModel


class BookFormatter:
    """
    A class for formatting various book-related information.
    """

    @staticmethod
    def format_authors(authors: Union[List[Dict[str, Any]], List[BaseModel]]) -> str:
        """
        Converts a list of authors into a comma-separated string.

        :param authors: A list of dictionaries or Pydantic models containing information about authors.
        :return: A string of author names separated by commas.
        """

        if authors and isinstance(authors[0], BaseModel):
            return ", ".join([getattr(author, "author_name") for author in authors])
        else:
            return ", ".join([author["author_name"] for author in authors])

    @staticmethod
    def format_file_formats(files: Union[List[Dict[str, Any]], List[BaseModel]]) -> str:
        """
        Converts a list of file formats into a comma-separated string.

        :param files: A list of dictionaries or Pydantic models containing information about files.
        :return: A string of file formats separated by commas.
        """

        if files and isinstance(files[0], BaseModel):
            return ", ".join([getattr(file, "format") for file in files])
        else:
            return ", ".join([file["format"] for file in files])

    @staticmethod
    def format_genres(genres: Union[List[Dict[str, Any]], List[BaseModel]]) -> str:
        """
        Converts a list of genres into a string of hashtags.

        :param genres: A list of dictionaries or Pydantic models containing information about genres.
        :return: A string of genre hashtags separated by spaces.
        """

        if genres and isinstance(genres[0], BaseModel):
            return " ".join(
                [
                    "#" + getattr(genre, "genre_name").strip().replace(" ", "_").lower()
                    for genre in genres
                ]
            )
        else:
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
