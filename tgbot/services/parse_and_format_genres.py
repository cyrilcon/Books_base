import re
from typing import Tuple, List, Dict


async def parse_and_format_genres(
    genres_from_message: str, genres: List[Dict[str, str]] = None
) -> Tuple[List[Dict[str, str]], bool]:
    """
    Parses and formats a string of genres into a list of dictionaries, checking for duplicates and length constraints.

    :param genres_from_message: String containing book genres separated by spaces.
    :param genres: Optional. A list of existing genre dictionaries to append to. Defaults to None.
    :return: A tuple containing:
             - A list of dictionaries, each with a 'genre' key and lowercase, underscore-separated value.
             - A boolean flag indicating if any genre exceeds 255 characters in length.
    """

    if genres is None:
        genres = []

    new_genres = re.findall(r"\b(\w+(?:\s+\w+)*)\b", genres_from_message)
    genre_too_long = False
    new_genres = [{"genre_name": genre} for genre in new_genres]

    for genre in new_genres:
        if len(genre["genre_name"]) > 255:
            genre_too_long = True
            break
        if genre["genre_name"] not in [g["genre_name"] for g in genres]:
            genres.append(genre)

    return genres, genre_too_long
