import unittest

import tomli  # you can use toml, json,yaml, or ryo for your config file
from config_parser import parse_config


class TestConfigParsing(unittest.TestCase):
    def test_parse_config_has_correct_location_and_spaces(self):
        with open("config.toml", "r") as file:
            config_string = file.read()
        config = tomli.loads(config_string)
        self.assertEqual(config['carpark']['name'], "Moondalup Parking Lot")
        self.assertEqual(config['carpark']['total_spaces'], 180)
