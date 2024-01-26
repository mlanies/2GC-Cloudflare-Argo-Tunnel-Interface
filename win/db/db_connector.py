
import os
import sqlite3


class SqliteDBConnect:
    def __init__(self):
        self.database_path = os.path.join(self.get_or_create_path(), "2gс.sqlite")
        self.__create_urls_table()
        self.__create_login_table()
        self.user_position = 1

    def __create_urls_table(self):

        query = ('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE
            )
        ''')
        self.execute_query(query)


        print(f"База данных {self.database_path} и таблица 'users' успешно созданы.")

    def __create_login_table(self):
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

    def execute_query(self, query):
        connect, cursor = self.get_connect()
        cursor.execute(query)
        if "select" in query.lower():
            first_user = cursor.fetchone()
            print(first_user)
            self.close_connect(connect)
            return first_user
        self.close_connect(connect)

    def get_all_records(self, query):
        connect, cursor = self.get_connect()
        cursor.execute(query)
        result = cursor.fetchall()
        self.close_connect(connect)
        return result

    def _insert_query(self, query, data):
        connect, cursor = self.get_connect()
        try:
            cursor.execute(query, data)
        except Exception as ex:
            print(59, f"{ex=}")
        finally:
            self.close_connect(connect)
    def get_connect(self):
        connect = sqlite3.connect(self.database_path)
        cursor = connect.cursor()
        return connect, cursor

    def close_connect(self, connect):
        connect.commit()
        connect.close()

    def set_or_update_url(self, url):
        query = """
        INSERT OR REPLACE INTO urls (id, url) VALUES (1, ?)
        """
        data = (url,)
        self._insert_query(query, data)

    def get_all_urls(self):
        query = "SELECT url FROM urls"
        return self.get_all_records(query)

    def get_url(self):
        query = "SELECT url FROM urls WHERE id = 1"
        result = self.get_all_records(query)
        if result:
            url = {"url": result[0][0]}
            return url
        return dict()

    def add_user_info(self, user_name, domain):
        query = "INSERT INTO user_info (login, domain_name) VALUES (?, ?)"
        data = (user_name, domain)
        self._insert_query(query, data)

    def get_user_info(self) -> dict:
        query = "SELECT login, domain_name FROM user_info ORDER BY id DESC LIMIT 1"
        result = self.get_all_records(query)
        print(result)
        if result:
            user_info = {"login": result[0][0], "domain_name": result[0][1]}
            return user_info
        return dict()
