import os
import sys
from typing import Any

from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction, QWidget, QDialog, QVBoxLayout, QListWidget, \
    QMessageBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QIcon

import subprocess
import time
import random


class App(QWidget):
    """
    App - Класс для управления серверами через графический интерфейс.

    Этот класс представляет собой графический интерфейс для управления серверами. Он создает окно с системным треем,
     список URL-адресов серверов и обеспечивает функциональность для включения и выключения серверов.

    Attributes:
        tray_icon (QSystemTrayIcon): Объект системного трея для отображения иконки в системном трее.
        menu (QMenu): Контекстное меню для системной иконки в системном трее.
        url_list (QListWidget): Виджет для отображения списка URL-адресов серверов.
        urls_list (list): Список URL-адресов серверов, полученных с помощью метода get_urls().
        server_states (dict): Словарь для отслеживания состояния серверов (включен/выключен).
        process (dict): Словарь для хранения процессов, связанных с серверами.

    Methods:
        __init__(): Конструктор класса, инициализирует основные компоненты интерфейса и переменные.
        initUI(): Метод для загрузки всех методов.
        show_icon(): Метод создает иконку в трее.
        set_menu(): Метод для добавления основных пунктов в меню.
        get_message_box(title: str, message: str): Методя для вывода предупреждающих сообщений.
        show_server_list(): Метод для добавления юрлов в меню.
        connect_to_server(url: str): Метод для формирования команд для запуска сервера.
        run_command(command: str, url: str=None): Метод для запуска команды.
        toggle_server_state(url: str): Метод для изменения состояние сервера.
        disconnect_socket(url: str): Метод для завершения процесса.
        add_application(): Метод для добавления нового url.
        save_url(url: str): Метод для добавления нового url в базу данных.
        del_line(url: str): Метод для удаление записи из базы данных.
        del_all(): Метод для очищения базы данных.
        get_urls(): Метод для получения записей из базы данных.
        create_dir(): Метод для получения пути до папки в которой будет храниться база данных.
        exit(): Метод для заверения работы приложения.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Server Manager')

        self.tray_icon = QSystemTrayIcon(self)
        self.menu = QMenu(self)
        self.url_list = QListWidget()

        self.setWindowTitle('Server Manager')

        # Добавление виджетов на форму
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.url_list)

        self.urls_list = self.get_urls()
        self.server_states = {}
        self.process = {}

        self.setLayout(main_layout)
        self.init_ui()

    def init_ui(self) -> None:
        """
        Метод для загрузки всех методов
        :return:
        """
        self.show_icon()

        self.show_server_list()

    def show_icon(self) -> None:
        """
        Метод создает иконку в трее
        :return:
        """
        images = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x03\x00\x00\x00D\xa4\x8a\xc6\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00 cHRM\x00\x00z&\x00\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17p\x9c\xbaQ<\x00\x00\x015PLTE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xb0\xc5o\xed\x00\x00\x00etRNS\x00\xfe\xf7\xf6\xf8\xfd\xe8V>\xe9\xf9n<?D\xca\xdaM\xe1\x1e\x07\xba\xce\x12\xcf\xed{h\xee\x08\xbb\x13\xbc\xd2\x15\xf3\xa3\x95\x96\x91%\x05o\x97\xc3\xdf\x1dk\xe2 \xe32\x85$\x04\xc2=\xb9E\xb8F_`i;\xb7\xf5\x06\xb6v\xb5\x8e\xab\xb4\xfc\xfa:\xac\xa9\xa1\xad\xf4Z\xbe\xdd\xd1\x14\x1f\xfbJ\x02q\x8c\x03l\xf1\x92L\x9a\xe5t\xb7\x0b3S\x00\x00\x00\x01bKGDf,\xd4\xd9%\x00\x00\x00\tpHYs\x00\x00\x9d{\x00\x00\x9d{\x01<\x9fw\xc4\x00\x00\x01.IDAT8\xcb\xbd\xd3WS\xc2@\x10\x07\xf0M.\x81\x13\x12\x0b\xa8\x08D#\x96\xa0b\x01Q\xc4\x8a\xbd\x80\x8a\r{\xd7\xfd\xfe_\xc1\x8d7\xe3\xe8\xe4.\xbe\xb1o\xff\x99\xdf\xc3\xee\xde\x1e\xe0?\x05m\x03\x9a\xce\x98\xae\xa1\xc1\x183\x11M\x91~\x83H\x94\xf3hG,n\xd9\x9d]\x88\xdd=\x94"\x7f@"\t\x90L\x186@o\x1fb\x7f\xcaO!` \x08\xd2\x99l6\xe3\xe8\x04\x06\x87\x08\xb8\x01 \x8a\xf9`\x1817\x12\x00\xa3c\xe3\x9e\xe7\xe5\'\x00&\xa7\n\xd33\xb3\xd2\x1e~j\xaeH\xa9T\x0c\x01\xf3%\x80\xb2\x13\x00\xa9\x85\xfc"@%^Xr\xca\x006\x93\x8c\xa9W\xc5\x14~\xb3R\xc0,\xda\xc3\xb2\x00+\x86\n\xac"\x1ak\x00\xebZ\x08\xd06\x00j(\x03\x9b\x04\xb6(\xd6\x14`\x9b\xc0\xce\xae\x00{J\xb0O\xf1\xc0\xe2\x87JpD\xb1\xdeh\x98RpL\x8b:AtN\x9b\xcd\xb3s\xd9\xa28-\xfa\xe2\xf2\xaau\rp#;\x98\xdb;\x02\xf7\x95\x87\x9c\xab\xb8(||\xf2\x1f\xeb\xb9\xe5\xca/*\x8d/\xafo\xdc\xae\xbe\x7f|~\'\xe9\xbf\x88\xd1\xe1\xd7%\xffB]m\x00_\x07\xa2\x13gn\x12\xc1`\x00\x00\x00%tEXtdate:create\x002018-05-10T16:04:56+02:00\xcf.R2\x00\x00\x00%tEXtdate:modify\x002018-05-10T16:04:56+02:00\xbes\xea\x8e\x00\x00\x00FtEXtsoftware\x00ImageMagick 6.7.8-9 2016-06-16 Q16 http://www.imagemagick.org\xe6\xbf4\xb6\x00\x00\x00\x18tEXtThumb::Document::Pages\x001\xa7\xff\xbb/\x00\x00\x00\x18tEXtThumb::Image::height\x00512\xc0\xd0PQ\x00\x00\x00\x17tEXtThumb::Image::Width\x00512\x1c|\x03\xdc\x00\x00\x00\x19tEXtThumb::Mimetype\x00image/png?\xb2VN\x00\x00\x00\x17tEXtThumb::MTime\x001525961096\x03\xcd\xb6\r\x00\x00\x00\x13tEXtThumb::Size\x005.87KBB-\x89\xd7\xda\x00\x00\x00DtEXtThumb::URI\x00file://./uploads/56/ZiPz5oE/1463/scoopit-black_100109.png\x9b\x9b\xc0\xec\x00\x00\x00\x00IEND\xaeB`\x82'
        with open('icon.png', 'wb') as f:
            f.write(images)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.png'))
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip('Server Manager')
        os.remove('icon.png')

    def set_menu(self) -> None:
        """
        Метод для добавления основных пунктов в меню
        :return:
        """
        server_list = QAction("Добавить приложение", self)
        server_list.triggered.connect(self.add_application)
        self.menu.addAction(server_list)

        if any(self.urls_list):
            clear_all = QAction("Удалить все url", self)
            clear_all.triggered.connect(self.del_all)
            self.menu.addAction(clear_all)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.exit)
        self.menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.menu)

    def get_message_box(self, title: str, message: str) -> None:
        """
        Методя для вывода предупреждающих сообщений
        :param title: str Заголовок окна
        :param message: str Сообщение с ошибкой
        :return: None
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)

        msg.setText(message)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()

    def show_server_list(self) -> None:
        """
        Метод для добавления юрлов в меню
        Проверяет наличие строки, если она не пустая добавляет её в меню
        :return: None
        """
        self.menu.clear()

        for url in self.urls_list:
            if url:
                server_url = self.menu.addMenu(f"{url}")

                def make_lambda(u):
                    return lambda checked, url=u: self.toggle_server_state(url)

                def del_url(u):
                    return lambda checked, url=u: self.del_line(url)

                action_toggle = QAction("Выключить" if self.server_states.get(url, False) else "Включить", self)
                action_toggle.triggered.connect(make_lambda(url))
                server_url.addAction(action_toggle)

                action_disable = QAction("Удалить из списка", self)
                action_disable.triggered.connect(del_url(url))
                server_url.addAction(action_disable)
        self.set_menu()

    def connect_to_server(self, url: str) -> None:
        """
        Метод для формирования команд для запуска сервера
        :param url: (str) Название сервера.
        :return: None
        """
        # url = "vm-srv-office.team108.ru"

        url = url
        port = random.randint(1100, 1200)

        cloudflared_cmd = f'cloudflared access rdp --hostname {url} --url rdp://localhost:{port}'

        self.run_command(cloudflared_cmd, url)

        time.sleep(2)

        mstsc_command = f'start cmd /c mstsc /v:localhost:{port}'
        self.run_command(mstsc_command)

    def run_command(self, command: str, url: str = None) -> None:
        """
            Метод для запуска команды
        Создает новый процесс для этой команды.
        Если передан url Добавляет эту команду в словарь.
        :param command: (str) команда для запуска в шеле.
        :param url: (str) Ключ для словаря по которому будет записана команда.
        :return:
        """
        try:
            process = subprocess.Popen(command, shell=True)
            if url:
                self.process[url] = process
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении команды: {e}")

    def toggle_server_state(self, url: str) -> None:
        """
            Метод для изменения состояние сервера.
        Проверяет текущее состояние сервера, меняет его кнопку, запускает, либо останавливает сервер.
        :param url: (str) Имя сервера
        :return: None
        """
        if url in self.server_states:
            self.server_states[url] = not self.server_states[url]
        else:
            self.server_states[url] = True
        # Получаем соответствующий QAction
        action_toggle = self.sender()
        if action_toggle:
            action_toggle.setText("Выключить" if self.server_states[url] else "Включить")

        # Дополнительно, если хотите, можете вызвать функцию connect_to_server или disconnect_socket здесь
        if self.server_states[url]:
            self.connect_to_server(url)
        else:
            self.disconnect_socket(url)

    def disconnect_socket(self, url: str) -> None:
        """
            Метод для завершения процесса.
        Находит процесс по ключу, останавливает его и удаляет из словаря процессов.
        :param url: (str) Ключ по которому будет найдем соответствующий процесс.

        :return: None.
        """
        try:
            if url in self.process:
                self.process[url].terminate()
                del self.process[url]
        except Exception as e:
            print(e)

    def add_application(self) -> None:
        """
            Метод для добавления нового url.
        Создает диалоговое окно, которое запрашивает у пользователя новый новый url без https://.
        :return: None
        """
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Новый сайт")
        dialog.setLabelText("Введите url: https://...")
        dialog.setOkButtonText("Применить")
        dialog.setCancelButtonText("Отмена")
        if dialog.exec_() == QDialog.Accepted:
            text = dialog.textValue()
            self.save_url(text)
            self.urls_list.append(text)
            self.show_server_list()

    def save_url(self, url: str) -> None:
        """
            Метод для добавления нового url в базу данных.
        :param url: (str) url адрес, который будет добавлен в базу данных.
        :return: None
        """
        path = self.create_dir()
        data_path = os.path.join(path, "data.txt")
        with open(data_path, "a") as f:
            f.write(f"{url}\n")

    def del_line(self, url: str) -> None:
        """
            Метод для удаление записи из базы данных.
        :param url: (str) Запись которую нужно удалить.
        :return: None
        """
        self.menu.clear()
        urls_list = self.get_urls()
        path = self.create_dir()
        data_path = os.path.join(path, "data.txt")
        with open(data_path, "w") as f:
            for u in urls_list:
                if u != url:
                    f.write(f"{u}\n")
        self.urls_list.remove(url)
        self.show_server_list()

    def del_all(self) -> None:
        """
            Метод для очищения базы данных.
        :return: None
        """
        self.urls_list.clear()
        path = self.create_dir()
        data_path = os.path.join(path, "data.txt")
        with open(data_path, "w") as f:
            pass
        self.show_server_list()

    def get_urls(self) -> Any:
        """
            Метод для получения записей из базы данных
        Проверяет наличие базы данных, если она еще не создана, создает пустую базу
        :return: None
        """
        path = self.create_dir()
        data_path = os.path.join(path, "data.txt")
        try:
            with open(data_path, "r") as f:
                data = f.read()
                return data.split("\n")
        except FileNotFoundError:
            with open(data_path, "a") as f:
                os.system(f'attrib +h "data.txt"')
                return []
        except Exception as ex:
            self.get_message_box("Что то не так с базой данных", ex)

    def exit(self) -> None:
        """
            Метод для заверения работы приложения.
        :return: None
        """
        self.tray_icon.setVisible(False)
        QApplication.quit()

    def create_dir(self) -> str:
        """
            Метод для получения пути до папки в которой будет храниться база данных.
        :return: (str) Путь до базы данных
        """
        db_path = os.path.join(os.environ["USERPROFILE"])
        if not "media108" in os.listdir(db_path):
            os.makedirs(os.path.join(db_path, "media108"))
        return os.path.join(db_path, "media108")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    ex = App()
    sys.exit(app.exec_())
