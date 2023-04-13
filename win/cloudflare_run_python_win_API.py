import os
import random
import subprocess
import sys
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from typing import List

import requests
import winreg

# API-конечная точка для получения списка приложений в App Launcher
API_URL = "https://api.cloudflare.com/client/v4/zones/{zone_id}/zero/applications"

# Замените {zone-id} на идентификатор вашей зоны Cloudflare
ZONE_ID = "{zone-id}"

# Замените {api-key} на ваш ключ API Cloudflare
API_KEY = "{api-key}"

# Конфигурация программы
SETTINGS_FILE = "settings.cfg"
AUTOSTART_REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


class AppLauncherTrayIcon:
    """Иконка в трее для программы App Launcher"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.tray_icon = tk.PhotoImage(file="tray_icon.png")
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Список серверов", command=self.show_applications)
        self.menu.add_command(label="Настройки", command=self.show_settings)
        self.root.iconphoto(True, self.tray_icon)
        self.root.config(menu=self.menu)
        self.root.withdraw()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Обработчик закрытия окна"""
        self.root.withdraw()

    def show_notification(self, title: str, message: str):
        """Отображает уведомление в трее"""
        self.root.tk.call(
            "tk::tray",
            "popup",
            self.tray_icon,
            "-text",
            message,
            "-title",
            title,
        )

    def show_info_dialog(self, title: str, message: str):
        """Отображает информационное диалоговое окно"""
        tkinter.messagebox.showinfo(title, message)

    def show_error_dialog(self, title: str, message: str):
        """Отображает диалоговое окно с ошибкой"""
        tkinter.messagebox.showerror(title, message)

    def show_applications(self):
        """Отображает список приложений в App Launcher"""
        applications = get_applications()
        if applications:
            ApplicationListWindow(self.root, applications)
        else:
            self.show_error_dialog(
                "Ошибка", "Не удалось получить список приложений из App Launcher"
            )

    def show_settings(self):
        """Отображает окно настроек"""
        SettingsWindow(self.root)


class ApplicationListWindow(tk.Toplevel):
    """Окно со списком приложений"""

    def __init__(self, parent, applications):
        super().__init__(parent)
        self.title("Список серверов")
        self.geometry("400x400")
        self.resizable(False, False)
        self.parent = parent
        self.applications = applications
        self.create_widgets()

    def create_widgets(self):
        """Создает виджеты окна"""
        tree = ttk.Treeview(self, columns=("name","url"), height=20, selectmode="browse")
tree.heading("#0", text="ID")
tree.heading("name", text="Имя")
tree.heading("url", text="URL")
for app in self.applications:
tree.insert("", "end", text=app["id"], values=(app["name"], app["url"]))
tree.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)
tree.bind("<Double-Button-1>", self.on_tree_double_click)

def on_tree_double_click(self, event):
    """Обработчик двойного щелчка на элементе списка"""
    item_id = event.widget.focus()
    if item_id:
        url = event.widget.item(item_id)["values"][1]
        self.run_rdp(url)

def run_rdp(self, url):
    """Запускает RDP-сессию"""
    port = random.randint(1100, 1200)
    cmd = f"cloudflared access rdp --hostname {url} --url rdp://localhost:{port}"
    try:
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.parent.show_notification("App Launcher", "RDP-сессия запущена")
        subprocess.Popen(f'start cmd /c mstsc /v:localhost:{port}', shell=True)
    except Exception as e:
        self.parent.show_error_dialog("Ошибка", str(e))

class SettingsWindow(tk.Toplevel):
"""Окно настроек"""
def __init__(self, parent):
    super().__init__(parent)
    self.title("Настройки")
    self.geometry("300x100")
    self.resizable(False, False)
    self.parent = parent
    self.create_widgets()

def create_widgets(self):
    """Создает виджеты окна"""
    autostart_var = tk.BooleanVar(value=self.get_autostart_setting())
    autostart_checkbox = ttk.Checkbutton(
        self, text="Автозапуск программы", variable=autostart_var, command=self.set_autostart_setting
    )
    autostart_checkbox.pack(padx=10, pady=10)

def get_autostart_setting(self):
    """Возвращает значение настройки автозапуска программы"""
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, AUTOSTART_REGISTRY_KEY, 0, winreg.KEY_READ
    ) as key:
        value, _ = winreg.QueryValueEx(key, os.path.basename(sys.argv[0]))
        return value == os.path.abspath(sys.argv[0])

