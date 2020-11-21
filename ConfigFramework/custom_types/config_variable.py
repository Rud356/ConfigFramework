from __future__ import annotations
from typing import TYPE_CHECKING
from . import logger

if TYPE_CHECKING:
    from ConfigFramework.custom_types.loaders import AbstractConfigLoader


class ConfigVariable:
    def __init__(
            self, key, value, loader: AbstractConfigLoader, *,
            caster=lambda x: x, dump_caster=lambda x: x
    ):
        self.key = key
        self._value = caster(value)
        self.loader = loader
        self.dump_caster = dump_caster
        self.caster = caster

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, var_value):
        try:
            self._value = self.caster(var_value)
            self.loader.set_variable(self.key, self.dump_caster(self.value))

        except Exception as e:
            logger.error(
                f"You've tried to set variable {self.key} a value {var_value} from loader {self.loader}\n",
                exc_info=e
            )
            raise e

    @classmethod
    def variable(cls, key, loader: AbstractConfigLoader, *, caster=lambda x: x, dump_caster=lambda x: x):
        return cls(key, loader[key], loader, caster=caster, dump_caster=dump_caster)

    def __repr__(self):
        return f"{self.key} = {self.value} ({self.loader})"

    def __str__(self):
        return repr(self)


__all__ = ("ConfigVariable", )
