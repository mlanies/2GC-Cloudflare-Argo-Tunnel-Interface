import os
import subprocess
import time
import random

from PyQt5.QtCore import QObject, QEvent, Qt
from PyQt5.QtGui import QCursor

from win.logs.log_tracker import FileLogger


class Controller(QObject):
    logger = FileLogger
    def __init__(self, model, view, connect_view):
        super().__init__()
        self.model = model
        self.main_view = view
        self.connect_view = connect_view
        self.set_main_input_text()
        self.set_connect_user_info()

        self.total_state = False
        self.server_states = {}
        self.process = {}
        self.server_port = {}

        self.main_view.switch_button.clicked.connect(self.handle_switch_click)
        self.main_view.open_connect.connect(self.open_connect_views)
        self.connect_view.dataSent.connect(self.receive_data)


    def set_main_input_text(self):
        try:
            url = self.model.get_url()
            if url:
                self.main_view.url_input.setText(url.get("url"))
            else:
                self.main_view.url_input.setPlaceholderText("введите URL")
        except Exception as ex:
            FileLogger.log_warning(ex)
            self.main_view.url_input.setPlaceholderText("введите URL")

    def set_connect_user_info(self):
        user_info = self.model.get_user_info()
        self.connect_view.set_user_info(user_info)


    def handle_switch_click(self):
        url = self.main_view.url_input.text()
        try:
            if url:
                try:
                    self.model.set_or_update_url(url)
                    self.main_view.url_input.setReadOnly(not self.total_state)
                    self.toggle_server_state(url)
                except Exception as ex:
                    self.logger.log_warning(ex)
                    print(1)
            else:
                self.main_view.empty_click()
        except Exception as ex:
            self.logger.log_warning(ex)
            print(2)

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
        if self.total_state:
            self.main_view.total_state = True
            self.main_view.connect_label.setCursor(QCursor(Qt.PointingHandCursor))
            print(self.main_view.rdp_on)
            self.main_view.connect_label.setPixmap(self.main_view.rdp_on.pixmap(50, 50))
        else:
            self.main_view.connect_label.setCursor(QCursor(Qt.ArrowCursor))

            self.main_view.connect_label.setPixmap(self.main_view.rdp_off.pixmap(50, 50))
            self.main_view.total_state = False

        if self.server_states[url]:
            self.connect_to_server(url)
        else:
            self.disconnect_socket(url)

    def connect_to_server(self, url: str) -> None:
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
        current_dir = os.getcwd()

        cloudflared_cmd = f'cloudflared-windows-amd64.exe access rdp --hostname {url} --url rdp://127.0.0.1:{port}'

        self.run_command(cloudflared_cmd, url)
        time.sleep(2)

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
                port = self.server_port[url]
                output = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True)
                lines = output.decode('utf-8').strip().split('\n')
                if lines:
                    conflicting_pid = lines[0].split()[-1]
                    os.system(f'taskkill /F /PID {conflicting_pid}')
        except Exception as ex:
            FileLogger.log_warning(ex)
            print(ex)

    def open_mstsc(self, user_name, domain_name, password):
        url = self.main_view.url_input.text()
        port = self.server_port[url]
        mstsc_command = f'rdp.exe /multimon /v:127.0.0.1:{port} /u:{user_name} /p:{password} '
        if domain_name:
            mstsc_command += f"/domain:{domain_name} "
        mstsc_command += f"/programtitle:2GC_{url} /title:2GC_{url}"
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
            FileLogger.log_info(f"Команда: {command[:50]}")
            process = subprocess.Popen(command, creationflags=0x08000000)
            if url:
                self.process[url] = process
        except subprocess.CalledProcessError as ex:
            FileLogger.log_warning(f"Ошибка при выполнении команды: {ex}")
            FileLogger.log_warning(f"Команда: {command[50]}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.main_view.connect_label.underMouse():
                print(1)
                # Клик произошел именно по self.connect_label
                if self.total_state:
                    self.connector.show()

                    # self.open_mstsc()
            else:
                self.moveFlag = True
                self.movePosition = event.globalPos() - self.pos()
                self.main_view.setCursor(QCursor(Qt.OpenHandCursor))
        super().self.main_view.mousePressEvent(event)

    def open_connect_views(self, open_window):
        print(open_window)
        if open_window:
            self.connect_view.show()

    def receive_data(self, user_name, password, domain_name, save_info):
        try:
            print(f"Received data: {user_name}, {password}, {domain_name}, {save_info}")
            if save_info:
                self.model.add_user_info(user_name, domain_name)
            self.open_mstsc(user_name, domain_name, password)
        except Exception as ex:
            print(188, ex)

