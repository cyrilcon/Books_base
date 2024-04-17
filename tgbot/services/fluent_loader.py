from pathlib import Path
from fluent.runtime import FluentLocalization, FluentResourceLoader


def get_fluent_localization(language: str) -> FluentLocalization:
    """
    Загружает файлы FTL для выбранного языка
    :param language: название языка, передаваемое из конфигурации
    :return: Объект FluentLocalization с загруженными файлами FTL для выбранного языка
    """

    # Check "locales" directory on the same level as this file
    locales_dir = Path(__file__).parent.parent / "locales"
    if not locales_dir.exists():
        err = '"locales" directory does not exist'
        raise FileNotFoundError(err)
    if not locales_dir.is_dir():
        err = '"locales" is not a directory'
        raise NotADirectoryError(err)

    locales_dir = locales_dir.absolute()
    locale_dir_found = False
    for directory in Path.iterdir(locales_dir):
        if directory.stem == language:
            locale_dir_found = True
            break
    if not locale_dir_found:
        err = f'Directory for "{language}" locale not found'
        raise FileNotFoundError(err)

    locale_files = list()
    for file in Path.iterdir(locales_dir):
        if file.suffix == ".ftl" and file.stem == language:
            locale_files.append(str(file.absolute()))

    l10n_loader = FluentResourceLoader(str(locales_dir / "{locale}"))

    return FluentLocalization([language], locale_files, l10n_loader)
