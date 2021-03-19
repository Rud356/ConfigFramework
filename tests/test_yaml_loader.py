import json
import unittest

from ConfigFramework.loaders import YAMLLoader

from .temp_files_utils import TempFile


class TestYamlLoader(unittest.TestCase):
    def test_loading_and_dumping(self):
        with TempFile() as path:
            with path.open(mode='w+') as f:
                f.write("Rud: 356")

            loader = YAMLLoader.load(path)
            loader['Rud'] = "hello"
            loader.dump()

            with path.open(mode='r') as f:
                self.assertEqual(f.read(), 'Rud: hello\n')
