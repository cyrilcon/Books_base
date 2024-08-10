import re
from typing import Tuple, List


async def genres_to_list(
    genres_from_message: str, genres: List[str] = None
) -> Tuple[List[dict], bool]:
    """
    Turns genres into a list.
    :param genres_from_message: Book genres.
    :param genres: A list with genres already recorded.
    :return: A list with genres and a flag indicating if any genre is too long.
    """

    if genres is None:
        genres = []

    new_genres = re.findall(r"\b(\w+(?:\s+\w+)*)\b", genres_from_message)
    too_long_genres = False
    new_genres = [
        {"genre": genre.strip().replace(" ", "_").lower()} for genre in new_genres
    ]

    for genre in new_genres:
        if len(genre["genre"]) > 255:
            too_long_genres = True
            break
        if genre["genre"] not in [g["genre"] for g in genres]:
            genres.append(genre)

    return genres, too_long_genres
