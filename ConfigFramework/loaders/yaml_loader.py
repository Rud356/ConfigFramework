from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import Dict, Optional, Union, TYPE_CHECKING

import yaml

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.custom_types import data_type, defaults_type

try:
    from yaml import CLoader as Loader, CDumper as Dumper

except ImportError:
    # Those are actually replacements for CDumper/CLoader
    # and so there must be no problem
    from yaml import Loader, Dumper  # type: ignore


if TYPE_CHECKING:
    from os import PathLike


class YAMLLoader(AbstractConfigLoader):
    dumper = partial(yaml.dump, Dumper=Dumper)
    loader = partial(yaml.load, Loader=Loader)

    def __init__(self, data: data_type, defaults: defaults_type, config_path: Path):
        super().__init__(data, defaults)
        self.config_path = config_path

    @classmethod
    def load(  # type: ignore
        cls, config_path: Union[str, Path, PathLike[str]], defaults: Optional[Dict] = None
    ):
        config_path = Path(config_path)

        if not config_path.is_file():
            raise ValueError(f"Invalid file path: {config_path}")

        with open(config_path, encoding='utf8') as yaml_f:
            return cls(cls.loader(yaml_f), defaults, config_path)

    def dump(self, include_defaults: bool = False) -> None:
        to_dump = self.data

        if include_defaults:
            to_dump = dict(self.lookup_data)

        with open(self.config_path, 'w', encoding="utf8") as yaml_f:
            self.dumper(to_dump, yaml_f)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.config_path}"
