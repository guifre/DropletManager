from unittest import TestCase

from config_provider import ConfigProvider


class TestConfigProvider(TestCase):
    def test(self):
        config_data = ConfigProvider().parse()
        self.assertTrue(config_data['size'] is not '')
        self.assertTrue(config_data['api_key'] is not '')
        self.assertTrue(config_data['snapshot'] is not '')
