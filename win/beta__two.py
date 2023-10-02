import os
import sys
from typing import Any

from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction, QWidget, QDialog, QVBoxLayout, QListWidget, \
    QMessageBox, QDesktopWidget, QMenuBar, QMainWindow, QHBoxLayout, QPushButton, QLineEdit, QLabel, QGroupBox, \
    QScrollArea
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QIcon, QPixmap

import subprocess
import time
import random
from dotenv import load_dotenv

from db.db_postg import PostgresDBConnect
from db.db_sqlite import SqliteDBConnect
from super_btn import Switch

class MyWidget(QDialog):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle("Авторизация")

        layout = QVBoxLayout()

        # Добавляем два поля ввода
        label1 = QLabel("Введите логин: ")
        self.input1 = QLineEdit()  # Сохраняем поле ввода как атрибут класса
        label2 = QLabel("Пароль: ")
        self.input2 = QLineEdit()  # Сохраняем поле ввода как атрибут класса

        layout.addWidget(label1)
        layout.addWidget(self.input1)
        layout.addWidget(label2)
        layout.addWidget(self.input2)

        label3 = QLabel()

        auth_button = QPushButton("Авторизация")

        hbox = QHBoxLayout()
        hbox.addWidget(label3)
        hbox.addWidget(auth_button)

        layout.addLayout(hbox)

        auth_button.clicked.connect(self.authenticate)  # Подключаем обработчик к кнопке

        self.setLayout(layout)
        self.setFixedSize(200, 150)

    def authenticate(self):
        login = self.input1.text()  # Получаем текст из первого поля ввода
        password = self.input2.text()  # Получаем текст из второго поля ввода

        # Здесь вы можете выполнить аутентификацию с использованием введенных логина и пароля
        # В данном примере мы просто выводим их на экран
        self.app.login = login
        self.app.password = password

        self.accept()  # Закрываем диалоговое окно

class RssItem(QWidget):
    print(4)
    def __init__(self, title, date, parent = None):
        super(RssItem, self).__init__(parent)
        self.initWidget(title, date)

    def initWidget(self, title, date):
        title = QLabel(title)
        date = QLabel(date)
        btn = Switch()
        titleBox = QHBoxLayout()
        titleBox.addWidget(title)
        titleBox.addWidget(date)
        titleBox.addWidget(btn)

        self.setLayout(titleBox)


class ItemsList(QWidget):
    def __init__(self, items, parent=None):
        super(ItemsList, self).__init__(parent)
        self.initWidget(items)

    def initWidget(self, items):
        listBox = QVBoxLayout(self)
        self.setLayout(listBox)

        scroll = QScrollArea(self)
        listBox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        for item in items:
            scrollLayout.addWidget(item)
        scroll.setWidget(scrollContent)

class App(QMainWindow):
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
        self.postgres_db = PostgresDBConnect(host=HOST, user=USER, port=PORT, password=PASSWORD, database=NAME)
        self.sqlite_db = SqliteDBConnect()

        self.open_window = True
        self.authorization = False

        self.setWindowTitle('2gs')
        self.setMinimumSize(330, 200)  # minimal size of window, чтобы не баловались
        self.resize(600, 350)

        self.init_ui()


    def init_ui(self):
        self.set_icon()
        self.set_position()
        self.set_structure()

        self.tray_icon.activated.connect(self.trigger)

    def set_structure(self):
        hbox = QHBoxLayout()
        self.header(hbox)


    def header(self, hbox):
        vbox = QVBoxLayout()
        self.header_widget = QWidget()
        image_label = QLabel(self)
        pixmap = QPixmap('logo.png')
        image_label.setPixmap(pixmap)
        hbox.addWidget(image_label)

        if self.authorization:
            self.bt_2 = QPushButton("Добавить сервер")
            # self.bt_2.clicked.connect(self.btn_2_clicked)
            urls_list = self.sqlite_db.get_project_list()
            print(urls_list)
        else:
            self.bt_2 = QPushButton("Авторизация")
            # self.bt_2.clicked.connect(self.btn_2_clicked)
        hbox.addWidget(self.bt_2)
        # hbox.set
        vbox.addLayout(hbox)
        # vbox.addStretch()
        self.header_widget.setLayout(vbox)
        hbox2 = QHBoxLayout()
        items = []
        for x in range(0, 15):
            items.append(RssItem("Title no %s" % x, "2000-1-%s" % x))
        hbox2.addWidget(ItemsList(items))
        vbox.addLayout(hbox2)
        vbox.addStretch()
        self.setCentralWidget(self.header_widget)
        # self.setCentralWidget(ItemsList(items))



        # hbox.addWidget(self.bt_2)
        # self.setLayout(hbox)

        # self.setCentralWidget(self, hbox)





    def set_icon(self) -> None:
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
        self.setWindowIcon(QIcon('icon.png'))
        os.remove('icon.png')

    def set_position(self):
        desktop = QDesktopWidget().availableGeometry()
        window_rect = self.frameGeometry()
        x = desktop.width() - window_rect.width()
        y = desktop.height() - window_rect.height()
        self.move(x, y - 30)

    def trigger(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if not self.open_window:
                self.show()
            else:
                self.hide()
            self.open_window = not self.open_window
        elif reason == 1:
            self.open_windowl = False



if __name__ == '__main__':
    load_dotenv()
    NAME = os.environ.get("POSTGRES_DB", "valera_test")
    USER = os.environ.get("POSTGRES_USER", "test")
    PASSWORD = os.environ.get("POSTGRES_PASSWORD", "123")
    HOST = os.environ.get("POSTGRES_HOST", "10.10.1.61")
    PORT = os.environ.get("PORT", '5438')


    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    ex = App()
    ex.show()

    # Устанавливаем стили для приложения
    sys.exit(app.exec_())
