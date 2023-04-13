import random
import subprocess
import sys

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QCheckBox, QInputDialog

# Функция для запуска cmd-команды
def run_command(command):
    subprocess.call(command, shell=True)

# Функция для генерации случайного порта
def generate_port():
    return random.randint(1100, 1200)

# Функция для сохранения URL в списке серверов
def save_url(url):
    # Реализация сохранения URL в списке серверов

# Функция для запуска RDP-сессии
def start_rdp_session(url):
    port = generate_port()
    run_command('cloudflared access rdp --hostname {} --url rdp://localhost:{}'.format(url, port))
    run_command('cmd /c mstsc /v:localhost:{}'.format(port))

# Функция для открытия окна настроек
def open_settings():
    # Реализация открытия окна настроек

# Функция для обработки нажатия на кнопку "Ввести URL"
def handle_url_input():
    url, ok_pressed = QInputDialog.getText(None, "Ввести URL", "Введите адрес URL:")
    if ok_pressed and url:
        save_url(url)

# Функция для обработки нажатия на кнопку "Настройки"
def handle_settings():
    # Реализация обработки настроек

# Функция для обработки нажатия на сохраненный URL в списке серверов
def handle_saved_url(url):
    start_rdp_session(url)

# Создание приложения и трея
app = QApplication(sys.argv)
tray_icon = QSystemTrayIcon(app)
tray_icon.setIcon(QIcon("icon.png"))

# Создание меню трея
menu = QMenu()
menu.addAction(QAction("Ввести URL", menu, triggered=handle_url_input))
menu.addSeparator()
menu.addAction(QAction("Настройки", menu, triggered=handle_settings))
menu.addSeparator()
# Добавление сохраненных URL в список
# Реализуйте этот блок кода в соответствии с вашей программой
for saved_url in saved_urls:
    menu.addAction(QAction(saved_url, menu, triggered=lambda url=saved_url: handle_saved_url(url)))
menu.addAction(QAction("Выход", menu, triggered=app.quit))

tray_icon.setContextMenu(menu)
tray_icon.show()

sys.exit(app.exec_())
