import unittest

from config_framework import VariableKey


class TestVariableKey(unittest.TestCase):
    def test_basic_variable_key(self):
        var_key = VariableKey("hello") / "world"
        self.assertEqual("hello[/]world", str(var_key))
        self.assertEqual(list(iter(var_key)), ["hello", "world"])

    def test_setting_invalid_type_to_var_key(self):
        with self.assertRaises(ValueError):
            VariableKey(123)  # noqa: testing

    def test_combining_keys(self):
        var_key1 = VariableKey("hello") / "world"
        var_key2 = VariableKey("more complicated key")
        combined_key = var_key1 / var_key2 / "ez"

        self.assertEqual(
            list(iter(combined_key)),
            ["hello", "world", "more complicated key", "ez"]
        )
