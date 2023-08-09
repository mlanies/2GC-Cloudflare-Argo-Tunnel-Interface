import subprocess
import time
import random


def run_command(command):
    try:
        subprocess.Popen(command, shell=True)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")

def connect_to_server(url):
    # url = "vm-srv-office.team108.ru"

    url = url
    port = random.randint(1100, 1200)

    cloudflared_cmd = f'cloudflared access rdp --hostname {url} --url rdp://localhost:{port}'

    run_command(cloudflared_cmd)

    time.sleep(2)

    mstsc_command = f'start cmd /c mstsc /v:localhost:{port}'
    run_command(mstsc_command)

# if __name__ == '__main__':
#
#     url = "vm-srv-office.team108.ru"
#     port = random.randint(1100, 1200)
#
#     cloudflared_cmd = f'cloudflared access rdp --hostname {url} --url rdp://localhost:{port}'
#
#     run_command(cloudflared_cmd)
#
#     time.sleep(2)
#
#     mstsc_command = f'start cmd /c mstsc /v:localhost:{port}'
#     run_command(mstsc_command)
