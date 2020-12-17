from enum import Enum

# TODO: improve casters


class Casters(Enum):
    str: callable = str
    bool: callable = lambda s: s.lower() in {
        'true', '1', 'yes', 'on', 'ok'
    } if isinstance(s, str) else bool(s)
    int: callable = int
    float: callable = float
