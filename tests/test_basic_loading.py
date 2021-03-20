import unittest

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.loaders.json_string_loader import JsonStringLoader


class TestBasicLoader(unittest.TestCase):
    def test_loading(self):
        loader = JsonStringLoader.load('{"Rud": [356, "author"]}')
        self.assertEqual(loader.data, {"Rud": [356, "author"]})

    def test_defaults(self):
        loader = JsonStringLoader.load('{"Rud": [356, "author"]}', defaults={"Hello world": "some config_var"})
        self.assertEqual(loader.lookup_data, {"Rud": [356, "author"], "Hello world": "some config_var"})

    def test_getting_variable(self):
        loader = JsonStringLoader.load('{"Rud": [356, "author"]}')
        self.assertEqual(loader.get("Rud"), [356, "author"])

    def test_getting_variable_using_path_like_key(self):
        loader = JsonStringLoader.load('{"Admins": {"Rud": [356, "author"]}}')
        self.assertEqual(loader.get("Admins/Rud"), [356, "author"])

    def test_getting_variable_with_default(self):
        loader = JsonStringLoader.load('{"Rud": [356, "author"]}')
        self.assertEqual(loader.get("Unknown key", "Default"), "Default")

    def test_getting_variable_with_getitem(self):
        loader = JsonStringLoader.load('{"Rud": [356, "author"]}')
        self.assertEqual(loader['Rud'], [356, "author"])

    def test_casting_key_to_path(self):
        self.assertEqual(
            AbstractConfigLoader.key_to_path_cast("key/as/path/example"),
            ("key", "as", "path", "example")
        )

    def test_single_word_path_casting(self):
        self.assertEqual(
            AbstractConfigLoader.key_to_path_cast("key"),
            ("key",)
        )

    def test_setting_value(self):
        loader = JsonStringLoader.load('{"Rud": [356, "author"]}')
        loader['Rud'] = "Is author of ConfigFramework"
        self.assertEqual(loader['Rud'], "Is author of ConfigFramework")
