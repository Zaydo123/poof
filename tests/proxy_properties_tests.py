from poof_util import Proxy
import unittest

class TestProxyProperties(unittest.TestCase):
    def setUp(self):
        self.proxy = Proxy('127.0.0.1', '8080', 'user', 'pass', 'http', 100, 'active')

    def test_get_protocol(self):
        self.assertEqual(self.proxy.get_protocol(), 'http')

    def test_get_ip(self):
        self.assertEqual(self.proxy.get_ip(), '127.0.0.1')

    def test_get_port(self):
        self.assertEqual(self.proxy.get_port(), '8080')

    def test_get_username(self):
        self.assertEqual(self.proxy.get_username(), 'user')

    def test_get_password(self):
        self.assertEqual(self.proxy.get_password(), 'pass')

    def test_get_auth(self):
        self.assertEqual(self.proxy.get_auth(), ('user', 'pass'))

    def test_get_speed(self):
        self.assertEqual(self.proxy.get_speed(), 100)

    def test_get_status(self):
        self.assertEqual(self.proxy.get_status(), 'active')

    def test_set_protocol(self):
        self.proxy.set_protocol('https')
        self.assertEqual(self.proxy.get_protocol(), 'https')

    def test_set_ip(self):
        self.proxy.set_ip('192.168.1.1')
        self.assertEqual(self.proxy.get_ip(), '192.168.1.1')

    def test_set_port(self):
        self.proxy.set_port('8000')
        self.assertEqual(self.proxy.get_port(), '8000')

    def test_set_username(self):
        self.proxy.set_username('new_user')
        self.assertEqual(self.proxy.get_username(), 'new_user')

    def test_set_password(self):
        self.proxy.set_password('new_pass')
        self.assertEqual(self.proxy.get_password(), 'new_pass')

    def test_set_auth(self):
        self.proxy.set_auth('new_user', 'new_pass')
        self.assertEqual(self.proxy.get_auth(), ('new_user', 'new_pass'))

    def test_set_speed(self):
        self.proxy.set_speed(200)
        self.assertEqual(self.proxy.get_speed(), 200)

    def test_set_status(self):
        self.proxy.set_status('inactive')
        self.assertEqual(self.proxy.get_status(), 'inactive')

    def test_str(self):
        self.assertEqual(str(self.proxy), '127.0.0.1:8080:user:pass')

if __name__ == '__main__':
    unittest.main()