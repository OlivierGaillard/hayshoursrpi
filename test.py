import unittest
from hayshours import HaysHours


class TestHayshours(unittest.TestCase):

    def testGetEndHour8(self):
        h = HaysHours()
        endHour = h.getEnd(8)
        self.assertEqual(endHour, "16:00:00")

    def testGetEndHour8_str(self):
        h = HaysHours()
        endHour = h.getEnd('8')
        self.assertEqual(endHour, "16:00:00")

    def testGetEndHour8_4(self):
        h = HaysHours()
        endHour = h.getEnd(8.4)
        self.assertEqual(endHour, "16:24:00")

    def testGetEndHour8_6(self):
        h = HaysHours()
        endHour = h.getEnd(8.6)
        self.assertEqual(endHour, "17:06:00")

    def testGetEndHour8_5(self):
        h = HaysHours()
        endHour = h.getEnd(8.5)
        self.assertEqual(endHour, "16:30:00")

    def testGetEndHour8_1(self):
        h = HaysHours()
        endHour = h.getEnd(8.1)
        self.assertEqual(endHour, "16:06:00")

    def testGetEndHour7_2(self):
        h = HaysHours()
        endHour = h.getEnd(7.2)
        self.assertEqual(endHour, "15:12:00")

    def testGetEndHour9_2(self):
        h = HaysHours()
        endHour = h.getEnd(9.2)
        self.assertEqual(endHour, "17:42:00")

    def testGetEndHour10_5(self):
        h = HaysHours()
        endHour = h.getEnd(10.5)
        self.assertEqual(endHour, "19:00:00")

    def testGetEndHour6_3(self):
        h = HaysHours()
        endHour = h.getEnd(6.3)
        self.assertEqual(endHour, "14:03:00")
