from __future__ import annotations

from typing import (
    TypeVar, Generic, Optional,
    Union, Any, TYPE_CHECKING,
    Type, Callable, overload
)

from . import custom_exceptions
from .variable_key import VariableKey

if TYPE_CHECKING:
    from .abstract.loader import AbstractLoader

Var = TypeVar("Var")
CustomSerializer = Callable[["Variable", Var], Any]
CustomDeserializer = Callable[["Variable", Any], Var]
CustomValidator = Callable[["Variable", Var], bool]


class Variable(Generic[Var]):
    source: Optional[AbstractLoader]
    _value: Var

    def __init__(
        self,
        key: Union[VariableKey, str],
        default: Optional[Var] = None
    ):
        self.default = default
        if default is not None:
            self.validate_value(default)
            self.default = default

        if isinstance(key, str):
            key = VariableKey(key)

        self.key: VariableKey = key

    @overload
    def __get__(
        self, instance: None, cls: Any
    ) -> Variable[Var]:
        ...

    @overload
    def __get__(
        self, instance: AbstractLoader, cls: Type[AbstractLoader]
    ) -> Var:
        ...

    def __get__(
        self, instance: Optional[AbstractLoader],
        cls: Union[Type[AbstractLoader], Any]
    ) -> Union[Var, Variable[Var]]:
        """
        Gives you a value or Variable with your value depending on condition.

        :param instance: if it is None then you will receive Variable instance.
            If it's not - you will get just a value inside of Variable.
        :param cls: class from which variable was called.
        returns: Variable._value or Variable instance, depending on conditions,
            explained previously.
        :raises ValueError: if there are no defaults or
        """
        if instance:
            try:
                return self._value

            except AttributeError:
                if self.default is not None:
                    return self.default

                raise ValueError(f"No variable value set for variable with key {self.key}")

        else:
            return self

    def __set__(self, obj: Optional[object], value: Var) -> None:
        """
        Sets a new value to your variable.

        :param obj: object from which method was called.
        :param value: which value will be assigned to _value field.
        :raises config_framework.types.custom_exceptions.ValueValidationError:
            adds explanation on where is invalid value in your config and
            from which loader value is from. This contains also a traceback
            to your config_framework.types.custom_exceptions.InvalidValueError.
        """
        self.validate_value(value)
        self._value = value

    def _set_value_from_loader(self, loader: AbstractLoader) -> None:
        """
        Helps to set value to Variable object with validation to allow initialization of it
        during creating Config object, so users can choose desired loaders on startup.

        :param loader:
        :return:
        """
        self.source = loader
        if not self.default:
            value = self.deserialize(loader[self.key])

        else:
            value = self.deserialize(loader.get(self.key, self.default))

        self.__set__(self, value)

    def serialize(
        self: Variable
    ) -> Any:  # noqa:
        # Might be used by other functions.
        """
        Casts variables value to specific loaders type, so it can be saved.

        :returns: anything.
        """
        return self.custom_serializer(self, self._value)

    def deserialize(
        self,
        from_value: Any
    ) -> Var:
        """
        Performs additional type casting if loader doesn't provides it
        out of the box and returns variable with needed type that will also
        be validated after being casted.

        :param from_value: raw value from loader.
        :returns: validated and caster to python type value.
        :raises config_framework.types.custom_exceptions.ValueValidationError:
            adds explanation on where is invalid value in your config and
            from which loader value is from. This contains also a traceback
            to your config_framework.types.custom_exceptions.InvalidValueError.
        """
        casted_value: Var = self.custom_deserializer(self, from_value)
        self.validate_value(casted_value)
        return casted_value

    def validate_value(self, value: Var) -> bool:
        """
        Checks if certain value is correct via users code.

        :param value: value of correct python type (after being cast from
            raw loader value) that will be validated.
        :returns: bool value representing if It's correct or not.

        :raises config_framework.types.custom_exceptions.ValueValidationError:
            adds explanation on where is invalid value in your config and
            from which loader value is from. This contains also a traceback
            to your config_framework.types.custom_exceptions.InvalidValueError.
        """
        try:
            is_valid = self.custom_validator(self, value)
            if not is_valid:
                raise custom_exceptions.ValueValidationError()

            return is_valid

        except custom_exceptions.ValueValidationError as user_error:
            raise custom_exceptions.InvalidValueError(
                f"{self.key} got invalid value"
            ) from user_error

    def _validate_default_value(self) -> None:
        try:
            if self.default is None:
                return None

            self.validate_value(self.default)

        except custom_exceptions.ValueValidationError as err:
            raise ValueError(
                f"Invalid default value for variable {self.key}"
            ) from err

    @staticmethod
    def custom_serializer(variable: Variable, value: Var) -> Any:
        """
        Casts variables value to specific loaders type so it can be saved. This
        method can be set to instance of Variable using decorator
        <variable_instance>.register_serializer.

        :param variable: variable instance.
        :param value: the value that will actually be translated into loaders
            savable type.
        :returns: anything.
        """
        return value

    @staticmethod
    def custom_deserializer(variable: Variable, from_value: Any) -> Var:
        """
        Method for defining how your custom variables must be casted from
        loaders type to pythons one (if they don't translate 1:1). Can be
        set using decorator <variable_instance>.register_deserializer.

        :param variable: instance of Variable that is used to get
            information about where this value from and etc.
        :param from_value: raw value from loader.
        :returns: validated and caster to python type value.
        :raises config_framework.types.custom_exceptions.ValueValidationError:
            adds explanation on where is invalid value in your config and
            from which loader value is from. This contains also a traceback
            to your config_framework.types.custom_exceptions.InvalidValueError.
        """
        return from_value

    @staticmethod
    def custom_validator(variable: Variable, value: Var) -> bool:
        """
        Method for defining how your variable must be validated. Can be set
        using decorator <variable_instance>.register_validator.

        :param variable: instance of Variable that is used to get
            information about where this value from and etc.
        :param value: value of correct python type (after being casted from
            raw loader value) that will be validated.
        :returns: bool value representing if its correct or not.

        :raises config_framework.types.custom_exceptions.ValueValidationError:
            adds explanation on where is invalid value in your config and
            from which loader value is from. This contains also a traceback
            to your config_framework.types.custom_exceptions.InvalidValueError.
        """
        return True

    def register_validator(
        self, f: CustomValidator
    ) -> CustomValidator:
        """
        Registers passed function as custom_validator to be used later
        and instantly validates current value.

        :param f: some method that signature matches to CustomValidator.
        :return: function itself.
        """
        setattr(self, "custom_validator", f)
        # Validating already existing value with new validator
        if self.default is not None:
            self.validate_value(self.default)

        if hasattr(self, "_value"):
            self.validate_value(self._value)
        return f

    def register_serializer(
        self, f: CustomSerializer
    ) -> CustomSerializer:
        """
        Registers passed function as custom_serializer to be used later
        and instantly uses it to trigger possible errors.

        :param f: some method that signature matches to CustomSerializer.
        :return: function itself.
        """
        setattr(self, "custom_serializer", f)
        return f

    def register_deserializer(
        self, f: CustomDeserializer
    ) -> CustomDeserializer:
        """
        Registers passed function as custom_deserializer to be used later
        and instantly uses it to trigger possible errors on value from.

        :param f: some method that signature matches to CustomDeserializer.
        :return: function itself.
        """
        setattr(self, "custom_deserializer", f)
        return f
