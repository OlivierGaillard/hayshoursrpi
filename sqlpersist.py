from mysql.connector import connect, Error
from persist import Persistable


class SQLPersist(Persistable):
    """
    Save / retrieve the last hour using mariadb.
    """

    def __init__(self, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.connection = None
        self.initStorage()

    def initStorage(self):
        """
        Create database. If  it does exist we catch the error.
        """
        self.create_connection()
        self.create_database()

    def create_connection(self):
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

    def create_table(self, table_query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(table_query)
        except Error as e:
            print(e)

    def save(self, result):
        save_query = "INSERT INTO hours(leaving)  VALUES ('" + result + "')"
        if not self.connection.is_connected():
            self.create_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("USE " + self.database)
                cursor.execute(save_query)
            self.connection.commit()
        except Error as e:
            print(e)

    def readLast(self):
        getlast_query = "SELECT `leaving` FROM hours"
        if not self.connection.is_connected():
            self.create_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("USE " + self.database)
                cursor.execute(getlast_query)
                result = cursor.fetchone()
                if result is not None:
                    return result[0]
                else:
                    return ''
        except Error as e:
            print(e)

    def deleteStorage(self):
        try:
            dropdb = "DROP DATABASE " + self.database
            with self.connection.cursor() as cursor:
                cursor.execute(dropdb)
        except Error as e:
            print(e)
