from ConfigFramework import BaseConfig, ConfigVariable, JSONStringConfigLoader

config_loader = JSONStringConfigLoader('{"hello example": "world", "variable name": 1024}')


def validator_example(var):
    if var < 512:
        return True

    else:
        # Raising ValueError inside of validator will drop its message to log, instead of more abstract one
        # So you may tell how to fix something in config
        raise ValueError("And that's how you do more advanced messages about what's wrong")


class Config(BaseConfig):
    hello = ConfigVariable.variable("hello example", config_loader)
    variable_validation_example = ConfigVariable.variable(
        "variable name", config_loader, caster=int, validator=validator_example
    )


conf = Config()
