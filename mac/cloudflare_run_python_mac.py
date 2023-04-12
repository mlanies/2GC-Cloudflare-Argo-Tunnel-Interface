import subprocess
import sys
import datetime
import os
import pystray
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

# Параметры запуска службы Cloudflare
cloudflare_params = ["service", "cloudflared", "start"]

# Параметры запуска RDP клиента
rdp_params = ["xfreerdp", "/u:<username>", "/p:<password>", "/v:<server>"]

app = QApplication(sys.argv)

# Создаем иконку в трее
tray_icon = QSystemTrayIcon(QIcon("icon.png"), app)

# Создаем меню для иконки в трее
menu = QMenu()

# Функция для запуска службы Cloudflare
def start_cloudflare():
    subprocess.run(cloudflare_params)

# Функция для запуска RDP клиента
def start_rdp():
    subprocess.run(rdp_params)

# Функция для отображения текущего времени на экране
def show_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    tray_icon.setToolTip(now)

# Добавляем действия в меню
start_cloudflare_action = QAction("Start Cloudflare", menu)
start_cloudflare_action.triggered.connect(start_cloudflare)

start_rdp_action = QAction("Start RDP", menu)
start_rdp_action.triggered.connect(start_rdp)

show_time_action = QAction("Show Time", menu)
show_time_action.triggered.connect(show_time)

exit_action = QAction("Exit", menu)
exit_action.triggered.connect(app.quit)

menu.addAction(start_cloudflare_action)
menu.addAction(start_rdp_action)
menu.addAction(show_time_action)
menu.addSeparator()
menu.addAction(exit_action)

tray_icon.setContextMenu(menu)

# Функция для выхода из программы
def on_exit(icon, item):
    tray_icon.setVisible(False)
    app.quit()

# Создаем иконку в трее с обработчиками событий
tray_icon = pystray.create_systray(icon="icon.png", menu=menu)
tray_icon.run(on_exit)

sys.exit(app.exec_())
