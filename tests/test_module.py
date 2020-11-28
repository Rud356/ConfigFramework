import json
import unittest
from os import unlink

from ConfigFramework import (
    ConfigVariable, JSONStringConfigLoader, JSONFileConfigLoader, YAMLConfigLoader,
    CompositeConfigLoader, BaseConfig
)


class TestConfigFramework(unittest.TestCase):
    def test_combined_loader(self):
        config_loader_1 = JSONStringConfigLoader('{"a": "world"}')
        config_loader_2 = JSONStringConfigLoader('{"pretty simple": true}')
        combined_loader = CompositeConfigLoader.load(config_loader_1, config_loader_2)

        class Config(BaseConfig):
            hello = ConfigVariable.variable("a", combined_loader)
            is_it_simple = ConfigVariable.variable("pretty simple", combined_loader)

        conf = Config()
        self.assertEqual(conf.hello.value, 'world')
        self.assertTrue(conf.is_it_simple.value)

    def test_usual_loader_and_saving(self):
        with open('testing', mode='w+') as s:
            s.writelines('{"a": "world"}')

        json_loader = JSONFileConfigLoader.load("testing")

        class Config(BaseConfig):
            hello = ConfigVariable.variable("a", json_loader)

            def __post_init__(self, *args, **kwargs):
                self.hello.value = "Tests"

        conf = Config()
        conf.hello.loader.dump()

        with open('testing') as f:
            self.assertEqual(json.load(f), json.loads('{"a": "Tests"}'))

        unlink('testing')

    def test_nested_loading_and_saving(self):
        with open('testing', mode='w+') as s:
            s.writelines('{"a": "world", "b": {"nested_var": "nested_val"}}')

        json_loader = JSONFileConfigLoader.load("testing")

        class Config(BaseConfig):
            nested = ConfigVariable.variable("b/nested_var", json_loader)

            def __post_init__(self, *args, **kwargs):
                self.nested.value = "Tests"

        conf = Config()
        conf.nested.loader.dump()

        with open('testing') as f:
            self.assertEqual(json.load(f), json.loads('{"a": "world", "b": {"nested_var": "Tests"}}'))

        unlink('testing')

    def test_yaml(self):
        with open('testing', mode='w+') as s:
            s.writelines('a: 12')

        yaml_loader = YAMLConfigLoader.load("testing")

        class Config(BaseConfig):
            a = ConfigVariable.variable("a", yaml_loader)

            def __post_init__(self, *args, **kwargs):
                self.a.value = 12

        conf = Config()
        unlink('testing')

        self.assertEqual(conf.a.value, 12)

    def test_translating(self):
        with open('testing.yaml', mode='w+') as yml, open('testing.json', mode='w+') as j:
            yml.writelines(['a: 12\n', 'b: 24'])
            j.writelines('{"c": 12}')

        yaml_loader = YAMLConfigLoader.load("testing.yaml")
        json_loader = JSONFileConfigLoader.load("testing.json")

        new_loader = json_loader.dump_to_other_loader(yaml_loader)

        self.assertEqual(new_loader.data, {"c": 12})

        unlink('testing.yaml')
        unlink('testing.json')
