from __future__ import annotations

from typing import Dict, Union, Any, Type, Optional

from config_framework.loaders.composite import Composite
from config_framework.types import Variable
from config_framework.types.abstract import AbstractLoader
from config_framework.types.variable import Var, CustomSerializer


class LoaderSpecificSerializer:
    """
    Class that helps to create serializers that act differently
    depending on where form variable were loaded.
    """
    def __init__(self, serializers: Dict[
        Union[str, Type[AbstractLoader]],
        CustomSerializer
    ]):
        """
        :param serializers: dictionary of loaders (or * as any not fitting)
            mapped to their deserializers.
        :return: nothing.
        """
        self.serializers: Dict[
            Union[str, Type[AbstractLoader]],
            CustomSerializer
        ] = serializers

    def __call__(
        self,
        variable: Variable,
        value: Var,
    ) -> Any:
        """
        Casts value to specific loaders type so it can be saved.

        :param value: python value that needs
            to be transformed to loaders type.
        :returns: anything.
        """
        assert hasattr(variable, "source"), f"No source loader specified for variable {variable.key}"
        cast_for_loader: Optional[AbstractLoader] = variable.source
        assert cast_for_loader is not None, f"Variable {variable.key} has loader set to None"

        if isinstance(cast_for_loader, Composite):
            cast_for_loader = self.fetch_original_source(
                variable,  # noqa: we need this value from internals
                cast_for_loader
            )

        try:
            if '*' in self.serializers:
                serializer: CustomSerializer = self.serializers.get(
                    type(cast_for_loader), self.serializers['*']
                )

            else:
                serializer = self.serializers[
                    type(cast_for_loader)
                ]

        except KeyError:
            raise KeyError(
                f"Serializer for {cast_for_loader} isn't specified"
                " and not found any default one."
            )

        return serializer(variable, value)

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
