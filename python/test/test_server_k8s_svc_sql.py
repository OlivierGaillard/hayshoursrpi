import unittest
import requests
import sys

# Services ports
SQL_PORT = 30036

K8S_SQL   = f"http://192.168.1.101:{SQL_PORT}/"


class TestServer(unittest.TestCase):
    '''
        Intrusive test! It will not delete the
        entries created in database 'worktime'.

        It uses the flask API defined in 'server.py' and does not
        directly access the database.
    '''

    def test_calcformpage(self):
        r = requests.get(K8S_SQL  + 'calc')
        self.assertEqual(200, r.status_code)

    def test_end(self):
        r = requests.get(K8S_SQL + 'end/8.5')
        self.assertEqual('16:30:00', r.text)

    def test_last(self):
        u = requests.get(K8S_SQL + 'end/9')
        r = requests.get(K8S_SQL + 'last')
        self.assertEqual('17:30:00', r.text)


if __name__ == '__main__':
    unittest.main()
