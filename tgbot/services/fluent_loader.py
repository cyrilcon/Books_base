from pathlib import Path
from fluent.runtime import FluentLocalization, FluentResourceLoader


def get_fluent_localization(language: str) -> FluentLocalization:
    """
    Loads FTL files for the selected language.
    :param language: Language name passed from the configuration.
    :return: FluentLocalisation object with loaded FTL files for the selected language.
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

    # If the requested language directory doesn't exist, fallback to "ru"
    language_dir = locales_dir / language
    if not language_dir.exists() or not language_dir.is_dir():
        language = "ru"
        language_dir = locales_dir / language

    # Load all .ftl files from the language directory
    locale_files = list()
    for file in language_dir.glob("*.ftl"):
        locale_files.append(str(file.absolute()))

    if not locale_files:
        err = f'No .ftl files found for "{language}" locale'
        raise FileNotFoundError(err)

    l10n_loader = FluentResourceLoader(str(locales_dir / "{locale}"))

    return FluentLocalization([language], locale_files, l10n_loader)
