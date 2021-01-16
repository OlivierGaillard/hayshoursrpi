import unittest
from hayshours import HaysHours
from persist import FilePersist
import os


class TestFilePersist(unittest.TestCase):

    def tearDown(self):
        if os.path.exists('db1'):
            os.remove('db1')

    def setUp(self):
        if os.path.exists('db1'):
            os.remove('db1')

    def testSaveData(self):
        p = FilePersist('db1')
        p.save('ceci')
        last = p.readLast()
        self.assertEqual(last, 'ceci\n')

    def testGetEndHour6_3(self):
        h = HaysHours()
        p = FilePersist('db1')
        h.set_db(p)
        endHour = h.getEnd('6.3')
        lastHourSaved = h.getLastSaved()
        self.assertEqual(endHour+'\n', lastHourSaved)

    def testNoSavedData(self):
        h = HaysHours()
        p = FilePersist('db1')
        h.set_db(p)
        endHour = h.getEnd('')
        lastHourSaved = h.getLastSaved()
        self.assertEqual('', lastHourSaved)

    def testSaveOneDate_andLastEmpty(self):
        '''Should return the pre-last non-empty'''
        h = HaysHours()
        p = FilePersist('db1')
        h.set_db(p)
        endHour = h.getEnd('6.3')
        h.getEnd('')
        lastHourSaved = h.getLastSaved()
        self.assertEqual(endHour+'\n', lastHourSaved)

if __name__ == '__main__':
    unittest.main()
