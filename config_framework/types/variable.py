from __future__ import annotations

from typing import (
    TypeVar, Generic, Optional,
    Union, Any, TYPE_CHECKING,
    Type, Callable,
)

from . import custom_exceptions
from .variable_key import VariableKey

if TYPE_CHECKING:
    from .abstract.loader import AbstractLoader

Var = TypeVar("Var")


class Variable(Generic[Var]):
    _value: Var

    def __init__(
        self, source: AbstractLoader,
        key: Union[VariableKey, str],
        default: Optional[Var] = None
    ):
        self.source: AbstractLoader = source

        if isinstance(key, str):
            key = VariableKey(key)
        self.key: VariableKey = key
        self.default = default

    def __get__(
        self, instance: Optional[AbstractLoader], cls: Type[AbstractLoader]
    ) -> Union[Var, Variable[Var]]:
        """
        Gives you a value or Variable with your value depending on condition.

        :param instance: if it is None then you will receive Variable instance.
            If it's not - you will get just a value inside of Variable.
        :param cls: class from which variable was called.
        returns: Variable._value or Variable instance, depending on conditions,
            explained previously.
        """
        if instance is None:
            return self

        return self._value

    def __set__(self, value: Var) -> None:
        """
        Sets a new value to your variable.

        :raises config_framework.types.custom_exceptions.ValueValidationError:
            adds explanation on where is invalid value in your config and
            from which loader value is from. This contains also a traceback
            to your config_framework.types.custom_exceptions.InvalidValueError.
        """
        self.validator(value)
        self._value = value
        self.source[self.key] = self.serialize(self.source)

    def serialize(self: Variable, cast_for_loader: AbstractLoader) -> Any:  # noqa:
        # Might be used by other functions.
        """
        Casts value to specific loaders type so it can be saved.

        :param cast_for_loader: loader for which we are serializing variable.
        :returns: anything.
        """
        return self._value

    @classmethod
    def deserialize(
        cls: Type[Variable],
        cast_from_loader: AbstractLoader,  # noqa: Used by custom ones
        from_value: Any
    ) -> Var:
        """
        Performs additional type casting if loader doesn't provides it
        out of the box and returns variable with needed type that will also
        be validated after being casted.

        :param cast_from_loader: loader from which we are
            deserializing variable from.
        :param from_value: raw value from loader.
        :returns: validated and caster to python type value.
        :raises config_framework.types.custom_exceptions.ValueValidationError:
            adds explanation on where is invalid value in your config and
            from which loader value is from. This contains also a traceback
            to your config_framework.types.custom_exceptions.InvalidValueError.
        """
        from_value: Var
        cls.validate_value(from_value)
        return from_value

    @classmethod
    def validator(cls: Type[Variable], value: Var) -> bool:  # noqa: Will be used by others.
        """
        Checks if certain value is correct via users code.

        :param value: value of correct python type (after being casted from
            raw loader value) that will be validated.
        :returns: bool value representing if its correct or not.
        :raises config_framework.types.custom_exceptions.InvalidValueError: if
            you want to write more detailed reason why value is not valid you
            raise this exception.
        """
        return True

    def validate_value(self) -> bool:
        """
        Checks if certain value is correct via users code.

        :param value: value of correct python type (after being casted from
            raw loader value) that will be validated.
        :returns: bool value representing if its correct or not.

        :raises config_framework.types.custom_exceptions.ValueValidationError:
            adds explanation on where is invalid value in your config and
            from which loader value is from. This contains also a traceback
            to your config_framework.types.custom_exceptions.InvalidValueError.
        """
        try:
            return self.validator(self._value)

        except custom_exceptions.ValueValidationError as user_error:
            raise custom_exceptions.InvalidValueError(
                f"{self.key} got invalid value from source {self.source}"
            ) from user_error

    def validator_registration(
        self, f: Callable[[Type[Variable], Var], bool]
    ):
        setattr(self, "validator", f)

    def serializer_registration(
        self, f: Callable[[Variable, AbstractLoader], bool]
    ):
        setattr(self, "serializer", f)

    def deserializer_registration(
        self, f: Callable[[Variable, AbstractLoader], bool]
    ):
        setattr(self, "deserializer", f)

