import os
import re
import sys
import time
import win32api
import win32con
import win32gui
import requests
import threading
from tkinter import *
from tkinter import messagebox

# Инициализация окна
root = Tk()
root.title("Cloudflare Zero Trust App Launcher")
root.iconbitmap('cloudflare.ico')
root.resizable(0, 0)

# Переменные
selected_url = StringVar()
port = 0
auto_start_var = IntVar()

# Функции
def add_servers():
    try:
        # Очищаем список перед обновлением
        server_listbox.delete(0, END)
        response = requests.get("https://api.cloudflare.com/client/v0/zero-trust/app-launcher/apps",
                                headers={'Authorization': 'Bearer ' + os.environ['CF_API_TOKEN']})
        if response.status_code == 200:
            for app in response.json()['result']:
                # Добавляем только те URL-адреса, которые содержат 'rdp'
                if 'rdp' in app['public_url']:
                    server_listbox.insert(END, app['public_url'])
        else:
            messagebox.showerror("Ошибка", "Не удалось получить список серверов. Попробуйте позже.")
    except KeyError:
        messagebox.showerror("Ошибка", "CF_API_TOKEN не установлен в переменных окружения.")
        close_button = Button(settings_window, text="Закрыть", command=close_settings)
close_button.pack(padx=10, pady=10)

 # Основное окно
 # Заголовок
 title_label = Label(root, text="Cloudflare Zero Trust App Launcher", font=("Arial", 16))
 title_label.pack(pady=20)
Список серверов
server_frame = Frame(root)
server_frame.pack(pady=10)

server_label = Label(server_frame, text="Список серверов:")
server_label.pack(side=LEFT)

server_scrollbar = Scrollbar(server_frame)
server_scrollbar.pack(side=RIGHT, fill=Y)

server_listbox = Listbox(server_frame, width=50, yscrollcommand=server_scrollbar.set)
server_listbox.pack(pady=5)

server_scrollbar.config(command=server_listbox.yview)

Кнопки
button_frame = Frame(root)
button_frame.pack(pady=10)

add_servers_button = Button(button_frame, text="Обновить список серверов", command=add_servers)
add_servers_button.pack(side=LEFT, padx=5)

start_session_button = Button(button_frame, text="Запустить сеанс", command=start_session)
start_session_button.pack(side=LEFT, padx=5)

settings_button = Button(button_frame, text="Настройки", command=show_settings)
settings_button.pack(side=LEFT, padx=5)

Запускаем обновление списка серверов при запуске программы
add_servers()

root.mainloop()
