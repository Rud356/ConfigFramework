import unittest

from ConfigFramework import loaders, base_config, variables


class TestConfigs(unittest.TestCase):
    def test_creating_basic_config(self):
        json_string_loader = loaders.JsonStringLoader.load('{"Rud": "original author"}')

        class ConfigSample(base_config.BaseConfig):
            rud = variables.ConfigVar("Rud", json_string_loader)

        config = ConfigSample()
        self.assertTrue(config.rud == "original author")

    def test_assigning_value(self):
        json_string_loader = loaders.JsonStringLoader.load('{"Rud": "original author"}')

        class ConfigSample(base_config.BaseConfig):
            rud = variables.ConfigVar("Rud", json_string_loader)

        config = ConfigSample()
        config.rud = "Hello world"
        self.assertTrue(config.rud == "Hello world")

    def test_assigning_to_constant(self):
        json_string_loader = loaders.JsonStringLoader.load('{"Rud": "original author"}')

        class ConfigSample(base_config.BaseConfig):
            rud = variables.ConfigVar("Rud", json_string_loader, constant=True)

        config = ConfigSample()

        try:
            config.rud = "Hello world"

        except NotImplementedError:
            return True

    def test_constant_field_using_function(self):
        json_string_loader = loaders.JsonStringLoader.load('{"Rud": "original author"}')

        class ConfigSample(base_config.BaseConfig):
            rud = variables.constant_var(variables.ConfigVar("Rud", json_string_loader))

        config = ConfigSample()

        try:
            config.rud = "Hello world"

        except NotImplementedError:
            return True

    def test_nested_config_classes(self):
        json_string_loader = loaders.JsonStringLoader.load('{"Rud": "original author", "Rud356": "test"}')

        class ConfigSample(base_config.BaseConfig):
            rud = variables.ConfigVar("Rud", json_string_loader)

            class SubConfig(base_config.BaseConfig):
                rud356 = variables.ConfigVar("Rud356", json_string_loader)

        config = ConfigSample()
        self.assertTrue(config.SubConfig.rud356 == "test")

    def test_config_variable_creation_with_predefined_args(self):
        json_string_loader = loaders.JsonStringLoader.load('{"Rud": "original author"}')

        class RudVariable(variables.ConfigVar):
            def __init__(self):
                super().__init__(key="Rud", loader=json_string_loader)

        class ConfigSample(base_config.BaseConfig):
            rud = RudVariable

        config = ConfigSample()
        self.assertTrue(config.rud == "original author")
