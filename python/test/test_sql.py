import unittest
from sqlpersist import SQLPersist
import mysql
import os


class TestDBSetup(unittest.TestCase):

    dbs = []
    dbname = "one"

    def tearDown(self):
        for p in TestDBSetup.dbs:
            p.deleteStorage()

    def setUp(self):
        self.host = "192.168.1.100"
        self.user = "root"
        self.password = os.getenv('MARIAPASS')
        self.port = 30306

    def test_Create_SameDB_2times(self):
        """Should create only one database"""
        db = TestDBSetup.dbname
        p1 = SQLPersist(self.host, self.user, self.password, self.port, db)
        TestDBSetup.dbs.append(p1)
        self.assertTrue(p1.database_exists(db))
        p2 = SQLPersist(self.host, self.user, self.password, self.port, db)
        self.assertTrue(p2.connection.is_connected())

    def test_database_exists(self):
        db = TestDBSetup.dbname
        p = SQLPersist(self.host, self.user, self.password, self.port, db)
        self.assertTrue(p.database_exists(db))

    def test_database_does_not_exist(self):
        db = TestDBSetup.dbname
        p = SQLPersist(self.host, self.user, self.password, self.port, db, create=False)
        self.assertFalse(p.database_exists(db))

    def test_table_exists(self):
        db = TestDBSetup.dbname
        table = "hhours"
        p = SQLPersist(self.host, self.user, self.password, self.port, db)
        TestDBSetup.dbs.append(p)
        create_table_query = f"CREATE TABLE {db}.{table}(leaving VARCHAR(10))"
        p.create_table(create_table_query, table)
        self.assertTrue(p.table_exists(table))

    def test_Create_SameTable_2times(self):
        """Should create only one table"""
        db = TestDBSetup.dbname
        table = "hours"
        p = SQLPersist(self.host, self.user, self.password, self.port, db)
        TestDBSetup.dbs.append(p)
        create_table_query = f"CREATE TABLE {db}.{table}(leaving VARCHAR(10))"
        p.create_table(create_table_query, table)
        p.create_table(create_table_query, table)

    def test_create_SQL_without_db_creation(self):
        db = TestDBSetup.dbname
        p = SQLPersist(self.host, self.user, self.password, self.port, db, create=False)

    def test_connect_db(self):
        db = TestDBSetup.dbname
        p = SQLPersist(self.host, self.user, self.password, self.port, db, create=True)
        p.create_connection_with_db(db)
        self.assertTrue(p.connection.is_connected)

    def test_connect_non_existing_db(self):
        db = "mafalda"
        p = SQLPersist(self.host, self.user, self.password, self.port, db, create=False)
        self.assertFalse(p.database_exists(db))

    def test_getlast(self):
        db = TestDBSetup.dbname
        t = "hours"
        id = "id MEDIUMINT NOT NULL AUTO_INCREMENT"
        primary = "PRIMARY KEY(id)"
        create_table_query = f"""CREATE TABLE {db}.{t}({id},
            leaving VARCHAR(10),
            {primary}
        )"""
        p = SQLPersist(self.host, self.user, self.password, self.port, db, create=True)
        p.create_table(create_table_query, t)
        p.save("16:45:15")
        p.save("16:55:25")
        p.save("17:00:05")
        self.assertEqual(p.readLast(), "17:00:05")


if __name__ == "__main__":
    unittest.main()
