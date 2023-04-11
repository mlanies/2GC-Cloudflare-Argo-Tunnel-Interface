from tkinter import *
import os
import time
import random
from pystray import Menu, MenuItem
import pystray

def cloudflare1():
url = input("Введите URL: ")
port = random.randint(1100, 1200)
os.system(
'start cmd /c cloudflared access rdp --hostname "{}" --url rdp://localhost:{}'
.format(url, port))
time.sleep(4)
os.system('start cmd /c mstsc /v:localhost:{}'.format(port))

def on_quit():
tray.icon = None
root.quit()

menu = Menu(MenuItem('Cloudflare 1', cloudflare1),
MenuItem('Quit', on_quit))

image = Image.open("icon.png")
tray = pystray.Icon("name", image, "title", menu)
tray.run()

root = Tk()
root.mainloop()
