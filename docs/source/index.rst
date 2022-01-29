Welcome to ConfigFramework's documentation!
===========================================

.. toctree::
    self
    modules.rst
    :maxdepth: 2

ConfigFramework
===============
.. image:: https://img.shields.io/pypi/v/ConfigFramework
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/ConfigFramework
    :alt: Python version

.. image:: https://img.shields.io/pypi/dm/ConfigFramework
    :alt: PyPi downloads/m

.. image:: https://img.shields.io/github/issues/Rud356/ConfigFramework
    :alt: Issues count



A small and simple framework to build your configs.

This project been created mostly because of me myself needing some simplistic
and at the same time powerful enough tool to create configs, validate them through have simple interface.

Installing
==========
Install with command:
``pip install ConfigFramework``

To install with mypy you must use command:
``pip install ConfigFramework[mypy]``

To install with mypy and docs building requirements you must use command:
``pip install ConfigFramework[mypy,docs]``

Example of usage
================

.. code-block:: python

    from typing import Tuple
    from config_framework import BaseConfig, VariableKey, Variable, types
    from config_framework.loaders import Dict

    loader = Dict.load(
        data=dict(
            user_id=1,
            nested_val=dict(pi=3.14),
            python="3.6.7"
        )
    )


    class ConfigSample(BaseConfig):
        user_id: Variable[int] = Variable(loader, VariableKey("user_id"))
        pi_value = Variable(loader, VariableKey("nested_val") / "pi")
        # Defaults only applied when key isn't found.
        # Also default values will be validated after initializing
        # and after you register new validator.
        some_value = Variable(loader, "not_found_value", default="Hello world")
        python: Variable[Tuple[int, int, int]] = Variable(
              loader, "python"
          )

        @staticmethod
        @python.register_deserializer
        def deserialize_version(
            var: Variable, value: str
        ) -> Tuple[int, int, int]:
            version = tuple(map(int, value.split(".")))
            if len(version) != 3:
                raise types.custom_exceptions.InvalidValueError(
                    "Version must contain 3 parts"
                )

            return version  # noqa: there's a check on being must be exactly 3 parts

        @staticmethod
        @python.register_serializer
        def serialize_version(
            var: Variable, value: Tuple[int, int, int]
        ) -> str:
            if len(value) != 3:
                raise types.custom_exceptions.InvalidValueError(
                    "Version must contain 3 parts"
                )

            version = ".".join(map(str, value))
            return version

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


    config = ConfigSample()
    print("User id:", config.user_id)
    print("Pi value:", config.pi_value)
    print("Some value:", config.some_value)
    print("Post inited value:", config.new_value)

    # Configs by default aren't modifiable since frozen=True
    # If you need changing variables for modifying config - you must
    # create an instance of like this: ConfigSample(frozen=False)
    # But right now it will raise NotImplementedError
    config.some_value = "random"


See examples with explanation `here <https://github.com/Rud356/ConfigFramework/blob/master/examples/>`_

Supported config formats
========================
- Yaml
- Json (strings or files)
- Environment variables
- Pythons dictionaries
- Composite loading from multiple simple loaders

Features
========
- Loading configs from multiple sources
- Creating custom loaders and variables types
- Nested configs
- Flexible configs definition
- Config values validations
- Casting variables values to specific types using functions
- Casting to acceptable variable type before dumping variable to loader
- Variables serialization/deserialization depending on from which loader it was fetched
- Default values for per loader or per variable
- Translating one config loaders data to other (with or without including default values for each one)
- Composite loaders that allow you to define where to look up values using only one loader, that handles
  combining others
- Simpler access to variables values (new in 3.0)

About 3.0
=========
This version of config framework breaks many things and has other structure,
so you will have to manually migrate to this one. I think it was necessary
to improve many things, and I hope it will make your life easier.

What's different?
=================
- Now module will be called config_framework when you import it into project
- Structure of whole project is different comparing to 2.0
- Usage of VariableKey to create key that will tell how to access nested values
  without worrying about what symbols to use, but requiring to explicitly write
  VariableKey whenever you want to go from this root key
- Improved usability by using descriptors and making more logical arguments order
- By default, config will not allow you assigning any values after `__post_init__` was called

Known issues
============
- Typehint for `Variable[any_type]` doesn't work properly and give
  only hints for Variable methods, while must give hints for any_type, when
  called from instance of any subclass of BaseConfig (This is related to Pycharm
  only and I can not fix it, see: https://youtrack.jetbrains.com/issue/PY-47698 )

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
