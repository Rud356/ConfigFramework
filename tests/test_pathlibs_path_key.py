import unittest

from pathlib import Path
from ConfigFramework.loaders import DictLoader


class TestPathAsKey(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.loader = DictLoader.load(
            {
                "a": 123, "b": 2331,
                "c": {
                    "k": {
                        "some": "value"
                    }
                }
            }
        )

    def test_path_as_key(self):
        val_1 = self.loader.get("c/k/some")
        val_2 = self.loader.get(Path("c/k/some"))
        self.assertEqual(val_1, val_2)

    def test_building_path(self):
        val_1 = self.loader.get("c/k/some")
        val_2 = self.loader.get(Path("c") / "k" / "some")
        self.assertEqual(val_1, val_2)
