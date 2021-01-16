import unittest
from hayshours import HaysHours
from persist import FilePersist
import os


class TestFilePersist(unittest.TestCase):

    def tearDown(self):
        os.remove('db1')

    def testSaveData(self):
        p = FilePersist('db1')
        p.save('ceci')
        last = p.readLast()
        self.assertEqual(last, 'ceci')

    def testGetEndHour6_3(self):
        h = HaysHours()
        p = FilePersist('db1')
        h.set_db(p)
        endHour = h.getEnd('6.3')
        lastHourSaved = h.getLastSaved()
        self.assertEqual(endHour, lastHourSaved)

if __name__ == '__main__':
    unittest.main()
