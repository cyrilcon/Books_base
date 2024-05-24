from fuzzywuzzy import fuzz


async def levenshtein_search_one_book(search_text, list_of_values):
    """
    Поиск книги по расстоянию Левенштейна.
    :param search_text: Текст, который вводится для поиска.
    :param list_of_values: Список со всеми книгами.
    :return: Название книги с наилучшим совпадением.
    """

    best_match = None
    best_ratio = 0

    search_text_lower = search_text.lower()

    for current_text in list_of_values:
        current_text_lower = current_text.lower()
        current_ratio = fuzz.partial_ratio(current_text_lower, search_text_lower)
        if current_ratio > best_ratio:
            best_ratio = current_ratio
            best_match = current_text

    if best_ratio >= 90:
        return best_match
    else:
        return None
