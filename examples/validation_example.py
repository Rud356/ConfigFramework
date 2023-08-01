from config_framework import BaseConfig, VariableKey, Variable
from config_framework.loaders import Dict
from config_framework.types.custom_exceptions import ValueValidationError, InvalidValueError

loader = Dict.load(
    data=dict(user_id=2)
)


class ConfigSample(BaseConfig):
    user_id: Variable[int] = Variable(VariableKey("user_id"))

    @staticmethod
    @user_id.register_validator
    def validate_user_id(var, value):
        # Functions can return bool values or raise
        # config_framework.types.custom_exceptions.InvalidValueError
        # for more detailed description.
        if value != 2:
            raise ValueValidationError(f"User id must be 2 (got {value})")

        return True


try:
    # here it is okay
    config = ConfigSample(loader, frozen=False)

    # and from here we'll get error after changing value
    config.user_id = 3

except InvalidValueError as e:
    print(f"Oh well, we got the error!\nException: {e}")
