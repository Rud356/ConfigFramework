class InvalidValueError(ValueError):
    """
    Raised to give traceback about variable validations with more details.
    """


class ValueValidationError(InvalidValueError):
    """
    Raised if received value that hasn't passed users checks.
    """
    pass
