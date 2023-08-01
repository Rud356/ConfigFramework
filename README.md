# ConfigFramework 4.0
![PyPI version](https://img.shields.io/pypi/v/ConfigFramework)
![Python version](https://img.shields.io/pypi/pyversions/ConfigFramework)
![PyPi downloads/m](https://img.shields.io/pypi/dm/ConfigFramework)
![Issues](https://img.shields.io/github/issues/Rud356/ConfigFramework)
[![Python package](https://github.com/Rud356/ConfigFramework/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Rud356/ConfigFramework/actions/workflows/python-tests.yml)

A small and simple framework to build your configs. 

This project been created mostly because of me myself needing some simplistic
and at the same time powerful enough tool to create configs, validate them through have simple interface.

## Installing
Pypi link: https://pypi.org/project/ConfigFramework

Install with command:
`pip install ConfigFramework`

To install with mypy you must use command:
`pip install ConfigFramework[mypy]`

If you have python below 3.11 or need toml format with ability to write it back:
`pip install ConfigFramework[toml]`

To install with mypy and dev dependencies building requirements you must use command:
`pip install ConfigFramework[mypy,dev]`

## Documentation
[ConfigFrameworks stable branch documentation](https://configframework.readthedocs.io)

### How to build docs for local usage
1. Install dev-requirements.txt via `pip install -r dev-requirements.txt`
2. Change a current directory to docs/
3. Execute `make html`
4. Open build/html folder and then open index.html in your browser

## Example of usage

Here's basic example:
```python3
from config_framework import BaseConfig, VariableKey, Variable
from config_framework.loaders import Dict

loader = Dict.load(
    data=dict(
        user_id=1,
        nested_val=dict(pi=3.14)
    )
)


class ConfigSample(BaseConfig):
    user_id: Variable[int] = Variable(VariableKey("user_id"))
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
```

See examples with explanation [here](https://github.com/Rud356/ConfigFramework/blob/master/examples/)

## Supported formats
Config formats:
- Yaml
- Toml (read only with default lib included with python 3.11, and read-write with toml external lib)
- Json (strings or files)
- Environment variables
- Pythons dictionaries
- Composite loading from multiple simple loaders

## Features
- Loading configs from multiple sources
- Creating custom loaders and variables types
- Flexible configs definition
- Config values validations
- Casting variables values to specific types using functions
- Casting to acceptable variable type before dumping variable to loader
- Variables serialization/deserialization depending on from which loader it was fetched
- Default values for per loader or per variable
- Translating one config loaders data to other (with or without including default values for each one)
- Composite loaders that allow you to define where to look up values using only one loader, that handles
  combining others
- Simple access to variables values
- Single entry point for initialization of config with loader

## About 4.0
This version of ConfigFramework is not backwards compatible and requires a bit of work to make migration.
It was needed to get rid of annoying initialization with one config loader per variable listing, which
also made it really hard to replace config sources and made it more uncertain where is the source of data for variable.

### What is different?
- Configs must get only one loader as input when initializing them, and all variables don't have argument for specifying
loader.
- Added toml support for python above 3.11 and with external library that adds ability to read and write data.
- Changes in internals regarding variables initialization to support assigning data from provided loader dynamically on
initialization of whole config.
- Added pyproject.toml for more modern package management.

### Known issues
- Typehint for `Variable[any_type]` doesn't work properly and give
only hints for Variable methods, while must give hints for any_type, when
called from instance of any subclass of BaseConfig
