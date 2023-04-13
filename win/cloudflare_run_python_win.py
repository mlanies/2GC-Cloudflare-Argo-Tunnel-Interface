import sys
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QCheckBox
from PyQt5.QtGui import QIcon

class App(QDialog):
    def __init__(self):
        super().__init__()

    # Создание иконки в системном трее
    self.tray_icon = QSystemTrayIcon(self)
    self.tray_icon.setIcon(QIcon('icon.png'))
    self.tray_icon.setVisible(True)
    self.tray_icon.setToolTip('Server Manager')

    # Создание контекстного меню для иконки
    menu = QMenu(self)
    
    # Добавление действий в меню
    enter_url = QAction("Ввести URL:", self)
    enter_url.triggered.connect(self.show_url_dialog)
    menu.addAction(enter_url)

    server_list = QAction("Список серверов", self)
    server_list.triggered.connect(self.show_server_list)
    menu.addAction(server_list)

    settings = QAction("Настройки", self)
    settings.triggered.connect(self.show_settings)
    menu.addAction(settings)

    exit_action = QAction("Выход", self)
    exit_action.triggered.connect(self.exit)
    menu.addAction(exit_action)

    self.tray_icon.setContextMenu(menu)

    # Создание других виджетов       
    self.url_list = QListWidget()
    self.autostart_checkbox = QCheckBox('Автозапуск программы', self)
    self.setWindowTitle('Server Manager')

    # Добавление виджетов на форму
    main_layout = QVBoxLayout()
    main_layout.addWidget(self.url_list)
    
    settings_layout = QHBoxLayout()
    settings_layout.addWidget(self.autostart_checkbox)
    main_layout.addLayout(settings_layout)

    self.setLayout(main_layout)

def show_url_dialog(self):
    # Создание диалогового окна для ввода URL
    url_dialog = QDialog(self)
    url_dialog.setWindowTitle('Введите URL')
    url_dialog.setGeometry(100, 100, 50, 100)

    url_label = QLabel('URL:', url_dialog)
    url_label.move(5, 5)

    url_edit = QLineEdit(url_dialog)
    url_edit.move(5, 25)

    ok_button = QPushButton('OK', url_dialog)
    ok_button.move(5, 45)
    
    # Обработчик нажатия на кнопку OK
    ok_button.clicked.connect(lambda: self.add_url(url_edit.text(), url_dialog))

    url_dialog.exec_()

def add_url(self, url, url_dialog):
    # Добавление URL в список
    self.url_list.addItem(url)
    url_dialog.hide()

def show_server_list(self):
    # Получение выделенного URL из списка
    selected_url = self.url_list.currentItem().text()
    
    # Генерация случайного номера порта от 1100 до 1200
    port = random.randint(1100, 1200)

    # Запуск команды cmd
    cmd_command = f'cloudflared access rdp --hostname "{selected_url}-host" --url rdp://localhost:{port}'
    os.system(cmd_command)

    # Запуск команды mstsc
    mstsc_command = f'start cmd /c mstsc /v:localhost:{port}'
    os.system(mstsc_command)

def show_settings(self):
    # Создание диалогового окна для настроек
    settings_dialog = QDialog(self)
    settings_dialog.setWindowTitle('Настройки')
    settings_dialog.setGeometry(100, 100, 300, 100)

    autostart_layout = QHBoxLayout()
    autostart_layout.addWidget(self.autostart_checkbox)

    settings_dialog.setLayout(autostart_layout)
    settings_dialog.exec_()

def exit(self):
    # Закрытие приложения
    self.tray_icon.setVisible(False)
    QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
