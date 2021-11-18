from config_framework.loaders import Dict
from config_framework import BaseConfig, VariableKey, Variable

loader = Dict.load(
    data=dict(
        nested_val=dict(
            longer_nested_value=dict(target="Hello world")
        )
    )
)


class ConfigSample(BaseConfig):
    path_to_variable = VariableKey("longer_nested_value") / "target"
    combined_key = VariableKey("nested_val") / path_to_variable

    var = Variable(loader, combined_key)


config = ConfigSample()
# This is an example of how you can combine multiple keys to split
# long keys into parts
print("Value:", config.var)
