from fuzzywuzzy import fuzz


async def levenshtein_search(search_text, list_of_values):
    """
    Поиск книг по расстоянию Левенштейна.
    :param search_text: Текст, который вводится для поиска.
    :param list_of_values: Список со всеми значениями.
    :return: Список с наилучшими совпадениями.
    """

    matching = []
    search_text_lower = search_text.lower()

    for current_text in list_of_values:
        current_text_lower = current_text.lower()

        # Для тестов, чтобы видеть процент схожести
        # found_title = process.extract(
        #     title_from_message, all_titles, scorer=fuzz.partial_ratio
        # )

        current_ratio = fuzz.partial_ratio(current_text_lower, search_text_lower)
        if current_ratio >= 60:  # Порог схожести
            matching.append(current_text)

            # # Если уже найдено 15 совпадений, завершает поиск
            # if len(matching) >= 15:
            #     break

    if len(matching) == 0:
        return None

    return matching
