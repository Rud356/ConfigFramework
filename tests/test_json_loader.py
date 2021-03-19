import json
import unittest

from ConfigFramework.loaders import JsonLoader

from tests.temp_files_utils import TempFile


class TestJsonLoader(unittest.TestCase):
    def test_loading_and_dumping(self):
        with TempFile() as path:
            with path.open(mode='w+') as f:
                json.dump({"Rud": 356}, f)

            loader = JsonLoader.load(path)
            loader['Rud'] = "hello"
            loader.dump()

            with path.open(mode='r') as f:
                self.assertEqual(loader.data, json.load(f))
