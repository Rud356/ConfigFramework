from typing import Any

from config_framework import BaseConfig, VariableKey, Variable
from config_framework.loaders import Dict

loader = Dict.load(
    data=dict(user_id="1")
)


class Uid(int):
    """
    Custom user id.
    """
    pass


class ConfigSample(BaseConfig):
    user_id: Variable[Uid] = Variable(VariableKey("user_id"))

    @staticmethod
    @user_id.register_serializer
    def serialize_user_id(var, value: Uid) -> Any:
        # Here we cast value back to int
        return str(int(value))

    @staticmethod
    @user_id.register_deserializer
    def deserialize_user_id(var, value: Any) -> Uid:
        # And there we cast our raw value to
        # Uid type so we can use it everywhere
        uid_value = Uid(value)
        return uid_value


# Here we will get error with more detailed explanation about what happened
# and our own addition will tell us more too!
config = ConfigSample(loader, frozen=False)
print(config.user_id)
print(type(config.user_id))

print("\nModifying values")
config.user_id = Uid("15")
print(config.user_id)
print(type(config.user_id))


# And here's the thing i wanted to show
print("\nStored values")
print(loader.get("user_id"))
# It is still string
print(type(loader.get("user_id")))