def set_autostart_setting(self):
    """Устанавливает настройку автозапуска программы"""
    autostart = self.get_autostart_setting()
    if autostart:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, AUTOSTART_REGISTRY_KEY, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, os.path.basename(sys.argv[0]))
    else:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, AUTOSTART_REGISTRY_KEY, 0, winreg.KEY_WRITE
        ) as key:
            winreg.SetValueEx(key, os.path.basename(sys.argv[0]), 0, winreg.REG_SZ, sys.argv[0])

            class TrayIcon:
"""Иконка в трее"""
def __init__(self, parent):
    self.parent = parent
    self.create_menu()
    self.create_icon()

def create_menu(self):
    """Создает меню иконки"""
    self.menu = tk.Menu(tearoff=0)
    self.menu.add_command(label="Список серверов", command=self.show_applications_window)
    self.menu.add_command(label="Настройки", command=self.show_settings_window)
    self.menu.add_command(label="Выход", command=self.quit)

def create_icon(self):
    """Создает иконку"""
    self.icon = tk.PhotoImage(file="icon.png")
    self.tray_icon = tk.Tk()
    self.tray_icon.withdraw()
    self.tray_icon.iconphoto(False, self.icon)
    self.tray_icon.protocol("WM_DELETE_WINDOW", self.quit)
    self.tray_icon.bind("<Button-1>", self.on_left_click)
    self.tray_icon.bind("<Button-3>", self.on_right_click)

def on_left_click(self, event):
    """Обработчик левого клика на иконке"""
    self.show_applications_window()

def on_right_click(self, event):
    """Обработчик правого клика на иконке"""
    self.menu.tk_popup(event.x_root, event.y_root)

def show_applications_window(self):
    """Отображает окно списка серверов"""
    ApplicationsWindow(self.parent)

def show_settings_window(self):
    """Отображает окно настроек"""
    SettingsWindow(self.parent)

def quit(self):
    """Выход из программы"""
    self.tray_icon.quit()
    self.tray_icon.destroy()
    sys.exit()

def start(self):
    """Запускает приложение"""
    self.tray_icon.mainloop()
if name == "main":
app = AppLauncher()
tray_icon = TrayIcon(app)
tray_icon.start()

class ApplicationsWindow:
"""Окно со списком приложений"""
def __init__(self, parent):
    self.parent = parent
    self.create_window()

def create_window(self):
    """Создает окно"""
    self.window = tk.Toplevel()
    self.window.title("Список серверов")
    self.window.geometry("400x300")
    self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    self.create_listbox()
    self.create_buttons()

def create_listbox(self):
    """Создает список приложений"""
    self.listbox = tk.Listbox(self.window)
    self.listbox.pack(fill=tk.BOTH, expand=1)
    self.update_listbox()

def update_listbox(self):
    """Обновляет список приложений"""
    self.listbox.delete(0, tk.END)
    for app in self.parent.applications:
        self.listbox.insert(tk.END, app["url"])

def create_buttons(self):
    """Создает кнопки"""
    frame = tk.Frame(self.window)
    frame.pack(fill=tk.X, padx=10, pady=10)
    add_button = tk.Button(frame, text="Добавить", command=self.add_application)
    add_button.pack(side=tk.LEFT)
    remove_button = tk.Button(frame, text="Удалить", command=self.remove_application)
    remove_button.pack(side=tk.LEFT, padx=5)
    refresh_button = tk.Button(frame, text="Обновить", command=self.update_listbox)
    refresh_button.pack(side=tk.LEFT)

def add_application(self):
    """Добавляет приложение"""
    url = simpledialog.askstring("Добавление сервера", "Введите URL сервера:")
    if url:
        self.parent.add_application(url)
        self.update_listbox()

def remove_application(self):
    """Удаляет приложение"""
    selection = self.listbox.curselection()
    if selection:
        index = selection[0]
        self.parent.remove_application(index)
        self.update_listbox()

def on_close(self):
    """Обработчик закрытия окна"""
    self.window.destroy()

    class SettingsWindow:
"""Окно настроек"""
def __init__(self, parent):
    self.parent = parent
    self.create_window()

def create_window(self):
    """Создает окно"""
    self.window = tk.Toplevel()
    self.window.title("Настройки")
    self.window.geometry("300x100")
    self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    self.create_checkbox()

def create_checkbox(self):
    """Создает чекбокс"""
    self.autostart_var = tk.BooleanVar()
    self.autostart_var.set(self.parent.autostart)
    self.checkbox = tk.Checkbutton(self.window, text="Автозапуск приложения", variable=self.autostart_var)
    self.checkbox.pack(padx=10, pady=10)

def on_close(self):
    """Обработчик закрытия окна"""
    self.parent.autostart = self.autostart_var.get()
    self.parent.save_settings()
    self.window.destroy()
if name == "main":
app = AppLauncher()
tray_icon = TrayIcon(app)
tray_icon.start()
