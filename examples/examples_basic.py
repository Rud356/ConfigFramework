from ConfigFramework import ConfigVariable, JSONFileConfigLoader, BaseConfig

# creating basic json config loader and adding default values
json_loader = JSONFileConfigLoader.load("example_config.json", defaults={"sample_default": 2*2})


# Creating our config class
class Config(BaseConfig):
    # Defining some variables in config and applying
    field1 = ConfigVariable.variable("var1", json_loader)
    # Here's example of how you can redefine type casters
    # Caster is responsible for what type will be used across all app
    # Dump_caster responsible for how variable will be saved

    # Default casters that you might need if using for example env vars
    # are located at ConfigFramework/custom_types/casters.py
    field2 = ConfigVariable.variable("var23", json_loader, caster=str, dump_caster=int)

    # Here's example of how we getting defaults
    sample_default = ConfigVariable.variable("sample_default", json_loader)
    nested_variable = ConfigVariable.variable("nested_example/variables here", json_loader)

    # This function will be ran right after init
    def __post_init__(self, *args, **kwargs):
        print("Field2:", self.field2.value)
        print("here's nested example:", self.nested_variable.value)
        self.field2.value = "123"


conf = Config()
conf.dump()
