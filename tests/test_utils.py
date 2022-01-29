import json
import unittest

from config_framework import loaders, utils, Variable


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.loader_json = loaders.JsonString.load(
            '{"hello": "rud", "version": "42"}'
        )
        cls.loader_dict = loaders.Dict.load(
            {
                "Variables": 3456
            }
        )

    def test_translating_to_other_loader(self):
        specific_deserializer = utils.LoaderSpecificDeserializer(
            {
                loaders.JsonString: lambda var, value: int(value),
            }
        )
        version_variable = Variable(self.loader_json, "version")
        version_variable.register_deserializer(specific_deserializer)

        self.assertEqual(version_variable._value, 42)

    def test_translating_to_any_loader(self):
        specific_deserializer = utils.LoaderSpecificDeserializer(
            {
                "*": lambda var, value: int(value)
            }
        )
        version_variable = Variable(self.loader_json, "version")
        version_variable.register_deserializer(specific_deserializer)

        self.assertEqual(version_variable._value, 42)

    def test_serializing_to_other_loader(self):
        specific_serializer = utils.LoaderSpecificSerializer(
            {
                loaders.JsonString: lambda var, value: json.dumps(value),
            }
        )
        version_variable = Variable(self.loader_json, "version")
        version_variable.register_serializer(specific_serializer)

        self.assertEqual(version_variable.serialize(), '"42"')

    def test_serializing_to_any_loader(self):
        specific_serializer = utils.LoaderSpecificSerializer(
            {
                "*": lambda var, value: json.dumps(value)
            }
        )
        version_variable = Variable(self.loader_json, "version")
        version_variable.register_serializer(specific_serializer)

        self.assertEqual(version_variable.serialize(), '"42"')
