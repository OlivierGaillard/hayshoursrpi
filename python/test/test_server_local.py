import unittest
import requests
import sys

LOCAL     = 'http://localhost:5000/'


class TestServer(unittest.TestCase):
    '''
        Intrusive test! It will not delete the
        entries created in database 'worktime'.

        It uses the flask API defined in 'server.py' and does not
        directly access the database.
    '''
    URL  = LOCAL

    @classmethod
    def setUpClass(cls):
        try:
            requests.get(LOCAL, timeout=5)
        except(requests.ConnectionError, requests.Timeout) as exception:
            unittest.TestCase.skipTest(cls, 'Flask is not running locally')

    def test_calcformpage(self):
        r = requests.get(TestServer.URL  + 'calc')
        self.assertEqual(200, r.status_code)

    def test_end(self):
        r = requests.get(TestServer.URL + 'end/8.5')
        self.assertEqual('16:30:00', r.text)

    def test_last(self):
        u = requests.get(TestServer.URL + 'end/9')
        r = requests.get(TestServer.URL + 'last')
        self.assertEqual('17:30:00', r.text)


if __name__ == '__main__':
    unittest.main()
