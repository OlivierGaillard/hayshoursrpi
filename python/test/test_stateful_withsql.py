import unittest
from hayshours import HaysHours
from sqlpersist import SQLPersist
import os

class TestSave(unittest.TestCase):

    database = "hours"

    def tearDown(self):
        self.p.deleteStorage()

    def setUp(self):
        self.host = "192.168.1.100"
        self.user = "root"
        self.password = os.getenv('MARIAPASS')
        self.port = 30306
        self.database = "hhours"
        self.table = "hours"
        self.p = SQLPersist(
            self.host, self.user, self.password, self.port, self.database, create=True
        )
        id = "id MEDIUMINT NOT NULL AUTO_INCREMENT"
        primary = "PRIMARY KEY(id)"
        create_table_query = f"""CREATE TABLE {self.database}.{self.table}({id},
            leaving VARCHAR(10),
            {primary}
        )"""
        self.p.create_table(create_table_query, self.table)

    def testConnection(self):
        self.assertTrue(self.p.connection.is_connected())

    def testSaveData(self):
        leave_time = "17:30:00"
        self.p.save(leave_time)
        last = self.p.readLast()
        self.assertEqual(last, leave_time)

    def testGetEndHour6_3(self):
        h = HaysHours()
        h.set_db(self.p)
        endHour = h.getEnd("6.3")
        lastHourSaved = h.getLastSaved()
        self.assertEqual(lastHourSaved, endHour)

    def testNoSavedData(self):
        h = HaysHours()
        h.set_db(self.p)
        h.getEnd("")
        lastHourSaved = h.getLastSaved()
        self.assertEqual("", lastHourSaved)

    def testSaveOneDate_andLastEmpty(self):
        """Should return the pre-last non-empty"""
        h = HaysHours()
        h.set_db(self.p)
        endHour = h.getEnd("6.3")
        h.getEnd("")
        lastHourSaved = h.getLastSaved()
        self.assertEqual(endHour, lastHourSaved)


if __name__ == "__main__":
    unittest.main()
