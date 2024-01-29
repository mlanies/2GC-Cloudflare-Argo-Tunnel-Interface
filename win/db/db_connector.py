"""
    Класс для взаимодействия с базой данных.

Class:
    SqliteDBConnect
"""


import os
import sqlite3
from typing import Any


class SqliteDBConnect:
    """
       Класс для работы с базой данных SQLite.

        Attributes:
        -----------
            :ivar: database_path (str): Путь к базе данных SQLite.
            :ivar: user_position (int): Позиция пользователя.

        Methods:
        -----------
        Public:
            execute_query(query): Выполняет SQL-запрос.
            get_url(): Возвращает URL-адрес из базы данных.
            get_connect(): Устанавливает соединение с базой данных.
            get_all_urls(): Возвращает все URL-адреса из базы данных.
            close_connect(connect): Закрывает соединение с базой данных.
            set_or_update_url(url): Добавляет или обновляет URL-адрес в базе данных.
            get_all_records(query): Возвращает все записи, соответствующие SQL-запросу.
            add_user_info(user_name, domain): Добавляет информацию о пользователе в базу данных.
            get_user_info() -> dict: Возвращает информацию о последнем пользователе из базы данных.
            get_or_create_path() -> str: Получает или создает путь к папке для хранения базы данных.

        Protect:
            _insert_query(query, data): Выполняет вставку данных в таблицу.

        Private:
           __create_urls_table(): Создает таблицу для URL-адресов, если она не существует.
           __create_login_table(): Создает таблицу для хранения информации о пользователе, если она не существует.
       """

    def __init__(self):
        """ Инициализирует экземпляр класса MainView. """
        self.database_path = os.path.join(self.get_or_create_path(), "2gс.sqlite")
        self.__create_urls_table()
        self.__create_login_table()
        self.user_position = 1

    def __create_urls_table(self):
        """
            Создает таблицу для URL-адресов, если она не существует.

        :return: None
        """
        query = ('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE
            )
        ''')
        self.execute_query(query)

    def __create_login_table(self):
        """
            Создает таблицу для хранения информации о пользователе, если она не существует.

        :return: None
        """
        query = ('''
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT ,
                domain_name TEXT 
            )
        ''')
        self.execute_query(query)

    def get_or_create_path(self) -> str:
        """
            Метод для получения пути до папки в которой будет храниться база данных.
        :return: (str) Путь до базы данных
        """
        current_directory = os.getcwd()
        db_folder_path = os.path.join(current_directory, "db")
        if not os.path.exists(db_folder_path) or not os.path.isdir(db_folder_path):
            os.makedirs(db_folder_path)
        return db_folder_path

    def execute_query(self, query: str) -> Any:
        """
            Выполняет SQL-запрос.

        :param: query: (str) SQL-запрос.
        :return: результат выполнения запроса или None
        """
        connect, cursor = self.get_connect()
        cursor.execute(query)
        if "select" in query.lower():
            first_user = cursor.fetchone()
            print(first_user)
            self.close_connect(connect)
            return first_user
        self.close_connect(connect)

    def get_all_records(self, query: str) -> list:
        """
            Возвращает все записи, соответствующие SQL-запросу.

        :param: query: (str) SQL-запрос.
        :return: список записей
        """
        connect, cursor = self.get_connect()
        cursor.execute(query)
        result = cursor.fetchall()
        self.close_connect(connect)
        return result

    def _insert_query(self, query: str, data: tuple) -> None:
        """
            Выполняет вставку данных в таблицу.

        :param: query: (str) SQL-запрос.
        :param: data: (tuple) Данные для вставки.
        :return: None
        """
        connect, cursor = self.get_connect()
        try:
            cursor.execute(query, data)
        except Exception as ex:
            print(59, f"{ex=}")
        finally:
            self.close_connect(connect)
    def get_connect(self) -> tuple:
        """
        Устанавливает соединение с базой данных.

        :return: кортеж (connect, cursor)
        """
        connect = sqlite3.connect(self.database_path)
        cursor = connect.cursor()
        return connect, cursor

    def close_connect(self, connect: sqlite3.connect) -> None:
        """
            Закрывает соединение с базой данных.

        :param: connect: соединение с базой данных
        :return: None
        """
        connect.commit()
        connect.close()

    def set_or_update_url(self, url: str) -> None:
        """
            Добавляет или обновляет URL-адрес в базе данных.

        :param url: (str) URL-адрес
        :return: None
        """
        query = """
        INSERT OR REPLACE INTO urls (id, url) VALUES (1, ?)
        """
        data = (url,)
        self._insert_query(query, data)

    def get_all_urls(self) -> list:
        """
            Возвращает все URL-адреса из базы данных.

        :return: (list) список URL-адресов
        """
        query = "SELECT url FROM urls"
        return self.get_all_records(query)

    def get_url(self) -> dict:
        """
            Возвращает URL-адрес из базы данных.

        :return: (dict) словарь с URL-адресом
        """
        query = "SELECT url FROM urls WHERE id = 1"
        result = self.get_all_records(query)
        if result:
            url = {"url": result[0][0]}
            return url
        return dict()

    def add_user_info(self, user_name: str, domain: str) -> None:
        """
            Добавляет информацию о пользователе в базу данных.

        :param user_name: (str) имя пользователя
        :param domain: (str) доменное имя пользователя
        :return: None
        """
        query = "INSERT INTO user_info (login, domain_name) VALUES (?, ?)"
        data = (user_name, domain)
        self._insert_query(query, data)

    def get_user_info(self) -> dict:
        """
            Возвращает информацию о последнем пользователе из базы данных.

        :return: (dict) словарь с информацией о пользователе
        """
        query = "SELECT login, domain_name FROM user_info ORDER BY id DESC LIMIT 1"
        result = self.get_all_records(query)
        print(result)
        if result:
            user_info = {"login": result[0][0], "domain_name": result[0][1]}
            return user_info
        return dict()
