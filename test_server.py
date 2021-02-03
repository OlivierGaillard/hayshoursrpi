import unittest
import requests
import sys

LOCAL = 'http://localhost:5000/'
K8S   = 'http://192.168.1.101:30036/'


class TestServer(unittest.TestCase):
    '''
        Intrusive test! It will not delete the
        entries created in database 'worktime'.

        It uses the flask API defined in 'server.py' and does no
        direct usage of the database.
    '''

    URL  = ''

    def test_calcformpage(self):
        r = requests.get(TestServer.URL  + 'calc')
        self.assertEqual(200, r.status_code)

    def test_end(self):
        r = requests.get(TestServer.URL + 'end/8.5')
        self.assertEqual('16:30:00', r.text)

    def test_last(self):
        requests.get(TestServer.URL + 'end/9')
        r = requests.get(TestServer.URL + 'last')
        self.assertEqual('17:30:00', r.text)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Give L (local) or K (K8S)')
        sys.exit(-1)
    test_environ = sys.argv.pop()
    if test_environ == 'L':
        TestServer.URL = LOCAL
        print('Using ' + LOCAL)
    else:
        TestServer.URL = K8S
        print('Using ' + K8S)
    print('environment: ' + test_environ)
    unittest.main()
