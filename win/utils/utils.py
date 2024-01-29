"""
    Фаил с дополнительными функциями.

Functions:
--------
    open_website(site_url): Открывает веб-сайт в браузере по умолчанию.

See Also
--------
    webbrowser: Библиотека для открытия сайта в основном браузере.
"""

import webbrowser


def open_website(site_url:str) -> None:
    """
        Открывает веб-сайт в браузере по умолчанию.

    :param: site_url: (str) ссылка, которую нужно открыть.

    :return: None
    """
    webbrowser.open(site_url)
