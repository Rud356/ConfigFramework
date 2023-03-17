from __future__ import annotations

from typing import Iterable, Union, Iterator, List


class VariableKey(Iterable):
    """
    Class that helps us organize how keys for config variables
    to look for inside of some complicated nested structures.
    """
    root_key: str
    next_pieces: List[VariableKey]

    __slots__ = ("root_key", "next_pieces")

    def __init__(self, root_key: str):
        """
        Initializes new variable key.

        :param root_key: string key that will be used to fetch value
            for certain config variable.
        :raises TypeError: if received not a str instance.
        """
        if not isinstance(root_key, str):
            raise ValueError(
                "Root key for VariableKey must be of type str: "
                f"got {type(root_key)}"
            )

        self.root_key = root_key
        self.next_pieces = []

    def __truediv__(self, other_key: Union[str, VariableKey]) -> VariableKey:
        """
        Creates a new piece of key, assigns it as next_piece and gives
        fresh piece as return to keep creating parts.

        :param other_key: value that will be assigned to
            next_piece of this key.
        :returns: next variable key.

        :raises TypeError: if received not VariableKey or str.
        """
        if isinstance(other_key, str):
            self.next_pieces.append(VariableKey(other_key))

        elif isinstance(other_key, type(self)):
            self.next_pieces.append(other_key)

        else:
            raise TypeError(
                "Invalid key type provided (must be str or VariableKey): "
                f"got {type(other_key)}"
            )

        return self

    def __iter__(self) -> Iterator[str]:
        """
        Gives iterable that will yield parts of a full key that will
        give be used to go inside of nested configs.

        :return: string.
        """
        yield self.root_key

        if self.next_pieces:
            for next_piece in self.next_pieces:
                yield from next_piece

    def __str__(self) -> str:
        return "[/]".join(iter(self))
