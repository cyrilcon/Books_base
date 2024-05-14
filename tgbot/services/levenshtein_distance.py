from fuzzywuzzy import fuzz


async def levenshtein_search(search_text, list_of_values):
    """
    Поиск книги по расстоянию Левенштейна.
    :param search_text: Текст, который вводится для поиска.
    :param list_of_values: Список со всеми значениями.
    :return: Список с наилучшими совпадениями.
    """

    matching = []

    for current_text in list_of_values:

        # Для тестов, чтобы видеть процент схожести
        # found_title = process.extract(
        #     title_from_message, all_titles, scorer=fuzz.partial_ratio
        # )

        current_ratio = fuzz.partial_ratio(current_text, search_text)
        if current_ratio >= 60:  # Порог схожести
            matching.append(current_text)

            # # Если уже найдено 15 совпадений, завершает поиск
            # if len(matching) >= 15:
            #     break
    if len(matching) == 0:
        return None

    return matching
