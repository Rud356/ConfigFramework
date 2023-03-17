from __future__ import annotations

from typing import Dict, Union, Any, Type, Optional

from config_framework.loaders.composite import Composite
from config_framework.types import Variable
from config_framework.types.abstract import AbstractLoader
from config_framework.types.variable import Var, CustomDeserializer


class LoaderSpecificDeserializer:
    """
    Class that helps to create deserializer that acts differently
    depending on where variable is loaded from.
    """
    def __init__(self, deserializers: Dict[
        Union[str, Type[AbstractLoader]],
        CustomDeserializer
    ]):
        """
        :param deserializers: dictionary of loaders (or * as any not fitting)
            mapped to their deserializers.
        :return: nothing.
        """
        self.deserializers: Dict[
            Union[str, Type[AbstractLoader]],
            CustomDeserializer
        ] = deserializers

    def __call__(
        self,
        variable: Variable[Var],
        from_value: Any,
    ) -> Var:
        """
        Casts value to specific loaders type, so it can be saved.

        :param from_value: raw value from loader.
        :returns: validated and caster to python type value.
        :raises config_framework.types.custom_exceptions.ValueValidationError:
            adds explanation on where is invalid value in your config and
            from which loader value is from. This contains also a traceback
            to your config_framework.types.custom_exceptions.InvalidValueError.
        """
        assert hasattr(variable, "source"), f"No source loader specified for variable {variable.key}"
        cast_from_loader: Optional[AbstractLoader] = variable.source
        assert cast_from_loader is not None, f"Variable {variable.key} has loader set to None"

        if isinstance(cast_from_loader, Composite):
            cast_from_loader = self.fetch_original_source(
                variable, cast_from_loader
            )

        try:
            if '*' in self.deserializers:
                deserializer: CustomDeserializer = self.deserializers.get(
                    type(cast_from_loader), self.deserializers['*']
                )

            else:
                deserializer = self.deserializers[
                    type(cast_from_loader)
                ]

        except KeyError:
            raise KeyError(
                f"Deserializer for {cast_from_loader} isn't specified"
                " and not found any default one."
            )

        deserialized_variable: Var = deserializer(
            variable,
            from_value
        )
        variable.validate_value(deserialized_variable)
        return deserialized_variable

    @staticmethod
    def fetch_original_source(
        variable: Variable, composite_loader: Composite
    ) -> AbstractLoader:
        """
        Function that helps us fetch a loader from which variable originates.
        :param variable: Variable instance.
        :param composite_loader: some composite loader.
        :return: loader instance.
        """
        for loader in composite_loader.loaders:
            try:
                loader[variable.key]

            except KeyError:
                continue

            else:
                return loader

        else:
            raise ValueError(
                f"{variable} isn't taken from {composite_loader}"
            )
