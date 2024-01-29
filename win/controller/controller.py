"""
    Класс Controller представляет основную логику приложения 2GC: Server Manager.

Class:
    Controller(QObject)

See Also:
    model: (SqliteDBConnect) Класс для работы с базой данных.
    view: (MainView) Класс представление главного окна приложения.
    connect_view: (Connector) Класс представление окна для подключения к столу.
"""


import os
import subprocess
import time
import random

from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QCursor

from win.logs.log_tracker import FileLogger


class Controller(QObject):
    """
    Контроллер для управления моделью и представлением.

    ...

    Attributes:
    -----------
        :cvar: logger (FileLogger): Логгер для записи сообщений.

        :cvar: total_state (bool): Общее состояние.
        :cvar: server_states (dict): Состояния серверов.
        :cvar: process (dict): Процессы.
        :cvar: server_port (dict): Порты серверов.

        :ivar: model: Модель данных.
        :ivar: view: Основное представление.
        :ivar: connect_view: Представление подключения.

    Methods:
    -----------
    Public:
        connect_signals(): Подключает сигналы к слотам.
        set_main_input_text(): Задает текст в окне ввода URL основного представления.
        set_connect_user_info(): Получает данные пользователя и передает их в окно подключения.
        connection_management(): Управляет пробросом сокета.
        handle_switch_click(): Обрабатывает нажатие на кнопку проброса сокета к серверу.
        toggle_server_state(url): Изменяет состояние сервера.
        changing_appearance_window(): Обновляет состояния и внешний вид кнопок.
        open_connect_views(): Открывает окно подключения, если параметр open_window равен True.
        receive_data(): Получает данные пользователя и открывает RDP-соединение.

    Protect:
        _connect_to_server(url): Формирует команду для запуска сервера.
        _disconnect_socket(url): Завершает процесс.

    Private:
        __open_rdp(): Открывает RDP-соединение с указанными данными пользователя.
        __run_command(): Запускает команду.
    """
    logger = FileLogger

    total_state = False
    server_states = {}
    process = {}
    server_port = {}

    def __init__(self, model, view, connect_view):
        """
            Инициализирует экземпляр класса Controller.

        :param: model (str):  Модель данных.
        :param: view (str): Основное представление.
        :param: connect_view (str): Представление подключения.
        """
        super().__init__()
        self.model = model
        self.main_view = view
        self.connect_view = connect_view

        self.set_main_input_text()
        self.set_connect_user_info()
        self.connect_signals()

    def connect_signals(self) -> None:
        """
        Подключить сигналы к слотам.
        """
        self.main_view.switch_button.clicked.connect(self.handle_switch_click)
        self.main_view.open_connect.connect(self.open_connect_views)
        self.connect_view.data_sent.connect(self.receive_data)

    def set_main_input_text(self) -> None:
        """
        Задает текст в окне ввода url главного приложения.

        :return: None
        """
        try:
            url = self.model.get_url()
            if url:
                self.main_view.url_input.setText(url.get("url"))
            else:
                self.main_view.url_input.setPlaceholderText("введите URL")
        except Exception as ex:
            FileLogger.log_warning(ex)
            self.main_view.url_input.setPlaceholderText("введите URL")

    def set_connect_user_info(self) -> None:
        """
            Получает из дабы данные пользователя и передает их в окно подключения.

        :return: None
        """
        user_info = self.model.get_user_info()
        self.connect_view.set_user_info(user_info)

    def connection_management(self, url: str) -> None:
        """
            Управление проброса сокета.

            Обновляет данные в модели, убирает возможность сменить url во время работы,
        вызывает метод для обработки дальнейших шагов для подключения.

        :param url: (str): Url адрес для подключения
        :return: None
        """
        try:
            self.model.set_or_update_url(url)
            self.main_view.url_input.setReadOnly(not self.total_state)
            self.toggle_server_state(url)
        except Exception as ex:
            self.logger.log_warning(ex)

    def handle_switch_click(self) -> None:
        """
            Обрабатывает нажатие на кнопку проброса сокета к серверу.

        :return: None
        """
        url = self.main_view.url_input.text()
        try:
            if url:
                self.connection_management(url)
            else:
                self.main_view.empty_click()
        except Exception as ex:
            self.logger.log_warning(ex)

    def toggle_server_state(self, url: str) -> None:
        """
            Метод для изменения состояние сервера.
        Проверяет текущее состояние сервера, меняет его кнопку, запускает, либо останавливает сервер.
        :param url: (str) Имя сервера
        :return: None
        """
        self.total_state = not self.total_state
        if url in self.server_states:
            self.server_states[url] = not self.server_states[url]
        else:
            self.server_states[url] = True

        self.changing_appearance_window()

        # Запуск или остановка сервера
        if self.server_states[url]:
            self._connect_to_server(url)
        else:
            self._disconnect_socket(url)

    def changing_appearance_window(self) -> None:
        """
            Обновление состояний и внешнего вида кнопок.

        :return: None
        """
        if self.total_state:
            self.main_view.total_state = True
            self.main_view.connect_label.setCursor(QCursor(Qt.PointingHandCursor))
            self.main_view.connect_label.setPixmap(self.main_view.rdp_on.pixmap(50, 50))
        else:
            self.main_view.total_state = False
            self.main_view.connect_label.setCursor(QCursor(Qt.ArrowCursor))
            self.main_view.connect_label.setPixmap(self.main_view.rdp_off.pixmap(50, 50))

    def _connect_to_server(self, url: str) -> None:
        """
        Метод для формирования команд для запуска сервера
        :param url: (str) Название сервера.
        :return: None
        """
        url = url
        if url in self.server_port:
            port = self.server_port[url]
        else:
            port = random.randint(1100, 1200)
            self.server_port[url] = port

        cloudflared_cmd = f'cloudflared-windows-amd64.exe access rdp --hostname {url} --url rdp://127.0.0.1:{port}'

        self.__run_command(cloudflared_cmd, url)
        time.sleep(2)

    def _disconnect_socket(self, url: str) -> None:
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
                port = self.server_port[url]
                output = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True)
                lines = output.decode('utf-8').strip().split('\n')
                if lines:
                    conflicting_pid = lines[0].split()[-1]
                    os.system(f'taskkill /F /PID {conflicting_pid}')
        except Exception as ex:
            FileLogger.log_warning(ex)
            print(ex)

    def __open_rdp(self, user_name: str, domain_name: str, password: str) -> None:
        """
            Открывает RDP-соединение с указанными данными пользователя.

        :param user_name: Имя пользователя для подключения к RDP.
        :param domain_name: Доменное имя для подключения к RDP (необязательно).
        :param password: Пароль пользователя для подключения к RDP.
        :return: None
        """
        url = self.main_view.url_input.text()
        port = self.server_port[url]
        mstsc_command = f'rdp.exe /multimon /v:127.0.0.1:{port} /u:{user_name} /p:{password} '
        if domain_name:
            mstsc_command += f"/domain:{domain_name} "
        mstsc_command += f"/programtitle:2GC_{url} /title:2GC_{url}"
        self.__run_command(mstsc_command)

    def __run_command(self, command: str, url: str = None) -> None:
        """
            Метод для запуска команды
        Создает новый процесс для этой команды.
        Если передан url Добавляет эту команду в словарь.
        :param command: (str) команда для запуска в шеле.
        :param url: (str) Ключ для словаря по которому будет записана команда.
        :return:
        """
        try:
            FileLogger.log_info(f"Команда: {command[:50]}")
            process = subprocess.Popen(command, creationflags=0x08000000)
            if url:
                self.process[url] = process
        except subprocess.CalledProcessError as ex:
            FileLogger.log_warning(f"Ошибка при выполнении команды: {ex}")
            FileLogger.log_warning(f"Команда: {command[50]}")

    def open_connect_views(self, open_window: bool) -> None:
        """
        Открывает окно подключения, если параметр open_window равен True.

        :param open_window: Флаг, указывающий, нужно ли открывать окно подключения.
        :return: None
        """
        if open_window:
            self.connect_view.show()

    def receive_data(self, user_name: str, password: str, domain_name: str, save_info: bool) -> None:
        """
        Получает данные пользователя и открывает RDP-соединение.

        :param user_name: Имя пользователя для подключения к RDP.
        :param password: Пароль пользователя для подключения к RDP.
        :param domain_name: Доменное имя для подключения к RDP (необязательно).
        :param save_info: Флаг, указывающий, нужно ли сохранять информацию о пользователе.
        :return: None
        """
        try:
            if save_info:
                self.model.add_user_info(user_name, domain_name)
            self.__open_rdp(user_name, domain_name, password)
        except Exception as ex:
            print(188, ex)
