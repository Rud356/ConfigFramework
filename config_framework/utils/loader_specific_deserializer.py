from __future__ import annotations

from typing import Dict, Union, Any, Callable, Type

from config_framework.loaders.composite import Composite
from config_framework.types import Variable
from config_framework.types.abstract import AbstractLoader
from config_framework.types.variable import Var


class LoaderSpecificDeserializer:
    """
    Class that helps to create deserializer that acts differently
    depending on where variable is loaded from.
    """
    def __init__(self, deserializers: Dict[
        Union[AbstractLoader, str],
        Callable[[Type[Variable], Var, AbstractLoader], Any]
    ]):
        """
        :param deserializers: dictionary of loaders (or * as any not fitting)
            mapped to their deserializers.
        :return: nothing.
        """
        self.deserializers: Dict[
            Union[AbstractLoader, str],
            Callable[[Type[Variable], Var, AbstractLoader], Any]
        ] = deserializers

    def __call__(
        self,
        cls: Type[Variable],
        variable: Variable,
        cast_from_loader: AbstractLoader
    ) -> Any:
        """
        Casts value to specific loaders type so it can be saved.

        :param cast_from_loader: loader for which we are serializing variable.
        :returns: anything.
        """
        if isinstance(cast_from_loader, Composite):
            cast_from_loader = self.fetch_original_source(
                variable, cast_from_loader
            )

        deserializer = self.deserializers.get(cast_from_loader, None)

        if deserializer is None:
            try:
                deserializer = self.deserializers['*']

            except KeyError:
                raise KeyError(
                    f"Deserializer for {cast_from_loader} isn't specified"
                    " and not found any default one."
                )

        return deserializer(cls, variable, cast_from_loader)

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
