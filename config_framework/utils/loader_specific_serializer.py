from __future__ import annotations

from typing import Dict, Union, Any, Callable

from config_framework.loaders.composite import Composite
from config_framework.types import Variable
from config_framework.types.abstract import AbstractLoader
from config_framework.types.variable import Var


class LoaderSpecificSerializer:
    """
    Class that helps to create serializers that act differently
    depending on where form variable were loaded.
    """
    def __init__(self, serializers: Dict[
        Union[AbstractLoader, str],
        Callable[[Var, AbstractLoader], Any]
    ]):
        """
        :param serializers: dictionary of loaders (or * as any not fitting)
            mapped to their serializers.
        :return: nothing.
        """
        self.serializers: Dict[
            Union[AbstractLoader, str],
            Callable[[Var, AbstractLoader], Any]
        ] = serializers

    def __call__(
        self,
        variable: Variable,
        cast_for_loader: AbstractLoader
    ) -> Any:
        """
        Casts value to specific loaders type so it can be saved.

        :param cast_for_loader: loader for which we are serializing variable.
        :returns: anything.
        """
        if isinstance(cast_for_loader, Composite):
            cast_for_loader = self.fetch_original_source(
                variable, cast_for_loader
            )

        serializer = self.serializers.get(cast_for_loader, None)

        if serializer is None:
            try:
                serializer = self.serializers['*']

            except KeyError:
                raise KeyError(
                    f"Serializer for {cast_for_loader} isn't specified"
                    " and not found any default one."
                )

        return serializer(variable, cast_for_loader)

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
