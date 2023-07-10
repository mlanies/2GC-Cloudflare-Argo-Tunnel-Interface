# import pystray
# from PIL import Image
# import subprocess
#
# # функция для запуска кода vbs
# def run_vbs(file_path):
#     subprocess.Popen(["cscript", file_path], shell=True)
#
# # функции для каждой кнопки
# def cloudflare_1(icon):
#     run_vbs("path_to_vbs_file_1.vbs")
#
# def cloudflare_2(icon):
#     run_vbs("path_to_vbs_file_2.vbs")
#
# def cloudflare_3(icon):
#     run_vbs("path_to_vbs_file_3.vbs")
#
# # создание иконки для трея
# icon_image = Image.open("path_to_icon_image.png")
# menu = (
#     ("Cloudflare 1", icon_image, cloudflare_1),
#     ("Cloudflare 2", icon_image, cloudflare_2),
#     ("Cloudflare 3", icon_image, cloudflare_3),
# )
#
# # отображение иконки в трее
# def on_clicked(icon, item):
#     item[2](icon)
#
# menu_icon = pystray.Icon("name_of_the_program", icon_image)
# menu_icon.menu = pystray.Menu(*menu)
# menu_icon.run(on_clicked)
