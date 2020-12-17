# ConfigFramework
A small and simple framework to build your configs. 

This project been created mostly because of me myself needing some simplistic
and same time powerful enough tool to create configs, validate them somewhat and to have easy interface.

Here's basic example:
```python
from ConfigFramework import ConfigVariable, JSONFileConfigLoader, BaseConfig

json_loader = JSONFileConfigLoader.load("example_config.json", defaults={"sample_default": 2*2})

class Config(BaseConfig):
    field1 = ConfigVariable.variable("var1", json_loader)
    field2 = ConfigVariable.variable("var23", json_loader, caster=str, dump_caster=int)
    sample_default = ConfigVariable.variable("sample_default", json_loader)

    def __post_init__(self, *args, **kwargs):
        print(self.field2)
        self.field2.value = "123"

conf = Config()
conf.dump()

```
[See full example with explanation here](https://github.com/Rud356/ConfigFramework/blob/master/examples/examples_basic.py)

## Installing
Pypi link: https://pypi.org/project/ConfigFramework

```pip install ConfigFramework```

## Important notes
- When you are using environment variables - you most likely will get error message for a first time
because I should've warned you about need in casters for it. You may change that behaviour in created config file for
config framework or create env loader with parameter mute_warn=True `EnvironmentConfigLoader(mute_warn=True)`
- Not all types can be translatable from one format to another so think of formats you are using
- Since [this commit](https://github.com/Rud356/ConfigFramework/tree/8acd351638897e49a3d08e4699b2af9b736e21dc)
for compatibility with environment variables and nested configs you will use only last part of variable path. For
example path `root/var` for environment variables will be taken as `var`

## Build your own config loaders, casters and fields usage examples

The way ConfigFramework been built allowing you to build your own loaders like that

```python
from ConfigFramework import AbstractConfigLoader

def load_from_internet() -> dict:
    ...

def upload_to_cloud(data):
    ...

class NewCustomConfigLoader(AbstractConfigLoader):
    @classmethod
    def load(cls, defaults=None):
        data: dict = load_from_internet()
        return cls(data, defaults)

    def dump(self):
        upload_to_cloud(self.data)

```

If you feel like you need some custom data type for your loader - why not to make it?
You will only need to write functions that will cast data to pythons type and back to savable format!

```python
from ConfigFramework import BaseConfig, ConfigVariable, JSONFileConfigLoader

loader = JSONFileConfigLoader.load("example_json.json")

class MyCustomType:
    def __init__(self, data):
        self.your_data = data

    @classmethod
    def load_from_string(cls, serialized: str):
        ...
        data = serialized
        return cls(data)
    
    def dump(self) -> str:
        ...


class Config(BaseConfig):
    variable_1 = ConfigVariable.variable(
        "example_var", loader,
        caster=MyCustomType.load_from_string, dump_caster=MyCustomType.dump
    )    

```

You may also want to cast one config to other type and i allow you to! Look at how easy it is:

```python
from ConfigFramework import YAMLConfigLoader, JSONFileConfigLoader

yaml_loader = YAMLConfigLoader.load("testing.yaml")
json_loader = JSONFileConfigLoader.load("testing.json")

new_loader = json_loader.dump_to_other_loader(yaml_loader)

```

But keep in mind that not all types are easily translated over formats (for example arrays and mappings) but you may
write serializers if you need!

It is possible to add validators and default values to exact field, and if something is wrong - get error message about
that:
```python
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
```

Examples of validation, defaulting and other:
- [Basic validation](https://github.com/Rud356/ConfigFramework/blob/master/examples/variable_validator_example.py)
- [Advanced validation](https://github.com/Rud356/ConfigFramework/blob/master/examples/example_advanced_validation.py)
- [Defaults per field](https://github.com/Rud356/ConfigFramework/blob/master/examples/example_default_variables_per_field.py)

Out of the box you also may combine multiple ConfigLoaders:
see in [combined config loaders example](https://github.com/Rud356/ConfigFramework/blob/master/examples/example_combined_loaders.py)

If you need some default type casters (for example if you loading ini file) - you may use one's from 
`ConfigFramework.custom_types.casters.Casters`

Some more examples [here](https://github.com/Rud356/ConfigFramework/tree/master/examples)

## Configuring

ConfigFramework have its own config, but there's not too much things you might need at the end.
Yet if you won't set `EnvironmentConfigLoader.mute_warning` to `False` - you'll be getting warning when creating
EnvironmentConfigLoader about need in casters for everything and not being able to dump loader itself somewhere.
Also it can help you set a path for log files.

If you need to change location of config file - just set an environment variable `CONFIGFRAMEWORK_SETTINGS_PATH`
to your liking with path to settings file.