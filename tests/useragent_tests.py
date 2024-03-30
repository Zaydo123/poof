from poof_util import UserAgent
import unittest


class TestUserAgents(unittest.TestCase):

    def setUp(self):
        self.generator = UserAgent()

    def test_get_all(self):
        result = self.generator.get_all()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_specific_platform(self):
        platforms = ['mac', 'windows', 'ios', 'linux', 'android', 'firefox', 'chrome', 'edge', 'opera', 'operagx', 'tv', 'crawler']
        for platform in platforms:
            with self.subTest(platform=platform):
                result = self.generator.get(platform=platform)
                self.assertIsInstance(result, list)
                self.assertTrue(len(result) > 0)

    def test_get_random(self):
        result = self.generator.get_random()
        self.assertIsInstance(result, str)

    def test_get_random_specific_platform(self):
        platforms = ['mac', 'windows', 'ios', 'linux', 'android', 'firefox', 'chrome', 'edge', 'opera', 'operagx', 'tv', 'crawler']
        for platform in platforms:
            with self.subTest(platform=platform):
                result = self.generator.get_random(platform=platform)
                self.assertIsInstance(result, str)

    def test_get_random_with_quantity(self):
        quantity = 5
        result = self.generator.get_random(quantity=quantity)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), quantity)

    def test_get_with_invalid_platform(self):
        result = self.generator.get(platform="invalid_platform")
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
