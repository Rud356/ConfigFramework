from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from . import logger

if TYPE_CHECKING:
    from ConfigFramework.custom_types.loaders import AbstractConfigLoader


class ConfigVariable:
    """
    Class that helps you manage variables from configs.


    If you need to specify variable that lies under other keys:
    you have to specify path to variable like a relative path from config root

    Example: config_root/setups/proxy_url

    Class usage examples:
        get value of variable  > VarName.value
        set value to variable  > VarName.value = other
        init variable in class > ConfigVariable.variable('some key', loader)
        init variable that is under other key: ConfigVariable.variable('some key/other key/var', loader)

    @:param key: specifies under which key the value is
    @:param value: provides interface to get and change value of variable
    @:param loader: AbstractConfigLoader
    @:param caster: specifies func that is used to give var to your app
    @:param dump_caster: specifies func to cast variables before dumping them
    """
    def __init__(
            self, key, value, loader: AbstractConfigLoader, *,
            caster=lambda x: x, dump_caster=lambda x: x, validator=lambda v: True, default=None
    ):
        self.key = key
        self._value = caster(value)
        self.loader = loader
        self.caster = caster
        self.dump_caster = dump_caster

        self.validator = validator
        self._validate_value(validator, default)

    def _validate_value(self, validator: Callable, default):
        """
        Function helps us validate variables (including default variable) through users validation function

        :param validator:
        :param default:
        :return:
        """
        try:
            if not validator(self._value):
                raise ValueError(f"Invalid value for variable | {self.key} |")

        except ValueError as invalid_value_exc:
            if default is None:
                logger.error(invalid_value_exc)
                raise invalid_value_exc

            else:
                self._value = default

                def validate_default_variable(var):
                    try:
                        return validator(var)

                    except ValueError as invalid_default_var:
                        raise ValueError(
                            f"Invalid default value for key | {self.key} | in loader {self.loader}"
                        ) from invalid_default_var

                self._validate_value(validate_default_variable, None)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, var_value):
        rollback_value = self._value

        try:
            self._value = self.caster(var_value)
            self._validate_value(self.validator, None)
            self.loader.set_variable(self.key, self.dump_caster(self.value))

        except Exception as e:
            logger.error(
                f"You've tried to set variable {self.key} a value {var_value} from loader {self.loader}\n",
                exc_info=e
            )
            self._value = rollback_value
            raise ValueError(f"Something gone wrong on setting value of {self.key}") from e

    @classmethod
    def variable(
            cls, key, loader: AbstractConfigLoader, *, caster=lambda x: x, dump_caster=lambda x: x,
            validator=lambda v: True, default=None
    ):
        """
        Method for creating a ConfigVariable with a bit less parameters.

        @:param key: specifies under which key the value is
        @:param loader: AbstractConfigLoader
        @:param caster: specifies func that is used to give var to your app
        @:param dump_caster: specifies func to cast variables before dumping them
        :return: ConfigVariable
        """
        return cls(
            key, loader[key], loader,
            caster=caster, dump_caster=dump_caster,
            validator=validator, default=default
        )

    def __repr__(self):
        return f"{self.key} = {self.value} ({self.loader})"

    def __str__(self):
        return repr(self)


__all__ = ("ConfigVariable", )
