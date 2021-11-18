from config_framework import BaseConfig, VariableKey, Variable
from config_framework.loaders import Dict
from config_framework.types.custom_exceptions import ValueValidationError

loader = Dict.load(
    data=dict(user_id=1)
)


class ConfigSample(BaseConfig):
    user_id: Variable[int] = Variable(loader, VariableKey("user_id"))

    @staticmethod
    @user_id.register_validator
    def validate_user_id(var, value):
        # Functions can return bool values or raise
        # config_framework.types.custom_exceptions.InvalidValueError
        # for more detailed description.
        if value != 2:
            raise ValueValidationError(f"User id must be 2 (got {value})")

        return True


# Here we will get error with more detailed explanation about what happened
# and our own addition will tell us more too!
config = ConfigSample()
