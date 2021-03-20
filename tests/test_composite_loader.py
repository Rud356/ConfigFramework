import json
import unittest

from ConfigFramework import loaders, base_config, variables
from ConfigFramework.abstract import AbstractConfigVar
from ConfigFramework.dump_caster import DumpCaster
from tests.temp_files_utils import TempFile, rm_temp_dir


class TestCompositeConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.yaml, self.json = TempFile(), TempFile()
        with open(self.yaml.temp_file_obj, 'w') as y, open(self.json.temp_file_obj, 'w') as j:
            y.write("Rud: is author")
            j.write('{"admins_ids": [123, 456]}')
        self.json_loader = loaders.JsonLoader.load(self.json.temp_file_obj)
        self.yaml_loader = loaders.YAMLLoader.load(self.yaml.temp_file_obj)
        self.composite_loader: loaders.CompositeLoader = loaders.composite_loader.CompositeLoader.load(
            self.json_loader, self.yaml_loader
        )

    def test_basic_composite_loading(self):
        class Config(base_config.BaseConfig):
            Rud = variables.ConfigVar("Rud", self.composite_loader)
            admins_ids = variables.ConfigVar("admins_ids", self.composite_loader)

        config = Config()
        self.assertTrue(config.Rud.value == "is author" and config.admins_ids.value == [123, 456])

    def test_setting_values_to_composite_loader(self):
        class Config(base_config.BaseConfig):
            Rud = variables.ConfigVar("Rud", self.composite_loader)
            admins_ids = variables.ConfigVar("admins_ids", self.composite_loader)

        config = Config()
        config.Rud.value = 356
        self.assertEqual(self.yaml_loader.get('Rud'), 356)

    def test_dumping_to_specific_loader(self):
        temp_json_loader_file = TempFile()
        with temp_json_loader_file as json_path:
            with json_path.open(mode='w+') as j:
                j.write('{}')
            temp_loader = loaders.json_loader.JsonLoader.load(json_path)
            self.composite_loader.dump_to(temp_loader)

            with json_path.open(mode='r') as j:
                self.assertEqual(json.load(j), self.composite_loader.lookup_data)

    def test_dumping_composite_loader(self):
        class Config(base_config.BaseConfig):
            Rud = variables.ConfigVar("Rud", self.composite_loader)
            admins_ids = variables.ConfigVar("admins_ids", self.composite_loader)

        config = Config()
        config.Rud.value = 356
        config.dump()
        self.assertEqual('Rud: 356\n', self.yaml.temp_file_obj.read_text(encoding='utf8'))

    def test_dump_casters_relative_to_loader(self):
        caster = DumpCaster({
            loaders.YAMLLoader: str,
            '*': int
        })

        class Config(base_config.BaseConfig):
            Rud: AbstractConfigVar = variables.ConfigVar("Rud", self.composite_loader, dump_caster=caster)

        class AltConfig(base_config.BaseConfig):
            Rud: AbstractConfigVar = variables.ConfigVar(
                "Rud", loader=loaders.JsonStringLoader.load('{"Rud": "234"}'),
                dump_caster=caster
            )

        config = Config()
        val = config.Rud.dump_caster(config.Rud)
        self.assertTrue(isinstance(val, str))

        alt_config = AltConfig()
        val = alt_config.Rud.dump_caster(alt_config.Rud)
        self.assertTrue(isinstance(val, int))

    @classmethod
    def tearDownClass(cls) -> None:
        rm_temp_dir()
