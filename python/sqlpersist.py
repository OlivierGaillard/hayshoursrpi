from mysql.connector import connect, Error
from persist import Persistable
import re


class SQLPersist(Persistable):
    """
    Save / retrieve the last hour using mariadb.
    """

    re_schema = re.compile(".*schema")
    re_mysql = "mysql"

    def __init__(self, host, user, password, port, database, create=True):
        self.stateful_type = "SQL"
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.connection = None
        self.create = create
        self.initStorage()

    def get_stateful_type(self):
        return self.stateful_type

    def initStorage(self):
        """
        Create database. If  it does exist we catch the error.
        """
        self.__create_connection()
        if self.create:
            if not self.database_exists(self.database):
                self.create_database()

    def __create_connection(self):
        try:
            self.connection = connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
            )
            # print(self.connection.get_server_info())
        except Error as e:
            print(e)

    def create_database(self):
        try:
            create_db_query = "CREATE DATABASE " + self.database
            with self.connection.cursor() as cursor:
                cursor.execute(create_db_query)
        except Error as e:
            print(e)

    def create_table(self, table_query, table_name):
        """
        table_query: full table query
        table_name: the table name
        """
        if not self.connection.is_connected():
            self.__create_connection()
        if not self.table_exists(table_name):
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(table_query)
            except Error as e:
                print(e)

    def save(self, result):
        save_query = "INSERT INTO hours(leaving)  VALUES ('" + result + "')"
        if not self.connection.is_connected():
            self.__create_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("USE " + self.database)
                cursor.execute(save_query)
            self.connection.commit()
        except Error as e:
            print(e)

    def readLast(self):
        getlast_query = (
            "select leaving from hours where id = (select max(id) from hours)"
        )
        if not self.connection.is_connected():
            self.__create_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("USE " + self.database)
                cursor.execute(getlast_query)
                result = cursor.fetchone()
                if result is not None:
                    return result[0]
                else:
                    return ""
        except Error as e:
            print(e)

    def list_database(self):
        if not self.connection.is_connected():
            self.__create_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                rows = cursor.fetchall()
                tmp = [d[0] for d in rows]
                tmp2 = [d for d in tmp if not SQLPersist.re_schema.match(d)]
                dbs = [d for d in tmp2 if not SQLPersist.re_mysql == d]
                return dbs
        except Error as e:
            print(e)

    def database_exists(self, db):
        """
        Check if database named 'db' exists.
        """
        return db in self.list_database()

    def table_exists(self, table):
        if not self.connection.is_connected():
            self.__create_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("USE " + self.database)
                cursor.execute("SHOW TABLES")
                rows = cursor.fetchall()
                tmp = [d[0] for d in rows]
                return table in tmp
        except Error as e:
            print(e)

    def deleteStorage(self):
        if self.database_exists(self.database):
            try:
                dropdb = "DROP DATABASE " + self.database
                with self.connection.cursor() as cursor:
                    cursor.execute(dropdb)
            except Error as e:
                print(e)
