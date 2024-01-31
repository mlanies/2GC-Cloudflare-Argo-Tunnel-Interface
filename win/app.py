import sys

import psutil
from PyQt5.QtWidgets import QApplication

from controller import Controller
from views import MainView, Connector
from db.db_connector import SqliteDBConnect


class App(QApplication):
    """
        Класс для запуска приложения.
    """

    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        version = "2.0.0"
        site_url = "https://2gc.io/"
        url_views = "2gc.io"
        self.model = SqliteDBConnect()
        self.main_view = MainView(version, url_views, site_url)
        self.connect_view = Connector(version, url_views, site_url)
        self.controller = Controller(self.model, self.main_view, self.connect_view)

        self.main_view.show()
        self.main_view.setWindowTitle("2GC Free")


def pre_init():
    try:
        # Получаем список всех запущенных процессов
        processes = psutil.process_iter(['pid', 'name'])

        # Подсчитываем количество запущенных процессов с именем "2gc.exe"
        count = sum(1 for proc in processes if proc.info['name'] == "2gc.exe")
        if count > 2:
            return False
        return True

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    pi = pre_init()
    if pi:
        app = App(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        sys.exit(app.exec_())
