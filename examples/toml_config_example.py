from pathlib import Path
from config_framework import BaseConfig, VariableKey, Variable
from config_framework.loaders import Toml

loader = Toml.load(Path("example.toml"))


class ConfigSample(BaseConfig):
    user_id: Variable[int] = Variable(VariableKey("Data") / "user_id")
    pi_value = Variable(VariableKey("nested_val") / "pi")
    # Defaults only applied when key isn't found.
    # Also default values will be validated after initializing, and after you register new validator.
    some_value = Variable("not_found_value", default="Hello world")

    @staticmethod
    @user_id.register_validator
    def validate_user_id(var, value):
        # Functions can return bool values or raise
        # config_framework.types.custom_exceptions.InvalidValueError
        # for more detailed description.
        return value == 1

    def __post_init__(self) -> None:
        print("Post init here!")
        print("Values aren't locked yet")

        self.new_value = 122


config = ConfigSample(loader)
print("User id:", config.user_id)
print("Pi value:", config.pi_value)
print("Some value:", config.some_value)
print("Post inited value:", config.new_value)

# Configs by default aren't modifiable since frozen=True
# If you need changing variables for modifying config - you must
# create an instance of like this: ConfigSample(frozen=False)
# But right now it will raise NotImplementedError
config.some_value = "random"
