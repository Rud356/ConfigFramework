from ConfigFramework import BaseConfig, ConfigVariable, JSONStringConfigLoader

config_loader = JSONStringConfigLoader('{"hello example": "world", "variable name": 1024}')


class Config(BaseConfig):
    hello = ConfigVariable.variable("hello example", config_loader)
    # That's how you can add simplest validator for variable
    # If you need to make it as simple as possible - just make function that returns bool value
    # So you will see an error in your console and log file with name of var that got wrong value
    variable_validation_example = ConfigVariable.variable(
        "variable name", config_loader, caster=int, validator=lambda var: var < 512
    )


conf = Config()
