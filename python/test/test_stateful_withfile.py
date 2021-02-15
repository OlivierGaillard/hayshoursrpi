import unittest
from hayshours import HaysHours
from filepersist import FilePersist


class TestSave(unittest.TestCase):

    fname = 'db1'

    def tearDown(self):
        self.p.deleteStorage()

    def setUp(self):
        self.p = FilePersist('./tmp', TestSave.fname)

    def testSaveData(self):
        self.p.save('ceci')
        last = self.p.readLast()
        self.assertEqual(last, 'ceci')

    def testGetEndHour6_3(self):
        h = HaysHours()
        h.set_db(self.p)
        endHour = h.getEnd('6.3')
        lastHourSaved = h.getLastSaved()
        self.assertEqual(lastHourSaved, endHour)

    def testNoSavedData(self):
        h = HaysHours()
        h.set_db(self.p)
        h.getEnd('')
        lastHourSaved = h.getLastSaved()
        self.assertEqual('', lastHourSaved)

    def testSaveOneDate_andLastEmpty(self):
        '''Should return the pre-last non-empty'''
        h = HaysHours()
        h.set_db(self.p)
        endHour = h.getEnd('6.3')
        h.getEnd('')
        lastHourSaved = h.getLastSaved()
        self.assertEqual(endHour, lastHourSaved)


if __name__ == '__main__':
    unittest.main()
