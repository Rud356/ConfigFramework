import unittest

from config_framework import loaders, VariableKey


class TestBasicLoader(unittest.TestCase):
    def test_json_string_loading(self):
        loader = loaders.JsonString.load('{"hello": "world"}')
        self.assertEqual(loader["hello"], "world")

    def test_json_string_loader_with_defaults(self):
        loader = loaders.JsonString.load('{"hello": "world"}', defaults={
            "example": "default"
        })
        self.assertEqual(loader["example"], "default")

    def test_getting_nested_vars(self):
        loader = loaders.Dict.load(
            {
                "first layer": {
                    "internal": ["values"]
                }
            }
        )
        key = VariableKey("first layer") / "internal"
        self.assertEqual(loader[key], ["values"])

    def test_setting_value(self):
        loader = loaders.Dict.load(
            {
                "first layer": {
                    "internal": ["values"]
                }
            }
        )
        key = VariableKey("first layer") / "internal"
        loader[key] = "Example of changing var"
        self.assertEqual(loader[key], "Example of changing var")

    def test_setting_not_existing_key(self):
        loader = loaders.Dict.load(
            {
                "first layer": {
                    "internal": ["values"]
                }
            }
        )

        with self.assertRaises(KeyError):
            loader['some not existing key'] = 123

    def test_deleting_value_from_loader(self):
        loader = loaders.Dict.load(
            {
                "first layer": {
                    "internal": ["values"]
                }
            }
        )
        key = VariableKey("first layer") / "internal"
        del loader[key]
        self.assertEqual(loader["first layer"], {})

    def test_deleting_not_existing_key_from_loader(self):
        loader = loaders.Dict.load(
            {
                "first layer": {
                    "internal": ["values"]
                }
            }
        )
        key = VariableKey("first layer") / "idk"
        with self.assertRaises(KeyError):
            del loader[key]

    def test_get_from_loader(self):
        loader = loaders.JsonString.load('{"hello": "world"}', defaults={
            "example": "default"
        })
        self.assertEqual(loader.get("example"), "default")

    def test_getting_not_existing_var(self):
        loader = loaders.JsonString.load('{"hello": "world"}')
        with self.assertRaises(KeyError):
            var = loader["missing key"]
