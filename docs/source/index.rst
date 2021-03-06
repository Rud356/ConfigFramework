Welcome to ConfigFramework's documentation!
===========================================

.. toctree::
    ConfigFramework.rst
    ConfigFramework.loaders.rst
    ConfigFramework.abstract.rst
    :maxdepth: 2

ConfigFramework
===============
.. |PyPI version| image:: https://img.shields.io/pypi/v/ConfigFramework
    :alt: PyPI version

.. |Python version| image:: https://img.shields.io/pypi/pyversions/ConfigFramework
    :alt: Python version

.. |PyPi downloads/m| image:: https://img.shields.io/pypi/dm/ConfigFramework
    :alt: PyPi downloads/m

.. |Issues| image:: https://img.shields.io/github/issues/Rud356/ConfigFramework
    :alt: Issues count



A small and simple framework to build your configs.

This project been created mostly because of me myself needing some simplistic
and at the same time powerful enough tool to create configs, validate them through have simple interface.

Installing
==========
Pypi link: https://pypi.org/project/ConfigFramework

``pip install ConfigFramework``

Example of usage
================

.. code-block:: python

    from ConfigFramework import loaders, variables, BaseConfig


    first_loader = loaders.JsonStringLoader.load('{"Is it simple?": true}', defaults={"useful?": "maybe", "pi": 2.74})
    second_loader = loaders.JsonStringLoader.load('{"Is it simple?": false, "Var": "value"}')
    composite_loader = loaders.CompositeLoader.load(first_loader, second_loader)


    class Config(BaseConfig):
        is_simple = variables.BoolVar("Is it simple?", first_loader)
        is_useful = variables.ConfigVar("useful?", first_loader, validator=lambda v: v == "maybe")
        pi = variables.FloatVar("pi", first_loader, default=3.14, constant=True, validator=lambda v: v == 3.14)

        class NestedConfig(BaseConfig):
            are_composite_loaders_simple = variables.BoolVar("Is it simple?", composite_loader)

            def __post_init__(self, *args, **kwargs):
                yes_or_no = 'Yes' if self.are_composite_loaders_simple.value else 'No'
                print(f"Is it simple to use composite loaders? {yes_or_no}")
                print("Nested config:", kwargs['phrase'])

        def __post_init__(self, *args, **kwargs):
            is_simple_to_str = 'simple' if self.is_simple.value else 'hard'
            print(f"ConfigFramework is {is_simple_to_str} and {self.is_useful.value} useful")
            print(f"Here's pi = {self.pi.value}")
            print("Main config:", kwargs['phrase'])

    config = Config(phrase="Here's a way to pass variables")

    try:
        print("pi is constant:", config.pi.is_constant)
        config.pi.value = 2.22

    except NotImplementedError:
        print("You can not set value to constants on runtime")

See examples with explanation `here <https://github.com/Rud356/ConfigFramework/blob/master/examples/>`_

Supported config formats
========================
- Yaml
- Json (strings or files)
- Environment variables
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
- Default values for per loader or per variable
- Translating one config loaders data to other (with or without including default values for each one)
- Composite loaders that allow you to define where to look up values using only one loader, that handles
  combining others


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
