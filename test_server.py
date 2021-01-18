import unittest
import requests


class TestServer(unittest.TestCase):

    def test_calcformpage(self):
        r = requests.get('http://localhost:5000/calc')
        self.assertEqual(200, r.status_code)

    def test_end(self):
        r = requests.get('http://localhost:5000/end/8.5')
        self.assertEqual('16:30:00\n', r.text)

    def test_last(self):
        requests.get('http://localhost:5000/end/9')
        r = requests.get('http://localhost:5000/last')
        self.assertEqual('17:30:00\n', r.text)


if __name__ == '__main__':
    unittest.main()
