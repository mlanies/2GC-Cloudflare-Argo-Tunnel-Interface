"""
Пакет для логирование данных.

Фаил логов находится в log_tracking/logs/logs.log
"""

import traceback
from dataclasses import dataclass

from loguru import logger



@dataclass
class FileLogger:
    """
    Класс реализации записи различных сценариев в логи.

    """
    log_file = "./logs/logs.log"
    # logger.remove()  # remove console logging
    logger.add("logs/logs.log", rotation="2 MB", level="INFO", catch=True,
               format="{time: YYYY-MM-DD HH:mm} | [{level}] | {function}:{line} | {message}")

    @classmethod
    def log_info(cls, message):
        """Обычное информационное сообщение, напр. старт или конец."""
        logger.info(message)


    @classmethod
    def log_warning(cls, message):
        """
        Промежуточное оповещение средней важности.

        Например - сервис не смог с первого раза собрать cookies.
        """
        logger.warning(message)

    @classmethod
    def log_error(cls, message):
        """Сообщение об ошибке."""
        logger.error(message)

    @classmethod
    def log_exception(cls, message):
        """Сообщение об исключении."""
        info_text = f"{traceback.format_exc().strip()}\n{message}"
        logger.error(info_text)
