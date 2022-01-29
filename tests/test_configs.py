import copy
import unittest
from typing import Any, Tuple

from config_framework import (
    VariableKey, BaseConfig, loaders,
    Variable, types
)


class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        config_data = loaders.Dict.load(
            {
                "rud": "356",
                "is author": True,
                "nested": {
                    "data": "value"
                }
            }
        )

        class BasicConfig(BaseConfig):
            rud: Variable[str] = Variable(config_data, "rud")
            is_author: Variable[str] = Variable(config_data, "is author")
            nested_data: Variable[str] = Variable(
                config_data, VariableKey("nested") / "data"
            )

            @staticmethod
            @rud.register_validator
            def validate_rud(variable: Variable, value: Any):
                if value != "356":
                    raise types.custom_exceptions.ValueValidationError(
                        "Value for Rud must be 356 only"
                    )

                return True

        cls.config_data = config_data
        cls.immutable_config: BasicConfig = BasicConfig()
        cls.ConfigClass = BasicConfig

    def test_variables_fetching(self):
        self.assertEqual(self.immutable_config.rud, "356")

    def test_assignment_to_immutable_config_instance(self):
        with self.assertRaises(NotImplementedError):
            self.immutable_config.rud = "356"

    def test_values_assignment(self):
        mutable_instance = copy.deepcopy(self.ConfigClass)(frozen=False)
        mutable_instance.is_author = False

    def test_validation_of_data(self):
        mutable_instance = copy.deepcopy(self.ConfigClass)(frozen=False)

        with self.assertRaises(types.custom_exceptions.InvalidValueError):
            # This value will fail check
            mutable_instance.rud = "366"

    def test_values_parsing(self):
        config_data = loaders.Dict.load(
            {
                "python": "3.6.7"
            }
        )

        class Config(BaseConfig):
            python: Variable[Tuple[int, int, int]] = Variable(
                config_data, "python"
            )

            @staticmethod
            @python.register_deserializer
            def deserialize_version(
                var: Variable, value: str
            ) -> Tuple[int, int, int]:
                version = tuple(map(int, value.split(".")))
                if len(version) != 3:
                    raise types.custom_exceptions.InvalidValueError(
                        "Version must contain 3 parts"
                    )

                return version # noqa: there's a check on being must be exactly 3 parts

        conf = Config()
        self.assertEqual(conf.python, (3, 6, 7))

    def test_invalid_values_parsing(self):
        config_data = loaders.Dict.load(
            {
                "python": "3.6.7.6"
            }
        )

        with self.assertRaises(types.custom_exceptions.InvalidValueError):
            python: Variable[Tuple[int, int, int]] = Variable(
                config_data, "python"
            )

            @python.register_deserializer
            def deserialize_version(
                var: Variable, value: str
            ) -> Tuple[int, int, int]:
                version = tuple(map(int, value.split(".")))
                if len(version) != 3:
                    raise types.custom_exceptions.InvalidValueError(
                        "Version must contain 3 parts"
                    )

                return version  # noqa: there's a check on being must be exactly 3 parts

    def test_values_serialization(self):
        config_data = loaders.Dict.load(
            {
                "python": "3.6.7"
            }
        )

        python: Variable[Tuple[int, int, int]] = Variable(
            config_data, "python"
        )

        @python.register_deserializer
        def deserialize_version(
            var: Variable, value: str
        ) -> Tuple[int, int, int]:
            version = tuple(map(int, value.split(".")))
            if len(version) != 3:
                raise types.custom_exceptions.InvalidValueError(
                    "Version must contain 3 parts"
                )

            return version  # noqa: there's a check on being must be exactly 3 parts

        @python.register_serializer
        def serialize_version(
            var: Variable, value: Tuple[int, int, int]
        ) -> str:
            if len(value) != 3:
                raise types.custom_exceptions.InvalidValueError(
                    "Version must contain 3 parts"
                )

            version = ".".join(map(str, value))
            return version

        self.assertEqual(config_data['python'], python.serialize())
