from ConfigFramework import BaseConfig, ConfigVariable, JSONStringConfigLoader

config_loader = JSONStringConfigLoader('{"hello example": "world", "variable name": 1024}')


def validator_example(var):
    if var < 512:
        return True

    else:
        # Raising ValueError inside of validator will drop its message to log, instead of more abstract one
        # So you may tell how to fix something in config
        raise ValueError("And that's how you do more advanced messages about what's wrong")

        # You can optionally return False value instead of raising ValueError, so do it as you wish


class Config(BaseConfig):
    hello = ConfigVariable.variable("hello example", config_loader)
    # If you start this example - you will not see any error, because it took its default value!
    # So from this example you can see that even if variable is invalid - it gonna take a valid value
    # Even though if default value is also invalid - you will get an error
    variable_validation_example = ConfigVariable.variable(
        "variable name", config_loader, caster=int, validator=validator_example,
        default=128
    )


conf = Config()
print(conf.variable_validation_example)
