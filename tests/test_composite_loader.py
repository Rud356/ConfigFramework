import unittest
import copy

from config_framework import loaders


class TestCompositeLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.loader_1: loaders.Dict = loaders.Dict.load(
            {
                "Hello world": "Rud is here",
                "Some key": "some value"
            }
        )
        cls.loader_2: loaders.Dict = loaders.Dict.load(
            {
                "Some key": "Just a duplicate key",
                "Other key": "testing order"
            }
        )
        cls.composite_loader: loaders.Composite = loaders.Composite.load(
            cls.loader_1, cls.loader_2,  # noqa: Those are loaders
            defaults={"pi": 3.14}
        )

    def test_fetching_duplicate_key(self):
        # according to load order - we must get firsts loader value
        self.assertEqual(self.composite_loader["Some key"], "some value")

    def test_dump_to_other_loader_without_defaults(self):
        loader = loaders.Dict.load({})
        self.composite_loader.dump_to(loader, include_defaults=False)

        with self.assertRaises(KeyError):
            pi = loader['pi']

        self.assertEqual(
            (
                self.loader_1['Hello world'],
                self.loader_1["Some key"],
                self.loader_2["Other key"]
            ),
            (
                loader['Hello world'],
                loader["Some key"],
                loader["Other key"]
            )
        )

    def test_dump_to_other_loader_with_defaults(self):
        loader = loaders.Dict.load({})
        self.composite_loader.dump_to(loader, include_defaults=True)

        self.assertEqual(loader['pi'], 3.14)

        self.assertEqual(
            (
                self.loader_1['Hello world'],
                self.loader_1["Some key"],
                self.loader_2["Other key"],
                self.composite_loader["pi"]
            ),
            (
                loader['Hello world'],
                loader["Some key"],
                loader["Other key"],
                loader['pi']
            )
        )

    def test_updating_values(self):
        loader_1 = copy.deepcopy(self.loader_1)
        loader_2 = copy.deepcopy(self.loader_2)
        composite_loader: loaders.Composite = loaders.Composite.load(
            loader_1, loader_2,
        )

        composite_loader['Hello world'] = "with new text"
        composite_loader["Some key"] = "this should modify only first loader"

        self.assertEqual(
            loader_1["Hello world"],
            "with new text"
        )
        self.assertEqual(
            loader_1["Some key"],
            "this should modify only first loader"
        )

        self.assertEqual(
            loader_2["Some key"],
            "Just a duplicate key"
        )

    def test_deleting_values(self):
        loader_1 = copy.deepcopy(self.loader_1)
        loader_2 = copy.deepcopy(self.loader_2)
        composite_loader: loaders.Composite = loaders.Composite.load(
            loader_1, loader_2,
        )

        # It should delete this value for all loaders, where key exists
        del composite_loader['Some key']
        with self.assertRaises(KeyError):
            text = loader_1["Some key"]

        with self.assertRaises(KeyError):
            text = loader_2["Some key"]

    def test_getting_missing_key(self):
        with self.assertRaises(KeyError):
            no_key = self.composite_loader["Not a key"]

    def test_setting_not_existing_key(self):
        with self.assertRaises(KeyError):
            self.composite_loader['keys'] = 123

    def test_deleting_missing_key(self):
        with self.assertRaises(KeyError):
            del self.composite_loader["Not a key"]
