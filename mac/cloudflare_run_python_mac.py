# import pystray
# from tkinter import *
# import subprocess
# import random
#
# # Класс для иконки в трее
# class App:
#     def __init__(self):
#         self.icon = pystray.Icon("rdp")
#         self.icon.menu = pystray.Menu(pystray.MenuItem(
#             'Exit', lambda icon, item: icon.stop()
#         ))
#         self.icon.run()
#         self.address_history = []  # список сохраненных адресов
#         self.port_history = []  # список сохраненных портов
#
#     # Функция запуска программы и получения случайного порта
#     def start_program(self):
#         port = str(random.randint(1100, 1200))
#         hostname = self.get_hostname()
#         cmd = f'cloudflared access rdp --hostname {hostname} --url rdp://localhost:{port}'
#         subprocess.Popen(cmd.split())
#         self.address_history.append(hostname)
#         self.port_history.append(port)
#
#     # Функция отображения окна для ввода hostname
#     def get_hostname(self):
#         self.hostname = ""
#         def submit():
#             self.hostname = entry.get()
#             root.destroy()
#
#         root = Tk()
#         root.title("Enter hostname")
#         entry = Entry(root, width=30)
#         entry.pack(side=LEFT, padx=5)
#         button = Button(root, text="OK", command=submit)
#         button.pack(side=LEFT, padx=5)
#         root.mainloop()
#
#         return self.hostname
#
#     # Функция запуска RDP
#     def start_rdp(self, hostname, port):
#         cmd = f'xfreerdp /v:{hostname}:{port}'
#         subprocess.Popen(cmd.split())
#
# app = App()
#
# # Добавление пунктов меню в иконку в трее
# app.icon.menu.append(pystray.MenuItem(
#     'Start program', lambda icon, item: app.start_program()
# ))
# app.icon.menu.append(pystray.MenuItem(
#     'History', pystray.Menu(
#         *[
#             pystray.MenuItem(f'{hostname}:{port}', lambda icon, item: app.start_rdp(hostname, port))
#             for hostname, port in zip(app.address_history, app.port_history)
#         ]
#     )
# ))
#
# # Запуск GUI
# app.icon.visible = True
# app.icon.systray = True
# app.icon.run()
