import subprocess
import random


def execute_cmd(commands):
    """Функция используется для выполнения команд cmd"""
    for command in commands:
        subprocess.run(command, shell=True)


def connect_to_server(url):
    """  Функция для формировании команды
    :param url - str Url сервера для которого нужно сформировать команду.

    Формирует список команд, и передает его в execute_cmd
    """
    url = url
    port = random.randint(1100, 1200)

    cloudflared_cmd = f'cloudflared access rdp --hostname {url} --url rdp://localhost:{port}'
    mtsc_cmd = f'mtsc localhost:{port}'

    commands = [cloudflared_cmd, mtsc_cmd]
    execute_cmd(commands)



