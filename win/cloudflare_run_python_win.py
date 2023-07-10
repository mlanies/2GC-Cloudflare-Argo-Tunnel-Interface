import sys

from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction, QWidget, QDialog, QVBoxLayout, QHBoxLayout, \
    QListWidget, QMessageBox, QCheckBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QIcon

from get_requests import get_projects_url


class App(QWidget):
    """
    Класс приложения

    """

    def __init__(self) -> None:
        """
        инизализатор класса
        Вызвыает инизиализатор родительского класса.
        Задает изначальные параметры:
            self.setWindowTitle : Заголовок окна
        Создает изначальные виджеты:
            self.tray_icon : Создание иконки в системном трее
             self.menu : Меню программы.
             self.url_list : Список юрлов

        """
        super().__init__()
        self.setWindowTitle('Server Manager')

        self.tray_icon = QSystemTrayIcon(self)
        self.menu = QMenu(self)
        self.url_list = QListWidget()
        self.__pattern = "rdp"

        self.autostart_checkbox = QCheckBox('Автозапуск программы', self)
        self.setWindowTitle('Server Manager')

        # Добавление виджетов на форму
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.url_list)

        settings_layout = QHBoxLayout()
        settings_layout.addWidget(self.autostart_checkbox)
        main_layout.addLayout(settings_layout)

        self.setLayout(main_layout)
        self.initUI()

    def initUI(self) -> None:
        """
        Метод для загрузки всех методов
        :return:
        """
        self.show_icon()
        self.set_menu()

    def show_icon(self) -> None:
        """
        Метод создает иконку в трее
        :return:
        """
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('images/icon.png'))
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip('Server Manager')

    def set_menu(self) -> None:
        """
        Метод для добавления меню
        :return:
        """
        server_list = QAction("Список серверов", self)
        server_list.triggered.connect(self.show_server_list)
        self.menu.addAction(server_list)

        server_list = QAction("Изменить паттерн", self)
        server_list.triggered.connect(self.set_pattern)
        self.menu.addAction(server_list)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.exit)
        self.menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.menu)

    def chech_urls(self, urls: list) -> bool:
        """
        Проверка наличия urls
        :param urls: list список url
        :return: bool Возращает True если удалось получить коректные url, в противном случае вызывает сообщение с ошибкой
        """
        if urls:
            return True
        self.get_message_box("Ошибочка", "Не найдено подходящих url")
        return False

    def get_message_box(self, title: str, message: str) -> None:
        """
        Методя для вывода предупреждающих сообщений
        :param title: str Заголовок окна
        :param message: str Сообщение с ошибкой
        :return: None
        """
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()

    def show_server_list(self) -> None:
        """
        Метод для добавления юрлов в меню
        Получает urls из get_requests
        Проверяет наличие хотя бы одного urla
        :return: None
        """
        self.menu.clear()
        urls = get_projects_url(self.__pattern)
        if self.chech_urls(urls):
            for url in urls:
                server_url = self.menu.addMenu(f"{url}")
                server_url.addAction("Включить")
                server_url.addAction("Выключить")
            self.set_menu()

    def set_pattern(self):
        """
        Функция для изменения паттерна поиска приложений.
        Создает диалоговое окно, которое запрашивает у пользователя новый паттерн
        :return: None
        """
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Изменение паттерна сайта")
        dialog.setLabelText("Введите новый паттерн")
        dialog.setOkButtonText("Применить")
        dialog.setCancelButtonText("Отмена")
        if dialog.exec_() == QDialog.Accepted:
            text = dialog.textValue()
            self.__pattern = text

    def exit(self):
        self.tray_icon.setVisible(False)
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    ex = App()
    sys.exit(app.exec_())
